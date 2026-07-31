# Ejercicio 04-01: Multi-Table JOIN Practice (Tipo A)

**Objetivo:** Escribir consultas combinando 3 tablas utilizando `INNER JOIN` y `LEFT JOIN` con alias adecuados.

---

## Setup de Datos

```sql
CREATE TABLE departments (
    id INTEGER PRIMARY KEY,
    dept_name TEXT NOT NULL
);

CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    dept_id INTEGER,
    FOREIGN KEY (dept_id) REFERENCES departments(id)
);

CREATE TABLE laptop_assignments (
    id INTEGER PRIMARY KEY,
    emp_id INTEGER NOT NULL,
    serial_number TEXT NOT NULL,
    FOREIGN KEY (emp_id) REFERENCES employees(id)
);

INSERT INTO departments VALUES (1, 'Engineering'), (2, 'Sales'), (3, 'HR');
INSERT INTO employees VALUES (101, 'Alice', 1), (102, 'Bob', 1), (103, 'Charlie', 2), (104, 'Diana', NULL);
INSERT INTO laptop_assignments VALUES (1, 101, 'SN-APPLE-001'), (2, 103, 'SN-DELL-999');
```

---

## Tareas

1. Escribe una consulta `INNER JOIN` que devuelva `full_name` y `dept_name` para todos los empleados asignados a un departamento.
2. Escribe una consulta `LEFT JOIN` de 3 tablas que devuelva el nombre del empleado (`full_name`), el nombre de su departamento (`dept_name` o `'Unassigned'`) y el número de serie de su laptop (`serial_number` o `'No Laptop'`).

---

<details>
<summary>👀 Ver Solución Esperada</summary>

```sql
-- 1. INNER JOIN simple
SELECT e.full_name, d.dept_name
FROM employees AS e
INNER JOIN departments AS d ON e.dept_id = d.id;

-- 2. Multi-table LEFT JOIN con COALESCE
SELECT 
    e.full_name,
    COALESCE(d.dept_name, 'Unassigned') AS department,
    COALESCE(la.serial_number, 'No Laptop') AS laptop_serial
FROM employees AS e
LEFT JOIN departments AS d ON e.dept_id = d.id
LEFT JOIN laptop_assignments AS la ON e.id = la.emp_id;
```
</details>
