from pydantic import ValidationError
from src.transactions import Income, Expense
import pytest
import logging
from src.utils.logger import setup_logger
from datetime import date


def test_pydantic_rejects_invalid_types():
    with pytest.raises(ValidationError):
        Income(id='tx1', amount='wrong', date='2026-04-28', currency='USD')


def test_logger_writes_error_to_file(tmp_path):
    log_file = tmp_path / "app.log"
    logger = setup_logger(log_path=str(log_file))

    logger.error("Transaction tx1 failed validation")

    content = log_file.read_text()
    assert "Transaction tx1 failed validation" in content
    assert "ERROR" in content


def test_pydantic_validates_date_format():
    txn = Income(id='tx1', amount='100.0', date='2026-04-28', currency="USD")
    assert isinstance(txn.date, date)
    assert txn.date == date(2026, 4, 28)


def test_income_rejects_negative_amount_pydantic():
    """Income with negative amount must be raise ValidationError"""
    with pytest.raises(ValidationError):
        Income(id='tx1', amount=-25, date='2026-04-28', currency='USD')
