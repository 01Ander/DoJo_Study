# Bitácora Táctica de Remediación — `05-cloud-aws`

> **Documento Rector:** [README.md](../README.md) — índice de la remediación (Ola 1)  
> **Directorio Canónico:** [`content/subjects/cloud/chronicles/CLOUD-AWS/`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/)  
> **Python / Venv:** `content/subjects/cloud/chronicles/CLOUD-AWS/.venv/bin/python`  
> **Estado:** En Preparación (Ola 1)

---

## 1. Carril B: Higiene del Material (Ejecución de Arquitecto / Asistente)

> [!CRITICAL]
> **Dependencia Obligatoria de Orden:**  
> El re-apuntado del evaluador en las 6 quests debe ejecutarse en el Carril B **antes** de que el Operador valide `AWS-011`, para garantizar que los tests unitarios midan `my_solution.py` y no `solution.py`.

### Re-apuntado de los Evaluadores (6 Quests)
- **Diagnóstico:** Los archivos `reference_test.py` estaban acoplados a la solución del generador (`solution.py`) mediante 8 imports directos (`from solution import ...`) y 7 targets de patch (`@patch('solution...')`), impidiendo evaluar el código real del estudiante en `my_solution.py`.
- **Sonda Inicial:**
  ```bash
  grep -rn "solution" content/subjects/cloud/chronicles/CLOUD-AWS/quests/*/reference/reference_test.py | grep -v "my_solution"
  ```
  *Resultado:* Reporta 15 ocurrencias activas acopladas a `solution`.
- **Acción:** Re-apuntar todos los imports y targets de patch a `my_solution`.
- **Sonda Final:**
  ```bash
  grep -rn "solution" content/subjects/cloud/chronicles/CLOUD-AWS/quests/*/reference/reference_test.py | grep -v "my_solution"
  ```
  *Criterio:* Devuelve 0 líneas (`exit code 1` en grep).

### AWS-012: Reconciliación Inversa en `chronicle.md`
- **Diagnóstico:** El temario no declaraba explícitamente `unittest.mock` para testing serverless ni transacciones ACID en PostgreSQL, a pesar de ser temas centrales en las quests.
- **Sonda Inicial:**
  ```bash
  grep -cE "unittest.mock|transacciones" content/subjects/cloud/chronicles/CLOUD-AWS/chronicle.md
  ```
  *Resultado:* `0` (exit 1).
- **Acción:** Declarar formalmente ambas tecnologías en el temario de `chronicle.md`.
- **Sonda Final:**
  ```bash
  grep -E "unittest.mock|transacciones" content/subjects/cloud/chronicles/CLOUD-AWS/chronicle.md
  ```
  *Criterio:* Declaradas explícitamente en los capítulos correspondientes.

---

## 2. Carril A: Aprendizaje Crítico (Tiempo de Estudio del Operador)

### AWS-001: Cierre Determinista de Conexiones en Bloques Finally
- **Archivo:** `quests/02-aws-rds/my_solution.py:L47`
- **Concepto:** Si una función inicializa `conn = None` antes del bloque `try`, y la conexión a la base de datos falla (por timeout o credenciales inválidas), evaluar `if 'conn' in locals(): conn.close()` detona `AttributeError: 'NoneType' object has no attribute 'close'`, porque la variable `'conn'` sí existe en el scope local con valor `None`. La comprobación debe evaluar el contenido: `if conn is not None: conn.close()`.
- **Domain Shifting (Espejo de Comunicación del Archi-Canciller):**
  ```python
  mirror = None
  try:
      mirror = connect_thaumic_mirror("Torre del Arte")
      transmit_message(mirror, "Alerta")
  finally:
      # Si el espejo nunca conectó, no intentes romper el enlace:
      if mirror is not None:
          mirror.disconnect()
  ```
- **Sonda Inicial:**
  ```bash
  content/subjects/cloud/chronicles/CLOUD-AWS/.venv/bin/python -c "import sys; sys.path.insert(0, 'content/subjects/cloud/chronicles/CLOUD-AWS/quests/02-aws-rds'); from unittest.mock import patch; from my_solution import check_status; patch('my_solution.psycopg2.connect', side_effect=Exception('Conn refused')).start(); check_status(42)"
  ```
  *Resultado:* `AttributeError: 'NoneType' object has no attribute 'close'` (exit 1).
- **Sonda Final (Contrato tras solución del Operador):**
  Mismo comando tras corregir a `if conn is not None: conn.close()` $\rightarrow$ Retorna `None` de forma segura con `exit code 0`.

### AWS-002: Convenciones DNS de Buckets S3 y Validación Client-Side
- **Archivo:** `quests/01-aws-s3/my_solution.py:L35`
- **Concepto:** Los nombres de bucket en AWS S3 deben seguir estrictamente el estándar de nombres de host DNS (solo minúsculas, números y guiones, sin espacios ni mayúsculas). `botocore` valida esta regla en el cliente local antes de enviar la solicitud por red.
- **Sonda Inicial (Fallo con nombre inválido):**
  ```bash
  content/subjects/cloud/chronicles/CLOUD-AWS/.venv/bin/python -c "import boto3; s3 = boto3.client('s3', region_name='us-east-1', aws_access_key_id='dummy', aws_secret_access_key='dummy'); s3.put_object(Bucket='Feed dragons', Key='test.json', Body=b'{}')"
  ```
  *Resultado:* `botocore.exceptions.ParamValidationError: Parameter validation failed: Invalid bucket name "Feed dragons"` (exit 1).
- **Sonda Final (Contrato tras solución del Operador):**
  ```bash
  content/subjects/cloud/chronicles/CLOUD-AWS/.venv/bin/python -c "import boto3, botocore.exceptions; s3 = boto3.client('s3', region_name='us-east-1', aws_access_key_id='dummy', aws_secret_access_key='dummy');
  try:
      s3.put_object(Bucket='dragon-food-swamp-prod', Key='test.json', Body=b'{}')
  except botocore.exceptions.ParamValidationError:
      print('FAIL: ParamValidationError')
      exit(1)
  except Exception:
      print('PASS: Client validation passed without ParamValidationError')
      exit(0)"
  ```
  *Criterio:* `exit code 0`.

### AWS-003: Mito 4/5 — Contratos Serverless Asíncronos (S3 $\rightarrow$ Lambda en Lore 03)
- **Archivo:** [`lore/03-aws-lambda.md:L12-L20, L82`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/lore/03-aws-lambda.md#L12-L20)
- **Concepto:** Cuando una Lambda se invoca de forma asíncrona (por ejemplo, disparada por un evento de S3 `s3:ObjectCreated:*`), AWS descarta el valor de retorno de la función. Devolver un diccionario `{'statusCode': 500, 'body': ...}` silencia el error ante AWS, haciendo creer a la plataforma que la invocación fue exitosa (`Invocations: 1, Errors: 0`), desactivando las alertas de CloudWatch y las Dead Letter Queues (DLQ).
- **Acción (Antigravity):** Inclusión de advertencia arquitectónica formal en la prosa de Lore 03 distinguiendo entre invocaciones síncronas (API Gateway / pruebas locales) e invocaciones asíncronas de datos (donde los fallos deben propagarse con `raise`).
- **Sonda de Comprobación:** La aclaración arquitectónica resuelve la contradicción entre el contrato de testing local de las quests y el requisito de producción del Rite.

---

## 2. Carril A: Aprendizaje Crítico (Tiempo de Estudio del Operador)

### AWS-001: Cierre Determinista de Conexiones en Bloques Finally
- **Archivo:** [`quests/02-aws-rds/my_solution.py:L47`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/quests/02-aws-rds/my_solution.py#L40-L50)
- **Concepto:** Si una función inicializa `conn = None` antes del bloque `try`, y la conexión a la base de datos falla (por timeout o credenciales inválidas), evaluar `if 'conn' in locals(): conn.close()` detona `AttributeError: 'NoneType' object has no attribute 'close'`, porque la variable `'conn'` sí existe en el scope local con valor `None`. La comprobación debe evaluar el contenido: `if conn is not None: conn.close()`.
- **Domain Shifting (Espejo de Comunicación del Archi-Canciller):**
  ```python
  mirror = None
  try:
      mirror = connect_thaumic_mirror("Torre del Arte")
      transmit_message(mirror, "Alerta")
  finally:
      # Si el espejo nunca conectó, no intentes romper el enlace:
      if mirror is not None:
          mirror.disconnect()
  ```
- **Sonda Inicial:**
  ```bash
  content/subjects/cloud/chronicles/CLOUD-AWS/.venv/bin/python -c "import sys; sys.path.insert(0, 'content/subjects/cloud/chronicles/CLOUD-AWS/quests/02-aws-rds'); from unittest.mock import patch; from my_solution import check_status; patch('my_solution.psycopg2.connect', side_effect=Exception('Conn refused')).start(); check_status(42)"
  ```
  *Resultado:* `AttributeError: 'NoneType' object has no attribute 'close'` (exit 1).
- **Sonda Final (Contrato tras solución del Operador):**
  Mismo comando tras corregir a `if conn is not None: conn.close()` $\rightarrow$ Retorna `None` de forma segura con `exit code 0`.

---

### AWS-002: Convenciones DNS de Buckets S3 y Validación Client-Side
- **Archivo:** [`quests/01-aws-s3/my_solution.py:L35`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/quests/01-aws-s3/my_solution.py#L30-L40)
- **Concepto:** Los nombres de bucket en AWS S3 deben seguir estrictamente el estándar de nombres de host DNS (solo minúsculas, números y guiones, sin espacios ni mayúsculas). `botocore` valida esta regla en el cliente local antes de enviar la solicitud por red.
- **Sonda Inicial (Fallo con nombre inválido):**
  ```bash
  content/subjects/cloud/chronicles/CLOUD-AWS/.venv/bin/python -c "import boto3; s3 = boto3.client('s3', region_name='us-east-1', aws_access_key_id='dummy', aws_secret_access_key='dummy'); s3.put_object(Bucket='Feed dragons', Key='test.json', Body=b'{}')"
  ```
  *Resultado:* `botocore.exceptions.ParamValidationError: Parameter validation failed: Invalid bucket name "Feed dragons"` (exit 1).
- **Sonda Final (Contrato tras solución del Operador):**
  ```bash
  content/subjects/cloud/chronicles/CLOUD-AWS/.venv/bin/python -c "import boto3, botocore.exceptions; s3 = boto3.client('s3', region_name='us-east-1', aws_access_key_id='dummy', aws_secret_access_key='dummy');
  try:
      s3.put_object(Bucket='dragon-food-swamp-prod', Key='test.json', Body=b'{}')
  except botocore.exceptions.ParamValidationError:
      print('FAIL: ParamValidationError')
      exit(1)
  except Exception:
      print('PASS: Client validation passed without ParamValidationError')
      exit(0)"
  ```
  *Criterio:* `exit code 0`.

---

### AWS-011: Coincidencia Literal en Metric Filters de CloudWatch
- **Archivo:** [`quests/04-aws-cloudwatch/my_solution.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/quests/04-aws-cloudwatch/my_solution.py) y [`quests/05-cloud-integration/my_solution.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/cloud/chronicles/CLOUD-AWS/quests/05-cloud-integration/my_solution.py)
- **Concepto:** CloudWatch Logs Metric Filters busca patrones de texto exactos y sensibles a mayúsculas/minúsculas y puntuación. Un carácter discordante (como `"Normal status. Finishing"` vs `"Normal status. Finishing."` o `'ETl'` vs `'ETL'`) hace que el filtro no detecte los eventos y desactive las alarmas de monitoreo en producción.
- **Sonda Final (Contrato tras solución del Operador):**
  ```bash
  cd content/subjects/cloud/chronicles/CLOUD-AWS/quests/04-aws-cloudwatch && ../../.venv/bin/pytest reference/reference_test.py
  ```
  *Criterio:* Tests pasan al 100% midiendo `my_solution.py` con `exit code 0`.

---

## 3. Log de Mutaciones y Verificación

| ID | Fecha | Carril | Responsable | Sonda Inicial (Salida) | Sonda Final (Salida) | Estado |
|---|---|---|---|---|---|---|
| Evaluadores | 2026-10-13 | B | Antigravity | 15 ocurrencias acopladas a solution | 15 re-apuntadas a my_solution (0 acoplados, exit 1) | ✅ Completado |
| AWS-012 | 2026-10-13 | B | Antigravity | `unittest.mock` y transacciones no declarados | Declaradas en temario de chronicle.md (exit 0) | ✅ Completado |
| AWS-003 | 2026-10-13 | B | Antigravity | Mito en Lore 03 (statusCode en S3 asíncrono) | Advertencia de invocación asíncrona en Lore 03 (exit 0) | ✅ Completado |
| AWS-001 | 2026-10-13 | A | Operador | `AttributeError` en finally | `if conn is not None: conn.close()` activo (exit 0) | ✅ Completado |
| AWS-002 | 2026-10-13 | A | Operador | `ParamValidationError` en bucket | Bucket `dragon-food-swamp-prod` (exit 0) | ✅ Completado |
| AWS-011 | 2026-10-13 | A | Operador | Erratas en cadenas de logs | Punto final alineado, tests 2/2 OK (exit 0) | ✅ Completado |
