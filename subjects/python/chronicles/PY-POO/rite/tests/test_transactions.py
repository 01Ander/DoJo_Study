import pytest
from src.transactions import Transaction, Income, Expense


def test_isinstance_of_transactions():
    income = Income(500, "2026-07-22")
    expense = Expense(200, "2026-07-23")

    assert isinstance(income, Transaction)
    assert isinstance(expense, Transaction)
    positive = income.get_signed_amount()
    negative = expense.get_signed_amount()
    assert positive == 500
    assert negative == -200
