# Ejercicio 08-01: Set Operations & INSERT INTO SELECT (Tipo A)

**Objetivo:** Combinar conjuntos de datos con `UNION ALL` y ejecutar transformaciones relacionales con `INSERT INTO ... SELECT`.

---

## Setup de Datos

```sql
CREATE TABLE temp_online_leads (
    full_name TEXT,
    email TEXT
);

CREATE TABLE temp_event_leads (
    full_name TEXT,
    email TEXT
);

CREATE TABLE master_contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    clean_name TEXT NOT NULL,
    clean_email TEXT NOT NULL UNIQUE,
    source TEXT NOT NULL
);

INSERT INTO temp_online_leads VALUES ('  carlos ruiz ', 'CARLOS@test.com');
INSERT INTO temp_event_leads VALUES ('diana Gomez', 'diana@test.com');
```

---

## Tareas

1. Escribe una consulta `UNION ALL` que consolide todos los prospectos de ambas tablas en una sola lista en pantalla.
2. Escribe sentencias `INSERT INTO master_contacts SELECT ...` para migrar los registros desde `temp_online_leads` y `temp_event_leads` hacia `master_contacts`, limpiando nombres a mayúsculas sin espacios (`UPPER(TRIM())`), correos a minúsculas (`LOWER()`) e indicando la fuente (`'ONLINE'` o `'EVENT'`).

---

<details>
<summary>👀 Ver Solución Esperada</summary>

```sql
-- 1. UNION ALL
SELECT full_name, email FROM temp_online_leads
UNION ALL
SELECT full_name, email FROM temp_event_leads;

-- 2. Ingestion y Transformacion ELT
INSERT INTO master_contacts (clean_name, clean_email, source)
SELECT 
    UPPER(TRIM(full_name)),
    LOWER(TRIM(email)),
    'ONLINE'
FROM temp_online_leads;

INSERT INTO master_contacts (clean_name, clean_email, source)
SELECT 
    UPPER(TRIM(full_name)),
    LOWER(TRIM(email)),
    'EVENT'
FROM temp_event_leads;
```
</details>
