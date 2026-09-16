"""Tests for the CLI wrapper around FinancialPipeline."""
from typer.testing import CliRunner
from pathlib import Path

from src.cli import app

runner = CliRunner()

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def test_nonexistent_input_shows_friendly_error():
    """--input-file apunta a ruta inexistente -> error amigable, sin traceback."""
    result = runner.invoke(app, [
        "--input-file", "/tmp/nonexistent_fake_XYZ.csv",
        "--output-format", "json",
    ])
    assert result.exit_code != 0
    assert "Traceback" not in result.output
    assert "exist" in result.output.lower() or "not found" in result.output.lower()


def test_output_format_restricted_to_json_csv():
    """--output-format solo acepta 'json' o 'csv'; Typer rechaza otros."""
    result = runner.invoke(app, [
        "--input-file", str(DATA_DIR / "data.csv"),
        "--output-format", "xml",
    ])
    assert result.exit_code != 0
    assert "json" in result.output.lower()
    assert "csv" in result.output.lower()


def test_successful_execution_returns_zero(tmp_path):
    """Pipeline exitoso -> exit code 0 (usando CliRunner)."""
    csv_file = tmp_path / "input.csv"
    csv_file.write_text(
        "id,date,amount,currency,type,description,category\n"
        "1,2024-01-15,5000.00,USD,Income,Mensual,Salary\n"
        "2,2024-01-20,120.50,USD,Expense,Supermercado,Groceries\n"
    )
    result = runner.invoke(app, [
        "--input-file", str(csv_file),
        "--output-format", "json",
    ])
    assert result.exit_code == 0