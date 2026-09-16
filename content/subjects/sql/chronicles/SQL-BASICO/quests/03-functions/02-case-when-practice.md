# Ejercicio 03-02: Categorization with CASE WHEN (Tipo B)

**Objetivo:** Construir expresiones condicionales complejas con `CASE WHEN` para segmentación analítica.

---

## Setup de Datos

```sql
CREATE TABLE employee_evaluations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emp_name TEXT NOT NULL,
    projects_completed INTEGER NOT NULL,
    satisfaction_score REAL -- 0.0 a 10.0
);

INSERT INTO employee_evaluations (emp_name, projects_completed, satisfaction_score) VALUES
('Carlos V', 12, 9.5),
('Ana G', 4, 7.0),
('Luis M', 0, NULL),
('Elena P', 8, 8.2),
('Sofia R', 15, 6.5);
```

---

## Tarea

Escribe una consulta `SELECT` que incluya las siguientes dos columnas calculadas con `CASE WHEN`:
1. `performance_tier`:
   - `'Top Performer'` si `projects_completed >= 10` y `satisfaction_score >= 8.0`
   - `'Solid Performer'` si `projects_completed >= 5`
   - `'Needs Improvement'` en cualquier otro caso
2. `review_status`:
   - `'Pending Eval'` si `satisfaction_score IS NULL`
   - `'Evaluated'` en caso contrario

---

<details>
<summary>👀 Ver Solución Esperada</summary>

```sql
SELECT 
    emp_name,
    projects_completed,
    COALESCE(satisfaction_score, 0.0) AS score,
    CASE 
        WHEN projects_completed >= 10 AND satisfaction_score >= 8.0 THEN 'Top Performer'
        WHEN projects_completed >= 5 THEN 'Solid Performer'
        ELSE 'Needs Improvement'
    END AS performance_tier,
    CASE 
        WHEN satisfaction_score IS NULL THEN 'Pending Eval'
        ELSE 'Evaluated'
    END AS review_status
FROM employee_evaluations;
```
</details>
