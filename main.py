import base64
import csv
import os
import re
import uuid
from pathlib import Path
from typing import Any, List, Tuple

import psycopg2
from dotenv import load_dotenv
from openpyxl import load_workbook


# ================= PostgreSQL Connection =================

class PostgreSQLConnection:
    def __init__(self) -> None:
        self._load_env()
        self.params = {
            "database": os.getenv("POSTGRES_DB"),
            "user": os.getenv("POSTGRES_USER"),
            "password": os.getenv("POSTGRES_PASSWORD"),
            "host": os.getenv("POSTGRES_HOST"),
            "port": os.getenv("POSTGRES_PORT"),
        }

    def _load_env(self) -> None:
        base_dir = Path(__file__).resolve().parent
        load_dotenv(base_dir / ".env")

    def connect(self):
        return psycopg2.connect(**self.params)


# ================= Data Processor =================

class DataProcessor:
    def __init__(self, connection: PostgreSQLConnection) -> None:
        self.connection = connection
        os.makedirs("images", exist_ok=True)
        os.makedirs("output", exist_ok=True)

    def fetch_data(self, query: str) -> Tuple[List[Tuple], List[str]]:
        with self.connection.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return cur.fetchall(), [col[0] for col in cur.description]

    def export_to_csv(self, csv_name: str, columns: List[str], rows: List[Tuple]) -> None:
        csv_path = Path("output") / f"{csv_name}.csv"

        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(columns)

            for row in rows:
                writer.writerow([
                    self.process_cell(value, columns[idx])
                    for idx, value in enumerate(row)
                ])

        print(f"✅ CSV created: {csv_path}")

    def extract_table_names(self, query: str) -> str:
        tables = re.findall(
            r"(?:FROM|JOIN)\s+([a-zA-Z0-9_.\"]+)",
            query,
            flags=re.IGNORECASE
        )

        clean_tables = {
            t.replace('"', "").split(".")[-1]
            for t in tables
        }

        if not clean_tables:
            return "result"

        return "_".join(sorted(clean_tables))

    def process_cell(self, value: Any, column_name: str) -> str:
        if value is None:
            return ""

        if isinstance(value, (bytes, bytearray)):
            if self._is_real_image(value):
                return self._save_image(value, column_name)
            return value.hex()

        if isinstance(value, str) and value.startswith("data:image"):
            try:
                img_bytes = base64.b64decode(value.split(",", 1)[1])
                if self._is_real_image(img_bytes):
                    return self._save_image(img_bytes, column_name)
            except Exception:
                pass

        return str(value)

    def _is_real_image(self, img_bytes: bytes) -> bool:
        return (
            img_bytes.startswith(b"\x89PNG") or
            img_bytes.startswith(b"\xff\xd8\xff") or
            img_bytes.startswith(b"RIFF")
        )

    def _get_image_extension(self, img_bytes: bytes) -> str:
        if img_bytes.startswith(b"\x89PNG"):
            return "png"
        if img_bytes.startswith(b"\xff\xd8\xff"):
            return "jpg"
        if img_bytes.startswith(b"RIFF"):
            return "webp"
        return "bin"

    def _save_image(self, img_bytes: bytes, column_name: str) -> str:
        ext = self._get_image_extension(img_bytes)
        filename = f"{column_name}_{uuid.uuid4().hex}.{ext}"
        path = Path("images") / filename

        with open(path, "wb") as f:
            f.write(img_bytes)

        return str(path)


# ================= Excel Helper =================

def get_excel_file() -> Path:
    base_dir = Path(__file__).resolve().parent

    excel_files = [
        f for f in base_dir.glob("*.xlsx")
        if not f.name.startswith("~$")
    ]

    if not excel_files:
        raise FileNotFoundError(
            "❌ No valid Excel file found.\n"
            "✔ Place the Excel file next to main.py\n"
            "✔ Close Excel before running the script"
        )

    if len(excel_files) > 1:
        print("⚠ Multiple Excel files found. Using:", excel_files[0].name)

    return excel_files[0]

def get_unique_csv_name(base_name: str) -> str:
    """
    Returns a unique CSV name by adding _1, _2, etc. if needed
    """
    output_dir = Path("output")
    csv_path = output_dir / f"{base_name}.csv"

    if not csv_path.exists():
        return base_name

    counter = 1
    while True:
        new_name = f"{base_name}_{counter}"
        if not (output_dir / f"{new_name}.csv").exists():
            return new_name
        counter += 1

# ================= MAIN =================

def main():
    postgres = PostgreSQLConnection()
    processor = DataProcessor(postgres)

    excel_file = get_excel_file()
    print(f"📄 Using Excel file: {excel_file.name}")

    wb = load_workbook(excel_file)
    sheet = wb.active

    for row in range(2, sheet.max_row + 1):
        query = sheet[f"C{row}"].value
        csv_cell = sheet[f"D{row}"]

        if not query or csv_cell.value:
            continue

        # csv_name = processor.extract_table_names(query)
        base_csv_name = processor.extract_table_names(query)
        csv_name = get_unique_csv_name(base_csv_name)


        print(f"▶ Processing row {row}: {csv_name}")

        try:
            data, columns = processor.fetch_data(query)
            processor.export_to_csv(csv_name, columns, data)
            csv_cell.value = f"{csv_name}.csv"
        except Exception as e:
            csv_cell.value = f"ERROR: {str(e)}"

    wb.save(excel_file)
    print("🎯 Excel updated successfully")


if __name__ == "__main__":
    main()
