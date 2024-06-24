import os
from db.db_connection import create_connection
from utils.logger import get_logger
import mysql.connector

logger = get_logger(__name__)

def insert_data(query, data):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.executemany(query, data)
            connection.commit()
            logger.info(f"Inserted {cursor.rowcount} records into the database")
        except mysql.connector.Error as error:
            logger.error(f"Failed to insert record into table: {error}")
        finally:
            cursor.close()
            connection.close()

def insert_account_info(account_info, pdf_path):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO mbna_file_tracker (file_name, description) 
                VALUES (%s, %s)
            """, (os.path.basename(pdf_path), 'MBNA statement for account ' + account_info['account_number']))
            file_id = cursor.lastrowid
            
            query = """
            INSERT INTO mbna_accounts (
                file_id, cardholder_name, account_number, credit_limit, cash_advance_limit, credit_available, 
                cash_advance_available, statement_closing_date, annual_interest_rate_purchases, 
                annual_interest_rate_balance_transfers, annual_interest_rate_cash_advances, total_points
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            data = [
                (
                    file_id,
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
            logger.info(f"Inserted account information for {account_info['account_number']} from file {pdf_path}")
        except mysql.connector.Error as error:
            logger.error(f"Failed to insert account information: {error}")
        finally:
            cursor.close()
            connection.close()
