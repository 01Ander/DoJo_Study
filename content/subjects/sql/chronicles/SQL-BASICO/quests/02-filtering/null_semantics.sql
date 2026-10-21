-- ============================================================================
-- Quest 02-03: Semántica Tri-Valor de NULL, Trampa de NOT IN y COALESCE
-- Dominio: Logística de Carga Internacional (GlobalCargoExpress)
-- ============================================================================

-- 1. Setup del Esquema
DROP TABLE IF EXISTS shipments;
DROP TABLE IF EXISTS sanctioned_destinations;

CREATE TABLE shipments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tracking_code TEXT NOT NULL UNIQUE,
    destination_country TEXT NOT NULL,
    weight_kg REAL NOT NULL,
    declared_value REAL,           -- Puede ser NULL si no ha sido declarado
    customs_fee REAL,              -- Puede ser NULL si está exento o pendiente
    carrier_id INTEGER             -- Puede ser NULL si no tiene transportista asignado
);

CREATE TABLE sanctioned_destinations (
    id INTEGER PRIMARY KEY,
    country_code TEXT              -- Contiene códigos de país y un NULL deliberado
);

-- 2. Inserción de Datos de Prueba
INSERT INTO shipments (tracking_code, destination_country, weight_kg, declared_value, customs_fee, carrier_id) VALUES
('TRK-1001', 'CAN', 12.5, 300.0, 25.0, 101),
('TRK-1002', 'MEX', 4.0, 120.0, NULL, 102),
('TRK-1003', 'FRA', 45.0, NULL, 80.0, NULL),
('TRK-1004', 'DEU', 8.2, 210.0, NULL, 101),
('TRK-1005', 'IRN', 15.0, 450.0, 50.0, NULL),
('TRK-1006', 'JPN', 2.5, 90.0, 15.0, 103),
('TRK-1007', 'PRK', 30.0, 800.0, 120.0, 104);

INSERT INTO sanctioned_destinations (id, country_code) VALUES
(1, 'IRN'),
(2, 'PRK'),
(3, NULL); -- ⚠️ El NULL que activa la trampa de 3VL si usas NOT IN sin filtrar


-- ============================================================================
-- DESAFÍO 1: Tarifa Efectiva con COALESCE
-- Crear la vista 'v_effective_customs_fees' que retorne:
--   - tracking_code
--   - destination_country
--   - effective_customs_fee: customs_fee + 10.0 de recargo administrativo fijo.
--     (Si customs_fee es NULL, debe tratarse como 0.0, resultando en 10.0).
--   - Ordenado por tracking_code ASC.
-- ============================================================================
DROP VIEW IF EXISTS v_effective_customs_fees;
CREATE VIEW v_effective_customs_fees AS
-- TODO: Reemplaza este SELECT dummy con tu consulta usando COALESCE
SELECT 
    tracking_code, 
    destination_country, 
    0.0 AS effective_customs_fee 
FROM shipments;


-- ============================================================================
-- DESAFÍO 2: Envíos No Sancionados (Eludiendo la Trampa de NOT IN con NULL)
-- Crear la vista 'v_unsanctioned_shipments' que retorne:
--   - tracking_code
--   - destination_country
--   - weight_kg
-- Para los envíos cuyo destination_country NO esté en 'sanctioned_destinations'.
-- CUIDADO: Recuerda que sanctioned_destinations contiene un NULL. Debes eludir
-- la trampa de 3VL asegurando que el subquery filtre WHERE country_code IS NOT NULL
-- (o usando NOT EXISTS).
-- Ordenado por tracking_code ASC.
-- ============================================================================
DROP VIEW IF EXISTS v_unsanctioned_shipments;
CREATE VIEW v_unsanctioned_shipments AS
-- TODO: Reemplaza este SELECT dummy con tu consulta eludiendo la trampa del NULL
SELECT 
    tracking_code, 
    destination_country, 
    weight_kg 
FROM shipments 
WHERE 1 = 0;


-- ============================================================================
-- DESAFÍO 3: Envíos sin Transportista Asignado (Filtro IS NULL)
-- Crear la vista 'v_unassigned_carriers' que retorne:
--   - tracking_code
--   - destination_country
-- Para aquellos paquetes donde carrier_id NO haya sido asignado aún.
-- Recuerda: En SQL nunca debes usar "= NULL", sino el operador adecuado.
-- Ordenado por tracking_code ASC.
-- ============================================================================
DROP VIEW IF EXISTS v_unassigned_carriers;
CREATE VIEW v_unassigned_carriers AS
-- TODO: Reemplaza este SELECT dummy con tu consulta usando IS NULL
SELECT 
    tracking_code, 
    destination_country 
FROM shipments 
WHERE 1 = 0;
