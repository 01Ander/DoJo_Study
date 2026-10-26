# Capítulo 04: Carga de Datos Estructurados a PostgreSQL (SQLAlchemy)

> 🎯 **Objetivo de Negocio:** El inventario curado de la Zona Gold está validado y saneado. Ahora debemos persistirlo de forma masiva, transaccional y permanente en el almacén de datos central (**PostgreSQL de producción**) para que los analistas, modelos de Machine Learning y dashboards de BI consuman información consistente.

En la ingeniería de datos profesional, SQLite es una herramienta excelente para prototipado rápido y pruebas unitarias aisladas en memoria. Sin embargo, **los pipelines de datos de producción exigen motores relacionales cliente-servidor como PostgreSQL**, capaces de soportar cientos de transacciones concurrentes, tipos nativos avanzados (`JSONB`, `UUID`, `TIMESTAMP WITH TIME ZONE`), particionamiento de tablas y control granular de roles y conexiones.

---

## 1. El Driver de Producción y la Cadena de Conexión (Connection URI)

Para comunicar Python con PostgreSQL, **SQLAlchemy** requiere un conector de bajo nivel (*DBAPI driver*). El estándar de la industria es **`psycopg2`** (o `psycopg2-binary`):

```bash
pip install sqlalchemy psycopg2-binary
```

### Anatomía de una Connection URI en PostgreSQL

```text
postgresql+psycopg2://dojo_user:dojo_password@localhost:5432/guild_gold
└──┬───────────────┘  └───┬───┘ └───┬─────────┘ └───┬───┘ └──┬─┘ └───┬──────┘
   │                      │         │               │        │       │
 Dialecto + Driver     Usuario   Contraseña        Host    Puerto Base de Datos
```

* **`dialect+driver`:** Informa a SQLAlchemy qué motor relacional se utilizará (`postgresql`) y a través de qué librería nativa de Python se ejecutarán los sockets (`psycopg2`).
* **Seguridad de Secretos:** Nunca escribas contraseñas en código duro. En pipelines productivos, estos valores se cargan desde variables de entorno (`os.getenv`) o administradores de secretos.

---

## 2. Aprovisionamiento Efímero con Docker Compose

Para evitar instalar PostgreSQL directamente en tu sistema operativo y garantizar reproducibilidad idéntica entre tu máquina local y los servidores de integración continua (CI), el DoJo incluye un archivo `docker-compose.yml` en la raíz del repositorio:

```yaml
services:
  postgres:
    image: postgres:16-alpine
    container_name: dojo_postgres
    environment:
      POSTGRES_USER: dojo_user
      POSTGRES_PASSWORD: dojo_password
      POSTGRES_DB: guild_gold
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

Con una sola instrucción en la terminal, levantas un cluster de PostgreSQL 16 aislado y listo:
```bash
docker compose up -d
```

---

## 3. Configuración de Engines de Producción (Connection Pooling)

Un error crítico en pipelines de datos es abrir y cerrar una conexión TCP nueva por cada fila o lote procesado. SQLAlchemy gestiona automáticamente un **Pool de Conexiones** (*Connection Pool*) reutilizable:

```python
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

# 🎯 Objetivo de Negocio: Instanciar un motor relacional de alto rendimiento con validación de liveness.

def get_postgres_engine(database_uri: str) -> Engine:
    return create_engine(
        database_uri,
        pool_size=5,             # Conexiones persistentes abiertas en el pool
        max_overflow=10,         # Conexiones adicionales permitidas durante picos de carga
        pool_timeout=30,         # Segundos de espera máxima antes de fallar si el pool está lleno
        pool_recycle=1800,       # Recicla conexiones tras 30 min para evitar desconexiones silenciosas
        pool_pre_ping=True       # "Pre-ping": verifica que el socket siga vivo antes de entregar la conexión
    )
```

> **¿Qué hace `pool_pre_ping=True`?**  
> Envía un `SELECT 1` imperceptible antes de ejecutar cualquier consulta. Si el firewall o el servidor cerró la conexión por inactividad, SQLAlchemy la descarta y abre una nueva automáticamente, eliminando errores de desconexión en jobs de larga duración.

---

## 4. Carga Masiva Profesional con Pandas (`to_sql`)

Pandas permite persistir DataFrames enteros directamente hacia PostgreSQL mediante el método `to_sql()`. Sin embargo, hacerlo sin configuración adecuada puede saturar la memoria RAM o generar miles de llamadas HTTP/TCP individuales.

```python
import pandas as pd
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from typing import Any

class DatabaseLoadError(Exception):
    """Excepción de dominio lanzada cuando la carga a base de datos falla."""
    pass

# 🎯 Objetivo de Negocio: Cargar datos en lotes controlados con manejo de errores transaccionales.

def load_dataframe_to_postgres(
    df: pd.DataFrame,
    table_name: str,
    engine: Engine,
    chunksize: int = 1000,
    dtype_mapping: dict[str, Any] | None = None
) -> int:
    """Inserta un DataFrame en PostgreSQL por bloques de forma transaccional.
    
    Retorna:
        Número total de registros cargados con éxito.
    """
    if df.empty:
        return 0

    try:
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists="append",   # 'append' preserva la tabla existente; 'replace' la borra
            index=False,          # Evita crear una columna numérica extra con el índice de Pandas
            chunksize=chunksize,  # Inserta en bloques (evita saturar la memoria con millones de filas)
            method="multi",       # Genera sintaxis multi-tupla: INSERT INTO table VALUES (...), (...)
            dtype=dtype_mapping   # Mapeo explícito a tipos PostgreSQL (opcional)
        )
        return len(df)
    except SQLAlchemyError as err:
        raise DatabaseLoadError(f"Fallo al cargar DataFrame en la tabla '{table_name}': {err}") from err
```

---

> [!NOTE]
> ### 🔍 Desglose de Sintaxis (Zero Surprise Syntax): Carga a BD
> * **`chunksize=1000`:** Divide el DataFrame internamente y emite inserciones en bloques de 1,000 registros, protegiendo al worker de desbordamiento de memoria (*OOM*).
> * **`method="multi"`:** Por defecto, SQLAlchemy ejecuta un `INSERT` por cada fila. `method="multi"` agrupa filas en un único comando SQL con múltiples valores (`VALUES (...), (...)`), acelerando la carga hasta 10 veces en redes de producción.
> * **`if_exists="append"`:** Agrega los nuevos registros sin destruir la tabla ni alterar las llaves primarias existentes.
> * **`DatabaseLoadError`:** Patrón de enmascaramiento defensivo: previene que excepciones internas de la base de datos (con detalles de conexión sensibles) se filtren sin control a capas superiores del sistema.

---

## 5. Verificación de Integridad con SQLAlchemy Core

En pruebas automatizadas y chequeos de reconciliación ETL, validamos la carga consultando directamente la base de datos:

```python
from sqlalchemy import text

# 🎯 Objetivo de Negocio: Verificar que los registros se hayan persistido correctamente en la tabla destino.

with engine.connect() as connection:
    # Contar total de filas
    count_query = text(f"SELECT COUNT(*) FROM {table_name}")
    total_records = connection.execute(count_query).scalar()
    
    # Inspeccionar una muestra
    sample_query = text(f"SELECT * FROM {table_name} LIMIT 5")
    rows = connection.execute(sample_query).fetchall()
```

---

### 🌐 Analogías del Mundo Real (Domain Shifting)

1. **Analogía 1 (Muelle de Carga Portuario — `chunksize` y `method="multi"`):**
   Descargar un barco de 100,000 toneladas llevando una caja individualmente en carretilla colapsa el muelle por congestión. `chunksize` y `method="multi"` equivalen a usar grúas pórtico que bajan contenedores marítimos estandarizados de 40 pies en un solo movimiento coordinado.

2. **Analogía 2 (Red de Bombeo Hidráulico — Connection Pool y `pool_pre_ping`):**
   Si una estación de bomberos tuviera que tender y desenrollar mangueras desde cero cada vez que se detecta humo, el edificio se quemaría. El Connection Pool mantiene líneas presurizadas listas; la válvula `pool_pre_ping` comprueba que la línea tenga agua y presión antes de abrir el grifo.

---

## 6. Misión a Seguir

Dirígete a `quests/04-carga-postgresql/` y completa el laboratorio de carga profesional a base de datos relacional.

