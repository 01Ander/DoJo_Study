# Ejercicio 03-01: Data Cleaning with Scalar Functions (Tipo A)

**Objetivo:** Aplicar funciones escalares de texto, fecha y manejo de nulos (`COALESCE`) para estandarizar datos sucios.

---

## Setup de Datos

```sql
CREATE TABLE raw_customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    raw_first_name TEXT,
    raw_last_name TEXT,
    signup_date TEXT,
    phone_number TEXT
);

INSERT INTO raw_customers (raw_first_name, raw_last_name, signup_date, phone_number) VALUES
('  pedro ', 'GARCIA ', '2025-03-10', '555-1234'),
('MARIA', ' lopes', '2024-11-01', NULL),
('john', 'DOE', '2026-01-15', '555-9999');
```

---

## Tareas

Escribe una consulta `SELECT` que devuelva una tabla limpia con las siguientes transformaciones:
1. `full_name`: Nombre y apellido unidos en mayúsculas y sin espacios al inicio/final (Ej: `'PEDRO GARCIA'`).
2. `cleaned_phone`: Número telefónico sustituyendo valores `NULL` por `'NO REGISTRADO'`.
3. `signup_year`: El año de registro extraído de `signup_date`.

---

<details>
<summary>👀 Ver Solución Esperada</summary>

```sql
SELECT 
    UPPER(TRIM(raw_first_name)) || ' ' || UPPER(TRIM(raw_last_name)) AS full_name,
    COALESCE(phone_number, 'NO REGISTRADO') AS cleaned_phone,
    STRFTIME('%Y', signup_date) AS signup_year
FROM raw_customers;
```
</details>
