# Quest 00-02 (Misión M4): Aprovisionamiento Programático de IAM y Políticas de Mínimo Privilegio (`AWS-004` + `AWS-010`)

**Objetivo:** Aprovisionar programáticamente con `boto3` el Rol de Ejecución IAM (`create_role` + `put_role_policy`) para el pipeline cloud de **FinCorp Global**, aplicando una política de mínimo privilegio con `Explicit Deny` contra el borrado de objetos en el Data Lake S3 (Lore 00 §3.1 y §3.2).

---

## Archivo de Trabajo

Edita [`fincorp_iam.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/quests/00-aws-iam/fincorp_iam.py) e implementa las dos funciones:

### 1. `build_fincorp_least_privilege_policy(bucket_name: str) -> dict[str, Any]`
Construye y retorna el diccionario de la Permissions Policy con `"Version": "2012-10-17"` y `"Statement"` conteniendo **2 bloques**:
1. **Allow de lectura/escritura:** `"Effect": "Allow"`, `"Action": ["s3:GetObject", "s3:PutObject"]`, `"Resource": f"arn:aws:s3:::{bucket_name}/*"`.
2. **Explicit Deny contra borrado:** `"Effect": "Deny"`, `"Action": ["s3:DeleteObject"]`, `"Resource": f"arn:aws:s3:::{bucket_name}/*"`.

---

### 2. `provision_fincorp_lambda_role(iam_client: Any, role_name: str, bucket_name: str) -> str`
1. Crea el diccionario `trust_policy` autorizando al servicio `"lambda.amazonaws.com"` a ejecutar `"sts:AssumeRole"` (`"Effect": "Allow"`).
2. Invoca `role_resp = iam_client.create_role(RoleName=role_name, AssumeRolePolicyDocument=json.dumps(trust_policy))`.
3. Genera la política de permisos llamando a `permissions_policy = build_fincorp_least_privilege_policy(bucket_name)`.
4. Adjunta la política invocando:
   ```python
   iam_client.put_role_policy(
       RoleName=role_name,
       PolicyName=f"{role_name}-least-privilege",
       PolicyDocument=json.dumps(permissions_policy),
   )
   ```
5. Retorna el ARN del rol creado (`role_resp["Role"]["Arn"]`).

---

## 🧪 Comando de Verificación Binaria (`M4`)
```bash
/Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/.venv/bin/pytest content/subjects/cloud/chronicles/CLOUD-AWS/quests/00-aws-iam/test_fincorp_iam.py -v
```
*(Criterio de éxito: `4 passed` con exit code 0).*

