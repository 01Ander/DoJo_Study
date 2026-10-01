import pytest
import os
from unittest.mock import patch, MagicMock


@patch.dict(os.environ, {"DB_HOST": "localhost", "DB_NAME": "db", "DB_USER": "u", "DB_PASSWORD": "p"})
@patch('rds.psycopg2.connect')
def test_check_load_to_rds(mock_connect):
    mock_conn = MagicMock()
    mock_cur = MagicMock()

    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cur

    sample_data = {
        "warehouse_id": "WH-01",
        "item_id": "SKU-99",
        "quantity": 42
    }
    from rds import load_to_rds
    load_to_rds(sample_data)

    mock_cur.execute.assert_called_once_with(
        "INSERT INTO inventory_logs (warehouse_id, item_id, quantity) VALUES (%s, %s, %s)",
        ("WH-01", "SKU-99", 42)
    )
    mock_cur.execute.assert_called_once()
    mock_conn.commit.assert_called_once()
    mock_conn.rollback.assert_not_called()
    mock_conn.close.assert_called_once()
