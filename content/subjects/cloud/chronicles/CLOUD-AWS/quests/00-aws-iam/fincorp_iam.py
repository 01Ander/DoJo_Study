"""
Quest 00-02 (Misión M4): IAM Programático y Políticas de Mínimo Privilegio (AWS-004 + AWS-010)
Dominio: FinCorp Global Cloud Pipeline
"""

import json
from typing import Any


def build_fincorp_least_privilege_policy(bucket_name: str) -> dict[str, Any]:
    """
    Construye y retorna el diccionario de política IAM con Version '2012-10-17' y dos Statements:
    1. Allow para ['s3:GetObject', 's3:PutObject'] sobre 'arn:aws:s3:::{bucket_name}/*'
    2. Deny explícito para ['s3:DeleteObject'] sobre 'arn:aws:s3:::{bucket_name}/*'
    """
    # TODO: Implementar diccionario de política IAM de mínimo privilegio
    permissions_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": ["s3:GetObject", "s3:PutObject"],
                "Resource": f"arn:aws:s3:::{bucket_name}/*",
            },
            {
                "Effect": "Deny",
                "Action": ["s3:DeleteObject"],
                "Resource": f"arn:aws:s3:::{bucket_name}/*",
            },
        ],
    }
    return permissions_policy


def provision_fincorp_lambda_role(
    iam_client: Any,
    role_name: str,
    bucket_name: str,
) -> str:
    """
    1. Define el trust_policy permitiendo a 'lambda.amazonaws.com' ejecutar 'sts:AssumeRole'.
    2. Llama a iam_client.create_role(RoleName=role_name, AssumeRolePolicyDocument=json.dumps(trust_policy)).
    3. Obtiene la política con build_fincorp_least_privilege_policy(bucket_name) y la adjunta con
       iam_client.put_role_policy(RoleName=role_name, PolicyName=f"{role_name}-least-privilege", PolicyDocument=json.dumps(...)).
    4. Retorna el ARN del rol: role_resp['Role']['Arn'].
    """
    # TODO: Implementar aprovisionamiento programático del rol IAM
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "lambda.amazonaws.com"},
                "Action": "sts:AssumeRole",
            }
        ],
    }
    role_resp = iam_client.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=json.dumps(trust_policy),
    )
    permissions_policy = build_fincorp_least_privilege_policy(bucket_name)
    iam_client.put_role_policy(
        RoleName=role_name,
        PolicyName=f"{role_name}-least-privilege",
        PolicyDocument=json.dumps(permissions_policy),
    )
    role_arn: str = role_resp["Role"]["Arn"]
    return role_arn
