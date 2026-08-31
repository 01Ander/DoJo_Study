import pytest
from thermostat import Thermostat


def test_thermostat_increases_temperature():
    # Arrange
    temp = Thermostat()

    # ACT
    temp.increase(5.0)

    # ASSERT
    assert temp.temperature == 25.0


def test_thermostat_respects_maximum_cap():
    # ARRANGE
    temp = Thermostat()
    # ACT
    temp.increase(50.0)
    # ASSERT
    assert temp.temperature == 30.0
