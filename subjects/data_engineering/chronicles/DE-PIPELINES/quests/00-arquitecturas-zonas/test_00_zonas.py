import pytest

# ==========================================
# QUEST 00: Data Architectures and Zones
# ==========================================
# Alchemist Guild: Storage Zones
# ==========================================

# ------------------------------------------
# Business Logic (Implement this!)
# ------------------------------------------

def load_to_bronze(raw_api_response: list) -> list:
    """
    BRONZE ZONE (Immutable)
    Rule: Return exactly the same raw data received. Do not alter ANYTHING.
    """
    pass

def process_to_silver(bronze_data: list) -> list:
    """
    SILVER ZONE (Cleaning)
    Rule: 
    1. Remove any dictionary that does not have the key 'ingredient'.
    2. Convert the 'ingredient' value to lowercase and strip whitespace.
    3. If 'amount' is None, assume it is 0.
    """
    pass

def aggregate_to_gold(silver_data: list) -> dict:
    """
    GOLD ZONE (Aggregation)
    Rule: Return a dictionary where keys are ingredient names, 
    and values are the total sum of their amounts.
    """
    pass


# ------------------------------------------
# Scaffolding: Level 1 (Read Tests)
# Run: pytest test_00_zonas.py
# ------------------------------------------

@pytest.fixture
def raw_data_payload():
    return [
        {"ingredient": " Healing Root ", "amount": 5},
        {"trash": "stone", "amount": 10},
        {"ingredient": "Fairy Dust", "amount": None},
        {"ingredient": "healing root", "amount": 2},
    ]

def test_bronze_zone_is_immutable(raw_data_payload):
    bronze = load_to_bronze(raw_data_payload)
    assert bronze == raw_data_payload
    assert len(bronze) == 4

def test_silver_zone_cleans_data(raw_data_payload):
    bronze = load_to_bronze(raw_data_payload)
    silver = process_to_silver(bronze)
    
    # Must have filtered the 'trash'
    assert len(silver) == 3
    
    # Must standardize text and handle Nones
    assert silver[0] == {"ingredient": "healing root", "amount": 5}
    assert silver[1] == {"ingredient": "fairy dust", "amount": 0}

def test_gold_zone_aggregates_results(raw_data_payload):
    bronze = load_to_bronze(raw_data_payload)
    silver = process_to_silver(bronze)
    gold = aggregate_to_gold(silver)
    
    # Healing root sums 5 + 2 = 7
    assert gold["healing root"] == 7
    assert gold["fairy dust"] == 0
