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

## 7. Agregaciones Condicionales con `CASE WHEN` (Pivoteo Analítico)

### ¿Qué es una Agregación Condicional?
Una **Agregación Condicional** es el patrón analítico que consiste en envolver una expresión `CASE WHEN` dentro de una función de agregación (`SUM`, `COUNT` o `AVG`).

A diferencia de la cláusula `WHERE` (que actúa como un filtro global descartando del reporte a todas las filas que no cumplan la condición), la agregación condicional evalúa cada fila individualmente dentro del acumulador. Esto permite calcular simultáneamente múltiples sub-métricas independientes sobre la misma tabla en **una sola pasada de escaneo**.

---

### Analogías del Mundo Real

#### Analogía 1: Las Ranuras de Clasificación en una Máquina Contadora de Monedas
Una máquina contadora de monedas en un banco no te exige que pases todas las monedas de $100 primero, vacíes la máquina, y luego metas las de $500. Tiene una sola ranura. A medida que entra cada moneda (cada fila de datos), sus sensores ópticos evalúan el diámetro y peso (`CASE WHEN`). Si es de $100, activa el acumulador de $100 (`SUM(CASE WHEN denomination = 100 THEN 1 ELSE 0)`); si es de $500, activa el acumulador de $500. En un único pase de lectura, la máquina entrega el total por cada denominación y el gran total general.

#### Analogía 2: El Tablero de Votos en un Parlamento Electrónico
En una asamblea legislativa de 200 diputados, cuando se vota una moción de ley, no se desaloja a los que votan en contra para contar primero a los que votan a favor. Todos los diputados presionan su botón al mismo tiempo. El software del tablero escanea los 200 asientos una sola vez y despliega tres columnas en la pantalla gigante: "A Favor", "En Contra" y "Abstenciones". Cada asiento sumó a un acumulador condicional diferente.

---

### ¿Por Qué Importa en Data Engineering?
1. **Pivoteo de Filas a Columnas (Pivot Table):** En bases de datos transaccionales, los estados suelen registrarse como filas verticales (ej. un registro por cada cambio de estado). Los reportes de Business Intelligence y Data Warehouses necesitan ver estos estados horizontalmente en columnas separadas (`active_users`, `churned_users`, `pending_verification`).
2. **Optimización Extrema de Cómputo (Single Table Scan):** En lugar de hacer 3 o 4 subconsultas con `JOIN` sobre tablas con miles de millones de filas (lo que multiplicaría por 4 el costo de I/O de disco y memoria), una agregación condicional resuelve todas las métricas en un único escaneo lineal.
3. **Cálculo de Ratios y KPIs:** Permite calcular porcentajes como la tasa de retención, porcentaje de aprobación o ratio de error directamente en SQL:
   $$\text{Tasa de Aprobación} = \frac{\text{Estudiantes con Nota } \ge 60}{\text{Total de Estudiantes}} \times 100$$

---

### Demostración Paso a Paso (Sistema Universitario)

Tomemos la tabla `grades` de nuestro dominio de ejemplo. Queremos generar un reporte ejecutivo por asignatura (`course_code`) que muestre:
- Total de inscritos.
- Cantidad de aprobados (nota $\ge 60.0$).
- Cantidad de reprobados (nota $< 60.0$).
- Cantidad de ausentes (nota `NULL`).
- Porcentaje de aprobación.

#### ❌ El Mal Camino: Subconsultas Múltiples o JOINs Repetitivos
```sql
-- ❌ MAL: Escanea la tabla 'grades' 3 veces distintas y las une con JOIN, desperdiciando recursos
SELECT 
    t.course_code,
    t.total_students,
    p.passed_count
FROM (SELECT course_code, COUNT(*) AS total_students FROM grades GROUP BY course_code) t
LEFT JOIN (SELECT course_code, COUNT(*) AS passed_count FROM grades WHERE numeric_score >= 60 GROUP BY course_code) p
  ON t.course_code = p.course_code;
```

#### ✅ El Buen Camino: Pivoteo Limpio en un Solo Escaneo con `SUM(CASE WHEN...)`
```sql
-- 🎯 Objetivo de Negocio: Pivotear el conteo de notas aprobadas, reprobadas y ausentes por curso en una sola pasada.

SELECT 
    course_code,
    COUNT(*) AS total_students,
    SUM(CASE WHEN numeric_score >= 60.0 THEN 1 ELSE 0 END) AS passed_students,
    SUM(CASE WHEN numeric_score < 60.0 THEN 1 ELSE 0 END) AS failed_students,
    SUM(CASE WHEN numeric_score IS NULL THEN 1 ELSE 0 END) AS absent_students,
    ROUND(
        SUM(CASE WHEN numeric_score >= 60.0 THEN 1.0 ELSE 0.0 END) / COUNT(*) * 100.0, 
        1
    ) AS pass_rate_pct
FROM grades
GROUP BY course_code
ORDER BY course_code ASC;
```

---

> [!NOTE]
> ### 🔍 Desglose de Sintaxis (Zero Surprise Syntax): `SUM(CASE WHEN...)` y Flotantes
> * **`SUM(CASE WHEN condicion THEN 1 ELSE 0 END)`:** Si la fila cumple la condición, el `CASE` evalúa a `1`; si no, evalúa a `0`. La función `SUM` suma todos los unos y ceros, actuando eficazmente como un contador selectivo.
> * **¿Por qué `1.0` en lugar de `1` en el ratio?** En SQLite y PostgreSQL, dividir dos enteros (ej. `3 / 4`) realiza una división entera truncando el resultado a `0`. Al colocar `1.0` en el `THEN`, forzamos a que el numerador sea de tipo `REAL` (punto flotante), permitiendo calcular decimales exactos (`3.0 / 4 = 0.75`).
> * **`ROUND(expresion, decimales)`:** Redondea el valor resultante al número especificado de posiciones decimales para presentación limpia en reportes.

---

## 8. Mapa de Ejercicios

Dirígete a la carpeta `quests/03-functions/`:

- [[01-data-cleaning.md]] (Tipo A: Escribir consultas de limpieza de texto, fechas y conversión de tipos)
- [[02-case-when-practice.md]] (Tipo B: Crear expresiones `CASE WHEN` complejas para categorizar registros de negocio)
- [[03-conditional-aggregations.md]] (Tipo A: Agregaciones condicionales `SUM(CASE WHEN...)` y pivoteo de métricas)

```text
subjects/sql/chronicles/SQL-BASICO/quests/03-functions/
├── 01-data-cleaning.md
├── 02-case-when-practice.md
└── 03-conditional-aggregations.md
```

