# Ejercicio 07-02: ETL Deduplication Pattern (Tipo B)

**Objetivo:** Implementar el patrón maestro de deduplicación de Data Engineering utilizando `ROW_NUMBER()` y CTEs.

---

## Setup de Datos

```sql
CREATE TABLE staging_web_clicks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    page_url TEXT NOT NULL,
    click_timestamp TEXT NOT NULL
);

-- Inserción de eventos duplicados por reconexión de red
INSERT INTO staging_web_clicks (user_id, page_url, click_timestamp) VALUES
(42, '/checkout', '2026-07-31 10:00:00'),
(42, '/checkout', '2026-07-31 10:00:01'), -- Duplicado mas reciente
(88, '/home',     '2026-07-31 10:05:00'),
(42, '/checkout', '2026-07-31 09:59:59'), -- Registro mas antiguo
(88, '/home',     '2026-07-31 10:05:05'); -- Duplicado mas reciente
```

---

## Reto

Escribe una consulta basada en una CTE (`WITH`) que utilice `ROW_NUMBER()` para particionar los registros por `user_id` y `page_url`, ordenando por `click_timestamp DESC`. Retorna únicamente la versión más reciente de cada evento por usuario (donde la posición de la ventana sea 1).

---

<details>
<summary>👀 Ver Solución Esperada</summary>

```sql
WITH RankedClicks AS (
    SELECT 
        id,
        user_id,
        page_url,
        click_timestamp,
        ROW_NUMBER() OVER(
            PARTITION BY user_id, page_url 
            ORDER BY click_timestamp DESC
        ) AS dedup_rank
    FROM staging_web_clicks
)
SELECT id, user_id, page_url, click_timestamp
FROM RankedClicks
WHERE dedup_rank = 1;
```
</details>
