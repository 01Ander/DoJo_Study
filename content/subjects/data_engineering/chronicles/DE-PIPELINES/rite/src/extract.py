import json
import logging
from datetime import datetime, timezone
from pathlib import Path

import requests

from src.config import BRONZE_DIR, MARKET_TOKEN, MARKET_URL

logger = logging.getLogger(__name__)


def fetch_market(catalog_url: str = MARKET_URL, market_token: str = MARKET_TOKEN) -> dict:
    headers = {'Authorization': f"Bearer {market_token}"}

    response = requests.get(catalog_url, headers=headers)
    response.raise_for_status()

    payload = response.json()
    logger.info("Market responded with %d ingredients",
                len(payload.get("results", [])))

    return payload


def load_raw(payload: dict, target_dir: str = BRONZE_DIR) -> str:
    directory = Path(target_dir)
    directory.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")
    path = directory / f"{stamp}.json"

    with path.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False)

    logger.info('Raw payload stored at %s', path)

    return str(path)
