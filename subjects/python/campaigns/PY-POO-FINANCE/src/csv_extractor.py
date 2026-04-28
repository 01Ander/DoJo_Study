import csv
from typing import Any, Dict, List
from src.abstract_extractor import AbstractExtractor


class CSVExtractor(AbstractExtractor):
    """Concrete extractor for CSV file."""

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def extract_data(self) -> List[Dict[str, Any]]:
        transactions: List[Dict[str, str]] = []
        with open(self.file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                transactions.append(row)

        return transactions
