# mbna_accounts
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

# mbna_payment_plans
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

# mbna_file_tracker
CREATE TABLE mbna_file_tracker (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Unique identifier for the file import record
    file_name VARCHAR(255) NOT NULL, -- Name of the imported file
    description TEXT, -- Description of the file
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp when the record was created
    INDEX (file_name) -- Index on the file_name column
);

# mbna_transactions
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
