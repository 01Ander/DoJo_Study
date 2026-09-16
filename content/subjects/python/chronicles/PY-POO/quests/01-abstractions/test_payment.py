from payment_gateway import CreditCardProcessor


def test_credit_card_processor_returns_true():
    processor = CreditCardProcessor()
    result = processor.process_payment(340)
    assert result is True
