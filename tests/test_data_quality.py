import pandas as pd
from src.validation.data_quality import validate_all


def test_source_dataset_passes_core_quality_checks():
    base = "data/raw"
    data = {
        "customers": pd.read_csv(f"{base}/customers.csv", parse_dates=["customer_since"]),
        "accounts": pd.read_csv(f"{base}/accounts.csv", parse_dates=["opening_date"]),
        "transactions": pd.read_csv(f"{base}/transactions.csv", parse_dates=["transaction_date"]),
        "products": pd.read_csv(f"{base}/products.csv"),
        "customer_products": pd.read_csv(f"{base}/customer_products.csv", parse_dates=["start_date"]),
    }
    result = validate_all(data)
    assert result["passed"].all()


def test_invalid_transaction_amount_is_caught():
    data = {
        "customers": pd.DataFrame({"customer_id":["C1"],"age":[30],"gender":["M"],"city":["X"],"occupation":["S"],"annual_income":[500000],"customer_since":["2024-01-01"]}),
        "accounts": pd.DataFrame({"account_id":["A1"],"customer_id":["C1"],"account_type":["Savings"],"opening_date":["2024-01-01"],"balance":[1000],"status":["Active"]}),
        "transactions": pd.DataFrame({"transaction_id":["T1"],"account_id":["A1"],"customer_id":["C1"],"transaction_date":["2024-01-02"],"transaction_type":["Debit"],"channel":["UPI"],"amount":[-50],"merchant_category":["Food"],"location":["X"],"status":["Success"]}),
        "products": pd.DataFrame({"product_id":["P1"],"product_name":["Savings"],"product_category":["Deposit"]}),
        "customer_products": pd.DataFrame({"customer_id":[],"product_id":[],"start_date":[],"status":[]}),
    }
    result = validate_all(data)
    row = result[(result.dataset == "transactions") & (result.check == "amount positive")].iloc[0]
    assert not row.passed
