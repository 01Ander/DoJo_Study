
import pytest
import csv
import json
import os
import tempfile

from src.etl import LogAnalyzer


# Test Case 1: `LogAnalyzer` can be instantiated with valid file paths, and its attributes (`input_path`, `output_path`, `log_path`) are correctly stored.

def test_instantiation():
    """Test that LogAnalyzer stores paths as instance attributes."""
    analyzer = LogAnalyzer(
        input_csv="data/input.csv",
        output_json="results/report.json",
        log_path="logs/errors.log"
    )

    assert analyzer.input_csv == "data/input.csv"
    assert analyzer.output_json == "results/report.json"
    assert analyzer.log_path == "logs/errors.log"
    assert analyzer._records == []
    assert analyzer._valid_records == []


# Test Case 3: Calling a private method directly (e.g., `analyzer._load_logs()`) returns the expected `list[str]` — demonstrating that helper methods are encapsulated within the object.

def test_calling_private_method():
    """Test for calling a private method directly of LogAnalyzer returns the expected."""
    analyzer = LogAnalyzer(
        input_csv="data/transactions_raw.csv",
        output_json="results/test_out.json",
        log_path="logs/test_errors.log"
    )
    result = analyzer._load_logs()

    assert isinstance(result, list)
    assert isinstance(result[0], dict)

# Test Case 2: `LogAnalyzer.run()` processes a mock dirty CSV and produces a valid `summary_report.json` identical to the procedural pipeline output.


def test_run_pipeline_produces_valid_json():
    # 1. Instancia con paths reales
    analyzer = LogAnalyzer(
        input_csv="data/transactions_raw.csv",
        output_json="data/test_report.json",
        log_path="data/test_errors.log"
    )

    # 2. Ejecuta el pipeline completo
    analyzer.run()

    # 3. Verifica que el JSON existe y tiene datos
    import json
    with open("data/test_report.json", "r") as f:
        report = json.load(f)

    assert isinstance(report, dict)
    assert len(report) > 0  # tiene al menos una categoría
