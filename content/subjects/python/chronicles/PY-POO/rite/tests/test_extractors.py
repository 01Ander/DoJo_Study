import pytest
from src.extractors import AbstractExtractor, CSVExtractor
from src.exceptions import DataSourceNotFoundError


def test_cannot_instantiate_abstract_class():
    with pytest.raises(TypeError):
        extractor = AbstractExtractor()


@pytest.fixture
def sample_csv(tmp_path):
    filepath = tmp_path / "test_data.csv"
    filepath.write_text(
        "id,date,amount,currency,type,description,category\n"
        "1,2024-01-15,5000.00,USD,Income,Mensual,Salary\n"
        "2,2024-01-20,120.50,USD,Expense,Supermercado,Groceries\n"
    )
    return filepath


def test_csv_extractor_returns_data(sample_csv):
    result = CSVExtractor()
    data_result = result.extract(str(sample_csv))
    assert isinstance(data_result, list)
    assert data_result[0]["id"] == "1"
    assert data_result[0]["amount"] == "5000.00"
    assert data_result[1]["type"] == "Expense"
    assert data_result[1]["category"] == "Groceries"


def test_data_source_not_found_error():
    with pytest.raises(DataSourceNotFoundError):
        result = CSVExtractor()
        data_result = result.extract("wrong_path.csv")
