import pytest
from src.transactions import Transaction, Income, Expense, build_transactions


def test_isinstance_of_transactions():
    income = Income(500, "2026-07-22", "Income")
    expense = Expense(200, "2026-07-23", "Expense")

    assert isinstance(income, Transaction)
    assert isinstance(expense, Transaction)
    positive = income.get_signed_amount()
    negative = expense.get_signed_amount()
    assert positive == 500
    assert negative == -200


def test_build_transactions():
    raw_data = [
        {"type": "Income", "amount": "5000", "date": "2024-01-15",
         "category": "Salary"},
        {"type": "Expense", "amount": "120.50", "date":
         "2024-01-20", "category": "Groceries"},
    ]
    result = build_transactions(raw_data)

    assert isinstance(result, list)
    assert isinstance(result[0], Income)
    assert isinstance(result[1], Expense)
    assert result[0].get_signed_amount() == 5000
    assert result[1].get_signed_amount() == -120.50
    assert result[0].category == "Salary"
