# Ejercicio 02-01: CRUD Operations & Filtering (Tipo A)

**Objetivo:** Practicar consultas de filtrado con `WHERE`, ordenamiento con `ORDER BY` y modificaciones seguras con `UPDATE` y `DELETE`.

---

## Setup de Datos

Ejecuta el siguiente script de inicio:

```sql
CREATE TABLE inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT NOT NULL,
    category TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL
);

INSERT INTO inventory (item_name, category, quantity, unit_price) VALUES
('Teclado Mecanico', 'Electrónica', 15, 85.0),
('Mouse Inalambrico', 'Electrónica', 40, 25.0),
('Monitor 27', 'Electrónica', 8, 250.0),
('Silla Ergonomica', 'Muebles', 5, 180.0),
('Escritorio Madera', 'Muebles', 0, 300.0),
('Cuaderno A5', 'Papelería', 100, 4.50);
```

---

## Tareas

1. Escribe una consulta `SELECT` que devuelva los productos de la categoría `'Electrónica'` con precio unitario mayor a `50.0` USD.
2. Escribe una consulta `SELECT` para obtener los productos sin inventario (`quantity = 0`).
3. Actualiza el precio del `'Monitor 27'` a `230.0` USD (utiliza `WHERE id = 3` o `WHERE item_name = 'Monitor 27'`).
4. Elimina los artículos de la categoría `'Papelería'` de forma segura.

---
My solution:
```sql
SELECT category, unit_price
FROM inventory
WHERE category = 'Electronica' AND unit_price > 50.0;

SELECT id, item_name, quantity
FROM inventory
WHERE quantity = 0;

SELECT id, item_name, unit_price FROM inventory;
UPDATE inventory
SET unit_price = 230.0 WHERE id = 3;

DELETE FROM inventory WHERE category = 'Papeleria';

```



<details>
<summary>👀 Ver Solución Esperada</summary>

```sql
-- 1. Filtrado de electrónica con precio > 50
SELECT item_name, unit_price 
FROM inventory 
WHERE category = 'Electrónica' AND unit_price > 50.0;

-- 2. Productos sin stock
SELECT item_name FROM inventory WHERE quantity = 0;

-- 3. Actualización segura
UPDATE inventory SET unit_price = 230.0 WHERE id = 3;

-- 4. Borrado controlado
DELETE FROM inventory WHERE category = 'Papelería';
```
</details>
