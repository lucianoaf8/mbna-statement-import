import re
from PyPDF2 import PdfFileReader
from utils.logger import get_logger

logger = get_logger(__name__)

def extract_account_info(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PdfFileReader(file)
        content = reader.getPage(0).extract_text()
        
        cardholder_name = re.search(r'Primary Cardholder:\s*(.*)', content).group(1)
        account_number = re.search(r'Account Number:\s*(\d+ \d+ \d+ \d+)', content).group(1)
        credit_limit = float(re.search(r'Credit Limit\s*\$([\d,]+)', content).group(1).replace(',', ''))
        cash_advance_limit = credit_limit  # Assumed same as credit limit
        credit_available = float(re.search(r'Credit Available\s*\$([\d,]+)', content).group(1).replace(',', ''))
        cash_advance_available = credit_available  # Assumed same as credit available
        statement_closing_date = re.search(r'Statement Closing Date\s*(.*)', content).group(1)
        annual_interest_rate_purchases = float(re.search(r'Annual Interest Rate for Purchases\s*([\d.]+)%', content).group(1))
        annual_interest_rate_balance_transfers = float(re.search(r'Annual Interest Rate for Balance Transfers and Access Cheques\s*([\d.]+)%', content).group(1))
        annual_interest_rate_cash_advances = float(re.search(r'Annual Interest Rate for Cash Advances\s*([\d.]+)%', content).group(1))
        total_points = int(re.search(r'Your Total Points\s*(\d+)', content).group(1))

        logger.info("Extracted account information successfully")

        return {
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
