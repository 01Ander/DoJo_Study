# ETL pipeline for a sprawling application generates large web server logs.


from datetime import datetime
from collections import defaultdict
from typing import Any


def normalize_logs_date(raw_date: str) -> str:
    """
    Args:
      raw_date: Date string in format 'YYYY-MM-DDTH:M:S.f' or 'DD-MM-YYYY H:M:S'

    Returns:
      Normalized date string in ISO-8601 format 'YYYY-MM-DDTH:M:S'.

    Raises:
      ValueError: If the data string doesn't match any know format.
    """
    format_list = [
        "%Y-%m-%dT%H:%M:%S.%f",
        "%d-%m-%Y %H:%M:%S"
    ]
    for fmt in format_list:
        try:
            parsed = datetime.strptime(raw_date.strip(), fmt)
            return parsed.strftime("%Y-%m-%dT%H:%M:%S")
        except ValueError:
            continue
    raise ValueError(f"Unknown date format: '{raw_date}'")


def parse_log_line(line: str) -> dict[str, Any]:
    """
    Args:
      Attempt to parse a single log line.

    Returns:
      dict with keys: timestamp, endpoint, status_code, response_time_ms
      OR None if the line is malformed.

    Raises:
      ValueError: If the line cannot be parsed.
    """

    validate_log = {
        "timestamp": str,
        "endpoint": str,
        "status_code": int,
        "response_time_ms": int
    }
    fields = line.split(",")
    if len(fields) < 4:
        raise ValueError(f"Error log: '{fields}'")

    status_code = _safe_cast_int(fields[2], "status_code")
    response_time_ms = _safe_cast_int(fields[3], "response_time_ms")

    validate_log = {
        'timestamp': normalize_logs_date(fields[0]),
        'endpoint': fields[1],
        'status_code': status_code,
        'response_time_ms': response_time_ms
    }

    return validate_log


def _safe_cast_int(value: str, field_name: str) -> int:
    """Private function of validation values"""
    try:
        return int(value)
    except ValueError as e:
        raise ValueError(f"Invalid {field_name} '{value}': {e}")
