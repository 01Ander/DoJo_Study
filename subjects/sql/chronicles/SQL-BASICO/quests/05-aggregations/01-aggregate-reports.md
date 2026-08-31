# Ejercicio 05-01: Aggregate Reports with GROUP BY & HAVING (Tipo A)

**Objetivo:** Escribir consultas analíticas consolidadas utilizando funciones de agregación, agrupación por dimensiones y filtrado de grupos con `HAVING`.

---

## Setup de Datos

```sql
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
```

---

## Tareas

1. Escribe una consulta `SELECT` que devuelva el total de ventas (`SUM(amount)`), el promedio de compra (`AVG(amount)` redondeado a 2 decimales) y el recuento de pedidos (`COUNT(*)`) por cada país (`country`).
2. Escribe una consulta `SELECT` que agrupe por país (`country`) y devuelva únicamente los países cuyo monto total de ventas sea **estrictamente mayor a 750.0 USD** (usando `HAVING`).

---

<details>
<summary>👀 Ver Solución Esperada</summary>

```sql
-- 1. Resumen por pais
SELECT 
    country,
    COUNT(*) AS total_orders,
    SUM(amount) AS total_sales,
    ROUND(AVG(amount), 2) AS avg_order_value
FROM ecom_orders
GROUP BY country;

-- 2. Filtrado de grupos con HAVING
SELECT 
    country,
    SUM(amount) AS total_sales
FROM ecom_orders
GROUP BY country
HAVING SUM(amount) > 750.0;
```
</details>
