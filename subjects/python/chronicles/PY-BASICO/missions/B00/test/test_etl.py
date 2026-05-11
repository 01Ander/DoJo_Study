

import pytest
import csv
import json
import os
import tempfile

from src.etl import normalize_transaction_date, clean_currency, aggregate_transactions, load_transactions, data_validation, process_records, export_report, run_pipeline

# test/test_etl.py
"""Unit tests for the ETL module."""

# Test Case 1: The date parser successfully normalizes different date formats (e.g., `12-31-2023` and `2023/12/31`) into standard ISO-8601 (`YYYY-MM-DD`)


def test_normalize_date_mm_dd_yyyy():
    """Test American format MM-DD-YYYY converts to ISO-8601."""
    assert normalize_transaction_date("12-31-2023") == "2023-12-31"


def test_normalize_date_yyyy_mm_dd():
    """Test ISO format YYYY/MM/DD converts to ISO-8601."""
    assert normalize_transaction_date("2023/12/31") == "2023-12-31"


def test_normalize_date_with_trailing_spaces():
    """Test that leading/trailing whitespace is stripped."""
    assert normalize_transaction_date("  01-15-2024  ") == "2024-01-15"


def test_normalize_date_unknown_format_raises():
    """Test that unsupported formats raise ValueError with a message."""
    with pytest.raises(ValueError, match="Unknown date format"):
        normalize_transaction_date("31/12/2023")

# Test Case 2: The type-casting logic raises a specific custom-logged exception when finding an alphanumeric string in a currency field instead of crashing implicitly.


def test_clean_currency_with_symbols():
    assert clean_currency("$1,234.55") == 1234.55


def test_clean_currency_with_space():
    assert clean_currency(" 258.36 ") == 258.36


def test_clean_currency_alphanumeric_raises():
    with pytest.raises(ValueError):
        clean_currency("100eur")


def test_clean_currency_empty_raises():
    with pytest.raises(ValueError):
        clean_currency("")


def test_clean_currency_alpha_raises():
    with pytest.raises(ValueError):
        clean_currency("million")


# Test Case 3: The aggregation engine correctly yields the Total, Mean, and Count for an overlapping Category dict.

def test_aggregation_yields_total_mean_count():
    """Check the aggregation engine: Total, Mean, and Count by category."""
    registros = [
        {"category": "Goblin", "amount": 10.0},
        {"category": "Orco", "amount": 50.0},
        {"category": "Goblin", "amount": 20.0},
    ]
    resultados = aggregate_transactions(registros)

    assert resultados["Goblin"]["count"] == 2
    assert resultados["Goblin"]["total"] == 30.0
    assert resultados["Goblin"]["mean"] == 15.0

    assert resultados["Orco"]["count"] == 1
    assert resultados["Orco"]["total"] == 50.0
    assert resultados["Orco"]["mean"] == 50.0


# Test reader validation

@pytest.fixture
def sample_csv(tmp_path):
    """Creates a temporary CSV with know data."""
    filepath = tmp_path / "test_manifest.csv"
    filepath.write_text(
        "item,quantity,condition\n"
        "plasma_cell,150,good\n"
        "oxygen_tank,300,damaged\n"
    )
    return filepath


def test_load_inventory_returns_list_of_dicts(sample_csv):
    result = load_transactions(str(sample_csv))
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["item"] == "plasma_cell"
    assert result[0]["quantity"] == "150"
    assert result[1]["condition"] == "damaged"


# Test data validation

def test_data_validation_success():
    """Valid financial transaction passes all validation rules."""
    raw = {
        "tx_id": "TX-001",
        "timestamp": "04-15-2026",
        "amount": "$1,250.00",
        "currency": "USD",
        "category": "Consulting",
        "description": "Legal advisory services",
        "status": "completed"
    }

    result = data_validation(raw)

    assert result["timestamp"] == "2026-04-15"
    assert isinstance(result["amount"], float)
    assert result["amount"] == 1250.00
    assert result["tx_id"] == "TX-001"
    assert result["currency"] == "USD"
    assert result["category"] == "Consulting"


def test_data_validation_bad_date_raises():
    """Corrupted date — transaction rejected."""
    raw = {
        "tx_id": "TX-002",
        "timestamp": "INVALID_DATE",
        "amount": "500.00",
        "currency": "USD",
        "category": "Travel",
        "description": "Flight to conference",
        "status": "pending"
    }

    with pytest.raises(ValueError, match="Unknown date format"):
        data_validation(raw)


def test_data_validation_bad_amount_raises():
    """Corrupted amount — transaction rejected."""
    raw = {
        "tx_id": "TX-003",
        "timestamp": "04-15-2026",
        "amount": "FREE_STUFF",
        "currency": "EUR",
        "category": "Donations",
        "description": "Charitable contribution",
        "status": "completed"
    }

    with pytest.raises(ValueError):
        data_validation(raw)

# Test process records validation


def test_process_records_mix_valid_and_invalid(tmp_path):
    """Mixed financial batch — valid transactions pass, corrupt ones logged."""
    raw_records = [
        {"tx_id": "TX-001", "timestamp": "04-15-2026",
            "amount": "$500.00", "currency": "USD", "category": "Consulting"},
        {"tx_id": "TX-002", "timestamp": "BLAH_DATE",
            "amount": "$300.00", "currency": "EUR", "category": "Travel"},
        {"tx_id": "TX-003", "timestamp": "04-16-2026",
            "amount": "FREE_ITEMS", "currency": "USD", "category": "Marketing"},
        {"tx_id": "TX-004", "timestamp": "2026/04/17",
            "amount": "$150.00", "currency": "USD", "category": "Consulting"},
    ]

    log_file = tmp_path / "ignored_records.log"

    valid = process_records(raw_records, str(log_file))

    assert len(valid) == 2
    assert valid[0]["tx_id"] == "TX-001"
    assert isinstance(valid[0]["amount"], float)
    assert valid[1]["tx_id"] == "TX-004"

    # Test the log file
    log_content = log_file.read_text()
    lines = log_content.strip().split("\n")
    assert len(lines) == 2
    assert "TX-002" in lines[0]
    assert "REJECTED" in lines[0]
    assert "TX-003" in lines[1]


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

# Test main function


def test_run_pipeline_end_to_end(tmp_path):
    """Full pipeline — from raw CSV to clean JSON report with rejection log."""
    # 1. Create dirty CSV with mix of valid and invalid records
    csv_file = tmp_path / "input.csv"
    csv_file.write_text(
        "tx_id,timestamp,amount,currency,category,description,status\n"
        "TX-001,04-15-2026,$500.00,USD,Consulting,Advisory,completed\n"
        "TX-002,INVALID_DATE,$300.00,EUR,Travel,Flight,pending\n"
        "TX-003,2026/04/16,NOT_A_NUMBER,USD,Marketing,Campaign,completed\n"
        "TX-004,04-17-2026,$-250.00,USD,Consulting,Refund,refunded\n"
        "TX-005,04-18-2026,$150.00,USD,Consulting,Review,completed\n"
    )

    json_file = tmp_path / "summary_report.json"
    log_file = tmp_path / "ignored_records.log"

    # 2. Run the full pipeline
    run_pipeline(str(csv_file), str(json_file), str(log_file))

    # 3. Verify JSON output was created and is correct
    report = json.loads(json_file.read_text())
    assert "Consulting" in report
    assert report["Consulting"]["count"] == 2
    assert report["Consulting"]["total"] == 650.0

    # 4. Verify rejection log was created with bad records
    log_content = log_file.read_text()
    assert "TX-002" in log_content
    assert "TX-003" in log_content
    assert "TX-004" in log_content
    assert "REJECTED" in log_content
