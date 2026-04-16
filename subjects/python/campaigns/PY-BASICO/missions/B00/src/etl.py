# ETL pipeline for financial transaction data resilience.

from datetime import datetime
from collections import defaultdict
from typing import Any
import csv
import json


def normalize_transaction_date(raw_date: str) -> str:
    """
    Args:
      raw_date: Date string in format 'MM-DD-YYYY' or 'YYYY/MM/DD'

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
            return parsed.strftime("%Y-%m-%d")
        except ValueError:
            continue

    raise ValueError(f"Unknown date format: '{raw_date}'")


def clean_currency(raw_currency: str) -> float:
    """
    Args:
      raw_currency: Currency string format.

    Returns:
      Currency float format.

    Raises:
      ValueError: If the currency string doesn't march any know format.
    """

    cleaned = raw_currency.replace("$", "").replace(",", "").strip()
    return float(cleaned)


def aggregate_transactions(records: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
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

    for record in records:
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

    return report


def load_transactions(filepath: str) -> list[dict[str, str]]:
    """
    Reads a CSV transactions and returns a list of dictionaries.

    Args:
      filepath: Path to the CSV file.

    Returns:
      A list of dicts, one per row.

    Raises:
      FileNotFoundError: If the file does not exist.
    """
    transactions: list[dict[str, str]] = []

    with open(filepath, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            transactions.append(dict(row))

    return transactions


ACCEPTED_CURRENCIES = {"USD", "EUR", "ARS", "COP", "CAD"}


def data_validation(raw_transactions: dict[str, str]) -> dict[str, Any]:
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

    cleaned["timestamp"] = normalize_transaction_date(cleaned["timestamp"])
    cleaned["amount"] = clean_currency(cleaned["amount"])
    if cleaned["amount"] <= 0:
        raise ValueError(f"Non-positive amount: '{cleaned['amount']}'")
    if cleaned["amount"] > 50000:
        raise ValueError(
            f"Suspiciously large amount: $'{cleaned['amount']}'")
    currency = cleaned.get("currency", "").strip().upper()
    if currency not in ACCEPTED_CURRENCIES:
        raise ValueError(f"Unsupported currency: '{currency}'")
    return cleaned


def process_records(records: list[dict[str, str]], log_path: str) -> list[dict[str, Any]]:
    """
    Supervises records through validation, logging failures without halting.

    Args:
      records: List of raw transaction dicts from load_transactions().
      log_path: File path for the rejected records logs.

    Returns:
      A list of validated records with normalized types.
    """

    valid_records = []
    with open(log_path, 'w', encoding="utf-8") as file:
        for record in records:
            try:
                validated = data_validation(record)
                valid_records.append(validated)
            except ValueError as e:
                file.write(f'REJECTED: {record} | Reason: {e}\n')
    return valid_records


def export_report(report: dict[str, dict[str, float]], filepath: str) -> None:
    """
    Exports the aggregated report to a JSON file.

    Args:
      report: A dict from aggregate transactions.
      filepath: Destination path for the JSON file.

    Return:
      None
    """
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)


def run_pipeline(input_csv: str, output_json: str, log_path: str) -> None:
    """
    Main function, read and load CSV data, validated records, generation report and export report.

    Args:
      input_csv: CSV original with raw transactions.
      output_json: JSON with report.
      log_path: File path for the rejected records logs.

    Returns:
      None. This function has side effects: writes output JSON and log files.
    """

    raw_transactions = load_transactions(input_csv)
    valid_records = process_records(raw_transactions, log_path)
    report = aggregate_transactions(valid_records)
    export_report(report, output_json)


if __name__ == "__main__":
    run_pipeline(
        input_csv="data/transactions_raw.csv",
        output_json="data/summary_report.json",
        log_path="data/ignored_records.log",
    )
