# Ejercicio 07-01: Window Functions (ROW_NUMBER, LAG, SUM OVER) (Tipo A)

**Objetivo:** Aplicar funciones de ventana para analítica de rankings, comparaciones de filas anteriores y totales acumulados.

---

## Setup de Datos

```sql
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
```

---

## Tareas

1. Escribe una consulta `SELECT` que incluya un `ROW_NUMBER() OVER(PARTITION BY branch_office ORDER BY revenue DESC)` para rankear los mejores días de venta por cada sede.
2. Escribe una consulta `SELECT` que utilice `LAG(revenue, 1)` para mostrar los ingresos del día anterior de cada sede y calcular la diferencia de ventas respecto al día previo.

---

<details>
<summary>👀 Ver Solución Esperada</summary>

```sql
-- 1. Ranking de días con mayores ingresos por sede
SELECT 
    branch_office,
    sale_date,
    revenue,
    ROW_NUMBER() OVER(PARTITION BY branch_office ORDER BY revenue DESC) AS rank_revenue
FROM daily_revenue;

-- 2. Comparativo dia anterior con LAG
SELECT 
    branch_office,
    sale_date,
    revenue AS today_revenue,
    LAG(revenue, 1) OVER(PARTITION BY branch_office ORDER BY sale_date) AS yesterday_revenue,
    ROUND(revenue - LAG(revenue, 1) OVER(PARTITION BY branch_office ORDER BY sale_date), 2) AS diff
FROM daily_revenue;
```
</details>
