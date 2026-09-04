# Capítulo 06: Subqueries & Common Table Expressions (CTEs)

A medida que las preguntas de negocio se vuelven más complejas, una sola consulta `SELECT` básica con `WHERE` y `JOIN` ya no resulta suficiente. A menudo necesitas responder una "pregunta previa" para usar su resultado dentro de la consulta principal: *"¿Cuáles empleados ganan más que el promedio de su departamento?", "¿Qué proyectos tienen tareas con retraso superior a la media?"*.

En este capítulo aprenderás a construir **Subqueries** (subconsultas en `WHERE`, `FROM` y correlacionadas) y su evolución moderna en la ingeniería de datos: las **Common Table Expressions (CTEs)** con la cláusula `WITH`.

---

## 1. Conceptos Fundamentales

### Analogía 1: La Pregunta dentro de la Pregunta
Imagina que le preguntas a tu asistente: *"¿Quién ganó el partido de fútbol que jugamos el martes pasado?"*. Para responder, tu asistente primero necesita averiguar: *"¿Cuál fue el partido que se jugó el martes pasado?"* (Subquery previa). Una vez obtiene ese ID de partido, busca el marcador final y te entrega el nombre del ganador (Query principal). 

### Analogía 2: Los Bloques LEGO de los Planos de Arquitectura (CTEs)
Piensa en una CTE (`WITH ... AS`) como la construcción de piezas de LEGO por separado antes de ensamblar el edificio final. En lugar de intentar amasar 500 piezas en una sola masa confusa de código, construyes la "Pieza A: Resumen de Horas Trabajas", luego la "Pieza B: Costos por Departamento", y en tu sentencia final simplemente unes la Pieza A con la Pieza B. Cada pieza tiene un nombre claro y legible.

---

## 2. Dominio de Ejemplo: Gestión de Proyectos (Domain Shifting)

Modelaremos un **Sistema de Proyectos, Tareas y Empleados** en una empresa de tecnología.

### Setup de Datos para la Terminal

Ejecuta este script en tu consola de `sqlite3 projects.db`:

```sql
CREATE TABLE departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    budget REAL NOT NULL
);

CREATE TABLE employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department_id INTEGER NOT NULL,
    salary REAL NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    budget REAL NOT NULL,
    department_id INTEGER NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    assigned_employee_id INTEGER,
    title TEXT NOT NULL,
    estimated_hours REAL NOT NULL,
    actual_hours REAL NOT NULL,
    status TEXT NOT NULL, -- 'Pending', 'In Progress', 'Completed'
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (assigned_employee_id) REFERENCES employees(id)
);

INSERT INTO departments (name, budget) VALUES
('Engineering', 250000.0),
('Design', 100000.0),
('Marketing', 120000.0);

INSERT INTO employees (name, department_id, salary) VALUES
('Alice Chen', 1, 95000.0),
('Bob Smith', 1, 82000.0),
('Charlie Brown', 1, 105000.0),
('Diana Prince', 2, 75000.0),
('Evan Wright', 3, 68000.0);

INSERT INTO projects (title, budget, department_id) VALUES
('Core API Migration', 150000.0, 1),
('Brand Redesign', 45000.0, 2),
('Q3 Ad Campaign', 60000.0, 3);

INSERT INTO tasks (project_id, assigned_employee_id, title, estimated_hours, actual_hours, status) VALUES
(1, 1, 'Database Schema Refactor', 40.0, 55.0, 'Completed'),
(1, 2, 'Auth Service Setup', 30.0, 28.0, 'Completed'),
(1, 3, 'Load Testing', 20.0, 35.0, 'In Progress'),
(2, 4, 'UI Mockups', 50.0, 48.0, 'Completed'),
(3, 5, 'Social Media Assets', 25.0, 30.0, 'In Progress');
```

---

## 3. Subqueries en `WHERE` y `FROM`

Una subquery es una consulta `SELECT` anidada dentro de otra consulta SQL.

### 3.1 Subquery Escalar en `WHERE`
Devuelve un **único valor** (una fila, una columna) para ser comparado.

```sql
-- Encontrar empleados cuyo salario es mayor que el salario promedio de la empresa
SELECT name, salary 
FROM employees 
WHERE salary > (SELECT AVG(salary) FROM employees);
```

### 3.2 Subquery con Operador `IN`
Devuelve una **lista de valores** (múltiples filas, una columna).

```sql
-- Obtener proyectos que tienen tareas con exceso de tiempo (actual_hours > estimated_hours)
SELECT title, budget 
FROM projects 
WHERE id IN (
    SELECT DISTINCT project_id 
    FROM tasks 
    WHERE actual_hours > estimated_hours
);
```

> 💡 **¿Por qué `SELECT DISTINCT project_id` en la subquery?**  
> Un mismo proyecto puede tener varias tareas con retraso. Sin `DISTINCT`, la subquery devolvería IDs duplicados como `(1, 1, 1, 2)`. Usar `DISTINCT` elimina las repeticiones antes de entregar la lista al operador `IN`, ahorrando comparaciones en memoria y dejando clara la intención del filtro.

### 3.3 Subquery Correlacionada
Una subquery es **correlacionada** cuando referencia columnas de la consulta exterior. Se ejecuta **una vez por cada fila** evaluada por la consulta principal.

```sql
-- Empleados que ganan mas que el promedio DE SU PROPIO DEPARTAMENTO
SELECT e.name, e.salary, e.department_id
FROM employees AS e
WHERE e.salary > (
    SELECT AVG(emp.salary) 
    FROM employees AS emp 
    WHERE emp.department_id = e.department_id -- Referencia a e.department_id del outer query
);
```

---

## 4. Common Table Expressions (CTEs) con `WITH`

Una **CTE** es una consulta nombrada temporal que existe únicamente durante la ejecución de la sentencia principal. Reemplaza las subqueries complejas por bloques limpios y reutilizables.

### Sintaxis Básica de una CTE

```sql
WITH DepartmentSalaries AS (
    -- CTE 1: Calcula el salario promedio por departamento
    SELECT 
        department_id,
        ROUND(AVG(salary), 2) AS avg_dept_salary
    FROM employees
    GROUP BY department_id
)
SELECT 
    e.name,
    e.salary,
    d.name AS department_name,
    ds.avg_dept_salary
FROM employees AS e
INNER JOIN departments AS d ON e.department_id = d.id
INNER JOIN DepartmentSalaries AS ds ON e.department_id = ds.department_id
WHERE e.salary > ds.avg_dept_salary;
```

---

## 5. Ejemplos Progresivos: Refactorización de Código Espagueti a CTEs

### Ejemplo Progresivo 1: Subqueries Anidadas Ilegibles vs CTEs Encadenadas

> 🎯 **Objetivo de Negocio:** Identificar aquellos proyectos cuyas horas reales totales dedicadas superen el promedio global de horas por proyecto de toda la empresa, mostrando el título del proyecto, sus horas reales acumuladas, el promedio global de referencia y el nombre del departamento asignado.

#### ❌ El Mal Camino: Múltiples Subqueries Anidadas en el `FROM` y `WHERE`
```sql
-- ❌ MAL: Código espagueti ilegible y difícil de debuggear
SELECT proj.title, task_summary.total_actual, dept.name
FROM projects AS proj
INNER JOIN (
    SELECT project_id, SUM(actual_hours) AS total_actual
    FROM tasks
    GROUP BY project_id
) AS task_summary ON proj.id = task_summary.project_id
INNER JOIN departments AS dept ON proj.department_id = dept.id
WHERE task_summary.total_actual > (
    SELECT AVG(total_actual) FROM (
        SELECT SUM(actual_hours) AS total_actual FROM tasks GROUP BY project_id
    )
);
```

#### ✅ El Buen Camino: CTEs Encadenadas Legibles y Modulares
```sql
-- ✅ BIEN: Mismo resultado, pero estructurado en pasos lógicos impecables
WITH ProjectTaskTotals AS (
    -- Paso 1: Sumar las horas reales por proyecto
    SELECT 
        project_id,
        SUM(actual_hours) AS total_actual_hours
    FROM tasks
    GROUP BY project_id
),
AverageProjectHours AS (
    -- Paso 2: Calcular el promedio global de horas por proyecto a partir del Paso 1
    SELECT AVG(total_actual_hours) AS global_avg_hours
    FROM ProjectTaskTotals
)
-- Paso 3: Consulta final ensamblando las CTEs limpiamente
SELECT 
    p.title AS project_title,
    ptt.total_actual_hours,
    ROUND(aph.global_avg_hours, 2) AS benchmark_avg,
    d.name AS department_name
FROM ProjectTaskTotals AS ptt
CROSS JOIN AverageProjectHours AS aph
INNER JOIN projects AS p ON ptt.project_id = p.id
INNER JOIN departments AS d ON p.department_id = d.id
WHERE ptt.total_actual_hours > aph.global_avg_hours;
```

> 💡 **¿Por qué usamos `CROSS JOIN AverageProjectHours AS aph` aquí?**  
> La CTE `AverageProjectHours` devuelve **exactamente 1 fila** (el promedio global de horas). Como no existe un ID en común para hacer un `INNER JOIN ... ON`, aplicamos un `CROSS JOIN`. Multiplicar todas las filas de proyectos por 1 sola fila ($N \times 1 = N$) **no duplica registros**, sino que "estampa" el valor del promedio global en cada fila de proyecto para poder proyectarlo en el `SELECT` y compararlo en el `WHERE`.

---

## 6. Guía de Decisión: ¿Cuándo usar qué?

| Técnica | Cuándo utilizarla | Ventajas / Desventajas |
|---|---|---|
| **Subquery en `WHERE`** | Filtros simples de una sola condición (`id IN (SELECT ...)`). | Rápido de escribir; se vuelve ilegible si se anida más de 1 nivel. |
| **JOIN Directo** | Cuando solo necesitas relacionar filas de dos tablas directamente. | La opción por defecto de mayor rendimiento para cruces simples. |
| **CTE (`WITH`)** | Consultas complejas, múltiples agregaciones intermedias, transformaciones ETL de varios pasos. | **Excelente legibilidad**, modularidad y facilidad para probar paso a paso. |

---

## 7. Mapa de Ejercicios

Dirígete a la carpeta `quests/06-subqueries/`:

- [[01-nested-queries.md]] (Tipo A: Escribir subqueries escalares, en `FROM` y subqueries correlacionadas)
- [[02-spaced-repetition.md]] (Tipo B: Refactorizar consultas anidadas complejas hacia CTEs modulares con `WITH`)

```text
subjects/sql/chronicles/SQL-BASICO/quests/06-subqueries/
├── 01-nested-queries.md
└── 02-spaced-repetition.md
```
