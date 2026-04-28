from src.transactions import Income, Expense, Transaction
from collections import defaultdict


class AnalyticsEngine:
    def calculate_report(self, transactions: list[Transaction]) -> dict:
        gross_income = 0.0
        total_expenses = 0.0
        for txn in transactions:
            if isinstance(txn, Income):
                gross_income += txn.amount
            elif isinstance(txn, Expense):
                total_expenses += txn.amount
        return {
            "gross_income": gross_income,
            "total_expenses": total_expenses,
            "net_balance": gross_income - total_expenses
        }

    def aggregate_by_category(self, transactions: list[Transaction]) -> dict:
        category_totals: dict[str, float] = defaultdict(float)

        for txn in transactions:
            if isinstance(txn, Expense):
                category_totals[txn.category] += txn.amount

        return dict(category_totals)
