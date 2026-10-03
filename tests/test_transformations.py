import pandas as pd
from src.transformation.transform import transform_transactions


def test_transaction_derived_fields():
    df = pd.DataFrame({
        "transaction_id":["T1"], "account_id":["A1"], "customer_id":["C1"],
        "transaction_date":["2025-01-04 13:00:00"], "transaction_type":["Debit"],
        "channel":["UPI"], "amount":[1200], "merchant_category":["Food"],
        "location":["Bhopal"], "status":["Success"]
    })
    out = transform_transactions(df)
    assert out.loc[0, "year_month"] == "2025-01"
    assert out.loc[0, "day_of_week"] == "Saturday"
    assert bool(out.loc[0, "is_weekend"])
    assert int(out.loc[0, "transaction_hour"]) == 13
