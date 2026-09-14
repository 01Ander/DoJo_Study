import pandas as pd

def process_silver_inventory(bronze_data: list) -> list:
    df = pd.DataFrame(bronze_data)
    df = df.dropna()
    df['ingredient'] = df['ingredient'].str.strip().str.lower()
    df['amount'] = df['amount'].astype(int)
    return df.to_dict(orient='records')

# SOLUTION TESTS
'''
import pytest

@pytest.fixture
def dirty_bronze_data():
    return [
        {"ingredient": "  Fairy DUST  ", "amount": "15"},
        {"ingredient": None, "amount": 10},
        {"ingredient": "Dragon Blood", "amount": None},
        {"ingredient": "Mandrake ROOT", "amount": "5"},
    ]

def test_process_inventory_cleans_and_casts(dirty_bronze_data):
    silver_data = process_silver_inventory(dirty_bronze_data)
    
    assert len(silver_data) == 2
    
    assert silver_data[0]["ingredient"] == "fairy dust"
    assert silver_data[0]["amount"] == 15
    assert isinstance(silver_data[0]["amount"], int)

    assert silver_data[1]["ingredient"] == "mandrake root"
    assert silver_data[1]["amount"] == 5
    assert isinstance(silver_data[1]["amount"], int)
'''
