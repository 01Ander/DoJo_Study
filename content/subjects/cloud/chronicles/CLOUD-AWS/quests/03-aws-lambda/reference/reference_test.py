import pytest
from solution import lambda_handler

def test_lambda_handler_success():
    """Validates that the handler extracts nested paths from the S3 event and returns 200."""
    
    # Mock event identical to what AWS S3 emits internally
    s3_event = {
        "Records": [
            {
                "eventSource": "aws:s3",
                "s3": {
                    "bucket": {
                        "name": "dragon-nursery-bucket"
                    },
                    "object": {
                        "key": "reports/new_birth.json"
                    }
                }
            }
        ]
    }
    
    mock_context = {}
    result = lambda_handler(s3_event, mock_context)
    
    assert type(result) is dict, "The handler must return a dictionary."
    assert result.get('statusCode') == 200, "Must return statusCode 200 on success."
    assert result.get('body') == "File reports/new_birth.json uploaded to dragon-nursery-bucket"

def test_lambda_handler_error():
    """Validates that if the event is not in S3 format, the Lambda returns 500 without crashing."""
    
    invalid_event = {"some_other_thing": 123}
    result = lambda_handler(invalid_event, {})
    
    assert result.get('statusCode') == 500, "Must return 500 if extraction fails."
    assert result.get('body') == "Error"
