import pytest
import os
import json
from unittest.mock import patch, MagicMock

# Mock S3 event
S3_EVENT = {
    "Records": [{"s3": {"bucket": {"name": "test-bucket"}, "object": {"key": "test.json"}}}]
}

@patch.dict(os.environ, {"DB_HOST": "localhost", "DB_NAME": "db", "DB_USER": "u", "DB_PASSWORD": "p"})
@patch('solution.psycopg2.connect')
@patch('solution.boto3.client')
def test_pipeline_success(mock_boto, mock_connect):
    """Validates the happy path: S3 -> Python -> RDS -> Commit."""
    from solution import lambda_handler
    
    # Mock S3 returning valid JSON file
    mock_s3 = MagicMock()
    mock_body = MagicMock()
    mock_body.read.return_value = json.dumps({"dragon_id": 42, "meat_kg": 100}).encode('utf-8')
    mock_s3.get_object.return_value = {'Body': mock_body}
    mock_boto.return_value = mock_s3
    
    # Mock PostgreSQL
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cur
    
    # Run the pipeline
    result = lambda_handler(S3_EVENT, {})
    
    assert result['statusCode'] == 200, "Must return 200 on success."
    
    # S3 verifications
    mock_s3.get_object.assert_called_once_with(Bucket="test-bucket", Key="test.json")
    
    # RDS ACID verifications
    mock_cur.execute.assert_called_once()
    mock_conn.commit.assert_called_once()
    mock_conn.rollback.assert_not_called()
    mock_conn.close.assert_called_once()

@patch.dict(os.environ, {"DB_HOST": "localhost", "DB_NAME": "db", "DB_USER": "u", "DB_PASSWORD": "p"})
@patch('solution.psycopg2.connect')
@patch('solution.boto3.client')
def test_pipeline_failure_rollback(mock_boto, mock_connect):
    """Validates that if RDS crashes during insertion, the pipeline rolls back and closes."""
    from solution import lambda_handler
    
    mock_s3 = MagicMock()
    mock_body = MagicMock()
    mock_body.read.return_value = json.dumps({"dragon_id": 99}).encode('utf-8')
    mock_s3.get_object.return_value = {'Body': mock_body}
    mock_boto.return_value = mock_s3
    
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cur
    
    # Mock DB disk full exception
    mock_cur.execute.side_effect = Exception("Disk full")
    
    result = lambda_handler(S3_EVENT, {})
    
    assert result['statusCode'] == 500, "Must return 500 on failure."
    
    # Resilience verifications
    mock_conn.commit.assert_not_called()
    mock_conn.rollback.assert_called_once()
    mock_conn.close.assert_called_once()
