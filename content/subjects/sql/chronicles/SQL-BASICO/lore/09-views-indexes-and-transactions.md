# Capítulo 09: Views, Indexes & Transactions (ACID)

Has llegado al capítulo final de la capa teórica de `SQL-BASICO`. En este punto eres capaz de escribir esquemas relacionales, consultar y filtrar información, unir múltiples tablas, agregar métricas y transformar datos con CTEs y Window Functions.

Para llevar tu código al estándar de producción en ingeniería de software, necesitas dominar tres conceptos arquitectónicos esenciales:
1. **Vistas (`VIEWS`):** Abstracción y seguridad de consultas complejas.
2. **Índices (`INDEXES`):** Optimización del rendimiento de lectura mediante la inspección del plan de ejecución (`EXPLAIN QUERY PLAN`).
3. **Transacciones (`ACID`):** Garantía de integridad atómica para operaciones financieras y mutaciones de estado crítico.

---

## 1. Conceptos Fundamentales

### Analogía 1: El Índice de un Libro de Texto
Imagina un libro de medicina de 1,500 páginas. Si quieres buscar información sobre la "Arritmia Cardiaca" y el libro no tiene índice al final, tendrías que ojear la 1,500 páginas una por una (en SQL esto se llama **Full Table Scan** / `SCAN TABLE`). Si el libro incluye un índice alfabetizado al final, vas directamente a la letra "A", lees que Arritmia está en la página 412 y saltas de inmediato a esa página (**Index Search** / `SEARCH TABLE`). 

### Analogía 2: La Transferencia Bancaria y el Principio de Atomicidad (ACID)
Imagina que transfieres 100 USD a un amigo desde tu aplicación bancaria. La operación consta de dos pasos: 1) Restar 100 USD de tu cuenta, 2) Sumar 100 USD a la cuenta de tu amigo. Si el sistema se apaga por una falla eléctrica justo después del Paso 1, tu dinero habría desaparecido en el aire. El principio de **Atomicidad** exige que ambos pasos ocurran juntos como una sola unidad indivisible (se confirman con `COMMIT`), o bien que si algo falla, el sistema revierta todo al estado inicial como si nada hubiera pasado (se aborta con `ROLLBACK`).

---

## 2. Dominio de Ejemplo: Sistema de E-Commerce (Domain Shifting)

Modelaremos un **Sistema de Pedidos, Inventario y Pagos en una Tienda Virtual**.

### Setup de Datos para la Terminal

Ejecuta este script en tu consola de `sqlite3 ecommerce.db`:

```sql
PRAGMA foreign_keys = ON;

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL CHECK(price >= 0),
    stock_quantity INTEGER NOT NULL CHECK(stock_quantity >= 0)
);

CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    balance REAL DEFAULT 0.0
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    order_date TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('Pending', 'Paid', 'Shipped', 'Cancelled')),
    total_amount REAL NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
);

CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK(quantity > 0),
    unit_price REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Inserción de datos iniciales
INSERT INTO products (name, category, price, stock_quantity) VALUES
('Laptop Pro 15', 'Electronics', 1200.0, 10),
('Wireless Mouse', 'Electronics', 25.0, 50),
('Ergonomic Chair', 'Furniture', 250.0, 5);

INSERT INTO customers (full_name, email, balance) VALUES
('John Doe', 'john@example.com', 1500.0),
('Jane Smith', 'jane@example.com', 300.0);
```

---

## 3. Vistas (`CREATE VIEW`)

Una **Vista** es una tabla virtual basada en el resultado de una consulta `SELECT`. No almacena los datos duplicados en disco (salvo en vistas materializadas avanzadas), sino que guarda el plano de la consulta y se ejecuta dinámicamente cada vez que la invocas.

```sql
-- Crear una vista simplificada para el equipo de finanzas
CREATE VIEW IF NOT EXISTS v_customer_order_summary AS
SELECT 
    c.id AS customer_id,
    c.full_name,
    c.email,
    COUNT(o.id) AS total_orders,
    COALESCE(SUM(o.total_amount), 0.0) AS total_spent
FROM customers AS c
LEFT JOIN orders AS o ON c.id = o.customer_id
GROUP BY c.id;

-- Consultar la vista como si fuera una tabla normal
SELECT * FROM v_customer_order_summary WHERE total_spent > 500.0;
```

---

## 4. Índices & Plan de Ejecución (`CREATE INDEX` & `EXPLAIN QUERY PLAN`)

Un **Índice** es una estructura de datos B-Tree que el motor relacional mantiene en segundo plano para acelerar las búsquedas por columnas específicas.

### Ejemplo Progresivo 1: Búsqueda sin Índice vs Búsqueda Indexada

> 🎯 **Objetivo de Negocio:** Acelerar el tiempo de respuesta del catálogo de la tienda virtual cuando los clientes consultan productos por la categoría `'Electronics'`, evitando leer todo el disco secuencialmente.

#### ❌ El Mal Camino: Consultar por una columna sin índice (`SCAN TABLE`)
```sql
-- Consultar el plan de ejecucion de una búsqueda por categoría en productos (sin indice)
EXPLAIN QUERY PLAN 
SELECT * FROM products WHERE category = 'Electronics';

-- Output esperado: SCAN TABLE products
```
**Problema:** `SCAN TABLE` significa que SQLite tuvo que leer cada una de las filas del disco para encontrar las coincidencias.

#### ✅ El Buen Camino: Crear un Índice dedicado (`SEARCH TABLE`)
```sql
-- Crear un indice sobre la columna de alta consulta 'category'
CREATE INDEX idx_products_category ON products(category);

-- Volver a consultar el plan de ejecucion
EXPLAIN QUERY PLAN 
SELECT * FROM products WHERE category = 'Electronics';

-- Output esperado: SEARCH TABLE products USING INDEX idx_products_category (category=?)
```

> ⚠️ **Trade-Off de Ingeniería:** Los índices aceleran drásticamente las consultas `SELECT`, pero hacen que las operaciones `INSERT`, `UPDATE` y `DELETE` sean más lentas porque el motor debe actualizar el árbol del índice cada vez que los datos cambian. **No crees índices en cada columna; solo en las claves de JOIN y filtros frecuentes.**

---

## 5. Transacciones y los Principios ACID (`BEGIN`, `COMMIT`, `ROLLBACK` y `SAVEPOINT`)

### ¿Qué es una Transacción?
Una **Transacción** es un conjunto de una o más operaciones SQL (`INSERT`, `UPDATE`, `DELETE`) ejecutadas como una **única unidad atómica de trabajo**. O se ejecutan todas las operaciones con éxito absoluto, o la base de datos revierte todas las modificaciones como si nunca hubieran ocurrido.

Las 4 garantías fundamentales que definen el estándar industrial de confiabilidad relacional se conocen como **ACID**:

| Principio ACID | Definición Conceptual | Valor de Negocio / Consecuencia de no tenerlo |
|---|---|---|
| **Atomicity (Atomicidad)** | Todo o nada (*All-or-Nothing*). La transacción no puede completarse a medias. | Si falla el paso 4 de 5, el sistema deshace los primeros 3 pasos, impidiendo registros huérfanos o dinero evaporado. |
| **Consistency (Consistencia)** | El estado de la base de datos siempre respeta todas las reglas (`CHECK`, `FOREIGN KEY`, `UNIQUE`, `NOT NULL`). | No pueden existir saldos negativos ni órdenes huérfanas sin cliente asociado. |
| **Isolation (Aislamiento)** | Las operaciones concurrentes de múltiples usuarios no interfieren ni ven datos en estados intermedios. | Evita lecturas sucias (*dirty reads*) o sobreescritura accidental de saldos simultáneos. |
| **Durability (Durabilidad)** | Una vez confirmado con `COMMIT`, los datos quedan guardados permanentemente en almacenamiento no volátil. | Si el servidor sufre un corte eléctrico un milisegundo después del `COMMIT`, los datos no se pierden. |

---

### Analogías del Mundo Real

#### Analogía 1: La Máquina del Tiempo de un Editor de Texto (`Ctrl + Z` / Deshacer)
Cuando redactas un contrato vital en tu computadora y accidentalmente borras una cláusula o aplicas un formato erróneo, presionas `Ctrl + Z`. La aplicación no te obliga a cerrar el programa ni a reescribir el documento desde cero; simplemente revierte el estado de la memoria al punto anterior al error. En una base de datos, **`ROLLBACK`** es el `Ctrl + Z` universal: si un paso intermedio detecta una infracción o una excepción, deshace instantáneamente todas las mutaciones realizadas desde el `BEGIN TRANSACTION`.

#### Analogía 2: La Cámara de Descompresión en un Submarino
Para que un buzo salga de un submarino bajo el agua, entra a una esclusa hermética de dos compuertas. La compuerta interna se cierra y la cámara comienza a inundarse. Si los sensores detectan una falla en el traje o una fuga de presión en la compuerta externa, el procedimiento se cancela de inmediato: se bombea toda el agua hacia afuera y se reabre la compuerta interna (**`ROLLBACK`**). La compuerta exterior jamás se abre (**`COMMIT`**) a menos que todas las condiciones de integridad sean 100% seguras, evitando que el submarino se inunde.

---

### Mecánica de Ejecución: `BEGIN`, `COMMIT`, `ROLLBACK` y `SAVEPOINT`

#### 1. Transacción Exitosa (`COMMIT`)
```sql
-- 🎯 Objetivo de Negocio: Transferir saldo y deducir stock en una sola unidad atómica confirmada.

BEGIN TRANSACTION;

-- Paso 1: Deducir stock
UPDATE products 
SET stock_quantity = stock_quantity - 1 
WHERE id = 1;

-- Paso 2: Descontar saldo del cliente
UPDATE customers 
SET balance = balance - 1200.0 
WHERE id = 1;

-- Paso 3: Registrar la orden
INSERT INTO orders (customer_id, order_date, status, total_amount) 
VALUES (1, '2026-07-31', 'Paid', 1200.0);

-- Si todo fue exitoso, confirmamos permanentemente los cambios
COMMIT;
```

#### 2. Reversión Total Explícita (`ROLLBACK`)
Si una validación de negocio falla o una restricción de integridad (`CHECK` o `FOREIGN KEY`) se rompe, la transacción se aborta con `ROLLBACK`, dejando las tablas en su estado exacto inicial:

```sql
-- 🎯 Objetivo de Negocio: Abortar una transferencia y revertir todas las mutaciones si se detecta saldo insuficiente.

BEGIN TRANSACTION;

-- Intentamos deducir saldo
UPDATE customers 
SET balance = balance - 5000.0 
WHERE id = 1;

-- Se detecta que la cuenta no tiene fondos suficientes o una regla de negocio se incumple
-- Deshacemos cualquier modificación previa:
ROLLBACK;
-- ✅ El balance del cliente permanece intacto, exactamente igual que antes del BEGIN.
```

#### 3. Puntos de Guardado Parciales (`SAVEPOINT` y `ROLLBACK TO`)
En flujos transaccionales extensos, es posible definir **marcadores intermedios** para revertir solo una porción fallida sin descartar la operación principal:

```sql
-- 🎯 Objetivo de Negocio: Procesar un pago principal pero revertir un cargo accesorio opcional si excede el límite.

BEGIN TRANSACTION;

-- Operación principal: Deducir monto de la orden
UPDATE customers SET balance = balance - 100.0 WHERE id = 1;

-- Marcador de guardado intermedio
SAVEPOINT pre_addon_fee;

-- Intentamos aplicar un recargo de seguro opcional
UPDATE customers SET balance = balance - 25.0 WHERE id = 1;

-- Si el cliente rechaza el seguro o la póliza no está disponible, revertimos solo al savepoint:
ROLLBACK TO pre_addon_fee;

-- Liberamos el savepoint y confirmamos la operación principal
RELEASE SAVEPOINT pre_addon_fee;
COMMIT;
-- ✅ Se descontaron los $100.0 principales, pero los $25.0 del recargo fueron limpiamente descartados.
```

---

> [!NOTE]
> ### 🔍 Desglose de Sintaxis (Zero Surprise Syntax): Control Transaccional
> * **`BEGIN TRANSACTION;` (o `BEGIN;`):** Desactiva el modo de autocommit de la sesión. A partir de esta línea, todas las modificaciones se guardan en un registro temporal de transacción (*Write-Ahead Log / WAL*) y no son definitivas.
> * **`COMMIT;`:** Aplica todas las mutaciones pendientes de forma permanente y atómica en el archivo de la base de datos.
> * **`ROLLBACK;`:** Cancela la transacción activa y descarta todas las mutaciones realizadas desde el `BEGIN TRANSACTION`, liberando bloqueos de concurrencia.
> * **`SAVEPOINT nombre;`:** Crea un punto de control nombrado dentro de la transacción activa.
> * **`ROLLBACK TO nombre;`:** Revierte las operaciones ejecutadas **después** del savepoint, pero mantiene vivas las operaciones anteriores.
> * **`RELEASE SAVEPOINT nombre;`:** Destruye el savepoint sin revertir sus efectos, manteniendo las mutaciones dentro de la transacción activa.

---

## 6. Modelado Dimensional y Slowly Changing Dimensions (SCD Tipo 2)

En aplicaciones transaccionales (OLTP), las tablas se normalizan en **3NF** para garantizar integridad referencial y evitar duplicaciones. Sin embargo, en la ingeniería de datos moderna y el almacenamiento analítico (**Data Warehouses** como BigQuery, Snowflake, Redshift o Databricks), el modelo dominante es el **Modelado Dimensional (Star Schema)** formalizado por Ralph Kimball.

```text
┌─────────────────────────┐          ┌─────────────────────────┐
│     dim_customers       │          │      dim_products       │
│─────────────────────────│          │─────────────────────────│
│ customer_sk (PK)        │          │ product_sk (PK)         │
│ customer_id (Nat Key)   │          │ product_id (Nat Key)    │
│ customer_name           │          │ product_name            │
│ tier / region           │          │ category                │
│ valid_from / valid_to   │          │ unit_price              │
│ is_current              │          └────────────┬────────────┘
└────────────┬────────────┘                       │
             │        ┌─────────────────────────┐ │
             │        │       fact_orders       │ │
             └───────>│─────────────────────────│<┘
                      │ order_id (PK)           │
                      │ order_date              │
                      │ customer_id (FK)        │
                      │ product_id (FK)         │
                      │ quantity                │
                      │ total_amount            │
                      └─────────────────────────┘
```

* **Tablas de Hechos (*Fact Tables*):** Registran eventos discretos de negocio y métricas numéricas acumulativas o aditivas (ej. `fact_orders`, `fact_payments`, `fact_impressions`).
* **Tablas de Dimensión (*Dimension Tables*):** Proveen el contexto descriptivo, jerarquías y atributos para filtrar y agrupar los hechos (ej. `dim_customers`, `dim_stores`, `dim_products`).

---

### El Dilema del Tiempo: ¿Qué pasa cuando los atributos de una dimensión cambian?

Imagina que el cliente `CUST-101` vive en **Bogotá** en 2024 y realiza compras por $50,000 USD. En enero de 2025, se muda a **Miami** y compra $10,000 USD.
* Si ejecutamos un simple `UPDATE dim_customers SET city = 'Miami' WHERE customer_id = 'CUST-101'`, habremos cometido el pecado de **SCD Tipo 1 (Sobrescritura)**. Al generar un reporte histórico de ventas por ciudad para 2024, parecerá falsamente que los $50,000 USD se vendieron en Miami, corrompiendo la auditoría de negocio.
* Para resolver esto, los ingenieros de datos implementan **Slowly Changing Dimensions Tipo 2 (SCD Tipo 2)**: en lugar de destruir el valor anterior, **se preserva el registro histórico intacto y se inserta una nueva fila con intervalos de vigencia temporal**.

---

### Anatomía de una Tabla de Dimensión SCD Tipo 2

Para rastrear cambios históricos, una dimensión SCD Tipo 2 introduce 3 componentes estructurales obligatorios:

1. **Surrogate Key (`_sk`):** Una llave primaria artificial (`INTEGER PRIMARY KEY AUTOINCREMENT`). Como la llave de negocio natural (`customer_id`) existirá en múltiples filas (una por cada versión histórica del cliente), la llave natural ya no puede ser la Primary Key.
2. **Columnas de Vigencia Temporal (`valid_from` y `valid_to`):** Marcas de tiempo o fechas en formato ISO-8601 (`YYYY-MM-DD` o `YYYY-MM-DD HH:MM:SS`) que definen el intervalo de tiempo exacto durante el cual dicha fila representó la realidad del negocio.
3. **Bandera de Estado Actual (`is_current`):** Un entero booleano (`1` o `0`) que permite a las consultas operacionales y dashboards consultar el estado presente sin escanear fechas.

```sql
-- 🎯 Objetivo de Negocio: Estructurar una dimensión de clientes con trazabilidad histórica completa (SCD Tipo 2).

CREATE TABLE dim_customers_scd2 (
    customer_sk INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id TEXT NOT NULL,           -- Business / Natural Key
    customer_name TEXT NOT NULL,
    membership_tier TEXT NOT NULL,       -- Atributo cambiante (e.g., 'BRONZE', 'GOLD', 'PLATINUM')
    discount_pct REAL NOT NULL,          -- Atributo cambiante (e.g., 0.05, 0.15)
    valid_from TEXT NOT NULL,            -- Inicio de vigencia (e.g., '2024-01-01')
    valid_to TEXT,                       -- Fin de vigencia (NULL o '9999-12-31' indica que sigue vigente)
    is_current INTEGER NOT NULL CHECK(is_current IN (0, 1)) -- 1 = Activo actual, 0 = Histórico
);
```

---

### El Ciclo de Transición SCD Tipo 2: Expirar e Insertar

Cuando un atributo del cliente cambia, el pipeline de datos ejecuta dos pasos atómicos dentro de una transacción:

```sql
-- 🎯 Objetivo de Negocio: Ascender a 'CUST-001' de 'BRONZE' a 'GOLD' con fecha efectiva 2025-06-01.

BEGIN TRANSACTION;

-- Paso 1: Expirar la versión activa actual cerrando su ventana de vigencia
UPDATE dim_customers_scd2
SET valid_to = '2025-06-01',
    is_current = 0
WHERE customer_id = 'CUST-001' 
  AND is_current = 1;

-- Paso 2: Insertar la nueva versión activa con los atributos actualizados
INSERT INTO dim_customers_scd2 (
    customer_id, 
    customer_name, 
    membership_tier, 
    discount_pct, 
    valid_from, 
    valid_to, 
    is_current
) VALUES (
    'CUST-001', 
    'Atlas Corp', 
    'GOLD', 
    0.15, 
    '2025-06-01', 
    NULL, 
    1
);

COMMIT;
```

---

### Consultas Temporales Point-in-Time (Cruce con Fact Tables)

La verdadera potencia del SCD Tipo 2 emerge al cruzar la tabla de hechos con la dimensión. Al unir por `customer_id` y restringir la fecha del hecho entre `valid_from` y `valid_to`, cada orden se asocia automáticamente a los beneficios y atributos que el cliente tenía **en el instante exacto en que ocurrió la orden**:

```sql
-- 🎯 Objetivo de Negocio: Reportar órdenes calculando el descuento histórico exacto vigente al momento de la compra.

SELECT 
    f.order_id,
    f.order_date,
    f.gross_amount,
    d.membership_tier AS historical_tier,
    d.discount_pct AS applied_discount_pct,
    ROUND(f.gross_amount * (1.0 - d.discount_pct), 2) AS net_amount_usd
FROM fact_orders f
JOIN dim_customers_scd2 d
  ON f.customer_id = d.customer_id
 AND f.order_date >= d.valid_from
 AND (f.order_date < d.valid_to OR d.valid_to IS NULL)
ORDER BY f.order_date ASC;
```

---

> [!NOTE]
> ### 🔍 Desglose de Sintaxis (Zero Surprise Syntax): Consultas Temporales SCD2
> * **`customer_sk` vs `customer_id`:** `customer_id` identifica a la entidad en el mundo real. `customer_sk` identifica de forma unívoca una *fotografía temporal* específica de esa entidad.
> * **`valid_to IS NULL`:** En SQL relacional, el registro vigente no tiene fecha de finalización conocida, por lo que `valid_to` se almacena como `NULL` (o alternativamente como fecha centinela `'9999-12-31'`).
> * **`f.order_date >= d.valid_from AND (f.order_date < d.valid_to OR d.valid_to IS NULL)`:** Esta cláusula de rango temporal garantiza que cada orden coincida con una y solo una versión histórica de la dimensión, evitando duplicaciones cartesianas.
> * **`WHERE is_current = 1`:** Permite obtener un snapshot instantáneo de todos los clientes activos hoy sin incurrir en cálculos de fechas.

---

### 🌐 Analogías del Mundo Real (Domain Shifting)

1. **Analogía 1 (Aeronáutica — Licencias de Piloto y Habilitaciones):**
   Un piloto comercial (`PILOT-442`) obtiene su licencia inicial con calificación monomotor (*Single-Engine*) en 2020. En 2023, obtiene la habilitación bimotor a reacción (*Multi-Engine Jet*). Si la aerolínea investiga un vuelo de 2021, la consulta SCD2 confirma con exactitud que en esa fecha el piloto volaba bajo su habilitación monomotor original, sin falsear la auditoría con sus calificaciones presentes.

2. **Analogía 2 (Telecomunicaciones — Planes Móviles y Roaming):**
   Un suscriptor de telefonía móvil inicia con el plan *Prepaid Standard* ($0.10/minuto). A los seis meses se pasa a *Postpaid Unlimited* ($0.00/minuto). Al auditar llamadas de su primer mes, la facturadora cruza con la dimensión SCD2 y cobra $0.10/minuto, mientras que las llamadas del séptimo mes se facturan a $0.00.

---

## 7. Resumen de la Chronicle `SQL-BASICO`

¡Felicitaciones! Has completado el recorrido teórico de los 10 capítulos de la Chronicle. Ahora posees la caja de herramientas completa que exige la industria en 2026:
- **Fundamentos:** Tablas, Tipos, DDL, DML.
- **Modelado:** Primary Keys, Foreign Keys, Normalización 3NF.
- **Consultas:** `WHERE`, `ORDER BY`, `LIMIT`, CRUD.
- **Funciones:** Limpieza de Strings, Fechas, `CAST`, `COALESCE`, `CASE WHEN`.
- **Relaciones:** `INNER JOIN`, `LEFT JOIN`, Self-Join, Aliases.
- **Agregaciones:** `GROUP BY`, `HAVING`, `COUNT`, `SUM`, `AVG`, Agregaciones condicionales.
- **Estructuras Avanzadas:** Subqueries correlacionadas, CTEs con `WITH`.
- **Analítica de Datos:** Window Functions (`ROW_NUMBER`, `RANK`, `LAG`, `LEAD`, deduplicación).
- **Patrones ETL:** `UNION ALL`, `INSERT INTO ... SELECT`.
- **Producción e Integridad:** Views, Indexes (`EXPLAIN QUERY PLAN`), Transacciones ACID (`COMMIT`, `ROLLBACK`, `SAVEPOINT`).
- **Arquitectura de Datos:** Star Schema dimensional y Slowly Changing Dimensions (SCD Tipo 2).

---

## 8. Mapa de Ejercicios

Dirígete a la carpeta `quests/09-integrity/`:

- [[01-transactions.md]] (Tipo A: Crear vistas, construir índices optimizados con `EXPLAIN`)
- [[02-final-review.md]] (Tipo B: Examen integrador completo de la chronicle)
- [[03-transactions-acid-rollback.md]] (Tipo A: Transacciones explícitas, `ROLLBACK`, `SAVEPOINT` y atomicidad ACID)
- [[04-scd-type2-dimensional-modeling.md]] (Tipo A: Modelado Star Schema y Slowly Changing Dimensions Tipo 2)

```text
subjects/sql/chronicles/SQL-BASICO/quests/09-integrity/
├── 01-transactions.md
├── 02-final-review.md
├── 03-transactions-acid-rollback.md
└── 04-scd-type2-dimensional-modeling.md
```


