# Torre de Control y Roadmap de Remediación — Ola 2 (Syllabus 3.0 & Contenidos Faltantes)

> **Documento Rector:** [`meta/audits/2026-q3-contenido/analisis/dictamen-final-consolidado.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/meta/audits/2026-q3-contenido/analisis/dictamen-final-consolidado.md)  
> **Ubicación Canónica de Gobernanza:** `meta/remediacion/`  
> **Estado General:** ✅ **OLA 2 CERRADA AL 100% (`Gate 2` Aprobado — Ola 3 `PORT-CAPSTONE` Desbloqueada)**  
> **Fecha de Inicio:** 2026-10-13 | **Fecha de Cierre (`Gate 2`):** 2026-11-10  
> **Prerrequisito Aprobado:** Gate 1 (Ola 1 cerrada al 100% en commit `57073c4`) | **Tablero Operativo:** [`tablero-operador.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/meta/remediacion/tablero-operador.md)

---

## 1. Misión y Alcance de la Ola 2

Habiendo saneado la totalidad de la base de código y eliminado los bloqueos mecánicos en la Ola 1 (31 entregables), la **Ola 2** tiene como objetivo **cerrar la brecha de contenido faltante (28 claims de auditoría) e incorporar los requerimientos obligatorios fijados por el mercado laboral internacional 2026 (los 8 CLAIM-MKT)**.

```mermaid
graph TD
    subgraph Previo [Gate 1 Superado]
        G1["Ola 1: Saneamiento Base (31 Entregables)<br/>✅ Commit 57073c4"]
    end

    subgraph Ola 2 [Ola 2: Reingeniería Curricular y Contenidos Faltantes]
        S3["2.0 Syllabus 3.0 (Ventana Arquitecto)<br/>Forma, Decisiones de Tooling, Podas, Frontera Fase 2"]
        B1["2.1 ROI Inmediato (7 Claims Tipo B)<br/>Exigido por Tests sin Enseñar en Lore"]
        B2["2.2 Núcleo Curricular (14 Tipo A Activos + 2 Podados)<br/>Postgres, IAM boto3, Parquet, Loaders, SCD2, Secrets"]
        B3["2.3 Profundización (5 Claims Tipo E)<br/>Agregaciones, NULLs tri-valor, Paginación, IAM, TDD"]
        B4["2.4 Tooling Transversal & Integración MKT<br/>Docker Compose, GitHub Actions, Columnar, Airflow, dbt"]
    end

    subgraph Futuro [Gate 2 Hacia Ola 3]
        G2["Gate 2: Criterios Binarios de Aceptación<br/>Bucle cerrado, cero regresión, Regla 5"]
        O3["Ola 3: Portafolio Unificado (PORT-CAPSTONE)"]
    end

    G1 --> S3
    S3 --> B1
    S3 --> B2
    S3 --> B3
    S3 --> B4
    B1 --> G2
    B2 --> G2
    B3 --> G2
    B4 --> G2
    G2 --> O3
```

---

## 2. Los 4 Pilares del Prerequisito: `Syllabus 3.0` (Ventana de Arquitecto)

Tal como lo dictamina la sección 4.2 del Dictamen Rector, antes de escribir una sola línea de contenido nuevo se resuelven las decisiones estructurales:

### 2.1 Decisión de Forma: Integración Natural vs Asignatura Aislada
* **Dictamen:** No fragmentar el aprendizaje en cursos hiper-específicos que aumenten la dispersión del Operador. El mercado pide que la cadena de datos funcione, no un catálogo de cursos introductorios.
* **Resolución:** **Integración en la Cadena Existente**:
  * **PostgreSQL real:** Se incorpora como motor de carga destino en `DE-PIPELINES` y motor relacional en `CLOUD-AWS` (RDS), desplazando el monocultivo de SQLite hacia pruebas unitarias en memoria.
  * **Warehouse Columnar (Snowflake / BigQuery / Redshift):** Se integra en el tramo analítico avanzado de `DE-PIPELINES` como destino de datos curados previo al Capstone.
  * **dbt:** Se integra en `DE-PIPELINES` para la capa de transformación declarativa y modelado SQL modular.
  * **AWS Glue + Athena:** Se incorporan en la sección analítica de `CLOUD-AWS`.
  * **Airflow básico:** Se enseña en `DE-PIPELINES` como estándar de referencia ATS (DAGs, dependencias `>>`, scheduler, reintentos).
  * **Docker pragmático:** Se adopta como tooling transversal para levantar Postgres y servicios locales sin fricción de instalación en el host.

### 2.2 Derogación de Contradicciones Históricas
* **Contenerización (Docker):** El `Protocol Yellow` trataba a Docker como complejidad opcional. El análisis de mercado laboral 2026 demuestra que Docker (`Dockerfile` y `docker-compose.yml`) es una expectativa pre-empleo básica. Se formaliza como herramienta transversal estándar del DoJo.
* **Spark:** El mercado le asigna un 33% sin declararlo obligatorio pre-empleo. Se define como lectura conceptual de arquitectura en `DE-PIPELINES` y se delega la práctica pesada a la Fase 2 (Post-empleo).

### 2.3 Formalización de Podas Curriculares (Las 3 Excepciones)
1. **Typer/Click (`PY-012`, Tipo A):** Queda formalmente podado a favor de `argparse` (ya enseñado y reconciliado en el Chronicle).
2. **Clean Architecture (`PY-015`, Tipo A):** Se redefine en el temario como "Diseño Modular por Capas y Separación de Responsabilidades", descartando dogmas teóricos que no aportan al rol de Data Automation.
3. **`load_dotenv` en Lambda:** Se erradica de las guías de Lambda; se enseña el estándar de producción: variables de entorno inyectadas por AWS Cloud y roles de ejecución IAM.

### 2.4 Delimitación de Frontera con Fase 2 (Post-Empleo RFC v5.2.0)
Para evitar la proliferación descontrolada de temas que retrasen la inserción laboral del Operador, se blinda el alcance pre-empleo conforme al RFC v5.2.0:
* **Dentro de Ruta Pre-Empleo (Ola 2 y Capstone):** Python OOP/TDD, SQL/PostgreSQL, Pandas, Docker local, Airflow/Prefect, S3/Parquet, IAM básico, RDS, Lambda, CloudWatch, dbt básico, Cloud Warehouse básico, Secrets Manager y CI con GitHub Actions.
* **Fase 2 (Post-Empleo — Retenido según validación propia):** QA formal exhaustivo, DevOps avanzado (Kubernetes, Terraform, CI/CD multi-ambiente), Dashboards complejos / BI, Seguridad y gobernanza corporativa avanzada, y LLM/RAG/GenAI (~9% de ofertas iniciales).

---


## 3. Matriz Maestra de Claims a Cerrar en Ola 2 (28 Claims de Auditoría + Integración MKT)

> **Trazabilidad Aritmética de los 28 Claims de Contenido Faltante:**  
> **7 Tipo B** (Bloque 3.1) + **14 Tipo A activos** (Bloque 3.2) + **2 Tipo A podados** (`PY-012` y `PY-015` en §2.3) + **5 Tipo E** (Bloque 3.3) = **28 Claims de Auditoría** (100% de cobertura).

### 3.1 Bloque 2.1 — ROI Inmediato (Los 7 Tipo B: Exigidos sin Enseñar)
*Son conceptos que el Rite o los tests ya evalúan pero que el Lore nunca explicó. Tienen el ratio esfuerzo/beneficio más alto.*

| Claim ID | Subject | Componente | Concepto Faltante | Estrategia Pedagógica | Carril | Estado |
|---|---|---|---|---|---|---|
| **`PY-016`** | `02-py-poo` | Lore 03 / Rite | `collections.defaultdict` | Añadida sección en Lore 03 §4 con Domain Shifting y agregaciones | B (Lore) / A (Quest) | ✅ Completado |
| **`PY-017`** | `02-py-poo` | Lore 05 / Tests Rite | Fixture `tmp_path` de `pytest` | Añadida sección en Lore 05 §4 y quest 05-03 de I/O efímero | B (Lore) / A (Quest) | ✅ Completado |
| **`PY-018`** | `02-py-poo` | Lore 05 / Tests Rite | `pytest.approx` | Añadida sección en Lore 05 §5 y quest 05-03 de tolerancia float | B (Lore) / A (Quest) | ✅ Completado |
| **`PY-019`** | `02-py-poo` | Lore 03 / Quest 03 | `@pytest.fixture` | Formalizada introducción en Lore 03 §5 y alineada quest 03-02 | B (Lore) / A (Quest) | ✅ Completado |
| **`SQL-012`**| `03-sql-basico` | Lore 04 / Rite | Cardinalidad N:M y "Autor Principal" | Añadida sección en Lore 04 §7 sobre reducción determinista con CTEs | B (Lore) / A (Quest) | ✅ Completado |
| **`DE-006`** | `04-de-pipelines` | Lore 02 / Rite | `df.groupby` en Pandas | Añadida sección en Lore 02 §5 sobre agregación de Zona Gold | B (Lore) / A (Quest) | ✅ Completado |
| **`DE-010`** | `04-de-pipelines` | Lore 01 / DoD Rite | `mypy` en Data Pipelines | Añadida sección en Lore 01 §5 sobre chequeo estático de tipos | B (Lore) / A (Quest) | ✅ Completado |

---

### 3.2 Bloque 2.2 — Núcleo Curricular y Profundización Ordenados por Secuencia Pedagógica

> ⚠️ **Regla de Secuencialidad Pedagógica Obligatoria (Directriz de Operación):**  
> A partir de las siguientes materias (`03-SQL-BASICO`, `04-DE-PIPELINES`, `05-CLOUD-AWS`), la ejecución de remediaciones y quests del Operador DEBE seguir estrictamente el orden canónico y cronológico de los capítulos del temario (Cap 00 $\rightarrow$ Cap 01 $\rightarrow$ Cap 02 $\rightarrow$ ...). Queda prohibido agrupar por número de ID de auditoría si esto implica saltar adelante y atrás entre capítulos, garantizando que los conceptos de soporte siempre precedan a sus consumidores.
>
> *Nota de Trazabilidad:* Los 2 Tipo A podados (`PY-012` Typer/Click y `PY-015` Clean Architecture) quedan formalmente ratificados como podas curriculares en §2.3.

#### Secuencia de Ejecución de Brechas por Materia y Capítulo:

| Claim ID | Subject | Ubicación Canónica | Brecha / Tema | Entregable Ola 2 | Carril | Estado |
|---|---|---|---|---|---|---|
| **`PY-010`** | `02-py-poo` | Cap 02: Entidades | Constructores con `super()` | Lore 02 §4 + Quest 02-03 jerarquías compuestas | B/A | 🟢 Completado |
| **`PY-011`** | `02-py-poo` | Cap 06: Error Handling | Validación con Pydantic V2 | Lore 06B + Quests 06-03 y 06-04 con contratos | B/A | 🟢 Completado |
| **`PY-013`** | `02-py-poo` | Cap 04: Orquestación | Patrón Output Loaders | Lore 04 §4-6 + Quest 04-03 `BaseOutputLoader` | B/A | 🟢 Completado |
| **`PY-014`** | `02-py-poo` | Cap 01: Abstracciones | Extractor desacoplado CSV/JSON | Lore 01 §5 + Quest 01-03 `AbstractDataExtractor` | B/A | 🟢 Completado |
| **`PY-020`** | `02-py-poo` | Cap 05: Testing | Modelado de ciclo TDD | Lore 05 §6 + Quest 05-04 Red-Green-Refactor | B/A | 🟢 Completado |
|---|---|---|---|---|---|---|
| **`SQL-013`** | `03-sql-basico`| Cap 02: Filtros | Semántica tri-valor de `NULL` | Lore 02 §4 + Quest 02-03 `null_semantics.sql` | B/A | 🟢 Completado |
| **`SQL-006`** | `03-sql-basico`| Cap 03: Agregaciones | Agregaciones condicionales | Lore 03 §7 + Quest 03-03 `conditional_aggregations.sql` | B/A | 🟢 Completado |
| **`SQL-005`** | `03-sql-basico`| Cap 09: Transacciones | `ROLLBACK` y ACID | Lore 09 §5 + Quest 09-03 `transactions_acid.sql` | B/A | 🟢 Completado |
| **`MKT-SQL-002`**| `03-sql-basico`| Cap 09: Modelado | SCD Tipo 2 en Star Schema | Lore 09 §6 + Quest 09-04 `scd_type2_dim.sql` | B/A | 🟢 Completado |
|---|---|---|---|---|---|---|
| **`DE-007`** | `04-de-pipelines`| Cap 01: Extracción API | Paginación resiliente de APIs | Lore 01 §3 + Quest 01-02 `api_paginator.py` | B/A | 🟢 Completado |
| **`DE-004`** | `04-de-pipelines`| Cap 04: Carga DB | Carga a PostgreSQL real | Docker Compose Postgres + Quest `postgres_loader.py` (`M1`) | B/A | 🟢 Completado |
| **`DE-009`** | `04-de-pipelines`| Cap 05: Orquestación | Logs estructurados de run | Lore 05 + Quest `fincorp_orchestrator.py` (`M2`) | B/A | 🟢 Completado |
| **`DE-005`** | `04-de-pipelines`| Cap 05: Orquestación | Orquestación Periódica/Airflow | Lore 05 §5-6 + Quest `fincorp_orchestrator.py` (`M2`) | B/A | 🟢 Completado |
|---|---|---|---|---|---|---|
| **`AWS-004`** | `05-cloud-aws` | Cap 00: Seguridad IAM | IAM Programático | Lore 00 §3.1-3.2 + Quest `fincorp_iam.py` (`M4`) | B/A | 🟢 Completado |
| **`AWS-010`** | `05-cloud-aws` | Cap 00: Seguridad IAM | Profundidad de políticas IAM | Lore 00 §3.1-3.2 + Quest `fincorp_iam.py` (`M4`) | B/A | 🟢 Completado |
| **`AWS-005`** | `05-cloud-aws` | Cap 01: Storage S3 | Creación de Buckets | Lore 01 §3.1 + Quest `fincorp_s3_parquet.py` (`M5`) | B/A | 🟢 Completado |
| **`AWS-006`** | `05-cloud-aws` | Cap 01: Storage S3 | Serialización Parquet | Lore 01 §3.2 + Quest `fincorp_s3_parquet.py` (`M5`) | B/A | 🟢 Completado |
| **`AWS-007`** | `05-cloud-aws` | Cap 02: Bases Cloud | RDS + Security Groups | Lore 02 §3.2 + Quest `fincorp_rds_secrets.py` (`M6`) | B/A | 🟢 Completado |
| **`MKT-AWS-002`**| `05-cloud-aws` | Cap 02: Bases Cloud | Gestión de Secretos (Cero Hardcode) | Lore 02 §3.1 + Quest `fincorp_rds_secrets.py` (`M6`) | B/A | 🟢 Completado |
| **`AWS-008`** | `05-cloud-aws` | Cap 03: Compute Serverless| Despliegue de Lambda | Lore 03 §3.1-3.2 + Quest `fincorp_lambda_deploy.py` (`M7`) | B/A | 🟢 Completado |
| **`AWS-009`** | `05-cloud-aws` | Cap 04: Observabilidad | CloudWatch Alarms | Lore 04 §5.1 + Quest `fincorp_cloudwatch_alarm.py` (`M8`) | B/A | 🟢 Completado |

---

### 3.3 Bloque 2.3 — Tooling Transversal e Integración de Mercado (CLAIM-MKT)


| Componente / MKT ID | Subject(s) | Implementación y Entregable Concreto |
|---|---|---|
| **Docker Compose Base** | Transversal | Archivo `docker-compose.yml` para levantar PostgreSQL efímero y reproducible sin fricción en el host |
| **CI/CD con GitHub Actions** | `DE-PIPELINES`, `CLOUD-AWS` | Workflows `.github/workflows/ci.yml` ejecutando `pytest` y `mypy` en cada push |
| **Data Quality (`DQ`) Explícito**| `DE-PIPELINES` | Suite formal de validación de esquemas y nulos previa a la transformación |
| **Cloud Warehouse Columnar**<br>*(BigQuery / Snowflake)* | `DE-PIPELINES` / Capstone | Carga de datos curados a motor columnar (BigQuery sandbox o DuckDB columnar proxy en local) con compresión y clustering |
| **Apache Airflow Básico** | `DE-PIPELINES` | Creación de DAG productivo con tareas dependientes (`>>`), `PythonOperator`, cron schedule y reintentos automáticos |
| **dbt Básico (Transformación)** | `DE-PIPELINES` | Modelos SQL declarativos modulares (`models/`) con materialización en tabla/vista y tests de unicidad/no-nulos |
| **AWS Athena / Glue (Concepto)**| `CLOUD-AWS` | Registro de catálogo de datos (Glue Catalog) y consultas SQL analíticas sobre S3 con Athena |

---

## 4. Cronograma de Ejecución y Asignación de Carriles

### 4.1 Dinámica de Carriles (A vs B) y Ratificación de la Regla 5
* **Carril B (Arquitecto / Antigravity):** Redacción de capítulos de teoría en `lore/`, actualización formal de temarios en `chronicle.md`, creación de suites de tests evaluadores y generación del andamiaje con plantillas (`pass`).
* **Carril A (Operador):** Resolución activa de las Quests mediante código propio.
* **Regla 5 Inviolable:** Para cada Quest asignada al Operador en Carril A, Antigravity proporcionará:
  1. Enunciado con contrato explícito de entrada/salida.
  2. Fundamento conceptual en Lore.
  3. Ejemplo de modelado con **Domain Shifting** (dominio ficticio, sin código de la solución real).
  4. Comando de prueba binaria con `exit code 0`.

### 4.2 Fases y Duración Estimada
1. **Fase 1: Formalización de `Syllabus 3.0` (Completado ✅)**
   * Actualizado formalmente [`system/docs/05-syllabus-maestro.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/system/docs/05-syllabus-maestro.md) y [`system/docs/06-syllabus-post-empleo-fase2.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/system/docs/06-syllabus-post-empleo-fase2.md).
   * Ratificadas podas en [`content/subjects/python/chronicles/PY-POO/chronicle.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/python/chronicles/PY-POO/chronicle.md) (Typer/Click y Clean Architecture) y delimitado criterio de `load_dotenv` (prohibido en Lambda, tolerado en dev local).
2. **Fase 2: Bloque 2.1 — ROI Inmediato (Completado ✅)**
   * Lore snippets y quests incorporados para `defaultdict` (Lore 03), `tmp_path` y `approx` (Lore 05 y Quest 05-03), fixtures en Lore 03, cardinalidad N:M en Lore 04, `df.groupby` en Lore 02 y `mypy` en Lore 01. Tests en verde con exit code 0.
3. **Fase 3: Bloques 2.2 y 2.3 por Materia (Semana 4-6)**
   * `02-py-poo`: Constructores `super()`, Pydantic, Loaders, TDD.
   * `03-sql-basico`: `ROLLBACK`, SCD Tipo 2, agregaciones condicionales, semántica `NULL`.
   * `04-de-pipelines`: Postgres con Docker, Airflow DAG, dbt básico, paginación, refactorización de `RateError(Exception)`.
   * `05-cloud-aws`: IAM programático con `boto3`, `create_bucket`, Parquet, RDS, Lambda deploy, Secrets Manager.
4. **Fase 4: Tooling Transversal & CI/CD (Semana 6-7)**
   * Configuración de workflows `.github/workflows/ci.yml` y suite de calidad.
5. **Cierre de Gate 2 (Semana 7)**:
   * Ejecución de la batería completa de verificación binaria antes de desbloquear el `PORT-CAPSTONE` (Ola 3).

---

## 5. Criterios Binarios de Aceptación de Gate 2 (Hacia Ola 3)

Para declarar formalmente concluida la Ola 2 y autorizar el inicio del proyecto unificado de portafolio (`PORT-CAPSTONE`):

1. **Bucle de Ejecución Cerrado (Regla 1):** Cada nuevo script, quest y módulo generado debe ejecutarse en un subproceso real finalizando con `exit code 0` o el código de retorno esperado.
2. **Separación Estricta Enunciado / Plantilla / Solución (Regla 2):** Ninguna nueva quest del Operador contendrá soluciones pre-cocinadas (`pass` en plantillas, soluciones aisladas en carpetas de referencia).
3. **Runner Agnóstico (Regla 3):** Toda nueva consulta SQL debe pasar por `system/tools/sql_runner.py` y toda nueva prueba de Python debe ejecutarse con `pytest` en su respectivo `.venv`.
4. **Unidireccionalidad (`Rite ⊆ Lore`) (Regla 4):** Queda terminantemente prohibido evaluar en un test o Rite cualquier concepto que no haya sido explicado previamente en el `lore/`.
5. **Cero Regresión:** Las suites de tests previas de los 4 subjects (consolidadas en Ola 1) deben mantenerse en estado 100% verde sin efectos colaterales.
6. **Desacoplamiento Semántico en Excepciones:** En `DE-PIPELINES`, refactorizar `RateError` para heredar directamente de `Exception` y actualizar el test correspondiente para desacoplarlo de `AssertionError`.
7. **Reconciliación 1:1 Anchor ↔ Material:** El Gate 2 auditará que cada bullet y competencia declarada en `Syllabus 3.0` y en los 4 chronicles cuente con respaldo verificable (capítulo en `lore/`, quest ejecutable o fase de rite), mitigando el riesgo estructural de promesas aspiracionales sin entrega real.
