import base64
import csv
import os
import re
from pathlib import Path
from typing import Any, List, Tuple

import psycopg2
from dotenv import load_dotenv


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

    # ---------- Read SQL File ----------
    def read_query(self, sql_file: str) -> str:
        with open(sql_file, "r", encoding="utf-8") as f:
            return f.read()

    # ---------- Extract Table Names (CSV Naming) ----------
    def extract_table_names(self, query: str) -> str:
        tables = re.findall(
            r"(?:FROM|JOIN)\s+([a-zA-Z0-9_.\"]+)",
            query,
            re.IGNORECASE
        )

        clean_tables = {
            t.replace('"', "").split(".")[-1]
            for t in tables
        }

        return "_".join(sorted(clean_tables)) if clean_tables else "result"

    # ---------- Execute Query ----------
    def fetch_data(self, query: str) -> Tuple[List[Tuple], List[str]]:
        with self.connection.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return cur.fetchall(), [col[0] for col in cur.description]

    # ---------- Export CSV ----------
    def export_to_csv(self, table_name: str, columns: List[str], rows: List[Tuple]) -> None:
        csv_file = f"output/{table_name}.csv"

        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(columns)

            for row in rows:
                writer.writerow([
                    self.process_cell(value, columns[idx])
                    for idx, value in enumerate(row)
                ])

        print(f"✅ CSV created: {csv_file}")

    # ---------- Process Each Cell (SAFE) ----------
    def process_cell(self, value: Any, column_name: str) -> str:
        if value is None:
            return ""

        # BYTEA / BLOB
        if isinstance(value, (bytes, bytearray)):
            if self._is_real_image(value):
                return self._save_image(value, column_name)
            return value.hex()  # safe fallback

        # STRING (possible base64 image)
        if isinstance(value, str):
            if value.startswith("data:image"):
                try:
                    img_bytes = base64.b64decode(value.split(",", 1)[1])
                    if self._is_real_image(img_bytes):
                        return self._save_image(img_bytes, column_name)
                except Exception:
                    pass
            return value  # normal text

        return str(value)

    # ---------- REAL Image Validation ----------
    def _is_real_image(self, img_bytes: bytes) -> bool:
        return (
            img_bytes.startswith(b"\x89PNG") or       # PNG
            img_bytes.startswith(b"\xff\xd8\xff") or  # JPG/JPEG
            img_bytes.startswith(b"RIFF")             # WEBP
        )

    # ---------- Save Image ----------
    def _save_image(self, img_bytes: bytes, column_name: str) -> str:
        filename = f"images/{column_name}_{len(os.listdir('images')) + 1}.png"
        with open(filename, "wb") as f:
            f.write(img_bytes)
        return filename


# ================= Main =================

def main():
    postgres = PostgreSQLConnection()
    processor = DataProcessor(postgres)

    # Read large query from file
    query = processor.read_query("query.sql")

    # CSV file name from table(s)
    table_name = processor.extract_table_names(query)

    data, columns = processor.fetch_data(query)
    processor.export_to_csv(table_name, columns, data)


if __name__ == "__main__":
    main()
