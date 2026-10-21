"""
Suite de Pruebas Automatizadas — Quest 01-03: Extractor Desacoplado CSV y JSON
"""

import json
import pytest

from data_extractors import (
    AbstractDataExtractor,
    CSVDataExtractor,
    JSONDataExtractor,
)


def test_abstract_extractor_cannot_be_instantiated():
    """Verifica que AbstractDataExtractor sea una clase abstracta pura."""
    with pytest.raises(TypeError):
        AbstractDataExtractor()


def test_csv_extractor_reads_rows_as_dicts(tmp_path):
    """Verifica que CSVDataExtractor lea un archivo CSV y devuelva una lista de diccionarios."""
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text("item,price\nKeyboard,75.0\nMouse,25.0\n", encoding="utf-8")

    extractor = CSVDataExtractor()
    records = extractor.extract(str(csv_file))

    assert isinstance(records, list)
    assert len(records) == 2
    assert records[0] == {"item": "Keyboard", "price": "75.0"}
    assert records[1] == {"item": "Mouse", "price": "25.0"}


def test_json_extractor_reads_array_and_single_object(tmp_path):
    """Verifica que JSONDataExtractor parsee tanto listas JSON como objetos individuales."""
    extractor = JSONDataExtractor()

    # Caso 1: Array JSON
    array_file = tmp_path / "array.json"
    array_file.write_text(json.dumps([{"code": "A1"}, {"code": "B2"}]), encoding="utf-8")
    records_array = extractor.extract(str(array_file))
    assert isinstance(records_array, list)
    assert len(records_array) == 2
    assert records_array[0]["code"] == "A1"

    # Caso 2: Objeto JSON único
    single_file = tmp_path / "single.json"
    single_file.write_text(json.dumps({"code": "C3"}), encoding="utf-8")
    records_single = extractor.extract(str(single_file))
    assert isinstance(records_single, list)
    assert len(records_single) == 1
    assert records_single[0]["code"] == "C3"


def test_polymorphic_extraction_contract(tmp_path):
    """Verifica que ambos extractores hereden de la clase base y compartan el mismo contrato."""
    csv_ext = CSVDataExtractor()
    json_ext = JSONDataExtractor()

    assert isinstance(csv_ext, AbstractDataExtractor)
    assert isinstance(json_ext, AbstractDataExtractor)

    def load_dataset(extractor: AbstractDataExtractor, path: str):
        return extractor.extract(path)

    json_file = tmp_path / "test.json"
    json_file.write_text('[{"status": "ok"}]', encoding="utf-8")

    result = load_dataset(json_ext, str(json_file))
    assert result == [{"status": "ok"}]
