# Interview Story

## 60-second version

“I built an end-to-end synthetic banking data platform using Python, SQL, PostgreSQL, Airflow and Power BI. I started with linked customer, account, product and transaction tables and built an ETL process to ingest and transform them. Before loading analytical data, I added automated checks for duplicate keys, missing fields, referential integrity, positive amounts, and transaction chronology. I then built a Customer 360 analytical table combining customer profile, balances, transaction behavior and product relationships. On top of that dataset, I used K-Means clustering for customer segmentation and exposed the outputs as Power BI-ready tables. Finally, I added Airflow orchestration, SQL analytics and Pytest checks so the project demonstrated both data engineering and analytics.”

## Questions you should prepare for

- Why synthetic data instead of real banking data?
- Why PostgreSQL?
- Why keep customer_id in transactions when it can be derived from accounts?
- How did you validate referential integrity?
- What happens when a data-quality check fails?
- Why did you choose K-Means?
- How did you decide the number of clusters?
- Why log-transform skewed variables before clustering?
- How would you process 10 million transactions instead of 200,000?
- What would you change for production?
- How would you secure bank data?
- How would you monitor an Airflow pipeline?
