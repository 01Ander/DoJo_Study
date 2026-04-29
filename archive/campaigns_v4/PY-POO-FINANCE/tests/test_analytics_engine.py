from datetime import date
import pytest
from src.transactions import Income, Expense


class TestAnalyticsEngine:
    @pytest.fixture
    def engine(self):
        from src.analytics_engine import AnalyticsEngine
        return AnalyticsEngine()

    def test_empty_list_returns_zeros(self, engine):
        report = engine.calculate_report([])
        assert report["gross_income"] == 0.0
        assert report["total_expenses"] == 0.0
        assert report["net_balance"] == 0.0

    def test_net_balance_income_minus_expenses(self, engine):
        transactions = [
            Income(id="1", amount=1500.00, date=date(
                2026, 1, 10), currency="USD"),
            Expense(id="2", amount=200.00, date=date(
                2026, 1, 12), currency="USD"),
            Expense(id="3", amount=50.00, date=date(
                2026, 1, 14), currency="USD"),
        ]
        report = engine.calculate_report(transactions)
        assert report["net_balance"] == pytest.approx(1250.00)
        assert report["gross_income"] == pytest.approx(1500.00)
        assert report["total_expenses"] == pytest.approx(250.00)

    def test_aggregate_by_category_sums(self, engine):
        transactions = [
            Expense(id="1", amount=100.00, date=date(
                2026, 1, 10), currency="USD", category="food"),
            Expense(id="2", amount=50.00, date=date(
                2026, 1, 12), currency="USD", category="transport"),
            Expense(id="3", amount=200.00, date=date(
                2026, 1, 14), currency="USD", category="food"),
        ]
        by_category = engine.aggregate_by_category(transactions)
        assert by_category["food"] == pytest.approx(300.00)
        assert by_category["transport"] == pytest.approx(50.00)
