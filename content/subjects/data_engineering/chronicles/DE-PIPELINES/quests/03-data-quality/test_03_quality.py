import pytest
import pandas as pd

# ==========================================
# QUEST 03: Data Quality (DQ)
# ==========================================
# The Vault Guard
# ==========================================

def certify_inventory_quality(df_inventory: pd.DataFrame) -> pd.DataFrame:
    """
    Mission:
    1. Remove duplicate rows based on 'potion_code' (drop_duplicates).
    2. Apply a Quality Gate (assert): Ensure NO null values exist in 'toxicity_level'.
       If any exist, raise AssertionError.
    3. Return processed DataFrame.
    """
    pass

# ------------------------------------------
# Scaffolding: Level 4 (Write from Description)
# Run: pytest test_03_quality.py
# ------------------------------------------

@pytest.fixture
def dirty_inventory():
    data = [
        {"potion_code": "P-001", "toxicity_level": 0.5},
        {"potion_code": "P-002", "toxicity_level": 0.0},
        {"potion_code": "P-001", "toxicity_level": 0.5}, # Duplicate!
        {"potion_code": "P-003", "toxicity_level": 0.9},
    ]
    return pd.DataFrame(data)

@pytest.fixture
def invalid_inventory():
    data = [
        {"potion_code": "P-004", "toxicity_level": 0.1},
        {"potion_code": "P-005", "toxicity_level": None}, # Invalid Null!
    ]
    return pd.DataFrame(data)

def test_certify_removes_duplicates(dirty_inventory):
    # Write your test here based on the Quest instructions
    pass

def test_certify_fails_on_nulls(invalid_inventory):
    # Write your test here based on the Quest instructions
    pass
