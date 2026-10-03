import pandas as pd
from src.analytics.customer_360 import build_customer_360


def test_customer_360_aggregates_relationships():
    customers = pd.DataFrame({
        "customer_id":["C1"], "age":[30], "gender":["M"], "city":["Bhopal"],
        "occupation":["Salaried Private"], "annual_income":[500000], "customer_since":pd.to_datetime(["2024-01-01"])
    })
    accounts = pd.DataFrame({
        "account_id":["A1","A2"], "customer_id":["C1","C1"], "account_type":["Savings","FD"],
        "opening_date":pd.to_datetime(["2024-01-01","2024-03-01"]), "balance":[10000,20000], "status":["Active","Active"]
    })
    transactions = pd.DataFrame({
        "transaction_id":["T1","T2"], "account_id":["A1","A2"], "customer_id":["C1","C1"],
        "transaction_date":pd.to_datetime(["2024-04-01","2024-05-01"]),
        "transaction_type":["Debit","Credit"], "channel":["UPI","NEFT"], "amount":[1000,5000],
        "merchant_category":["Food","Salary"], "location":["Bhopal","Bhopal"], "status":["Success","Success"]
    })
    cp = pd.DataFrame({"customer_id":["C1"],"product_id":["P006"],"start_date":pd.to_datetime(["2024-03-01"]),"status":["Active"]})
    out = build_customer_360({"customers":customers,"accounts":accounts,"transactions":transactions,"products":pd.DataFrame(),"customer_products":cp})
    row = out.iloc[0]
    assert row.total_accounts == 2
    assert row.total_balance == 30000
    assert row.successful_transactions == 2
    assert row.total_transaction_value == 6000
    assert bool(row.has_credit_card)
