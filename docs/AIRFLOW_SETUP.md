# Airflow Setup Notes

Airflow is included as the orchestration layer, but you can complete the portfolio project without installing it first.

## Local development

1. Get the core Python pipeline working:
   `python scripts/run_pipeline.py`
2. Verify tests:
   `pytest -q`
3. Start PostgreSQL if needed:
   `docker compose up -d postgres`
4. Set `AIRFLOW_HOME` to a directory outside the repository or use an Airflow virtual environment that matches your Python version.
5. Make the repository importable by Airflow (for example, install the project package or set `PYTHONPATH` to the project root).
6. Copy/register `dags/banking_pipeline.py` in the Airflow DAGs folder.

## DAG behavior

The DAG runs daily at 06:00 and executes:

`extract → transform → validate → load_postgres → customer_360_and_ml → publish_powerbi`

The quality step raises an error when a data-quality check fails, preventing downstream analytics publication.
