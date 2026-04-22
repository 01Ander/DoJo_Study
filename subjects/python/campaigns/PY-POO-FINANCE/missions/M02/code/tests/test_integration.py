"""Integration test: M01 CSV output -> M02 factory -> List[Transaction]."""
from src.transactions import Transaction, Income, Expense, map_all
import sys
import csv
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parent.parent.parent.parent / \
    "M01" / "code" / "data" / "transactions.csv"
# Add M01 to path so we can import the extractor
# M01_PATH = Path(file).resolve().parent.parent.parent / "M01" / "code"
# sys.path.insert(0, str(M01_PATH))


def load_raw_dicts():
    """Read M01 CSV and return raw dicts (what M01's extractor would yield)."""
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_m01_to_m02_full_pipeline():
    """Read real CSV from M01, feed it to M02 factory, verify all rows become valid Transactions."""
    raw_dicts = load_raw_dicts()

    # Smoke test: data exists
    assert len(raw_dicts) > 0

    transactions = map_all(raw_dicts)

    # All raw rows become Transaction instances
    assert len(transactions) == len(raw_dicts)
    assert all(isinstance(t, Transaction) for t in transactions)

    # Count by type
    incomes = [t for t in transactions if isinstance(t, Income)]
    expenses = [t for t in transactions if isinstance(t, Expense)]

    # We know the CSV has incomes and expenses
    assert len(incomes) > 0
    assert len(expenses) > 0


def test_expense_amounts_are_positive():
    """Verify Expense _post_init__ normalizes negative CSV amounts to positive."""
    raw_dicts = load_raw_dicts()
    transactions = map_all(raw_dicts)

    for t in transactions:
        if isinstance(t, Expense):
            assert t.amount >= 0, f"Expense {t.id} has negative amount: {t.amount}"
