# Quest 04-02: Carga Masiva a PostgreSQL con SQLAlchemy y Connection Pools (Nivel 4)

**Objetivo:** Diseñar un cargador de datos profesional hacia bases de datos relacionales cliente-servidor (PostgreSQL), construyendo URIs de conexión validadas, configurando engines con *connection pooling* y ejecutando cargas masivas segmentadas en *chunks* con manejo de excepciones de dominio (Lore 04).

---

## Contexto de Negocio (Domain Shifting: Ingesta Financiera FinCorp Global)

La firma de inteligencia financiera **FinCorp Global** procesa transacciones conciliadas de la Zona Gold (`gold_transactions`). En el tramo final del pipeline ETL, los DataFrames procesados por Pandas deben persistirse de forma transaccional hacia la base de datos PostgreSQL de producción.

El cargador debe:
1. Construir dinámicamente la Connection URI conforme al estándar `postgresql+psycopg2://...`.
2. Configurar un `Engine` con pool de conexiones y validación pesimista de liveness (`pool_pre_ping`).
3. Persistir DataFrames particionados en bloques (*chunks*) para proteger la memoria, enmascarando cualquier fallo en la excepción de dominio `DatabaseLoadError`.

---

## Archivo de Trabajo

Edita el archivo [`postgres_loader.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/data_engineering/chronicles/DE-PIPELINES/quests/04-carga-postgresql/postgres_loader.py).

Debes implementar la clase de configuración y las dos funciones principales:

### 1. `class DatabaseConfig`
Estructura de datos para modelar los parámetros de conexión:
* Atributos: `host: str`, `port: int`, `database: str`, `username: str`, `password: str`, `driver: str = "postgresql+psycopg2"`.
* Método `get_uri(self) -> str`: Retorna el string formateado:
  `f"{self.driver}://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"`

---

### 2. `create_production_engine(connection_uri: str, pool_size: int = 5, pool_pre_ping: bool = True) -> Engine`
Instancia y retorna un `Engine` de SQLAlchemy configurado con:
* `pool_size = pool_size`
* `pool_pre_ping = pool_pre_ping`

---

### 3. `load_gold_dataframe(df: pd.DataFrame, table_name: str, engine: Engine, chunksize: int = 500) -> int`
Inserta el contenido de un DataFrame en la tabla especificada:
* Si `df.empty`, retorna `0` inmediatamente sin tocar la base de datos.
* Ejecuta `df.to_sql()` con los siguientes parámetros obligatorios:
  - `name = table_name`
  - `con = engine`
  - `if_exists = "append"`
  - `index = False`
  - `chunksize = chunksize`
* Manejo de errores: Si ocurre cualquier excepción `SQLAlchemyError`, captúrala y lanza `DatabaseLoadError` encadenando el error original (`raise DatabaseLoadError(...) from err`).
* Retorna el recuento total de filas insertadas (`len(df)`).

---

### 4. [`Dockerfile`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/data_engineering/chronicles/DE-PIPELINES/quests/04-carga-postgresql/Dockerfile) Multi-Stage para el Worker ETL
Edita también el archivo [`Dockerfile`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/data_engineering/chronicles/DE-PIPELINES/quests/04-carga-postgresql/Dockerfile) en la misma carpeta aplicando el patrón Multi-Stage de Lore 04 (§2.1):
1. **Etapa 1 (`builder`):** `FROM python:3.12-slim AS builder`, `WORKDIR /build`, copia `requirements.txt` y ejecuta `RUN pip install --no-cache-dir --prefix=/install -r requirements.txt`.
2. **Etapa 2 (`runtime`):** `FROM python:3.12-slim AS runtime`, `WORKDIR /app`, declara `ENV PYTHONDONTWRITEBYTECODE=1` y `ENV PYTHONUNBUFFERED=1`.
3. **Copia de artefactos y arranque:** Incluye `COPY --from=builder /install /usr/local`, `COPY postgres_loader.py .` y `CMD ["python", "postgres_loader.py"]`.

---

## 🧪 Comandos de Verificación Binaria

Ejecuta la suite de pruebas unitarias automatizada:
```bash
/Users/ander/Documents/DoJo/DoJo_Study/content/subjects/data_engineering/chronicles/DE-PIPELINES/.venv/bin/pytest content/subjects/data_engineering/chronicles/DE-PIPELINES/quests/04-carga-postgresql/test_postgres_loader.py -v
```
*(Criterio de éxito: 6 passed con exit code 0).*

---

<details>
<summary>👀 Ver Solución de Referencia</summary>

```python
from dataclasses import dataclass
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

class DatabaseLoadError(Exception):
    pass

@dataclass
class DatabaseConfig:
    host: str
    port: int
    database: str
    username: str
    password: str
    driver: str = "postgresql+psycopg2"

    def get_uri(self) -> str:
        return f"{self.driver}://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"

def create_production_engine(connection_uri: str, pool_size: int = 5, pool_pre_ping: bool = True) -> Engine:
    return create_engine(connection_uri, pool_size=pool_size, pool_pre_ping=pool_pre_ping)

def load_gold_dataframe(df: pd.DataFrame, table_name: str, engine: Engine, chunksize: int = 500) -> int:
    if df.empty:
        return 0
    try:
        df.to_sql(name=table_name, con=engine, if_exists="append", index=False, chunksize=chunksize)
        return len(df)
    except SQLAlchemyError as err:
        raise DatabaseLoadError(f"Failed to load into {table_name}: {err}") from err
```
</details>
