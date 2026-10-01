import pytest
import os
import json
from unittest.mock import patch, MagicMock

# Mock S3 event
S3_EVENT = {
    "Records": [{"s3": {"bucket": {"name": "test-bucket"}, "object": {"key": "test.json"}}}]
}


@patch.dict(os.environ, {"DB_HOST": "localhost", "DB_NAME": "db", "DB_USER": "u", "DB_PASSWORD": "p"})
@patch('rds.psycopg2.connect')
@patch('extract_s3.s3_client')
def test_pipeline_success(mock_s3, mock_connect):
    """Validates the happy path: S3 -> Python -> RDS -> Commit."""

    sample_payload = {
        "warehouse_id": "WH-01",
        "item_id": "SKU-99",
        "quantity": 42
    }

    from pipeline import lambda_handler

    # Mock S3 returning valid JSON file

    mock_body = MagicMock()
    mock_body.read.return_value = json.dumps(sample_payload).encode('utf-8')
    mock_s3.get_object.return_value = {'Body': mock_body}

    # Mock PostgreSQL
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cur

    # Run the pipeline
    result = lambda_handler(S3_EVENT, {})

    # S3 verifications
    mock_s3.get_object.assert_called_once_with(
        Bucket="test-bucket", Key="test.json")

    # RDS ACID verifications
    mock_cur.execute.assert_called_once()
    mock_conn.commit.assert_called_once()
    mock_conn.rollback.assert_not_called()
    mock_conn.close.assert_called_once()
