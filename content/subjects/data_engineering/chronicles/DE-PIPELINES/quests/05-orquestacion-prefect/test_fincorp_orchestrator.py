"""
Suite de evaluación automatizada para Misión M2 (DE-005 + DE-009):
Orquestación periódica y logging estructurado con Prefect.
"""

from unittest.mock import MagicMock, patch
import pandas as pd
import pytest

from fincorp_orchestrator import (
    SCHEDULE_CRON,
    extract_fincorp_transactions,
    fincorp_nightly_flow,
    load_fincorp_gold,
)


def test_schedule_cron_and_prefect_metadata():
    """Verifica el contrato de calendarización Cron y los decoradores @task / @flow."""
    assert SCHEDULE_CRON == "0 2 * * *", "SCHEDULE_CRON debe ser exactamente '0 2 * * *'"
    assert hasattr(extract_fincorp_transactions, "retries"), "Falta decorador @task en extract_fincorp_transactions"
    assert extract_fincorp_transactions.retries == 3, "extract_fincorp_transactions debe tener retries=3"
    assert extract_fincorp_transactions.retry_delay_seconds == 5, "retry_delay_seconds debe ser 5"
    assert hasattr(load_fincorp_gold, "name"), "Falta decorador @task en load_fincorp_gold"
    assert getattr(fincorp_nightly_flow, "name", None) == "FinCorp_Nightly_ETL", (
        "El flujo debe estar decorado con @flow(name='FinCorp_Nightly_ETL')"
    )


def test_extract_task_logs_info_and_returns_dataframe():
    """Verifica que la tarea de extracción use get_run_logger().info y retorne un DataFrame."""
    sample_data = [
        {"tx_id": "TX-100", "amount": 250.0},
        {"tx_id": "TX-101", "amount": 500.0},
    ]
    mock_logger = MagicMock()

    with patch("fincorp_orchestrator.get_run_logger", return_value=mock_logger):
        df = extract_fincorp_transactions.fn(lambda: sample_data)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert mock_logger.info.call_count >= 1
    mock_logger.warning.assert_not_called()


def test_extract_task_logs_warning_when_empty():
    """Verifica que una extracción vacía emita un warning estructurado con get_run_logger()."""
    mock_logger = MagicMock()

    with patch("fincorp_orchestrator.get_run_logger", return_value=mock_logger):
        df = extract_fincorp_transactions.fn(lambda: [])

    assert isinstance(df, pd.DataFrame)
    assert df.empty
    mock_logger.warning.assert_called_once()


def test_load_task_skips_empty_dataframe_with_warning():
    """Verifica que load_fincorp_gold no llame al loader si el DataFrame está vacío y emita warning."""
    mock_logger = MagicMock()
    mock_loader = MagicMock(return_value=0)

    with patch("fincorp_orchestrator.get_run_logger", return_value=mock_logger):
        result = load_fincorp_gold.fn(pd.DataFrame(), mock_loader)

    assert result == 0
    mock_loader.assert_not_called()
    mock_logger.warning.assert_called_once()


def test_fincorp_nightly_flow_chains_extract_and_load_end_to_end():
    """Verifica la ejecución end-to-end del flujo encadenando extracción, carga y logs estructurados."""
    sample_data = [
        {"tx_id": "TX-201", "amount": 1200.0},
        {"tx_id": "TX-202", "amount": 850.5},
        {"tx_id": "TX-203", "amount": 430.0},
    ]
    mock_logger = MagicMock()
    captured_dfs: list[pd.DataFrame] = []

    def fake_loader(df: pd.DataFrame) -> int:
        captured_dfs.append(df)
        return len(df)

    with patch("fincorp_orchestrator.get_run_logger", return_value=mock_logger):
        total = fincorp_nightly_flow(fetcher=lambda: sample_data, loader=fake_loader)

    assert total == 3
    assert len(captured_dfs) == 1
    assert len(captured_dfs[0]) == 3
    assert mock_logger.info.call_count >= 3

