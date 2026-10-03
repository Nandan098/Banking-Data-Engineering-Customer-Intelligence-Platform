from pathlib import Path
import pandas as pd


def read_raw_data(raw_dir: Path) -> dict[str, pd.DataFrame]:
    """Read the five source tables without changing their business meaning."""
    return {
        "customers": pd.read_csv(raw_dir / "customers.csv", parse_dates=["customer_since"]),
        "accounts": pd.read_csv(raw_dir / "accounts.csv", parse_dates=["opening_date"]),
        "transactions": pd.read_csv(raw_dir / "transactions.csv", parse_dates=["transaction_date"]),
        "products": pd.read_csv(raw_dir / "products.csv"),
        "customer_products": pd.read_csv(
            raw_dir / "customer_products.csv", parse_dates=["start_date"]
        ),
    }
