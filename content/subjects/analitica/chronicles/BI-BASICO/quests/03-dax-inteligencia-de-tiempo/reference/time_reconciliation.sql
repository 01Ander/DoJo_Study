-- Reference SQL reconciliation query for Quest BI-03 (Libreria El Faro, safe on sparse months)
WITH monthly_sales AS (
    SELECT
        d.year,
        d.month_number,
        SUM(f.amount_cop) AS total_revenue
    FROM fact_book_sales f
    JOIN dim_date d ON f.sale_date = d.date_key
    GROUP BY d.year, d.month_number
)
SELECT
    cur.year,
    cur.month_number,
    cur.total_revenue,
    SUM(cur.total_revenue) OVER (
        PARTITION BY cur.year
        ORDER BY cur.month_number
    ) AS ytd_revenue,
    ROUND(
        (cur.total_revenue - prev_m.total_revenue) * 100.0
        / NULLIF(prev_m.total_revenue, 0),
        2
    ) AS mom_pct,
    ROUND(
        (cur.total_revenue - prev_y.total_revenue) * 100.0
        / NULLIF(prev_y.total_revenue, 0),
        2
    ) AS yoy_pct
FROM monthly_sales cur
LEFT JOIN monthly_sales prev_m
    ON prev_m.year * 12 + prev_m.month_number
     = cur.year * 12 + cur.month_number - 1
LEFT JOIN monthly_sales prev_y
    ON prev_y.year = cur.year - 1
   AND prev_y.month_number = cur.month_number
ORDER BY cur.year, cur.month_number;
