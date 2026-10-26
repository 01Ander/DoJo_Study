"""Validation suite for Quest 03-03: Conditional Aggregations with CASE WHEN.

Evaluates metric pivoting and success rate ratio calculations against an
in-memory SQLite database executing the operator's SQL views.
"""

from pathlib import Path
import sqlite3
import pytest

SQL_FILE = Path(__file__).parent / "conditional_aggregations.sql"


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


def test_merchant_status_pivot_values(db_conn: sqlite3.Connection) -> None:
    """Desafío 1: v_merchant_status_pivot debe pivotear conteos de estado y sumar montos completados."""
    cursor = db_conn.cursor()
    cursor.execute(
        "SELECT merchant_id, total_orders, completed_orders, failed_orders, "
        "refunded_orders, total_completed_amount "
        "FROM v_merchant_status_pivot ORDER BY merchant_id ASC"
    )
    rows = cursor.fetchall()

    assert len(rows) == 3, f"Expected 3 merchants, got {len(rows)}"

    m_map = {row["merchant_id"]: row for row in rows}

    # Merchant 10
    m10 = m_map.get(10)
    assert m10 is not None, "Missing merchant_id 10"
    assert m10["total_orders"] == 4, f"Merchant 10 total_orders expected 4, got {m10['total_orders']}"
    assert m10["completed_orders"] == 2, f"Merchant 10 completed expected 2, got {m10['completed_orders']}"
    assert m10["failed_orders"] == 1, f"Merchant 10 failed expected 1, got {m10['failed_orders']}"
    assert m10["refunded_orders"] == 1, f"Merchant 10 refunded expected 1, got {m10['refunded_orders']}"
    assert m10["total_completed_amount"] == pytest.approx(420.0), (
        f"Merchant 10 total_completed_amount expected 420.0, got {m10['total_completed_amount']}"
    )

    # Merchant 20
    m20 = m_map.get(20)
    assert m20 is not None, "Missing merchant_id 20"
    assert m20["total_orders"] == 3
    assert m20["completed_orders"] == 2
    assert m20["failed_orders"] == 1
    assert m20["refunded_orders"] == 0
    assert m20["total_completed_amount"] == pytest.approx(350.0)

    # Merchant 30
    m30 = m_map.get(30)
    assert m30 is not None, "Missing merchant_id 30"
    assert m30["total_orders"] == 2
    assert m30["completed_orders"] == 1
    assert m30["failed_orders"] == 0
    assert m30["refunded_orders"] == 1
    assert m30["total_completed_amount"] == pytest.approx(70.0)


def test_merchant_payment_breakdown_and_success_rate(
    db_conn: sqlite3.Connection,
) -> None:
    """Desafío 2: v_merchant_payment_breakdown debe calcular canales y porcentaje de éxito."""
    cursor = db_conn.cursor()
    cursor.execute(
        "SELECT merchant_id, credit_card_orders, crypto_orders, success_rate_pct "
        "FROM v_merchant_payment_breakdown ORDER BY merchant_id ASC"
    )
    rows = cursor.fetchall()

    assert len(rows) == 3, f"Expected 3 merchants, got {len(rows)}"

    m_map = {row["merchant_id"]: row for row in rows}

    # Merchant 10: 2/4 completed = 50.0%
    m10 = m_map[10]
    assert m10["credit_card_orders"] == 2
    assert m10["crypto_orders"] == 1
    assert m10["success_rate_pct"] == pytest.approx(50.0, abs=0.1)

    # Merchant 20: 2/3 completed = 66.7%
    m20 = m_map[20]
    assert m20["credit_card_orders"] == 2
    assert m20["crypto_orders"] == 1
    assert m20["success_rate_pct"] == pytest.approx(66.7, abs=0.1)

    # Merchant 30: 1/2 completed = 50.0%
    m30 = m_map[30]
    assert m30["credit_card_orders"] == 1
    assert m30["crypto_orders"] == 0
    assert m30["success_rate_pct"] == pytest.approx(50.0, abs=0.1)
