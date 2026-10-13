from pathlib import Path


class TreasuryReportReader:
    def parse_total_gold(self, filepath: str) -> float:
        total = 0.0
        with open(filepath, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line and not line.startswith("gold"):
                    parts = line.split(",")
                    total += float(parts[0])
        return total


class GoldLedger:
    def sum_micro_transactions(self, amounts: list[float]) -> float:
        return sum(amounts)
