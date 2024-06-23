import os
import mysql.connector
from mysql.connector import errorcode
import PyPDF2
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MYSQL_URL = os.getenv("MYSQL_URL")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")

# Establish database connection
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host=MYSQL_URL,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
        )
        return connection
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return None

# Extract data from PDF
def extract_data_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        number_of_pages = reader.getNumPages()
        text = ""
        for page_number in range(number_of_pages):
            page = reader.getPage(page_number)
            text += page.extract_text()
    
    # Parse the required fields from the text
    account_number = parse_account_number(text)
    statement_period_start, statement_period_end = parse_statement_period(text)
    statement_date = parse_statement_date(text)
    credit_limit, cash_advance_limit = parse_limits(text)
    previous_balance, payments, new_purchases, balance_transfers, cash_advances, interest, fees, new_balance, minimum_payment, minimum_payment_due_date = parse_summary(text)
    transactions = parse_transactions(text)

    return {
        "account_number": account_number,
        "statement_period_start": statement_period_start,
        "statement_period_end": statement_period_end,
        "statement_date": statement_date,
        "credit_limit": credit_limit,
        "cash_advance_limit": cash_advance_limit,
        "previous_balance": previous_balance,
        "payments": payments,
        "new_purchases": new_purchases,
        "balance_transfers": balance_transfers,
        "cash_advances": cash_advances,
        "interest": interest,
        "fees": fees,
        "new_balance": new_balance,
        "minimum_payment": minimum_payment,
        "minimum_payment_due_date": minimum_payment_due_date,
        "transactions": transactions
    }

# Parse functions
def parse_account_number(text):
    # Implement parsing logic here
    # Example parsing logic
    import re
    match = re.search(r'Account Number:\s+(\d{4} \d{2}XX XXXX \d{4})', text)
    return match.group(1) if match else None

def parse_statement_period(text):
    # Implement parsing logic here
    # Example parsing logic
    import re
    match = re.search(r'Statement Period:\s+(\d{2}/\d{2}/\d{2}) to (\d{2}/\d{2}/\d{2})', text)
    start_date = datetime.strptime(match.group(1), '%m/%d/%y').date() if match else None
    end_date = datetime.strptime(match.group(2), '%m/%d/%y').date() if match else None
    return start_date, end_date

def parse_statement_date(text):
    # Implement parsing logic here
    # Example parsing logic
    import re
    match = re.search(r'Statement Date:\s+(\d{2}/\d{2}/\d{2})', text)
    return datetime.strptime(match.group(1), '%m/%d/%y').date() if match else None

def parse_limits(text):
    # Implement parsing logic here
    # Example parsing logic
    import re
    credit_limit = None
    cash_advance_limit = None
    match = re.search(r'Credit Limit \$([0-9,]+\.\d{2})', text)
    if match:
        credit_limit = float(match.group(1).replace(',', ''))
    match = re.search(r'Cash Advance Limit \$([0-9,]+\.\d{2})', text)
    if match:
        cash_advance_limit = float(match.group(1).replace(',', ''))
    return credit_limit, cash_advance_limit

def parse_summary(text):
    # Implement parsing logic here
    # Example parsing logic
    import re
    previous_balance = payments = new_purchases = balance_transfers = cash_advances = interest = fees = new_balance = minimum_payment = None
    minimum_payment_due_date = None

    match = re.search(r'Previous Statement Balance \$([0-9,]+\.\d{2})', text)
    if match:
        previous_balance = float(match.group(1).replace(',', ''))
    match = re.search(r'Payments -\$([0-9,]+\.\d{2})', text)
    if match:
        payments = float(match.group(1).replace(',', ''))
    match = re.search(r'New Purchases \$([0-9,]+\.\d{2})', text)
    if match:
        new_purchases = float(match.group(1).replace(',', ''))
    match = re.search(r'Balance Transfers and Access Cheques \$([0-9,]+\.\d{2})', text)
    if match:
        balance_transfers = float(match.group(1).replace(',', ''))
    match = re.search(r'Cash Advances \$([0-9,]+\.\d{2})', text)
    if match:
        cash_advances = float(match.group(1).replace(',', ''))
    match = re.search(r'Interest \$([0-9,]+\.\d{2})', text)
    if match:
        interest = float(match.group(1).replace(',', ''))
    match = re.search(r'Fees \$([0-9,]+\.\d{2})', text)
    if match:
        fees = float(match.group(1).replace(',', ''))
    match = re.search(r'Your New Balance \$([0-9,]+\.\d{2})', text)
    if match:
        new_balance = float(match.group(1).replace(',', ''))
    match = re.search(r'Your Minimum Payment \$([0-9,]+\d{2})', text)
    if match:
        minimum_payment = float(match.group(1).replace(',', ''))
    match = re.search(r'Your Minimum Payment Due Date (\w+ \d{1,2}, \d{4})', text)
    if match:
        minimum_payment_due_date = datetime.strptime(match.group(1), '%B %d, %Y').date()
    
    return previous_balance, payments, new_purchases, balance_transfers, cash_advances, interest, fees, new_balance, minimum_payment, minimum_payment_due_date

def parse_transactions(text):
    # Implement parsing logic here
    # Example parsing logic
    import re
    transactions = []
    transaction_lines = re.findall(r'(\d{2}/\d{2}/\d{2})\s+(\d{2}/\d{2}/\d{2})\s+([^\d]+)\s+\d+\s+-?\$([0-9,]+\.\d{2})', text)
    for line in transaction_lines:
        transaction_date = datetime.strptime(line[0], '%m/%d/%y').date()
        posting_date = datetime.strptime(line[1], '%m/%d/%y').date()
        description = line[2].strip()
        amount = float(line[3].replace(',', ''))
        transactions.append({
            "transaction_date": transaction_date,
            "posting_date": posting_date,
            "description": description,
            "amount": amount
        })
    return transactions

# Insert data into database
def insert_data_into_db(file_name, data, connection):
    cursor = connection.cursor()
    try:
        # Check if the file is already processed
        cursor.execute("SELECT id FROM mbna_file_tracker WHERE file_name = %s", (file_name,))
        if cursor.fetchone():
            print(f"File {file_name} is already processed.")
            return
        
        # Insert into mbna_file_tracker
        add_file_tracker = ("INSERT INTO mbna_file_tracker (file_name, description) VALUES (%s, %s)")
        file_data = (file_name, "MBNA Statement")
        cursor.execute(add_file_tracker, file_data)
        file_tracker_id = cursor.lastrowid

        # Insert into mbna_account
        add_account = ("INSERT INTO mbna_account (account_number, account_name, mbna_file_tracker_id) VALUES (%s, %s, %s)")
        account_data = (data["account_number"], "Primary Cardholder", file_tracker_id)
        cursor.execute(add_account, account_data)
        account_id = cursor.lastrowid

        # Insert into mbna_statement
        add_statement = ("INSERT INTO mbna_statement (account_number, statement_period_start, statement_period_end, statement_date, credit_limit, cash_advance_limit, previous_balance, payments, new_purchases, balance_transfers, cash_advances, interest, fees, new_balance, minimum_payment, minimum_payment_due_date, mbna_account_id, mbna_file_tracker_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        statement_data = (data["account_number"], data["statement_period_start"], data["statement_period_end"], data["statement_date"], data["credit_limit"], data["cash_advance_limit"], data["previous_balance"], data["payments"], data["new_purchases"], data["balance_transfers"], data["cash_advances"], data["interest"], data["fees"], data["new_balance"], data["minimum_payment"], data["minimum_payment_due_date"], account_id, file_tracker_id)
        cursor.execute(add_statement, statement_data)
        statement_id = cursor.lastrowid

        # Insert into mbna_transaction
        add_transaction = ("INSERT INTO mbna_transaction (statement_id, transaction_date, posting_date, description, amount, mbna_file_tracker_id) VALUES (%s, %s, %s, %s, %s, %s)")
        for transaction in data["transactions"]:
            transaction_data = (statement_id, transaction["transaction_date"], transaction["posting_date"], transaction["description"], transaction["amount"], file_tracker_id)
            cursor.execute(add_transaction, transaction_data)
        
        # Commit the transaction
        connection.commit()
        print(f"Successfully processed {file_name}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        connection.rollback()
    finally:
        cursor.close()

# Main function
def main():
    connection = connect_to_db()
    if not connection:
        print("Failed to connect to the database.")
        return

    pdf_folder = "./pdf_statements"
    for file_name in os.listdir(pdf_folder):
        if file_name.endswith(".pdf"):
            file_path = os.path.join(pdf_folder, file_name)
            try:
                data = extract_data_from_pdf(file_path)
                insert_data_into_db(file_name, data, connection)
            except Exception as e:
                print(f"Failed to process {file_name}: {e}")

    connection.close()

if __name__ == "__main__":
    main()
