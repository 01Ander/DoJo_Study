CREATE TABLE daily_revenue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    branch_office TEXT NOT NULL,
    sale_date TEXT NOT NULL,
    revenue REAL NOT NULL
);

INSERT INTO daily_revenue (branch_office, sale_date, revenue) VALUES
('Sede Centro', '2026-07-01', 1000.0),
('Sede Centro', '2026-07-02', 1200.0),
('Sede Centro', '2026-07-03', 1100.0),
('Sede Norte',  '2026-07-01', 800.0),
('Sede Norte',  '2026-07-02', 950.0);

SELECT
        branch_office,
        sale_date,
        revenue,
        ROW_NUMBER() OVER(PARTITION by branch_office ORDER BY revenue DESC) AS best_day
FROM daily_revenue;

SELECT
        branch_office,
        sale_date,
        revenue AS today_revenue,
        LAG(revenue, 1) OVER(PARTITION BY branch_office ORDER BY revenue) AS yesterday_sales,
        ROUND(revenue - LAG(revenue, 1) OVER(PARTITION BY branch_office ORDER BY revenue), 2) AS daily_diff
FROM daily_revenue;
