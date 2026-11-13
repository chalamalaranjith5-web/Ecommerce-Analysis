-- LAYER 2 (Data Analyst): business-ready marts

-- Monthly KPIs
DROP TABLE IF EXISTS mart_monthly_kpis;
CREATE TABLE mart_monthly_kpis AS
SELECT
    SUBSTR(order_date, 1, 7)                 AS order_month,
    COUNT(*)                                 AS orders,
    COUNT(DISTINCT customer_id)              AS active_customers,
    ROUND(SUM(revenue), 0)                   AS revenue,
    ROUND(SUM(revenue) * 1.0 / COUNT(*), 2)  AS avg_order_value,
    ROUND(AVG(is_late) * 100, 1)             AS late_delivery_pct,
    ROUND(AVG(review_score), 2)              AS avg_review
FROM stg_orders
GROUP BY 1
ORDER BY 1;

-- Delivery delay vs customer satisfaction
DROP TABLE IF EXISTS mart_delay_vs_review;
CREATE TABLE mart_delay_vs_review AS
SELECT
    CASE WHEN days_late = 0 THEN '0 (on time)'
         WHEN days_late <= 2 THEN '1-2 days'
         WHEN days_late <= 4 THEN '3-4 days'
         ELSE '5+ days' END                  AS delay_bucket,
    COUNT(*)                                 AS orders,
    ROUND(AVG(review_score), 2)              AS avg_review,
    ROUND(AVG(CASE WHEN review_score <= 2 THEN 1.0 ELSE 0 END) * 100, 1) AS bad_review_pct
FROM stg_orders
WHERE review_score IS NOT NULL
GROUP BY 1
ORDER BY 1;

-- Region performance
DROP TABLE IF EXISTS mart_region;
CREATE TABLE mart_region AS
SELECT c.region,
       COUNT(*)                         AS orders,
       ROUND(SUM(o.revenue), 0)         AS revenue,
       ROUND(AVG(o.is_late) * 100, 1)   AS late_delivery_pct,
       ROUND(AVG(o.review_score), 2)    AS avg_review
FROM stg_orders o
JOIN stg_customers c USING (customer_id)
GROUP BY 1
ORDER BY revenue DESC;
