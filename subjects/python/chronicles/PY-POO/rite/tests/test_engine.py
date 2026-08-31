from src.engine import AnalyticsEngine
from src.transactions import Expense
import pytest


@pytest.fixture
def engine():
    return AnalyticsEngine()


def test_calculate_report(engine):
    sample_transactions = [
        Expense(amount=100.00, date="2024-01-15",
                category="food"),
        Expense(amount=50.00, date="2024-01-15",
                category="transport"),
        Expense(amount=200.00, date="2024-01-15",
                category="food"),
    ]

    result = engine.calculate_report(sample_transactions)
    assert result["food"] == pytest.approx(-300.00)
    assert result["transport"] == pytest.approx(-50.00)
