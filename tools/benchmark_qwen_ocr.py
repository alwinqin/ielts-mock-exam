#!/usr/bin/env python3
"""Qwen3.6-27B OCR benchmark — streamlined version."""

import json, os, re, sys, time
from collections import defaultdict
from pathlib import Path
import fitz
from vlm_client import render_jpeg, vlm_call, PDF_DIR

BASE = Path(__file__).parent
OUTPUT = BASE / "data" / "validation_reports" / "qwen_ocr_benchmark.json"

os.environ.setdefault("VLM_API_URL", "http://100.114.112.77:8000/v1/chat/completions")
os.environ.setdefault("VLM_MODEL", "Qwen3.6-27B")

# ── Ground truth from cam17 text ──

def extract_cam17_ground_truth():
    results = {}
    doc = fitz.open(str(PDF_DIR / "cam17_questions.pdf"))
    for pg in range(118, 127):
        if pg >= doc.page_count:
            continue
        text = doc[pg].get_text()
        parsed = parse_gt_page(text)
        for tn, sections in parsed.items():
            results.setdefault(tn, {})
            for s, ans in sections.items():
                results[tn].setdefault(s, {}).update(ans)
    doc.close()
    return results

def clean_ans(raw):
    s = str(raw).strip().replace("．", "").replace("巾", "").replace("\t", " ")
    return re.sub(r"\s+", " ", s).strip()

def parse_gt_page(text):
    results = {}
    current_test = current_section = pending_q = None
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            pending_q = None
            continue
        if re.match(r"^\d{3}$", line): continue
        if "Listening and Reading answer keys" in line: continue
        m = re.match(r"TEST\s+(\d)", line, re.I)
        if m:
            current_test = int(m.group(1))
            results.setdefault(current_test, {})
            pending_q = None
            continue
        if re.match(r"LISTENI?N?G$", line):
            current_section = "listening"
            if current_test in results:
                results[current_test].setdefault(current_section, {})
            pending_q = None
            continue
        if re.match(r"READING$", line):
            current_section = "reading"
            if current_test in results:
                results[current_test].setdefault(current_section, {})
            pending_q = None
            continue
        if any(kw in line for kw in ["If you score","you are unlikely","you may get",
            "you are likely","acceptable score","examination conditions","recommend",
            "Resource Bank","Sample Writing"]):
            pending_q = None
            continue
        if re.match(r"(Section|Part|Reading Passage|Questions)\s+\d", line):
            pending_q = None
            continue
        if re.match(r"^\d{1,2}[–\-]\d{1,2}$", line):
            pending_q = None
            continue
        if current_test is None or current_section is None:
            continue
        m = re.match(r"^(\d{1,2})$", line)
        if m and 1 <= int(m.group(1)) <= 40:
            pending_q = int(m.group(1))
            continue
        if pending_q is not None and len(line) <= 100:
            results[current_test].setdefault(current_section, {})
            results[current_test][current_section][pending_q] = clean_ans(line)
            pending_q = None
    return results

# ── VLM prompt ──

VLM_PROMPT = """Task: Extract ALL answer keys from this IELTS page. Reply ONLY with the answer lines.

Format EXACTLY:
TestN Listening: 1.answer1 2.answer2 ... (all answers 1-40)
TestN Reading: 1.answer1 2.answer2 ... (all answers 1-40)

Rules:
- Letter answers: just the letter (e.g., 11.A)
- Word answers: FULL word/phrase (e.g., 1.creativity, 10.35/thirty five)
- TFNG/YNNG: TRUE, FALSE, or NOT GIVEN
- IN EITHER ORDER pairs: use / notation (e.g., 15.A/D 16.A/D)
- Keep alternative answers with / (e.g., 10.35/thirty five)

Example: Test1 Listening: 1.litter 2.dogs 3.insects 4.butterflies 5.wall 6.island 7.boots 8.beginners 9.spoons 10.35/thirty-five 11.A 12.C ... 40.anxiety

NO analysis. NO commentary. ONLY the TestN line(s)."""

# ── VLM output parsing ──

def parse_vlm_output(text):
    """Parse VLM answer lines, handling thinking tags."""
    # Strip thinking section if present
    if "<｜end▁of▁thinking｜>" in text:
        text = text.split("<｜end▁of▁thinking｜>", 1)[1]
    if "<｜end▁of▁thinking｜>" in text:
        text = text.split(" response", 1)[-1]

    results = {}
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        m = re.match(r"Test\s*(\d)\s+(Listening|Reading)\s*:?\s*(.+)", line, re.I)
        if m:
            tn = int(m.group(1))
            section = m.group(2).lower()
            results.setdefault(tn, {}).setdefault(section, {})
            # Parse tokens accounting for spaces within answers
            tail = m.group(3)
            parse_tokens(tail, results[tn][section])
    return results

def parse_tokens(text, target):
    """Parse '1.answer 2.answer ...' where answers may contain spaces (e.g., '35/thirty five')."""
    # Split on number. prefix pattern
    parts = re.split(r"\s+(?=\d{1,2}\.)", text)
    for part in parts:
        m = re.match(r"(\d{1,2})\.(.+)", part)
        if m:
            q = int(m.group(1))
            a = m.group(2).strip().rstrip(".,")
            if 1 <= q <= 40:
                target[q] = a

def answers_equal(a, b):
    a = str(a).strip().upper()
    b = str(b).strip().upper()
    if a == b:
        return True
    if a.replace(" ", "") == b.replace(" ", ""):
        return True
    if a.replace(" ", "").replace("/", "") == b.replace(" ", "").replace("/", ""):
        return True
    # TFNG abbreviations
    tfng = {"T":"TRUE","F":"FALSE","N":"NOT GIVEN","NG":"NOT GIVEN"}
    if a in tfng and tfng[a] == b:
        return True
    if b in tfng and tfng[b] == a:
        return True
    # Letter sets
    a_lets = set(re.findall(r"[A-G]", a))
    b_lets = set(re.findall(r"[A-G]", b))
    if len(a_lets) >= 2 and a_lets == b_lets:
        return True
    # Single letter in multi-letter
    if len(a_lets) == 1 and len(b_lets) >= 2 and a_lets.issubset(b_lets):
        return True
    if len(b_lets) == 1 and len(a_lets) >= 2 and b_lets.issubset(a_lets):
        return True
    # "35/thirty five" vs "35 / thirty five"
    a_parts = set(re.split(r"[/\s]+", a))
    b_parts = set(re.split(r"[/\s]+", b))
    if a_parts == b_parts:
        return True
    # TH variations
    a_cl = re.sub(r"\(?TH\)?", "", a, flags=re.I).strip()
    b_cl = re.sub(r"\(?TH\)?", "", b, flags=re.I).strip()
    if a_cl == b_cl:
        return True
    return False

def classify_type(a):
    a = str(a).strip().upper()
    if re.match(r"^[A-G](/[A-G])?$", a): return "letter"
    if a in ("TRUE","FALSE","NOT GIVEN"): return "tfng"
    if a in ("YES","NO"): return "ynng"
    if re.match(r"^[IVX]+$", a): return "roman"
    if re.match(r"^\d+", a): return "number"
    return "word"

# ── Main ──

def main():
    print("=" * 60)
    print("  Qwen3.6-27B OCR Benchmark")
    print("=" * 60)

    # Ground truth
    print("\n── Ground truth extraction ──")
    gt = extract_cam17_ground_truth()
    gt_total = sum(len(a) for s in gt.values() for a in s.values())
    print(f"  {gt_total} answers across {len(gt)} tests")
    for tn in sorted(gt):
        for sec in sorted(gt[tn]):
            print(f"    Test {tn} {sec}: {len(gt[tn][sec])} answers")

    # VLM benchmark
    print("\n── Qwen3.6-27B extraction ──")
    doc = fitz.open(str(PDF_DIR / "cam17_questions.pdf"))
    all_comparisons = []

    for pg in range(118, min(128, doc.page_count)):
        pn = pg + 1
        img = render_jpeg(doc, pg, dpi=200)
        if not img:
            continue

        print(f"  Page {pn}: ", end="", flush=True)
        t0 = time.time()
        raw = vlm_call(img, VLM_PROMPT, max_tokens=1024, temperature=0.0)
        elapsed = time.time() - t0

        if not raw:
            print("FAILED")
            continue

        parsed = parse_vlm_output(raw)
        n_parsed = sum(len(a) for s in parsed.values() for a in s.values())
        print(f"{n_parsed} answers, {elapsed:.1f}s")

        # Compare
        for tn, sections in parsed.items():
            if tn not in gt:
                continue
            for sec, answers in sections.items():
                if sec not in gt[tn]:
                    continue
                for qn, vlm_a in sorted(answers.items()):
                    if qn not in gt[tn][sec]:
                        continue
                    gt_a = str(gt[tn][sec][qn])
                    match = answers_equal(vlm_a, gt_a)
                    all_comparisons.append({
                        "test": tn, "section": sec, "question": qn,
                        "vlm": str(vlm_a), "gt": gt_a,
                        "match": match, "type": classify_type(gt_a),
                    })

    doc.close()

    # Accuracy by type
    by_type = defaultdict(lambda: {"correct": 0, "total": 0})
    for c in all_comparisons:
        by_type[c["type"]]["total"] += 1
        if c["match"]:
            by_type[c["type"]]["correct"] += 1

    print("\n── Accuracy by answer type ──")
    for t in ["letter", "word", "tfng", "ynng", "number", "roman"]:
        if t in by_type:
            d = by_type[t]
            acc = f"{d['correct']/d['total']*100:.1f}%"
            print(f"  {t:10s}: {d['correct']:3d}/{d['total']:3d} → {acc}")

    # Errors
    errors = [c for c in all_comparisons if not c["match"]]
    if errors:
        print(f"\n── Mismatches ({len(errors)}) ──")
        for e in errors[:30]:
            print(f"  T{e['test']} {e['section'][:4]:4s} Q{e['question']:2d}: "
                  f"VLM='{e['vlm'][:40]}' vs GT='{e['gt'][:40]}'")

    # Summary
    total = len(all_comparisons)
    correct = sum(1 for c in all_comparisons if c["match"])
    acc = f"{correct/total*100:.1f}%" if total else "N/A"

    print(f"\n{'=' * 60}")
    print(f"  OVERALL: {correct}/{total} = {acc}")
    print(f"{'=' * 60}")

    # Save
    report = {
        "model": os.environ.get("VLM_MODEL"),
        "total_compared": total,
        "total_correct": correct,
        "overall_accuracy": acc,
        "by_type": {t: {"correct": d["correct"], "total": d["total"],
            "accuracy": f"{d['correct']/d['total']*100:.1f}%"}
            for t, d in sorted(by_type.items())},
        "errors": errors,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"  Report: {OUTPUT}")

if __name__ == "__main__":
    main()
