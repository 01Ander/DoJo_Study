import pytest
import pandas as pd
from sqlalchemy import create_engine, text

# ==========================================
# QUEST 04: Database Loading
# ==========================================
# The Teleportation Portal
# ==========================================

# ------------------------------------------
# Scaffolding: Level 5 (From Zero)
# Run: pytest test_04_carga.py
# ------------------------------------------

# 🎯 YOUR TURN:
# 1. Write the load_gold_inventory function.
# 2. Write the fixtures and test functions to validate it.


def load_gold_inventory(df: pd.DataFrame, engine):
    df.to_sql(
        name='potion_stock',
        con=engine,
        if_exists='append',
        index=False
    )


@pytest.fixture
def test_engine():
    db_engine = create_engine('sqlite:///:memory:')
    return db_engine


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
        result = conn.execute(
            text('SELECT * FROM potion_stock')).fetchall()
    assert len(result) == 2
    assert result[0][0] == 'Love Potion'
    assert result[1][1] == 1
