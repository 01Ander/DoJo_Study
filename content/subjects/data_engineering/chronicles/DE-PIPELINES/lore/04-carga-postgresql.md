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

## 2. Contenerización Pragmática: `Dockerfile` Multi-Stage y `docker-compose.yml`

En la ingeniería de datos moderna, instalar bases de datos o librerías del sistema directamente en el sistema operativo anfitrión (*host*) provoca conflictos de versiones ("en mi máquina sí funciona"). **Docker** resuelve esto empaquetando el código Python y la base de datos PostgreSQL en unidades estandarizadas.

### 2.0 Los 3 Conceptos Base (Para entender Docker a primera vista)

Antes de ver código, distingue estas tres piezas:
1. **Imagen (*Image*):** Es una **plantilla inmutable (congelada)** que contiene el sistema operativo mínimo (ej. Linux Debian Slim), Python instalado y tus librerías. Piensa en ella como el **plano o molde** de una fábrica.
2. **Contenedor (*Container*):** Es una **instancia viva en ejecución** creada a partir de una Imagen. Puedes levantar, detener o destruir 10 contenedores idénticos a partir del mismo molde sin ensuciar tu Mac.
3. **`Dockerfile` vs. `docker-compose.yml`:**
   * El **`Dockerfile`** construye **una** imagen propia (por ejemplo, la imagen de tu worker de Python).
   * El **`docker-compose.yml`** conecta y enciende **varios contenedores a la vez** (por ejemplo: tu worker de Python + el servidor de PostgreSQL) dentro de una misma red virtual.

### 2.1 Creación de Imágenes Reproducibles con `Dockerfile` Multi-Stage

Un `Dockerfile` es una lista secuencial de instrucciones en mayúsculas. En producción usamos el patrón **Multi-Stage Build** (construcción en dos etapas: `builder` y `runtime`).

**¿Por qué dos etapas en vez de una sola?**
Algunas librerías de datos (como `psycopg2` o `pyarrow`) necesitan compiladores de C pesadísimos para instalarse. Si instalamos todo en una sola etapa, la imagen final pesará casi 1 GB y tendrá herramientas innecesarias. Con **Multi-Stage**:
* En la **Etapa 1 (`builder`)** instalamos los paquetes en una carpeta limpia (`/install`).
* En la **Etapa 2 (`runtime`)** partimos de un Python virgen y **solo copiamos la carpeta `/install` ya lista**, logrando una imagen ligera y segura.

```dockerfile
# ==========================================
# ETAPA 1: Builder (Instalación y compilación)
# ==========================================
FROM python:3.12-slim AS builder

WORKDIR /build

# Evita archivos .pyc y fuerza logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ==========================================
# ETAPA 2: Runtime (Imagen limpia de producción)
# ==========================================
FROM python:3.12-slim AS runtime

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copiamos únicamente los paquetes ya instalados desde la etapa builder
COPY --from=builder /install /usr/local

# Copiamos el código fuente del pipeline
COPY src/ ./src/

# Comando por defecto al iniciar el contenedor
CMD ["python", "-m", "src.pipeline"]
```

> [!NOTE]
> ### 🔍 Desglose de Sintaxis (Zero Surprise Syntax): Instrucciones del `Dockerfile`
> * **`FROM python:3.12-slim AS builder`:** Descarga la imagen oficial ligera (`slim`) de Python 3.12 y bautiza esta primera etapa con el alias `builder`.
> * **`WORKDIR /build`:** Equivale a hacer `mkdir -p /build && cd /build` dentro del contenedor. Todos los comandos siguientes (`COPY`, `RUN`, `CMD`) se ejecutarán dentro de esa carpeta.
> * **`ENV VARIABLE=valor`:** Define variables de entorno permanentes dentro del contenedor:
>   * `PYTHONDONTWRITEBYTECODE=1`: Impide que Python genere archivos `.pyc` (innecesarios en contenedores efímeros).
>   * `PYTHONUNBUFFERED=1`: Desactiva el buffer de salida de Python para que cualquier log aparezca instantáneamente en la consola de Docker.
> * **`COPY <origen_host> <destino_contenedor>`:** Copia archivos desde tu carpeta local hacia el contenedor (el punto `.` significa "el `WORKDIR` actual").
> * **`RUN pip install --no-cache-dir --prefix=/install -r requirements.txt`:** Ejecuta un comando durante la construcción de la imagen. `--no-cache-dir` evita guardar basura de descarga, y `--prefix=/install` guarda todas las librerías instaladas dentro de `/install` para poder mudarlas fácilmente a la etapa 2.
> * **`COPY --from=builder /install /usr/local`:** La magia del *Multi-Stage*: toma las librerías que dejó listas la etapa `builder` en `/install` y las coloca en `/usr/local` de la etapa `runtime` (donde Python busca los paquetes globales).
> * **`CMD ["ejecutable", "arg1", ...]`:** Define el comando que correrá automáticamente cuando el contenedor se encienda. Se escribe en formato lista JSON (*exec form*).

### 2.2 Orquestación Local Multi-Contenedor con `docker-compose.yml` e `init.sql`

Mientras el `Dockerfile` define **una** imagen, **`docker-compose.yml`** orquesta **múltiples contenedores** conectados a través de una red virtual interna, gestionando volúmenes persistentes, scripts de arranque (`init.sql`) y controles de salud (*healthchecks*):

```yaml
services:
  postgres:
    image: postgres:16-alpine
    container_name: dojo_postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-dojo_user}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-dojo_password}
      POSTGRES_DB: ${POSTGRES_DB:-guild_gold}
    ports:
      - "${POSTGRES_PORT:-5432}:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./docker/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    networks:
      - dojo_net
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-dojo_user} -d ${POSTGRES_DB:-guild_gold}"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:

networks:
  dojo_net:
    driver: bridge
```

* **`/docker-entrypoint-initdb.d/init.sql:ro`:** Todo archivo `.sql` montado en esa ruta oficial de la imagen de PostgreSQL se ejecuta automáticamente al inicializar el volumen por primera vez (ideal para crear esquemas o tablas base en modo solo lectura `:ro`).
* **`healthcheck` (`pg_isready`):** Verifica que el motor PostgreSQL no solo haya arrancado como proceso, sino que ya esté aceptando conexiones TCP antes de que el pipeline intente cargar datos.
* **`networks` (`dojo_net`):** Aísla el tráfico entre el contenedor del pipeline y la base de datos en una red bridge privada.

Con una sola instrucción en la terminal levantas el clúster local:
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

def get_postgres_engine(
    database_uri: str,
    pool_size: int = 5,
    pool_pre_ping: bool = True,
) -> Engine:
    return create_engine(
        database_uri,
        pool_size=pool_size,         # Conexiones persistentes abiertas en el pool
        pool_pre_ping=pool_pre_ping, # "Pre-ping": verifica que el socket siga vivo antes de entregar la conexión
    )
```

> **Nota sobre argumentos de `create_engine()`:**  
> `create_engine` solo recibe `database_uri` como argumento posicional. Todos los parámetros de configuración (`pool_size=...`, `pool_pre_ping=...`) **deben pasarse siempre por nombre (`keyword arguments`)**. En servidores PostgreSQL dedicados también existen parámetros opcionales de ajuste fino como `max_overflow` o `pool_recycle`, pero no se usan cuando el mismo código se testea contra `sqlite:///:memory:`.

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
> * **`DatabaseLoadError` y `raise ... from err` (*Exception Chaining*):** Cuando capturamos un error técnico bajo (`except SQLAlchemyError as err:`) y lanzamos nuestra propia excepción de dominio con `raise DatabaseLoadError("...") from err`, el keyword **`from err`** preserva la causa original adjunta (`__cause__`). Así los logs de auditoría muestran tanto el error de negocio como el fallo exacto de SQL subyacente.

---

## 5. Conexión con Testing: Cómo Probar Cargadores SQL sin Levantar Servidores

En pruebas unitarias automatizadas (`pytest`), levantar un contenedor pesado para cada test haría que la suite sea lenta. Gracias a que SQLAlchemy abstrae el motor mediante el objeto `Engine`, podemos probar toda la lógica de nuestro cargador (`to_sql`, `chunksize`, conteo de filas y manejo de errores) inyectando un `Engine` ligero en memoria (`sqlite:///:memory:`) y siguiendo el **ciclo AAA (Arrange, Act, Assert)**:

```python
import pandas as pd
import pytest
from sqlalchemy import create_engine, text

# 🎯 Objetivo de Negocio: Validar mediante el ciclo AAA que el cargador persiste lotes y envuelve fallos.

def test_load_dataframe_persists_all_chunks():
    # 1. ARRANGE: Preparamos un Engine en memoria y un DataFrame de prueba
    engine = create_engine("sqlite:///:memory:")
    df_potions = pd.DataFrame([
        {"potion_id": "P-01", "stock": 50},
        {"potion_id": "P-02", "stock": 30},
    ])

    # 2. ACT: Ejecutamos la función real de carga con chunksize pequeño
    inserted = load_dataframe_to_postgres(df_potions, "gold_potions", engine, chunksize=1)

    # 3. ASSERT: Verificamos tanto el valor retornado como los registros reales en la BD
    assert inserted == 2
    with engine.connect() as conn:
        total_in_db = conn.execute(text("SELECT COUNT(*) FROM gold_potions")).scalar()
        assert total_in_db == 2


def test_load_dataframe_wraps_sqlalchemy_error():
    # 1. ARRANGE: Preparamos un DataFrame válido pero un engine inválido
    df_potions = pd.DataFrame([{"potion_id": "P-01", "stock": 50}])
    broken_engine = object()  # Objeto que no es un Engine válido

    # 2. ACT & 3. ASSERT: Verificamos que se lance nuestra excepción de dominio
    with pytest.raises(DatabaseLoadError):
        load_dataframe_to_postgres(df_potions, "gold_potions", broken_engine)  # type: ignore
```

> **Desglose de Sintaxis de Testing:**
> * **`conn.execute(text("SELECT COUNT(*) ...")).scalar()`:** `text()` envuelve una consulta SQL cruda de forma segura en SQLAlchemy 2.0, y `.scalar()` extrae directamente el primer valor de la primera fila (por ejemplo, el entero `2` en lugar de una tupla `(2,)`).

---

### 🌐 Analogías del Mundo Real (Domain Shifting)

1. **Analogía 1 (Muelle de Carga Portuario — `chunksize` y `method="multi"`):**
   Descargar un barco de 100,000 toneladas llevando una caja individualmente en carretilla colapsa el muelle por congestión. `chunksize` y `method="multi"` equivalen a usar grúas pórtico que bajan contenedores marítimos estandarizados de 40 pies en un solo movimiento coordinado.

2. **Analogía 2 (Red de Bombeo Hidráulico — Connection Pool y `pool_pre_ping`):**
   Si una estación de bomberos tuviera que tender y desenrollar mangueras desde cero cada vez que se detecta humo, el edificio se quemaría. El Connection Pool mantiene líneas presurizadas listas; la válvula `pool_pre_ping` comprueba que la línea tenga agua y presión antes de abrir el grifo.

---

## 6. Misión a Seguir

Dirígete a `quests/04-carga-postgresql/` y completa el laboratorio de carga profesional a base de datos relacional.

