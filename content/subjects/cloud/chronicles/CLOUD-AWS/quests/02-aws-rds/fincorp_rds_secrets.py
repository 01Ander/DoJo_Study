"""
Quest 02-02 (Misión M6): RDS + Security Groups + AWS Secrets Manager (AWS-007 + MKT-AWS-002)
Dominio: FinCorp Global Cloud Warehouse (Continuidad de DatabaseConfig de M1)
"""

from dataclasses import dataclass
import json
from typing import Any


@dataclass
class RDSConfig:
    host: str
    port: int
    database: str
    username: str
    password: str
    driver: str = "postgresql+psycopg2"

    def get_uri(self) -> str:
        """Retorna la URI de conexión con el mismo formato de M1: driver://username:password@host:port/database"""
        # TODO: Implementar construcción de URI (reutiliza tu lógica de DatabaseConfig de M1)
        return f"{self.driver}://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"


def load_rds_config_from_secrets(secrets_client: Any, secret_id: str) -> RDSConfig:
    """
    1. Consulta el secreto llamando a `secrets_client.get_secret_value(SecretId=secret_id)`.
    2. Parsea `response["SecretString"]` con `json.loads(...)`.
    3. Retorna una instancia de `RDSConfig` con `host`, `port` (int, default 5432),
       `database` (leído de `dbname`), `username` y `password`.
    """
    # TODO: Implementar carga de credenciales desde Secrets Manager

    response = secrets_client.get_secret_value(SecretId=secret_id)

    secret_payload = json.loads(response["SecretString"])

    return RDSConfig(
        host=secret_payload["host"],
        port=int(secret_payload.get("port", 5432)),
        database=secret_payload["dbname"],
        username=secret_payload["username"],
        password=secret_payload["password"],
    )


def authorize_rds_ingress(
    ec2_client: Any,
    group_id: str,
    cidr_ip: str,
) -> dict[str, Any]:
    """
    Si `cidr_ip == "0.0.0.0/0"`, lanza `ValueError`.
    Si es un CIDR privado válido, llama y retorna:
    `ec2_client.authorize_security_group_ingress(GroupId=group_id, IpProtocol="tcp", FromPort=5432, ToPort=5432, CidrIp=cidr_ip)`
    """
    # TODO: Implementar regla de Security Group hacia el puerto 5432
    if cidr_ip == "0.0.0.0/0":
        raise ValueError(
            "Violación de seguridad: Prohibido abrir el puerto 5432 de RDS a 0.0.0.0/0")

    return ec2_client.authorize_security_group_ingress(
        GroupId=group_id,
        IpProtocol="tcp",
        FromPort=5432,
        ToPort=5432,
        CidrIp=cidr_ip,
    )
