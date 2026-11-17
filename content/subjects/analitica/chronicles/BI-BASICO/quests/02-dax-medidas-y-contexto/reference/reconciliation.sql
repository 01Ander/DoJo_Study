-- Reference SQL reconciliation query for Quest BI-02 (Libreria El Faro, 2026)
WITH store_metrics AS (
    SELECT
        s.store_name,
        SUM(f.amount_cop) AS total_revenue,
        COUNT(*) AS total_orders,
        SUM(f.units * f.unit_cost) AS total_cost,
        ROUND(SUM(f.amount_cop)::numeric / NULLIF(COUNT(*), 0), 2) AS avg_ticket
    FROM fact_book_sales f
    JOIN dim_store s ON f.store_id = s.store_id
    JOIN dim_date d ON f.sale_date = d.date_key
    WHERE d.year = 2026
    GROUP BY s.store_name
)
SELECT
    store_name,
    total_revenue,
    total_orders,
    total_cost,
    avg_ticket,
    ROUND(total_revenue * 100.0 / SUM(total_revenue) OVER (), 2) AS pct_of_total_revenue
FROM store_metrics
ORDER BY total_revenue DESC;
