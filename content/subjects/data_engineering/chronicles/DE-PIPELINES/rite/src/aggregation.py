import logging
import pandas as pd

logger = logging.getLogger(__name__)


def aggregate_silver_market(silver_records: list[dict]) -> pd.DataFrame:

    logger.info('Records received: %d', len(silver_records))

    df = pd.DataFrame(silver_records)
    total_stock_by_name = df.groupby('name', as_index=False)[['stock']].sum()
    total_stock_by_name = total_stock_by_name.rename(
        columns={'stock': 'total_stock'})

    logger.info('Ingredients groups produced: %d', len(total_stock_by_name))

    return total_stock_by_name
