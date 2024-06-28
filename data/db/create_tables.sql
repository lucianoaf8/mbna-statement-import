/*
mbna_accounts
    Table Description: Table to store account information for MBNA cardholders, including details about credit limits, available credit, and interest rates.
Examples:
    id=1
    cardholder_name='Luciano Almeida'
    account_number='1139'
    credit_limit=5200.00
    cash_advance_limit=5200.00
    credit_available=0.00
    cash_advance_available=0.00
    statement_closing_date='2024-06-24'
    annual_interest_rate_purchases=19.99
    annual_interest_rate_balance_transfers=22.99
    annual_interest_rate_cash_advances=22.99
*/
CREATE TABLE mbna_accounts (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Unique identifier for each account
    cardholder_name VARCHAR(100), -- Name of the cardholder
    account_number VARCHAR(20), -- Account number of the cardholder
    credit_limit DECIMAL(10, 2), -- Total credit limit for the account
    cash_advance_limit DECIMAL(10, 2), -- Total cash advance limit for the account
    credit_available DECIMAL(10, 2), -- Available credit for purchases
    cash_advance_available DECIMAL(10, 2), -- Available credit for cash advances
    statement_closing_date DATE, -- Date when the statement closes
    annual_interest_rate_purchases DECIMAL(5, 2), -- Annual interest rate for purchases
    annual_interest_rate_balance_transfers DECIMAL(5, 2), -- Annual interest rate for balance transfers
    annual_interest_rate_cash_advances DECIMAL(5, 2) -- Annual interest rate for cash advances
);

/*
mbna_payment_plans
    Table Description: Table to store payment plans associated with accounts, including details about interest rates, balances, and payment schedules.
Examples:
    id=1
    account_id=1
    plan_name='Balance Transfer Plan'
    annual_interest_rate=15.99
    plan_balance=1000.00
    start_date='2024-01-01'
    end_date='2025-01-01'
    plan_interest_charges=150.00
    monthly_payment=85.00
*/
CREATE TABLE mbna_payment_plans (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Unique identifier for each payment plan
    account_id INT, -- Foreign key referencing mbna_accounts(id)
    plan_name VARCHAR(100), -- Name of the payment plan
    annual_interest_rate DECIMAL(5, 2), -- Annual interest rate for the plan
    plan_balance DECIMAL(10, 2), -- Current balance of the plan
    start_date DATE, -- Start date of the plan
    end_date DATE, -- End date of the plan
    plan_interest_charges DECIMAL(5, 2), -- Interest charges for the plan
    monthly_payment DECIMAL(10, 2), -- Monthly payment amount
    FOREIGN KEY (account_id) REFERENCES mbna_accounts(id) -- Foreign key constraint
);

/*
mbna_file_tracker
    Table Description: Table to track file imports, including metadata about the imported files such as their name, description, and the timestamp when they were imported.
Examples:
    id=1
    file_name='April2024_1139.csv'
    description='data/csv_files\\April2024_1139.csv'
    created_at='2024-06-25 17:11:10'
*/
CREATE TABLE mbna_file_tracker (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Unique identifier for the file import record
    file_name VARCHAR(255) NOT NULL, -- Name of the imported file
    description TEXT, -- Description of the file
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp when the record was created
    INDEX (file_name) -- Index on the file_name column
);

/*
mbna_transactions
    Table Description: Table to store transaction details, including information about the associated file, account, and transaction specifics such as posting date, payee, and amount.
Examples:
    transaction_id=1
    file_id=1
    account_id=1139
    posting_date='2024-04-01'
    payeee='PAYMENT'
    adrdress=''
    amount=400.00
*/
CREATE TABLE mbna_transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY, -- Unique identifier for each transaction
    file_id INT, -- Foreign key referencing mbna_file_tracker(id)
    account_id INT, -- Foreign key referencing mbna_accounts(id)
    posting_date DATE, -- Date the transaction was posted
    payeee VARCHAR(255), -- Name of the payee
    adrdress VARCHAR(20), -- Address related to the transaction
    amount DECIMAL(10, 2), -- Amount of the transaction
    FOREIGN KEY (file_id) REFERENCES mbna_file_tracker(id) ON DELETE CASCADE -- Foreign key constraint with cascade delete
);
