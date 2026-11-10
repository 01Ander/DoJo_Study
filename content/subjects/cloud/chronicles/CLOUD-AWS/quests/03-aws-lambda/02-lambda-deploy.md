# Quest 03-02 (Misión M7): Empaquetado `.zip` y Despliegue de AWS Lambda (`AWS-008`)

**Objetivo:** Empaquetar en memoria el código del worker de **FinCorp Global** en un archivo `.zip` (`io.BytesIO` + `zipfile.ZipFile`) y desplegarlo programáticamente con `lambda_client.create_function(...)` asociando el Rol IAM creado en `M4` y las variables de entorno nativas de AWS (Lore 03 §5.1).

---

## Archivo de Trabajo

Edita [`fincorp_lambda_deploy.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/quests/03-aws-lambda/fincorp_lambda_deploy.py) e implementa las dos funciones:

### 1. `build_lambda_zip(source_code: str, filename: str = "handler.py") -> bytes`
* Crea `buffer = io.BytesIO()`.
* Abre el archivo comprimido con `with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:` y escribe el código con `zf.writestr(filename, source_code)`.
* Retorna `buffer.getvalue()`.

---

### 2. `deploy_serverless_worker(lambda_client: Any, function_name: str, role_arn: str, zip_bytes: bytes, env_vars: dict[str, str]) -> str`
* Invoca `lambda_client.create_function(...)` con los argumentos:
  ```python
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
  ```
* Retorna `response["FunctionArn"]`.

---

## 🧪 Comando de Verificación Binaria (`M7`)
```bash
/Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/.venv/bin/pytest content/subjects/cloud/chronicles/CLOUD-AWS/quests/03-aws-lambda/test_fincorp_lambda_deploy.py -v
```
*(Criterio de éxito: `3 passed` con exit code 0).*

