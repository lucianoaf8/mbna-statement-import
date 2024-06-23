from PyPDF2.errors import PdfReadError
from PyPDF2 import PdfReader
import logging
from parsers import parse_account_number, parse_statement_period, parse_statement_date, parse_limits, parse_summary, parse_transactions

def extract_data_from_pdf(file_path):
    try:
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            text = ""
            for page_num, page in enumerate(reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text
                    else:
                        logging.warning(f"No text extracted from page {page_num} in file {file_path}")
                        print(f"No text extracted from page {page_num} in file {file_path}")
                except PdfReadError as e:
                    logging.warning(f"Error reading page {page_num} in file {file_path}: {e}")
                    print(f"Error reading page {page_num} in file {file_path}: {e}")
                    continue  # Skip the problematic page
        
        # If no text could be extracted at all, raise an error
        if not text.strip():
            raise ValueError("No text could be extracted from the PDF.")

        # Clean and normalize text
        text = clean_text(text)
        
        # Parse the required fields from the text
        account_number = parse_account_number(text)
        if not account_number:
            raise ValueError("Account number not found in the PDF.")
        statement_period_start, statement_period_end = parse_statement_period(text)
        statement_date = parse_statement_date(text)
        credit_limit, cash_advance_limit = parse_limits(text)
        summary_data = parse_summary(text)
        transactions = parse_transactions(text)

        logging.debug(f"Extracted data from PDF: {file_path}")
        print(f"Extracted data from PDF: {file_path}")
        return {
            "account_number": account_number,
            "statement_period_start": statement_period_start,
            "statement_period_end": statement_period_end,
            "statement_date": statement_date,
            "credit_limit": credit_limit,
            "cash_advance_limit": cash_advance_limit,
            **summary_data,
            "transactions": transactions
        }
    except PdfReadError as e:
        logging.error(f"Error extracting data from PDF {file_path}: {e}")
        print(f"Error extracting data from PDF {file_path}: {e}")
        return None
    except Exception as e:
        logging.error(f"Error extracting data from PDF {file_path}: {e}")
        print(f"Error extracting data from PDF {file_path}: {e}")
        return None

def clean_text(text):
    # Implement text cleaning to handle special characters, spaces, etc.
    return ' '.join(text.split())
