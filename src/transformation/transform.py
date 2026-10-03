from __future__ import annotations
import pandas as pd


def _clean_text(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    out = df.copy()
    for col in columns:
        if col in out.columns:
            out[col] = out[col].astype("string").str.strip()
    return out


def transform_customers(df: pd.DataFrame) -> pd.DataFrame:
    out = _clean_text(df, ["customer_id", "gender", "city", "occupation"])
    out["age"] = pd.to_numeric(out["age"], errors="coerce").astype("Int64")
    out["annual_income"] = pd.to_numeric(out["annual_income"], errors="coerce")
    out["customer_since"] = pd.to_datetime(out["customer_since"], errors="coerce")
    return out


def transform_accounts(df: pd.DataFrame) -> pd.DataFrame:
    out = _clean_text(df, ["account_id", "customer_id", "account_type", "status"])
    out["opening_date"] = pd.to_datetime(out["opening_date"], errors="coerce")
    out["balance"] = pd.to_numeric(out["balance"], errors="coerce")
    return out


def transform_transactions(df: pd.DataFrame) -> pd.DataFrame:
    out = _clean_text(
        df,
        ["transaction_id", "account_id", "customer_id", "transaction_type", "channel",
         "merchant_category", "location", "status"],
    )
    out["transaction_date"] = pd.to_datetime(out["transaction_date"], errors="coerce")
    out["amount"] = pd.to_numeric(out["amount"], errors="coerce")
    # Derived fields support time-based SQL/BI analysis while retaining the original fields.
    out["transaction_day"] = out["transaction_date"].dt.date
    out["year_month"] = out["transaction_date"].dt.to_period("M").astype(str)
    out["day_of_week"] = out["transaction_date"].dt.day_name()
    out["is_weekend"] = out["transaction_date"].dt.dayofweek >= 5
    out["transaction_hour"] = out["transaction_date"].dt.hour
    return out


def transform_products(df: pd.DataFrame) -> pd.DataFrame:
    return _clean_text(df, ["product_id", "product_name", "product_category"])


def transform_customer_products(df: pd.DataFrame) -> pd.DataFrame:
    out = _clean_text(df, ["customer_id", "product_id", "status"])
    out["start_date"] = pd.to_datetime(out["start_date"], errors="coerce")
    return out


def transform_all(raw: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    return {
        "customers": transform_customers(raw["customers"]),
        "accounts": transform_accounts(raw["accounts"]),
        "transactions": transform_transactions(raw["transactions"]),
        "products": transform_products(raw["products"]),
        "customer_products": transform_customer_products(raw["customer_products"]),
    }
