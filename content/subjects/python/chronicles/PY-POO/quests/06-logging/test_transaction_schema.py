"""
Suite de Pruebas Automatizadas — Quest 06-03: Validación de Esquemas con Pydantic
"""

import pytest
from pydantic import ValidationError

from transaction_schema import (
    TransactionPayload,
    InvalidTransactionDataError,
    validate_and_create_transaction,
)


def test_valid_transaction_creation():
    """Valida que una transacción con datos válidos se instancie correctamente y normalice la moneda."""
    tx = TransactionPayload(
        transaction_id="TX-1001",
        account_id=42,
        amount=150.50,
        currency="cop",
    )
    assert tx.transaction_id == "TX-1001"
    assert tx.account_id == 42
    assert tx.amount == 150.50
    assert tx.currency == "COP"  # Normalizado a mayúsculas


def test_default_currency_is_usd():
    """Verifica que la moneda por defecto sea USD si no se suministra."""
    tx = TransactionPayload(
        transaction_id="TX-2002",
        account_id=10,
        amount=50.0,
    )
    assert tx.currency == "USD"


def test_invalid_fields_raise_validation_error():
    """Verifica que restricciones como gt=0 y min_length arrojen ValidationError."""
    # amount menor o igual a 0
    with pytest.raises(ValidationError):
        TransactionPayload(transaction_id="TX-3003", account_id=1, amount=0.0)

    # account_id menor o igual a 0
    with pytest.raises(ValidationError):
        TransactionPayload(transaction_id="TX-3003", account_id=0, amount=10.0)

    # transaction_id con menos de 3 caracteres
    with pytest.raises(ValidationError):
        TransactionPayload(transaction_id="TX", account_id=1, amount=10.0)


def test_unsupported_currency_raises_validation_error():
    """Verifica que monedas no soportadas disparen el validador personalizado."""
    with pytest.raises(ValidationError):
        TransactionPayload(
            transaction_id="TX-4004",
            account_id=5,
            amount=99.9,
            currency="BITCOIN",
        )


def test_validate_and_create_transaction_success():
    """Verifica que el helper de validación retorne un modelo válido ante un diccionario crudo correcto."""
    raw_data = {
        "transaction_id": "TX-5005",
        "account_id": 88,
        "amount": 320.0,
        "currency": "eur",
    }
    tx = validate_and_create_transaction(raw_data)
    assert isinstance(tx, TransactionPayload)
    assert tx.currency == "EUR"
    assert tx.amount == 320.0


def test_validate_and_create_transaction_wraps_validation_error():
    """Verifica que el helper traduzca ValidationError a la excepción de dominio InvalidTransactionDataError."""
    bad_data = {
        "transaction_id": "A",
        "account_id": -5,
        "amount": -100.0,
    }
    with pytest.raises(InvalidTransactionDataError) as exc_info:
        validate_and_create_transaction(bad_data)

    # Debe ser una instancia de la excepción de dominio y contener información
    assert isinstance(exc_info.value, InvalidTransactionDataError)
