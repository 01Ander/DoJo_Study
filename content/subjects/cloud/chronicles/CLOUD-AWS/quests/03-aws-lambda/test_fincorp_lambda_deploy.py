"""Suite evaluadora para Misión M7 (AWS-008): Empaquetado .zip y create_function en AWS Lambda."""

import io
from pathlib import Path
import sys
from unittest.mock import MagicMock
import zipfile

sys.path.insert(0, str(Path(__file__).parent))

from fincorp_lambda_deploy import (
    build_lambda_zip,
    deploy_serverless_worker,
)


def test_build_lambda_zip_creates_valid_in_memory_archive():
    code = "def lambda_handler(event, context):\n    return {'statusCode': 200}\n"
    zip_bytes = build_lambda_zip(code, filename="handler.py")

    assert isinstance(zip_bytes, bytes)
    with zipfile.ZipFile(io.BytesIO(zip_bytes), mode="r") as zf:
        assert "handler.py" in zf.namelist()
        extracted = zf.read("handler.py").decode("utf-8")
        assert extracted == code


def test_deploy_serverless_worker_invokes_create_function_with_role_and_env():
    mock_lambda = MagicMock()
    expected_arn = "arn:aws:lambda:us-east-1:123456789012:function:fincorp-gold-worker"
    mock_lambda.create_function.return_value = {"FunctionArn": expected_arn}

    zip_payload = b"PK\x03\x04fakezip"
    role_arn = "arn:aws:iam::123456789012:role/fincorp-etl-role"
    env_vars = {"GOLD_BUCKET": "fincorp-gold-lake-2026", "RDS_SECRET_ID": "prod/fincorp/rds/gold"}

    arn = deploy_serverless_worker(
        mock_lambda,
        function_name="fincorp-gold-worker",
        role_arn=role_arn,
        zip_bytes=zip_payload,
        env_vars=env_vars,
    )

    assert arn == expected_arn
    mock_lambda.create_function.assert_called_once()
    kwargs = mock_lambda.create_function.call_args.kwargs
    assert kwargs["FunctionName"] == "fincorp-gold-worker"
    assert kwargs["Runtime"] == "python3.12"
    assert kwargs["Role"] == role_arn
    assert kwargs["Handler"] == "handler.lambda_handler"
    assert kwargs["Code"] == {"ZipFile": zip_payload}
    assert kwargs["Environment"] == {"Variables": env_vars}


def test_end_to_end_zip_and_deploy_integration():
    mock_lambda = MagicMock()
    mock_lambda.create_function.return_value = {
        "FunctionArn": "arn:aws:lambda:us-east-1:123456789012:function:fincorp-e2e"
    }
    zip_bytes = build_lambda_zip("def lambda_handler(event, context): pass")
    arn = deploy_serverless_worker(
        mock_lambda,
        "fincorp-e2e",
        "arn:aws:iam::123456789012:role/fincorp-etl-role",
        zip_bytes,
        {"STAGE": "prod"},
    )
    assert arn.endswith(":function:fincorp-e2e")

