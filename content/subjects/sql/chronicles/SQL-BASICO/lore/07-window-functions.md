# Capítulo 07: Window Functions — Analytics & Deduplication

Las **Window Functions (Funciones de Ventana)** representan uno de los saltos cualitativos más importantes en el dominio de SQL. En los capítulos anteriores viste que `GROUP BY` colapsa múltiples filas en un solo resultado agregado por grupo. Sin embargo, en la analítica avanzada e ingeniería de datos a menudo necesitas calcular métricas sobre un conjunto de filas **manteninedo la identidad individual de cada fila**.

Ejemplos típicos en pipelines de datos: *"Eliminar registros duplicados dejando solo la versión más reciente", "Calcular la diferencia de ventas entre hoy y ayer para cada tienda", "Calcular el acumulado de ingresos (running total) día por día"*.

En este capítulo aprenderás la sintaxis de la cláusula `OVER()`, las funciones de numeración (`ROW_NUMBER`, `RANK`, `DENSE_RANK`), las funciones de desplazamiento (`LAG`, `LEAD`) y el patrón maestro de deduplicación en ETL.

---

## 1. Conceptos Fundamentales

### Analogía 1: La Mirada desde la Ventana del Tren
Imagina que vas sentado en un tren en movimiento. Cada pasajero en su asiento representa una fila individual de la tabla. Al mirar por la ventana (`OVER`), ves a otros pasajeros o estaciones pasar sin que tú pierdas tu asiento individual. A diferencia de `GROUP BY` (que metería a todos los pasajeros en una sola licuadora para darte una masa única), la función de ventana le permite a cada fila "mirar" a sus vecinas y calcular métricas contextuales sin destruirse.

### Analogía 2: El Marcador del Maratón con Pantalla Personal
Piensa en una carrera donde cada corredor lleva una pantalla en su muñeca. La pantalla de Juan muestra su nombre y tiempo individual (`Row`), pero también muestra en vivo su posición exacta en el grupo (`RANK`), cuánto tiempo le lleva de ventaja al corredor que viene detrás (`LAG`), y el tiempo promedio de todos los corredores de su categoría (`AVG OVER`).

---

## 2. Dominio de Ejemplo: Ventas de Cadena de Supermercados (Domain Shifting)

Modelaremos un **Sistema de Registro de Ventas Diarias en un Supermercado**.

### Setup de Datos para la Terminal

Ejecuta este script en tu consola de `sqlite3 supermarket.db`:

```sql
CREATE TABLE store_sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    store_name TEXT NOT NULL,
    sale_date TEXT NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    created_at TEXT NOT NULL -- Timestamp de insercion para deduplicacion
);

INSERT INTO store_sales (store_name, sale_date, category, amount, created_at) VALUES
('Sede Norte', '2026-07-01', 'Lacteos', 150.0, '2026-07-01 08:00:00'),
('Sede Norte', '2026-07-01', 'Lacteos', 150.0, '2026-07-01 08:05:00'), -- DUPLICADO EVENTUAL
('Sede Norte', '2026-07-02', 'Lacteos', 220.0, '2026-07-02 08:00:00'),
('Sede Norte', '2026-07-03', 'Lacteos', 180.0, '2026-07-03 08:00:00'),
('Sede Sur',   '2026-07-01', 'Lacteos', 300.0, '2026-07-01 09:00:00'),
('Sede Sur',   '2026-07-02', 'Lacteos', 310.0, '2026-07-02 09:00:00'),
('Sede Sur',   '2026-07-03', 'Lacteos', 290.0, '2026-07-03 09:00:00'),
('Sede Norte', '2026-07-01', 'Carnes',  450.0, '2026-07-01 10:00:00'),
('Sede Norte', '2026-07-02', 'Carnes',  500.0, '2026-07-02 10:00:00');
```

---

## 3. Anatomía de una Window Function (`OVER`)

La estructura general de una función de ventana consta de tres componentes principales:

```sql
FUNCTION() OVER (
    PARTITION BY columna_grupo                   -- 1. Opcional: Divide el dataset en ventanas/grupos independientes
    ORDER BY columna_orden                       -- 2. Opcional: Ordena los registros dentro de cada ventana
    ROWS BETWEEN limite_inicio AND limite_fin    -- 3. Opcional: Marco de ventana (Window Frame) para acumulados
)
```

### 3.1 El Marco de Ventana (`Window Frame`)
Cuando calculas totales acumulados (*running totals*) o promedios móviles, necesitas decirle al motor cuántas filas incluir en el cálculo relativo a la fila actual:
- **`ROWS BETWEEN`**: Delimita el rango de filas que componen la ventana de cálculo.
- **`UNBOUNDED PRECEDING`**: "Desde el inicio de la partición (sin límite hacia atrás)".
- **`CURRENT ROW`**: "Hasta la fila actual que se está evaluando".
- **Ejemplo clásico de acumulado:** `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` acumula todos los valores desde la primera fila hasta la fila presente.

---

## 4. Funciones de Numeración & Ranking

- **`ROW_NUMBER()`:** Asigna un entero secuencial único (1, 2, 3...) a cada fila dentro de la partición.
- **`RANK()`:** Asigna rango con empates (1, 2, 2, 4...).
- **`DENSE_RANK()`:** Asigna rango sin saltos en empates (1, 2, 2, 3...).

```sql
-- Numerar y rankear las ventas de cada sede ordenadas de mayor a menor monto
SELECT 
    store_name,
    sale_date,
    category,
    amount,
    ROW_NUMBER() OVER(PARTITION BY store_name ORDER BY amount DESC) AS row_num,
    RANK()       OVER(PARTITION BY store_name ORDER BY amount DESC) AS rank_num
FROM store_sales;
```

---

## 5. Funciones de Desplazamiento (`LAG` & `LEAD`) y Acumulados

- **`LAG(columna, offset)`:** Accede a los datos de una fila **anterior** dentro de la partición (`offset` indica cuántas filas hacia atrás mirar; si no se especifica, por defecto es 1).
- **`LEAD(columna, offset)`:** Accede a los datos de una fila **posterior** dentro de la partición (`offset` indica cuántas filas hacia adelante mirar; por defecto 1).

### Ejemplo de Comparación Día a Día con `LAG`

```sql
SELECT 
    store_name,
    sale_date,
    amount AS today_sales,
    LAG(amount, 1) OVER(PARTITION BY store_name ORDER BY sale_date) AS yesterday_sales,
    ROUND(amount - LAG(amount, 1) OVER(PARTITION BY store_name ORDER BY sale_date), 2) AS daily_diff
FROM store_sales
WHERE category = 'Lacteos';
```

---

## 6. Ejemplos Progresivos de Ingeniería de Datos

### Ejemplo Progresivo 1: Deduplicación de Registros (El Patrón ETL #1)

> 🎯 **Objetivo de Negocio:** En un pipeline donde fallas de red insertan transacciones duplicadas de una misma compra (`store_name`, `sale_date`, `category`), retener únicamente la versión más reciente (el mayor `created_at`) de cada registro y descartar las réplicas anteriores.

#### ❌ El Mal Camino: Subquery anidada compleja con `MAX()` que falla si los timestamps son iguales
```sql
-- ❌ MAL: Lógica frágil y lenta basada en subqueries de fechas
SELECT * FROM store_sales 
WHERE (store_name, sale_date, category, created_at) IN (
    SELECT store_name, sale_date, category, MAX(created_at)
    FROM store_sales
    GROUP BY store_name, sale_date, category
);
```

#### ✅ El Buen Camino: Deduplicación Robusta con CTE + `ROW_NUMBER()`
```sql
-- ✅ BIEN: El patrón profesional utilizado en dbt, Spark y Snowflake
WITH RankedSales AS (
    SELECT 
        id,
        store_name,
        sale_date,
        category,
        amount,
        created_at,
        ROW_NUMBER() OVER(
            PARTITION BY store_name, sale_date, category 
            ORDER BY created_at DESC
        ) AS dedup_rank
    FROM store_sales
)
SELECT id, store_name, sale_date, category, amount, created_at
FROM RankedSales
WHERE dedup_rank = 1; -- Elimina los duplicados garantizando el ultimo registro retenido
```

---

### Ejemplo Progresivo 2: Acumulado de Ventas (Running Total)

> 🎯 **Objetivo de Negocio:** Calcular el acumulado progresivo de ingresos día a día (*running total*) para cada sede del supermercado de forma independiente, de modo que cada fila muestre la venta del día y el monto financiero total acumulado hasta esa fecha.

#### ❌ El Mal Camino: Simular acumulados con Self-Join
```sql
-- ❌ MAL: Self-Join cuadrático O(N^2) que destruye el motor relacional con muchos datos
SELECT s1.store_name, s1.sale_date, s1.amount, SUM(s2.amount) AS running_total
FROM store_sales s1
JOIN store_sales s2 ON s1.store_name = s2.store_name AND s2.sale_date <= s1.sale_date
GROUP BY s1.store_name, s1.sale_date;
```

#### ✅ El Buen Camino: Ventana Acumulativa en O(N)
```sql
-- ✅ BIEN: Una sola pasada sobre las ventanas ordenadas
SELECT 
    store_name,
    sale_date,
    amount,
    SUM(amount) OVER(
        PARTITION BY store_name 
        ORDER BY sale_date 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total
FROM store_sales;
```

> 💡 **Desglose del marco acumulativo (`Running Total`):**
> - `PARTITION BY store_name`: Reinicia el acumulador de ventas para cada sede de forma independiente.
> - `ORDER BY sale_date`: Asegura que las ventas se sumen en orden cronológico.
> - `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`: Especifica que para cada fila, sume desde el primer día registrado (`UNBOUNDED PRECEDING`) hasta la fecha de la fila que se está procesando (`CURRENT ROW`).

---

## 7. Mapa de Ejercicios

Dirígete a la carpeta `quests/07-windows/`:

- [[01-window-practice.md]] (Tipo A: Escribir consultas analíticas utilizando `ROW_NUMBER`, `RANK`, `LAG`, `LEAD` y ventanas acumulativas)
- [[02-deduplication.md]] (Tipo B: Implementar el patrón ETL de deduplicación sobre un dataset con registros duplicados)

```text
subjects/sql/chronicles/SQL-BASICO/quests/07-windows/
├── 01-window-practice.md
└── 02-deduplication.md
```
