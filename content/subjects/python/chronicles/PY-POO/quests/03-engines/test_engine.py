import pytest
from dataclasses import dataclass


@dataclass
class User:
    age: int


class UserAnalyticsEngine:
    def get_average_age(self, users: list[User]) -> float:
        if not users:
            return 0.0
        return sum(u.age for u in users) / len(users)


@pytest.fixture
def test_data():
    return [User(age=20), User(age=30)]


def test_engine_calculates_average_age(test_data):
    engine = UserAnalyticsEngine()
    result = engine.get_average_age(test_data)
    assert result == 25.0
