# E-commerce Sales Performance Analysis

End-to-end sales analysis for a French online store (electronics, home, clothing, beauty and sports products), built with **SQL**, **Power BI** and **Python**.

> 🚧 Work in progress

## Business questions

1. How do sales evolve month by month?
2. Which categories and products bring the most revenue?
3. Which cities have the most customers and revenue?
4. What is the Average Order Value (AOV)?

## Data

Synthetic dataset covering January 2025 to June 2026.

| File | Description |
|---|---|
| `data/ecommerce.db` | SQLite database with 3 tables: `orders` (520 rows), `customers` (160), `products` (28) |
| `data/clean/*.csv` | Same 3 tables as CSV files |
| `data/raw/orders_export_raw.csv` | Monthly website export with real-world quality issues (inconsistent city names, mixed date formats, prices stored as text, missing quantities, duplicate rows) |

### Data model

```
customers (customer_id, first_name, city, signup_date)
     │ 1
     │
     │ *
orders (order_id, order_date, customer_id, product_id, quantity)
     │ *
     │
     │ 1
products (product_id, product_name, category, unit_price)
```

## Project structure

| Folder | Content |
|---|---|
| `data/` | Database, clean tables and raw export |
| `sql/` | SQL queries answering the business questions |
| `powerbi/` | Power BI report (.pbix) |
| `python/` | Data cleaning and analysis with pandas |
| `images/` | Dashboard screenshots |

## Roadmap

- [x] Project setup and dataset
- [ ] SQL analysis: filtering, aggregations, joins
- [ ] Power BI: Power Query cleaning, star schema, DAX measures
- [ ] Power BI sales dashboard
- [ ] Python / pandas: automated cleaning of the raw export
- [ ] Key insights and recommendations

## Tools

SQL (SQLite) · Power BI · Power Query · DAX · Python · pandas · Git

---
*Author: Ranjith Chalamala*
