# 🎯 Tablero Único de Ejecución — Ola 2 (Plan Híbrido: 2 Sprints, 9 Misiones)

> **Propósito:** Fuente única de estado y acción para cerrar la Ola 2 sin fricción ni saltos de contexto. Reconciliado 1:1 con [`roadmap-ola-2.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/meta/remediacion/roadmap-ola-2.md) tras superar **`M9` (Gate 2)**.  
> **Última Actualización:** 2026-11-10  
> **Hilo Conductor Unificado:** Pipeline Financiero **FinCorp Global** (Local ETL $\rightarrow$ Orquestación $\rightarrow$ Cloud AWS).  
> **Estado Global:** **🏆 OLA 2 CERRADA AL 100% (`Gate 2` Aprobado — Ola 3 `PORT-CAPSTONE` Desbloqueada)**

---

## 1. Mapa Maestro de las 9 Misiones hacia Gate 2 (`M1`–`M9`)

> **Bloques Cerrados al 100%:**  
> ✅ **Bloque 2.1 (7/7 Tipo B)** | ✅ **`02-py-poo` (5/5 Claims)** | ✅ **`03-sql-basico` (4/4 Claims)** | ✅ **SPRINT 1: `04-de-pipelines` (`32/32` + Grimoire Pass)** | ✅ **SPRINT 2: `05-cloud-aws` (`22/22` + Grimoire Pass)** | ✅ **`M9` Gate 2 (`92/92 tests passed`)**

| Sprint | Misión | Claims Fusionados | Materia / Cap | Entregable del Operador (Carril A) | Continuidad (Hilo FinCorp) | Estado |
|---|---|---|---|---|---|---|
| **SPRINT 1** | **`M1`** | `DE-004` + `DOCKER` | `04-de-pipelines`<br>Cap 04 | [`postgres_loader.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/data_engineering/chronicles/DE-PIPELINES/quests/04-carga-postgresql/postgres_loader.py) + [`Dockerfile`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/data_engineering/chronicles/DE-PIPELINES/quests/04-carga-postgresql/Dockerfile) | Carga la Zona Gold de FinCorp a PostgreSQL con pooling, chunks y Dockerfile | 🟢 **COMPLETADO (`6/6 passed`)** |
| **SPRINT 1** | **`M2`** | `DE-005` + `DE-009` | `04-de-pipelines`<br>Cap 05 | [`fincorp_orchestrator.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/data_engineering/chronicles/DE-PIPELINES/quests/05-orquestacion-prefect/fincorp_orchestrator.py) | Orquesta el extractor (`DE-007`) y el loader de `M1` con `get_run_logger` y Cron | 🟢 **COMPLETADO (`5/5 passed`)** |
| **SPRINT 1** | **`M3`** | Rite `DE` + `GIT-CI` | `04-de-pipelines`<br>Rite / Cap 03 | [`rite/src/quality.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/data_engineering/chronicles/DE-PIPELINES/rite/src/quality.py) + [`grimoire.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/data_engineering/chronicles/DE-PIPELINES/grimoire.md) | Desacopla `RateError(Exception)` de `AssertionError` y cierra `DE-PIPELINES` | 🟢 **COMPLETADO (`21/21 passed`)** |
|---|---|---|---|---|---|---|
| **SPRINT 2**<br>*(Listo en lote)* | **`M4`** | `AWS-004` + `AWS-010` | `05-cloud-aws`<br>Cap 00 (IAM) | [`quests/00-aws-iam/fincorp_iam.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/quests/00-aws-iam/fincorp_iam.py) | Crea programáticamente el rol IAM y políticas (`Allow` + `Explicit Deny`) para `M5–M7` | 🟢 **COMPLETADO (`4/4 passed`)** |
| **SPRINT 2**<br>*(Listo en lote)* | **`M5`** | `AWS-005` + `AWS-006` | `05-cloud-aws`<br>Cap 01 (S3) | [`quests/01-aws-s3/fincorp_s3_parquet.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/quests/01-aws-s3/fincorp_s3_parquet.py) | Crea bucket S3 validado por DNS y persiste la Zona Gold en **Parquet Snappy** | 🟢 **COMPLETADO (`8/8 passed`)** |
| **SPRINT 2**<br>*(Listo en lote)* | **`M6`** | `AWS-007` + `MKT-AWS-002` | `05-cloud-aws`<br>Cap 02 (RDS) | [`quests/02-aws-rds/fincorp_rds_secrets.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/quests/02-aws-rds/fincorp_rds_secrets.py) | Lee secretos de **Secrets Manager**, valida Security Group y reutiliza `get_uri()` de `M1` | 🟢 **COMPLETADO (`4/4 passed`)** |
| **SPRINT 2**<br>*(Listo en lote)* | **`M7`** | `AWS-008` | `05-cloud-aws`<br>Cap 03 (Lambda) | [`quests/03-aws-lambda/fincorp_lambda_deploy.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/quests/03-aws-lambda/fincorp_lambda_deploy.py) | Empaqueta en `.zip` en RAM y despliega con `create_function` el worker que usa `M4` y `M5` | 🟢 **COMPLETADO (`3/3 passed`)** |
| **SPRINT 2**<br>*(Listo en lote)* | **`M8`** | `AWS-009` | `05-cloud-aws`<br>Cap 04 (CW) | [`quests/04-aws-cloudwatch/fincorp_cloudwatch_alarm.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/quests/04-aws-cloudwatch/fincorp_cloudwatch_alarm.py) | Configura `Metric Filter` y `CloudWatch Alarm` sobre los fallos del worker de `M7` | 🟢 **COMPLETADO (`3/3 passed`)** |
| **CIERRE** | **`M9`** | Gate 2 | Transversal | [`CLOUD-AWS/grimoire.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/grimoire.md#L153) + Conciliación 1:1 $\rightarrow$ **Apertura Ola 3 (`PORT-CAPSTONE`)** | Cierre formal de Ola 2 | 🟢 **COMPLETADO (`92/92 passed`)** |

---

## 2. ☁️ SPRINT 2 EN LOTE: Recorrido Continuo de `05-cloud-aws` (`M4` $\rightarrow$ `M8`)

> 💡 **Paridad 1:1 Lore $\leftrightarrow$ Ejercicio Garantizada:**  
> En este Sprint cada capítulo tiene **exactamente la misma firma y argumentos** en su sección nueva del Lore (`§3.1/§3.2` o `§5.1/§5.2`) y en la plantilla del ejercicio. No hay parámetros ocultos ni sorpresas de sintaxis.

---

### 🔹 PASO 1 DE 5 — MISIÓN `M4` (`AWS-004` + `AWS-010`): IAM Programático y Políticas (`Explicit Deny`)

* **Archivo a editar:** [`content/subjects/cloud/chronicles/CLOUD-AWS/quests/00-aws-iam/fincorp_iam.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/quests/00-aws-iam/fincorp_iam.py)
* **Enunciado:** [`02-iam-provisioning.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/quests/00-aws-iam/02-iam-provisioning.md) | **Teoría:** [`lore/00-aws-iam.md` (§3.1 y §3.2)](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/lore/00-aws-iam.md#L53)

#### 📋 Contrato a implementar en `fincorp_iam.py`:
1. **`build_fincorp_least_privilege_policy(bucket_name: str) -> dict[str, Any]`**:
   * Retorna un diccionario con `"Version": "2012-10-17"` y `"Statement"` con 2 diccionarios:
     - `{"Effect": "Allow", "Action": ["s3:GetObject", "s3:PutObject"], "Resource": f"arn:aws:s3:::{bucket_name}/*"}`
     - `{"Effect": "Deny", "Action": ["s3:DeleteObject"], "Resource": f"arn:aws:s3:::{bucket_name}/*"}`
2. **`provision_fincorp_lambda_role(iam_client: Any, role_name: str, bucket_name: str) -> str`**:
   * Define `trust_policy` con `"Version": "2012-10-17"` y `"Statement": [{"Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]`.
   * Llama a `role_resp = iam_client.create_role(RoleName=role_name, AssumeRolePolicyDocument=json.dumps(trust_policy))`.
   * Obtiene `permissions_policy = build_fincorp_least_privilege_policy(bucket_name)`.
   * Llama a `iam_client.put_role_policy(RoleName=role_name, PolicyName=f"{role_name}-least-privilege", PolicyDocument=json.dumps(permissions_policy))`.
   * Retorna `role_resp["Role"]["Arn"]`.

#### 🧪 Comando de Verificación Binaria (`M4`):
```bash
/Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/.venv/bin/pytest content/subjects/cloud/chronicles/CLOUD-AWS/quests/00-aws-iam/test_fincorp_iam.py -v
```
*(Criterio: `4 passed` con exit code 0).*

---

### 🔹 PASO 2 DE 5 — MISIÓN `M5` (`AWS-005` + `AWS-006`): Bucket S3 con Validación DNS y Parquet Snappy

* **Archivo a editar:** [`content/subjects/cloud/chronicles/CLOUD-AWS/quests/01-aws-s3/fincorp_s3_parquet.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/quests/01-aws-s3/fincorp_s3_parquet.py)
* **Enunciado:** [`02-s3-parquet.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/quests/01-aws-s3/02-s3-parquet.md) | **Teoría:** [`lore/01-aws-s3.md` (§5.1, §5.2 y §5.3)](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/lore/01-aws-s3.md#L118)

#### 📋 Contrato a implementar en `fincorp_s3_parquet.py`:
1. **`provision_valid_bucket(s3_client: Any, bucket_name: str) -> str`**:
   * Si `not re.fullmatch(BUCKET_DNS_REGEX, bucket_name): raise ValueError(...)`.
   * Llama a `s3_client.create_bucket(Bucket=bucket_name)` y retorna `bucket_name`.
2. **`upload_gold_parquet(s3_client: Any, df: pd.DataFrame, bucket_name: str, s3_key: str) -> int`**:
   * Crea `buffer = io.BytesIO()`.
   * Ejecuta `df.to_parquet(buffer, engine="pyarrow", compression="snappy", index=False)`.
   * Obtiene `parquet_bytes = buffer.getvalue()`, llama a `s3_client.put_object(Bucket=bucket_name, Key=s3_key, Body=parquet_bytes)` y retorna `len(parquet_bytes)`.

#### 🧪 Comando de Verificación Binaria (`M5`):
```bash
/Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/.venv/bin/pytest content/subjects/cloud/chronicles/CLOUD-AWS/quests/01-aws-s3/test_fincorp_s3_parquet.py -v
```
*(Criterio: `8 passed` con exit code 0).*

---

### 🔹 PASO 3 DE 5 — MISIÓN `M6` (`AWS-007` + `MKT-AWS-002`): RDS + Secrets Manager + Security Group

* **Archivo a editar:** [`content/subjects/cloud/chronicles/CLOUD-AWS/quests/02-aws-rds/fincorp_rds_secrets.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/quests/02-aws-rds/fincorp_rds_secrets.py)
* **Enunciado:** [`02-rds-secrets.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/quests/02-aws-rds/02-rds-secrets.md) | **Teoría:** [`lore/02-aws-rds.md` (§5.1 y §5.2)](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/lore/02-aws-rds.md#L106)

#### 📋 Contrato a implementar en `fincorp_rds_secrets.py`:
1. **`RDSConfig.get_uri(self) -> str`**:
   * Reutiliza tu implementación de `M1`: retorna `f"{self.driver}://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"`.
2. **`load_rds_config_from_secrets(secrets_client: Any, secret_id: str) -> RDSConfig`**:
   * Llama a `response = secrets_client.get_secret_value(SecretId=secret_id)`.
   * Parsea `secret_payload = json.loads(response["SecretString"])`.
   * Retorna `RDSConfig(host=secret_payload["host"], port=int(secret_payload.get("port", 5432)), database=secret_payload["dbname"], username=secret_payload["username"], password=secret_payload["password"])`.
3. **`authorize_rds_ingress(ec2_client: Any, group_id: str, cidr_ip: str) -> dict[str, Any]`**:
   * Si `cidr_ip == "0.0.0.0/0": raise ValueError(...)`.
   * Retorna `ec2_client.authorize_security_group_ingress(GroupId=group_id, IpProtocol="tcp", FromPort=5432, ToPort=5432, CidrIp=cidr_ip)`.

#### 🧪 Comando de Verificación Binaria (`M6`):
```bash
/Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/.venv/bin/pytest content/subjects/cloud/chronicles/CLOUD-AWS/quests/02-aws-rds/test_fincorp_rds_secrets.py -v
```
*(Criterio: `4 passed` con exit code 0).*

---

### 🔹 PASO 4 DE 5 — MISIÓN `M7` (`AWS-008`): Empaquetado `.zip` y Despliegue de AWS Lambda

* **Archivo a editar:** [`content/subjects/cloud/chronicles/CLOUD-AWS/quests/03-aws-lambda/fincorp_lambda_deploy.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/quests/03-aws-lambda/fincorp_lambda_deploy.py)
* **Enunciado:** [`02-lambda-deploy.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/quests/03-aws-lambda/02-lambda-deploy.md) | **Teoría:** [`lore/03-aws-lambda.md` (§5.1)](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/lore/03-aws-lambda.md#L90)

#### 📋 Contrato a implementar en `fincorp_lambda_deploy.py`:
1. **`build_lambda_zip(source_code: str, filename: str = "handler.py") -> bytes`**:
   * Crea `buffer = io.BytesIO()`.
   * Con `with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:` ejecuta `zf.writestr(filename, source_code)`.
   * Retorna `buffer.getvalue()`.
2. **`deploy_serverless_worker(lambda_client: Any, function_name: str, role_arn: str, zip_bytes: bytes, env_vars: dict[str, str]) -> str`**:
   * Llama a `response = lambda_client.create_function(FunctionName=function_name, Runtime="python3.12", Role=role_arn, Handler="handler.lambda_handler", Code={"ZipFile": zip_bytes}, Environment={"Variables": env_vars}, Timeout=60, MemorySize=256)` y retorna `response["FunctionArn"]`.

#### 🧪 Comando de Verificación Binaria (`M7`):
```bash
/Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/.venv/bin/pytest content/subjects/cloud/chronicles/CLOUD-AWS/quests/03-aws-lambda/test_fincorp_lambda_deploy.py -v
```
*(Criterio: `3 passed` con exit code 0).*

---

### 🔹 PASO 5 DE 5 — MISIÓN `M8` (`AWS-009`): Metric Filters y Alarmas en CloudWatch

* **Archivo a editar:** [`content/subjects/cloud/chronicles/CLOUD-AWS/quests/04-aws-cloudwatch/fincorp_cloudwatch_alarm.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/quests/04-aws-cloudwatch/fincorp_cloudwatch_alarm.py)
* **Enunciado:** [`02-cloudwatch-alarms.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/quests/04-aws-cloudwatch/02-cloudwatch-alarms.md) | **Teoría:** [`lore/04-aws-cloudwatch.md` (§5.1)](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/lore/04-aws-cloudwatch.md#L81)

#### 📋 Contrato a implementar en `fincorp_cloudwatch_alarm.py`:
1. **`configure_failure_alarm(logs_client: Any, cw_client: Any, log_group_name: str, metric_name: str, metric_namespace: str = "FinCorp/ETL") -> str`**:
   * Llama a `logs_client.put_metric_filter(logGroupName=log_group_name, filterName=f"{metric_name}-Filter", filterPattern="ERROR", metricTransformations=[{"metricName": metric_name, "metricNamespace": metric_namespace, "metricValue": "1"}])`.
   * Define `alarm_name = f"{metric_name}-CriticalAlarm"`, llama a `cw_client.put_metric_alarm(AlarmName=alarm_name, MetricName=metric_name, Namespace=metric_namespace, Statistic="Sum", Period=60, EvaluationPeriods=1, Threshold=1.0, ComparisonOperator="GreaterThanOrEqualToThreshold")` y retorna `alarm_name`.

#### 🧪 Comando de Verificación Binaria (`M8`):
```bash
/Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/.venv/bin/pytest content/subjects/cloud/chronicles/CLOUD-AWS/quests/04-aws-cloudwatch/test_fincorp_cloudwatch_alarm.py -v
```
*(Criterio: `3 passed` con exit code 0).*

---

### 📓 Validación de Conocimiento de `05-cloud-aws` (Grimoire — Síntesis Feynman)
Al terminar `M4`–`M8`, responde las **2 preguntas de síntesis del Sprint 2** al final de [`CLOUD-AWS/grimoire.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/grimoire.md#L153).
