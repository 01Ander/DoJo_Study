import pytest
from unittest.mock import patch, MagicMock
from solution import check_status

@patch('solution.psycopg2.connect')
def test_check_status_success(mock_connect):
    """Validates that the query is parameterized, returns data, and cleans up resources."""
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cur
    
    mock_cur.fetchone.return_value = (89,)
    
    result = check_status(42)
    
    assert result == 89, "Should return 89 converted to an integer"
    
    mock_cur.execute.assert_called_once()
    execute_args = mock_cur.execute.call_args[0]
    assert execute_args[1] == (42,), "dragon_id must be passed as a safe parameter to execute()"
    
    mock_cur.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch('solution.psycopg2.connect')
def test_check_status_error_cleanup(mock_connect):
    """Validates that the connection is closed even if an error occurs."""
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cur
    
    mock_cur.execute.side_effect = Exception("Relation dragons_health does not exist")
    
    result = check_status(99)
    
    assert result is None, "Should return None on error"
    mock_conn.close.assert_called_once()
