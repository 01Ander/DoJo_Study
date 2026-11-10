"""
Quest 01-02 (Misión M5): Creación de Buckets S3 y Serialización Parquet Snappy (AWS-005 + AWS-006)
Dominio: FinCorp Global Cloud Data Lake
"""

import io
import re
from typing import Any
import pandas as pd

BUCKET_DNS_REGEX = r"^[a-z0-9][a-z0-9\-]{1,61}[a-z0-9]$"


def provision_valid_bucket(s3_client: Any, bucket_name: str) -> str:
    """
    Valida que `bucket_name` cumpla `re.fullmatch(BUCKET_DNS_REGEX, bucket_name)`.
    Si es inválido, lanza `ValueError`.
    Si es válido, llama a `s3_client.create_bucket(Bucket=bucket_name)` y retorna `bucket_name`.
    """
    # TODO: Implementar validación DNS y creación del bucket S3
    if not re.fullmatch(BUCKET_DNS_REGEX, bucket_name):
        raise ValueError(
            f"Nombre de bucket inválido según DNS de S3: '{bucket_name}'")

    s3_client.create_bucket(Bucket=bucket_name)
    return bucket_name


def upload_gold_parquet(
    s3_client: Any,
    df: pd.DataFrame,
    bucket_name: str,
    s3_key: str,
) -> int:
    """
    Serializa `df` a formato Parquet en un buffer `io.BytesIO()` usando
    `engine='pyarrow'`, `compression='snappy'` e `index=False`.
    Sube los bytes con `s3_client.put_object(Bucket=bucket_name, Key=s3_key, Body=...)`
    y retorna la cantidad total de bytes enviados (`len(parquet_bytes)`).
    """
    # TODO: Implementar serialización Parquet Snappy en memoria y subida a S3
    buffer = io.BytesIO()

    df.to_parquet(buffer, engine="pyarrow", compression="snappy", index=False)

    parquet_bytes = buffer.getvalue()
    s3_client.put_object(
        Bucket=bucket_name,
        Key=s3_key,
        Body=parquet_bytes,
    )
    return len(parquet_bytes)
