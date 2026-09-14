import pandas as pd

def load_gold_inventory(df: pd.DataFrame, engine):
    df.to_sql(
        name='potion_stock',
        con=engine,
        if_exists='append',
        index=False
    )

# SOLUTION TESTS
'''
import pytest
from sqlalchemy import create_engine, text

@pytest.fixture
def test_engine():
    return create_engine('sqlite:///:memory:')

@pytest.fixture
def test_gold_df():
    data = [
        {"potion": "Love Potion", "total_amount": 42},
        {"potion": "Felix Felicis", "total_amount": 1},
    ]
    return pd.DataFrame(data)

def test_load_inventory_successfully(test_gold_df, test_engine):
    load_gold_inventory(test_gold_df, test_engine)
    
    with test_engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM potion_stock")).fetchall()
        
        assert len(result) == 2
        assert result[0][0] == "Love Potion"
        assert result[0][1] == 42
'''
