-- 1. Top customers by successful transaction value
SELECT customer_id, SUM(amount) AS total_transaction_value
FROM transactions
WHERE status = 'Success'
GROUP BY customer_id
ORDER BY total_transaction_value DESC
LIMIT 20;

-- 2. Monthly transaction trend
SELECT year_month, COUNT(*) AS transactions, SUM(amount) AS transaction_value
FROM transactions
WHERE status = 'Success'
GROUP BY year_month
ORDER BY year_month;

-- 3. Channel performance
SELECT channel, COUNT(*) AS transactions, SUM(amount) AS transaction_value, AVG(amount) AS avg_transaction
FROM transactions
WHERE status = 'Success'
GROUP BY channel
ORDER BY transaction_value DESC;

-- 4. Product adoption
SELECT p.product_name, p.product_category, COUNT(DISTINCT cp.customer_id) AS active_customers
FROM customer_products cp
JOIN products p ON p.product_id = cp.product_id
WHERE cp.status = 'Active'
GROUP BY p.product_name, p.product_category
ORDER BY active_customers DESC;

-- 5. Customers with multiple products
SELECT customer_id, COUNT(DISTINCT product_id) AS product_count
FROM customer_products
WHERE status = 'Active'
GROUP BY customer_id
HAVING COUNT(DISTINCT product_id) >= 3
ORDER BY product_count DESC;

-- 6. Balance by city
SELECT c.city, COUNT(DISTINCT c.customer_id) AS customers, SUM(a.balance) AS total_balance
FROM customers c
JOIN accounts a ON a.customer_id = c.customer_id
GROUP BY c.city
ORDER BY total_balance DESC;

-- 7. Transaction value by merchant category
SELECT merchant_category, COUNT(*) AS transactions, SUM(amount) AS transaction_value
FROM transactions
WHERE status = 'Success'
GROUP BY merchant_category
ORDER BY transaction_value DESC;

-- 8. Weekend vs weekday behavior
SELECT CASE WHEN is_weekend THEN 'Weekend' ELSE 'Weekday' END AS period,
       COUNT(*) AS transactions, SUM(amount) AS transaction_value
FROM transactions
WHERE status = 'Success'
GROUP BY period;

-- 9. High-value successful transactions above the 99th percentile
WITH cutoff AS (
    SELECT percentile_cont(0.99) WITHIN GROUP (ORDER BY amount) AS p99
    FROM transactions
    WHERE status = 'Success'
)
SELECT t.transaction_id, t.customer_id, t.amount, t.channel, t.location, t.transaction_date
FROM transactions t CROSS JOIN cutoff c
WHERE t.status = 'Success' AND t.amount >= c.p99
ORDER BY t.amount DESC;

-- 10. Dormant accounts with no recent transactions
SELECT a.account_id, a.customer_id, a.balance, a.status
FROM accounts a
LEFT JOIN transactions t
    ON t.account_id = a.account_id
    AND t.status = 'Success'
    AND t.transaction_date >= DATE '2025-04-01'
WHERE a.status = 'Dormant'
GROUP BY a.account_id, a.customer_id, a.balance, a.status
HAVING COUNT(t.transaction_id) = 0;
