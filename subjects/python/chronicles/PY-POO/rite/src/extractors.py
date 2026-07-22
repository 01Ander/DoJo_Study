from abc import ABC, abstractmethod
from src.exceptions import DataSourceNotFoundError
import csv
import os


class AbstractExtractor(ABC):

    @abstractmethod
    def extract(self, filepath: str) -> list[dict]:
        pass


class CSVExtractor(AbstractExtractor):

    def extract(self, filepath: str) -> list[dict]:

        if not os.path.exists(filepath):
            raise DataSourceNotFoundError(f"{filepath} not found")

        transactions: list[dict[str, str]] = []

        with open(filepath, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                transactions.append(dict(row))

        return transactions
