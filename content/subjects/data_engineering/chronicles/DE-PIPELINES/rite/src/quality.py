import json
import logging
import pandas as pd
from prefect import task
from src.config import RESULT_KEY, CRITICAL_COLUMNS


logger = logging.getLogger(__name__)


@task
def validate_silver_market(bronze_path: str, records: list) -> list[dict]:
    with open(bronze_path, encoding='utf-8') as fh:
        payload = json.load(fh)

    logger.info('Silver candidates received: %d', len(records))

    df = pd.DataFrame(records)

    initial_count = len(payload[RESULT_KEY])
    final_count = len(df)
    loss_rate = (initial_count - final_count) / initial_count

    logger.info('Reconciliation metrics: %d in, %d out, loss rate %.2f%%',
                initial_count, final_count, loss_rate * 100)
    assert loss_rate <= 0.1, f"Data quality failed: Loss rate is {loss_rate*100}%"

    silver_data = df.drop_duplicates()

    for item in CRITICAL_COLUMNS:
        assert silver_data[item].notnull().all(
        ), f"Data quality failed: null values found in critical column: {item}"

    silver_data_dict = silver_data.to_dict(orient='records')

    logger.info('Silver records validated: %d', len(silver_data_dict))
    return silver_data_dict
