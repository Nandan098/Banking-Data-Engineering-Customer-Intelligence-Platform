# Data Model

## customers
One row per synthetic customer.

Primary key: `customer_id`

## accounts
One row per bank account.

Primary key: `account_id`
Foreign key: `customer_id -> customers.customer_id`

## transactions
One row per transaction.

Primary key: `transaction_id`
Foreign keys: `account_id`, `customer_id`

`customer_id` is intentionally retained as a denormalized analytical reference in the source data; the account relationship is validated so the two references stay consistent.

## products
Banking product catalog.

Primary key: `product_id`

## customer_products
Many-to-many relationship between customers and products.

Composite primary key: `customer_id, product_id`
