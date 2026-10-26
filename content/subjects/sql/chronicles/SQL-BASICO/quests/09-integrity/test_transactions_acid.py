"""Validation suite for Quest 09-03: Explicit Transactions, ROLLBACK and ACID.

Executes transactions_acid.sql in an in-memory SQLite database and validates
that atomic commits, rollbacks, and partial savepoint rollbacks behave according
to ACID specifications.
"""

from pathlib import Path
import sqlite3
import pytest

SQL_FILE = Path(__file__).parent / "transactions_acid.sql"


@pytest.fixture(scope="module")
def db_conn() -> sqlite3.Connection:
    """Creates an in-memory SQLite database and executes the student's SQL script."""
    assert SQL_FILE.exists(), f"Missing required SQL file: {SQL_FILE}"
    sql_script = SQL_FILE.read_text(encoding="utf-8")

    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    try:
        conn.executescript(sql_script)
    except sqlite3.Error as err:
        pytest.fail(f"SQL execution failed in {SQL_FILE.name}: {err}")
    return conn


def test_transaction_1_committed_transfer(db_conn: sqlite3.Connection) -> None:
    """Transacción 1: La transferencia de $300.0 de VAULT-001 a VAULT-002 debe estar confirmada con log."""
    cursor = db_conn.cursor()

    # Verificar balance de VAULT-002 (500 + 300 = 800)
    cursor.execute("SELECT balance_usd FROM vault_accounts WHERE account_number = 'VAULT-002'")
    row = cursor.fetchone()
    assert row is not None, "Missing VAULT-002"
    assert row["balance_usd"] == pytest.approx(800.0), (
        f"VAULT-002 expected balance 800.0 after confirmed transfer, got {row['balance_usd']}"
    )

    # Verificar log de auditoría
    cursor.execute(
        "SELECT sender_account, receiver_account, amount, status FROM transfer_logs "
        "WHERE sender_account = 'VAULT-001' AND receiver_account = 'VAULT-002'"
    )
    log = cursor.fetchone()
    assert log is not None, "Missing audit log for transfer from VAULT-001 to VAULT-002"
    assert log["amount"] == pytest.approx(300.0)
    assert log["status"] == "CONFIRMED"


def test_transaction_2_and_3_savepoint_and_final_balances(
    db_conn: sqlite3.Connection,
) -> None:
    """Transacciones 2 y 3: Validar que el ROLLBACK protegió VAULT-003 y que el SAVEPOINT descartó el recargo."""
    cursor = db_conn.cursor()

    cursor.execute("SELECT account_number, balance_usd FROM vault_accounts")
    balances = {row["account_number"]: row["balance_usd"] for row in cursor.fetchall()}

    # VAULT-001: 1000 - 300 (Tx 1) - 100 (Tx 3 principal) = 600.0 (recargo de 50.0 revertido por SAVEPOINT)
    assert balances["VAULT-001"] == pytest.approx(600.0), (
        f"VAULT-001 expected balance 600.0, got {balances['VAULT-001']}. "
        "Did you rollback the $50 fee using 'ROLLBACK TO fee_step'?"
    )

    # VAULT-002: 500 + 300 (Tx 1) = 800.0
    assert balances["VAULT-002"] == pytest.approx(800.0)

    # VAULT-003: 200 (inicial) - 500 (Tx 2 revertido con ROLLBACK) + 100 (Tx 3 recibido) = 300.0
    assert balances["VAULT-003"] == pytest.approx(300.0), (
        f"VAULT-003 expected balance 300.0, got {balances['VAULT-003']}. "
        "Did you correctly execute 'ROLLBACK;' in Transaction 2?"
    )
