"""
Cross-validate and auto-fix JSON data against official PDF ground truth.

Compares:
  1. Question count per part (must be exactly 10)
  2. Question types
  3. Multi-select handling (must be one stem, not split into "second option" dummies)
  4. Matching question options (must match the option box for that section)
  5. Answer keys (from official answer key pages)

Usage:
  python3 cross_validate_fix.py                       # Validate all
  python3 cross_validate_fix.py --fix                 # Auto-fix issues
  python3 cross_validate_fix.py --cam cam17 --dry-run # Preview issues only
  python3 cross_validate_fix.py --report              # Generate detailed report
"""

import json
import os
import re
import sys
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

DATA_DIR = Path("data/cambridge")
EXTRACTED_DIR = Path("data/extracted")


@dataclass
class Issue:
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    location: str  # e.g. "cam17_t1_l_p2"
    description: str
    fix_action: str = ""


def load_ground_truth(cam_id: str) -> Optional[dict]:
    """Load extracted ground truth JSON."""
    path = EXTRACTED_DIR / f"{cam_id}_ground_truth.json"
    if not path.exists():
        print(f"  [WARN] No ground truth for {cam_id} at {path}")
        return None
    with open(path) as f:
        return json.load(f)


def load_existing_json(cam_id: str, skill: str = "listening") -> Optional[dict]:
    """Load existing JSON data."""
    path = DATA_DIR / cam_id / f"{skill}.json"
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)


# ── Validation ──


def validate(cam_id: str) -> Tuple[List[Issue], dict]:
    """Run all validations. Returns (issues, stats)."""
    gt = load_ground_truth(cam_id)
    existing = load_existing_json(cam_id)

    if not gt or not existing:
        return [], {"status": "missing_data"}

    issues = []
    stats = {"parts_checked": 0, "questions_checked": 0, "issues_by_severity": defaultdict(int)}

    # Build lookup maps
    gt_by_id = {}
    for test_data in gt.get("tests", {}).values():
        for part in test_data.get("parts", []):
            for q in part.get("questions", []):
                gt_by_id[q["id"]] = q

    existing_by_id = {}
    for test in existing.get("tests", []):
        for part in test.get("parts", []):
            stats["parts_checked"] += 1
            for q in part.get("questions", []):
                existing_by_id[q["id"]] = q
                stats["questions_checked"] += 1

    # Check 1: Question count per part
    for test in existing.get("tests", []):
        for part in test.get("parts", []):
            qs = part.get("questions", [])
            if len(qs) != 10:
                issues.append(Issue(
                    severity="CRITICAL",
                    location=part["id"],
                    description=f"Part has {len(qs)} questions, expected 10",
                    fix_action="Remove dummy questions / add missing ones",
                ))

    # Check 2: Dummy "second option" questions
    for test in existing.get("tests", []):
        for part in test.get("parts", []):
            for q in part.get("questions", []):
                if "second option" in q.get("question", "").lower():
                    issues.append(Issue(
                        severity="CRITICAL",
                        location=q["id"],
                        description=f"Dummy 'second option' question — should be merged into multi-select group",
                        fix_action=f"Merge into question {int(q['id'].split('_q')[-1]) - 1} as multi-select",
                    ))

    # Check 3: Answer key validation
    for qid, gt_q in gt_by_id.items():
        if "correct_answer_from_book" not in gt_q:
            continue
        book_answer = gt_q["correct_answer_from_book"].strip()
        if qid not in existing_by_id:
            continue

        ex_q = existing_by_id[qid]
        ex_answer = ex_q.get("correctAnswer", "").strip()

        if not ex_answer:
            issues.append(Issue(
                severity="HIGH",
                location=qid,
                description=f"Missing answer in JSON (book says: {book_answer})",
                fix_action=f"Set correctAnswer to '{book_answer}'",
            ))
        elif ex_answer != book_answer:
            # Normalize comparison
            ex_norm = _normalize_answer(ex_answer)
            bk_norm = _normalize_answer(book_answer)
            if ex_norm != bk_norm:
                issues.append(Issue(
                    severity="HIGH",
                    location=qid,
                    description=f"Answer mismatch: JSON='{ex_answer}', Book='{book_answer}'",
                    fix_action=f"Set correctAnswer to '{book_answer}'",
                ))

    # Check 4: Matching question options
    for qid, gt_q in gt_by_id.items():
        if gt_q.get("type") != "matching":
            continue
        if qid not in existing_by_id:
            continue

        ex_q = existing_by_id[qid]
        ex_opts = ex_q.get("options", [])
        gt_opts = gt_q.get("options", [])

        if len(ex_opts) < len(gt_opts):
            issues.append(Issue(
                severity="CRITICAL",
                location=qid,
                description=f"Matching question has {len(ex_opts)} options, expected {len(gt_opts)}",
                fix_action="Replace options with correct option box entries",
            ))

    # Check 5: Multi-select question type
    for qid, gt_q in gt_by_id.items():
        if gt_q.get("type") != "multiple_choice_multi":
            continue
        if qid not in existing_by_id:
            continue

        ex_q = existing_by_id[qid]
        if ex_q.get("type") != "multiple_choice_multi":
            issues.append(Issue(
                severity="HIGH",
                location=qid,
                description=f"Should be multiple_choice_multi but is {ex_q.get('type')}",
                fix_action="Change type to multiple_choice_multi",
            ))

    for issue in issues:
        stats["issues_by_severity"][issue.severity] += 1

    return issues, stats


def _normalize_answer(ans: str) -> str:
    """Normalize answer for comparison."""
    s = ans.strip().upper()
    s = re.sub(r"\s+", "", s)
    # Handle multi-letter answers like "A,D" vs "A, D"
    s = s.replace(" ", "")
    # Handle slash alternatives
    s = s.split("/")[0].strip()
    return s


# ── Auto-fix ──


def auto_fix(cam_id: str) -> dict:
    """Auto-fix issues in the existing JSON using ground truth."""
    gt = load_ground_truth(cam_id)
    existing = load_existing_json(cam_id)

    if not gt or not existing:
        return {}

    # Build GT lookup
    gt_by_id = {}
    for test_data in gt.get("tests", {}).values():
        for part in test_data.get("parts", []):
            for q in part.get("questions", []):
                gt_by_id[q["id"]] = q

    # Build GT section ranges for matching option lookup
    gt_sections = {}
    for test_data in gt.get("tests", {}).values():
        for part in test_data.get("parts", []):
            pid = part["id"]
            for q in part.get("questions", []):
                if q.get("section_type") == "matching" and q.get("option_box"):
                    gt_sections[pid] = q.get("option_box", {})

    fixes_applied = []
    modified = deepcopy(existing)

    for test in modified["tests"]:
        for part in test["parts"]:
            pid = part["id"]
            questions = part["questions"]

            # Fix 1: Fix dummy "second option" questions — copy stem from preceding Q
            new_qs = []
            for i, q in enumerate(questions):
                if "second option" in q.get("question", "").lower():
                    # This should be a multi-select pair with the previous question
                    prev_q = questions[i - 1] if i > 0 else None
                    if prev_q and prev_q.get("type") in ("multiple_choice_multi", "multiple_choice"):
                        q["question"] = prev_q["question"]
                        q["type"] = "multiple_choice_multi"
                        q["options"] = prev_q.get("options", [])
                        fixes_applied.append(
                            f"FIXED dummy: {q['id']} -> multi_select, stem from {prev_q['id']}"
                        )
                    else:
                        fixes_applied.append(f"REMOVED dummy (no prev Q): {q['id']}")
                        continue
                new_qs.append(q)

            if len(new_qs) != len(questions):
                part["questions"] = new_qs
                questions = new_qs

            # Fix 2: Correct question types for multi-select
            for q in questions:
                qid = q["id"]
                if qid in gt_by_id:
                    gt_type = gt_by_id[qid].get("type")
                    if gt_type == "multiple_choice_multi" and q.get("type") != "multiple_choice_multi":
                        old_type = q.get("type")
                        q["type"] = "multiple_choice_multi"
                        fixes_applied.append(f"TYPE FIX: {qid} {old_type} -> multiple_choice_multi")

            # Fix 3: Correct matching question options
            if pid in gt_sections:
                opt_box = gt_sections[pid]
                gt_opts = [f"{l}. {t}" for l, t in sorted(opt_box.items())]
                for q in questions:
                    qid = q["id"]
                    if qid in gt_by_id and gt_by_id[qid].get("type") == "matching":
                        current_opts = q.get("options", [])
                        if len(current_opts) < len(gt_opts):
                            old_count = len(current_opts)
                            q["options"] = gt_opts
                            fixes_applied.append(
                                f"OPTION FIX: {qid} {old_count}->{len(gt_opts)} options"
                            )

            # Fix 4: Correct answer keys
            for q in questions:
                qid = q["id"]
                if qid in gt_by_id and "correct_answer_from_book" in gt_by_id[qid]:
                    book_answer = gt_by_id[qid]["correct_answer_from_book"]
                    current = q.get("correctAnswer", "")
                    if _normalize_answer(current) != _normalize_answer(book_answer):
                        old = current
                        q["correctAnswer"] = book_answer
                        fixes_applied.append(
                            f"ANSWER FIX: {qid} '{old}' -> '{book_answer}'"
                        )

    return {
        "cam_id": cam_id,
        "fixes_applied": fixes_applied,
        "num_fixes": len(fixes_applied),
        "modified_data": modified,
    }


def save_fixed(cam_id: str, modified_data: dict) -> str:
    """Save the fixed JSON, backing up the original."""
    orig_path = DATA_DIR / cam_id / "listening.json"
    bak_path = DATA_DIR / cam_id / "listening.json.bak"

    # Backup original if not already backed up
    if not bak_path.exists():
        import shutil
        shutil.copy2(orig_path, bak_path)

    with open(orig_path, "w") as f:
        json.dump(modified_data, f, indent=2, ensure_ascii=False)

    return str(orig_path)


# ── CLI ──

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Cross-validate IELTS data against official PDF ground truth"
    )
    parser.add_argument("--cam", type=str, default="cam17")
    parser.add_argument("--fix", action="store_true", help="Auto-fix issues")
    parser.add_argument("--dry-run", action="store_true", help="Show fixes without saving")
    parser.add_argument("--report", action="store_true", help="Generate detailed report")
    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"  Validating {args.cam}")
    print(f"{'='*60}")

    issues, stats = validate(args.cam)

    if stats.get("status") == "missing_data":
        print("  Cannot validate: missing ground truth or existing data")
        sys.exit(1)

    print(f"\n  Parts checked:     {stats['parts_checked']}")
    print(f"  Questions checked: {stats['questions_checked']}")
    print(f"  Issues found:      {len(issues)}")
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        count = stats["issues_by_severity"].get(sev, 0)
        if count:
            print(f"    {sev}: {count}")

    if issues:
        print(f"\n  Issues:")
        for issue in issues:
            print(f"    [{issue.severity}] {issue.location}: {issue.description}")

    if args.fix or args.dry_run:
        print(f"\n{'='*60}")
        print(f"  Auto-fixing {args.cam}")
        print(f"{'='*60}")

        result = auto_fix(args.cam)
        print(f"\n  Fixes applied: {result['num_fixes']}")
        for fix in result["fixes_applied"]:
            print(f"    - {fix}")

        if args.fix and not args.dry_run:
            path = save_fixed(args.cam, result["modified_data"])
            print(f"\n  Data saved to: {path}")
            print(f"  Original backed up to: {path.replace('.json', '.json.bak')}")
        else:
            print("\n  [DRY RUN] No files modified. Use --fix to apply changes.")

    if not issues:
        print("\n  All checks passed!")
