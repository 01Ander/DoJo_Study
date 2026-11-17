-- Operator workspace for Quest BI-02 SQL Reconciliation (year = 2026)
WITH store_metrics AS (
    SELECT
        s.store_name,
        -- TODO: Add total_revenue, total_orders, total_cost, avg_ticket
    FROM fact_book_sales f
    JOIN dim_store s ON f.store_id = s.store_id
    JOIN dim_date d ON f.sale_date = d.date_key
    WHERE d.year = 2026
    GROUP BY s.store_name
)
SELECT
    store_name
    -- TODO: Select metrics and pct_of_total_revenue using SUM(...) OVER ()
FROM store_metrics
ORDER BY total_revenue DESC;
