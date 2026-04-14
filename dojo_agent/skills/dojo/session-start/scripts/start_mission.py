#!/usr/bin/env python3
"""DoJo Session Start Script — Validates and loads campaign/mission context."""

import os
import sys
from pathlib import Path


def find_dojo_root() -> Path:
    """Find the DoJo_Study root directory."""
    # Try common locations
    candidates = [
        Path.home() / "Documents" / "DoJo" / "DoJo_Study",
        Path.cwd(),
    ]
    for candidate in candidates:
        if (candidate / "subjects").exists():
            return candidate
    raise FileNotFoundError("Could not find DoJo_Study root directory")


def resolve_case_insensitive(base_path: Path, target_name: str) -> str:
    """Find the real name with correct casing on disk."""
    if not base_path.exists():
        return target_name
    for name in os.listdir(base_path):
        if name.lower() == target_name.lower():
            return name
    return target_name


def start_mission(campaign_raw: str, mission_raw: str) -> None:
    """Validate and load a DoJo mission context."""
    root = find_dojo_root()
    campaigns_dir = root / "subjects" / "python" / "campaigns"

    if not campaigns_dir.exists():
        print(f"[Error] Campaigns directory not found: {campaigns_dir}")
        return

    # Resolve case-insensitive names
    campaign = resolve_case_insensitive(campaigns_dir, campaign_raw)
    missions_dir = campaigns_dir / campaign / "missions"
    mission = resolve_case_insensitive(missions_dir, mission_raw)
    mission_path = missions_dir / mission

    if not mission_path.exists():
        # List available missions
        available = []
        if missions_dir.exists():
            available = [
                d for d in os.listdir(missions_dir)
                if os.path.isdir(missions_dir / d)
            ]
        print(f"[Error] Mission '{mission_raw}' not found in campaign '{campaign}'.")
        if available:
            print(f"[Info] Available missions: {', '.join(sorted(available))}")
        else:
            print(f"[Info] No missions found. Available campaigns: "
                  f"{', '.join(sorted(os.listdir(campaigns_dir)))}")
        return

    # Load requirements.md
    req_path = mission_path / "requirements.md"
    requirements_content = ""
    if req_path.exists():
        with open(req_path, "r", encoding="utf-8") as f:
            requirements_content = f.read()[:3000]

    # Load journal.md tail
    journal_path = mission_path / "journal.md"
    journal_tail = ""
    if journal_path.exists():
        with open(journal_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            journal_tail = "".join(lines[-10:]) if len(lines) > 10 else "".join(lines)

    # Output context
    print(f"\n{'='*60}")
    print(f"  ⛩️  DoJo SESSION STARTED")
    print(f"  Campaign: {campaign}")
    print(f"  Mission:  {mission}")
    print(f"  Path:     {mission_path}")
    print(f"{'='*60}")

    if requirements_content:
        print(f"\n📋 REQUIREMENTS (requirements.md):\n")
        print(requirements_content)

    if journal_tail:
        print(f"\n📝 LAST JOURNAL ENTRIES:\n")
        print(journal_tail)

    if not requirements_content and not journal_tail:
        print("\n[Info] Empty mission. No requirements.md or journal.md found yet.")

    print(f"\n{'='*60}")
    print(f"  Context is now active. The agent will use this mission's")
    print(f"  requirements and journal for all subsequent interactions.")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python start_mission.py <campaign> <mission>")
        print("Example: python start_mission.py py-basico B00")
        sys.exit(1)

    start_mission(sys.argv[1], sys.argv[2])
