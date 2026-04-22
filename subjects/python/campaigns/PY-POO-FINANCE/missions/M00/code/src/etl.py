# M00

import csv
import json
import logging
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

ACCEPTED_CURRENCIES = {"USD", "EUR", "ARS", "COP", "CAD"}


class LogAnalyzer:
    """ Encapsulates the ETL pipeline for processing dirty log files.

    The LogAnalyzer takes raw CSV input, normalizes records, filters anomalies, aggregates metrics, and exports a structured JSON report.
    """

    def __init__(
        self,
        input_csv: str,
        output_json: str,
        log_path: str
    ) -> None:
        """Construct a LogAnalyzer instance with pipeline file paths.

        Args:
            input_csv: Path to the raw CSV file with dirty records.
            output_json: Destination path for the aggregated JSON report.
            log_path: Destination path for the errors/ignored records log.
        """
        self.input_csv = input_csv
        self.output_json = output_json
        self.log_path = log_path
        self._records: list[dict] = []
        self._valid_records: list[dict] = []
        self._report: dict = []

    def run(self) -> None:
        """Execute the full ETL pipeline sequentially.

        Orchestrates: load → process → aggregate → export.
        No arguments needed — all paths are stored as instance attributes.
        """
        self._load_logs()
        self._process_records()
        self._aggregate_transactions()
        self._export()

    def _load_logs(self) -> list[dict]:
        """Read the raw CSV and return a list of record dictionaries.

        Raises ValueError if the file cannot be found or is unreadable.
        """
        logs: list[dict[str, str]] = []
        try:
            with open(self.input_csv, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    logs.append(dict(row))
            self._records = logs
            return self._records
        except FileNotFoundError as e:
            raise ValueError(f"Cannot load file: {self.input_csv}") from e

    def _normalize_transaction_date(self, raw_date: str) -> str:
        """
        Args:
            raw_date: Date string from transaction record (various formats supported).

        Returns:
            Normalized date string in ISO-8601 format.

        Raises:
            ValueError: If the data string doesn't match any know format.
        """
        format_list = [
            "%m-%d-%Y",
            "%Y/%m/%d",
            "%d-%m-%Y",
            "%Y-%m-%d",
            "%d-%m-%Y %H:%M:%S",
            "%m-%d-%Y %H:%M:%S",
            "%Y/%m/%d %H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
            "%d/%m/%Y %H:%M:%S",
            "%d/%m/%Y %H:%M",
        ]

        for fmt in format_list:
            try:
                parsed = datetime.strptime(raw_date.strip(), fmt)
                data_parsed = parsed.strftime("%Y-%m-%d")
                return data_parsed
            except ValueError:
                continue

        raise ValueError(f"Unknown date format: '{self.input_csv}'")

    def _format_currency(self, raw_currency: str) -> float:
        """
        Args:
            raw_currency: Currency string format.

        Returns:
            Currency float format.

        Raises:
            ValueError: If the currency string doesn't march any know format.
        """

        cleaned = raw_currency.replace("$", "").replace(",", "").strip()
        if not cleaned:
            raise ValueError("Empty currency value")
        return float(cleaned)

    def _validate_data(self, raw_transactions: dict[str, str]) -> dict[str, Any]:
        """
        Validation and Normalized of date and currency.

        Args:
            A dicts raw.

        Return:
            A dicts with data validate.

        Raises:
            ValueError: If date and currency is no valid in function.
        """

        cleaned: dict[str, Any] = dict(raw_transactions)

        cleaned["timestamp"] = self._normalize_transaction_date(
            cleaned["timestamp"])
        cleaned["amount"] = self._format_currency(cleaned["amount"])
        if cleaned["amount"] <= 0:
            raise ValueError(f"Non-positive amount: '{cleaned['amount']}'")
        if cleaned["amount"] > 50000:
            raise ValueError(
                f"Suspiciously large amount: $'{cleaned['amount']}'")
        currency = cleaned.get("currency", "").strip().upper()
        if currency not in ACCEPTED_CURRENCIES:
            raise ValueError(f"Unsupported currency: '{currency}'")
        return cleaned

    def _aggregate_transactions(self) -> dict[str, dict[str, float]]:
        """
        Groups validated records by category and calculates Total, Count, and Mean.

        Args:
            records: List of validated transaction dicts. Each dict must contain
            "category" (str) and "amount" (float).

        Returns:
            A dict mapping each category to its aggregation stats (count, total, mean).

        Raises:
            KeyError: If a record is missing "category" or "amount".
        """

        groups = defaultdict(list)

        for record in self._valid_records:
            category = record["category"]
            amount = record["amount"]
            groups[category].append(amount)

        report = {}

        for category, amounts in groups.items():
            report[category] = {
                'count': len(amounts),
                'total': sum(amounts),
                'mean': sum(amounts) / len(amounts)
            }
        self._report = report

        return self._report

    def _process_records(self) -> list[dict[str, Any]]:
        """
        Supervises records through validation, logging failures without halting.

        Args:
            records: List of raw transaction dicts from load_transactions().
            log_path: File path for the rejected records logs.

        Returns:
            A list of validated records with normalized types.
        """

        valid_records = []

        with open(self.log_path, 'w', encoding='utf-8') as file:
            for record in self._records:
                try:
                    validated = self._validate_data(record)
                    valid_records.append(validated)
                except ValueError as e:
                    file.write(f'REJECTED: {record} | Reason: {e}\n')
        self._valid_records = valid_records
        return self._valid_records

    def _export(self) -> None:
        """
        Exports the aggregated report to a JSON file.

        Args:
          report: A dict from aggregate transactions.
          filepath: Destination path for the JSON file.

        Return:
          None
        """

        with open(self.output_json, 'w', encoding="utf-8") as file:
            json.dump(self._report, file, indent=2)
