"""
Data regression checker for answer_keys.json.
Compares current state against last snapshot, reports:
- Answer changes (potential corruption)
- Confidence downgrades (high->low)
- New unverified entries
- Coverage percentage changes
"""
import json
import sys
import os
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent
ANSWER_KEYS = ROOT / "data" / "ground_truth" / "answer_keys.json"
SNAPSHOT = ROOT / "data" / "validation_reports" / "answer_keys_snapshot.json"

REGRESSION = 0
WARNING = 0


def load_json(path):
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)


def severity(level):
    return {"high": 3, "medium": 2, "low": 1, "json_only": 0}.get(level, 0)


def main():
    global REGRESSION, WARNING
    current = load_json(ANSWER_KEYS)
    if not current:
        print("ERROR: answer_keys.json not found")
        sys.exit(1)

    answers = current.get("answers", {})
    total = sum(
        len(tests.get("listening", {})) + len(tests.get("reading", {}))
        for book in answers.values()
        for tests in book.values()
        if isinstance(tests, dict)
    )
    # Count by confidence
    by_conf = {"high": 0, "medium": 0, "low": 0, "json_only": 0}
    for book in answers.values():
        for tn in book.values():
            if not isinstance(tn, dict):
                continue
            for section in tn.values():
                if not isinstance(section, dict):
                    continue
                for q in section.values():
                    if isinstance(q, dict):
                        conf = q.get("confidence", "json_only")
                        by_conf[conf] = by_conf.get(conf, 0) + 1

    coverage = 100 * by_conf["high"] / total if total > 0 else 0

    print(f"Current state:")
    print(f"  Total answers:   {total}")
    print(f"  High confidence: {by_conf['high']} ({coverage:.1f}%)")
    print(f"  Medium:          {by_conf['medium']}")
    print(f"  Low:             {by_conf['low']}")
    print(f"  json_only:       {by_conf['json_only']}")

    # Compare with snapshot
    snapshot = load_json(SNAPSHOT)
    if snapshot:
        snap_by_conf = snapshot.get("confidence_counts", {})
        snap_total = snapshot.get("total_answers", 0)
        snap_coverage = snapshot.get("coverage_pct", 0)

        print(f"\nSnapshot state ({snapshot.get('date', 'unknown')}):")
        print(f"  Total answers:   {snap_total}")
        print(f"  High confidence: {snap_by_conf.get('high', 0)} ({snap_coverage:.1f}%)")

        # Check for regressions
        changed_answers = []
        downgraded = []

        for book_name, book_data in answers.items():
            snap_book = snapshot.get("answers", {}).get(book_name, {})
            for tn, tn_data in book_data.items():
                if not isinstance(tn_data, dict):
                    continue
                snap_tn = snap_book.get(tn, {})
                for sec, sec_data in tn_data.items():
                    if not isinstance(sec_data, dict):
                        continue
                    snap_sec = snap_tn.get(sec, {})
                    for qid, qdata in sec_data.items():
                        if not isinstance(qdata, dict):
                            continue
                        snap_q = snap_sec.get(qid, {})
                        if snap_q:
                            old_ans = snap_q.get("answer", "")
                            new_ans = qdata.get("answer", "")
                            if old_ans and new_ans and old_ans != new_ans:
                                changed_answers.append((qid, old_ans, new_ans))
                            old_sev = severity(snap_q.get("confidence", "json_only"))
                            new_sev = severity(qdata.get("confidence", "json_only"))
                            if new_sev < old_sev:
                                downgraded.append(
                                    (qid, snap_q.get("confidence"), qdata.get("confidence"))
                                )

        if changed_answers:
            REGRESSION += len(changed_answers)
            print(f"\n⚠ ANSWER CHANGES DETECTED ({len(changed_answers)}):")
            for qid, old, new in changed_answers[:10]:
                print(f"  {qid}: \"{old}\" → \"{new}\"")
            if len(changed_answers) > 10:
                print(f"  ... and {len(changed_answers) - 10} more")

        if downgraded:
            REGRESSION += len(downgraded)
            print(f"\n⚠ CONFIDENCE DOWNGRADES ({len(downgraded)}):")
            for qid, old, new in downgraded[:10]:
                print(f"  {qid}: {old} → {new}")

        if coverage < snap_coverage - 0.5:
            WARNING += 1
            print(f"\n⚠ Coverage dropped: {snap_coverage:.1f}% → {coverage:.1f}%")

    # Save snapshot
    snapshot_data = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_answers": total,
        "coverage_pct": coverage,
        "confidence_counts": by_conf,
        "answers": answers,
    }
    SNAPSHOT.parent.mkdir(parents=True, exist_ok=True)
    with open(SNAPSHOT, "w") as f:
        json.dump(snapshot_data, f, indent=2, ensure_ascii=False)
    print(f"\nSnapshot saved to {SNAPSHOT}")

    if REGRESSION > 0:
        print(f"\n❌ {REGRESSION} regression(s) found")
        sys.exit(1)
    else:
        print(f"\n✓ No regressions detected")
        sys.exit(0)


if __name__ == "__main__":
    main()
