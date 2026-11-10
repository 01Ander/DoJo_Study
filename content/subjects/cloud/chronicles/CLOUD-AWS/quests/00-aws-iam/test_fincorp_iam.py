"""Suite evaluadora para Misión M4 (AWS-004 + AWS-010): IAM Programático y Políticas."""

import json
from pathlib import Path
import sys
from unittest.mock import MagicMock

sys.path.insert(0, str(Path(__file__).parent))

from fincorp_iam import (
    build_fincorp_least_privilege_policy,
    provision_fincorp_lambda_role,
)


def test_least_privilege_policy_structure_and_arn():
    policy = build_fincorp_least_privilege_policy("fincorp-gold-prod")
    assert isinstance(policy, dict), "Debe retornar un diccionario"
    assert policy.get("Version") == "2012-10-17"
    statements = policy.get("Statement", [])
    assert len(statements) == 2, "Debe contener exactamente 2 bloques en Statement (Allow y Deny)"


def test_least_privilege_policy_enforces_explicit_deny_on_delete():
    policy = build_fincorp_least_privilege_policy("fincorp-gold-prod")
    statements = policy["Statement"]
    allow_stmt = next(s for s in statements if s["Effect"] == "Allow")
    deny_stmt = next(s for s in statements if s["Effect"] == "Deny")

    assert set(allow_stmt["Action"]) == {"s3:GetObject", "s3:PutObject"}
    assert allow_stmt["Resource"] == "arn:aws:s3:::fincorp-gold-prod/*"
    assert deny_stmt["Action"] == ["s3:DeleteObject"] or deny_stmt["Action"] == "s3:DeleteObject"
    assert deny_stmt["Resource"] == "arn:aws:s3:::fincorp-gold-prod/*"


def test_provision_lambda_role_creates_trust_policy_and_returns_arn():
    mock_iam = MagicMock()
    expected_arn = "arn:aws:iam::123456789012:role/fincorp-etl-role"
    mock_iam.create_role.return_value = {"Role": {"RoleName": "fincorp-etl-role", "Arn": expected_arn}}

    arn = provision_fincorp_lambda_role(mock_iam, "fincorp-etl-role", "fincorp-gold-prod")

    assert arn == expected_arn
    mock_iam.create_role.assert_called_once()
    call_kwargs = mock_iam.create_role.call_args.kwargs
    assert call_kwargs["RoleName"] == "fincorp-etl-role"
    trust_doc = json.loads(call_kwargs["AssumeRolePolicyDocument"])
    assert trust_doc["Statement"][0]["Principal"] == {"Service": "lambda.amazonaws.com"}
    assert trust_doc["Statement"][0]["Action"] == "sts:AssumeRole"


def test_provision_lambda_role_attaches_inline_least_privilege_policy():
    mock_iam = MagicMock()
    mock_iam.create_role.return_value = {
        "Role": {"RoleName": "fincorp-etl-role", "Arn": "arn:aws:iam::123456789012:role/fincorp-etl-role"}
    }

    provision_fincorp_lambda_role(mock_iam, "fincorp-etl-role", "fincorp-gold-prod")

    mock_iam.put_role_policy.assert_called_once()
    put_kwargs = mock_iam.put_role_policy.call_args.kwargs
    assert put_kwargs["RoleName"] == "fincorp-etl-role"
    assert put_kwargs["PolicyName"] == "fincorp-etl-role-least-privilege"
    attached_doc = json.loads(put_kwargs["PolicyDocument"])
    assert len(attached_doc["Statement"]) == 2

