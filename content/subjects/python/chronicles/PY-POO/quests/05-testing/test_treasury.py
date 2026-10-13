from pathlib import Path
import pytest
from treasury import TreasuryReportReader, GoldLedger


def test_reader_parses_gold_file_with_tmp_path(tmp_path: Path):
    # 1. Arrange: crear archivo en directorio temporal aislado
    csv_file = tmp_path / "records.csv"
    csv_file.write_text("gold,silver\n100.25,50.00\n200.50,10.00\n", encoding="utf-8")

    # 2. Act
    reader = TreasuryReportReader()
    total = reader.parse_total_gold(str(csv_file))

    # 3. Assert con approx
    assert total == pytest.approx(300.75)


def test_ledger_avoids_floating_point_imprecision():
    # Arrange & Act
    ledger = GoldLedger()
    result = ledger.sum_micro_transactions([0.1, 0.2, 0.3])

    # Assert
    assert result == pytest.approx(0.6)
