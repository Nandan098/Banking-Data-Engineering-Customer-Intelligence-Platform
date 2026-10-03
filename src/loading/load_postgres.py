from __future__ import annotations
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text


def load_processed_to_postgres(processed_dir: Path, db_url: str) -> None:
    """Load processed tables into PostgreSQL in FK-safe order.

    The database schema is defined in sql/schema.sql. This loader truncates the
    core tables before a full reload, which is appropriate for this portfolio project.
    """
    engine = create_engine(db_url, pool_pre_ping=True)
    files = [
        ("products", processed_dir / "products.csv"),
        ("customers", processed_dir / "customers.csv"),
        ("accounts", processed_dir / "accounts.csv"),
        ("customer_products", processed_dir / "customer_products.csv"),
        ("transactions", processed_dir / "transactions.csv"),
    ]
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE transactions, customer_products, accounts, customers, products RESTART IDENTITY CASCADE"))
    for table, path in files:
        df = pd.read_csv(path)
        df.to_sql(table, engine, if_exists="append", index=False, method="multi", chunksize=5000)
    engine.dispose()
