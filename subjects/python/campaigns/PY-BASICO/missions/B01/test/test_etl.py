import pytest


from src.etl import normalize_logs_date, parse_log_line

# Test Case 1: The log parser correctly handles dates and times, converting string formatted datetime into standardized ISO-8601 strings.


def test_normalize_date_yyyy_mm_dd_T_H_M_S():
    """Test ISO format YYYY-MM-DDTH:M:S.f converts to ISO-8601."""
    assert normalize_logs_date(
        "2023-12-31T10:22:43.258500") == "2023-12-31T10:22:43"


def test_normalize_date_dd_mm_yyyy_H_M_S():
    """Test ISO format dd-mm-yyyy H:M:S. converts to ISO-8601."""
    assert normalize_logs_date("17-04-2026 10:22:26") == "2026-04-17T10:22:26"


def test_normalize_date_unknown_format_raise():
    """Test that invalid date format raises ValueError."""
    with pytest.raises(ValueError, match="Unknown date format"):
        normalize_logs_date("ERROR")


# Test Case 2: The parsing loop appropriately catches index or casting errors on malformed lines and continues execution without crashing.

def test_validation_line_dict():
    """Test that validated if have log error or empty values"""
    assert parse_log_line("2026-04-17T10:00:24.140000,/home,400,1120") == {
        "timestamp": '2026-04-17T10:00:24',
        "endpoint": '/home',
        "status_code": 400,
        "response_time_ms": 1120
    }


def test_validation_line_dict_error_log():
    """Test that invalid error log"""
    with pytest.raises(ValueError, match="Error log"):
        parse_log_line(
            "ERROR: CONNECTION RESET BY PEER at 2026-04-17T10:00:38.654000")


def test_validation_line_dict_invalide_value():
    """Test that invalid value in line"""
    with pytest.raises(ValueError, match='Invalid'):
        parse_log_line(
            "2026-04-17T10:01:41.665000,/login,OK,439"
        )
    with pytest.raises(ValueError, match='Invalid'):
        parse_log_line(
            "2026-04-17T10:03:34.720000,/home,200,abv"
        )
