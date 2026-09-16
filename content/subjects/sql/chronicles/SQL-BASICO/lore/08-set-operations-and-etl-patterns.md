# Capítulo 08: Set Operations & ETL Patterns

En los capítulos anteriores aprendiste a combinar columnas de distintas tablas horizontalmente mediante `JOIN`. Sin embargo, en la ingeniería de datos a menudo necesitas combinar filas de distintas consultas **verticalmente** (apilar registros de múltiples fuentes) o comparar conjuntos de datos para encontrar coincidencias y diferencias.

Asimismo, aprenderás el patrón básico más utilizado en las canalizaciones de datos relacionales (ELT): **`INSERT INTO ... SELECT`**, que permite extraer datos de una o varias tablas de origen, transformarlos sobre la marcha mediante SQL y cargarlos directamente en una tabla de destino.

En este capítulo aprenderás a dominar las **Operaciones de Conjuntos** (`UNION`, `UNION ALL`, `INTERSECT`, `EXCEPT`) y los patrones fundamentales de migración y transformación de datos.

---

## 1. Conceptos Fundamentales

### Analogía 1: Las Listas de Asistencia a Reuniones
Imagina que organizas dos eventos en tu empresa: el taller del lunes (Lista A) y el taller del martes (Lista B).
- **`UNION ALL`:** Simplemente pegas la Lista B debajo de la Lista A. Si Juan asistió ambos días, aparecerá dos veces en la lista combinada.
- **`UNION`:** Pegas ambas listas pero con un borrador de duplicados en la mano: si Juan aparece en ambas, borras la segunda entrada dejando una lista de asistentes únicos.
- **`INTERSECT`:** Comparas ambas listas y dejas solo a las personas que asistieron a **AMBOS** talleres.
- **`EXCEPT`:** Tomas la Lista A y tachas a cualquiera que también esté en la Lista B. El resultado son las personas que fueron el lunes pero **NO** el martes.

### Analogía 2: La Cinta Transportadora de la Fábrica (`INSERT INTO ... SELECT`)
Piensa en una cinta transportadora industrial. En un extremo tienes la materia prima (datos crudos en una tabla de staging). La cinta hace pasar los datos por una estación de lavado y empaque (la consulta `SELECT` con `CASE WHEN` y funciones escalares), y al final cae directamente dentro de las cajas de envío listas para distribución (la tabla final de producción mediante `INSERT INTO`).

---

## 2. Dominio de Ejemplo: Sistema de Recursos Humanos Multi-Sede (Domain Shifting)

Modelaremos un **Sistema de RRHH de una Empresa con Sedes en Bogotá y Medellín**, que procesa nóminas migradas desde sistemas heredados.

### Setup de Datos para la Terminal

Ejecuta este script en tu consola de `sqlite3 hr_system.db`:

```sql
CREATE TABLE legacy_bogota_staff (
    id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL,
    dept TEXT NOT NULL,
    salary_cop REAL NOT NULL
);

CREATE TABLE legacy_medellin_staff (
    id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL,
    dept TEXT NOT NULL,
    salary_cop REAL NOT NULL
);

CREATE TABLE master_employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    department TEXT NOT NULL,
    monthly_salary_usd REAL NOT NULL,
    office_location TEXT NOT NULL
);

-- Inserción de datos en sistemas heredados
INSERT INTO legacy_bogota_staff VALUES
(101, 'Carlos Ramirez', 'carlos.r@company.com', 'Engineering', 12000000.0),
(102, 'Maria Torres', 'maria.t@company.com', 'HR', 8000000.0),
(103, 'Jorge Gomez', 'jorge.g@company.com', 'Sales', 9500000.0);

INSERT INTO legacy_medellin_staff VALUES
(201, 'Maria Torres', 'maria.t@company.com', 'HR', 8000000.0), -- Empleado duplicado/trasladado
(202, 'Ana Ruiz', 'ana.r@company.com', 'Engineering', 11000000.0),
(203, 'Pedro Infante', 'pedro.i@company.com', 'Marketing', 7500000.0);
```

---

## 3. Operaciones de Conjuntos (`UNION`, `INTERSECT`, `EXCEPT`)

### Reglas Obligatorias para Operaciones de Conjuntos:
1. Todas las sentencias `SELECT` involucradas deben retornar exactamente el **mismo número de columnas**.
2. Las columnas correspondientes en cada `SELECT` deben tener **tipos de datos compatibles** en el mismo orden.

### 3.1 `UNION` vs `UNION ALL`

```sql
-- UNION ALL: Combina todas las filas manteniendo duplicados (Rápido, no requiere sorting en memoria)
SELECT full_name, email, dept, 'Bogota' AS city FROM legacy_bogota_staff
UNION ALL
SELECT full_name, email, dept, 'Medellin' AS city FROM legacy_medellin_staff;

-- UNION: Combina y elimina registros duplicados exactos (Mas lento, ejecuta deduplicación)
SELECT full_name, email, dept FROM legacy_bogota_staff
UNION
SELECT full_name, email, dept FROM legacy_medellin_staff;
```

### 3.2 `INTERSECT` y `EXCEPT`

```sql
-- INTERSECT: Encontrar empleados que estan registrados en AMBAS sedes
SELECT email FROM legacy_bogota_staff
INTERSECT
SELECT email FROM legacy_medellin_staff;

-- EXCEPT: Encontrar empleados que estan en Bogota pero NO en Medellin
SELECT email FROM legacy_bogota_staff
EXCEPT
SELECT email FROM legacy_medellin_staff;
```

---

## 4. Patrones de Carga y Transformación ELT (`INSERT INTO ... SELECT`)

El patrón `INSERT INTO target_table SELECT ... FROM source_table` es la técnica estándar para migrar y transformar registros entre tablas dentro de la base de datos relacional.

### Ejemplo Progresivo 1: Migración y Transformación en un Solo Paso

> 🎯 **Objetivo de Negocio:** Migrar y unificar los empleados de sistemas legados de dos sedes (Bogotá y Medellín) hacia la tabla corporativa maestra `master_employees`, limpiando nombres a mayúsculas sin espacios, estandarizando correos a minúsculas, convirtiendo los salarios de COP a USD (tasa 4,000) y descartando correos duplicados.

#### ❌ El Mal Camino: Extraer registros a Python, transformarlos con bucles `for` y reinsertarlos
```sql
-- ❌ MAL: Traer todos los registros a la memoria de Python para hacer la conversion de moneda y reinsertar
-- SELECT * FROM legacy_bogota_staff; 
-- # En Python: for row in rows: cursor.execute("INSERT INTO master_employees VALUES (...)")
```
**Problema:** Ineficiente. Consume miles de peticiones I/O de red entre la aplicación y la BD.

#### ✅ El Buen Camino: Transformación y Carga Directa en el Motor SQL
```sql
-- ✅ BIEN: El motor de BD extrae, convierte la moneda (COP -> USD a 4000) y carga en 1 sola sentencia atómica
INSERT INTO master_employees (full_name, email, department, monthly_salary_usd, office_location)
SELECT 
    UPPER(TRIM(full_name)) AS full_name,
    LOWER(email) AS email,
    dept AS department,
    ROUND(salary_cop / 4000.0, 2) AS monthly_salary_usd,
    'Bogota' AS office_location
FROM legacy_bogota_staff;

-- Cargar la segunda sede omitiendo duplicados de email mediante WHERE NOT IN
INSERT INTO master_employees (full_name, email, department, monthly_salary_usd, office_location)
SELECT 
    UPPER(TRIM(full_name)),
    LOWER(email),
    dept,
    ROUND(salary_cop / 4000.0, 2),
    'Medellin'
FROM legacy_medellin_staff
WHERE LOWER(email) NOT IN (SELECT email FROM master_employees);
```

---

## 5. Creación de Tablas a partir de Consultas (`CREATE TABLE ... AS SELECT`)

Puedes generar una tabla permanente que almacene una "fotografía" o snapshot de los datos resultantes de una consulta:

```sql
-- Crear una tabla consolidada de ingenieros con su salario transformado
CREATE TABLE engineering_snapshot AS
SELECT 
    full_name,
    email,
    monthly_salary_usd
FROM master_employees
WHERE department = 'Engineering';
```

---

## 6. Mapa de Ejercicios

Dirígete a la carpeta `quests/08-set-ops/`:

- [[01-union-practice.md]] (Tipo A: Utilizar `UNION ALL`, `EXCEPT` y ejecutar canalizaciones `INSERT INTO ... SELECT`)
- [[02-spaced-repetition.md]] (Tipo B: Repaso de Window Functions + Operaciones de Conjuntos e ingesta de datos)

```text
subjects/sql/chronicles/SQL-BASICO/quests/08-set-ops/
├── 01-union-practice.md
└── 02-spaced-repetition.md
```
