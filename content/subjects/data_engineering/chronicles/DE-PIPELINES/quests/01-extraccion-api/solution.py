import requests

def extract_market_catalog(api_url: str, token: str) -> list:
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    return data.get("results", [])

# SOLUTION TESTS (How test_01_api.py should look like)
'''
import pytest
import requests
import responses

@responses.activate
def test_extract_catalog_success():
    token = "magic_token_123"
    url = "https://api.blackmarket.fake/items"
    responses.add(responses.GET, url, json={"results": [{"name": "Eye of Newt"}]}, status=200)
    
    result = extract_market_catalog(url, token)
    
    assert len(result) == 1
    assert result[0]["name"] == "Eye of Newt"

@responses.activate
def test_extract_catalog_no_results():
    url = "https://api.blackmarket.fake/empty"
    responses.add(responses.GET, url, json={}, status=200)

    result = extract_market_catalog(url, "token")
    assert result == []

@responses.activate
def test_extract_catalog_auth_failure():
    url = "https://api.blackmarket.fake/items"
    responses.add(responses.GET, url, json={"error": "Unauthorized"}, status=401)

    with pytest.raises(requests.exceptions.HTTPError):
        extract_market_catalog(url, "invalid_token")
'''
