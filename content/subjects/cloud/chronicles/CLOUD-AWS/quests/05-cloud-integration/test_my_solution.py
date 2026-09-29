# Write your E2E tests here.
# Tip: Remember to use mocks (unittest.mock.patch) to avoid real AWS calls.

import os
import pytest
import json
from unittest.mock import patch, MagicMock


@patch.dict(os.environ, {
    "DB_HOST": "localhost",
    "DB_NAME": "test_db",
    "DB_USER": "test_user",
    "DB_PASSWORD": "password"
})
@patch('my_solution.psycopg2.connect')
@patch('my_solution.boto3.client')
def test_full_pipeline(mock_boto, mock_connect):
    from my_solution import lambda_handler

    mock_s3 = MagicMock()
    mock_body = MagicMock()
    mock_body.read.return_value = json.dumps(
        {"dragon_id": 42, "meat_kg": 100}).encode('utf-8')
    mock_s3.get_object.return_value = {'Body': mock_body}
    mock_boto.return_value = mock_s3

    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cur

    mock_event = {'Records': [
        {'s3': {'bucket': {'name': 'test-bucket'}, 'object': {'key': 'test.json'}}}]}

    result = lambda_handler(mock_event, {})

    assert result['statusCode'] == 200
    mock_s3.get_object.assert_called_once()
    mock_cur.execute.assert_called_once()
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()


@patch.dict(os.environ, {
    "DB_HOST": "localhost",
    "DB_NAME": "test_db",
    "DB_USER": "test_user",
    "DB_PASSWORD": "password"
})
@patch('my_solution.psycopg2.connect')
@patch('my_solution.boto3.client')
def test_pipeline_failure_rollback(mock_boto, mock_connect):
    from my_solution import lambda_handler

    mock_s3 = MagicMock()
    mock_body = MagicMock()
    mock_body.read.return_value = json.dumps(
        {"dragon_id": 99, "meat_kg": 50}).encode('utf-8')
    mock_s3.get_object.return_value = {'Body': mock_body}
    mock_boto.return_value = mock_s3

    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cur

    mock_cur.execute.side_effect = Exception("Disk full")

    mock_event = {"Records": [
        {"s3": {"bucket": {"name": "test-bucket"}, "object": {"key": "test.json"}}}]}
    result = lambda_handler(mock_event, {})

    # Assert: Returns 500, rolls back, and closes connection
    assert result['statusCode'] == 500
    mock_conn.commit.assert_not_called()
    mock_conn.rollback.assert_called_once()
    mock_conn.close.assert_called_once()
