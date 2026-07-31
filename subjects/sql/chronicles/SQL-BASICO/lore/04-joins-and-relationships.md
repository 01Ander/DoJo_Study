# Capítulo 04: JOINs & Table Relationships

En una base de datos relacional normalizada, la información vive fragmentada en múltiples tablas especializadas. Por ejemplo, los datos de una venta están en una tabla, los datos del cliente en otra y los detalles del producto en una tercera. Para producir reportes útiles o alimentar un pipeline de datos, necesitamos **combinar** esas tablas.

En este capítulo aprenderás a dominar la cláusula **`JOIN`** en sus distintas variantes (`INNER`, `LEFT`, `CROSS`, `Self-Join`), el uso obligatorio de alias (`AS`), consultas multi-tabla y a diagnosticar anti-patrones como el producto cartesiano accidental.

---

## 1. Conceptos Fundamentales

### Analogía 1: Las Piezas de Rompecabezas
Imagina que tienes dos conjuntos de piezas de rompecabezas: el conjunto A (Clientes) y el conjunto B (Compras). Cada cliente tiene una "muesca" única con su `ID`. Una operación `JOIN` consiste en buscar las piezas de A y B cuya muesca encaje perfectamente (`ON A.id = B.customer_id`). 
- **`INNER JOIN`:** Solo se muestran las parejas donde la pieza de A encajó con la de B.
- **`LEFT JOIN`:** Se muestran **todas** las piezas de A; si alguna no encontró pareja en B, el lado de B se llena con piezas transparentes (`NULL`).

### Analogía 2: La Lista de Invitados y las Mesas asignadas
Piensa en una fiesta de bodas. Tienes una lista de 50 invitados en la entrada (Tabla A) y una lista de 10 mesas numeradas (Tabla B). 
- Con `INNER JOIN`, solo obtendrás la lista de invitados que ya tienen una mesa asignada.
- Con `LEFT JOIN`, obtendrás la lista completa de los 50 invitados; aquellos que aún no tienen mesa asignada aparecerán listados con `Mesa: NULL`.

---

## 2. Dominio de Ejemplo: Tienda de Videojuegos (Domain Shifting)

Modelaremos un **Sistema de Inventario y Ventas de Videojuegos**.

### Setup de Datos para la Terminal

Ejecuta este script en tu consola de `sqlite3 gamestore.db`:

```sql
CREATE TABLE platforms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    manufacturer TEXT NOT NULL
);

CREATE TABLE games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    genre TEXT NOT NULL,
    platform_id INTEGER,
    price REAL NOT NULL,
    FOREIGN KEY (platform_id) REFERENCES platforms(id)
);

CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    referred_by_id INTEGER, -- Self-Join: ID de otro cliente que lo refirió
    FOREIGN KEY (referred_by_id) REFERENCES customers(id)
);

CREATE TABLE sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    sale_date TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (game_id) REFERENCES games(id),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- Inserción de datos
INSERT INTO platforms (name, manufacturer) VALUES
('PlayStation 5', 'Sony'),
('Xbox Series X', 'Microsoft'),
('Nintendo Switch', 'Nintendo'),
('PC', 'Valve/Custom'); -- ID 4

INSERT INTO games (title, genre, platform_id, price) VALUES
('Elden Ring', 'Action RPG', 1, 59.99),
('Halo Infinite', 'FPS', 2, 49.99),
('Zelda: Tears of the Kingdom', 'Adventure', 3, 69.99),
('Cyberpunk 2077', 'RPG', 4, 39.99),
('Indie Mystery Game', 'Puzzle', NULL, 9.99); -- Juego sin plataforma asignada (platform_id IS NULL)

INSERT INTO customers (full_name, referred_by_id) VALUES
('Carlos Gamer', NULL),        -- ID 1
('Beatriz Pro', 1),            -- ID 2 (Referida por Carlos)
('Diego Arcade', 1),           -- ID 3 (Referido por Carlos)
('Elena Casual', NULL);        -- ID 4 (Sin compras registradas)

INSERT INTO sales (game_id, customer_id, sale_date, quantity) VALUES
(1, 1, '2026-07-01', 1),
(3, 2, '2026-07-02', 1),
(1, 3, '2026-07-03', 2);
```

---

## 3. Tipos de JOINs y Ejemplos Prácticos

### 3.1 `INNER JOIN` (Intersección Exacta)
Devuelve únicamente los registros que tienen coincidencias en ambas tablas.

```sql
-- Obtener el nombre del juego junto con el nombre de su plataforma
SELECT 
    g.title AS game_title,
    g.genre,
    p.name AS platform_name,
    p.manufacturer
FROM games AS g
INNER JOIN platforms AS p ON g.platform_id = p.id;
```
> Notice: 'Indie Mystery Game' (con `platform_id IS NULL`) **no aparece** en el resultado porque no tiene coincidencia en `platforms`.

### 3.2 `LEFT JOIN` (Conservar la Tabla Izquierda)
Devuelve **todos** los registros de la tabla izquierda (`games`), e incluye los datos de la tabla derecha (`platforms`) si existen. Si no coinciden, devuelve `NULL`.

```sql
-- Obtener TODOS los juegos, incluyendo los que no tienen plataforma asignada
SELECT 
    g.title AS game_title,
    COALESCE(p.name, 'Sin Plataforma') AS platform_name
FROM games AS g
LEFT JOIN platforms AS p ON g.platform_id = p.id;
```

---

## 4. Multi-Table JOINs & Self-Join

### Multi-Table JOINs (Unir 3 o más Tablas)
Puedes encadenar múltiples cláusulas `JOIN` para construir consultas complejas.

```sql
-- Reporte de ventas completo: Cliente + Juego + Plataforma + Fecha
SELECT 
    c.full_name AS customer,
    g.title AS game,
    p.name AS platform,
    s.sale_date,
    s.quantity,
    (s.quantity * g.price) AS total_spent
FROM sales AS s
INNER JOIN customers AS c ON s.customer_id = c.id
INNER JOIN games AS g ON s.game_id = g.id
LEFT JOIN platforms AS p ON g.platform_id = p.id;
```

### Self-Join (Una Tabla unida consigo misma)
Se utiliza cuando una tabla contiene una Foreign Key que apunta a su propia Primary Key (ej: empleados y sus jefes, o clientes y quienes los refirieron).

```sql
-- Obtener los clientes y el nombre de la persona que los refirió
SELECT 
    c.full_name AS customer,
    COALESCE(r.full_name, 'Sin Referidor (Directo)') AS referred_by
FROM customers AS c
LEFT JOIN customers AS r ON c.referred_by_id = r.id;
```

---

## 5. Ejemplos Progresivos & Anti-patrones

### Ejemplo Progresivo 1: El problema de las N+1 Consultas Manuales vs JOIN

#### ❌ El Mal Camino: Simular JOINs en código de aplicación (N+1 Queries)
```sql
-- ❌ MAL: Traer las ventas y luego hacer 1 query extra por cada cliente en Python/aplicación
SELECT * FROM sales; -- Retorna N ventas
-- Luego por cada venta ejecutas: SELECT * FROM customers WHERE id = sale.customer_id;
```
**Problema:** Genera N+1 viajes de red hacia la base de datos, destruyendo el rendimiento de la aplicación.

#### ✅ El Buen Camino: Un solo JOIN procesado en el motor relacional
```sql
-- ✅ BIEN: El motor SQL resuelve la relación en 1 sola consulta optimizada
SELECT s.id, c.full_name, s.sale_date 
FROM sales AS s
INNER JOIN customers AS c ON s.customer_id = c.id;
```

---

### Ejemplo Progresivo 2: El Producto Cartesiano Accidental (`CROSS JOIN` no deseado)

#### ❌ El Mal Camino: Olvidar la condición `ON` o usar sintaxis antigua basada en comas
```sql
-- ❌ MAL: Olvidar el ON genera un producto cartesiano (Multiplica todas las filas de A por todas las de B)
SELECT g.title, p.name 
FROM games g, platforms p; -- Si hay 5 juegos y 4 plataformas, retorna 20 filas inservibles
```

#### ✅ El Buen Camino: Usar sintaxis explícita `JOIN ... ON`
```sql
-- ✅ BIEN: La sintaxis moderna explicita la condicion de cruce y previene errores
SELECT g.title, p.name 
FROM games AS g
INNER JOIN platforms AS p ON g.platform_id = p.id;
```

---

## 6. Nota sobre `RIGHT JOIN` y `FULL OUTER JOIN` en SQLite

> ⚠️ **Limitación de SQLite:** SQLite no soporta nativamente la sintaxis `RIGHT JOIN` ni `FULL OUTER JOIN`.
> - Para hacer un `RIGHT JOIN`, simplemente invierte el orden de las tablas en la consulta y usa `LEFT JOIN`.
> - Para simular un `FULL OUTER JOIN`, se combina un `LEFT JOIN` con una operación `UNION` (tema que veremos en el Cap 08).

---

## 7. Mapa de Ejercicios

Dirígete a la carpeta `quests/04-joins/`:

- [[01-join-practice.md]] (Tipo A: Escribir consultas complejas combinando 3 o más tablas con alias)
- [[02-spaced-repetition.md]] (Tipo B: Repaso de capítulos 00-03 + ejercicios avanzados de JOINs y Self-Joins)

```text
subjects/sql/chronicles/SQL-BASICO/quests/04-joins/
├── 01-join-practice.md
└── 02-spaced-repetition.md
```
