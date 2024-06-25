import logging
import os
from utils.convert_pdf_to_csv import convert_pdf_to_csv
from extractors.account_extractor import extract_account_info_from_csv
from db.db_inserter import insert_account_info

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(pdf_paths):
    for pdf_path in pdf_paths:
        try:
            # Ensure the converted_files directory exists
            if not os.path.exists("converted_files"):
                os.makedirs("converted_files")
            
            # Define CSV file path
            csv_path = os.path.join("converted_files", os.path.basename(pdf_path).replace(".PDF", ".csv"))
            
            # Convert PDF to CSV
            convert_pdf_to_csv(pdf_path, csv_path)
            
            # Extract account information from CSV
            account_info = extract_account_info_from_csv(csv_path)
            if not account_info:
                raise ValueError("No account information could be extracted.")

            insert_account_info(account_info, pdf_path)
            logger.info(f"Processing completed successfully for file {pdf_path}")

        except Exception as e:
            logger.error(f"Failed to process file {pdf_path}: {str(e)}")
            print(f"Failed to process file {pdf_path}: {str(e)}")

if __name__ == "__main__":
    pdf_paths = ["pdf_statements/Amazon_23May2024.PDF"]  # List all your PDF files here
    main(pdf_paths)
