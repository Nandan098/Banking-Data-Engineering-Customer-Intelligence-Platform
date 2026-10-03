# EDA Results — Validated Banking Dataset

This report records observations from the exact dataset packaged with the project. The data is synthetic and intended to simulate realistic banking behavior.

## Volume
- Customers: **5,000**
- Accounts: **7,688**
- Transactions: **200,000**
- Customer-product relationships: **16,289**

## Distribution checks
- Median annual income: **₹539,044**; 90th percentile: **₹1,328,309**; 99th percentile: **₹2,845,667**.
- Median account balance: **₹117,626**; 90th percentile: **₹735,715**; 99th percentile: **₹2,918,478**.
- Median transaction amount: **₹1,375**; 90th percentile: **₹12,587**; 99th percentile: **₹94,704**.
- Customers with one account: **60.72%**; with two or more: **39.28%**.
- Customers with no transactions: **150**.
- Median transactions per active customer: **21**; 90th percentile: **95.1**; 99th percentile: **312.0**.

## Channel mix
- UPI: **51.27%**
- Debit Card: **12.53%**
- Credit Card: **10.21%**
- ATM: **7.92%**
- NEFT: **6.28%**
- IMPS: **5.49%**
- Net Banking: **4.69%**
- RTGS: **1.60%**

## Data quality
- Checks: **24**; passed: **24**; failed: **0**; quality score: **100.00%**.
- Referential integrity and transaction chronology are validated by the pipeline.

## ML segmentation
- Candidate K values: 3, 4, 5, 6.
- Selected K: **3** using silhouette score (**0.1708**).
- Balanced: **2,967 customers**.
- High Value & Active: **1,877 customers**.
- Inactive / No Successful Transactions: **156 customers**.

## Interpretation
The data is deliberately non-uniform: income, balances, transaction activity, channel use, city population and product adoption are not equally weighted. The project treats this as a synthetic approximation rather than a claim about any specific bank population.
