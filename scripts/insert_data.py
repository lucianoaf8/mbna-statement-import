# scripts/insert_data.py
import os
import logging
from .db_utils import connect, check_file_imported

# Set up logging for insert_data.py
log_file = 'logs/insert_data.log'
os.makedirs(os.path.dirname(log_file), exist_ok=True)
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s:%(message)s'
)

def insert_file_tracker(connection, file_name, description):
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO mbna_file_tracker (file_name, description) VALUES (%s, %s)", (file_name, description))
        connection.commit()
        logging.info(f'Inserted file tracker for {file_name}')
        return cursor.lastrowid
    except Exception as e:
        logging.error(f'Error inserting file tracker for {file_name}: {e}')
        raise

def insert_account(connection, file_id, data):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO mbna_accounts (
                file_id, cardholder_name, account_number, credit_limit, cash_advance_limit, credit_available,
                cash_advance_available, statement_closing_date, annual_interest_rate_purchases,
                annual_interest_rate_balance_transfers, annual_interest_rate_cash_advances, total_points
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            file_id, data['cardholder_name'], data['account_number'], data['credit_limit'], data['cash_advance_limit'],
            data['credit_available'], data['cash_advance_available'], data['statement_closing_date'],
            data['annual_interest_rate_purchases'], data['annual_interest_rate_balance_transfers'],
            data['annual_interest_rate_cash_advances'], data['total_points']
        ))
        connection.commit()
        logging.info(f'Inserted account data for file ID {file_id}')
        return cursor.lastrowid
    except Exception as e:
        logging.error(f'Error inserting account data for file ID {file_id}: {e}')
        raise

def insert_transactions(connection, file_id, account_id, transactions):
    try:
        cursor = connection.cursor()
        for transaction in transactions:
            cursor.execute("""
                INSERT INTO mbna_transactions (
                    file_id, account_id, transaction_date, posting_date, description, amount
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                file_id, account_id, transaction['transaction_date'], transaction['posting_date'], transaction['description'],
                transaction['amount']
            ))
        connection.commit()
        logging.info(f'Inserted transactions for account ID {account_id}')
    except Exception as e:
        logging.error(f'Error inserting transactions for account ID {account_id}: {e}')
        raise

def insert_payments(connection, file_id, account_id, payments):
    try:
        cursor = connection.cursor()
        for payment in payments:
            cursor.execute("""
                INSERT INTO mbna_payments (
                    file_id, account_id, payment_date, amount
                ) VALUES (%s, %s, %s, %s)
            """, (
                file_id, account_id, payment['payment_date'], payment['amount']
            ))
        connection.commit()
        logging.info(f'Inserted payments for account ID {account_id}')
    except Exception as e:
        logging.error(f'Error inserting payments for account ID {account_id}: {e}')
        raise

def insert_interest_charges(connection, file_id, account_id, interest_charges):
    try:
        cursor = connection.cursor()
        for charge in interest_charges:
            cursor.execute("""
                INSERT INTO mbna_interest_charges (
                    file_id, account_id, charge_date, amount
                ) VALUES (%s, %s, %s, %s)
            """, (
                file_id, account_id, charge['charge_date'], charge['amount']
            ))
        connection.commit()
        logging.info(f'Inserted interest charges for account ID {account_id}')
    except Exception as e:
        logging.error(f'Error inserting interest charges for account ID {account_id}: {e}')
        raise

def insert_fees(connection, file_id, account_id, fees):
    try:
        cursor = connection.cursor()
        for fee in fees:
            cursor.execute("""
                INSERT INTO mbna_fees (
                    file_id, account_id, fee_date, amount, fee_type
                ) VALUES (%s, %s, %s, %s, %s)
            """, (
                file_id, account_id, fee['fee_date'], fee['amount'], fee['fee_type']
            ))
        connection.commit()
        logging.info(f'Inserted fees for account ID {account_id}')
    except Exception as e:
        logging.error(f'Error inserting fees for account ID {account_id}: {e}')
        raise

def insert_payment_plans(connection, file_id, account_id, payment_plans):
    try:
        cursor = connection.cursor()
        for plan in payment_plans:
            cursor.execute("""
                INSERT INTO mbna_payment_plans (
                    file_id, account_id, plan_name, plan_balance, start_date, end_date, plan_interest_rate, monthly_payment
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                file_id, account_id, plan['plan_name'], plan['plan_balance'], plan['start_date'], plan['end_date'],
                plan['plan_interest_rate'], plan['monthly_payment']
            ))
        connection.commit()
        logging.info(f'Inserted payment plans for account ID {account_id}')
    except Exception as e:
        logging.error(f'Error inserting payment plans for account ID {account_id}: {e}')
        raise
