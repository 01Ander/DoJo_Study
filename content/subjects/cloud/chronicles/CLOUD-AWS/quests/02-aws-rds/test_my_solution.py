import pytest
from unittest.mock import patch, MagicMock
from my_solution import check_status


@patch('my_solution.psycopg2.connect')
def test_check_status_success(mock_connect):
    """Validates parameterized query and connection cleanup."""
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cur

    # Mock fetchone() return tuple
    mock_cur.fetchone.return_value = (89,)

    # EXERCISE: Call check_status(42) and assert return value
    # Make sure to also assert that mock_conn.close() was called
    # Your code here:

    from my_solution import check_status
    level = check_status(42)

    assert level == 89, "Return 89"
    mock_cur.close.assert_called_once()
    mock_conn.close.assert_called_once()


@patch('my_solution.psycopg2.connect')
def test_check_status_error_cleanup(mock_connect):
    """Validates that the connection is closed even if an error occurs."""
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cur

    # Simulate database error during execute
    mock_cur.execute.side_effect = Exception(
        "Relation dragons_health does not exist")

    # EXERCISE: Call check_status(99)
    # Assert that result is None and that mock_conn.close() was called
    # Your code here:

    from my_solution import check_status
    level = check_status(99)

    assert level is None
    mock_conn.close.assert_called_once()
