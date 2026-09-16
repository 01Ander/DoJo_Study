import pytest
from payments import PaymentProcessor, ExpiredCardError


def test_charge_raises_error_for_old_cards():
    processor = PaymentProcessor()

    with pytest.raises(ExpiredCardError):
        processor.charge(2020)
