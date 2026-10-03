from __future__ import annotations
import argparse
from pathlib import Path
from .config import RAW_DIR, PROCESSED_DIR, QUALITY_DIR, ANALYTICS_DIR, POWERBI_DIR, DB_URL
from .ingestion.read_raw import read_raw_data
from .transformation.transform import transform_all
from .validation.data_quality import validate_all, save_quality_report
from .analytics.customer_360 import (
    build_customer_360, build_monthly_transaction_summary, build_channel_summary, build_product_summary
)
from .ml.customer_segmentation import fit_customer_segments


def run(skip_db: bool = True):
    for d in [PROCESSED_DIR, QUALITY_DIR, ANALYTICS_DIR, POWERBI_DIR]:
        d.mkdir(parents=True, exist_ok=True)

    raw = read_raw_data(RAW_DIR)
    transformed = transform_all(raw)

    # Save transformed tables.
    for name, df in transformed.items():
        df.to_csv(PROCESSED_DIR / f"{name}.csv", index=False)

    quality = validate_all(transformed)
    save_quality_report(quality, QUALITY_DIR)
    if not quality.passed.all():
        raise RuntimeError("Data-quality validation failed. Inspect data/quality_reports/data_quality_report.csv")

    customer_360 = build_customer_360(transformed)
    monthly = build_monthly_transaction_summary(transformed["transactions"])
    channel = build_channel_summary(transformed["transactions"])
    product = build_product_summary(transformed)

    segmented, k_eval, profiles = fit_customer_segments(customer_360)

    customer_360.to_csv(ANALYTICS_DIR / "customer_360.csv", index=False)
    monthly.to_csv(ANALYTICS_DIR / "monthly_transaction_summary.csv", index=False)
    channel.to_csv(ANALYTICS_DIR / "channel_summary.csv", index=False)
    product.to_csv(ANALYTICS_DIR / "product_summary.csv", index=False)
    segmented.to_csv(ANALYTICS_DIR / "customer_segments.csv", index=False)
    k_eval.to_csv(ANALYTICS_DIR / "segmentation_model_selection.csv", index=False)
    profiles.to_csv(ANALYTICS_DIR / "segment_profiles.csv", index=False)

    # Power BI-ready copies / curated tables.
    for name in [
        "customer_360","monthly_transaction_summary","channel_summary","product_summary",
        "customer_segments","segment_profiles"
    ]:
        src = ANALYTICS_DIR / f"{name}.csv"
        shutil = __import__("shutil")
        shutil.copy2(src, POWERBI_DIR / src.name)
    shutil.copy2(QUALITY_DIR / "data_quality_summary.csv", POWERBI_DIR / "data_quality_summary.csv")
    shutil.copy2(QUALITY_DIR / "data_quality_report.csv", POWERBI_DIR / "data_quality_report.csv")

    if not skip_db:
        from .loading.load_postgres import load_processed_to_postgres
        load_processed_to_postgres(PROCESSED_DIR, DB_URL)

    print("Pipeline completed successfully.")
    print(f"Quality score: {quality.passed.mean()*100:.2f}%")
    print(f"Best segmentation k: {int(k_eval.loc[k_eval.silhouette_score.idxmax(),'k'])}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--load-db", action="store_true", help="Also load processed data into PostgreSQL")
    args = parser.parse_args()
    run(skip_db=not args.load_db)
