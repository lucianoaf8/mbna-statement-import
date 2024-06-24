# main.py
import os
from datetime import datetime
import logging
from scripts.extract_pdf import extract_data_from_pdf
from scripts.db_utils import connect, check_file_imported
from scripts.insert_data import (
    insert_file_tracker, insert_account, insert_transactions,
    insert_payments, insert_interest_charges, insert_fees, insert_payment_plans
)

# Set up logging for main.py
log_file = 'logs/main.log'
os.makedirs(os.path.dirname(log_file), exist_ok=True)
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s:%(message)s'
)

def main():
    logging.info('Script started.')
    
    pdf_directory = 'data/pdf_statements/'
    pdf_files = [os.path.join(pdf_directory, f) for f in os.listdir(pdf_directory) if f.lower().endswith('.pdf')]

    connection = connect()
    if not connection:
        logging.error('Failed to connect to the database.')
        return

    for file_path in pdf_files:
        file_name = os.path.basename(file_path)
        logging.info(f'Processing file: {file_name}')

        if check_file_imported(connection, file_name):
            logging.info(f'File {file_name} already imported.')
            continue

        try:
            data = extract_data_from_pdf(file_path)
            logging.info(f'Data extracted successfully from {file_name}')
        except Exception as e:
            logging.error(f'Error extracting data from {file_name}: {e}')
            continue

        try:
            file_id = insert_file_tracker(connection, file_name, 'MBNA Canada Amazon.ca Credit Card Statement')
            account_id = insert_account(connection, file_id, data)

            insert_transactions(connection, file_id, account_id, data['transactions'])
            insert_payments(connection, file_id, account_id, data['payments'])
            insert_interest_charges(connection, file_id, account_id, data['interest_charges'])
            insert_fees(connection, file_id, account_id, data['fees'])
            insert_payment_plans(connection, file_id, account_id, data['payment_plans'])

            logging.info(f'Successfully processed and inserted data from file: {file_name}')
        except Exception as e:
            logging.error(f'Error inserting data for {file_name}: {e}')

    logging.info('Script finished.')

if __name__ == "__main__":
    main()
