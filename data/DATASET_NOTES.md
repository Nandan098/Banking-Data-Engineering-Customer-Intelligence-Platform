# Dataset Notes

This project uses the validated synthetic banking dataset generated for the project. It contains uneven distributions and customer-level behavioral variation rather than equal-probability toy data.

Initial dataset size:
- 5,000 customers
- 7,688 accounts
- 200,000 transactions
- 12 products
- 16,289 customer-product relationships

The validated source dataset contains no expected nulls and no broken foreign-key relationships. Transaction timestamps were corrected so transactions do not occur before the corresponding account opening date.

Do not describe this as real customer data on a resume or in an interview. Describe it as a **synthetic dataset designed to simulate realistic banking behavior**.
