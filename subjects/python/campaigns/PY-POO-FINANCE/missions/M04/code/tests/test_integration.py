import json
import pytest

from src.abstract_loader import AbstractLoader
from src.json_loader import JSONLoader
from src.pipeline import FinancialPipeline
from src.abstract_extractor import AbstractExtractor
from src.analytics_engine import AnalyticsEngine


class TestAbstractorLoader(AbstractLoader):
    pass


def test_abstract_loader_enforces_signatures():
    with pytest.raises(TypeError):
        TestAbstractorLoader()


def test_json_loader_writes_json(tmp_path):
    my_loader = JSONLoader()
    save_data = {"motors": "active", "fuel": "full"}
    output_path = str(tmp_path / "info.json")

    my_loader.load_data(save_data, filename=output_path)

    with open(output_path, 'r') as f:
        real_content = json.load(f)

    assert real_content == save_data


def test_pipeline_validates_extractor_type():
    with pytest.raises(TypeError):
        FinancialPipeline("wrong_thing", AnalyticsEngine(), JSONLoader())
