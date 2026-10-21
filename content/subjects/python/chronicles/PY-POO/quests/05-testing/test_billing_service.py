"""Unit tests for Cloud Storage Billing Service expressing the business contract in TDD.

Following protocol 09: Full AAA testing cycle with pytest.approx and pytest.raises.
"""

import pytest
from billing_service import StorageBillingCalculator


def test_negative_storage_raises_value_error() -> None:
    # 1. ARRANGE
    calculator = StorageBillingCalculator()

    # 2. ACT & 3. ASSERT
    with pytest.raises(ValueError, match="Storage consumption cannot be negative"):
        calculator.calculate_invoice(-10.0)


def test_zero_storage_consumption_is_free() -> None:
    # 1. ARRANGE
    calculator = StorageBillingCalculator()

    # 2. ACT
    total = calculator.calculate_invoice(0.0)

    # 3. ASSERT
    assert total == pytest.approx(0.0)


def test_tier1_standard_consumption_without_discount() -> None:
    # 1. ARRANGE
    calculator = StorageBillingCalculator()

    # 2. ACT & 3. ASSERT (<= 100 GB billed at $0.02/GB)
    assert calculator.calculate_invoice(50.0) == pytest.approx(1.00)
    assert calculator.calculate_invoice(100.0) == pytest.approx(2.00)


def test_tier2_tiered_overage_consumption() -> None:
    # 1. ARRANGE
    calculator = StorageBillingCalculator()

    # 2. ACT (200 GB: first 100 GB @ $0.02 = $2.00; next 100 GB @ $0.015 = $1.50 -> $3.50)
    total = calculator.calculate_invoice(200.0)

    # 3. ASSERT
    assert total == pytest.approx(3.50)


def test_enterprise_discount_applied_on_tiered_consumption() -> None:
    # 1. ARRANGE
    calculator = StorageBillingCalculator()

    # 2. ACT (200 GB base = $3.50; 10% enterprise discount -> $3.15)
    total = calculator.calculate_invoice(200.0, is_enterprise=True)

    # 3. ASSERT
    assert total == pytest.approx(3.15)
