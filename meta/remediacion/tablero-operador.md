# 🎯 Tablero de Acción del Operador — Ola 2

> **Propósito:** Registro directo, claro y accionable de las tareas que el Operador debe programar (Carril A) y de los nuevos cambios introducidos en el sistema (Carril B), sin la sobrecarga del roadmap general.  
> **Última Actualización:** 2026-10-21  
> **Materia Activa:** `03-sql-basico` (SQL Básico, Modelado y Transacciones)

---

## 1. Radar de Progreso de Tareas del Operador (Carril A)

### 🐍 Fase 1: `02-py-poo` (100% COMPLETADO 🟢)
| Tarea ID | Materia | Concepto | Archivo editado | Estado |
|---|---|---|---|---|
| `PY-010` | `02-py-poo` | Constructores con `super()` | `quests/02-entities/rpg_character.py` | 🟢 **COMPLETADO** |
| `PY-011.1` | `02-py-poo` | De Dataclass a Pydantic con `Field` | `quests/06-logging/user_account_schema.py` | 🟢 **COMPLETADO** |
| `PY-011.2` | `02-py-poo` | Validadores de Negocio y Excepciones | `quests/06-logging/transaction_schema.py` | 🟢 **COMPLETADO** |
| `PY-013` | `02-py-poo` | Patrón Output Loaders | `quests/04-orchestration/output_loaders.py` | 🟢 **COMPLETADO** |
| `PY-014` | `02-py-poo` | Extractor desacoplado CSV/JSON | `quests/01-abstractions/data_extractors.py` | 🟢 **COMPLETADO** |
| `PY-020` | `02-py-poo` | Ciclo TDD Red-Green-Refactor | `quests/05-testing/billing_service.py` | 🟢 **COMPLETADO** |

---

### 🗄️ Fase 2: `03-sql-basico` (100% COMPLETADO 🟢)
| Tarea ID | Materia | Ubicación | Concepto | Archivo que debes editar | Comando de Verificación | Estado |
|---|---|---|---|---|---|---|
| **`SQL-013`** | `03-sql-basico` | Cap 02: Filtros | Semántica 3VL de `NULL`, trampa de `NOT IN` y `COALESCE` | [`quests/02-filtering/null_semantics.sql`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/quests/02-filtering/null_semantics.sql) | `pytest quests/02-filtering/test_null_semantics.py` | 🟢 **COMPLETADO** |
| **`SQL-006`** | `03-sql-basico` | Cap 03: Agregaciones | Agregaciones condicionales `SUM(CASE WHEN...)` | [`quests/03-functions/conditional_aggregations.sql`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/quests/03-functions/conditional_aggregations.sql) | `pytest quests/03-functions/test_conditional_aggregations.py` | 🟢 **COMPLETADO** |
| **`SQL-005`** | `03-sql-basico` | Cap 09: Transacciones | Transacciones explícitas, `ROLLBACK`, `SAVEPOINT` y ACID | [`quests/09-integrity/transactions_acid.sql`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/quests/09-integrity/transactions_acid.sql) | `pytest quests/09-integrity/test_transactions_acid.py` | 🟢 **COMPLETADO** |
| **`MKT-SQL-002`**| `03-sql-basico` | Cap 09: Modelado | SCD Tipo 2 en Star Schema dimensional | [`quests/09-integrity/scd_type2_dim.sql`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/sql/chronicles/SQL-BASICO/quests/09-integrity/scd_type2_dim.sql) | `pytest quests/09-integrity/test_scd_type2_dim.py` | 🟢 **COMPLETADO** |

---

### ⚙️ Fase 3: `04-de-pipelines` (En Curso 🟡)
| Tarea ID | Materia | Ubicación | Concepto | Archivo que debes editar | Comando de Verificación | Estado |
|---|---|---|---|---|---|---|
| **`DE-007`** | `04-de-pipelines` | Cap 01: Extracción API | Paginación resiliente (Offset & Cursor) y Rate Limits | [`quests/01-extraccion-api/api_paginator.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/data_engineering/chronicles/DE-PIPELINES/quests/01-extraccion-api/api_paginator.py) | `pytest quests/01-extraccion-api/test_api_pagination.py` | 🟡 **ACTIVA (Tu turno)** |
| **`DE-004`** | `04-de-pipelines` | Cap 04: Carga DB | Carga a PostgreSQL real con Docker Compose | `quests/04-carga-postgresql/postgres_loader.py` | — | ⏳ En espera |
| **`DE-009`** | `04-de-pipelines` | Cap 05: Orquestación | Logs estructurados de run (`get_run_logger`) | `quests/05-orquestacion-prefect/flow_logger.py` | — | ⏳ En espera |
| **`DE-005`** | `04-de-pipelines` | Cap 05: Orquestación | Orquestación Periódica/Airflow básico | `quests/05-orquestacion-prefect/airflow_dag.py` | — | ⏳ En espera |

---

## 2. 🚀 MISIÓN ACTIVA: `DE-007` — Consumo Resiliente de APIs con Paginación y Rate Limiting (AeroFleet Telemetry)

* **Materia:** `04-de-pipelines` (Capítulo 01: Extracción Automatizada — APIs REST)  
* **Archivo a editar por el Operador:** [`content/subjects/data_engineering/chronicles/DE-PIPELINES/quests/01-extraccion-api/api_paginator.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/data_engineering/chronicles/DE-PIPELINES/quests/01-extraccion-api/api_paginator.py)  
* **Enunciado de la Quest:** [`content/subjects/data_engineering/chronicles/DE-PIPELINES/quests/01-extraccion-api/02-api-pagination.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/data_engineering/chronicles/DE-PIPELINES/quests/01-extraccion-api/02-api-pagination.md)  
* **Teoría de Respaldo:** [`content/subjects/data_engineering/chronicles/DE-PIPELINES/lore/01-extraccion-api.md` (§3)](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/data_engineering/chronicles/DE-PIPELINES/lore/01-extraccion-api.md#3-paginación-cuando-el-catálogo-es-masivo)

### 📋 El Contrato que debes cumplir:

Implementa en [`api_paginator.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/data_engineering/chronicles/DE-PIPELINES/quests/01-extraccion-api/api_paginator.py) las dos funciones extractoras:

1. **`extract_paginated_offset(api_url: str, token: str, page_size: int = 20, max_pages: int = 50) -> list[dict[str, Any]]`**
   * Envía cabecera `Authorization: Bearer <token>`.
   * Itera iniciando en `page = 1`, enviando `params={"page": page, "limit": page_size}`.
   * Extrae la lista bajo la llave `"data"` de la respuesta JSON.
   * **Deduplicación:** Filtra registros duplicados por `"id"` usando un `set()` de memoria.
   * **Parada:** Detén el bucle si `batch` está vacío, si `len(batch) < page_size`, o si `page > max_pages`.
   * Retorna la lista acumulada de diccionarios únicos.

2. **`extract_paginated_cursor(api_url: str, token: str, max_pages: int = 50, max_retries: int = 3) -> list[dict[str, Any]]`**
   * Envía cabecera `Authorization: Bearer <token>`.
   * Envía `params={"limit": 50}` (y añade `"cursor": next_cursor` si `next_cursor` no es `None`).
   * **Resiliencia ante Rate Limits (HTTP 429):**
     * Si `response.status_code == 429`:
       * Extrae el tiempo de espera de `response.headers.get("Retry-After", 1.0)`.
       * Ejecuta `time.sleep(wait_time)`.
       * Reintenta hasta `max_retries` veces.
       * Si se agotan los reintentos, lanza `RateLimitExceededError`.
     * Para otros estados no exitosos, llama `response.raise_for_status()`.
   * Acumula los elementos de `"items"`.
   * Extrae `"next_cursor"` del payload: si es `None` o vacío, o si `pages_processed >= max_pages`, termina el bucle.
   * Retorna la lista acumulada de eventos.

---

### 💡 Ejemplo con Domain Shifting (Ingesta de Clientes CRM):

```python
# 🎯 Objetivo de Negocio: Extraer leads paginados por offset deduplicando contactos y respetando límite de seguridad.

def extract_crm_leads(api_url: str, api_key: str, page_size: int = 10, max_pages: int = 20) -> list[dict]:
    headers = {"Authorization": f"Bearer {api_key}"}
    leads = []
    seen_emails = set()
    page = 1

    while page <= max_pages:
        resp = requests.get(api_url, headers=headers, params={"page": page, "limit": page_size}, timeout=10)
        resp.raise_for_status()
        batch = resp.json().get("leads", [])
        
        if not batch:
            break

        for item in batch:
            email = item.get("email")
            if email and email not in seen_emails:
                seen_emails.add(email)
                leads.append(item)

        if len(batch) < page_size:
            break

        page += 1

    return leads
```

---

### 🧪 Comandos de Verificación Binaria:

```bash
/Users/ander/Documents/DoJo/DoJo_Study/content/subjects/data_engineering/chronicles/DE-PIPELINES/.venv/bin/pytest content/subjects/data_engineering/chronicles/DE-PIPELINES/quests/01-extraccion-api/test_api_pagination.py -v
```
*(Criterio de éxito: 5 passed con exit code 0).*

---

## 3. Bitácora de Cambios del Sistema (Carril B — Antigravity)

Registro de archivos nuevos o actualizados en el sistema bajo las reglas de `09-generation-protocol.md`:

* `content/subjects/sql/chronicles/SQL-BASICO/quests/09-integrity/scd_type2_dim.sql`:
  * *Cambio:* **Implementado y aprobado por el Operador (`3/3 passed`, exit code 0). Cierre definitivo de la materia `03-sql-basico`.**
* `content/subjects/data_engineering/chronicles/DE-PIPELINES/lore/01-extraccion-api.md`:
  * *Cambio:* Sección 3 profundamente expandida con teoría de paginación por Offset vs Cursor, resiliencia ante Rate Limits (HTTP 429), cabecera `Retry-After`, backoff, deduplicación y salvaguardas de bucles.
* `content/subjects/data_engineering/chronicles/DE-PIPELINES/quests/01-extraccion-api/02-api-pagination.md`:
  * *Cambio:* Enunciado didáctico de la Quest 01-02 (`DE-007`).
* `content/subjects/data_engineering/chronicles/DE-PIPELINES/quests/01-extraccion-api/api_paginator.py`:
  * *Cambio:* Plantilla inicial para el Operador con `RateLimitExceededError` y funciones `extract_paginated_offset` y `extract_paginated_cursor`.
* `content/subjects/data_engineering/chronicles/DE-PIPELINES/quests/01-extraccion-api/test_api_pagination.py`:
  * *Cambio:* Suite evaluadora automatizada con 5 tests unitarios validando paginación multi-página, deduplicación, salvaguarda de páginas máximas, cursores continuos y reintentos ante HTTP 429.








