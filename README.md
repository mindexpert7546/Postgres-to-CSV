# PostgreSQL Data Exporter

## Description
This Python script connects to a PostgreSQL database, fetches data from a specified table, and exports the data to a CSV file. Additionally, it saves images stored as base64 strings in the database to individual image files.

## Configuration

### Prerequisites
- Python 3.10 or higher
- PostgreSQL database with the required table
- Python packages listed in `requirements.txt`

### Installation
1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/your-repository.git
    cd your-repository
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Rename the project file `.env.example` to `.env` and set the following environment variables:

    ```env
    POSTGRES_DB=your_database_name
    POSTGRES_USER=your_database_user
    POSTGRES_PASSWORD=your_database_password
    POSTGRES_HOST=your_database_host
    POSTGRES_PORT=your_database_port

    PGADMIN_DEFAULT_EMAIL=xxx@example.com
    PGADMIN_DEFAULT_PASSWORD=xxx
    ```

## Usage

1. Run the script:

    ```bash
    python main.py
    ```

    This will connect to the PostgreSQL database, fetch data from the specified table, and export it to a CSV file (`output.csv`) in the project root. Image files will be saved in the `images` directory.

2. Customize SQL Query (Optional):

    Edit the SQL query in the `DataProcessor` class within `main.py` to fetch data based on your specific requirements:

    ```python
    # Customize your SQL query here
    cur.execute("SELECT * FROM your_schema.your_table")
    ```

    Replace `your_schema` and `your_table` with your specific schema and table names.

3. View the Output:

    The exported CSV file (`output.csv`) will contain the selected data columns. Image files will be saved in the `images` directory with filenames generated based on the first two columns of the fetched data.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
