"""Validation suite for Quest 02-03: Three-Valued Logic and NULL Semantics.

Runs the operator's SQL views against an ephemeral SQLite database and validates
contract fulfillment with clear, actionable diagnostics.
"""

from pathlib import Path
import sqlite3
import pytest

SQL_FILE = Path(__file__).parent / "null_semantics.sql"


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


def test_effective_customs_fee_calculation(db_conn: sqlite3.Connection) -> None:
    """Desafío 1: v_effective_customs_fees debe calcular customs_fee + 10.0 con fallback COALESCE."""
    cursor = db_conn.cursor()
    cursor.execute(
        "SELECT tracking_code, destination_country, effective_customs_fee "
        "FROM v_effective_customs_fees ORDER BY tracking_code ASC"
    )
    rows = cursor.fetchall()

    assert len(rows) == 7, f"Expected 7 rows in v_effective_customs_fees, got {len(rows)}"

    fee_map = {row["tracking_code"]: row["effective_customs_fee"] for row in rows}

    # TRK-1001: 25.0 + 10.0 = 35.0
    assert fee_map["TRK-1001"] == pytest.approx(35.0), "TRK-1001 fee should be 25.0 + 10.0 = 35.0"

    # TRK-1002: NULL fee -> 0.0 + 10.0 = 10.0 (COALESCE must prevent NULL contamination)
    assert fee_map["TRK-1002"] == pytest.approx(
        10.0
    ), "TRK-1002 had NULL customs_fee; COALESCE should result in 10.0"

    # TRK-1004: NULL fee -> 0.0 + 10.0 = 10.0
    assert fee_map["TRK-1004"] == pytest.approx(10.0), "TRK-1004 fee should be 10.0"


def test_unsanctioned_shipments_bypasses_not_in_null_trap(
    db_conn: sqlite3.Connection,
) -> None:
    """Desafío 2: v_unsanctioned_shipments debe eludir la trampa de 3VL y retornar 5 envíos."""
    cursor = db_conn.cursor()
    cursor.execute(
        "SELECT tracking_code, destination_country, weight_kg "
        "FROM v_unsanctioned_shipments ORDER BY tracking_code ASC"
    )
    rows = cursor.fetchall()

    if len(rows) == 0:
        pytest.fail(
            "Zero rows returned! You fell into the 3VL 'NOT IN' trap. "
            "Because sanctioned_destinations contains a NULL, NOT IN evaluates to UNKNOWN. "
            "Make sure your subquery filters 'WHERE country_code IS NOT NULL' or use 'NOT EXISTS'."
        )

    assert len(rows) == 5, f"Expected 5 unsanctioned shipments, got {len(rows)}"

    actual_codes = [row["tracking_code"] for row in rows]
    expected_codes = ["TRK-1001", "TRK-1002", "TRK-1003", "TRK-1004", "TRK-1006"]
    assert actual_codes == expected_codes, f"Expected {expected_codes}, got {actual_codes}"

    actual_countries = [row["destination_country"] for row in rows]
    assert "IRN" not in actual_countries, "Sanctioned destination IRN must not be present"
    assert "PRK" not in actual_countries, "Sanctioned destination PRK must not be present"


def test_unassigned_carriers_is_null_filter(db_conn: sqlite3.Connection) -> None:
    """Desafío 3: v_unassigned_carriers debe filtrar con IS NULL y retornar 2 envíos."""
    cursor = db_conn.cursor()
    cursor.execute(
        "SELECT tracking_code, destination_country "
        "FROM v_unassigned_carriers ORDER BY tracking_code ASC"
    )
    rows = cursor.fetchall()

    assert (
        len(rows) == 2
    ), f"Expected 2 shipments without assigned carrier (carrier_id IS NULL), got {len(rows)}"

    actual_codes = [row["tracking_code"] for row in rows]
    expected_codes = ["TRK-1003", "TRK-1005"]
    assert actual_codes == expected_codes, f"Expected {expected_codes}, got {actual_codes}"
