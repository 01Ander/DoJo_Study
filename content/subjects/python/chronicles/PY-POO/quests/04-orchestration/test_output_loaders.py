"""
Suite de Pruebas Automatizadas — Quest 04-03: Patrón Output Loaders y Orquestación ETL
"""

import json
from unittest.mock import Mock
import pytest

from output_loaders import (
    BaseOutputLoader,
    ConsoleOutputLoader,
    JsonFileOutputLoader,
    ManagedDataPipeline,
)


def test_base_loader_cannot_be_instantiated_directly():
    """Verifica que BaseOutputLoader sea una interfaz abstracta pura y no pueda instanciarse."""
    with pytest.raises(TypeError):
        BaseOutputLoader()


def test_console_loader_prints_and_returns_count(capsys):
    """Verifica que ConsoleOutputLoader emita los registros a stdout y retorne el total."""
    loader = ConsoleOutputLoader()
    sample_records = [
        {"item_id": "REC-01", "score": 98.5},
        {"item_id": "REC-02", "score": 87.0},
    ]

    count = loader.load(sample_records, destination="audit_log")

    assert count == 2
    captured = capsys.readouterr()
    assert "[CONSOLE:audit_log]" in captured.out
    assert "REC-01" in captured.out
    assert "REC-02" in captured.out


def test_json_file_loader_writes_valid_json(tmp_path):
    """Verifica que JsonFileOutputLoader serialice correctamente en disco con formato JSON."""
    target_file = tmp_path / "output_data.json"
    loader = JsonFileOutputLoader()
    sample_records = [
        {"code": "STAR-01", "magnitude": 4.2},
        {"code": "STAR-02", "magnitude": 1.8},
    ]

    count = loader.load(sample_records, str(target_file))

    assert count == 2
    assert target_file.exists()

    with open(target_file, "r", encoding="utf-8") as f:
        loaded_data = json.load(f)

    assert loaded_data == sample_records


def test_managed_data_pipeline_orchestrates_etl_flow():
    """Verifica mediante Mocks que el pipeline ejecute rigurosamente la secuencia Extract -> Process -> Load."""
    mock_extractor = Mock()
    mock_extractor.extract.return_value = ["raw_record_1", "raw_record_2"]

    mock_engine = Mock()
    mock_engine.process.return_value = [{"clean": 1}, {"clean": 2}]

    mock_loader = Mock(spec=BaseOutputLoader)
    mock_loader.load.return_value = 2

    pipeline = ManagedDataPipeline(
        extractor=mock_extractor,
        engine=mock_engine,
        loader=mock_loader,
    )

    result = pipeline.run(source_path="source.csv", destination_path="target.json")

    assert result == 2
    mock_extractor.extract.assert_called_once_with("source.csv")
    mock_engine.process.assert_called_once_with(["raw_record_1", "raw_record_2"])
    mock_loader.load.assert_called_once_with([{"clean": 1}, {"clean": 2}], "target.json")


def test_managed_data_pipeline_with_real_json_loader(tmp_path):
    """Verifica la integración del pipeline orquestando con una instancia real de JsonFileOutputLoader."""
    target_file = tmp_path / "pipeline_out.json"

    mock_extractor = Mock()
    mock_extractor.extract.return_value = "raw_content"

    mock_engine = Mock()
    mock_engine.process.return_value = [{"event": "login", "user": "ander"}]

    real_loader = JsonFileOutputLoader()

    pipeline = ManagedDataPipeline(
        extractor=mock_extractor,
        engine=mock_engine,
        loader=real_loader,
    )

    count = pipeline.run("dummy_source.dat", str(target_file))

    assert count == 1
    assert target_file.exists()
    with open(target_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data == [{"event": "login", "user": "ander"}]
