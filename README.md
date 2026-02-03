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
    git clone https://github.com/mindexpert7546/Postgres-to-CSV.git
    cd Postgres-to-CSV
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Rename the project file `.env.example` to `.env` and set the following environment variables:

    ```env
    OE_DSN=OpenEdgeDSN
    OE_USER=dbuser
    OE_PASSWORD=dbpassword

    ```

## Usage

1. Run the script:

    ```bash
    python main.py
    ```

    This will connect to the PostgreSQL database, fetch data from the specified table, and export it to a CSV file (`output/tableName.csv`) in the project root. Image files will be saved in the `images` directory.

2. Customize SQL Query (Optional): Via QueryDetails.xlx

3. View the Output: In output folder followed by csv name in excel

# Alternate Approach : 
### 1. Install Python : https://www.python.org/downloads/
### 2. check version : 
```
 py --version
```
### 3. Download requirements
```
  py -m pip install -r requirements.txt
```

### 4. Download the Source Code : https://github.com/mindexpert7546/Postgres-to-CSV
### 5. Rename the project file .env.example to config.env and set the following environment variables
```
	OE_DSN=OpenEdgeDSN
	OE_USER=dbuser
	OE_PASSWORD=dbpassword
```

### 6. Fill the QueryDetails.xlsx

### 7. Run the script by : 
 ```
py main.py
```

### 8. Output : You can see the output in output folder

# How to verify the query via GUI : 

### 1. Download dbeaver : https://dbeaver.io/download/
### 2. Connect the DB and write the query 
#### This will connect to the PostgreSQL database, fetch data from the specified table, and export it to a CSV file (`output/tableName.csv`) in the project root. Image files will be saved in the `images` directory.

### 2. Customize SQL Query (Optional): Via QueryDetails.xlx

### 3. View the Output: In output folder followed by csv name in excel
