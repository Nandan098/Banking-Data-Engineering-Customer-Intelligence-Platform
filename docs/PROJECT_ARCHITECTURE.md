# Project Architecture

```text
                    SYNTHETIC BANKING DATA
                              |
             +----------------+----------------+
             |                |                |
         Customers         Accounts        Products
             |                |                |
             +--------- Customer Products -----+
                              |
                        Transactions
                              |
                              v
                    Python Ingestion Layer
                              |
                              v
                  Transformation / Cleaning
                              |
                              v
                    Data Quality Framework
                    /      |       |       \
              schema   nulls   keys   chronology
                              |
                              v
                         PostgreSQL
                              |
             +----------------+----------------+
             |                                 |
             v                                 v
       Customer 360                       SQL Analytics
             |
             v
       ML Segmentation
             |
             v
      Power BI Ready Tables
             |
             v
       Power BI Dashboard

Airflow orchestrates the stages and Pytest covers unit/data checks.
```

## Design decisions

1. Raw files remain immutable inputs; processed files are generated outputs.
2. Data quality gates run before analytical outputs are published.
3. PostgreSQL is the relational serving layer for the portfolio project.
4. Customer 360 is a customer-level feature store for analytics and clustering.
5. ML is intentionally downstream of data engineering so the project demonstrates the role's pipeline/quality requirements first.
6. All customer and transaction data are synthetic; no real bank PII is used.
