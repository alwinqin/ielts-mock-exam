#!/usr/bin/env python3
"""Normalize standalone speaking files: move followUpQuestions from part2 to part3."""
import json
import os
from pathlib import Path

SPEAKING_DIR = Path(__file__).parent / "data" / "speaking"

count = 0
for fpath in sorted(SPEAKING_DIR.glob("*.json")):
    with open(fpath, encoding="utf-8") as f:
        data = json.load(f)

    p2 = data.get("part2", {})
    fups = p2.pop("followUpQuestions", None) if isinstance(p2, dict) else None

    if fups:
        # Create part3 if it doesn't exist
        data["part3"] = [{"topic": "Discussion", "questions": fups}]
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  ✓ {fpath.name}: {len(fups)} questions → part3")
        count += 1
    else:
        print(f"  - {fpath.name}: no followUpQuestions, skipped")

print(f"\nDone. {count} files normalized.")
