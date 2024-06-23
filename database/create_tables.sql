-- Create file tracker table
CREATE TABLE mbna_file_tracker (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX (file_name)
);

-- Create Account table
CREATE TABLE mbna_account (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_number VARCHAR(100) NOT NULL,
    account_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    mbna_file_tracker_id INT,
    FOREIGN KEY (mbna_file_tracker_id) REFERENCES mbna_file_tracker(id) ON DELETE CASCADE
);

-- Create Statement table
CREATE TABLE mbna_statement (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_number VARCHAR(100),
    statement_period_start DATE,
    statement_period_end DATE,
    statement_date DATE,
    credit_limit DECIMAL(10, 2),
    cash_advance_limit DECIMAL(10, 2),
    previous_balance DECIMAL(10, 2),
    payments DECIMAL(10, 2),
    new_purchases DECIMAL(10, 2),
    balance_transfers DECIMAL(10, 2),
    cash_advances DECIMAL(10, 2),
    interest DECIMAL(10, 2),
    fees DECIMAL(10, 2),
    new_balance DECIMAL(10, 2),
    minimum_payment DECIMAL(10, 2),
    minimum_payment_due_date DATE,
    mbna_account_id INT,
    mbna_file_tracker_id INT,
    FOREIGN KEY (mbna_account_id) REFERENCES mbna_account(id) ON DELETE CASCADE,
    FOREIGN KEY (mbna_file_tracker_id) REFERENCES mbna_file_tracker(id) ON DELETE CASCADE
);

-- Create Transaction table
CREATE TABLE mbna_transaction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    statement_id INT,
    transaction_date DATE,
    posting_date DATE,
    description VARCHAR(255),
    amount DECIMAL(10, 2),
    mbna_file_tracker_id INT,
    FOREIGN KEY (statement_id) REFERENCES mbna_statement(id) ON DELETE CASCADE,
    FOREIGN KEY (mbna_file_tracker_id) REFERENCES mbna_file_tracker(id) ON DELETE CASCADE
);
