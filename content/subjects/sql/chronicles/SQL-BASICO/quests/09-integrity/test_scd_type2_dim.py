"""Validation suite for Quest 09-04: Slowly Changing Dimensions Type 2 (SCD2).

Executes scd_type2_dim.sql in an in-memory SQLite database and validates
that the SCD Type 2 dimension transition, the Point-in-Time analytical reporting view,
and the current dimension state view comply with data warehousing standards.
"""

from pathlib import Path
import sqlite3
import pytest

SQL_FILE = Path(__file__).parent / "scd_type2_dim.sql"


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


def test_scd2_dimension_transition(db_conn: sqlite3.Connection) -> None:
    """Desafío 1: Validar que dim_merchants registre correctamente el historial SCD Tipo 2."""
    cursor = db_conn.cursor()

    cursor.execute(
        "SELECT merchant_sk, merchant_id, risk_tier, fee_rate, valid_from, valid_to, is_current "
        "FROM dim_merchants WHERE merchant_id = 'MKT-101' ORDER BY merchant_sk ASC"
    )
    rows = cursor.fetchall()
    assert len(rows) == 2, (
        f"Expected exactly 2 historical versions for 'MKT-101' in dim_merchants, got {len(rows)}. "
        "Did you expire the old row and insert the new row?"
    )

    # Versión histórica anterior (expirada el 2025-07-01)
    old_version = rows[0]
    assert old_version["is_current"] == 0, "Old version of MKT-101 must have is_current = 0"
    assert old_version["valid_to"] == "2025-07-01", (
        f"Old version valid_to expected '2025-07-01', got '{old_version['valid_to']}'"
    )
    assert old_version["risk_tier"] == "LOW"
    assert old_version["fee_rate"] == pytest.approx(0.020)

    # Versión activa nueva (vigente desde 2025-07-01)
    new_version = rows[1]
    assert new_version["is_current"] == 1, "New version of MKT-101 must have is_current = 1"
    assert new_version["valid_from"] == "2025-07-01", (
        f"New version valid_from expected '2025-07-01', got '{new_version['valid_from']}'"
    )
    assert new_version["valid_to"] is None, "New active version valid_to must be NULL"
    assert new_version["risk_tier"] == "HIGH"
    assert new_version["fee_rate"] == pytest.approx(0.050)

    # Validar recuento global de activos en la dimensión
    cursor.execute("SELECT COUNT(*) AS active_count FROM dim_merchants WHERE is_current = 1")
    active_row = cursor.fetchone()
    assert active_row["active_count"] == 3, "Expected exactly 3 active merchants across the dimension"


def test_point_in_time_settlement_reporting(db_conn: sqlite3.Connection) -> None:
    """Desafío 2: Validar que v_settlement_reporting calcule comisiones con fidelidad temporal Point-in-Time."""
    cursor = db_conn.cursor()

    cursor.execute("SELECT * FROM v_settlement_reporting ORDER BY settlement_id ASC")
    rows = cursor.fetchall()
    assert len(rows) == 5, (
        f"View v_settlement_reporting expected 5 settlement rows, got {len(rows)}. "
        "Check your temporal join condition with dim_merchants."
    )

    expected_data = [
        # (id, date, merchant_id, expected_tier, expected_rate, expected_fee)
        (1, "2025-03-15", "MKT-101", "LOW",    0.020, 200.0),
        (2, "2025-04-10", "MKT-102", "MEDIUM", 0.035, 700.0),
        (3, "2025-07-20", "MKT-101", "HIGH",   0.050, 750.0),
        (4, "2025-08-05", "MKT-103", "LOW",    0.020, 160.0),
        (5, "2025-09-01", "MKT-101", "HIGH",   0.050, 600.0),
    ]

    for row, expected in zip(rows, expected_data):
        exp_id, exp_date, exp_mkt, exp_tier, exp_rate, exp_fee = expected
        assert row["settlement_id"] == exp_id, f"Row ID mismatch: expected {exp_id}, got {row['settlement_id']}"
        assert row["settlement_date"] == exp_date
        assert row["merchant_id"] == exp_mkt
        assert row["risk_tier"] == exp_tier, (
            f"Settlement {exp_id} on {exp_date} for {exp_mkt}: expected historical risk_tier '{exp_tier}', "
            f"got '{row['risk_tier']}'"
        )
        assert row["fee_rate"] == pytest.approx(exp_rate)
        assert row["fee_amount_usd"] == pytest.approx(exp_fee), (
            f"Settlement {exp_id}: expected fee_amount_usd {exp_fee}, got {row['fee_amount_usd']}"
        )


def test_current_merchants_snapshot(db_conn: sqlite3.Connection) -> None:
    """Desafío 3: Validar que v_current_merchants proyecte únicamente la versión vigente de cada comercio."""
    cursor = db_conn.cursor()

    cursor.execute("SELECT * FROM v_current_merchants ORDER BY merchant_id ASC")
    rows = cursor.fetchall()
    assert len(rows) == 3, f"View v_current_merchants expected 3 current rows, got {len(rows)}"

    merchants_by_id = {row["merchant_id"]: row for row in rows}
    assert "MKT-101" in merchants_by_id
    assert "MKT-102" in merchants_by_id
    assert "MKT-103" in merchants_by_id

    # MKT-101 debe reflejar su estado actual reclasificado (HIGH, 5%)
    mkt101 = merchants_by_id["MKT-101"]
    assert mkt101["risk_tier"] == "HIGH", f"Current MKT-101 risk_tier must be 'HIGH', got '{mkt101['risk_tier']}'"
    assert mkt101["fee_rate"] == pytest.approx(0.050)
    assert mkt101["valid_from"] == "2025-07-01"
