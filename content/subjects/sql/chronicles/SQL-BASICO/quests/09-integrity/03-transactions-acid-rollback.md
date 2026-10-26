# Ejercicio 09-03: Transacciones Explícitas, ROLLBACK y Principios ACID (Nivel 4)

**Objetivo:** Implementar transacciones atómicas con `BEGIN TRANSACTION`, `COMMIT`, `ROLLBACK` y puntos de guardado parciales con `SAVEPOINT` para garantizar la integridad ACID en operaciones financieras críticas (Lore 09 §5).

---

## Contexto de Negocio (Domain Shifting: Bóveda de Custodia Financiera)

La plataforma de custodia institucional **VaultCustodian** resguarda fondos corporativos de alta cuantía en cuentas de bóveda (`vault_accounts`). La base de datos tiene una restricción inviolable de integridad: ninguna cuenta puede tener saldo negativo (`CHECK(balance_usd >= 0.0)`). 

Cuentas iniciales:
- `VAULT-001` (Saturn Holdings): `$1,000.0`
- `VAULT-002` (Neptune Capital): `$500.0`
- `VAULT-003` (Jupiter Treasury): `$200.0`

---

## Archivo de Trabajo

Edita el archivo [`transactions_acid.sql`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/quests/09-integrity/transactions_acid.sql).

Debes escribir las tres transacciones secuenciales siguiendo las especificaciones de cada desafío:

### 1. Transacción 1: Transferencia Atómica Confirmada (`COMMIT`)
Transfiere `$300.0` de `VAULT-001` a `VAULT-002`:
* Abre la transacción con `BEGIN TRANSACTION;`.
* Resta `$300.0` del `balance_usd` de `'VAULT-001'`.
* Suma `$300.0` al `balance_usd` de `'VAULT-002'`.
* Inserta un registro en `transfer_logs`:
  - `sender_account`: `'VAULT-001'`
  - `receiver_account`: `'VAULT-002'`
  - `amount`: `300.0`
  - `status`: `'CONFIRMED'`
* Confirma permanentemente con `COMMIT;`.
* *Saldos esperados tras Tx 1:* `VAULT-001` = `$700.0`, `VAULT-002` = `$800.0`.

### 2. Transacción 2: Retiro Abortado con Reversión Total (`ROLLBACK`)
Simula un retiro no autorizado o sobregiro de `$500.0` sobre `VAULT-003` (cuyo saldo es solo `$200.0`):
* Abre la transacción con `BEGIN TRANSACTION;`.
* Intenta debitar `$500.0` de `VAULT-003`: `UPDATE vault_accounts SET balance_usd = balance_usd - 500.0 WHERE account_number = 'VAULT-003';`.
* Aborta la transacción inmediatamente con `ROLLBACK;`.
* *Verificación de Integridad:* Gracias a `ROLLBACK`, el saldo de `VAULT-003` permanece inalterado en `$200.0`.

### 3. Transacción 3: Savepoint y Reversión Parcial (`SAVEPOINT` & `ROLLBACK TO`)
Procesa una transferencia principal de `$100.0` de `VAULT-001` a `VAULT-003`, pero revierte un cargo de seguro opcional:
* Abre la transacción con `BEGIN TRANSACTION;`.
* Resta `$100.0` de `'VAULT-001'` y suma `$100.0` a `'VAULT-003'`.
* Crea un punto de guardado: `SAVEPOINT fee_step;`.
* Intenta aplicar un recargo debitando `$50.0` adicionales de `'VAULT-001'`.
* El cliente declina el recargo: revierte únicamente el recargo con `ROLLBACK TO fee_step;`.
* Libera el savepoint con `RELEASE SAVEPOINT fee_step;`.
* Confirma la transferencia principal con `COMMIT;`.
* *Saldos finales:*
  - `VAULT-001`: `$600.0` (el recargo de `$50.0` fue descartado).
  - `VAULT-002`: `$800.0`
  - `VAULT-003`: `$300.0` (`$200.0` iniciales + `$100.0` recibidos en Tx 3).

---

## 🧪 Comandos de Verificación Binaria

Ejecuta la suite de pruebas unitarias:
```bash
/Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/rite/.venv/bin/pytest content/subjects/sql/chronicles/SQL-BASICO/quests/09-integrity/test_transactions_acid.py -v
```
*(Criterio de éxito: 2 passed con exit code 0).*

También puedes verificar la validez sintáctica de todo el script SQL con el runner agnóstico del DoJo:
```bash
python3 system/tools/sql_runner.py content/subjects/sql/chronicles/SQL-BASICO/quests/09-integrity/transactions_acid.sql
```

---

<details>
<summary>👀 Ver Solución de Referencia</summary>

```sql
-- Transacción 1: COMMIT
BEGIN TRANSACTION;
UPDATE vault_accounts SET balance_usd = balance_usd - 300.0 WHERE account_number = 'VAULT-001';
UPDATE vault_accounts SET balance_usd = balance_usd + 300.0 WHERE account_number = 'VAULT-002';
INSERT INTO transfer_logs (sender_account, receiver_account, amount, status)
VALUES ('VAULT-001', 'VAULT-002', 300.0, 'CONFIRMED');
COMMIT;

-- Transacción 2: ROLLBACK
BEGIN TRANSACTION;
UPDATE vault_accounts SET balance_usd = balance_usd - 500.0 WHERE account_number = 'VAULT-003';
ROLLBACK;

-- Transacción 3: SAVEPOINT & ROLLBACK TO
BEGIN TRANSACTION;
UPDATE vault_accounts SET balance_usd = balance_usd - 100.0 WHERE account_number = 'VAULT-001';
UPDATE vault_accounts SET balance_usd = balance_usd + 100.0 WHERE account_number = 'VAULT-003';
SAVEPOINT fee_step;
UPDATE vault_accounts SET balance_usd = balance_usd - 50.0 WHERE account_number = 'VAULT-001';
ROLLBACK TO fee_step;
RELEASE SAVEPOINT fee_step;
COMMIT;
```
</details>
