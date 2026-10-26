-- ============================================================================
-- Quest 09-03: Transacciones Explícitas, ROLLBACK y Principios ACID
-- Dominio: Bóveda de Custodia Financiera (VaultCustodian)
-- ============================================================================

PRAGMA foreign_keys = ON;

-- 1. Setup del Esquema
DROP TABLE IF EXISTS transfer_logs;
DROP TABLE IF EXISTS vault_accounts;

CREATE TABLE vault_accounts (
    id INTEGER PRIMARY KEY,
    account_number TEXT NOT NULL UNIQUE,
    holder_name TEXT NOT NULL,
    balance_usd REAL NOT NULL
);

CREATE TABLE transfer_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_account TEXT NOT NULL,
    receiver_account TEXT NOT NULL,
    amount REAL NOT NULL,
    status TEXT NOT NULL,
    executed_at TEXT NOT NULL DEFAULT (DATETIME('now'))
);

-- 2. Inserción de Datos Iniciales
INSERT INTO vault_accounts (id, account_number, holder_name, balance_usd) VALUES
(1, 'VAULT-001', 'Saturn Holdings', 1000.0),
(2, 'VAULT-002', 'Neptune Capital',  500.0),
(3, 'VAULT-003', 'Jupiter Treasury',  200.0);


-- ============================================================================
-- TRANSACCIÓN 1: Transferencia Atómica Confirmada (COMMIT)
-- Objetivo: Transferir $300.0 de 'VAULT-001' a 'VAULT-002'.
-- Pasos:
--   1. Iniciar transacción con BEGIN TRANSACTION;
--   2. Restar 300.0 del balance de 'VAULT-001'.
--   3. Sumar 300.0 al balance de 'VAULT-002'.
--   4. Insertar un registro en 'transfer_logs' con:
--      sender_account = 'VAULT-001', receiver_account = 'VAULT-002',
--      amount = 300.0, status = 'CONFIRMED'
--   5. Confirmar permanentemente con COMMIT;
-- ============================================================================

-- TODO: Escribe tu bloque transaccional 1 aquí abajo:
-- BEGIN TRANSACTION;
-- ...
-- COMMIT;
BEGIN TRANSACTION;

UPDATE vault_accounts SET balance_usd = balance_usd - 300.0 WHERE account_number = 'VAULT-001';

UPDATE vault_accounts SET balance_usd = balance_usd + 300.0 WHERE account_number = 'VAULT-002';

INSERT INTO transfer_logs (sender_account, receiver_account, amount, status) VALUES ('VAULT-001', 'VAULT-002', 300.0, 'CONFIRMED');

COMMIT;


-- ============================================================================
-- TRANSACCIÓN 2: Retiro Abortado por Infracción / Reversión (ROLLBACK)
-- Objetivo: Simular un retiro no autorizado de $500.0 de 'VAULT-003' (saldo $200.0).
-- Pasos:
--   1. Iniciar transacción con BEGIN TRANSACTION;
--   2. Modificar el balance de 'VAULT-003' restando $500.0 (o intentar la deducción).
--   3. Ejecutar ROLLBACK; para cancelar de inmediato todas las mutaciones.
--   4. Verificar que el saldo de 'VAULT-003' permanezca intacto en $200.0.
-- ============================================================================

-- TODO: Escribe tu bloque transaccional 2 aquí abajo:
-- BEGIN TRANSACTION;
-- ...
-- ROLLBACK;

BEGIN TRANSACTION;

UPDATE vault_accounts SET balance_usd = balance_usd - 500.0 WHERE account_number = 'VAULT-003';

ROLLBACK;

-- ============================================================================
-- TRANSACCIÓN 3: Savepoint y Reversión Parcial (SAVEPOINT & ROLLBACK TO)
-- Objetivo: Transferir $100.0 de 'VAULT-001' a 'VAULT-003', pero descartar un cargo adicional.
-- Pasos:
--   1. Iniciar transacción con BEGIN TRANSACTION;
--   2. Restar $100.0 de 'VAULT-001' y sumar $100.0 a 'VAULT-003'.
--   3. Crear un punto de guardado: SAVEPOINT fee_step;
--   4. Intentar aplicar un recargo de seguro debitando $50.0 adicionales a 'VAULT-001'.
--   5. Revertir únicamente el recargo: ROLLBACK TO fee_step;
--   6. Liberar el savepoint: RELEASE SAVEPOINT fee_step;
--   7. Confirmar la operación principal: COMMIT;
-- ============================================================================

-- TODO: Escribe tu bloque transaccional 3 aquí abajo:
-- BEGIN TRANSACTION;
-- ...
-- COMMIT;
BEGIN TRANSACTION;

UPDATE vault_accounts SET balance_usd = balance_usd - 100 WHERE account_number = 'VAULT-001';

UPDATE vault_accounts SET balance_usd = balance_usd + 100 WHERE account_number = 'VAULT-003';

SAVEPOINT fee_step;

UPDATE vault_accounts SET balance_usd = balance_usd - 50.0 WHERE account_number = 'VAULT-001';

ROLLBACK TO fee_step;
RELEASE SAVEPOINT fee_step;
COMMIT;