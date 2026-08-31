# Ejercicio 06-02: Refactoring to CTEs (WITH) (Tipo B)

**Objetivo:** Refactorizar consultas anidadas complejas hacia una estructura modular limpia utilizando Common Table Expressions (`WITH`).

---

## Setup de Datos

```sql
CREATE TABLE sales_agents (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    region TEXT NOT NULL
);

CREATE TABLE agent_deals (
    id INTEGER PRIMARY KEY,
    agent_id INTEGER,
    deal_amount REAL NOT NULL,
    FOREIGN KEY (agent_id) REFERENCES sales_agents(id)
);

INSERT INTO sales_agents VALUES (1, 'Carlos', 'LATAM'), (2, 'Diana', 'LATAM'), (3, 'Eric', 'EMEA');
INSERT INTO agent_deals VALUES (10, 1, 5000.0), (11, 1, 3000.0), (12, 2, 9000.0), (13, 3, 4000.0);
```

---

## Reto

Construye una CTE nombrada `AgentTotals` que calcule el total de ventas (`SUM(deal_amount)`) por cada agente. Luego, en la consulta principal, une `sales_agents` con `AgentTotals` y muestra únicamente a los agentes cuyas ventas totales superen el promedio global de ventas por agente.

---

<details>
<summary>👀 Ver Solución Esperada</summary>

```sql
WITH AgentTotals AS (
    SELECT 
        agent_id,
        SUM(deal_amount) AS total_sales
    FROM agent_deals
    GROUP BY agent_id
),
GlobalAverage AS (
    SELECT AVG(total_sales) AS avg_sales FROM AgentTotals
)
SELECT 
    sa.name,
    sa.region,
    at.total_sales
FROM sales_agents AS sa
INNER JOIN AgentTotals AS at ON sa.id = at.agent_id
CROSS JOIN GlobalAverage AS ga
WHERE at.total_sales > ga.avg_sales;
```
</details>
