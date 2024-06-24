import re
from PyPDF2 import PdfReader
from utils.logger import get_logger

logger = get_logger(__name__)

def extract_account_info(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            content = reader.pages[0].extract_text()
            
            cardholder_name = re.search(r'Primary Cardholder:\s*(.*)', content)
            cardholder_name = cardholder_name.group(1) if cardholder_name else None

            account_number = re.search(r'Account Number:\s*(\d+ \d+ \d+ \d+)', content)
            account_number = account_number.group(1) if account_number else None

            credit_limit = re.search(r'Credit Limit\s*\$([\d,]+)', content)
            credit_limit = float(credit_limit.group(1).replace(',', '')) if credit_limit else None

            cash_advance_limit = re.search(r'Cash Advance Limit\s*\$([\d,]+)', content)
            cash_advance_limit = float(cash_advance_limit.group(1).replace(',', '')) if cash_advance_limit else None

            credit_available = re.search(r'Credit Available\s*\$([\d,]+)', content)
            credit_available = float(credit_available.group(1).replace(',', '')) if credit_available else None

            cash_advance_available = re.search(r'Cash Advance Available\s*\$([\d,]+)', content)
            cash_advance_available = float(cash_advance_available.group(1).replace(',', '')) if cash_advance_available else None

            statement_closing_date = re.search(r'Statement Closing Date\s*(.*)', content)
            statement_closing_date = statement_closing_date.group(1) if statement_closing_date else None

            annual_interest_rate_purchases = re.search(r'Annual Interest Rate for Purchases\s*([\d.]+)%', content)
            annual_interest_rate_purchases = float(annual_interest_rate_purchases.group(1)) if annual_interest_rate_purchases else None

            annual_interest_rate_balance_transfers = re.search(r'Annual Interest Rate for Balance Transfers and Access Cheques\s*([\d.]+)%', content)
            annual_interest_rate_balance_transfers = float(annual_interest_rate_balance_transfers.group(1)) if annual_interest_rate_balance_transfers else None

            annual_interest_rate_cash_advances = re.search(r'Annual Interest Rate for Cash Advances\s*([\d.]+)%', content)
            annual_interest_rate_cash_advances = float(annual_interest_rate_cash_advances.group(1)) if annual_interest_rate_cash_advances else None

            total_points = re.search(r'Your Total Points\s*(\d+)', content)
            total_points = int(total_points.group(1)) if total_points else None

            logger.info("Extracted account information successfully from %s", pdf_path)

            account_info = {
                'cardholder_name': cardholder_name,
                'account_number': account_number,
                'credit_limit': credit_limit,
                'cash_advance_limit': cash_advance_limit,
                'credit_available': credit_available,
                'cash_advance_available': cash_advance_available,
                'statement_closing_date': statement_closing_date,
                'annual_interest_rate_purchases': annual_interest_rate_purchases,
                'annual_interest_rate_balance_transfers': annual_interest_rate_balance_transfers,
                'annual_interest_rate_cash_advances': annual_interest_rate_cash_advances,
                'total_points': total_points
            }

            print("Extracted account information for:", account_info)
            return account_info

    except Exception as e:
        logger.error("Failed to extract account information from %s: %s", pdf_path, str(e))
        print(f"Failed to extract account information from {pdf_path}: {str(e)}")
        return None
