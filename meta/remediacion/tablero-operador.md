# 🎯 Tablero de Acción del Operador — Ola 2

> **Propósito:** Registro directo, claro y accionable de las tareas que el Operador debe programar (Carril A) y de los nuevos cambios introducidos en el sistema (Carril B), sin la sobrecarga del roadmap general.  
> **Última Actualización:** 2026-10-26  
> **Materia Activa:** `04-de-pipelines` (Data Pipelines, ETL, PostgreSQL y Prefect)

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
| **`DE-007`** | `04-de-pipelines` | Cap 01: Extracción API | Paginación resiliente (Offset & Cursor) y Rate Limits | [`quests/01-extraccion-api/api_paginator.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/data_engineering/chronicles/DE-PIPELINES/quests/01-extraccion-api/api_paginator.py) | `pytest quests/01-extraccion-api/test_api_pagination.py` | 🟢 **COMPLETADO** |
| **`DE-004`** | `04-de-pipelines` | Cap 04: Carga DB | Carga a PostgreSQL real con Docker Compose | [`quests/04-carga-postgresql/postgres_loader.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/data_engineering/chronicles/DE-PIPELINES/quests/04-carga-postgresql/postgres_loader.py) | `pytest quests/04-carga-postgresql/test_postgres_loader.py` | 🟡 **ACTIVA (Tu turno)** |
| **`DE-009`** | `04-de-pipelines` | Cap 05: Orquestación | Logs estructurados de run (`get_run_logger`) | `quests/05-orquestacion-prefect/flow_logger.py` | — | ⏳ En espera |
| **`DE-005`** | `04-de-pipelines` | Cap 05: Orquestación | Orquestación Periódica/Airflow básico | `quests/05-orquestacion-prefect/airflow_dag.py` | — | ⏳ En espera |

---

## 2. 🚀 MISIÓN ACTIVA: `DE-004` — Carga Masiva a PostgreSQL con SQLAlchemy y Connection Pools (FinCorp Global)

* **Materia:** `04-de-pipelines` (Capítulo 04: Carga de Datos Estructurados a PostgreSQL)  
* **Archivo a editar por el Operador:** [`content/subjects/data_engineering/chronicles/DE-PIPELINES/quests/04-carga-postgresql/postgres_loader.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/data_engineering/chronicles/DE-PIPELINES/quests/04-carga-postgresql/postgres_loader.py)  
* **Enunciado de la Quest:** [`content/subjects/data_engineering/chronicles/DE-PIPELINES/quests/04-carga-postgresql/02-postgres-loader.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/data_engineering/chronicles/DE-PIPELINES/quests/04-carga-postgresql/02-postgres-loader.md)  
* **Teoría de Respaldo:** [`content/subjects/data_engineering/chronicles/DE-PIPELINES/lore/04-carga-postgresql.md`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/data_engineering/chronicles/DE-PIPELINES/lore/04-carga-postgresql.md)

### 📋 El Contrato que debes cumplir:

Implementa en [`postgres_loader.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/data_engineering/chronicles/DE-PIPELINES/quests/04-carga-postgresql/postgres_loader.py) los 3 componentes:

1. **`class DatabaseConfig` (Método `get_uri(self) -> str`)**
   * Retorna la URI con formato estándar:
     `f"{self.driver}://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"`

2. **`create_production_engine(connection_uri: str, pool_size: int = 5, pool_pre_ping: bool = True) -> Engine`**
   * Retorna un `create_engine(connection_uri, pool_size=pool_size, pool_pre_ping=pool_pre_ping)`.

3. **`load_gold_dataframe(df: pd.DataFrame, table_name: str, engine: Engine, chunksize: int = 500) -> int`**
   * Si `df.empty`: retorna `0`.
   * Bloque `try / except SQLAlchemyError as err`:
     * Ejecuta `df.to_sql(name=table_name, con=engine, if_exists="append", index=False, chunksize=chunksize)`.
     * Retorna `len(df)`.
     * Si falla, lanza `raise DatabaseLoadError(f"Fallo al cargar en {table_name}: {err}") from err`.

---

### 💡 Ejemplo con Domain Shifting (Ingesta Logística LogiTrack):

```python
# 🎯 Objetivo de Negocio: Construir connection URI y persistir despachos de transporte por bloques.

@dataclass
class FleetDbConfig:
    host: str
    port: int
    db: str
    user: str
    pwd: str

    def build_url(self) -> str:
        return f"postgresql+psycopg2://{self.user}:{self.pwd}@{self.host}:{self.port}/{self.db}"

def persist_shipments(df: pd.DataFrame, table: str, engine: Engine) -> int:
    if df.empty:
        return 0
    try:
        df.to_sql(name=table, con=engine, if_exists="append", index=False, chunksize=250)
        return len(df)
    except SQLAlchemyError as err:
        raise DatabaseLoadError(f"Error persisting to {table}") from err
```

---

### 🧪 Comandos de Verificación Binaria:

```bash
/Users/ander/Documents/DoJo/DoJo_Study/content/subjects/data_engineering/chronicles/DE-PIPELINES/.venv/bin/pytest content/subjects/data_engineering/chronicles/DE-PIPELINES/quests/04-carga-postgresql/test_postgres_loader.py -v
```
*(Criterio de éxito: 5 passed con exit code 0).*

---

## 3. Bitácora de Cambios del Sistema (Carril B — Antigravity)

Registro de archivos nuevos o actualizados en el sistema bajo las reglas de `09-generation-protocol.md`:

* `docker-compose.yml`:
  * *Cambio:* Creado en la raíz del proyecto para aprovisionamiento local de PostgreSQL 16 Alpine con healthcheck.
* `content/subjects/data_engineering/chronicles/DE-PIPELINES/quests/01-extraccion-api/api_paginator.py`:
  * *Cambio:* **Implementado y aprobado por el Operador (`5/5 passed`, exit code 0). Cierre formal de la brecha `DE-007`.**
* `content/subjects/data_engineering/chronicles/DE-PIPELINES/lore/04-carga-postgresql.md`:
  * *Cambio:* Reescribo exhaustivo con driver `psycopg2`, Connection URIs formales, Docker Compose, Connection Pooling (`pool_pre_ping=True`) y carga masiva por chunks.
* `content/subjects/data_engineering/chronicles/DE-PIPELINES/quests/04-carga-postgresql/02-postgres-loader.md`:
  * *Cambio:* Enunciado didáctico de la Quest 04-02 (`DE-004`).
* `content/subjects/data_engineering/chronicles/DE-PIPELINES/quests/04-carga-postgresql/postgres_loader.py`:
  * *Cambio:* Plantilla inicial para el Operador con `DatabaseConfig`, `create_production_engine` y `load_gold_dataframe`.
* `content/subjects/data_engineering/chronicles/DE-PIPELINES/quests/04-carga-postgresql/test_postgres_loader.py`:
  * *Cambio:* Suite evaluadora automatizada con 5 tests unitarios validando formato de URI, pooling, inserción en chunks y captura de errores.








