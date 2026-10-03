# Assumptions and Limitations

- All records are synthetic and are for portfolio/learning use.
- Product names/categories are generic examples; they are not a representation of any bank's actual product catalog.
- Business rules and analytical definitions are project choices, not bank policy.
- The PostgreSQL loader performs a full refresh for simplicity; production systems would typically use incremental loads and audit/control tables.
- Power BI `.pbix` is not generated here; the repository provides Power BI-ready CSVs, a theme, and a build guide.
- Airflow DAG code is included, but the local project can be run end-to-end without installing Airflow first; Airflow is introduced as the orchestration layer after the core pipeline works.
