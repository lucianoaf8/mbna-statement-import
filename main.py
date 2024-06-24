# main.py
import os
from scripts.extract_pdf import extract_data_from_pdf
from scripts.db_utils import connect, check_file_imported
from scripts.insert_data import (
    insert_file_tracker, insert_account, insert_transactions,
    insert_payments, insert_interest_charges, insert_fees, insert_payment_plans
)

def main():
    log_file = 'logs/process.log'
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    pdf_files = ['../data/Amazon_23May2024.PDF']  # List PDF files here

    connection = connect()
    if not connection:
        with open(log_file, 'a') as log:
            log.write('Failed to connect to the database.\n')
        return

    for file_path in pdf_files:
        file_name = os.path.basename(file_path)
        with open(log_file, 'a') as log:
            log.write(f'Processing file: {file_name}\n')

        if check_file_imported(connection, file_name):
            with open(log_file, 'a') as log:
                log.write(f'File {file_name} already imported.\n')
            continue

        data = extract_data_from_pdf(file_path)
        file_id = insert_file_tracker(connection, file_name, 'MBNA Canada Amazon.ca Credit Card Statement')
        account_id = insert_account(connection, file_id, data)

        insert_transactions(connection, file_id, account_id, data['transactions'])
        insert_payments(connection, file_id, account_id, data['payments'])
        insert_interest_charges(connection, file_id, account_id, data['interest_charges'])
        insert_fees(connection, file_id, account_id, data['fees'])
        insert_payment_plans(connection, file_id, account_id, data['payment_plans'])

        with open(log_file, 'a') as log:
            log.write(f'Successfully processed and inserted data from file: {file_name}\n')

if __name__ == "__main__":
    main()
