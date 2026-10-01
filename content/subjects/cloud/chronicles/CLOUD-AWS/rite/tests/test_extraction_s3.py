import pytest
import json
from unittest.mock import patch, MagicMock


@patch('extract_s3.s3_client')
def test_extraction_from_s3(mock_s3):

    sample_payload = {
        "warehouse_id": "WH-01",
        "item_id": "SKU-99",
        "quantity": 42
    }

    mock_body = MagicMock()
    mock_body.read.return_value = json.dumps(sample_payload).encode('utf-8')
    mock_s3.get_object.return_value = {'Body': mock_body}

    from extract_s3 import extraction_from_s3

    result = extraction_from_s3(bucket="mock_bucket", key="mock_json.json")

    assert result == sample_payload
    mock_s3.get_object.assert_called_once_with(
        Bucket="mock_bucket", Key="mock_json.json")
