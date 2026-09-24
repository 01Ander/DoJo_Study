# Matriz de Trazabilidad — `CLOUD-AWS`

> **Propósito:** Este archivo mapea cada término o concepto introducido en el lore de la chronicle contra las competencias del syllabus maestro. Asegura que no existan conceptos "mencionados de pasada" y que el Rite no exija cosas no enseñadas.
>
> **Instrucción para el modelo:** Actualiza este archivo incrementalmente al final de cada capítulo (PASO 4). Úsalo como input para auditar el lore (GATE 2), el grimoire (GATE 3) y el Rite (GATE 5).

## Área: `cloud`
## Chronicle: `CLOUD-AWS`

---

| Término / Concepto | Capítulo | Definido (Qué / Cómo / Por qué) | Competencia del Syllabus |
|---|---|---|---|
| AWS IAM | Cap 00 | ✅ / ✅ / ✅ | AWS IAM: Creación de usuarios, roles, políticas |
| IAM User (Servicio programático) | Cap 00 | ✅ / ✅ / ✅ | AWS IAM: Creación de usuarios de servicio |
| IAM Policy (Least Privilege, JSON) | Cap 00 | ✅ / ✅ / ✅ | AWS IAM: políticas de mínimo privilegio |
| IAM Role (Asunción temporal) | Cap 00 | ✅ / ✅ / ✅ | AWS IAM: roles |
| Variables de Entorno (.env, boto3) | Cap 00 | ✅ / ✅ / ✅ | AWS IAM: manejo de credenciales mediante variables de entorno |
| Amazon S3 (Buckets y Objects) | Cap 01 | ✅ / ✅ / ✅ | Amazon S3: Creación de buckets, almacenamiento |
| Date Partitioning (year/month/day) | Cap 01 | ✅ / ✅ / ✅ | Amazon S3: particionamiento de carpetas por fecha |
| JSON (Payload crudo) | Cap 01 | ✅ / ✅ / ✅ | Amazon S3: almacenamiento de payloads raw JSON |
| Parquet (Formato columnar) | Cap 01 | ✅ / ✅ / ✅ | Amazon S3: almacenamiento de formato columnar Parquet |
| Amazon RDS (Base administrada) | Cap 02 | ✅ / ✅ / ✅ | Amazon RDS: aprovisionamiento |
| Security Groups (Inbound rules) | Cap 02 | ✅ / ✅ / ✅ | Amazon RDS: configuración de Security Groups |
| DBAPI (psycopg2, cursores, execute) | Cap 02 | ✅ / ✅ / ✅ | Amazon RDS: conexión segura desde Python |
| AWS Lambda (Serverless Compute) | Cap 03 | ✅ / ✅ / ✅ | AWS Lambda: Funciones serverless |
| Event-Driven Architecture (Triggers vs Polling) | Cap 03 | ✅ / ✅ / ✅ | AWS Lambda: tareas ligeras de extracción y disparo de eventos |
| lambda_handler(event, context) | Cap 03 | ✅ / ✅ / ✅ | AWS Lambda: configuración de código |
| Execution Role | Cap 03 | ✅ / ✅ / ✅ | AWS Lambda: roles de ejecución |
| Amazon CloudWatch (Observabilidad) | Cap 04 | ✅ / ✅ / ✅ | Amazon CloudWatch: Monitoreo de logs |
| Log Groups y Log Streams | Cap 04 | ✅ / ✅ / ✅ | Amazon CloudWatch: Monitoreo de logs |
| Log Retention Policies | Cap 04 | ✅ / ✅ / ✅ | Amazon CloudWatch: Control de retención y costos |
| Módulo logging (logger.info, logger.error) | Cap 04 | ✅ / ✅ / ✅ | Amazon CloudWatch: Monitoreo de logs estructurados |
| Metric Filters y Alarmas | Cap 04 | ✅ / ✅ / ✅ | Amazon CloudWatch: configuración de alertas de fallo |
| Integración E2E (End-to-End) | Cap 05 | ✅ / ✅ / ✅ | AWS Cloud: Integración E2E |
| Variables de entorno nativas | Cap 05 | ✅ / ✅ / ✅ | AWS Lambda: sin .env local |
| Transacciones ACID (commit, rollback) | Cap 05 | ✅ / ✅ / ✅ | Amazon RDS: transacciones seguras |
| Manejo de recursos (finally, conn.close) | Cap 05 | ✅ / ✅ / ✅ | AWS Lambda: limpieza de conexiones RDS |

---

## Reglas de Auditoría (Gates)

*   **GATE 2 (Lore):** Si un concepto no tiene los 3 checkmarks (✅), el capítulo es un FAIL y debe ser corregido antes de avanzar.
*   **GATE 3 (Grimoire):** Toda pregunta del Grimoire debe basarse en un concepto que exista en esta tabla.
*   **GATE 5 (Rite):** El Rite no puede exigir el uso de ninguna herramienta o concepto que no esté listado en esta tabla.
