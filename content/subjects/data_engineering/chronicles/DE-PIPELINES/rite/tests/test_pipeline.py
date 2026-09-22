import json
import re
from pathlib import Path
import pytest
import requests
import responses
from src.extract import fetch_market, load_raw
from src.transform import build_silver_market

FIXTURE = Path(__file__).parent / "fixtures" / "market_catalog.json"
MARKET_URL = "https://api.dark_market.fake/items"
MARKET_TOKEN = "market_token_ara"

# --------- Fase 1 ------------


def load_payload():
    with FIXTURE.open(encoding="utf-8") as fh:
        return json.load(fh)


@responses.activate
def test_fetch_returns_whole_body():
    responses.add(responses.GET, MARKET_URL, json=load_payload(), status=200)

    # fetch_market sera la funcion que haga la extraccion, aun no importada pero se menciona para cuando se haga en src
    result = fetch_market(MARKET_URL, MARKET_TOKEN)

    assert "results" in result
    assert len(result["results"]) == 10
    assert result["results"][0]["name"] == " Eye of Newt "
    assert result["results"][3]["price"] == "150"
    assert result["results"][8]["stock"] == "2"


@responses.activate
def test_token_travels_in_authorization_header():
    responses.add(responses.GET, MARKET_URL, json=load_payload(), status=200)

    fetch_market(MARKET_URL, MARKET_TOKEN)

    sent = responses.calls[0].request.headers['Authorization']
    assert sent == f"Bearer {MARKET_TOKEN}"


@responses.activate
def test_unauthorized_raises():
    responses.add(responses.GET, MARKET_URL, json={
                  "error": "nope"}, status=401)

    with pytest.raises(requests.exceptions.HTTPError):
        fetch_market(MARKET_URL, MARKET_TOKEN)


def test_store_raw_writes_file_and_returns_path(tmp_path):
    payload = load_payload()

    path = load_raw(payload, str(tmp_path))

    written = Path(path)
    assert written.exists()
    assert written.parent == tmp_path
    assert re.fullmatch(r"\d{8}T\d{6}\d{6}\.json", written.name)
    assert json.loads(written.read_text(encoding="utf-8")) == payload


def test_two_runs_leave_two_files_in_chronological_order(tmp_path):
    payload = load_payload()

    first = load_raw(payload, str(tmp_path))
    second = load_raw(payload, str(tmp_path))

    first_name = Path(first).name
    second_name = Path(second).name

    assert first_name != second_name
    assert second_name > first_name
    assert len(list(tmp_path.glob("*.json"))) == 2

# --------- Fase 2 ------------


@pytest.fixture
def bronze_file(tmp_path):
    filepath = tmp_path / "bronze.json"
    filepath.write_text(json.dumps(load_payload()), encoding="utf-8")
    return filepath


def test_unwraps_bronze_payload_into_ingredient_columns(bronze_file):
    silver_records = build_silver_market(str(bronze_file))
    assert list(silver_records[0].keys()) == ["name", "price", "stock"]


def test_removes_rows_with_null_values(bronze_file):
    silver_records = build_silver_market(str(bronze_file))
    assert len(silver_records) == 9


def test_normalizes_ingredient_names(bronze_file):
    silver_records = build_silver_market(str(bronze_file))
    assert silver_records[0]['name'] == 'eye of newt'
    assert silver_records[2]['name'] == 'dragon scale'


def test_casts_price_to_integer(bronze_file):
    silver_records = build_silver_market(str(bronze_file))
    assert silver_records[0]['price'] == 12
