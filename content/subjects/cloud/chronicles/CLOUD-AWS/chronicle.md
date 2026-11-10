# Chronicle: AWS Cloud Pragmático para Data Engineering
## General Information
**Chronicle Name:** CLOUD-AWS
**Chronicle Code:** CLOUD-AWS
**Version:** 1.0
**Chronicle Type:** CORE-CLOUD

---

## 🎯 Business Context & ROI

**Business Context:**
> La mayoría de los pipelines de datos modernos no corren en computadoras locales, sino en la nube. Las empresas requieren ingenieros capaces de interactuar de manera programática, segura y tolerante a fallos con servicios en la nube (almacenamiento, bases de datos y cómputo serverless) sin necesitar infraestructura on-premise.

**ROI Estimado:**
> Capacita al Operador para desplegar y gestionar su propia infraestructura básica de datos, reduciendo bloqueos con equipos de DevOps, asegurando el principio de menor privilegio y sentando las bases para pipelines productivos, aumentando la empleabilidad en roles Mid-Level remotos.

---

## 🎭 Domain Shifting Rule

- **Dominio del Lore (Teoría):** Logística y Monitoreo de Dragones de Pantano (Swamp Dragons). *Gestión de su dieta, niveles de explosividad y hábitats en la nube.*
- **Dominio del Rite (Proyecto Final):** E-commerce Startup B2B (Logística de almacenes y procesamiento de inventarios).

---

## 🛠️ Technical Objective

**Technical Objective:**
> "Aprovisionar, configurar e integrar de forma segura y programática los servicios core de AWS (IAM, S3, RDS, Lambda, CloudWatch) para soportar arquitecturas de datos en la nube."

---

## 📚 Syllabus (Course Structure)

### Lore (Capítulos Teóricos)

- **[Cap 00: AWS Identity & Access Management (IAM)](lore/00-aws-iam.md)** — Usuarios de servicio, roles, políticas de mínimo privilegio (`Explicit Deny`, ARNs, `Condition`), creación programática (`create_role`, `put_role_policy`) y manejo de credenciales.
- **[Cap 01: Amazon S3 (Simple Storage Service)](lore/01-aws-s3.md)** — Creación programática de buckets con validación DNS (`create_bucket`), particionamiento por fecha (`year/month/day`), almacenamiento JSON y serialización columnar **Parquet (Snappy)**, más consultas analíticas serverless con **AWS Glue Data Catalog y Amazon Athena**.
- **[Cap 02: Amazon RDS (Relational Database Service)](lore/02-aws-rds.md)** — Instancias administradas de PostgreSQL, transacciones ACID, reglas de red en **Security Groups** (`authorize_security_group_ingress`), gestión de credenciales con **AWS Secrets Manager / KMS** (`get_secret_value`, cero hardcoding) y conexión segura desde Python.
- **[Cap 03: AWS Lambda (Serverless Compute)](lore/03-aws-lambda.md)** — Arquitectura orientada a eventos, configuración del handler, roles de ejecución IAM, variables de entorno nativas de AWS, empaquetado `.zip` en memoria y despliegue programático (`create_function`).
- **[Cap 04: Amazon CloudWatch & Observabilidad](lore/04-aws-cloudwatch.md)** — Configuración de Log Groups, políticas de retención, creación programática de **Metric Filters** (`put_metric_filter`) y **CloudWatch Alarms** (`put_metric_alarm`) ante fallos de ejecución.
- **[Cap 05: Integración Cloud End-to-End](lore/05-cloud-integration.md)** — Ensamblaje de un pipeline serverless: evento dispara Lambda, Lambda extrae datos hacia S3, los carga a RDS, y CloudWatch monitorea errores y logs.

---

### [Quests (Laboratorios Prácticos)](quests/)
Cada capítulo teórico (Lore) tiene una carpeta homóloga en `quests/` con ejercicios prácticos.
> *Nota: Debido a la naturaleza en la nube, estos quests requerirán el uso de librerías como `boto3`, `unittest.mock` o `moto` para testing, o ejecución contra un entorno AWS real usando perfiles locales.*

### [Grimoire](grimoire.md)
Documento de síntesis y retención de conocimientos donde el Operador responde preguntas clave usando la Técnica Feynman.

---

### [Rite (Proyecto Final — Rito de Paso)](rite/requirements.md)

**Descripción:**
> Construir el backend logístico cloud para una Startup E-commerce B2B. El proyecto debe ser un pipeline completamente desplegado en AWS que reciba datos de inventario diarios, los ingeste en formato raw particionado, los limpie y los cargue en una base de datos relacional administrada, alertando al equipo ante cualquier anomalía.

**Fases Desbloqueables:**
1. **Fase 1: Configuración de Seguridad e Identidad** (Mapea a Cap 00)
2. **Fase 2: Data Lake Layer (Raw y Curated)** (Mapea a Cap 01)
3. **Fase 3: Relational Warehouse Setup** (Mapea a Cap 02)
4. **Fase 4: Serverless Ingestion Worker** (Mapea a Cap 03)
5. **Fase 5: Observabilidad Activa** (Mapea a Cap 04 y 05)

---

## 🎓 Domain Criteria (Definition of Done)

- Can create IAM users/roles and apply least-privilege policies.
- Can programmatically read/write objects to S3 and enforce date-based partitioning.
- Can connect Python applications securely to an RDS PostgreSQL database.
- Can deploy and execute AWS Lambda functions using proper IAM execution roles.
- Can trace execution logs in CloudWatch and configure failure alarms.
- Can connect AWS services together securely without hardcoded credentials.

---

## 🚀 Derived Future Chronicles
- `PORT-CAPSTONE` (Pipeline Unificado End-to-End combinando DE-PIPELINES y CLOUD-AWS).
