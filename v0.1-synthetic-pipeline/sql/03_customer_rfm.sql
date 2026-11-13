-- LAYER 3 (Marketing & Growth): RFM segmentation with window functions
DROP TABLE IF EXISTS mart_customer_rfm;
CREATE TABLE mart_customer_rfm AS
WITH base AS (
    SELECT customer_id,
           JULIANDAY('2026-01-01') - JULIANDAY(MAX(order_date)) AS recency_days,  -- Snowflake: DATEDIFF('day', MAX(order_date), '2026-01-01')
           COUNT(*)                                             AS frequency,
           SUM(revenue)                                         AS monetary
    FROM stg_orders
    GROUP BY customer_id
),
scored AS (
    SELECT *,
           NTILE(4) OVER (ORDER BY recency_days DESC) AS r_score,   -- 4 = most recent
           NTILE(4) OVER (ORDER BY frequency)         AS f_score,
           NTILE(4) OVER (ORDER BY monetary)          AS m_score
    FROM base
)
SELECT s.*, c.acquisition_channel, c.region,
       CASE WHEN r_score >= 3 AND f_score >= 3 THEN 'Champions'
            WHEN r_score >= 3 AND f_score <  3 THEN 'Promising'
            WHEN r_score <  3 AND f_score >= 3 THEN 'At Risk'
            ELSE 'Hibernating' END AS segment
FROM scored s JOIN stg_customers c USING (customer_id);

DROP TABLE IF EXISTS mart_segment_summary;
CREATE TABLE mart_segment_summary AS
SELECT segment,
       COUNT(*)                                  AS customers,
       ROUND(SUM(monetary), 0)                   AS revenue,
       ROUND(SUM(monetary) * 100.0 / (SELECT SUM(monetary) FROM mart_customer_rfm), 1) AS revenue_share_pct,
       ROUND(AVG(frequency), 2)                  AS avg_orders
FROM mart_customer_rfm
GROUP BY 1
ORDER BY revenue DESC;

-- Repeat-purchase rate by acquisition channel
DROP TABLE IF EXISTS mart_channel_retention;
CREATE TABLE mart_channel_retention AS
SELECT acquisition_channel,
       COUNT(*)                                                   AS customers,
       ROUND(AVG(CASE WHEN frequency >= 2 THEN 1.0 ELSE 0 END) * 100, 1) AS repeat_rate_pct,
       ROUND(AVG(monetary), 0)                                    AS avg_customer_value
FROM mart_customer_rfm
GROUP BY 1
ORDER BY repeat_rate_pct DESC;
