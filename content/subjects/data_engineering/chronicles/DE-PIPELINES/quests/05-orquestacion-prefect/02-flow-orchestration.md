# Quest 05-02 (Misión M2): Orquestación Periódica y Logging Estructurado con Prefect (`DE-005` + `DE-009`)

**Objetivo:** Ensamblar y orquestar el pipeline de **FinCorp Global** uniendo la extracción resiliente y la carga a PostgreSQL dentro de un Grafo Acíclico Dirigido (`@flow` y `@task`), instrumentando trazabilidad forense con `get_run_logger()` (`DE-009`), políticas de reintentos y calendarización nocturna mediante expresiones Cron (`DE-005`).

---

## Contexto de Negocio (Hilo Conductor: FinCorp Global)

En la **Misión M1 (`DE-004`)** construiste el cargador hacia PostgreSQL (`load_gold_dataframe`), y previamente en **`DE-007`** construiste el extractor paginado de transacciones. Ahora el equipo de Plataforma de **FinCorp Global** necesita que ambos pasos corran automáticamente todas las madrugadas a las **02:00 AM UTC** (`"0 2 * * *"`), dejando auditoría estructurada en los logs de Prefect en cada etapa y reintentando automáticamente ante micro-cortes de red.

---

## Archivo de Trabajo

Edita el archivo [`fincorp_orchestrator.py`](file:///Users/ander/Documents/DoJo/DoJo_Study/content/subjects/data_engineering/chronicles/DE-PIPELINES/quests/05-orquestacion-prefect/fincorp_orchestrator.py).

Debes definir la constante de calendarización e implementar las 2 tareas (`@task`) y el flujo maestro (`@flow`):

### 1. Constante `SCHEDULE_CRON`
* Define en el nivel superior del módulo la expresión Cron para ejecución diaria a las 02:00 AM:
  `SCHEDULE_CRON: str = "0 2 * * *"`

---

### 2. `@task(retries=3, retry_delay_seconds=5)` $\rightarrow$ `extract_fincorp_transactions(fetcher: Callable[[], list[dict[str, Any]]]) -> pd.DataFrame`
* Decora la función con `@task(retries=3, retry_delay_seconds=5)`.
* Obtén el logger de ejecución activo llamando a `logger = get_run_logger()`.
* Registra un mensaje informativo (`logger.info(...)`) antes de extraer.
* Invoca `raw_records = fetcher()` y conviértelo en un `pd.DataFrame(raw_records)`.
* Si el DataFrame resultante está vacío (`df.empty`), registra una advertencia con `logger.warning(...)`. En caso contrario, registra con `logger.info(...)` la cantidad de filas extraídas (`len(df)`).
* Retorna el DataFrame `df`.

---

### 3. `@task` $\rightarrow$ `load_fincorp_gold(df: pd.DataFrame, loader: Callable[[pd.DataFrame], int]) -> int`
* Decora la función con `@task`.
* Obtén el logger con `logger = get_run_logger()`.
* Si `df.empty`, registra un `logger.warning(...)` indicando que se omite la carga y retorna `0` sin llamar a `loader`.
* Si tiene datos, invoca `inserted = loader(df)`, registra con `logger.info(...)` cuántas filas fueron persistidas en PostgreSQL y retorna `inserted`.

---

### 4. `@flow(name="FinCorp_Nightly_ETL")` $\rightarrow$ `fincorp_nightly_flow(fetcher: Callable[[], list[dict[str, Any]]], loader: Callable[[pd.DataFrame], int]) -> int`
* Decora la función con `@flow(name="FinCorp_Nightly_ETL")`.
* Obtén el logger con `logger = get_run_logger()` y registra con `logger.info(...)` el inicio del pipeline nocturno junto con el calendario `SCHEDULE_CRON`.
* Encadena las dos tareas en orden:
  1. `df = extract_fincorp_transactions(fetcher)`
  2. `total_loaded = load_fincorp_gold(df, loader)`
* Registra con `logger.info(...)` el cierre exitoso del flujo y retorna `total_loaded`.

---

## 🧪 Comandos de Verificación Binaria

Ejecuta la suite de pruebas automatizada:
```bash
/Users/ander/Documents/DoJo/DoJo_Study/content/subjects/data_engineering/chronicles/DE-PIPELINES/.venv/bin/pytest content/subjects/data_engineering/chronicles/DE-PIPELINES/quests/05-orquestacion-prefect/test_fincorp_orchestrator.py -v
```
*(Criterio de éxito: 5 passed con exit code 0).*

---

<details>
<summary>👀 Ver Solución de Referencia</summary>

```python
from typing import Any, Callable
import pandas as pd
from prefect import flow, get_run_logger, task

SCHEDULE_CRON: str = "0 2 * * *"


@task(retries=3, retry_delay_seconds=5)
def extract_fincorp_transactions(
    fetcher: Callable[[], list[dict[str, Any]]],
) -> pd.DataFrame:
    logger = get_run_logger()
    logger.info("Iniciando extracción de transacciones FinCorp...")
    records = fetcher()
    df = pd.DataFrame(records)
    if df.empty:
        logger.warning("La extracción no devolvió registros (DataFrame vacío).")
    else:
        logger.info(f"Extracción completada: {len(df)} registros obtenidos.")
    return df


@task
def load_fincorp_gold(
    df: pd.DataFrame,
    loader: Callable[[pd.DataFrame], int],
) -> int:
    logger = get_run_logger()
    if df.empty:
        logger.warning("DataFrame vacío: omitiendo carga hacia PostgreSQL.")
        return 0
    inserted = loader(df)
    logger.info(f"Carga a PostgreSQL completada: {inserted} filas insertadas.")
    return inserted


@flow(name="FinCorp_Nightly_ETL")
def fincorp_nightly_flow(
    fetcher: Callable[[], list[dict[str, Any]]],
    loader: Callable[[pd.DataFrame], int],
) -> int:
    logger = get_run_logger()
    logger.info(f"Ejecutando FinCorp_Nightly_ETL bajo calendario {SCHEDULE_CRON}")
    df = extract_fincorp_transactions(fetcher)
    total_loaded = load_fincorp_gold(df, loader)
    logger.info(f"Flujo finalizado exitosamente. Total cargado: {total_loaded}")
    return total_loaded
```
</details>

