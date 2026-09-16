# Capítulo 03: Scalar Functions, CASE WHEN & Data Types

En la ingeniería de datos del mundo real, los datos crudos que ingresan a un pipeline nunca vienen perfectamente limpios. Encontrarás nombres formateados en mayúsculas y minúsculas mezcladas, fechas guardadas como texto, valores nulos donde se esperaban números y códigos de categorías inconsistentes.

En este capítulo aprenderás a utilizar **Funciones Escalares** (operaciones que procesan fila por fila y devuelven un valor transformado) para cadenas de texto, fechas y tipos de datos, así como la estructura condicional **`CASE WHEN`** para aplicar lógica de negocio directamente dentro de tus consultas SQL.

---

## 1. Conceptos Fundamentales

### Analogía 1: El Semáforo Inteligente
Piensa en la expresión `CASE WHEN` como un semáforo inteligente en un cruce de vías. La computadora evalúa cada vehículo (fila de datos) que se aproxima: si es una ambulancia (`WHEN vehicle = 'Ambulance'`), enciende la luz verde inmediata (`THEN 'Priority 1'`); si es un autobús escolar (`WHEN vehicle = 'School Bus'`), le da paso secundario (`THEN 'Priority 2'`); para cualquier otro vehículo (`ELSE`), aplica el flujo normal (`THEN 'Standard'`). `CASE WHEN` no elimina registros; simplemente los categoriza o transforma según reglas lógicas.

### Analogía 2: La Red de Seguridad `COALESCE`
Imagina que vas a pagar en una tienda y tienes varios métodos de pago guardados en tu billetera digital: primero intentas pagar con tu tarjeta de crédito principal; si no tiene fondos (es `NULL`), la aplicación automáticamente intenta con la tarjeta de débito secundaria; si esa tampoco responde, recurre al saldo en efectivo. La función `COALESCE(opcion1, opcion2, opcion3, valor_default)` opera exactamente así: prueba una lista de expresiones de izquierda a derecha y devuelve la **primera que no sea `NULL`**.

---

## 2. Dominio de Ejemplo: Registro Universitario (Domain Shifting)

Modelaremos un **Sistema de Registro de Estudiantes y Calificaciones** en una universidad.

### Setup de Datos para la Terminal

Copia y ejecuta este script en tu consola de `sqlite3 university.db`:

```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    raw_name TEXT NOT NULL,
    email TEXT,
    enrollment_date TEXT NOT NULL, -- ISO Format: YYYY-MM-DD
    scholarship_pct REAL DEFAULT 0.0
);

CREATE TABLE grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    course_code TEXT NOT NULL,
    numeric_score REAL, -- Puede contener NULL si no se ha presentado el examen
    semester TEXT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id)
);

INSERT INTO students (raw_name, email, enrollment_date, scholarship_pct) VALUES
('  juan perez  ', 'JUAN.PEREZ@univ.edu', '2023-01-15', 0.25),
('MARIA GOMEZ', NULL, '2022-08-20', 0.50),
('carlos  LOPEZ', 'c.lopez@gmail.com', '2024-01-10', NULL),
('Ana Martinez', 'ana.m@univ.edu', '2021-08-15', 0.0);

INSERT INTO grades (student_id, course_code, numeric_score, semester) VALUES
(1, 'CS101', 88.5, '2024-1'),
(1, 'MATH201', 92.0, '2024-1'),
(2, 'CS101', 54.0, '2024-1'),
(2, 'MATH201', NULL, '2024-1'),
(3, 'CS101', 75.0, '2024-1'),
(4, 'CS101', 98.0, '2024-1');
```

---

## 3. Funciones Escalares de Texto y Limpieza de Datos

SQLite incluye funciones integradas para manipular cadenas de caracteres:

- **`TRIM(string)`:** Elimina espacios en blanco al inicio y al final.
- **`UPPER(string)` / `LOWER(string)`:** Convierte a mayúsculas o minúsculas.
- **`LENGTH(string)`:** Retorna la longitud en caracteres.
- **`SUBSTR(string, start, length)`:** Extrae una subcadena.
- **`REPLACE(string, search, replace)`:** Reemplaza ocurrencias de un texto.
- **`||` (Operador de Concatenación):** Une dos o más cadenas de texto.

```sql
-- Limpieza de nombres: Eliminar espacios extra y formatear en Mayusculas
SELECT 
    id,
    raw_name AS original,
    UPPER(TRIM(raw_name)) AS cleaned_name,
    LOWER(email) AS standardized_email,
    'EST-' || id AS student_code
FROM students;
```

---

## 4. Funciones de Fecha y Manejo de Tiempo

Las fechas en SQLite se almacenan comúnmente como texto en formato ISO-8601 (`YYYY-MM-DD` o `YYYY-MM-DD HH:MM:SS`). Para trabajar con ellas usamos las funciones nativas:

```sql
-- Modificadores de fecha y calculo de antigüedad de inscripción en dias/años
SELECT 
    raw_name,
    enrollment_date,
    STRFTIME('%Y', enrollment_date) AS enrollment_year,
    STRFTIME('%m', enrollment_date) AS enrollment_month,
    CAST(JULIANDAY('now') - JULIANDAY(enrollment_date) AS INTEGER) AS days_enrolled
FROM students;
```

---

## 5. Conversión de Tipos y Manejo de Nulos (`CAST` & `COALESCE`)

- **`CAST(expresion AS TIPO)`:** Convierte explícitamente un dato de un tipo a otro (`INTEGER`, `REAL`, `TEXT`).
- **`COALESCE(val1, val2, ...)`:** Reemplaza valores `NULL` por un valor por defecto seguro.

### Ejemplo Progresivo 1: Manejo de Nulos en Cálculos

#### ❌ El Mal Camino: Operar directamente sobre campos NULL
```sql
-- ❌ MAL: Si scholarship_pct es NULL, el calculo devuelve NULL y se pierde la informacion
SELECT raw_name, scholarship_pct, (1000.0 * scholarship_pct) AS discount 
FROM students;
```

#### ✅ El Buen Camino: Envolver con `COALESCE`
```sql
-- ✅ BIEN: COALESCE convierte NULL en 0.0 antes de multiplicar
SELECT 
    raw_name, 
    COALESCE(scholarship_pct, 0.0) AS clean_scholarship,
    (1000.0 * COALESCE(scholarship_pct, 0.0)) AS discount
FROM students;
```

---

## 6. Lógica Condicional (`CASE WHEN`)

La estructura `CASE WHEN` permite crear columnas derivadas dinámicas según condiciones lógicas.

### Sintaxis del `CASE` Buscado (Searched CASE)

```sql
SELECT 
    student_id,
    course_code,
    numeric_score,
    CASE 
        WHEN numeric_score IS NULL THEN 'Pendiente de Presentar'
        WHEN numeric_score >= 90.0 THEN 'Excelente (A)'
        WHEN numeric_score >= 75.0 THEN 'Aprobado (B)'
        WHEN numeric_score >= 60.0 THEN 'Suficiente (C)'
        ELSE 'Reprobado (F)'
    END AS academic_status
FROM grades;
```

### Ejemplo Progresivo 2: Categorización de Datos Compleja

#### ❌ El Mal Camino: Varias consultas `SELECT` separadas para categorizar
```sql
-- ❌ MAL: Ejecutar 3 queries separadas para saber la situacion de becas
SELECT * FROM students WHERE scholarship_pct >= 0.5;
SELECT * FROM students WHERE scholarship_pct > 0 AND scholarship_pct < 0.5;
SELECT * FROM students WHERE scholarship_pct = 0 OR scholarship_pct IS NULL;
```

#### ✅ El Buen Camino: Una sola consulta con `CASE WHEN`
```sql
-- ✅ BIEN: Una sola pasada sobre los datos agrupando categorias en una columna calculada
SELECT 
    UPPER(TRIM(raw_name)) AS student_name,
    COALESCE(scholarship_pct, 0.0) AS pct,
    CASE 
        WHEN COALESCE(scholarship_pct, 0.0) >= 0.50 THEN 'Beca Completa / Alta'
        WHEN COALESCE(scholarship_pct, 0.0) > 0.0  THEN 'Beca Parcial'
        ELSE 'Sin Beca'
    END AS scholarship_category
FROM students;
```

---

## 7. Mapa de Ejercicios

Dirígete a la carpeta `quests/03-functions/`:

- [[01-data-cleaning.md]] (Tipo A: Escribir consultas de limpieza de texto, fechas y conversión de tipos)
- [[02-case-when-practice.md]] (Tipo B: Crear expresiones `CASE WHEN` complejas para categorizar registros de negocio)

```text
subjects/sql/chronicles/SQL-BASICO/quests/03-functions/
├── 01-data-cleaning.md
└── 02-case-when-practice.md
```
