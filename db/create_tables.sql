-- Create file tracker table
CREATE TABLE mbna_file_tracker (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX (file_name)
);

-- Create account table
CREATE TABLE mbna_accounts (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    file_id INT,
    cardholder_name VARCHAR(100),
    account_number VARCHAR(20),
    credit_limit DECIMAL(10, 2),
    cash_advance_limit DECIMAL(10, 2),
    credit_available DECIMAL(10, 2),
    cash_advance_available DECIMAL(10, 2),
    statement_closing_date DATE,
    annual_interest_rate_purchases DECIMAL(5, 2),
    annual_interest_rate_balance_transfers DECIMAL(5, 2),
    annual_interest_rate_cash_advances DECIMAL(5, 2),
    total_points INT,
    FOREIGN KEY (file_id) REFERENCES mbna_file_tracker(id) ON DELETE CASCADE
);

-- Create transactions table
CREATE TABLE mbna_transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    file_id INT,
    account_id INT,
    transaction_date DATE,
    posting_date DATE,
    description VARCHAR(255),
    promotional_air VARCHAR(20),
    reference_number VARCHAR(20),
    amount DECIMAL(10, 2),
    FOREIGN KEY (file_id) REFERENCES mbna_file_tracker(id) ON DELETE CASCADE,
    FOREIGN KEY (account_id) REFERENCES mbna_accounts(account_id) ON DELETE CASCADE
);

-- Create payments table
CREATE TABLE mbna_payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    file_id INT,
    account_id INT,
    payment_date DATE,
    amount DECIMAL(10, 2),
    FOREIGN KEY (file_id) REFERENCES mbna_file_tracker(id) ON DELETE CASCADE,
    FOREIGN KEY (account_id) REFERENCES mbna_accounts(account_id) ON DELETE CASCADE
);

-- Create interest charges table
CREATE TABLE mbna_interest_charges (
    interest_id INT AUTO_INCREMENT PRIMARY KEY,
    file_id INT,
    account_id INT,
    charge_date DATE,
    amount DECIMAL(10, 2),
    FOREIGN KEY (file_id) REFERENCES mbna_file_tracker(id) ON DELETE CASCADE,
    FOREIGN KEY (account_id) REFERENCES mbna_accounts(account_id) ON DELETE CASCADE
);

-- Create fees table
CREATE TABLE mbna_fees (
    fee_id INT AUTO_INCREMENT PRIMARY KEY,
    file_id INT,
    account_id INT,
    fee_date DATE,
    amount DECIMAL(10, 2),
    fee_type VARCHAR(50),
    FOREIGN KEY (file_id) REFERENCES mbna_file_tracker(id) ON DELETE CASCADE,
    FOREIGN KEY (account_id) REFERENCES mbna_accounts(account_id) ON DELETE CASCADE
);

-- Create payment plans table
CREATE TABLE mbna_payment_plans (
    plan_id INT AUTO_INCREMENT PRIMARY KEY,
    file_id INT,
    account_id INT,
    plan_name VARCHAR(100),
    plan_balance DECIMAL(10, 2),
    start_date DATE,
    end_date DATE,
    plan_interest_rate DECIMAL(5, 2),
    monthly_payment DECIMAL(10, 2),
    FOREIGN KEY (file_id) REFERENCES mbna_file_tracker(id) ON DELETE CASCADE,
    FOREIGN KEY (account_id) REFERENCES mbna_accounts(account_id) ON DELETE CASCADE
);
