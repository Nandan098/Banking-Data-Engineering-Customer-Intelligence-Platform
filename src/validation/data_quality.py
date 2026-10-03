from __future__ import annotations
from dataclasses import dataclass
import pandas as pd

@dataclass
class QualityResult:
    dataset: str
    check: str
    passed: bool
    issue_count: int
    details: str


def validate_all(data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    customers = data["customers"]
    accounts = data["accounts"]
    transactions = data["transactions"]
    products = data["products"]
    customer_products = data["customer_products"]
    results: list[QualityResult] = []

    def result(dataset, check, passed, issue_count, details):
        results.append(QualityResult(dataset, check, bool(passed), int(issue_count), details))

    # Primary keys
    for name, key in [("customers","customer_id"),("accounts","account_id"),
                      ("transactions","transaction_id"),("products","product_id")]:
        df = data[name]
        dup = int(df[key].duplicated().sum())
        result(name, f"{key} unique", dup == 0, dup, f"duplicate rows={dup}")
        null = int(df[key].isna().sum())
        result(name, f"{key} not null", null == 0, null, f"null keys={null}")

    # Required-field null checks
    required = {
        "customers": ["age","city","occupation","annual_income","customer_since"],
        "accounts": ["customer_id","account_type","opening_date","balance","status"],
        "transactions": ["account_id","customer_id","transaction_date","transaction_type","channel","amount","status"],
        "products": ["product_name","product_category"],
        "customer_products": ["customer_id","product_id","start_date","status"],
    }
    for name, cols in required.items():
        null_cells = int(data[name][cols].isna().sum().sum())
        result(name, "required fields populated", null_cells == 0, null_cells, f"null cells={null_cells}")

    # Referential integrity
    bad = int((~accounts.customer_id.isin(customers.customer_id)).sum())
    result("accounts", "customer foreign keys valid", bad == 0, bad, f"invalid customer references={bad}")
    bad = int((~transactions.account_id.isin(accounts.account_id)).sum())
    result("transactions", "account foreign keys valid", bad == 0, bad, f"invalid account references={bad}")
    bad = int((~transactions.customer_id.isin(customers.customer_id)).sum())
    result("transactions", "customer foreign keys valid", bad == 0, bad, f"invalid customer references={bad}")
    bad = int((~customer_products.customer_id.isin(customers.customer_id)).sum())
    result("customer_products", "customer foreign keys valid", bad == 0, bad, f"invalid customer references={bad}")
    bad = int((~customer_products.product_id.isin(products.product_id)).sum())
    result("customer_products", "product foreign keys valid", bad == 0, bad, f"invalid product references={bad}")

    # Domain checks
    bad = int(((customers.age < 18) | (customers.age > 100)).fillna(True).sum())
    result("customers", "age in domain", bad == 0, bad, f"invalid ages={bad}")
    bad = int((customers.annual_income <= 0).fillna(True).sum())
    result("customers", "income positive", bad == 0, bad, f"invalid incomes={bad}")
    bad = int((accounts.balance < 0).fillna(True).sum())
    result("accounts", "balance non-negative", bad == 0, bad, f"negative/invalid balances={bad}")
    bad = int((transactions.amount <= 0).fillna(True).sum())
    result("transactions", "amount positive", bad == 0, bad, f"invalid amounts={bad}")

    # Chronology
    account_open = accounts.set_index("account_id")["opening_date"]
    tx_open = transactions["account_id"].map(account_open)
    bad = int((transactions["transaction_date"] < tx_open).fillna(True).sum())
    result("transactions", "transaction after account opening", bad == 0, bad, f"chronology violations={bad}")

    # Consistency of denormalized customer_id in transactions
    account_customer = accounts.set_index("account_id")["customer_id"]
    expected_customer = transactions["account_id"].map(account_customer)
    bad = int((expected_customer != transactions["customer_id"]).fillna(True).sum())
    result("transactions", "account/customer relationship consistent", bad == 0, bad, f"mismatched customer references={bad}")

    out = pd.DataFrame([r.__dict__ for r in results])
    out["quality_score_pct"] = 100.0 * out["passed"].mean()
    return out


def save_quality_report(results: pd.DataFrame, quality_dir) -> Path:
    quality_dir.mkdir(parents=True, exist_ok=True)
    path = quality_dir / "data_quality_report.csv"
    results.to_csv(path, index=False)
    summary = pd.DataFrame([{
        "total_checks": len(results),
        "passed_checks": int(results.passed.sum()),
        "failed_checks": int((~results.passed).sum()),
        "quality_score_pct": round(results.passed.mean()*100, 2),
    }])
    summary.to_csv(quality_dir / "data_quality_summary.csv", index=False)
    return path
