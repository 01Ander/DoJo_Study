"""Suite evaluadora para Misión M5 (AWS-005 + AWS-006): S3 create_bucket DNS + Parquet Snappy."""

import io
from pathlib import Path
import sys
from unittest.mock import MagicMock
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent))

from fincorp_s3_parquet import (
    provision_valid_bucket,
    upload_gold_parquet,
)


def test_provision_valid_bucket_accepts_compliant_dns_name():
    mock_s3 = MagicMock()
    result = provision_valid_bucket(mock_s3, "fincorp-gold-lake-2026")
    assert result == "fincorp-gold-lake-2026"
    mock_s3.create_bucket.assert_called_once_with(Bucket="fincorp-gold-lake-2026")


@pytest.mark.parametrize(
    "invalid_name",
    [
        "FinCorp_Upper_Underscore",
        "bucket with spaces",
        "-starts-with-hyphen",
        "ends-with-hyphen-",
        "ab",
    ],
)
def test_provision_valid_bucket_rejects_invalid_dns_names(invalid_name: str):
    mock_s3 = MagicMock()
    with pytest.raises(ValueError):
        provision_valid_bucket(mock_s3, invalid_name)
    mock_s3.create_bucket.assert_not_called()


def test_upload_gold_parquet_serializes_valid_parquet_bytes():
    mock_s3 = MagicMock()
    df = pd.DataFrame(
        [
            {"tx_id": "TX-01", "amount": 150.5, "status": "SETTLED"},
            {"tx_id": "TX-02", "amount": 320.0, "status": "SETTLED"},
        ]
    )

    byte_count = upload_gold_parquet(
        mock_s3,
        df,
        bucket_name="fincorp-gold-lake-2026",
        s3_key="gold/transactions/2026/11/04/batch.parquet",
    )

    assert isinstance(byte_count, int) and byte_count > 0
    mock_s3.put_object.assert_called_once()
    call_kwargs = mock_s3.put_object.call_args.kwargs
    assert call_kwargs["Bucket"] == "fincorp-gold-lake-2026"
    assert call_kwargs["Key"] == "gold/transactions/2026/11/04/batch.parquet"

    body_bytes = call_kwargs["Body"]
    assert isinstance(body_bytes, bytes)
    assert body_bytes[:4] == b"PAR1", "El payload subido no tiene la cabecera mágica de Apache Parquet (PAR1)"


def test_upload_gold_parquet_roundtrip_preserves_columns_without_index():
    mock_s3 = MagicMock()
    df = pd.DataFrame([{"tx_id": "TX-99", "amount": 999.99}])

    upload_gold_parquet(mock_s3, df, "fincorp-gold-lake-2026", "gold/batch.parquet")
    uploaded_bytes = mock_s3.put_object.call_args.kwargs["Body"]

    recovered_df = pd.read_parquet(io.BytesIO(uploaded_bytes))
    assert list(recovered_df.columns) == ["tx_id", "amount"]
    assert len(recovered_df) == 1
    assert recovered_df.iloc[0]["tx_id"] == "TX-99"

