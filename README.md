## Overview

CSV Transaction Importer is a Python-based project designed to import transaction data from CSV files into a MySQL database. This project reads CSV files, extracts relevant transaction details, and inserts them into the database, ensuring that files are not imported more than once.

## Features

- **Environment Variable Management**: Uses `.env` file for sensitive information.
- **Logging**: Logs messages to track the progress of the script.
- **Database Interaction**: Connects to a MySQL database and performs CRUD operations.
- **CSV Parsing**: Reads and processes CSV files.
- **File Tracking**: Keeps track of imported files to avoid duplicate imports.

## Prerequisites

- Python 3.x
- MySQL server
- `pip` (Python package installer)

## Installation

1. **Clone the repository**:
    
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```
    
2. **Set up the virtual environment** (optional but recommended):
    
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
    
3. **Install the required packages**:
    
    ```bash
    pip install -r requirements.txt
    ```
    
4. **Create a `.env` file** in the project root directory with the following content:
    
    ```
    MYSQL_URL=mysql://<your_mysql_host>:<your_mysql_port>/<your_database_name>
    MYSQL_USER=<your_mysql_user>
    MYSQL_PASSWORD=<your_mysql_password>
    ```
    
5. **Set up the MySQL database**:
    - Use the provided `create_tables.sql` script to create the necessary tables in your MySQL database.

## Usage

1. **Place your CSV files**:
    - Ensure your CSV files are placed in the `data/csv_files` directory.
2. **Run the script**:
    
    ```bash
    python main.py
    ```
    

## File Structure

- `main.py`: The main script that handles CSV import and database interaction.
- `create_tables.sql`: SQL script to set up the necessary database tables.
- `requirements.txt`: List of dependencies required to run the project.

## Database Tables

The database consists of two main tables:

- `mbna_file_tracker`: Tracks the files that have been imported.
- `mbna_transactions`: Stores the transaction details extracted from the CSV files.

## Environment Variables

- `MYSQL_URL`: URL of the MySQL server.
- `MYSQL_USER`: MySQL username.
- `MYSQL_PASSWORD`: MySQL password.

## Dependencies

The project relies on the following Python packages, which are listed in `requirements.txt`:

- `python-dotenv`: To manage environment variables.
- `mysql-connector-python`: To interact with the MySQL database.