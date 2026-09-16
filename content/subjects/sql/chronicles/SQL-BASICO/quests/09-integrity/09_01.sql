PRAGMA foreign_keys = ON;

CREATE TABLE accounts (
    id INTEGER PRIMARY KEY,
    holder_name TEXT NOT NULL,
    balance REAL CHECK(balance >= 0)
);

INSERT INTO accounts VALUES (1, 'Alice', 500.0), (2, 'Bob', 150.0);

BEGIN TRANSACTION;

UPDATE accounts SET balance = balance - 200.0 WHERE id = 1;
UPDATE accounts SET balance = balance + 200.0 WHERE id = 2;

COMMIT;

CREATE VIEW IF NOT EXISTS v_wealthy_accounts AS
SELECT
    holder_name,
    balance
FROM accounts
WHERE balance > 300.0;

CREATE INDEX idx_accounts_holder ON accounts(holder_name);
EXPLAIN QUERY PLAN
SELECT * FROM accounts WHERE holder_name = 'Alice';