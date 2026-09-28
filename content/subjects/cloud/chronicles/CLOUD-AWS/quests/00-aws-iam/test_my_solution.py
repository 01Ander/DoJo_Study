import pytest
from unittest.mock import patch, MagicMock
from my_solution import verify_identity


def test_verify_identity_success():
    """Validates that the function returns the username when AWS API responds successfully."""
    mock_aws_response = {'User': {'UserName': 'novice-dragon-keeper'}}

    with patch('my_solution.boto3.client') as mock_boto:
        mock_iam = MagicMock()
        mock_iam.get_user.return_value = mock_aws_response
        mock_boto.return_value = mock_iam

        # EXERCISE: Run verify_identity() and assert it returns the expected username
        user = verify_identity()
        assert user == 'novice-dragon-keeper'


def test_verify_identity_error():
    """Validates that the function catches the exception and returns the default error message."""
    with patch('my_solution.boto3.client') as mock_boto:
        mock_iam = MagicMock()
        mock_iam.get_user.side_effect = Exception("Invalid Access Key")
        mock_boto.return_value = mock_iam

        # EXERCISE: Run verify_identity() and assert it catches the error returning "Authentication failed"
        user = verify_identity()
        assert user == "Authentication failed"
