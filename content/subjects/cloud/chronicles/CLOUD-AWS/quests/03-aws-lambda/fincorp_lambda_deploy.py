"""
Quest 03-02 (Misión M7): Empaquetado .zip y Despliegue de AWS Lambda (AWS-008)
Dominio: FinCorp Global Serverless Worker (Usa el Role ARN de M4 y apunta al Bucket de M5)
"""

import io
from typing import Any
import zipfile


def build_lambda_zip(source_code: str, filename: str = "handler.py") -> bytes:
    """
    Empaqueta `source_code` dentro de un archivo .zip en memoria (`io.BytesIO`)
    bajo el nombre `filename` (usando `zipfile.ZIP_DEFLATED`) y retorna los bytes del .zip.
    """
    # TODO: Implementar creación del paquete .zip en memoria
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(filename, source_code)
    return buffer.getvalue()


def deploy_serverless_worker(
    lambda_client: Any,
    function_name: str,
    role_arn: str,
    zip_bytes: bytes,
    env_vars: dict[str, str],
) -> str:
    """
    Despliega la función llamando a `lambda_client.create_function(...)` con:
    - FunctionName=function_name
    - Runtime="python3.12"
    - Role=role_arn
    - Handler="handler.lambda_handler"
    - Code={"ZipFile": zip_bytes}
    - Environment={"Variables": env_vars}
    - Timeout=60
    - MemorySize=256
    Retorna `response["FunctionArn"]`.
    """
    # TODO: Implementar despliegue con create_function
    response = lambda_client.create_function(
        FunctionName=function_name,
        Runtime="python3.12",
        Role=role_arn,
        Handler="handler.lambda_handler",
        Code={"ZipFile": zip_bytes},
        Environment={"Variables": env_vars},
        Timeout=60,
        MemorySize=256,
    )
    return response["FunctionArn"]
