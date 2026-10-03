CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    age INTEGER NOT NULL,
    gender VARCHAR(20) NOT NULL,
    city VARCHAR(100) NOT NULL,
    occupation VARCHAR(100) NOT NULL,
    annual_income NUMERIC(14,2) NOT NULL CHECK (annual_income > 0),
    customer_since DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR(20) PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    product_category VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS accounts (
    account_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL REFERENCES customers(customer_id),
    account_type VARCHAR(50) NOT NULL,
    opening_date DATE NOT NULL,
    balance NUMERIC(16,2) NOT NULL CHECK (balance >= 0),
    status VARCHAR(30) NOT NULL
);

CREATE TABLE IF NOT EXISTS customer_products (
    customer_id VARCHAR(20) NOT NULL REFERENCES customers(customer_id),
    product_id VARCHAR(20) NOT NULL REFERENCES products(product_id),
    start_date DATE NOT NULL,
    status VARCHAR(30) NOT NULL,
    PRIMARY KEY (customer_id, product_id)
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id VARCHAR(30) PRIMARY KEY,
    account_id VARCHAR(20) NOT NULL REFERENCES accounts(account_id),
    customer_id VARCHAR(20) NOT NULL REFERENCES customers(customer_id),
    transaction_date TIMESTAMP NOT NULL,
    transaction_type VARCHAR(20) NOT NULL,
    channel VARCHAR(50) NOT NULL,
    amount NUMERIC(16,2) NOT NULL CHECK (amount > 0),
    merchant_category VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    status VARCHAR(30) NOT NULL,
    transaction_day DATE,
    year_month VARCHAR(7),
    day_of_week VARCHAR(20),
    is_weekend BOOLEAN,
    transaction_hour SMALLINT
);

CREATE INDEX IF NOT EXISTS idx_accounts_customer ON accounts(customer_id);
CREATE INDEX IF NOT EXISTS idx_tx_account ON transactions(account_id);
CREATE INDEX IF NOT EXISTS idx_tx_customer ON transactions(customer_id);
CREATE INDEX IF NOT EXISTS idx_tx_date ON transactions(transaction_date);
CREATE INDEX IF NOT EXISTS idx_cp_customer ON customer_products(customer_id);
