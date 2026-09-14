import pytest
import pandas as pd

# ==========================================
# QUEST 02: Pandas Manipulation
# ==========================================
# The Alchemist Ledger
# ==========================================

def process_silver_inventory(bronze_data: list) -> list:
    """
    Mission:
    1. Convert 'bronze_data' list to pd.DataFrame.
    2. Drop ALL rows containing any null values (dropna).
    3. Ensure 'ingredient' column is lowercase and stripped of whitespaces.
    4. Cast 'amount' column to int.
    5. Return the clean data as a list of dicts (using to_dict(orient='records')).
    """
    pass

# ------------------------------------------
# Scaffolding: Level 3 (GIVEN/WHEN/THEN)
# Run: pytest test_02_pandas.py
# ------------------------------------------

@pytest.fixture
def dirty_bronze_data():
    return [
        {"ingredient": "  Fairy DUST  ", "amount": "15"},
        {"ingredient": None, "amount": 10},
        {"ingredient": "Dragon Blood", "amount": None},
        {"ingredient": "Mandrake ROOT", "amount": "5"},
    ]

def test_process_inventory_cleans_and_casts(dirty_bronze_data):
    # GIVEN dirty_bronze_data fixture
    
    # WHEN calling process_silver_inventory
    # silver_data = ...
    
    # THEN assert length is exactly 2 (nulls removed)
    
    # THEN assert first row's ingredient is "fairy dust"
    
    # THEN assert first row's amount is exactly 15 and is an integer
    
    # THEN assert second row's ingredient is "mandrake root"
    
    # THEN assert second row's amount is exactly 5 and is an integer
    pass
