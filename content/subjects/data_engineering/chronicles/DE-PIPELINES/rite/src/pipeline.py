import logging
from prefect import flow
from sqlalchemy import create_engine
from src.extract import fetch_market, load_raw
from src.transform import transform_market_catalog
from src.quality import validate_silver_market
from src.aggregation import aggregate_silver_market
from src.save_gold import save_gold_inventory

from src.config import DB_URL, BRONZE_DIR, MARKET_TOKEN, MARKET_URL


@flow(name="Dark_Market_Pipeline")
def pipeline(db_url=DB_URL, bronze_dir=BRONZE_DIR):

    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(levelname)s: %(message)s")

    db_engine = create_engine(db_url)
    payload = fetch_market(MARKET_URL, MARKET_TOKEN)
    bronze_path = load_raw(payload, bronze_dir)
    records_transform = transform_market_catalog(bronze_path)
    silver_records = validate_silver_market(
        str(bronze_path), records_transform)
    aggregation_silver = aggregate_silver_market(silver_records)
    save_gold_inventory(aggregation_silver, db_engine)


if __name__ == "__main__":
    pipeline()
