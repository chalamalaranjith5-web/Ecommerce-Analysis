-- LAYER 1 (Analytics Engineering): raw -> clean staging tables
-- Written in standard SQL; runs on SQLite locally and on Snowflake with minor changes.

DROP TABLE IF EXISTS stg_orders;
CREATE TABLE stg_orders AS
SELECT DISTINCT                                   -- removes duplicate rows from the export
    order_id,
    customer_id,
    DATE(order_date)                    AS order_date,
    product_category,
    unit_price,
    quantity,
    ROUND(unit_price * quantity, 2)     AS revenue,
    order_status,
    promised_days,
    delivery_days,
    CASE WHEN delivery_days > promised_days
         THEN delivery_days - promised_days ELSE 0 END AS days_late,
    CASE WHEN delivery_days > promised_days THEN 1 ELSE 0 END AS is_late,
    review_score
FROM raw_orders
WHERE order_status = 'delivered';

DROP TABLE IF EXISTS stg_customers;
CREATE TABLE stg_customers AS
SELECT customer_id, region, acquisition_channel, DATE(signup_date) AS signup_date
FROM raw_customers;
