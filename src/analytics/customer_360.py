from __future__ import annotations
import pandas as pd


def build_customer_360(data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    customers = data["customers"].copy()
    accounts = data["accounts"].copy()
    transactions = data["transactions"].copy()
    cp = data["customer_products"].copy()

    acct = accounts.groupby("customer_id").agg(
        total_accounts=("account_id","nunique"),
        active_accounts=("status",lambda s: (s == "Active").sum()),
        total_balance=("balance","sum"),
        average_balance=("balance","mean"),
    ).reset_index()

    tx = transactions[transactions["status"] == "Success"].copy()
    tx_agg = tx.groupby("customer_id").agg(
        successful_transactions=("transaction_id","nunique"),
        total_transaction_value=("amount","sum"),
        average_transaction_value=("amount","mean"),
        median_transaction_value=("amount","median"),
        max_transaction_value=("amount","max"),
        last_transaction_date=("transaction_date","max"),
        debit_value=("amount",lambda s: s[tx.loc[s.index,"transaction_type"].eq("Debit")].sum()),
        credit_value=("amount",lambda s: s[tx.loc[s.index,"transaction_type"].eq("Credit")].sum()),
    ).reset_index()

    product_agg = cp.groupby("customer_id").agg(
        products_owned=("product_id","nunique"),
        active_products=("status",lambda s: (s == "Active").sum()),
    ).reset_index()

    credit_card_customers = set(cp.loc[cp.product_id.eq("P006"),"customer_id"])
    loan_products = {"P008","P009","P010"}
    loan_customers = set(cp.loc[cp.product_id.isin(loan_products),"customer_id"])
    investment_products = {"P004","P005","P012"}
    investment_customers = set(cp.loc[cp.product_id.isin(investment_products),"customer_id"])

    out = customers.merge(acct, on="customer_id", how="left")
    out = out.merge(tx_agg, on="customer_id", how="left")
    out = out.merge(product_agg, on="customer_id", how="left")

    fill_zero = ["total_accounts","active_accounts","total_balance","average_balance",
                 "successful_transactions","total_transaction_value","average_transaction_value",
                 "median_transaction_value","max_transaction_value","debit_value","credit_value",
                 "products_owned","active_products"]
    out[fill_zero] = out[fill_zero].fillna(0)
    out["last_transaction_date"] = pd.to_datetime(out["last_transaction_date"], errors="coerce")
    out["customer_tenure_years"] = ((pd.Timestamp("2025-06-30") - out["customer_since"]).dt.days / 365.25).round(2)
    out["has_credit_card"] = out.customer_id.isin(credit_card_customers)
    out["has_loan"] = out.customer_id.isin(loan_customers)
    out["has_investment_product"] = out.customer_id.isin(investment_customers)
    out["transactions_per_month"] = (out["successful_transactions"] / out["customer_tenure_years"].clip(lower=0.5) / 12).round(2)
    out["income_to_balance_ratio"] = (out["total_balance"] / out["annual_income"].replace(0, pd.NA)).fillna(0).round(4)
    return out


def build_monthly_transaction_summary(transactions: pd.DataFrame) -> pd.DataFrame:
    tx = transactions.copy()
    tx["year_month"] = tx["transaction_date"].dt.to_period("M").astype(str)
    return (tx[tx.status == "Success"]
            .groupby("year_month")
            .agg(transactions=("transaction_id","count"),
                 transaction_value=("amount","sum"),
                 average_transaction=("amount","mean"))
            .reset_index())


def build_channel_summary(transactions: pd.DataFrame) -> pd.DataFrame:
    return (transactions[transactions.status == "Success"]
            .groupby("channel")
            .agg(transactions=("transaction_id","count"),
                 transaction_value=("amount","sum"),
                 average_transaction=("amount","mean"))
            .reset_index()
            .sort_values("transaction_value", ascending=False))


def build_product_summary(data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    cp = data["customer_products"]
    products = data["products"]
    out = (cp[cp.status == "Active"]
           .groupby("product_id")
           .agg(active_customers=("customer_id","nunique"))
           .reset_index()
           .merge(products, on="product_id", how="left"))
    return out.sort_values("active_customers", ascending=False)
