import os
from extractors.account_extractor import extract_account_info
from db.db_inserter import insert_data
from utils.logger import get_logger

logger = get_logger(__name__)

def process_pdf(pdf_path):
    if not check_file_exists(pdf_path):
        account_info = extract_account_info(pdf_path)
        insert_account_info(account_info, pdf_path)
        logger.info("Processed file: %s", pdf_path)
    else:
        logger.info("File already processed: %s", pdf_path)

def check_file_exists(pdf_path):
    # Logic to check if file has already been processed (implement as needed)
    return False

def insert_account_info(account_info, pdf_path):
    # Example query and data insertion
    query = """
    INSERT INTO mbna_accounts (
        file_id, cardholder_name, account_number, credit_limit, cash_advance_limit, credit_available, 
        cash_advance_available, statement_closing_date, annual_interest_rate_purchases, 
        annual_interest_rate_balance_transfers, annual_interest_rate_cash_advances, total_points
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    data = [
        (
            1,  # Example file_id, should be obtained by checking the file tracker
            account_info['cardholder_name'],
            account_info['account_number'],
            account_info['credit_limit'],
            account_info['cash_advance_limit'],
            account_info['credit_available'],
            account_info['cash_advance_available'],
            account_info['statement_closing_date'],
            account_info['annual_interest_rate_purchases'],
            account_info['annual_interest_rate_balance_transfers'],
            account_info['annual_interest_rate_cash_advances'],
            account_info['total_points']
        )
    ]
    insert_data(query, data)

if __name__ == "__main__":
    pdf_files = [f for f in os.listdir('path/to/pdf/files') if f.endswith('.pdf')]
    for pdf_file in pdf_files:
        process_pdf(os.path.join('path/to/pdf/files', pdf_file))
