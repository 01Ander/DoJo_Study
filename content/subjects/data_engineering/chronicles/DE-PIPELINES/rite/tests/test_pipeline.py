import json
import re
from pathlib import Path
import pytest
import requests
import responses
import pandas as pd
from sqlalchemy import create_engine, text
from src.extract import fetch_market, load_raw
from src.transform import transform_market_catalog
from src.quality import validate_silver_market
from src.aggregation import aggregate_silver_market
from src.save_gold import save_gold_inventory
from src.pipeline import pipeline


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

    result = fetch_market(MARKET_URL, MARKET_TOKEN)

    assert "results" in result
    assert len(result["results"]) == 12
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
    silver_records = transform_market_catalog(str(bronze_file))
    assert list(silver_records[0].keys()) == ["name", "price", "stock"]


def test_removes_rows_with_null_values(bronze_file):
    silver_records = transform_market_catalog(str(bronze_file))
    assert len(silver_records) == 11


def test_normalizes_ingredient_names(bronze_file):
    silver_records = transform_market_catalog(str(bronze_file))
    assert silver_records[0]['name'] == 'eye of newt'
    assert silver_records[2]['name'] == 'dragon scale'


def test_casts_price_to_integer(bronze_file):
    silver_records = transform_market_catalog(str(bronze_file))
    assert silver_records[0]['price'] == 12


# --------- Fase 3 ------------


def test_returns_deduplicated_records_within_the_loss_limit(bronze_file):
    records = transform_market_catalog(str(bronze_file))
    silver_records = validate_silver_market(str(bronze_file), records)

    assert len(silver_records) == 9


def test_reconciliation_gate_blocks_loss_above_ten_percent(bronze_file):
    records = transform_market_catalog(str(bronze_file))
    with pytest.raises(AssertionError):
        validate_silver_market(str(bronze_file), records[:6])


def test_null_gate_blocks_records_with_null_values(bronze_file):
    records = transform_market_catalog(str(bronze_file))
    null_record = load_payload()["results"][-1]

    with pytest.raises(AssertionError):
        validate_silver_market(str(bronze_file), records + [null_record])


# --------- Fase 4 ------------


@pytest.fixture
def test_engine():
    db_engine = create_engine('sqlite:///:memory:')
    return db_engine


@pytest.fixture
def test_gold_df():
    return pd.DataFrame([
        {"name": "eye of newt", "total_stock": 55},
        {"name": "dragon scale", "total_stock": 10},
    ])


def test_aggregates_stock_by_ingredient(bronze_file):
    records = transform_market_catalog(str(bronze_file))
    silver_records = validate_silver_market(str(bronze_file), records)
    gold = aggregate_silver_market(silver_records)

    totals = {}
    for row in gold.to_dict("records"):
        totals[row["name"]] = row["total_stock"]
    assert totals["eye of newt"] == 55
    assert isinstance(gold, pd.DataFrame)
    assert len(gold) == 7


def test_saves_gold_into_clean_inventory_table(bronze_file, test_engine):
    records = transform_market_catalog(str(bronze_file))
    silver_records = validate_silver_market(str(bronze_file), records)
    gold = aggregate_silver_market(silver_records)
    save_gold_inventory(gold, test_engine)

    with test_engine.connect() as conn:
        result = conn.execute(text('SELECT * FROM clean_inventory')).fetchall()
    assert len(result) == 7
    totals = {}
    for row in result:
        totals[row[0]] = row[1]
    assert totals["eye of newt"] == 55


def test_appends_without_destroying_the_table(test_gold_df, test_engine):
    save_gold_inventory(test_gold_df, test_engine)
    save_gold_inventory(test_gold_df, test_engine)
    with test_engine.connect() as conn:
        result = conn.execute(text('SELECT * FROM clean_inventory')).fetchall()
        assert len(result) == 4


def test_does_not_store_the_pandas_index(test_gold_df, test_engine):
    save_gold_inventory(test_gold_df, test_engine)
    with test_engine.connect() as conn:
        result = conn.execute(text('SELECT * FROM clean_inventory'))
    assert list(result.keys()) == ['name', 'total_stock']


# --------- Fase 5 ------------

@responses.activate
def test_extract_task_retries_on_transient_failure():
    responses.add(responses.GET, MARKET_URL, json={
        "error": "market unavailable"}, status=500)
    responses.add(responses.GET, MARKET_URL, json={
        "error": "market unavailable"}, status=500)
    responses.add(responses.GET, MARKET_URL, json=load_payload(), status=200)

    result = fetch_market(MARKET_URL, MARKET_TOKEN)

    assert len(responses.calls) == 3
    assert len(result['results']) == 12


@responses.activate
def test_pipeline_loads_gold_into_the_database(tmp_path):
    responses.add(responses.GET, MARKET_URL, json=load_payload(), status=200)
    db_url = f"sqlite:///{tmp_path / 'guild.db'}"
    pipeline(db_url=db_url)
    new_engine = create_engine(db_url)
    with new_engine.connect() as conn:
        result = conn.execute(text('SELECT * FROM clean_inventory')).fetchall()
    assert len(result) == 7
    totals = {}
    for row in result:
        totals[row[0]] = row[1]
    assert totals["eye of newt"] == 55


@responses.activate
def test_pipeline_stops_when_the_quality_gate_fails(tmp_path):
    payload = load_payload()
    payload["results"][0]["stock"] = None
    responses.add(responses.GET, MARKET_URL, json=payload, status=200)
    db_url = f"sqlite:///{tmp_path / 'guild.db'}"

    with pytest.raises(AssertionError):
        pipeline(db_url=db_url, bronze_dir=str(tmp_path))
    assert not (tmp_path / "guild.db").exists()


def test_stages_are_prefect_tasks():
    assert fetch_market.retries == 3
    assert hasattr(transform_market_catalog, "name"), "Missing @task decorator"
    assert pipeline.name == "Dark_Market_Pipeline"
