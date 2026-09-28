import pytest
from unittest.mock import patch, MagicMock
from solution import verify_identity

def test_verify_identity_success():
    """Validates that the function returns the username when AWS API responds successfully."""
    mock_aws_response = {
        'User': {
            'UserName': 'novice-dragon-keeper'
        }
    }
    
    with patch('boto3.client') as mock_boto:
        mock_iam = MagicMock()
        mock_iam.get_user.return_value = mock_aws_response
        mock_boto.return_value = mock_iam
        
        result = verify_identity()
        
        assert result == 'novice-dragon-keeper', "The function must return the UserName extracted from the response."

def test_verify_identity_error():
    """Validates that the function catches exceptions and returns the default error message."""
    with patch('boto3.client') as mock_boto:
        mock_iam = MagicMock()
        mock_iam.get_user.side_effect = Exception("Invalid Access Key")
        mock_boto.return_value = mock_iam
        
        result = verify_identity()
        
        assert result == "Authentication failed", "The function must catch exceptions and return 'Authentication failed'."
