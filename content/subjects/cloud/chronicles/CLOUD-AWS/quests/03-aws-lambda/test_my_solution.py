import pytest
from my_solution import lambda_handler


def test_lambda_handler_success():
    """Validates that the handler extracts nested paths from the S3 event and returns 200."""
    s3_event = {
        "Records": [
            {
                "eventSource": "aws:s3",
                "s3": {
                    "bucket": {"name": "dragon-nursery-bucket"},
                    "object": {"key": "reports/new_birth.json"}
                }
            }
        ]
    }

    # EXERCISE: Call lambda_handler(s3_event, {}) and assert:
    # 1. The result is a dictionary
    # 2. 'statusCode' is 200
    # 3. 'body' is "File reports/new_birth.json uploaded to dragon-nursery-bucket"
    # Your code here:
    response = lambda_handler(s3_event, {})

    assert isinstance(response, dict)
    assert response['statusCode'] == 200
    assert response['body'] == "File reports/new_birth.json uploaded to dragon-nursery-bucket"


def test_lambda_handler_error():
    """Validates that if the event is not in S3 format, the Lambda returns 500 without crashing."""
    invalid_event = {"some_other_thing": 123}

    # EXERCISE: Call lambda_handler(invalid_event, {}) and assert:
    # 1. 'statusCode' is 500
    # 2. 'body' is "Error"
    # Your code here:
    response = lambda_handler(invalid_event, {})

    assert isinstance(response, dict)
    assert response['statusCode'] == 500
    assert response['body'] == 'Error'
