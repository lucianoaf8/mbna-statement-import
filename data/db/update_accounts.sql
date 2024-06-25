UPDATE mbna_accounts
SET credit_available = 0,
    cash_advance_available = 0,
    statement_closing_date = '2024-12-30'
WHERE account_number = 0000;
