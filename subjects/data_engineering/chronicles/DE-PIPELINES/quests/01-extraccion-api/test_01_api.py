import pytest
import requests
import responses

# ==========================================
# QUEST 01: Automated Extraction
# ==========================================
# The Black Market Messenger
# ==========================================

def extract_market_catalog(api_url: str, token: str) -> list:
    """
    Mission:
    1. Use 'requests' to make a GET request to api_url.
    2. Send the token in the 'Authorization' header with format 'Bearer <token>'.
    3. If successful (use raise_for_status), return the list under the 'results' key.
    4. If the 'results' key doesn't exist, return an empty list.
    """
    pass


# ------------------------------------------
# Scaffolding: Level 2 (Complete the Asserts)
# Run: pytest test_01_api.py
# ------------------------------------------

@responses.activate
def test_extract_catalog_success():
    # Setup the mock response
    token = "magic_token_123"
    url = "https://api.blackmarket.fake/items"
    
    responses.add(
        responses.GET,
        url,
        json={"results": [{"name": "Eye of Newt"}]},
        status=200
    )
    
    result = extract_market_catalog(url, token)
    
    # 🎯 FILL IN THE ASSERTS
    # Verify that the result length is 1
    assert False, "Replace this with assert len(result) == 1"
    
    # Verify that the first item's name is 'Eye of Newt'
    assert False, "Replace this with the correct assert"

@responses.activate
def test_extract_catalog_no_results():
    url = "https://api.blackmarket.fake/empty"
    responses.add(responses.GET, url, json={}, status=200)

    result = extract_market_catalog(url, "token")
    
    # 🎯 FILL IN THE ASSERTS
    # Verify that the result is an empty list
    assert False, "Replace this with the correct assert"

@responses.activate
def test_extract_catalog_auth_failure():
    url = "https://api.blackmarket.fake/items"
    responses.add(responses.GET, url, json={"error": "Unauthorized"}, status=401)

    # 🎯 FILL IN THE ASSERTS
    # Use a context manager to expect an HTTPError
    assert False, "Replace this with: with pytest.raises(requests.exceptions.HTTPError):"
    # extract_market_catalog(url, "invalid_token")
