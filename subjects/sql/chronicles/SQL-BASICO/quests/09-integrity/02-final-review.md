# Ejercicio 09-02: Final Review & Assessment (Tipo B)

**Objetivo:** Examen integrador completo de la Chronicle `SQL-BASICO` evaluando capacidades relacionales, analíticas y de producción.

---

## Reto Integrador

Se requiere construir un reporte analítico de ventas integrando múltiples conceptos de la crónica. Dado el siguiente esquema:

```sql
CREATE TABLE sales_staging (
    sale_id INTEGER PRIMARY KEY,
    customer_email TEXT,
    product_category TEXT,
    sale_amount REAL,
    sale_date TEXT
);

INSERT INTO sales_staging VALUES 
(1, 'ALICE@mail.com', 'Tech', 1200.0, '2026-07-01'),
(2, 'bob@mail.com', 'Tech', 800.0, '2026-07-01'),
(3, 'alice@mail.com', 'Home', 150.0, '2026-07-02'),
(4, 'charlie@mail.com', 'Tech', 950.0, '2026-07-02');
```

Escribe una sola consulta profesional basada en una **CTE** que:
1. Normalice los correos a minúsculas (`LOWER`).
2. Calcule las ventas acumuladas por categoría (`SUM(sale_amount) OVER(PARTITION BY product_category ORDER BY sale_date)`).
3. Clasifique las ventas con `CASE WHEN` (`'High Value'` si `sale_amount >= 1000`, de lo contrario `'Standard Value'`).
4. Ordene los resultados finales por categoría y fecha.

---

<details>
<summary>👀 Ver Solución Esperada</summary>

```sql
WITH CleanSales AS (
    SELECT 
        sale_id,
        LOWER(TRIM(customer_email)) AS clean_email,
        product_category,
        sale_amount,
        sale_date
    FROM sales_staging
)
SELECT 
    sale_id,
    clean_email,
    product_category,
    sale_amount,
    sale_date,
    CASE 
        WHEN sale_amount >= 1000.0 THEN 'High Value'
        ELSE 'Standard Value'
    END AS deal_size,
    SUM(sale_amount) OVER(
        PARTITION BY product_category 
        ORDER BY sale_date 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS category_running_total
FROM CleanSales
ORDER BY product_category, sale_date;
```
</details>
