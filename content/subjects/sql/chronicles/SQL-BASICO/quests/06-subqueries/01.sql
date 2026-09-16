CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL
);

INSERT INTO products (product_name, category, price) VALUES
('Laptop Pro', 'Tech', 1200.0),
('Teclado RGB', 'Tech', 80.0),
('Mouse Ergonomico', 'Tech', 40.0),
('Escritorio', 'Furniture', 300.0),
('Silla Gamer', 'Furniture', 250.0),
('Lampara LED', 'Furniture', 35.0);

SELECT
    product_name,
    price
FROM products
WHERE price > (SELECT AVG(price) FROM products)


SELECT p.product_name, p.price, p.category
FROM products AS p
WHERE p.price > (
    SELECT AVG(pro.price)
    FROM products AS pro
    WHERE pro.category = p.category);