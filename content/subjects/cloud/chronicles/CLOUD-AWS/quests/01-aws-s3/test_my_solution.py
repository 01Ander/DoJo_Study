import pytest
import json
from unittest.mock import patch, MagicMock
import datetime


class MockDatetime(datetime.datetime):
    @classmethod
    def now(cls, tz=None):
        return cls(2026, 9, 24)

# Apply mocks to simulate S3 and freeze time


@patch('my_solution.datetime', MockDatetime)
@patch('my_solution.boto3.client')
def test_save_diet_success(mock_boto):
    from my_solution import save_diet
    mock_s3 = MagicMock()
    mock_boto.return_value = mock_s3

    diet = ["sulfur", "rocks"]

    # EXERCISE: Call save_diet(42, diet) and assert that it returns "raw/diets/2026/09/24/dragon_42.json"
    # Your code here:
    result = save_diet(42, diet)
    expected_key = 'raw/diets/2026/09/24/dragon_42.json'
    assert result == expected_key
    mock_s3.put_object.assert_called_once()
    assert mock_s3.put_object.call_args[1]['Key'] == expected_key


@patch('my_solution.boto3.client')
def test_save_diet_error(mock_boto):
    """Validates that an S3 error is caught and returns None."""
    from my_solution import save_diet
    mock_s3 = MagicMock()
    # Simulate S3 failure (e.g. Access Denied)
    mock_s3.put_object.side_effect = Exception("Access Denied")
    mock_boto.return_value = mock_s3

    # EXERCISE: Call save_diet(99, ["salad"]) and assert that it returns None
    # Your code here:
    result = save_diet(99, ['salad'])
    assert result is None
