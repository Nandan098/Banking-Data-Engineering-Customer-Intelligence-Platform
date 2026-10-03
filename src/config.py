from pathlib import Path
import os

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
QUALITY_DIR = DATA_DIR / "quality_reports"
ANALYTICS_DIR = DATA_DIR / "analytics"
POWERBI_DIR = DATA_DIR / "powerbi"

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "banking_db")
DB_USER = os.getenv("DB_USER", "banking_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "banking_password")

DB_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

TRANSACTION_ID = "transaction_id"
ACCOUNT_ID = "account_id"
CUSTOMER_ID = "customer_id"
PRODUCT_ID = "product_id"
