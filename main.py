import os
import glob
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import fitz  # PyMuPDF for reading PDF files

# Load environment variables
load_dotenv()

MYSQL_URL = os.getenv("MYSQL_URL")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB")

# Connect to the MySQL database
def create_connection():
    try:
        connection = mysql.connector.connect(
            host=MYSQL_URL,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB
        )
        if connection.is_connected():
            print("Connected to MySQL database")
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Check if the file has already been imported
def file_already_imported(cursor, file_name):
    query = "SELECT COUNT(*) FROM mbna_file_tracker WHERE file_name = %s"
    cursor.execute(query, (file_name,))
    return cursor.fetchone()[0] > 0

# Insert data into the mbna_file_tracker table
def insert_file_tracker(cursor, file_name, description):
    query = "INSERT INTO mbna_file_tracker (file_name, description) VALUES (%s, %s)"
    cursor.execute(query, (file_name, description))
    return cursor.lastrowid

# Insert data into the mbna_account table
def insert_account(cursor, account_number, account_name, file_tracker_id):
    query = "INSERT INTO mbna_account (account_number, account_name, mbna_file_tracker_id) VALUES (%s, %s, %s)"
    cursor.execute(query, (account_number, account_name, file_tracker_id))
    return cursor.lastrowid

# Insert data into the mbna_statement table
def insert_statement(cursor, statement_data, account_id, file_tracker_id):
    query = """
    INSERT INTO mbna_statement 
    (account_number, statement_period_start, statement_period_end, statement_date, 
    credit_limit, cash_advance_limit, previous_balance, payments, new_purchases, 
    balance_transfers, cash_advances, interest, fees, new_balance, minimum_payment, 
    minimum_payment_due_date, mbna_account_id, mbna_file_tracker_id) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (*statement_data, account_id, file_tracker_id))
    return cursor.lastrowid

# Insert data into the mbna_transaction table
def insert_transaction(cursor, transaction_data, statement_id, file_tracker_id):
    query = """
    INSERT INTO mbna_transaction 
    (statement_id, transaction_date, posting_date, description, amount, mbna_file_tracker_id) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (*transaction_data, statement_id, file_tracker_id))

# Extract data from PDF file
def extract_data_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    # Logic to extract data from the PDF
    # Placeholder for extracted data
    account_name = "LUCIANO ALMEIDA"
    account_number = "5234 41XX XXXX 2708"
    statement_data = (
        account_number, "2023-12-21", "2024-01-22", "2024-01-22", 
        8000.00, 8000.00, 7639.12, 50.00, 0.00, 0.00, 0.00, 0.00, 0.00, 7589.12, 10.00, "2024-02-15"
    )
    transactions = [
        ("2024-01-08", "2024-01-08", "PAYMENT", -50.00)
    ]
    return account_name, account_number, statement_data, transactions

def main():
    connection = create_connection()
    if connection is None:
        return

    cursor = connection.cursor()

    pdf_files = glob.glob("./pdf_statements/*.pdf")
    for pdf_file in pdf_files:
        file_name = os.path.basename(pdf_file)

        if file_already_imported(cursor, file_name):
            print(f"File {file_name} has already been imported.")
            continue

        account_name, account_number, statement_data, transactions = extract_data_from_pdf(pdf_file)
        file_tracker_id = insert_file_tracker(cursor, file_name, "Imported bank statement")

        account_id = insert_account(cursor, account_number, account_name, file_tracker_id)
        statement_id = insert_statement(cursor, statement_data, account_id, file_tracker_id)

        for transaction in transactions:
            insert_transaction(cursor, transaction, statement_id, file_tracker_id)

        connection.commit()
        print(f"Successfully imported {file_name}")

    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()
