# Ejercicio 09-01: Views, Indexes & ACID Transactions (Tipo A)

**Objetivo:** Crear vistas reutilizables, construir índices verificando el plan de ejecución (`EXPLAIN QUERY PLAN`) y envolver operaciones multitable en bloques transaccionales.

---

## Setup de Datos

```sql
PRAGMA foreign_keys = ON;

CREATE TABLE accounts (
    id INTEGER PRIMARY KEY,
    holder_name TEXT NOT NULL,
    balance REAL CHECK(balance >= 0)
);

INSERT INTO accounts VALUES (1, 'Alice', 500.0), (2, 'Bob', 150.0);
```

---

## Tareas

1. Escribe un bloque de transacción atómica (`BEGIN TRANSACTION ... COMMIT`) que transfiera `200.0` USD de la cuenta de Alice (ID 1) a la cuenta de Bob (ID 2).
2. Crea una vista llamada `v_wealthy_accounts` que seleccione las cuentas con balance mayor a `300.0` USD.
3. Crea un índice llamado `idx_accounts_holder` sobre la columna `holder_name` y verifica su plan de consulta con `EXPLAIN QUERY PLAN SELECT * FROM accounts WHERE holder_name = 'Alice';`.

---

<details>
<summary>👀 Ver Solución Esperada</summary>

```sql
-- 1. Transacción Atómica
BEGIN TRANSACTION;
UPDATE accounts SET balance = balance - 200.0 WHERE id = 1;
UPDATE accounts SET balance = balance + 200.0 WHERE id = 2;
COMMIT;

-- 2. Creación de Vista
CREATE VIEW v_wealthy_accounts AS
SELECT id, holder_name, balance FROM accounts WHERE balance > 300.0;

-- 3. Creación de Índice y Plan de Ejecución
CREATE INDEX idx_accounts_holder ON accounts(holder_name);

EXPLAIN QUERY PLAN 
SELECT * FROM accounts WHERE holder_name = 'Alice';
```
</details>
