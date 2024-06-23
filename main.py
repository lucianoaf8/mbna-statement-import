import logging
from db_connection import connect_to_db
from load_files import load_files_from_directory
from extract_data import extract_data_from_pdf
from parse_data import (
    parse_account_number, parse_statement_period, parse_statement_date,
    parse_limits, parse_summary, parse_transactions
)
from insert_data import insert_data_into_db

# Set up logging
log_file_path = './logs/pdf_to_db.log'
logging.basicConfig(filename=log_file_path, level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s:%(message)s')

def main():
    connection = connect_to_db()
    if not connection:
        logging.error("Failed to connect to the database.")
        print("Failed to connect to the database.")
        return

    pdf_folder = "./pdf_statements"
    pdf_files = load_files_from_directory(pdf_folder)

    for file_path in pdf_files:
        try:
            text = extract_data_from_pdf(file_path)
            data = {
                "account_number": parse_account_number(text),
                "statement_period_start": parse_statement_period(text)[0],
                "statement_period_end": parse_statement_period(text)[1],
                "statement_date": parse_statement_date(text),
                "credit_limit": parse_limits(text)[0],
                "cash_advance_limit": parse_limits(text)[1],
                "previous_balance": parse_summary(text)[0],
                "payments": parse_summary(text)[1],
                "new_purchases": parse_summary(text)[2],
                "balance_transfers": parse_summary(text)[3],
                "cash_advances": parse_summary(text)[4],
                "interest": parse_summary(text)[5],
                "fees": parse_summary(text)[6],
                "new_balance": parse_summary(text)[7],
                "minimum_payment": parse_summary(text)[8],
                "minimum_payment_due_date": parse_summary(text)[9],
                "transactions": parse_transactions(text)
            }
            insert_data_into_db(file_path, data, connection)
        except Exception as e:
            logging.error(f"Failed to process {file_path}: {e}")
            print(f"Failed to process {file_path}: {e}")

    connection.close()

if __name__ == "__main__":
    main()
