# Ejercicio 00-01: First Database (Tipo A)

**Objetivo:** Crear una base de datos relacional en SQLite desde la terminal de macOS, definir una tabla con tipos de datos e insertar y consultar registros.

---

## Contexto de Negocio (Domain Shifting: Gestión de Libros Electrónicos)

Trabajas para una tienda de publicaciones digitales. Necesitas crear una base de datos `ebooks.db` y registrar la información de los libros disponibles para venta.

---

## Instrucciones

1. Abre tu terminal de macOS y verifica que `sqlite3` está disponible.
2. Crea/Abre la base de datos `ebooks.db`:
   ```bash
   sqlite3 ebooks.db
   ```
3. Activa los encabezados y el modo columna:
   ```sql
   .headers on
   .mode column
   ```
4. Escribe el comando DDL para crear la tabla `books` con las siguientes columnas:
   - `id`: Entero, Clave Primaria.
   - `title`: Texto, no nulo.
   - `author`: Texto, no nulo.
   - `publication_year`: Entero.
   - `price_usd`: Decimal (REAL).
5. Inserta los siguientes 3 libros:
   - "Clean Code", de "Robert Martin", año 2008, precio 35.50
   - "The Pragmatic Programmer", de "Andrew Hunt", año 1999, precio 42.00
   - "Designing Data-Intensive Applications", de "Martin Kleppmann", año 2017, precio 49.99
6. Ejecuta un `SELECT` que muestre únicamente las columnas `title` y `price_usd`.

---

<details>
<summary>👀 Ver Solución Esperada</summary>

```sql
-- 1. Creación de la tabla
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    publication_year INTEGER,
    price_usd REAL
);

-- 2. Inserción de registros
INSERT INTO books (title, author, publication_year, price_usd) VALUES
('Clean Code', 'Robert Martin', 2008, 35.50),
('The Pragmatic Programmer', 'Andrew Hunt', 1999, 42.00),
('Designing Data-Intensive Applications', 'Martin Kleppmann', 2017, 49.99);

-- 3. Consulta de columnas específicas
SELECT title, price_usd FROM books;
```

**Output Esperado en la Consola:**
```text
title                                   price_usd
--------------------------------------  ----------
Clean Code                              35.5
The Pragmatic Programmer                42.0
Designing Data-Intensive Applications   49.99
```
</details>
