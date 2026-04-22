import pytest

from src.transactions import Income, Expense, Transaction, create_transaction


# Test Case 1: Attempting to instantiate an `Income` entity with `amount = -50` raises a custom `ValueError`.

def test_income_rejects_negative_amount():
    with pytest.raises(ValueError, match="Amount must be positive"):
        Income(id=1, amount=-50, date="2026-04-22", currency="USD")


# Test Case 2: Ensure `Expense` objects store amounts as absolute positive values internally, regardless of raw input format.

def test_store_amounts_positive_values():
    value_f = Expense(id=1, amount=-25, date="2026-04-22", currency="USD")
    value_s = Expense(id=1, amount="-75", date="2026-04-22", currency="USD")

    assert value_f.amount == 25
    assert value_s.amount == 75


# Test Case 3: Both `Income` and `Expense` correctly inherit from the `Transaction` base class (`isinstance` checks).

def test_isinstance_income_expense_by_transaction():

    income = Income(id=1, amount=100, date="2026-04-22", currency="USD")
    expense = Expense(id=1, amount=50, date="2026-04-22", currency="USD")
    assert isinstance(income, Transaction)
    assert isinstance(expense, Transaction)

# Factory tests


def test_isinstance_dict_by_input_Income():
    raw_data = {"id": "1", "amount": 50, "type": "income",
                "date": "2026-04-07", "currency": "USD"}
    raw_income = create_transaction(raw_data)

    assert isinstance(raw_income, Income)


def test_isinstance_dict_by_input_Expense():
    raw_data = {"id": "1", "amount": -50, "type": "expense",
                "date": "2026-04-07", "currency": "USD"}
    raw_expense = create_transaction(raw_data)

    assert isinstance(raw_expense, Expense)


def test_unknown_type_by_input():
    with pytest.raises(ValueError, match="Unknown type by data input"):
        raw_data = {"id": "1", "amount": 50, "type": "null",
                    "date": "2026-04-07", "currency": "USD"}
        create_transaction(raw_data)
