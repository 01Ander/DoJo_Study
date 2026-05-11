# ETL pipeline for a sprawling application generates large web server logs.

import csv
import json
from datetime import datetime
from collections import defaultdict
from typing import Any


def normalize_logs_date(raw_date: str) -> str:
    """
    Args:
        raw_date: Date string in format 'YYYY-MM-DDTH:M:S.f' or 'DD-MM-YYYY H:M:S'

    Returns:
        Normalized date string in ISO-8601 format 'YYYY-MM-DDTH:M:S'.

    Raises:
        ValueError: If the data string doesn't match any know format.
    """
    format_list = [
        "%Y-%m-%dT%H:%M:%S.%f",
        "%d-%m-%Y %H:%M:%S"
    ]
    for fmt in format_list:
        try:
            parsed = datetime.strptime(raw_date.strip(), fmt)
            return parsed.strftime("%Y-%m-%dT%H:%M:%S")
        except ValueError:
            continue
    raise ValueError(f"Unknown date format: '{raw_date}'")


def parse_log_line(line: str) -> dict[str, Any]:
    """
    Args:
        Attempt to parse a single log line.

    Returns:
        dict with keys: timestamp, endpoint, status_code, response_time_ms

    Raises:
        ValueError: If the line cannot be parsed.
    """

    fields = line.split(",")
    if len(fields) < 4:
        raise ValueError(f"Error log: '{fields}'")

    status_code = _safe_cast_int(fields[2], "status_code")
    response_time_ms = _safe_cast_int(fields[3], "response_time_ms")

    validate_log = {
        'timestamp': normalize_logs_date(fields[0]),
        'endpoint': fields[1],
        'status_code': status_code,
        'response_time_ms': response_time_ms
    }

    return validate_log


def _safe_cast_int(value: str, field_name: str) -> int:
    """Private function of validation values"""
    try:
        return int(value)
    except ValueError as e:
        raise ValueError(f"Invalid {field_name} '{value}': {e}")


def aggregation_logs(parsed_records: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    """
    Groups validated records by status HTTP.
    Args:
        parsed_records: List of validated logs dicts.
    Returns:
        A dict mapping each category to its aggregation stats (total).
    Raises:
        KeyError: If a record is missing in categories.
    """

    groups = defaultdict(list)

    for record in parsed_records:
        endpoint = record["endpoint"]
        status_code = record["status_code"]
        groups[status_code].append(endpoint)

    report = {}

    for status_code, endpoint in groups.items():
        report[status_code] = {
            'total': len(endpoint)
        }

    return report


def load_logs(filepath: str) -> list[str]:
    """
        Reads a CSV logs and returns a list.

    Args:
        filepath: Path to the CSV file.

    Returns:
        A list of logs.

    Raises:
        FileNotFoundError: If the file does not exist.
    """

    lines: list[str] = []

    with open(filepath, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            lines.append(",".join(row))

    return lines


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


def process_logs(lines: list[str], log_path: str) -> list[dict[str, Any]]:
    """
        Supervises records through validation, logging failures without halting.

    Args:
        records: List of strings dicts from load_logs().
        log_path: File path for the rejected records logs.

    Returns:
        A list of validated records with normalized types.
    """

    valid_logs = []
    with open(log_path, "w", encoding="utf-8") as file:
        for line in lines:
            try:
                validated = parse_log_line(line)
                valid_logs.append(validated)
            except ValueError as e:
                file.write(f'REJECTED: {line} | Reason: {e}\n')
    return valid_logs


def run_pipeline(input_csv: str, output_json: str, log_path: str) -> None:
    """
    Main function, read and load CSV data, validated logs, generation report and export report.

    Args:
        input_csv: CSV original with raw logs.
        output_json: JSON with report.
        log_path: File path for the rejected logs.

    Returns:
        None. This function has side effects: writes output JSON and log files.
    """

    raw_logs = load_logs(input_csv)
    valid_logs = process_logs(raw_logs, log_path)
    report = aggregation_logs(valid_logs)
    export_report(report, output_json)


if __name__ == "__main__":
    run_pipeline(
        input_csv="mock_data/server_logs.csv",
        output_json="mock_data/summary_report.json",
        log_path="mock_data/ignored_records.log",
    )
