import re
from datetime import datetime

def parse_account_number(text):
    match = re.search(r'Account Number:\s+(\d{4} \d{2}XX XXXX \d{4})', text)
    return match.group(1) if match else None

def parse_statement_period(text):
    match = re.search(r'Statement Period:\s+(\d{2}/\d{2}/\d{2}) to (\d{2}/\d{2}/\d{2})', text)
    start_date = datetime.strptime(match.group(1), '%m/%d/%y').date() if match else None
    end_date = datetime.strptime(match.group(2), '%m/%d/%y').date() if match else None
    return start_date, end_date

def parse_statement_date(text):
    match = re.search(r'Statement Date:\s+(\d{2}/\d{2}/\d{2})', text)
    return datetime.strptime(match.group(1), '%m/%d/%y').date() if match else None

def parse_limits(text):
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
