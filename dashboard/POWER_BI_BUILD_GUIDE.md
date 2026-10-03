# Power BI Dashboard Build Guide

The project cannot ship a `.pbix` binary from a Python-only environment, so the repository includes **Power BI-ready CSV extracts** under `data/powerbi/` plus this exact build specification.

## Page 1 — Executive Overview

Use `customer_360.csv`, `monthly_transaction_summary.csv`, and `channel_summary.csv`.

Cards:
- Total Customers
- Total Accounts
- Successful Transactions
- Total Transaction Value
- Average Account Balance
- Average Products per Customer
- Data Quality Score

Visuals:
- Line chart: `year_month` vs `transaction_value`
- Column chart: `channel` vs `transaction_value`
- Bar chart: city vs customer count from `customer_360`
- Donut: account/product ownership indicators as appropriate

## Page 2 — Customer Intelligence

Use `customer_segments.csv` joined on `customer_id` to `customer_360`.

Visuals:
- Customer count by `segment_name`
- Median balance by segment
- Median transaction value by segment
- Scatter: `total_balance` vs `total_transaction_value`
- Table with customer_id, city, annual_income, total_balance, successful_transactions, products_owned, segment_name

## Page 3 — Data Engineering Monitor

Use `data_quality_summary.csv` and `data_quality_report.csv`.

Show:
- Quality score
- Passed checks
- Failed checks
- Issue count by dataset
- Table of checks and status

## Recommended relationships

- `customer_360[customer_id]` 1:* `customer_segments[customer_id]` if you keep both tables separately; alternatively use `customer_segments` as the enriched customer table.
- `customer_360` is the main customer-level analytical table.
- Monthly/channel/product summaries are standalone aggregate tables used in visuals.
