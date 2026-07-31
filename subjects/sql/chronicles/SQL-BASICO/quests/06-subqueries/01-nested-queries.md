# Ejercicio 06-01: Subqueries (Escalares y Correlacionadas) (Tipo A)

**Objetivo:** Practicar subconsultas en `WHERE` y subconsultas correlacionadas para resolver preguntas lógicas de negocio.

---

## Setup de Datos

```sql
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
```

---

## Tareas

1. Escribe una consulta con una subquery escalar en `WHERE` que devuelva todos los productos cuyo precio sea mayor al precio promedio global de todos los productos.
2. Escribe una subquery correlacionada que devuelva los productos cuyo precio sea estrictamente mayor al promedio de precio de **SU MISMA CATEGORÍA**.

---

<details>
<summary>👀 Ver Solución Esperada</summary>

```sql
-- 1. Mayor al promedio global
SELECT product_name, price 
FROM products 
WHERE price > (SELECT AVG(price) FROM products);

-- 2. Subquery correlacionada (Mayor al promedio de su categoria)
SELECT p.product_name, p.category, p.price
FROM products AS p
WHERE p.price > (
    SELECT AVG(sub.price) 
    FROM products AS sub 
    WHERE sub.category = p.category
);
```
</details>
