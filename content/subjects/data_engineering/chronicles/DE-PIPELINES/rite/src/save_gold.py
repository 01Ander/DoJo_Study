import logging
import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine
from src.config import GOLD_TABLE

logger = logging.getLogger(__name__)


def save_gold_inventory(df_gold: pd.DataFrame, db_engine: Engine) -> None:

    df_gold.to_sql(
        name=GOLD_TABLE,
        con=db_engine,
        if_exists='append',
        index=False
    )

    with db_engine.connect() as conn:
        gold_inventory = conn.execute(
            text(f'SELECT * FROM {GOLD_TABLE}')).fetchall()
        logger.info('Rows verified in clean_inventory: %d',
                    len(gold_inventory))
