#!/usr/bin/env python3
"""Fix audioFile paths in Cambridge listening.json files.

The JSON files reference audio as "cam14_test1_part1.mp3" but actual
files on disk are "cam14_s1.mp3" (s1-s16 sequentially across 4 tests).
Mapping: s_index = (test_number - 1) * 4 + part_number
"""

import json
import os
import re

DATA_DIR = "data/cambridge"

for book_id in sorted(os.listdir(DATA_DIR)):
    path = os.path.join(DATA_DIR, book_id, "listening.json")
    if not os.path.exists(path):
        continue

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    fixed = 0
    for test in data.get("tests", []):
        test_num = test.get("testNumber", 0)
        if isinstance(test_num, str):
            test_num = int(test_num)
        parts = test.get("parts", [])
        for i, part in enumerate(parts):
            part_num = i + 1
            s_idx = (test_num - 1) * 4 + part_num
            expected = f"{book_id}_s{s_idx}.mp3"
            old = part.get("audioFile", "")
            if old != expected:
                part["audioFile"] = expected
                fixed += 1
                print(f"  {old} -> {expected}")

    if fixed > 0:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Fixed {fixed} audioFile entries in {path}")
    else:
        print(f"No changes needed for {path}")

print("\nDone!")
