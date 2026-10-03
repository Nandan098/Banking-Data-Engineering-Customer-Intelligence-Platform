CREATE OR REPLACE VIEW vw_successful_transactions AS
SELECT * FROM transactions WHERE status = 'Success';

CREATE OR REPLACE VIEW vw_customer_transaction_summary AS
SELECT
    customer_id,
    COUNT(*) AS successful_transactions,
    SUM(amount) AS total_transaction_value,
    AVG(amount) AS average_transaction_value,
    MAX(transaction_date) AS last_transaction_date
FROM transactions
WHERE status = 'Success'
GROUP BY customer_id;

CREATE OR REPLACE VIEW vw_customer_balance_summary AS
SELECT
    customer_id,
    COUNT(*) AS total_accounts,
    COUNT(*) FILTER (WHERE status = 'Active') AS active_accounts,
    SUM(balance) AS total_balance,
    AVG(balance) AS average_balance
FROM accounts
GROUP BY customer_id;
