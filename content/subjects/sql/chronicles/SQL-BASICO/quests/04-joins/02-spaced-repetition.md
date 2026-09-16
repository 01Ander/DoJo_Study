# Ejercicio 04-02: Spaced Repetition — Self-Joins & Filters (Tipo B)

**Objetivo:** Repasar conceptos de capítulos anteriores (00-03) integrados con la técnica de **Self-Join**.

---

## Setup de Datos

```sql
CREATE TABLE company_hierarchy (
    emp_id INTEGER PRIMARY KEY,
    emp_name TEXT NOT NULL,
    job_title TEXT NOT NULL,
    manager_id INTEGER,
    FOREIGN KEY (manager_id) REFERENCES company_hierarchy(emp_id)
);

INSERT INTO company_hierarchy VALUES
(1, 'CEO Elizabeth', 'Executive', NULL),
(2, 'VP Mark', 'Executive', 1),
(3, 'Lead Dev Sarah', 'Engineering', 2),
(4, 'Junior Dev Tom', 'Engineering', 3),
(5, 'Sales Rep Kevin', 'Sales', 2);
```

---

## Reto

Escribe una consulta **Self-Join** (`LEFT JOIN`) que devuelva el nombre del empleado (`employee`), su puesto (`job_title`), y el nombre de su jefe directo (`manager_name`). Si el empleado no tiene jefe (ej: el CEO), debe mostrar `'Top Management'`.

Filtra el resultado para mostrar únicamente empleados pertenecientes al departamento o puesto que contenga la palabra `'Engineering'` o los supervisados por `'VP Mark'`.

---

<details>
<summary>👀 Ver Solución Esperada</summary>

```sql
SELECT 
    e.emp_name AS employee,
    e.job_title,
    COALESCE(m.emp_name, 'Top Management') AS manager_name
FROM company_hierarchy AS e
LEFT JOIN company_hierarchy AS m ON e.manager_id = m.emp_id
WHERE e.job_title LIKE '%Engineering%' OR m.emp_name = 'VP Mark';
```
</details>
