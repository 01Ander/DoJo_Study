import pandas as pd
import json
from src.config import RESULT_KEY


def build_silver_market(path: str) -> list[dict]:
    with open(path, encoding='utf-8') as fh:
        payload = json.load(fh)

    df = pd.DataFrame(payload[RESULT_KEY])
    df = df.dropna()
    df['name'] = df['name'].str.strip().str.lower()
    df['price'] = df['price'].astype(int)
    clean_data = df.to_dict(orient='records')
    return clean_data
