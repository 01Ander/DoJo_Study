# Capítulo 05: Aggregations & Grouping

En el trabajo diario de un Data Engineer o Data Analyst, rara vez los usuarios de negocio quieren examinar registros individuales. Lo que necesitan son **métricas consolidadas**: *"¿Cuántas ventas procesamos hoy?", "¿Cuál es el promedio de edad de nuestros clientes por región?", "¿Qué categorías generaron más de 10,000 USD en ingresos?"*.

En este capítulo aprenderás a dominar las **Funciones de Agregación** (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`), la agrupación por dimensiones con `GROUP BY`, el filtrado de métricas agregadas con `HAVING` (y en qué se diferencia de `WHERE`), y la regla de oro de la agrupación relacional.

---

## 1. Conceptos Fundamentales

### Analogía 1: El Resumen Ejecutivo del Gerente
Imagina que el Director Ejecutivo de una empresa entra a tu oficina. No quiere que le leas los 50,000 recibos de caja emitidos durante el mes. Quiere tres números en una servilleta: la suma total del dinero (`SUM`), el promedio por transacción (`AVG`), y el recuento total de clientes atendidos (`COUNT`). Las funciones de agregación toman un conjunto completo de filas y lo colapsan en un **único valor escalar**.

### Analogía 2: Las Cajas de Clasificación en el Correo
Piensa en una oficina de correos. Llegan miles de cartas en una pila gigante. Los trabajadores colocan varias cajas con etiquetas de ciudades: "Medellín", "Bogotá", "Cali". Con el `GROUP BY`, tomas la pila heterogénea y repartes las cartas en sus cajas correspondientes. Luego, aplicas una función (ej: contar cuántas cartas quedaron dentro de cada caja de ciudad).

---

## 2. Dominio de Ejemplo: Registro de Carreras de Running (Domain Shifting)

Modelaremos un **Sistema de Inscripciones y Tiempos en Maratones y Carreras de Atletismo**.

### Setup de Datos para la Terminal

Ejecuta este script en tu consola de `sqlite3 running.db`:

```sql
CREATE TABLE runners (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    gender TEXT NOT NULL,
    age INTEGER NOT NULL,
    city TEXT NOT NULL
);

CREATE TABLE race_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    runner_id INTEGER NOT NULL,
    event_name TEXT NOT NULL,
    category TEXT NOT NULL, -- '10K', '21K', '42K'
    finish_time_minutes REAL NOT NULL,
    bib_number INTEGER NOT NULL,
    FOREIGN KEY (runner_id) REFERENCES runners(id)
);

INSERT INTO runners (full_name, gender, age, city) VALUES
('Carlos Vives', 'M', 34, 'Bogota'),
('Diana Trujillo', 'F', 28, 'Medellin'),
('Mateo Gomez', 'M', 45, 'Bogota'),
('Sofia Vergara', 'F', 22, 'Cali'),
('Esteban Quito', 'M', 29, 'Medellin');

INSERT INTO race_results (runner_id, event_name, category, finish_time_minutes, bib_number) VALUES
(1, 'Maraton de las Flores', '21K', 105.5, 101),
(2, 'Maraton de las Flores', '21K', 98.0, 102),
(3, 'Maraton de las Flores', '42K', 240.0, 103),
(4, 'Maraton de las Flores', '10K', 52.0, 104),
(5, 'Maraton de las Flores', '21K', 110.0, 105),
(1, 'Media Maraton de Bogota', '21K', 102.0, 501),
(2, 'Media Maraton de Bogota', '21K', 95.5, 502),
(3, 'Media Maraton de Bogota', '42K', 230.0, 503);
```

---

## 3. Funciones de Agregación Fundamentales

- **`COUNT(*)`:** Cuenta el número total de filas retenidas por la consulta.
- **`COUNT(columna)`:** Cuenta las filas donde `columna` **no** es `NULL`.
- **`COUNT(DISTINCT columna)`:** Cuenta los valores únicos no nulos de una columna.
- **`SUM(columna)`:** Suma los valores numéricos.
- **`AVG(columna)`:** Calcula el promedio aritmético.
- **`MIN(columna)` / `MAX(columna)`:** Obtiene el valor mínimo o máximo.

```sql
-- Metricas generales de la base de datos de atletismo
SELECT 
    COUNT(*) AS total_records,
    COUNT(DISTINCT runner_id) AS unique_runners,
    ROUND(AVG(finish_time_minutes), 2) AS avg_time_overall,
    MIN(finish_time_minutes) AS fastest_time,
    MAX(finish_time_minutes) AS slowest_time
FROM race_results;
```

---

## 4. Agrupación de Datos (`GROUP BY`)

La cláusula `GROUP BY` divide las filas devueltas por la consulta en grupos de filas que comparten los mismos valores en una o más columnas especificadas.

```sql
-- Calcular el tiempo promedio y total de corredores agrupado por Categoria (10K, 21K, 42K)
SELECT 
    category,
    COUNT(*) AS total_participants,
    ROUND(AVG(finish_time_minutes), 2) AS avg_finish_time,
    MIN(finish_time_minutes) AS best_time
FROM race_results
GROUP BY category;
```

### ⚠️ La Regla de Oro del `GROUP BY`
Cuando utilizas `GROUP BY`, **toda columna listada en la cláusula `SELECT` debe cumplir una de dos condiciones:**
1. Debe estar presente explícitamente en la lista del `GROUP BY`.
2. Debe estar envuelta dentro de una función de agregación (`SUM`, `COUNT`, `AVG`, etc.).

---

## 5. Ejemplos Progresivos & Filtrado de Agregados (`HAVING` vs `WHERE`)

### Ejemplo Progresivo 1: Filtrar métricas agregadas (`WHERE` que falla vs `HAVING`)

#### ❌ El Mal Camino: Intentar usar `WHERE` con una función de agregación
```sql
-- ❌ MAL: Intentar filtrar grupos en el WHERE causa un error de sintaxis en SQL
SELECT category, COUNT(*) AS runners_count
FROM race_results
WHERE COUNT(*) > 2 -- 💥 ERROR: misinterpretation of aggregate function COUNT()
GROUP BY category;
```
**¿Por qué falla?:** La cláusula `WHERE` se ejecuta **antes** de que los datos sean agrupados y agregados. `WHERE` solo conoce filas individuales.

#### ✅ El Buen Camino: Filtrar filas individuales con `WHERE` y grupos con `HAVING`
```sql
-- ✅ BIEN: WHERE filtra antes de agrupar; HAVING filtra sobre el resultado de la agregacion
SELECT 
    category, 
    COUNT(*) AS runners_count,
    ROUND(AVG(finish_time_minutes), 2) AS avg_time
FROM race_results
WHERE finish_time_minutes < 300.0 -- 1. WHERE: Filtra corredores que no hayan sido descalificados
GROUP BY category                 -- 2. GROUP BY: Agrupa por categoria
HAVING COUNT(*) >= 2              -- 3. HAVING: Filtra solo categorias que tengan 2 o mas participantes
ORDER BY avg_time ASC;
```

---

### Ejemplo Progresivo 2: Agregaciones con JOINs Multi-tabla

#### ❌ El Mal Camino: Seleccionar columnas no agregadas fuera del GROUP BY
```sql
-- ❌ MAL: Seleccionar la ciudad del corredor sin agregar ni agrupar genera resultados ambiguos
SELECT r.city, res.category, AVG(res.finish_time_minutes)
FROM race_results res
INNER JOIN runners r ON res.runner_id = r.id
GROUP BY res.category; -- 'r.city' no está en el GROUP BY ni en una función de agregación
```

#### ✅ El Buen Camino: Incluir todas las dimensiones en el `GROUP BY`
```sql
-- ✅ BIEN: Agrupar por ambas dimensiones (Ciudad del corredor y Categoria de la carrera)
SELECT 
    r.city,
    res.category,
    COUNT(res.id) AS total_races,
    ROUND(AVG(res.finish_time_minutes), 2) AS avg_time
FROM race_results AS res
INNER JOIN runners AS r ON res.runner_id = r.id
GROUP BY r.city, res.category
ORDER BY r.city, avg_time ASC;
```

---

## 6. Resumen del Flujo de Ejecución Lógica en SQL

Es fundamental entender en qué orden procesa el motor relacional una consulta completa:

1. **`FROM` / `JOIN`:** Identifica las tablas y las une.
2. **`WHERE`:** Filtra filas individuales.
3. **`GROUP BY`:** Agrupa las filas restantes.
4. **`HAVING`:** Filtra los grupos creados.
5. **`SELECT`:** Calcula las expresiones y agregaciones finales.
6. **`DISTINCT`:** Remueve filas duplicadas.
7. **`ORDER BY`:** Ordena el resultado final.
8. **`LIMIT` / `OFFSET`:** Restringe las filas retornadas a la aplicación.

---

## 7. Mapa de Ejercicios

Dirígete a la carpeta `quests/05-aggregations/`:

- [[01-aggregate-reports.md]] (Tipo A: Generar reportes analíticos consolidados con `GROUP BY` y `HAVING`)
- [[02-spaced-repetition.md]] (Tipo B: Repaso de JOINs + Agregaciones avanzadas con `ROUND` y `COUNT(DISTINCT)`)

```text
subjects/sql/chronicles/SQL-BASICO/quests/05-aggregations/
├── 01-aggregate-reports.md
└── 02-spaced-repetition.md
```
