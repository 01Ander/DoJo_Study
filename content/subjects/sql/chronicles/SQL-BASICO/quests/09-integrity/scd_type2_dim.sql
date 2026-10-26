-- ============================================================================
-- Quest 09-04: Modelado Dimensional y Slowly Changing Dimensions (SCD Tipo 2)
-- Dominio: NovaPay Settlements (Liquidaciones Financieras B2B)
-- ============================================================================

PRAGMA foreign_keys = ON;

-- 1. Setup del Esquema Dimensional (Star Schema)
DROP VIEW IF EXISTS v_current_merchants;
DROP VIEW IF EXISTS v_settlement_reporting;
DROP TABLE IF EXISTS fact_settlements;
DROP TABLE IF EXISTS dim_merchants;

-- Tabla de Dimensión con soporte para SCD Tipo 2
CREATE TABLE dim_merchants (
    merchant_sk INTEGER PRIMARY KEY AUTOINCREMENT,
    merchant_id TEXT NOT NULL,           -- Natural / Business Key
    merchant_name TEXT NOT NULL,
    risk_tier TEXT NOT NULL,             -- Atributo cambiante: 'LOW', 'MEDIUM', 'HIGH'
    fee_rate REAL NOT NULL,              -- Atributo cambiante: Comisión aplicada (e.g., 0.02, 0.05)
    valid_from TEXT NOT NULL,            -- Fecha inicio de vigencia (YYYY-MM-DD)
    valid_to TEXT,                       -- Fecha fin de vigencia (NULL si sigue activa)
    is_current INTEGER NOT NULL CHECK(is_current IN (0, 1)) -- 1 = Activa, 0 = Histórica
);

-- Tabla de Hechos: Eventos de Liquidación Diaria
CREATE TABLE fact_settlements (
    settlement_id INTEGER PRIMARY KEY,
    merchant_id TEXT NOT NULL,
    settlement_date TEXT NOT NULL,
    gross_volume_usd REAL NOT NULL
);

-- 2. Inserción de Datos Iniciales (Seed Data)
INSERT INTO dim_merchants (merchant_sk, merchant_id, merchant_name, risk_tier, fee_rate, valid_from, valid_to, is_current) VALUES
(1, 'MKT-101', 'Solaris Market',  'LOW',    0.020, '2025-01-01', NULL, 1),
(2, 'MKT-102', 'Vortex Digital',  'MEDIUM', 0.035, '2025-01-01', NULL, 1),
(3, 'MKT-103', 'Apex Logistics',  'LOW',    0.020, '2025-01-01', NULL, 1);

INSERT INTO fact_settlements (settlement_id, merchant_id, settlement_date, gross_volume_usd) VALUES
(1, 'MKT-101', '2025-03-15', 10000.0), -- Ocurrida durante la vigencia de risk_tier = 'LOW' (tasa 2%)
(2, 'MKT-102', '2025-04-10', 20000.0), -- MKT-102 en risk_tier = 'MEDIUM' (tasa 3.5%)
(3, 'MKT-101', '2025-07-20', 15000.0), -- Ocurrida después del cambio: debe aplicar 'HIGH' (tasa 5%)
(4, 'MKT-103', '2025-08-05',  8000.0), -- MKT-103 en risk_tier = 'LOW' (tasa 2%)
(5, 'MKT-101', '2025-09-01', 12000.0); -- Ocurrida después del cambio: debe aplicar 'HIGH' (tasa 5%)


-- ============================================================================
-- DESAFÍO 1: Transición SCD Tipo 2 (Evolución de Atributos)
-- Objetivo: El '2025-07-01', 'MKT-101' sube a risk_tier = 'HIGH' y fee_rate = 0.050.
-- Pasos:
--   1. Iniciar transacción con BEGIN TRANSACTION;
--   2. Expirar la versión activa de 'MKT-101':
--      SET valid_to = '2025-07-01', is_current = 0 WHERE merchant_id = 'MKT-101' AND is_current = 1;
--   3. Insertar la nueva versión activa con:
--      merchant_id = 'MKT-101', merchant_name = 'Solaris Market', risk_tier = 'HIGH',
--      fee_rate = 0.050, valid_from = '2025-07-01', valid_to = NULL, is_current = 1.
--   4. Confirmar con COMMIT;
-- ============================================================================

-- TODO: Escribe tu bloque DML de transición SCD Tipo 2 aquí:
-- BEGIN TRANSACTION;
-- ...
-- COMMIT;
BEGIN TRANSACTION;

UPDATE dim_merchants
SET valid_to = '2025-07-01', is_current = 0 WHERE merchant_id = 'MKT-101' AND is_current = 1;

INSERT INTO dim_merchants (
    merchant_id,
    merchant_name,
    risk_tier,
    fee_rate,
    valid_from,
    valid_to,
    is_current
) VALUES (
    'MKT-101',
    'Solaris Market',
    'HIGH',
    0.050,
    '2025-07-01',
    NULL,
    1
);

COMMIT;

-- ============================================================================
-- DESAFÍO 2: Vista Analítica Point-in-Time (v_settlement_reporting)
-- Objetivo: Unir fact_settlements con dim_merchants usando la ventana temporal de vigencia.
-- Columnas requeridas:
--   - settlement_id
--   - settlement_date
--   - merchant_id
--   - merchant_name
--   - risk_tier (histórico vigente al momento del hecho)
--   - gross_volume_usd
--   - fee_rate (histórico vigente al momento del hecho)
--   - fee_amount_usd (ROUND(gross_volume_usd * fee_rate, 2))
-- Regla de Join:
--   ON f.merchant_id = d.merchant_id
--  AND f.settlement_date >= d.valid_from
--  AND (f.settlement_date < d.valid_to OR d.valid_to IS NULL)
-- Orden: settlement_id ASC
-- ============================================================================

-- TODO: Reemplaza la consulta dummy de la vista v_settlement_reporting:
CREATE VIEW v_settlement_reporting AS
SELECT
    f.settlement_id,
    f.settlement_date,
    f.merchant_id,
    d.merchant_name,
    d.risk_tier,
    f.gross_volume_usd,
    d.fee_rate,
    ROUND(f.gross_volume_usd * d.fee_rate, 2) AS fee_amount_usd
FROM fact_settlements AS f
JOIN dim_merchants AS d
ON f.merchant_id = d.merchant_id
AND f.settlement_date >= d.valid_from
AND (f.settlement_date < d.valid_to OR d.valid_to IS NULL)
ORDER BY settlement_id ASC;

-- ============================================================================
-- DESAFÍO 3: Vista de Estado Actual de la Dimensión (v_current_merchants)
-- Objetivo: Consultar el catálogo de comercios vigentes actualmente (is_current = 1).
-- Columnas requeridas:
--   - merchant_id
--   - merchant_name
--   - risk_tier
--   - fee_rate
--   - valid_from
-- Orden: merchant_id ASC
-- ============================================================================

-- TODO: Reemplaza la consulta dummy de la vista v_current_merchants:
CREATE VIEW v_current_merchants AS
SELECT
    merchant_id,
    merchant_name,
    risk_tier,
    fee_rate,
    valid_from
FROM dim_merchants
WHERE is_current = 1
ORDER BY merchant_id ASC;