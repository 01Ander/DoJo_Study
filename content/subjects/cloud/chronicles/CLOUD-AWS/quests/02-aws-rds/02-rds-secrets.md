# Quest 02-02 (Misión M6): Gestión de Secretos en RDS y Reglas de Security Group (`AWS-007` + `MKT-AWS-002`)

**Objetivo:** Conectar la capa de base de datos de **FinCorp Global** en AWS recuperando las credenciales de RDS desde **AWS Secrets Manager** (cero hardcoding, `MKT-AWS-002`), reutilizando el diseño `get_uri()` de `M1` y asegurando las reglas de entrada del **Security Group** (`AWS-007`, Lore 02 §5.1 y §5.2).

---

## Archivo de Trabajo

Edita [`fincorp_rds_secrets.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/quests/02-aws-rds/fincorp_rds_secrets.py) e implementa los 3 componentes:

### 1. `RDSConfig.get_uri(self) -> str`
Idéntico al método que construiste en `M1` (`DE-004`):
* Retorna `f"{self.driver}://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"`.

---

### 2. `load_rds_config_from_secrets(secrets_client: Any, secret_id: str) -> RDSConfig`
* Invoca `response = secrets_client.get_secret_value(SecretId=secret_id)`.
* Parsea el JSON con `secret_payload = json.loads(response["SecretString"])`.
* Retorna una instancia de `RDSConfig`:
  ```python
  return RDSConfig(
      host=secret_payload["host"],
      port=int(secret_payload.get("port", 5432)),
      database=secret_payload["dbname"],
      username=secret_payload["username"],
      password=secret_payload["password"],
  )
  ```

---

### 3. `authorize_rds_ingress(ec2_client: Any, group_id: str, cidr_ip: str) -> dict[str, Any]`
* Si `cidr_ip == "0.0.0.0/0"`, lanza `raise ValueError(...)` para impedir que el puerto `5432` quede abierto al público.
* En caso contrario, invoca y retorna:
  ```python
  return ec2_client.authorize_security_group_ingress(
      GroupId=group_id,
      IpProtocol="tcp",
      FromPort=5432,
      ToPort=5432,
      CidrIp=cidr_ip,
  )
  ```

---

## 🧪 Comando de Verificación Binaria (`M6`)
```bash
/Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/.venv/bin/pytest content/subjects/cloud/chronicles/CLOUD-AWS/quests/02-aws-rds/test_fincorp_rds_secrets.py -v
```
*(Criterio de éxito: `4 passed` con exit code 0).*

