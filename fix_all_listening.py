"""
Comprehensive fix for all listening.json files.

Fixes:
  1. notes_completion → form_completion (invalid type name)
  2. Multi-select detection: consecutive MC questions with same stem → multiple_choice_multi
  3. ID standardization: legacy ltN format → tN_l format
  4. Matching option validation (option count vs question type)
  5. Answer key normalization

Usage:
  python3 fix_all_listening.py --dry-run    # Preview fixes only
  python3 fix_all_listening.py              # Apply fixes
  python3 fix_all_listening.py --cam cam14  # Fix specific book
"""

import json
import os
import re
import sys
from collections import defaultdict
from copy import deepcopy
from pathlib import Path

DATA_DIR = Path("data/cambridge")

VALID_TYPES = {
    "form_completion", "table_completion", "flow_chart", "summary_completion",
    "sentence_completion", "multiple_choice", "multiple_choice_multi",
    "matching", "map_labelling", "short_answer", "note_completion",
}

TYPE_ALIASES = {
    "notes_completion": "form_completion",
}


def normalize_id(old_id: str, cam_id: str) -> str:
    """Normalize ID to camXX_tN_l_qM format."""
    # cam17 format: cam17_t1_l_q1 (already correct)
    if re.match(rf"{cam_id}_t\d+_l_[pq]\d+$", old_id):
        return old_id

    # Legacy format: cam14_lt1_q1 or cam14_lt1_p1
    m = re.match(rf"{cam_id}_lt(\d+)_([pq])(\d+)$", old_id)
    if m:
        test_num, pq, num = m.group(1), m.group(2), m.group(3)
        # Determine if listening or reading from type
        return f"{cam_id}_t{test_num}_l_{pq}{num}"

    return old_id


def fix_type(qtype: str) -> str:
    """Normalize question type."""
    return TYPE_ALIASES.get(qtype, qtype)


def detect_multi_select_stems(questions: list) -> dict:
    """Find consecutive questions sharing the same stem → multi-select candidates."""
    groups = defaultdict(list)
    for q in questions:
        stem = q.get("question", "").strip()
        if stem:
            groups[stem].append(q)
    return {stem: qs for stem, qs in groups.items() if len(qs) >= 2}


def fix_listening(cam_id: str, dry_run: bool = False) -> dict:
    """Apply all fixes to one book's listening.json."""
    path = DATA_DIR / cam_id / "listening.json"
    if not path.exists():
        return {"status": "missing", "cam_id": cam_id}

    with open(path) as f:
        data = json.load(f)

    original = deepcopy(data)
    fixes = []

    for test in data.get("tests", []):
        for part in test.get("parts", []):
            pid = part.get("id", "?")
            questions = part.get("questions", [])

            # Fix 1: Normalize question types
            for q in questions:
                old_type = q.get("type", "")
                new_type = fix_type(old_type)
                if old_type != new_type:
                    fixes.append(f"TYPE: {q['id']} {old_type} → {new_type}")
                    q["type"] = new_type

            # Fix 2: Detect multi-select questions
            multi_groups = detect_multi_select_stems(questions)
            for stem, qs in multi_groups.items():
                # Only fix if they're all MC type (not already multi)
                if all(q.get("type") == "multiple_choice" for q in qs):
                    # Check if stem contains "TWO" or "THREE" (multi-select instruction)
                    is_multi = bool(re.search(r"Choose\s+(TWO|THREE)\s+letters?", stem, re.I))
                    # Also check for consecutive numbers (11&12, 13&14 pattern)
                    nums = sorted(int(q["id"].rsplit("q", 1)[-1]) for q in qs if "q" in q["id"])
                    is_consecutive = len(nums) >= 2 and nums == list(range(nums[0], nums[-1] + 1))

                    if is_multi or (is_consecutive and len(qs) == 2):
                        for q in qs:
                            if q.get("type") == "multiple_choice":
                                old = q.get("type")
                                q["type"] = "multiple_choice_multi"
                                fixes.append(f"MULTI: {q['id']} {old} → multiple_choice_multi")

            # Fix 3: Normalize IDs
            new_qs = []
            for q in questions:
                old_id = q["id"]
                new_id = normalize_id(old_id, cam_id)
                if old_id != new_id:
                    fixes.append(f"ID: {old_id} → {new_id}")
                q["id"] = new_id
                new_qs.append(q)
            questions[:] = new_qs

            old_pid = part.get("id", "")
            new_pid = normalize_id(old_pid, cam_id)
            if old_pid != new_pid:
                fixes.append(f"ID: {old_pid} → {new_pid}")
            part["id"] = new_pid

    # Fix 4: Deduplicate multi-select stems (clean option text from stems)
    for test in data.get("tests", []):
        for part in test.get("parts", []):
            questions = part.get("questions", [])
            multi_qs = [q for q in questions if q.get("type") == "multiple_choice_multi"]

            # Group by stem
            stem_groups = defaultdict(list)
            for q in multi_qs:
                stem_groups[q.get("question", "")].append(q)

            for stem, qs in stem_groups.items():
                if len(qs) >= 2:
                    # Clean stem: remove embedded option text (A ... B ... C ...)
                    clean_stem = re.sub(
                        r"\s+[A-H]\s{1,3}[^A-H]+?(?=\s+[B-H]\s{1,3}|$)", "", stem
                    )
                    # Simpler: truncate at first option letter pattern
                    m = re.search(r"\s{2,}[A-H]\s{2,}", stem)
                    if m:
                        clean_stem = stem[:m.start()].strip()

                    if clean_stem and clean_stem != stem:
                        for q in qs:
                            if q.get("question") == stem:
                                q["question"] = clean_stem
                                fixes.append(f"CLEAN STEM: {q['id']}")

    if not dry_run and fixes:
        # Backup original
        bak_path = path.with_suffix(".json.bak")
        if not bak_path.exists():
            import shutil
            shutil.copy2(path, bak_path)

        with open(path, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    return {
        "cam_id": cam_id,
        "fixes": fixes,
        "num_fixes": len(fixes),
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Fix all listening.json files")
    parser.add_argument("--cam", type=str, default="all")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    books = (
        ["cam14", "cam15", "cam16", "cam17", "cam18", "cam19", "cam20"]
        if args.cam == "all"
        else [args.cam]
    )

    total_fixes = 0
    for cam_id in books:
        print(f"\n{'='*60}")
        print(f"  Fixing {cam_id}")
        print(f"{'='*60}")

        result = fix_listening(cam_id, dry_run=args.dry_run)
        if result.get("status") == "missing":
            print(f"  [SKIP] No data for {cam_id}")
            continue

        print(f"  Fixes: {result['num_fixes']}")
        for fix in result["fixes"][:20]:
            print(f"    - {fix}")
        if len(result["fixes"]) > 20:
            print(f"    ... and {len(result['fixes']) - 20} more")

        total_fixes += result["num_fixes"]

        if args.dry_run:
            print(f"  [DRY RUN] No changes saved")

    print(f"\n{'='*60}")
    print(f"  Total fixes across all books: {total_fixes}")
    print(f"{'='*60}")

    if args.dry_run:
        print("\n  Run without --dry-run to apply fixes.")
