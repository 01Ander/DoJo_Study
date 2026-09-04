CREATE TABLE ecom_orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country TEXT NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL
);

INSERT INTO ecom_orders (country, category, amount) VALUES
('Colombia', 'Tech', 500.0),
('Colombia', 'Tech', 350.0),
('Colombia', 'Home', 120.0),
('Mexico', 'Tech', 900.0),
('Mexico', 'Home', 80.0),
('Chile', 'Tech', 200.0),
('Chile', 'Home', 150.0),
('Chile', 'Home', 300.0);


SELECT
    country,
    SUM(amount) AS total_sales,
    ROUND(AVG(amount), 2) AS avg_sales,
    COUNT(*) AS total_orders
FROM ecom_orders
GROUP BY country;


SELECT
    country,
    SUM(amount) AS total_sales
FROM ecom_orders
GROUP BY country
HAVING SUM(amount) > 750.0;