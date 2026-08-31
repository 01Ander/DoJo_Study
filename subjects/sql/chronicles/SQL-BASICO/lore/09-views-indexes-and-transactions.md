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

## 5. Transacciones y los Principios ACID (`BEGIN`, `COMMIT`, `ROLLBACK`)

### Las 4 Propiedades ACID:
- **Atomicity (Atomicidad):** Todo o nada. Si una sola sentencia dentro de la transacción falla, todas se revierten.
- **Consistency (Consistencia):** La base de datos pasa de un estado válido a otro respetando todos los constraints.
- **Isolation (Aislamiento):** Las transacciones concurrentes no interfieren entre sí.
- **Durability (Durabilidad):** Una vez confirmado el `COMMIT`, los datos persisten en disco a prueba de fallos de energía.

---

### Ejemplo Progresivo 2: Procesamiento de Orden sin Transacción vs Transacción ACID Atómica

#### ❌ El Mal Camino: Modificar múltiples tablas sin bloque transaccional
```sql
-- ❌ MAL: Si falla la deduccion de stock, la orden ya fue creada dejando datos inconsistentes
INSERT INTO orders (customer_id, order_date, status, total_amount) 
VALUES (1, '2026-07-31', 'Paid', 1200.0);

-- Si el sistema se apaga AQUI, el cliente pagó pero nunca se descontó el stock ni se verificó su saldo
UPDATE products SET stock_quantity = stock_quantity - 1 WHERE id = 1;
UPDATE customers SET balance = balance - 1200.0 WHERE id = 1;
```

#### ✅ El Buen Camino: Envolver la operación completa en `BEGIN TRANSACTION`
```sql
-- ✅ BIEN: Operacion atomica con ROLLBACK en caso de error
BEGIN TRANSACTION;

-- Step 1: Registrar la orden
INSERT INTO orders (customer_id, order_date, status, total_amount) 
VALUES (1, '2026-07-31', 'Paid', 1200.0);

-- Step 2: Descontar stock (Si la cantidad es insuficiente, el CHECK(stock_quantity >= 0) fallará)
UPDATE products 
SET stock_quantity = stock_quantity - 1 
WHERE id = 1;

-- Step 3: Descontar saldo del cliente
UPDATE customers 
SET balance = balance - 1200.0 
WHERE id = 1;

-- Si todas las sentencias fueron exitosas, confirmamos los cambios permanentemente en disco
COMMIT;

-- Nota: Si cualquiera de los pasos falla por un constraint o error, SQLite ejecuta un ROLLBACK automatico.
```

---

## 6. Resumen de la Chronicle `SQL-BASICO`

¡Felicitaciones! Has completado el recorrido teórico de los 10 capítulos de la Chronicle. Ahora posees la caja de herramientas completa:
- **Fundamentos:** Tablas, Tipos, DDL, DML.
- **Modelado:** Primary Keys, Foreign Keys, Normalización 3NF.
- **Consultas:** `WHERE`, `ORDER BY`, `LIMIT`, CRUD.
- **Funciones:** Limpieza de Strings, Fechas, `CAST`, `COALESCE`, `CASE WHEN`.
- **Relaciones:** `INNER JOIN`, `LEFT JOIN`, Self-Join, Aliases.
- **Agregaciones:** `GROUP BY`, `HAVING`, `COUNT`, `SUM`, `AVG`.
- **Estructuras Avanzadas:** Subqueries correlacionadas, CTEs con `WITH`.
- **Analítica de Datos:** Window Functions (`ROW_NUMBER`, `RANK`, `LAG`, `LEAD`, deduplicación).
- **Patrones ETL:** `UNION ALL`, `INSERT INTO ... SELECT`.
- **Producción:** Views, Indexes (`EXPLAIN QUERY PLAN`), Transacciones ACID.

---

## 7. Mapa de Ejercicios

Dirígete a la carpeta `quests/09-integrity/`:

- [[01-transactions.md]] (Tipo A: Crear vistas, construir índices optimizados con `EXPLAIN` y escribir bloques transaccionales `BEGIN/COMMIT/ROLLBACK`)
- [[02-final-review.md]] (Tipo B: Examen integrador completo de la chronicle cubriendo capítulos 00 al 09)

```text
subjects/sql/chronicles/SQL-BASICO/quests/09-integrity/
├── 01-transactions.md
└── 02-final-review.md
```
