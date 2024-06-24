# scripts/extract_pdf.py
from pdfminer.high_level import extract_text
import re

def extract_data_from_pdf(file_path):
    text = extract_text(file_path)
    data = {}

    # Extract account details
    data['cardholder_name'] = re.search(r'Primary Cardholder:\s+(.*)', text).group(1)
    data['account_number'] = re.search(r'Account Number:\s+([\d\sX]+)', text).group(1).replace(' ', '')
    data['credit_limit'] = float(re.search(r'Credit Limit\s+\$([\d,\.]+)', text).group(1).replace(',', ''))
    data['cash_advance_limit'] = float(re.search(r'Cash Advance Limit\s+\$([\d,\.]+)', text).group(1).replace(',', ''))
    data['credit_available'] = float(re.search(r'Credit Available\s+\$([\d,\.]+)', text).group(1).replace(',', ''))
    data['cash_advance_available'] = float(re.search(r'Cash Advance Available\s+\$([\d,\.]+)', text).group(1).replace(',', ''))
    data['statement_closing_date'] = re.search(r'Statement Closing Date\s+(\d{2}/\d{2}/\d{2})', text).group(1)
    data['annual_interest_rate_purchases'] = float(re.search(r'Annual Interest Rate for Purchases\s+(\d{2}\.\d{2})%', text).group(1))
    data['annual_interest_rate_balance_transfers'] = float(re.search(r'Annual Interest Rate for Balance Transfers and Access Cheques\s+(\d{2}\.\d{2})%', text).group(1))
    data['annual_interest_rate_cash_advances'] = float(re.search(r'Annual Interest Rate for Cash Advances\s+(\d{2}\.\d{2})%', text).group(1))
    data['total_points'] = int(re.search(r'Your Total Points\s+(\d+)', text).group(1))

    # Extract transactions
    transactions = []
    transactions_section = re.search(r'Details of your transactions\n(.*?)\nSubtotal', text, re.DOTALL).group(1)
    for match in re.finditer(r'(\d{2}/\d{2}/\d{2})\s+(\d{2}/\d{2}/\d{2})\s+(.*?)\s+(\$[\d,\.]+)', transactions_section):
        transactions.append({
            'transaction_date': match.group(1),
            'posting_date': match.group(2),
            'description': match.group(3),
            'amount': float(match.group(4).replace('$', '').replace(',', ''))
        })
    data['transactions'] = transactions

    # Extract payments
    payments = []
    payments_section = re.search(r'PAYMENTS\n(.*?)\nTotal', text, re.DOTALL).group(1)
    for match in re.finditer(r'(\d{2}/\d{2}/\d{2})\s+(.*?)\s+(\$-[\d,\.]+)', payments_section):
        payments.append({
            'payment_date': match.group(1),
            'description': match.group(2),
            'amount': float(match.group(3).replace('$', '').replace(',', '').replace('-', ''))
        })
    data['payments'] = payments

    # Extract interest charges
    interest_charges = []
    interest_section = re.search(r'INTEREST CHARGED\n(.*?)\nTotal', text, re.DOTALL).group(1)
    for match in re.finditer(r'(\d{2}/\d{2}/\d{2})\s+INTEREST CHARGE\s+(\$[\d,\.]+)', interest_section):
        interest_charges.append({
            'charge_date': match.group(1),
            'amount': float(match.group(2).replace('$', '').replace(',', ''))
        })
    data['interest_charges'] = interest_charges

    # Extract fees
    fees = []
    fees_section = re.search(r'FEES CHARGED\n(.*?)\nTotal', text, re.DOTALL).group(1)
    for match in re.finditer(r'(\d{2}/\d{2}/\d{2})\s+(.*?)\s+(\$[\d,\.]+)', fees_section):
        fees.append({
            'fee_date': match.group(1),
            'fee_type': match.group(2),
            'amount': float(match.group(3).replace('$', '').replace(',', ''))
        })
    data['fees'] = fees

    # Extract payment plans
    payment_plans = []
    plans_section = re.search(r'Active Payment Plan\(s\)\n(.*?)\nTotal', text, re.DOTALL).group(1)
    for match in re.finditer(r'(.*?)\s+\$([\d,\.]+)\s+(\d{2}/\d{2}/\d{2})\s+(\d{2}/\d{2}/\d{2})\s+\$([\d,\.]+)\s+\$([\d,\.]+)', plans_section):
        payment_plans.append({
            'plan_name': match.group(1),
            'plan_balance': float(match.group(2).replace(',', '')),
            'start_date': match.group(3),
            'end_date': match.group(4),
            'plan_interest_rate': 0.00,
            'monthly_payment': float(match.group(6).replace(',', ''))
        })
    data['payment_plans'] = payment_plans

    return data
