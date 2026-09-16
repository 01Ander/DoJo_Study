import pytest
from unittest.mock import Mock
from src.pipeline import PipelineOrchestrator


def test_transactions_pipeline():
    mock_extractor = Mock()
    mock_engine = Mock()

    mock_extractor.extract.return_value = [
        {"type": "Income", "amount": "5000",
            "date": "2024-01-15", "category": "Salary"},
        {"type": "Expense", "amount": "120.50",
            "date": "2024-01-20", "category": "Groceries"},
    ]
    mock_engine.calculate_report.return_value = {
        "Salary": 5000.0,
        "Groceries": -120.50,
    }

    orchestration = PipelineOrchestrator(
        extractor=mock_extractor, engine=mock_engine)
    orchestration.run("data.csv")

    mock_extractor.extract.assert_called_once_with("data.csv")
    mock_engine.calculate_report.assert_called_once()
