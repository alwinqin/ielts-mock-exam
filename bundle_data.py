#!/usr/bin/env python3
"""Bundle all JSON test data into a single JS file for file:// protocol support."""

import json
import os
from pathlib import Path

BASE = Path(__file__).parent  # ielts-reading-exam/

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def bundle_category(dir_path, pattern):
    """Load all JSON files matching pattern in dir_path, keyed by filename without .json"""
    result = {}
    if not dir_path.exists():
        return result
    for f in sorted(dir_path.glob(pattern)):
        key = f.stem  # e.g., "test1"
        result[key] = load_json(f)
    return result

bundle = {
    "reading": bundle_category(BASE / "data", "test*.json"),
    "listening": bundle_category(BASE / "data" / "listening", "test*.json"),
    "writing": bundle_category(BASE / "data" / "writing", "test*.json"),
    "speaking": bundle_category(BASE / "data" / "speaking", "test*.json"),
}

js = f"// Auto-generated data bundle — do not edit\nwindow.__DATA_BUNDLE__ = {json.dumps(bundle, ensure_ascii=False)};\n"

out = BASE / "js" / "data-bundle.js"
with open(out, 'w', encoding='utf-8') as f:
    f.write(js)

# Report
for cat, items in bundle.items():
    print(f"  {cat}: {len(items)} files")
print(f"\nWritten: {out} ({len(js) / 1024:.0f} KB)")
