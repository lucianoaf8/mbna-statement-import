-- Create account table
CREATE TABLE mbna_accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cardholder_name VARCHAR(100),
    account_number VARCHAR(20),
    credit_limit DECIMAL(10, 2),
    cash_advance_limit DECIMAL(10, 2),
    statement_closing_date DATE,
    annual_interest_rate_purchases DECIMAL(5, 2),
    annual_interest_rate_balance_transfers DECIMAL(5, 2),
    annual_interest_rate_cash_advances DECIMAL(5, 2)
);

-- Create payment plans table
CREATE TABLE mbna_payment_plans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT,
    plan_name VARCHAR(100),
    annual_interest_rate DECIMAL(5, 2),
    plan_balance DECIMAL(10, 2),
    start_date DATE,
    end_date DATE,
    plan_interest_charges DECIMAL(5, 2),
    monthly_payment DECIMAL(10, 2),
    FOREIGN KEY (account_id) REFERENCES mbna_accounts(id)
);

-- Create file tracker table
CREATE TABLE mbna_file_tracker (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX (file_name)
);

-- Create transactions table
CREATE TABLE mbna_transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    file_id INT,
    account_id INT,
    posting_date DATE,
    payeee VARCHAR(255),
    adrdress VARCHAR(20),
    amount DECIMAL(10, 2),
    FOREIGN KEY (file_id) REFERENCES mbna_file_tracker(id) ON DELETE CASCADE,
    FOREIGN KEY (account_id) REFERENCES mbna_accounts(id) ON DELETE CASCADE
);

