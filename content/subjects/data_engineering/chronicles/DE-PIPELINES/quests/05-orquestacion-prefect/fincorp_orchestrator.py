"""
Quest 05-02 (Misión M2): Orquestación Periódica y Logging Estructurado (DE-005 + DE-009)
Dominio: FinCorp Global (Continuidad de DE-007 Extracción y M1 Carga a PostgreSQL)
"""

from typing import Any, Callable
import pandas as pd
from prefect import flow, get_run_logger, task

# TODO 1: Define la expresión Cron estándar para las 02:00 AM todos los días ("0 2 * * *")
SCHEDULE_CRON: str = "0 2 * * *"


# TODO 2: Decora como @task con retries=3 y retry_delay_seconds=5
@task(retries=3, retry_delay_seconds=5)
def extract_fincorp_transactions(
    fetcher: Callable[[], list[dict[str, Any]]],
) -> pd.DataFrame:
    """
    Extrae transacciones invocando `fetcher()`, registra logs con `get_run_logger()`
    (info al iniciar y al extraer con éxito, warning si el DataFrame queda vacío)
    y retorna un DataFrame de Pandas.
    """
    logger = get_run_logger()
    logger.info("Iniciando extraccion")
    raw_records = fetcher()
    df = pd.DataFrame(raw_records)
    if df.empty:
        logger.warning("Transacciones vacias")
    else:
        logger.info(f"Recibidas {len(df)} transacciones")
    return df


# TODO 3: Decora como @task
@task
def load_fincorp_gold(
    df: pd.DataFrame,
    loader: Callable[[pd.DataFrame], int],
) -> int:
    """
    Carga el DataFrame en PostgreSQL invocando `loader(df)`.
    Si `df.empty` es True, emite un `logger.warning(...)` con `get_run_logger()` y retorna 0.
    Si tiene filas, ejecuta `loader(df)`, emite `logger.info(...)` y retorna el total insertado.
    """
    logger = get_run_logger()
    if df.empty:
        logger.warning("Sin registros")
        return 0
    inserted = loader(df)
    logger.info(f"Carga a PostgreSQL completada: {inserted} filas insertadas")
    return inserted


# TODO 4: Decora como @flow con name="FinCorp_Nightly_ETL"
@flow(name="FinCorp_Nightly_ETL")
def fincorp_nightly_flow(
    fetcher: Callable[[], list[dict[str, Any]]],
    loader: Callable[[pd.DataFrame], int],
) -> int:
    """
    Flujo principal que registra su inicio con `get_run_logger()`, encadena
    `extract_fincorp_transactions` -> `load_fincorp_gold` y retorna el total de filas cargadas.
    """
    logger = get_run_logger()
    logger.info(f"Inicio de pipeline sync {SCHEDULE_CRON}")
    df = extract_fincorp_transactions(fetcher)
    total_loaded = load_fincorp_gold(df, loader)
    logger.info(f"Sync finalizado: {total_loaded}")
    return total_loaded
