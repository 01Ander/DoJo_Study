"""
Suite de Pruebas Automatizadas — Quest 06-03: De Dataclass a Pydantic BaseModel
"""

import pytest
from pydantic import ValidationError

from user_account_schema import UserAccount


def test_valid_user_account_creation():
    """Verifica que una cuenta válida se instancie correctamente con todos los valores."""
    user = UserAccount(username="alice", age=25, balance=150.75, is_active=False)
    assert user.username == "alice"
    assert user.age == 25
    assert user.balance == 150.75
    assert user.is_active is False


def test_default_is_active_is_true():
    """Verifica que is_active tome el valor por defecto True."""
    user = UserAccount(username="bob_builder", age=30, balance=0.0)
    assert user.is_active is True


def test_coercion_of_compatible_types():
    """Verifica que Pydantic realice coerción automática de tipos convertibles."""
    user = UserAccount(username="charlie", age="40", balance="99.50")
    assert user.age == 40
    assert isinstance(user.age, int)
    assert user.balance == 99.50
    assert isinstance(user.balance, float)


def test_username_too_short_raises_validation_error():
    """Verifica que usernames con menos de 3 caracteres disparen ValidationError."""
    with pytest.raises(ValidationError):
        UserAccount(username="ab", age=20, balance=10.0)


def test_underage_or_negative_balance_raises_validation_error():
    """Verifica que edades menores a 18 o balances negativos disparen ValidationError."""
    # Menor de 18
    with pytest.raises(ValidationError):
        UserAccount(username="diana", age=17, balance=10.0)

    # Balance negativo
    with pytest.raises(ValidationError):
        UserAccount(username="diana", age=22, balance=-0.01)
