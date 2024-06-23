import logging
import mysql.connector

def insert_data_into_db(file_name, data, connection):
    cursor = connection.cursor()
    try:
        # Check if the file is already processed
        cursor.execute("SELECT id FROM mbna_file_tracker WHERE file_name = %s", (file_name,))
        if cursor.fetchone():
            logging.info(f"File {file_name} is already processed.")
            print(f"File {file_name} is already processed.")
            return
        
        # Insert into mbna_file_tracker
        add_file_tracker = ("INSERT INTO mbna_file_tracker (file_name, description) VALUES (%s, %s)")
        file_data = (file_name, "MBNA Statement")
        cursor.execute(add_file_tracker, file_data)
        file_tracker_id = cursor.lastrowid

        # Insert into mbna_account
        add_account = ("INSERT INTO mbna_account (account_number, account_name, mbna_file_tracker_id) VALUES (%s, %s, %s)")
        account_data = (data["account_number"], "Primary Cardholder", file_tracker_id)
        cursor.execute(add_account, account_data)
        account_id = cursor.lastrowid

        # Insert into mbna_statement
        add_statement = ("INSERT INTO mbna_statement (account_number, statement_period_start, statement_period_end, statement_date, credit_limit, cash_advance_limit, previous_balance, payments, new_purchases, balance_transfers, cash_advances, interest, fees, new_balance, minimum_payment, minimum_payment_due_date, mbna_account_id, mbna_file_tracker_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        statement_data = (
            data["account_number"], data["statement_period_start"], data["statement_period_end"], 
            data["statement_date"], data["credit_limit"], data["cash_advance_limit"], 
            data["previous_balance"], data["payments"], data["new_purchases"], 
            data["balance_transfers"], data["cash_advances"], data["interest"], data["fees"], 
            data["new_balance"], data["minimum_payment"], data["minimum_payment_due_date"], 
            account_id, file_tracker_id
        )
        cursor.execute(add_statement, statement_data)
        statement_id = cursor.lastrowid

        # Insert into mbna_transaction
        add_transaction = ("INSERT INTO mbna_transaction (statement_id, transaction_date, posting_date, description, amount, mbna_file_tracker_id) VALUES (%s, %s, %s, %s, %s, %s)")
        for transaction in data["transactions"]:
            transaction_data = (statement_id, transaction["transaction_date"], transaction["posting_date"], transaction["description"], transaction["amount"], file_tracker_id)
            cursor.execute(add_transaction, transaction_data)
        
        # Commit the transaction
        connection.commit()
        logging.info(f"Successfully processed {file_name}")
        print(f"Successfully processed {file_name}")
    except mysql.connector.Error as err:
        logging.error(f"Database insertion error for file {file_name}: {err}")
        print(f"Database insertion error for file {file_name}: {err}")
        connection.rollback()
    finally:
        cursor.close()
