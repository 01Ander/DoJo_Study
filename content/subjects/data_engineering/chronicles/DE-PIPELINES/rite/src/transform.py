import pandas as pd
import json
import logging
from src.config import RESULT_KEY

logger = logging.getLogger(__name__)


def transform_market_catalog(path: str) -> list[dict]:
    with open(path, encoding='utf-8') as fh:
        payload = json.load(fh)

    logger.info('Bronze records loaded: %d', len(payload[RESULT_KEY]))

    df = pd.DataFrame(payload[RESULT_KEY])
    df = df.dropna()
    df['name'] = df['name'].str.strip().str.lower()
    df['price'] = df['price'].astype(int)
    clean_data = df.to_dict(orient='records')

    logger.info('Clean records produced: %d', len(clean_data))
    return clean_data
