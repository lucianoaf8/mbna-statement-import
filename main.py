import os
import csv
from datetime import datetime
from dotenv import load_dotenv
from urllib.parse import urlparse
import mysql.connector
from mysql.connector import errorcode

# Load environment variables from .env file
load_dotenv()

MYSQL_URL = os.getenv("MYSQL_URL")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")

# Set up logging
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

dbconfig = {
    "host": urlparse(MYSQL_URL).hostname,
    "port": urlparse(MYSQL_URL).port if urlparse(MYSQL_URL).port else 3306,
    "user": MYSQL_USER,
    "password": MYSQL_PASSWORD,
    "database": urlparse(MYSQL_URL).path.lstrip('/')
}

# Connect to the database
try:
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    print("Database connection successful!")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
    exit(1)

# Function to check if a file has already been imported
def file_already_imported(file_name):
    query = "SELECT COUNT(*) FROM mbna_file_tracker WHERE file_name = %s"
    cursor.execute(query, (file_name,))
    result = cursor.fetchone()
    return result[0] > 0

# Function to insert a file record into mbna_file_tracker
def insert_file_tracker(file_name, description):
    query = "INSERT INTO mbna_file_tracker (file_name, description) VALUES (%s, %s)"
    cursor.execute(query, (file_name, description))
    conn.commit()
    return cursor.lastrowid

# Function to insert transactions into mbna_transactions
def insert_transactions(file_id, transactions):
    query = """
    INSERT INTO mbna_transactions (file_id, account_id, posting_date, payeee, adrdress, amount)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(query, transactions)
    conn.commit()

# Function to extract account ID from file name
def extract_account_id(file_name):
    return int(file_name[-8:-4])

# Import CSV files from data/csv_files folder
csv_folder = 'data/csv_files'
for file_name in os.listdir(csv_folder):
    if file_name.endswith('.csv'):
        file_path = os.path.join(csv_folder, file_name)
        account_id = extract_account_id(file_name)

        # Check if the file has already been imported
        if file_already_imported(file_name):
            print(f"File {file_name} has already been imported. Skipping.")
            continue

        # Insert file record into mbna_file_tracker
        file_id = insert_file_tracker(file_name, file_path)

        # Read and insert transactions from the CSV file
        transactions = []
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                transaction = (
                    file_id,
                    account_id,
                    datetime.strptime(row['Posted Date'], '%m/%d/%Y').date(),
                    row['Payee'],
                    row['Address'],
                    float(row['Amount'])
                )
                transactions.append(transaction)

        # Insert transactions into mbna_transactions
        insert_transactions(file_id, transactions)
        print(f"Imported {file_name} successfully.")

# Close the database connection
cursor.close()
conn.close()
print("Database connection closed.")
