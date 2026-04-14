#!/usr/bin/env python3
"""DoJo Journal Log Script — Writes timestamped entries to mission journal."""

import os
import sys
from datetime import datetime
from pathlib import Path


def find_dojo_root() -> Path:
    """Find the DoJo_Study root directory."""
    candidates = [
        Path.home() / "Documents" / "DoJo" / "DoJo_Study",
        Path.cwd(),
    ]
    for candidate in candidates:
        if (candidate / "subjects").exists():
            return candidate
    raise FileNotFoundError("Could not find DoJo_Study root directory")


def log_entry(campaign: str, mission: str, message: str) -> None:
    """Write a timestamped entry to the mission's journal.md."""
    root = find_dojo_root()
    mission_path = root / "subjects" / "python" / "campaigns" / campaign / "missions" / mission
    journal_path = mission_path / "journal.md"

    if not mission_path.exists():
        print(f"[Error] Mission path does not exist: {mission_path}")
        print("[Info] Use /dojo-start to set an active mission first.")
        return

    # Create journal if it doesn't exist
    os.makedirs(mission_path, exist_ok=True)
    if not journal_path.exists():
        with open(journal_path, "w", encoding="utf-8") as f:
            f.write(f"# Journal - {mission}\n\n## Bitácora Cronológica\n")

    # Write entry
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"\n- **[User | {timestamp}]:** {message}\n"

    with open(journal_path, "a", encoding="utf-8") as f:
        f.write(entry)

    print(f"[Sistema] ✅ Bitácora actualizada en misión: {mission}")
    print(f"[Entrada] {timestamp} → {message[:100]}{'...' if len(message) > 100 else ''}")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python log_entry.py <campaign> <mission> <message>")
        print("Example: python log_entry.py py-basico B00 'Completed first test'")
        sys.exit(1)

    log_entry(sys.argv[1], sys.argv[2], " ".join(sys.argv[3:]))
