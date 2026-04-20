import pytest
import csv
import json
import os
import tempfile

from src.etl import normalize_logs_date, parse_log_line, aggregation_logs, load_logs, export_report, process_logs, run_pipeline

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


# Test Case 3: The aggregation engine tallies accurate request counts and HTTP status totals, utilizing `defaultdict`.

def test_aggregation_yields_total_mean_count():
    """Check the aggregation engine: total endpoint by status code."""
    logs = [
        {"timestamp": "2026-04-17T10:00:24", "endpoint": "/home",
            "status_code": 200, "response_time_ms": 120},
        {"timestamp": "2026-04-17T10:00:25", "endpoint": "/api/users",
            "status_code": 200, "response_time_ms": 45},
        {"timestamp": "2026-04-17T10:00:26", "endpoint": "/home",
            "status_code": 404, "response_time_ms": 12},
        {"timestamp": "2026-04-17T10:00:27", "endpoint": "/api/users",
            "status_code": 200, "response_time_ms": 67},
        {"timestamp": "2026-04-17T10:00:28", "endpoint": "/login",
            "status_code": 500, "response_time_ms": 230},
    ]

    report = aggregation_logs(logs)

    assert report[200]["total"] == 3
    assert report[404]["total"] == 1
    assert report[500]["total"] == 1


# --------------------

@pytest.fixture
def sample_csv(tmp_path):
    """Creates a temporary CSV with know data."""
    filepath = tmp_path / "test_manifest.csv"
    filepath.write_text(
        "timestamp,endpoint,status_code,response_time_ms\n"
        "2026-04-17T10:00:08.416000,/home,400,626\n"
        "2026-04-17T10:00:11.468000,/api/v1/users,200,1195\n"
        "2026-04-17T10:00:11.973000,/api/v1/products,400,685\n"
        "2026-04-17T10:00:13.061000,/api/v1/users,200,1271\n"
        "2026-04-17T10:00:14.199000,/api/v1/users,200,1353\n"
    )
    return filepath


def test_load_logs_returns_list_of_dicts(sample_csv):
    result = load_logs(str(sample_csv))
    assert isinstance(result, list)
    assert len(result) == 5
    assert result[0] == "2026-04-17T10:00:08.416000,/home,400,626"
    assert result[2] == "2026-04-17T10:00:11.973000,/api/v1/products,400,685"
    assert result[4] == "2026-04-17T10:00:14.199000,/api/v1/users,200,1353"


# Test creation/write for export report

def test_export_report_creates_valid_json(tmp_path):
    """Aggregated stats are saved as a readable JSON file."""
    report = {
        "Fuel": {"count": 2, "total": 650.0, "mean": 325.0},
        "Rations": {"count": 1, "total": 300.0, "mean": 300.0},
    }
    output = tmp_path / "summary_report.json"

    export_report(report, str(output))

    assert output.exists()
    result = json.loads(output.read_text())
    assert result["Fuel"]["count"] == 2
    assert result["Fuel"]["total"] == 650.0
    assert result["Rations"]["mean"] == 300.0


# Test process logs validation

def test_process_logs_filters_invalid_and_writes_ignored(tmp_path):
    """Test that process_logs validates records and writes rejected lines to ignored file."""
    ignored_file = tmp_path / "ignored_logs.txt"

    raw_logs = [
        "2026-04-17T10:00:24.255000,/home,200,120",  # String CSV
        "2026-04-17T10:00:25.325000,/api/users,200,45",
        "ERROR: CONNECTION RESET BY PEER",  # Invalid
        "2026-04-17T10:00:26.125000,/login,OK,30",  # Invalid status
        "2026-04-17T10:00:27.158000,/home,404,12",
    ]

    valid_logs = process_logs(raw_logs, str(ignored_file))

    # Assert: 3 valid records returned
    assert len(valid_logs) == 3
    assert valid_logs[0]["status_code"] == 200  # int, not string
    assert valid_logs[0]["response_time_ms"] == 120  # int, not string

    # Assert: 2 lines written to ignored file
    ignored_content = ignored_file.read_text()
    assert "REJECTED" in ignored_content
    assert ignored_content.count("\n") == 2  # 2 rejected lines

# Test main function


def test_run_pipeline_end_to_end(tmp_path):
    """Full pipeline - from raw csv to clean json report with rejection log,"""
    # 1. Create dirty CSV with mix of valid and invalid records
    csv_file = tmp_path / "test_manifest.csv"
    csv_file.write_text(
        "timestamp,endpoint,status_code,response_time_ms\n"
        "2026-04-17T10:00:08.416000,/home,400,626\n"
        "2026-04-17T10:00:11.468000,/api/v1/users,200,1195\n"
        "ERROR: CONNECTION RESET BY PEER\n"  # Invalid line
        "2026-04-17T10:00:15.000000,/login,OK,30\n"  # Invalid status
        "2026-04-17T10:00:11.973000,/api/v1/products,400,685\n"
        "2026-04-17T10:00:13.061000,/api/v1/users,200,1271\n"
        "2026-04-17T10:00:14.199000,/api/v1/users,200,1353\n"
    )
    json_file = tmp_path / "summary_logs.json"
    log_file = tmp_path / "ignored_logs.log"

    # 2. Run the full pipeline
    run_pipeline(str(csv_file), str(json_file), str(log_file))

    # 3. Verify JSON output was created and is correct
    report = json.loads(json_file.read_text())
    assert "200" in report  # Status code 200 exists
    assert "400" in report  # Status code 400 exists
    assert report["200"]["total"] == 3  # 3 requests with status 200
    assert report["400"]["total"] == 2  # 2 requests with status 400

    # 4. Verify rejection log was created with bad records
    log_content = log_file.read_text()
    assert "REJECTED" in log_content
    assert log_content.count("\n") == 2  # 2 rejected lines
