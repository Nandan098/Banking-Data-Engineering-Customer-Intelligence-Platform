from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

from src.ingestion.read_raw import read_raw_data
from src.transformation.transform import transform_all
from src.validation.data_quality import validate_all, save_quality_report
from src.analytics.customer_360 import build_customer_360, build_monthly_transaction_summary, build_channel_summary, build_product_summary
from src.ml.customer_segmentation import fit_customer_segments
from src.config import RAW_DIR, PROCESSED_DIR, QUALITY_DIR, ANALYTICS_DIR, POWERBI_DIR


def extract():
    # Airflow task boundary retained as an explicit stage for the portfolio DAG.
    read_raw_data(RAW_DIR)


def transform():
    raw = read_raw_data(RAW_DIR)
    transformed = transform_all(raw)
    for name, df in transformed.items():
        df.to_csv(PROCESSED_DIR / f"{name}.csv", index=False)


def validate():
    data = read_raw_data(RAW_DIR)
    data = transform_all(data)
    result = validate_all(data)
    save_quality_report(result, QUALITY_DIR)
    if not result.passed.all():
        raise ValueError("Data-quality checks failed")


def analytics_and_ml():
    data = transform_all(read_raw_data(RAW_DIR))
    c360 = build_customer_360(data)
    c360.to_csv(ANALYTICS_DIR / "customer_360.csv", index=False)
    build_monthly_transaction_summary(data["transactions"]).to_csv(ANALYTICS_DIR / "monthly_transaction_summary.csv", index=False)
    build_channel_summary(data["transactions"]).to_csv(ANALYTICS_DIR / "channel_summary.csv", index=False)
    build_product_summary(data).to_csv(ANALYTICS_DIR / "product_summary.csv", index=False)
    segmented, eval_df, profiles = fit_customer_segments(c360)
    segmented.to_csv(ANALYTICS_DIR / "customer_segments.csv", index=False)
    eval_df.to_csv(ANALYTICS_DIR / "segmentation_model_selection.csv", index=False)
    profiles.to_csv(ANALYTICS_DIR / "segment_profiles.csv", index=False)


def publish_powerbi():
    import shutil
    POWERBI_DIR.mkdir(parents=True, exist_ok=True)
    for path in ANALYTICS_DIR.glob("*.csv"):
        shutil.copy2(path, POWERBI_DIR / path.name)
    for path in QUALITY_DIR.glob("*.csv"):
        shutil.copy2(path, POWERBI_DIR / path.name)


def load_db():
    from src.loading.load_postgres import load_processed_to_postgres
    from src.config import DB_URL
    load_processed_to_postgres(PROCESSED_DIR, DB_URL)

with DAG(
    dag_id="banking_data_platform",
    start_date=datetime(2026, 1, 1),
    schedule="0 6 * * *",
    catchup=False,
    tags=["banking", "data-engineering", "customer-intelligence"],
) as dag:
    t_extract = PythonOperator(task_id="extract", python_callable=extract)
    t_transform = PythonOperator(task_id="transform", python_callable=transform)
    t_validate = PythonOperator(task_id="validate", python_callable=validate)
    t_analytics = PythonOperator(task_id="customer_360_and_ml", python_callable=analytics_and_ml)
    t_publish = PythonOperator(task_id="publish_powerbi", python_callable=publish_powerbi)
    t_load = PythonOperator(task_id="load_postgres", python_callable=load_db)

    t_extract >> t_transform >> t_validate >> t_load >> t_analytics >> t_publish
