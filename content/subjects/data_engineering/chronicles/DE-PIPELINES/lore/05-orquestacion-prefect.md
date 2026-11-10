# Capítulo 05: Orquestación Local de Flujos (Prefect)

> 🎯 **Objetivo de Negocio:** Ya tenemos el código para extraer (Cap 01), limpiar (Cap 02), auditar (Cap 03) y guardar (Cap 04). Pero si un alquimista novato tiene que ejecutar el script manualmente todos los días a las 3:00 AM, eventualmente se quedará dormido. Necesitamos al Gran Maestro Alquimista (Orquestador) que dirija el proceso a nivel macro y nos avise si algo falla.

En el mercado laboral, a esto se le llama **Orquestación de Pipelines**. Usaremos **Prefect**, una herramienta moderna construida nativamente en Python.

## 1. El Gran Maestro y sus Ayudantes

*Zero Assumption Setup:* Necesitamos instalar prefect en nuestro entorno.
```bash
pip install prefect
```

**Analogía (El Laboratorio Central):**
Imagina que las funciones de Python que hiciste antes son pequeños ayudantes mágicos (homúnculos). Por sí solos no hacen mucho. Prefect es el Gran Maestro Alquimista. Toma a los ayudantes y les asigna tareas específicas (Tasks). Luego, coordina a todos los ayudantes en un mecanismo principal llamado Flujo (Flow). Si un ayudante tropieza y derrama un vial, el Gran Maestro lo sabe y puede ordenarle intentarlo de nuevo (Retries).

## 2. Decoradores: La Magia de Prefect

En Python, un decorador (el símbolo `@` arriba de una función) es una forma de inyectarle superpoderes a tu función sin cambiar su código interno (conceptos vistos en `PY-POO`).

Prefect usa dos decoradores principales:
- `@task`: Convierte una función normal en un "Ayudante Mágico" observable. Prefect registrará cuánto tarda en ejecutarse y si falló.
- `@flow`: Convierte una función en el "Flujo". Un Flow es el Gran Maestro que manda a llamar a las Tasks.

### Ejemplo Progresivo: El Orquestador Mágico

**El Mal Camino (Script secuencial ciego):**
```python
import time

def get_dust():
    # Si esto falla por un error de red temporal, todo el programa explota 
    # y hay que despertarse a correrlo de nuevo a mano.
    time.sleep(1)
    return "Polvo recolectado"

def potion_master():
    print("Iniciando trabajo...")
    p = get_dust()
    print(f"Terminado: {p}")

# Ejecución ciega
potion_master()
```

**El Buen Camino (Prefect Flow con Retries):**
```python
import time
from prefect import task, flow

# Le damos el superpoder de reintentar hasta 3 veces si hay un error
@task(retries=3, retry_delay_seconds=2)
def get_dust():
    print("Intentando conseguir polvo...")
    # Simulamos un error de red aleatorio
    if int(time.time()) % 2 == 0:
        raise ConnectionError("El mensajero tropezó. Reintentando...")
    return "Polvo recolectado"

# Este es el mecanismo principal
@flow(name="Daily_Potion_Logistics")
def potion_master():
    print("El Gran Maestro Alquimista inicia su turno.")
    p = get_dust() # Llama a la tarea
    print(f"Reporte Final: {p}")

# Ejecución observada
if __name__ == "__main__":
    potion_master()
```

> **Explicación de Sintaxis:**
> - `from prefect import task, flow`: Importamos los decoradores mágicos de Prefect.
> - `@task(retries=3, retry_delay_seconds=2)`: Le decimos a Prefect: "Si esta función lanza un error, no mates el programa. Espera 2 segundos y vuelve a ejecutarla. Ríndete solo si falla 3 veces seguidas".
> - `@flow(name="...")`: Define el punto de entrada principal. Cuando ejecutes este script en tu terminal, verás unos hermosos logs de colores indicando el estado de cada tarea.

## 3. Dependencias y Grafos (DAGs)

Un pipeline rara vez es una sola tarea. Normalmente tienes múltiples pasos: extraer, limpiar, cargar. Estas tareas tienen **dependencias**: no puedes limpiar si la extracción falló.

En orquestación, a esto se le llama un **DAG** (Directed Acyclic Graph - Grafo Acíclico Dirigido). Es una secuencia de tareas donde el flujo viaja en una sola dirección.

En Prefect, las dependencias se crean de forma natural (implícita) simplemente pasando el resultado de una `@task` como parámetro a la siguiente `@task` dentro del `@flow`.

**Ejemplo de DAG (Tareas Dependientes):**
```python
@task(retries=3)
def get_dust():
    return ["polvo", "tierra"]

@task
def clean_dust(raw_data):
    # Esta tarea depende de que get_dust() termine exitosamente y le pase raw_data
    return [item for item in raw_data if item != "tierra"]

@flow(name="Refinery_Pipeline")
def potion_master():
    # El Grafo se construye automáticamente por el paso de datos:
    raw = get_dust()        # Tarea A
    clean = clean_dust(raw) # Tarea B (depende de A)
    print(f"Resultado final: {clean}")
```

**¿Por qué esto mejora la resiliencia?**
Si `get_dust()` falla (y agota sus 3 reintentos), el orquestador marcará la tarea como fallida, y **automáticamente cancelará** `clean_dust()` porque depende de ella. Así evitas que la segunda tarea intente procesar datos que no existen (evitando errores crípticos más adelante).

**Analogía:** El Gran Maestro no envía al Herbolario a limpiar raíces hasta que el Mensajero haya regresado del bosque con ellas. Si el Mensajero se pierde, la orden del Herbolario se cancela automáticamente.

---

## 4. Logging Estructurado de Ejecución con `get_run_logger` (`DE-009`)

En scripts caseros usamos `print()`, pero en un orquestador de producción los `print()` sueltos carecen de severidad (`INFO`, `WARNING`, `ERROR`), no quedan vinculados al identificador único de la corrida (`flow_run_id` / `task_run_id`) y no pueden filtrarse en herramientas de monitoreo.

Prefect provee la función nativa **`get_run_logger()`**, que devuelve un logger contextualizado automáticamente con la tarea o el flujo que se está ejecutando en ese instante.

```python
from prefect import flow, task, get_run_logger

@task(retries=2, retry_delay_seconds=5)
def extract_guild_ledger(endpoint: str) -> list[dict]:
    logger = get_run_logger()
    logger.info(f"Iniciando extracción desde el endpoint: {endpoint}")
    
    records = [{"potion": "Elixir Solar", "qty": 10}]
    logger.info(f"Extracción completada: {len(records)} registros obtenidos.")
    return records

@flow(name="Alchemical_Audit_Flow")
def run_audit_pipeline(endpoint: str) -> int:
    logger = get_run_logger()
    logger.info("Arrancando flujo maestro de auditoría.")
    data = extract_guild_ledger(endpoint)
    logger.info(f"Flujo finalizado con {len(data)} registros procesados.")
    return len(data)
```

> **Regla de Oro de `get_run_logger()`:**  
> Siempre debes instanciar `logger = get_run_logger()` **dentro del cuerpo** de una función decorada con `@task` o `@flow` (nunca en el ámbito global del módulo), ya que necesita un contexto de ejecución activo de Prefect para adjuntar los metadatos de la corrida.

### 4.1 Desacoplamiento de Tareas mediante `Callable` (Inyección de Dependencias)

En pipelines profesionales, las tareas de un orquestador (`@task`) no suelen tener "cableado en duro" el cliente HTTP o el motor de base de datos, sino que reciben la función extractora o cargadora como un parámetro. En Python tipamos una función que se pasa como argumento usando **`Callable`** del módulo `typing`:

```python
from typing import Any, Callable
import pandas as pd

# Callable[[Tipos_De_Entrada], Tipo_De_Retorno]
# 1. Una función que NO recibe argumentos () y devuelve una lista de diccionarios:
FetcherFn = Callable[[], list[dict[str, Any]]]

# 2. Una función que recibe un DataFrame y devuelve un entero (filas insertadas):
LoaderFn = Callable[[pd.DataFrame], int]
```

> **¿Cómo se usa dentro de tu `@task`?**  
> Simplemente la invocas con paréntesis como cualquier función normal:
> * `records = fetcher()` (llama a la función extractora que te pasaron por parámetro).
> * `inserted = loader(df)` (llama a la función cargadora pasándole el DataFrame `df`).
> Esto permite que en producción le pases el extractor real de la API y el cargador real de PostgreSQL, mientras que en los tests le pasas una función simulada rápida (`lambda: [...]`).

---

## 5. Orquestación Periódica y Calendarización (`Schedules` & `Cron`) (`DE-005`)

Un pipeline productivo no depende de que un humano ejecute el comando cada mañana. Se configura con una **política de calendarización (Schedule)** basada en intervalos fijos o en **expresiones Cron** estándar de 5 campos separados por espacios:

```text
  ┌───────────── minuto (0 - 59)
  │ ┌─────────── hora (0 - 23, formato 24h)
  │ │ ┌───────── día del mes (1 - 31)
  │ │ │ ┌─────── mes (1 - 12)
  │ │ │ │ ┌───── día de la semana (0 - 6, donde 0=Domingo, 1=Lunes)
  │ │ │ │ │
  * * * * *
```

* **`"0 2 * * *"`:** En el minuto `0` de la hora `2` (02:00 AM), todos los días del mes (`*`), todos los meses (`*`), todos los días de la semana (`*`).
* **`"*/15 * * * *"`:** Cada 15 minutos (`*/15`).
* **`"0 6 * * 1"`:** Todos los lunes (`1`) a las 06:00 AM (`0 6`).

En Prefect, cualquier `@flow` puede desplegarse y mantenerse escuchando su calendario mediante `.serve()` (o definirse mediante una constante de contrato para el scheduler):

```python
SCHEDULE_CRON = "0 2 * * *"  # Ejecución nocturna diaria a las 02:00 AM

if __name__ == "__main__":
    # Deja un proceso ligero ejecutando el flujo según el calendario Cron
    run_audit_pipeline.serve(
        name="nightly-alchemical-audit",
        cron=SCHEDULE_CRON,
        parameters={"endpoint": "https://api.guild.internal/ledger"}
    )
```

---

## 6. Estándar de Referencia ATS: Equivalencia con Apache Airflow

Aunque **Prefect** es más ergonómico y moderno para escribir pipelines en Python puro, muchos sistemas corporativos legacy y filtros curriculares (ATS) buscan familiaridad con **Apache Airflow**. Ambos resuelven exactamente el mismo problema (construir un **DAG** con tareas, reintentos y calendario), cambiando únicamente la sintaxis:

| Concepto | En Prefect (Pythonic) | En Apache Airflow (Declarativo Clásico) |
|---|---|---|
| **Grafo / Flujo** | `@flow(name="mi_pipeline")` | `with DAG(dag_id="mi_pipeline", schedule="0 2 * * *"):` |
| **Tarea** | `@task(retries=3)` sobre una función | `PythonOperator(task_id="extraer", python_callable=fn)` |
| **Dependencias** | Paso directo de argumentos: `b = limpiar(extraer())` | Operador bitshift explícito: `t_extraer >> t_limpiar >> t_cargar` |
| **Reintentos** | En el decorador `@task(retries=3, retry_delay_seconds=10)` | En el diccionario `default_args={"retries": 3, "retry_delay": timedelta(seconds=10)}` |

```python
# Referencia de arquitectura: Cómo se ve el mismo DAG en Apache Airflow
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    "owner": "data_engineering",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="guild_nightly_etl",
    default_args=default_args,
    schedule="0 2 * * *",
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:
    t_extract = PythonOperator(task_id="extract_potions", python_callable=extract_fn)
    t_load = PythonOperator(task_id="load_postgres", python_callable=load_fn)

    # Definición explícita de dependencia en el grafo (t_extract precede a t_load)
    t_extract >> t_load
```

---

## 7. Conexión con Testing: Cómo Probar `@task`, `@flow` y `get_run_logger()`

Cuando escribimos pruebas unitarias (`pytest`) para pipelines en Prefect, necesitamos validar tres aspectos siguiendo el ciclo **AAA (Arrange, Act, Assert)**:

1. **Inspección de Metadatos del Decorador (`hasattr`, `.retries`, `.name`):**
   Cuando decoras una función con `@task(retries=3, retry_delay_seconds=5)` o `@flow(name="Mi_Flow")`, Prefect transforma la función en un objeto que expone esos parámetros como atributos directos (`mi_tarea.retries`, `mi_tarea.retry_delay_seconds`, `mi_flujo.name`).
2. **Ejecución Aislada de una Tarea con `.fn()`:**
   Si quieres probar únicamente la lógica interna de una `@task` en un test unitario ultrarrápido sin levantar el motor de flujo de Prefect, todo objeto `@task` guarda tu función original en el atributo **`.fn`** (`mi_tarea.fn(...)`).
3. **Mocking de `get_run_logger()` con `unittest.mock.patch`:**
   Como `get_run_logger()` exige un contexto activo de Prefect, al probar una tarea con `.fn()` reemplazamos temporalmente `get_run_logger` con un `MagicMock()` usando `with patch(...)`.

```python
from unittest.mock import MagicMock, patch
import pandas as pd

# 🎯 Objetivo de Negocio: Verificar metadatos del decorador y logs estructurados de una tarea Prefect.

def test_extract_potions_metadata_and_logging():
    # 1. ARRANGE: Preparamos un logger simulado y una función extractora falsa (Callable)
    mock_logger = MagicMock()
    fake_fetcher = lambda: [{"potion": "Mana", "qty": 5}]

    # 2. ACT: Parcheamos get_run_logger y ejecutamos la función subyacente con .fn()
    with patch("__main__.get_run_logger", return_value=mock_logger):
        result_df = extract_guild_ledger.fn("https://api.guild.fake/potions")

    # 3. ASSERT: Validamos metadatos del decorador, resultado y llamadas al logger
    assert extract_guild_ledger.retries == 2
    assert isinstance(result_df, list)
    assert mock_logger.info.call_count >= 1
```

---

## Misión a seguir
Es hora de ensamblar todas las piezas de la Chronicle. Ve a `quests/05-orquestacion-prefect/` y agrégale superpoderes a tus funciones usando los decoradores de Prefect.

> [!TIP]
> **Semantic Commit:** Al finalizar este capítulo y su quest, recuerda hacer un commit semántico en tu repositorio. Ej: `docs(lore): asimilar orquestacion con prefect` o `feat(quests): orquestar pipeline final con flows y tasks`.
