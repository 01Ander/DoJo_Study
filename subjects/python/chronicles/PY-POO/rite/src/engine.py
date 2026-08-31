from src.transactions import Transaction
from collections import defaultdict


class AnalyticsEngine:
    def calculate_report(self, transactions: list[Transaction]) -> dict:
        category_totals = defaultdict(float)

        for txn in transactions:
            category_totals[txn.category] += txn.get_signed_amount()
        return dict(category_totals)
