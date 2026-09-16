import pytest
from profile import UserProfile


@pytest.fixture
def new_profile():
    return UserProfile('john_doe')


def test_initial_followers_is_zero(new_profile):
    assert new_profile.followers == 0


def test_add_follower_increases_count(new_profile):
    new_profile.add_follower()
    assert new_profile.followers == 1
