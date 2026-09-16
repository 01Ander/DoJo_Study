from src.transactions import Income, Expense, Transaction
from collections import defaultdict
from src.utils.logger import setup_logger


class AnalyticsEngine:
    def __init__(self):
        self.logger = setup_logger(name="src.analytics_engine")

    def calculate_report(self, transactions: list[Transaction]) -> dict:
        gross_income = 0.0
        total_expenses = 0.0
        for txn in transactions:
            if isinstance(txn, Income):
                gross_income += txn.amount
            elif isinstance(txn, Expense):
                total_expenses += txn.amount

        result = {
            "gross_income": gross_income,
            "total_expenses": total_expenses,
            "net_balance": gross_income - total_expenses
        }

        self.logger.info(
            f"Report: gross_income={gross_income}, "
            f"total_expenses={total_expenses}, "
            f"net_balance={gross_income - total_expenses}"
        )
        return result

    def aggregate_by_category(self, transactions: list[Transaction]) -> dict:
        category_totals: dict[str, float] = defaultdict(float)

        for txn in transactions:
            if isinstance(txn, Expense):
                category_totals[txn.category] += txn.amount

        self.logger.info(f"Categories: {dict(category_totals)}")
        return dict(category_totals)
