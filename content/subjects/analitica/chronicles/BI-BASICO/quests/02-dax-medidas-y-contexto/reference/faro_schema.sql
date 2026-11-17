-- ============================================================================
-- Faro schema — soporte para la reconciliación SQL de BI-02 y BI-03
-- ============================================================================
-- Este script NO se evalúa: solo materializa en PostgreSQL las mismas tablas
-- que construiste en Power BI (BI-00 / BI-01), para poder ejecutar
-- my_reconciliation.sql y my_time_reconciliation.sql.
--
-- Carga sugerida (desde la raíz de la chronicle):
--   1. Ejecuta este script completo: crea las tablas y llena dim_date.
--   2. \copy dim_store FROM 'quests/data/faro_stores.csv' WITH (FORMAT csv, HEADER true)
--   3. Exporta la consulta limpia fact_book_sales desde Power BI (Export data)
--      con solo estas columnas: sale_id, sale_date, store_id, units, unit_price,
--      unit_cost, amount_cop, order_status (store_name vive en dim_store).
--      Guárdala como 'quests/data/faro_sales_clean.csv' y cárgala:
--      \copy fact_book_sales FROM 'quests/data/faro_sales_clean.csv' WITH (FORMAT csv, HEADER true)
-- ============================================================================

DROP TABLE IF EXISTS fact_book_sales;
DROP TABLE IF EXISTS dim_store;
DROP TABLE IF EXISTS dim_date;

CREATE TABLE dim_store (
    store_id   TEXT PRIMARY KEY,
    store_name TEXT NOT NULL,
    city       TEXT NOT NULL,
    region     TEXT NOT NULL
);

CREATE TABLE dim_date (
    date_key     DATE PRIMARY KEY,
    year         INT  NOT NULL,
    month_number INT  NOT NULL,
    month_name   TEXT NOT NULL,
    year_month   TEXT NOT NULL
);

CREATE TABLE fact_book_sales (
    sale_id      TEXT PRIMARY KEY,
    sale_date    DATE NOT NULL REFERENCES dim_date(date_key),
    store_id     TEXT NOT NULL REFERENCES dim_store(store_id),
    units        INT  NOT NULL,
    unit_price   INT  NOT NULL,
    unit_cost    INT  NOT NULL,
    amount_cop   INT  NOT NULL,
    order_status TEXT NOT NULL
);

-- Calendario continuo 2025-01-01 .. 2026-12-31 (helper de carga, no se evalúa).
INSERT INTO dim_date (date_key, year, month_number, month_name, year_month)
SELECT CAST(DATE '2025-01-01' + i AS DATE),
       CAST(EXTRACT(YEAR FROM DATE '2025-01-01' + i) AS INT),
       CAST(EXTRACT(MONTH FROM DATE '2025-01-01' + i) AS INT),
       TO_CHAR(DATE '2025-01-01' + i, 'Mon'),
       TO_CHAR(DATE '2025-01-01' + i, 'YYYY-MM')
FROM generate_series(0, 729) AS i;
