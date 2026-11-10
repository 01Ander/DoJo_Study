"""Suite evaluadora para Misión M6 (AWS-007 + MKT-AWS-002): RDS Security Groups y Secrets Manager."""

import json
from pathlib import Path
import sys
from unittest.mock import MagicMock
import pytest

sys.path.insert(0, str(Path(__file__).parent))

from fincorp_rds_secrets import (
    RDSConfig,
    authorize_rds_ingress,
    load_rds_config_from_secrets,
)


def test_rds_config_get_uri_matches_m1_contract():
    cfg = RDSConfig(
        host="fincorp-rds.cxyz.us-east-1.rds.amazonaws.com",
        port=5432,
        database="fincorp_gold",
        username="fincorp_admin",
        password="KmsDecryptedSecret!99",
    )
    assert (
        cfg.get_uri()
        == "postgresql+psycopg2://fincorp_admin:KmsDecryptedSecret!99@fincorp-rds.cxyz.us-east-1.rds.amazonaws.com:5432/fincorp_gold"
    )


def test_load_rds_config_from_secrets_parses_secret_string():
    mock_secrets = MagicMock()
    secret_payload = {
        "host": "fincorp-rds.internal.aws",
        "port": 5432,
        "dbname": "fincorp_gold",
        "username": "etl_svc",
        "password": "RotatedPassword_2026",
    }
    mock_secrets.get_secret_value.return_value = {"SecretString": json.dumps(secret_payload)}

    cfg = load_rds_config_from_secrets(mock_secrets, "prod/fincorp/rds/gold")

    mock_secrets.get_secret_value.assert_called_once_with(SecretId="prod/fincorp/rds/gold")
    assert isinstance(cfg, RDSConfig)
    assert cfg.host == "fincorp-rds.internal.aws"
    assert cfg.database == "fincorp_gold"
    assert cfg.username == "etl_svc"
    assert cfg.password == "RotatedPassword_2026"


def test_authorize_rds_ingress_allows_private_cidr_on_port_5432():
    mock_ec2 = MagicMock()
    mock_ec2.authorize_security_group_ingress.return_value = {"Return": True}

    res = authorize_rds_ingress(mock_ec2, "sg-0123456789abcdef0", "10.20.0.0/16")

    assert res == {"Return": True}
    mock_ec2.authorize_security_group_ingress.assert_called_once_with(
        GroupId="sg-0123456789abcdef0",
        IpProtocol="tcp",
        FromPort=5432,
        ToPort=5432,
        CidrIp="10.20.0.0/16",
    )


def test_authorize_rds_ingress_blocks_world_open_cidr():
    mock_ec2 = MagicMock()
    with pytest.raises(ValueError):
        authorize_rds_ingress(mock_ec2, "sg-0123456789abcdef0", "0.0.0.0/0")
    mock_ec2.authorize_security_group_ingress.assert_not_called()

