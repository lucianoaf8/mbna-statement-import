import os
from extractors.account_extractor import extract_account_info
from db.db_inserter import insert_account_info
from utils.logger import get_logger
from db.db_connection import create_connection

logger = get_logger(__name__)

def process_pdf(pdf_path):
    if not check_file_exists(pdf_path):
        logger.info(f"Processing file: {pdf_path}")
        account_info = extract_account_info(pdf_path)
        if account_info:
            insert_account_info(account_info, pdf_path)
        else:
            logger.error(f"Failed to extract account information from {pdf_path}")
    else:
        logger.info(f"File already processed: {pdf_path}")

def check_file_exists(pdf_path):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM mbna_file_tracker WHERE file_name = %s", (os.path.basename(pdf_path),))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result[0] > 0

if __name__ == "__main__":
    pdf_dir = 'pdf_statements'
    pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith('.pdf')]
    for pdf_file in pdf_files:
        process_pdf(os.path.join(pdf_dir, pdf_file))
