#!/usr/bin/env python3
"""
Answer Key Extractor — Qwen3.6-27B edition.

Re-extracts answer keys from cam14-cam19 using Qwen3.6-27B (99.3% OCR accuracy),
then cross-validates against JSON data.

Usage:
  python3 extract_qwen_answer_keys.py
"""

import json, os, re, sys, time
from collections import defaultdict
from pathlib import Path

import fitz

from vlm_client import PDF_DIR, render_jpeg, vlm_call

BASE = Path(__file__).parent
OUTPUT = BASE / "data" / "validation_reports" / "extracted_answer_keys_qwen.json"

# ── Configuration ──

# Known answer key pages per book (1-indexed)
ANSWER_KEY_PAGES = {
    "cam14": list(range(119, 127)),  # 119-126
    "cam15": list(range(118, 129)),  # search wider
    "cam16": list(range(119, 131)),  # search wider
    "cam17": list(range(119, 127)),  # 119-126 (text-based)
    "cam18": list(range(119, 129)),  # search wider
    "cam19": list(range(120, 133)),  # search wider
}

# ── VLM prompt (tuned for Qwen3.6-27B) ──

VLM_PROMPT = """Task: Extract ALL answer keys from this IELTS page. Reply ONLY with the answer lines.

Format EXACTLY:
TestN Listening: 1.answer1 2.answer2 ... (all answers 1-40)
TestN Reading: 1.answer1 2.answer2 ... (all answers 1-40)

Rules:
- Letter answers: just the letter (e.g., 11.A)
- Word answers: FULL word/phrase (e.g., 1.creativity, 10.35/thirty five)
- TFNG/YNNG: TRUE, FALSE, or NOT GIVEN
- IN EITHER ORDER pairs: use / notation (e.g., 15.A/D 16.A/D)
- Keep alternative answers with / (e.g., 10.35/thirty five, 24.flavour/flavor)

Example: Test1 Listening: 1.litter 2.dogs 3.insects 4.butterflies 5.wall 6.island 7.boots 8.beginners 9.spoons 10.35/thirty-five 11.A 12.C ... 40.anxiety

NO analysis. NO commentary. ONLY the TestN line(s)."""

# ── Parsing ──

def parse_vlm_output(text):
    """Parse VLM answer lines, handling Qwen's thinking tags."""
    # Strip Qwen thinking section: everything before </think>
    think_end = text.find("</think>")
    if think_end != -1:
        text = text[think_end + len("</think>"):]

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
            parse_tokens(m.group(3), results[tn][section])
    return results

def parse_tokens(text, target):
    """Parse '1.answer 2.answer ...' where answers may contain spaces."""
    parts = re.split(r"\s+(?=\d{1,2}\.)", text)
    for part in parts:
        m = re.match(r"(\d{1,2})\.(.+)", part)
        if m:
            q = int(m.group(1))
            a = m.group(2).strip().rstrip(".,")
            if 1 <= q <= 40:
                target[q] = clean_vlm_answer(a)

def clean_vlm_answer(raw):
    """Normalize a single VLM answer."""
    s = str(raw).strip()
    s = re.sub(r"\s+", " ", s)
    # Fix "C 23" → "C" (next question number stuck)
    s = re.sub(r"\s+\d{1,2}$", "", s)
    return s

# ── Text-based extraction (cam17 only) ──

def extract_cam17_text():
    """Extract cam17 answer keys from text layer (reliable ground truth)."""
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
            results[current_test][current_section][pending_q] = clean_gt_answer(line)
            pending_q = None
    return results

def clean_gt_answer(raw):
    s = str(raw).strip().replace("．", "").replace("巾", "").replace("\t", " ")
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s*IN\s+EITHER\s+ORDER\s*", "", s, flags=re.I).strip()
    return s

# ── Normalization & comparison ──

NUMBER_WORDS = {
    "one":"1","two":"2","three":"3","four":"4","five":"5",
    "six":"6","seven":"7","eight":"8","nine":"9","ten":"10",
    "eleven":"11","twelve":"12","thirteen":"13","fourteen":"14",
    "fifteen":"15","sixteen":"16","seventeen":"17","eighteen":"18",
    "nineteen":"19","twenty":"20","thirty":"30","thirty five":"35",
    "forty":"40","fifty":"50",
}

def normalize_answer(raw):
    s = str(raw).strip()
    s = re.sub(r'[;:,]+$', '', s)
    s = re.sub(r'\s+', ' ', s)
    if re.match(r'^[A-Ga-g]$', s):
        return s.upper()
    slash_parts = [p.strip() for p in s.split('/')]
    if len(slash_parts) == 2:
        for part in slash_parts:
            if re.match(r'^\d+$', part):
                return part
            if part.lower() in NUMBER_WORDS:
                return NUMBER_WORDS[part.lower()]
    s = re.sub(r'\(th\)', 'th', s)
    return s.strip()

def answers_match(a, b):
    na = normalize_answer(a)
    nb = normalize_answer(b)
    if na == nb:
        return True
    if na.upper() == nb.upper():
        return True
    if na.replace(" ", "").upper() == nb.replace(" ", "").upper():
        return True
    # TH variations
    na_cl = re.sub(r'\(?TH\)?', '', na, flags=re.I)
    nb_cl = re.sub(r'\(?TH\)?', '', nb, flags=re.I)
    if na_cl == nb_cl:
        return True
    # Number words
    if re.match(r'^\d+$', na) and nb.lower() in NUMBER_WORDS:
        if na == NUMBER_WORDS[nb.lower()]:
            return True
    if re.match(r'^\d+$', nb) and na.lower() in NUMBER_WORDS:
        if nb == NUMBER_WORDS[na.lower()]:
            return True
    # Multi-letter sets
    na_lets = set(re.findall(r'[A-G]', na.upper()))
    nb_lets = set(re.findall(r'[A-G]', nb.upper()))
    if len(na_lets) >= 2 and na_lets == nb_lets:
        return True
    # Single letter matches first char of option text
    if re.match(r'^[A-Ga-g]$', na) and nb and na.upper() == nb[0].upper():
        return True
    if re.match(r'^[A-Ga-g]$', nb) and na and nb.upper() == na[0].upper():
        return True
    # TFNG
    tfng = {"T":"TRUE","F":"FALSE","N":"NOT GIVEN","NG":"NOT GIVEN",
            "Y":"YES","NO":"NO","NOT":"NOT GIVEN"}
    if na.upper() in tfng and tfng[na.upper()] == nb.upper():
        return True
    if nb.upper() in tfng and tfng[nb.upper()] == na.upper():
        return True
    # Slash sets
    if "/" in na or "/" in nb:
        na_parts = set(re.split(r'[/()]|\band\b', na, flags=re.I))
        nb_parts = set(re.split(r'[/()]|\band\b', nb, flags=re.I))
        na_clean = {p.strip().lower() for p in na_parts if p.strip()}
        nb_clean = {p.strip().lower() for p in nb_parts if p.strip()}
        if na_clean and na_clean == nb_clean:
            return True
        if na_clean and nb_clean:
            if na_clean.issubset(nb_clean) or nb_clean.issubset(na_clean):
                return True
    return False

# ── Cross-validation ──

def cross_validate(extracted, book_id):
    mismatches = []
    stats = {"compared": 0, "matched": 0, "mismatched": 0}

    for data_type in ["listening", "reading"]:
        json_path = BASE / "data" / "cambridge" / book_id / f"{data_type}.json"
        if not json_path.exists():
            continue

        data = json.loads(json_path.read_text(encoding="utf-8"))

        for test in data.get("tests", []):
            test_id = test.get("id", "")
            m = re.search(r"t(\d)$", test_id)
            if not m:
                continue
            test_num = int(m.group(1))

            if test_num not in extracted:
                continue
            if data_type not in extracted[test_num]:
                continue

            expected = extracted[test_num][data_type]
            qs = []
            for container in test.get("parts", test.get("passages", [])):
                qs.extend(container.get("questions", []))

            for q in qs:
                qid = q.get("id", "")
                m = re.search(r"q(\d+)$", qid)
                if not m:
                    continue
                q_num = int(m.group(1))

                if q_num in expected:
                    stats["compared"] += 1
                    json_answer = str(q.get("correctAnswer", "")).strip()
                    key_answer = str(expected[q_num]).strip()

                    if answers_match(json_answer, key_answer):
                        stats["matched"] += 1
                    else:
                        stats["mismatched"] += 1
                        mismatches.append({
                            "book": book_id, "test": test_num,
                            "section": data_type, "question": qid,
                            "json_answer": json_answer,
                            "key_answer": key_answer,
                        })

    return stats, mismatches

# ── Main ──

def main():
    print("=" * 70)
    print("  Answer Key Extractor — Qwen3.6-27B")
    print("=" * 70)

    all_keys = {}
    validation = {}

    for book_id in ["cam14", "cam15", "cam16", "cam17", "cam18", "cam19"]:
        print(f"\n{'─' * 50}")
        print(f"  {book_id}")

        if book_id == "cam17":
            # Text-based extraction (ground truth quality)
            keys = extract_cam17_text()
        else:
            keys = extract_vlm_book(book_id)

        if keys:
            total = sum(len(a) for sections in keys.values() for a in sections.values())
            print(f"  Total: {total} answers")
            for tn in sorted(keys):
                for sec in sorted(keys[tn]):
                    print(f"    Test {tn} {sec}: {len(keys[tn][sec])} answers")
            all_keys[book_id] = keys
        else:
            print(f"  FAILED: no answers extracted")

    # Cross-validate
    print(f"\n{'=' * 70}")
    print("  Cross-validation against JSON data")
    print(f"{'=' * 70}")

    for book_id, keys in sorted(all_keys.items()):
        stats, mismatches = cross_validate(keys, book_id)
        validation[book_id] = {"stats": stats, "mismatches": mismatches}
        total = stats["compared"]
        acc = f"{stats['matched']/total*100:.1f}%" if total else "N/A"
        print(f"\n  {book_id}: {stats['compared']} compared, "
              f"{stats['matched']} matched, {stats['mismatched']} mismatched → {acc}")

        if mismatches:
            print(f"    Sample (first 5):")
            for m in mismatches[:5]:
                print(f"      {m['question']}: key='{m['key_answer'][:40]}' json='{m['json_answer'][:40]}'")

    # Save report
    report = {
        "version": "qwen3.6-27b",
        "model": "Qwen3.6-27B",
        "extracted_keys": {
            book: {
                f"test{tn}": {
                    s: {str(q): a for q, a in sorted(ans.items())}
                    for s, ans in sorted(sections.items())
                }
                for tn, sections in sorted(keys.items())
            }
            for book, keys in sorted(all_keys.items())
        },
        "validation": validation,
        "summary": {
            "books_processed": len(all_keys),
            "total_compared": sum(v["stats"]["compared"] for v in validation.values()),
            "total_matched": sum(v["stats"]["matched"] for v in validation.values()),
            "total_mismatched": sum(v["stats"]["mismatched"] for v in validation.values()),
        },
    }

    tc = report["summary"]["total_compared"]
    tm = report["summary"]["total_matched"]
    report["summary"]["overall_accuracy"] = f"{tm/tc*100:.1f}%" if tc else "N/A"

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n{'=' * 70}")
    print(f"  Report: {OUTPUT}")
    print(f"  Books: {len(all_keys)} | Compared: {tc} | "
          f"Matched: {tm} | Mismatched: {report['summary']['total_mismatched']}")
    print(f"  Overall: {report['summary']['overall_accuracy']}")
    print(f"{'=' * 70}")

def extract_vlm_book(book_id):
    """Extract answer keys using Qwen3.6-27B VLM."""
    pdf_path = PDF_DIR / f"{book_id}_questions.pdf"
    if not pdf_path.exists():
        print(f"  PDF not found: {pdf_path}")
        return {}

    pages = ANSWER_KEY_PAGES.get(book_id, list(range(110, 135)))
    doc = fitz.open(str(pdf_path))
    results = {}

    for pg_num in pages:
        pg = pg_num - 1  # Convert to 0-indexed
        if pg >= doc.page_count:
            continue

        img = render_jpeg(doc, pg, dpi=200)
        if not img:
            continue

        print(f"    p{pg_num}: ", end="", flush=True)
        t0 = time.time()
        raw = vlm_call(img, VLM_PROMPT, max_tokens=1024, temperature=0.0)
        elapsed = time.time() - t0

        if not raw:
            print("FAILED")
            continue

        parsed = parse_vlm_output(raw)
        n = sum(len(a) for s in parsed.values() for a in s.values())
        print(f"{n} answers, {elapsed:.1f}s")

        for tn, sections in parsed.items():
            results.setdefault(tn, {})
            for sec, answers in sections.items():
                results[tn].setdefault(sec, {}).update(answers)

        time.sleep(0.3)

    doc.close()
    return results

if __name__ == "__main__":
    main()
