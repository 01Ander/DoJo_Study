import json
import csv
import pytest
from pathlib import Path
from src.pipeline import FinancialPipeline
from src.csv_extractor import CSVExtractor
from src.analytics_engine import AnalyticsEngine
from src.json_loader import JSONLoader


def test_full_pipeline_e2e(tmp_path):
    data_csv = tmp_path / "data.csv"
    data_csv.write_text(
        "id,date,amount,currency,type,description,category\n"
        "1,2024-01-15,5000.00,USD,Income,Mensual,Salary\n"
        "2,2024-01-20,120.50,USD,Expense,Supermercado,Groceries\n"
        "3,2024-01-25,45.00,USD,Expense,Streaming,Entertainment\n"
    )

    extractor = CSVExtractor(data_csv)
    engine = AnalyticsEngine()
    loader_json = JSONLoader()

    pipeline = FinancialPipeline(extractor, engine, loader_json)

    output_path = str(tmp_path / "info.json")
    result = pipeline.run(output_path)

    assert result["gross_income"] == 5000.0
    assert result["total_expenses"] == pytest.approx(165.50)
    assert result["net_balance"] == pytest.approx(4834.50)

    with open(output_path, 'r') as f:
        saved = json.load(f)

    assert saved == result


def test_pipeline_processor_rejects_missing_file(tmp_path):
    reader = CSVExtractor("wrong_path.csv")
    engine = AnalyticsEngine()
    loader_json = JSONLoader()

    pipeline = FinancialPipeline(reader, engine, loader_json)

    with pytest.raises(FileNotFoundError):
        pipeline.run(output_json=str(tmp_path / "result.json"))


def test_pipeline_validates_extractor_type():
    with pytest.raises(TypeError):
        FinancialPipeline("wrong_thing", AnalyticsEngine(), JSONLoader())


def test_pipeline_validates_engine_type():
    extractor = CSVExtractor("dummy.csv")
    with pytest.raises(TypeError):
        FinancialPipeline(extractor, "wrong_thing", JSONLoader())


def test_pipeline_validates_loader_type():
    extractor = CSVExtractor("dummy.csv")
    with pytest.raises(TypeError):
        FinancialPipeline(extractor, AnalyticsEngine(), "wrong_thing")
