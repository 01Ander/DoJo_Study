import pytest
import json
from unittest.mock import patch, MagicMock
import datetime

# Mock datetime.now() to ensure tests remain deterministic
class MockDatetime(datetime.datetime):
    @classmethod
    def now(cls, tz=None):
        return cls(2026, 9, 24)

@patch('solution.datetime', MockDatetime)
@patch('boto3.client')
def test_save_diet_success(mock_boto):
    """Validates that JSON is generated properly, path is partitioned, and S3 is called."""
    from solution import save_diet
    
    mock_s3 = MagicMock()
    mock_boto.return_value = mock_s3
    
    diet = ["sulfur", "rocks"]
    result = save_diet(42, diet)
    
    expected_key = "raw/diets/2026/09/24/dragon_42.json"
    assert result == expected_key, f"Expected {expected_key}, but got {result}"
    
    mock_s3.put_object.assert_called_once()
    called_kwargs = mock_s3.put_object.call_args[1]
    
    assert called_kwargs['Bucket'] == 'dragon-food-swamp-prod', "Incorrect bucket was used."
    assert called_kwargs['Key'] == expected_key, "Key sent to S3 does not match."
    
    sent_body = json.loads(called_kwargs['Body'])
    assert sent_body['dragon_id'] == 42
    assert "sulfur" in sent_body['diet']

@patch('boto3.client')
def test_save_diet_error(mock_boto):
    """Validates that an S3 error is caught and returns None."""
    from solution import save_diet
    
    mock_s3 = MagicMock()
    mock_s3.put_object.side_effect = Exception("Access Denied")
    mock_boto.return_value = mock_s3
    
    result = save_diet(99, ["salad"])
    
    assert result is None, "If S3 raises an error, the function must return None."
