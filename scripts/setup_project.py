"""Small helper that checks the project structure and prints next commands."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
required = [
    ROOT / "data/raw/customers.csv",
    ROOT / "data/raw/accounts.csv",
    ROOT / "data/raw/transactions.csv",
    ROOT / "data/raw/products.csv",
    ROOT / "data/raw/customer_products.csv",
    ROOT / "src/pipeline.py",
    ROOT / "sql/schema.sql",
]
missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
if missing:
    raise SystemExit("Missing required files: " + ", ".join(missing))
print("Project structure OK.")
print("Next: pip install -r requirements.txt && python scripts/run_pipeline.py && pytest -q")
