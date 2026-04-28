import pytest


from src.abstract_extractor import AbstractExtractor
from src.csv_extractor import CSVExtractor


# Test Case 1: Instantiating `AbstractExtractor` directly raises a `TypeError` (enforcing abstract behavior).

def test_abstract_extractor_cannot_be_instantiated():
    with pytest.raises(TypeError):
        AbstractExtractor()

# Test Case 2: A poorly defined concrete class missing the `extract_data` implementation throws a `TypeError` upon instantiation.


def test_incomplete_subclass_raises_type_error():
    class BrokenExtractor(AbstractExtractor):
        pass

    with pytest.raises(TypeError):
        BrokenExtractor()


# Test Case 3: `CSVExtractor.extract_data()` correctly returns a structurally valid `List[dict]` given a valid mock CSV file.

def test_csv_extractor_returns_list_of_dicts(tmp_path):
    csv_file = tmp_path / "transactions.csv"
    csv_file.write_text(
        "id,fecha,monto\n1,2024-01-10,50.0\n2,2024-01-11,75.5\n")

    extractor = CSVExtractor(csv_file)

    result = extractor.extract_data()

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["id"] == "1"
    assert result[0]["fecha"] == "2024-01-10"
