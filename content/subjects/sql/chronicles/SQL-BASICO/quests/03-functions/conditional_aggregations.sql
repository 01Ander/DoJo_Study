-- ============================================================================
-- Quest 03-03: Agregaciones Condicionales con CASE WHEN (Pivoteo Analítico)
-- Dominio: Plataforma de Pagos Digitales y E-Commerce (FinTechPay)
-- ============================================================================

-- 1. Setup del Esquema
DROP TABLE IF EXISTS orders;

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_code TEXT NOT NULL UNIQUE,
    merchant_id INTEGER NOT NULL,
    payment_method TEXT NOT NULL, -- 'CREDIT_CARD', 'CRYPTO', 'BANK_TRANSFER'
    order_status TEXT NOT NULL,   -- 'COMPLETED', 'FAILED', 'REFUNDED'
    amount REAL NOT NULL,
    fee_amount REAL               -- Comisión administrativa
);

-- 2. Inserción de Datos de Prueba
INSERT INTO orders (order_code, merchant_id, payment_method, order_status, amount, fee_amount) VALUES
('ORD-501', 10, 'CREDIT_CARD',   'COMPLETED', 120.0, 3.60),
('ORD-502', 10, 'CREDIT_CARD',   'FAILED',     45.0, 0.00),
('ORD-503', 10, 'CRYPTO',        'COMPLETED', 300.0, 6.00),
('ORD-504', 10, 'BANK_TRANSFER', 'REFUNDED',   80.0, 2.00),
('ORD-505', 20, 'CREDIT_CARD',   'COMPLETED', 200.0, 6.00),
('ORD-506', 20, 'CREDIT_CARD',   'COMPLETED', 150.0, 4.50),
('ORD-507', 20, 'CRYPTO',        'FAILED',     90.0, 0.00),
('ORD-508', 30, 'BANK_TRANSFER', 'REFUNDED',  500.0, 10.00),
('ORD-509', 30, 'CREDIT_CARD',   'COMPLETED',  70.0, 2.10);


-- ============================================================================
-- DESAFÍO 1: Pivoteo de Estados de Órdenes y Monto Completado
-- Crear la vista 'v_merchant_status_pivot' que agrupe por 'merchant_id' y retorne:
--   - merchant_id
--   - total_orders: Total de órdenes (COUNT(*))
--   - completed_orders: Conteo de órdenes con status 'COMPLETED'
--   - failed_orders: Conteo de órdenes con status 'FAILED'
--   - refunded_orders: Conteo de órdenes con status 'REFUNDED'
--   - total_completed_amount: Suma del 'amount' únicamente para órdenes 'COMPLETED'
--                             (Si no hay completadas, debe sumar 0.0)
-- Ordenado por merchant_id ASC.
-- ============================================================================
DROP VIEW IF EXISTS v_merchant_status_pivot;
CREATE VIEW v_merchant_status_pivot AS
-- TODO: Reemplaza este SELECT dummy con tu consulta de agregación condicional
SELECT
    merchant_id,
    COUNT(*) AS total_orders,
    SUM(CASE WHEN order_status = 'COMPLETED' THEN 1 ELSE 0 END) AS completed_orders,
    SUM(CASE WHEN order_status = 'FAILED' THEN 1 ELSE 0 END) AS failed_orders,
    SUM(CASE WHEN order_status = 'REFUNDED' THEN 1 ELSE 0 END) AS refunded_orders,
    SUM(CASE WHEN order_status = 'COMPLETED' THEN amount ELSE 0 END) AS total_completed_amount
FROM orders
GROUP BY merchant_id
ORDER BY merchant_id ASC;


-- ============================================================================
-- DESAFÍO 2: Métricas de Canal de Pago y Tasa de Éxito
-- Crear la vista 'v_merchant_payment_breakdown' que agrupe por 'merchant_id' y retorne:
--   - merchant_id
--   - credit_card_orders: Conteo de órdenes pagadas con 'CREDIT_CARD'
--   - crypto_orders: Conteo de órdenes pagadas con 'CRYPTO'
--   - success_rate_pct: Porcentaje de éxito de órdenes 'COMPLETED' sobre el total,
--                       redondeado a 1 decimal (ej: ROUND(... / COUNT(*) * 100.0, 1)).
--                       Asegúrate de usar flotantes para evitar división entera.
-- Ordenado por merchant_id ASC.
-- ============================================================================
DROP VIEW IF EXISTS v_merchant_payment_breakdown;
CREATE VIEW v_merchant_payment_breakdown AS
-- TODO: Reemplaza este SELECT dummy con tu consulta calculando canales y ratio
SELECT
    merchant_id,
    SUM(CASE WHEN payment_method = 'CREDIT_CARD' THEN 1 ELSE 0 END) AS credit_card_orders,
    SUM(CASE WHEN payment_method = 'CRYPTO' THEN 1 ELSE 0 END) AS crypto_orders,
    ROUND(
        SUM(CASE WHEN order_status = 'COMPLETED' THEN 1.0 ELSE 0 END) / COUNT(*) * 100.0, 1) AS success_rate_pct
FROM orders
GROUP BY merchant_id
ORDER BY merchant_id ASC;
