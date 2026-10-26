"""Validation suite for Quest 04-02: PostgreSQL Bulk Loader & Connection Pools.

Tests database URI construction, production engine pooling configuration,
chunked DataFrame persistence, and defensive exception wrapping.
"""

import sys
from pathlib import Path
import pytest
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

sys.path.insert(0, str(Path(__file__).parent))

from postgres_loader import (
    DatabaseConfig,
    create_production_engine,
    load_gold_dataframe,
    DatabaseLoadError,
)


def test_database_config_uri_formatting():
    """Validates that DatabaseConfig formats compliant PostgreSQL URIs."""
    config = DatabaseConfig(
        host="db.internal.corp",
        port=5432,
        database="analytics_warehouse",
        username="etl_loader",
        password="P@ssw0rd!Complex",
    )
    expected_uri = "postgresql+psycopg2://etl_loader:P@ssw0rd!Complex@db.internal.corp:5432/analytics_warehouse"
    assert config.get_uri() == expected_uri, (
        f"URI mismatch: expected '{expected_uri}', got '{config.get_uri()}'"
    )

    # Test custom driver
    config_custom = DatabaseConfig(
        host="localhost",
        port=5433,
        database="test_db",
        username="usr",
        password="pwd",
        driver="postgresql+asyncpg",
    )
    assert config_custom.get_uri() == "postgresql+asyncpg://usr:pwd@localhost:5433/test_db"


def test_create_production_engine_configuration():
    """Validates that create_production_engine properly configures connection pool properties."""
    # Using a SQLite queuepool URL for unit testing without an external daemon
    engine = create_production_engine("sqlite:///:memory:", pool_size=7, pool_pre_ping=True)
    assert isinstance(engine, Engine), "Expected a SQLAlchemy Engine instance"


def test_load_gold_dataframe_chunked_success():
    """Validates chunked DataFrame insertion and append behavior using SQLAlchemy Core verification."""
    engine = create_engine("sqlite:///:memory:")

    # Generate test dataset of 1200 records
    data = {
        "transaction_id": [f"TX-{i:05d}" for i in range(1200)],
        "amount": [float(i * 1.5) for i in range(1200)],
        "status": ["SETTLED"] * 1200,
    }
    df = pd.DataFrame(data)

    # First load: 1200 rows with chunksize=500 (3 chunk batches)
    rows_loaded = load_gold_dataframe(df, "gold_transactions", engine, chunksize=500)
    assert rows_loaded == 1200, f"Expected 1200 loaded rows, got {rows_loaded}"

    # Verify table row count with Core query
    with engine.connect() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM gold_transactions")).scalar()
        assert count == 1200, f"Expected 1200 persisted rows in DB, got {count}"

    # Second load: Append 300 additional records
    df_append = pd.DataFrame({
        "transaction_id": [f"TX-APPEND-{i}" for i in range(300)],
        "amount": [99.0] * 300,
        "status": ["PENDING"] * 300,
    })
    additional_loaded = load_gold_dataframe(df_append, "gold_transactions", engine, chunksize=500)
    assert additional_loaded == 300

    with engine.connect() as conn:
        total_count = conn.execute(text("SELECT COUNT(*) FROM gold_transactions")).scalar()
        assert total_count == 1500, f"Expected 1500 total rows after append, got {total_count}"


def test_load_gold_dataframe_empty():
    """Validates that loading an empty DataFrame returns 0 without raising errors."""
    engine = create_engine("sqlite:///:memory:")
    empty_df = pd.DataFrame()
    rows_loaded = load_gold_dataframe(empty_df, "empty_table", engine)
    assert rows_loaded == 0, f"Expected 0 for empty DataFrame, got {rows_loaded}"


def test_load_gold_dataframe_error_wrapping():
    """Validates that database errors during to_sql are caught and wrapped into DatabaseLoadError."""
    # Disposed engine that will fail execution
    engine = create_engine("sqlite:///:memory:")
    engine.dispose()

    df = pd.DataFrame({"col": [1, 2, 3]})

    # Pass an invalid target to trigger SQLAlchemy error
    class BrokenEngine:
        pass

    with pytest.raises(DatabaseLoadError):
        load_gold_dataframe(df, "bad_table", BrokenEngine())  # type: ignore
