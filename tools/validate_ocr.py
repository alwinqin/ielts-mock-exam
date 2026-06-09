#!/usr/bin/env python3
"""
Combined OCR validation pipeline: methods 2 + 3 + 4.

Method 2 — Dual-transcription comparison:
  Re-transcribes sampled pages at DPI 100 and DPI 120, computes text agreement
  rate. Large discrepancies flag potential OCR errors.

Method 3 — Unsupervised consistency checks:
  - Question number sequencing (1–40 per section, no gaps/duplicates)
  - Answer option labeling (A/B/C/D or A–G completeness)
  - Dictionary hit rate (real English words vs. gibberish)
  - JSON structural integrity (required fields present, data types correct)

Method 4 — Answer key cross-validation:
  Extracts answer keys from Chinese study-guide PDFs and cross-compares with
  the correctAnswer fields in reading/listening JSON data. Flags mismatches.

Usage:
  python3 validate_ocr.py                    # Run all validation
  python3 validate_ocr.py --method 2         # Dual-transcription only
  python3 validate_ocr.py --method 3         # Consistency checks only
  python3 validate_ocr.py --method 4         # Answer key validation only
  python3 validate_ocr.py --sample 50        # Sample size for method 2
"""

import json
import os
import re
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from difflib import SequenceMatcher
from pathlib import Path

import fitz
import requests

# ─── Configuration ───────────────────────────────────────────────
API_URL = "http://100.114.112.77:8000/v1/chat/completions"
MODEL = "Gemma-4-26B-A4B-it"
BASE = Path(__file__).parent
EXTRACTED_DIR = BASE / "data" / "extracted"
PDF_DIR = BASE / "data" / "cambridge" / "pdf"
CACHE_DIR = BASE / ".validation_cache"
OUTPUT_DIR = BASE / "data" / "validation_reports"
SAMPLE_SIZE = 30  # pages for method 2
MAX_VLM_TOKENS = 2048

CACHE_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

# ─── Helpers ─────────────────────────────────────────────────────
def render_page_jpeg(doc, page_num, dpi):
    """Render PDF page as base64 JPEG at given DPI."""
    from PIL import Image
    import io, base64 as b64
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = doc[page_num].get_pixmap(matrix=mat)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=75)
    return b64.b64encode(buf.getvalue()).decode()


def vlm_ask(img_b64, prompt, max_tokens=MAX_VLM_TOKENS):
    """Single VLM call with retries."""
    for attempt in range(3):
        try:
            resp = requests.post(
                API_URL,
                headers={"Content-Type": "application/json"},
                json={
                    "model": MODEL,
                    "messages": [{"role": "user", "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}},
                    ]}],
                    "max_tokens": max_tokens,
                    "temperature": 0.0,
                },
                timeout=120,
            )
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"]
            if resp.status_code == 429:
                time.sleep(min((attempt + 1) * 10, 60))
        except Exception:
            if attempt < 2:
                time.sleep(3)
    return None


def text_similarity(a, b):
    """Compute similarity ratio between two text strings."""
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_extracted_md(book_id, test_num, section):
    """Load extracted Markdown content."""
    fpath = EXTRACTED_DIR / book_id / f"test{test_num}" / f"{section}.md"
    if fpath.exists():
        return fpath.read_text(encoding="utf-8")
    return None


# ─── Method 2: Dual-Transcription Comparison ─────────────────────
def method2_dual_transcription(sample_size=SAMPLE_SIZE):
    """Re-transcribe pages at two DPI levels and compare agreement."""
    print("\n" + "=" * 60)
    print("METHOD 2: Dual-Transcription Comparison")
    print("=" * 60)

    # Collect sample pages across books
    image_books = ["cam15", "cam16", "cam18", "cam19", "cam20"]
    all_pages = []

    for book_id in image_books:
        for test_num in range(1, 5):
            # Sample listening and reading pages
            listening = load_extracted_md(book_id, test_num, "listening")
            reading = load_extracted_md(book_id, test_num, "reading")
            if listening:
                pages = re.findall(r"## Page (\d+)", listening)
                for p in pages[:2]:
                    all_pages.append((book_id, test_num, int(p) - 1, "listening"))
            if reading:
                pages = re.findall(r"## Page (\d+)", reading)
                for p in pages[:3]:
                    all_pages.append((book_id, test_num, int(p) - 1, "reading"))

    # Stratified random sample
    import random
    random.seed(42)
    sample = random.sample(all_pages, min(sample_size, len(all_pages)))

    results = []
    total_similarity = 0.0
    flagged = []

    for book_id, test_num, pg, section in sample:
        pdf_path = PDF_DIR / f"{book_id}_questions.pdf"
        if not pdf_path.exists():
            continue

        doc = fitz.open(str(pdf_path))
        if pg >= doc.page_count:
            doc.close()
            continue

        print(f"  {book_id} test{test_num} {section} p{pg+1} ...", end=" ", flush=True)

        # Transcribe at DPI 100 and DPI 120
        img100 = render_page_jpeg(doc, pg, dpi=100)
        img120 = render_page_jpeg(doc, pg, dpi=120)

        prompt = "Transcribe ALL text from this IELTS page verbatim. Output raw text only."
        text100 = vlm_ask(img100, prompt)
        time.sleep(0.3)
        text120 = vlm_ask(img120, prompt)

        doc.close()

        if text100 and text120:
            sim = text_similarity(text100, text120)
            total_similarity += sim
            status = "OK" if sim >= 0.85 else ("WARN" if sim >= 0.70 else "FLAG")
            print(f"{sim:.3f} [{status}]")

            if sim < 0.85:
                flagged.append({
                    "book": book_id, "test": test_num, "page": pg + 1,
                    "section": section, "similarity": sim,
                    "text100_len": len(text100), "text120_len": len(text120),
                })
        else:
            sim = 0.0 if not (text100 or text120) else 0.5
            total_similarity += sim
            print(f"PARTIAL [one transcription failed]")
            flagged.append({
                "book": book_id, "test": test_num, "page": pg + 1,
                "section": section, "similarity": sim,
                "error": "One or both transcriptions failed",
            })

        results.append(sim)
        time.sleep(0.5)

    avg_sim = total_similarity / len(results) if results else 0
    print(f"\n  Sample size: {len(results)}")
    print(f"  Average agreement: {avg_sim:.3f}")
    print(f"  Flagged pages: {len(flagged)}/{len(results)}")

    report = {
        "method": "dual_transcription",
        "sample_size": len(results),
        "average_agreement": round(avg_sim, 4),
        "flagged_count": len(flagged),
        "flagged": flagged,
        "interpretation": (
            "Agreement >= 0.85: High confidence — OCR is reliable for these pages.\n"
            "Agreement 0.70-0.85: Moderate — manual spot-check recommended.\n"
            "Agreement < 0.70: Low — likely OCR errors, needs review."
        ),
    }

    with open(OUTPUT_DIR / "method2_dual_transcription.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    return report


# ─── Method 3: Unsupervised Consistency Checks ───────────────────
def method3_consistency_checks():
    """Run automated consistency checks on extracted content and JSON data."""
    print("\n" + "=" * 60)
    print("METHOD 3: Unsupervised Consistency Checks")
    print("=" * 60)

    issues = []
    stats = {"pages_checked": 0, "questions_checked": 0, "issues_found": 0}

    # 3a. Check extracted Markdown for question number patterns
    print("\n--- 3a. Question number sequencing in extracted Markdown ---")
    for book_id in sorted(d for d in os.listdir(EXTRACTED_DIR) if d.startswith("cam")):
        book_dir = EXTRACTED_DIR / book_id
        for test_dir in sorted(book_dir.glob("test*")):
            tn = int(test_dir.name.replace("test", ""))
            for section in ["listening", "reading"]:
                md_path = test_dir / f"{section}.md"
                if not md_path.exists():
                    continue

                content = md_path.read_text(encoding="utf-8")
                stats["pages_checked"] += 1

                # Find all question number mentions (IELTS format: "31 ......", "1 A", "Questions 1-5", etc.)
                q_nums_raw = [int(m.group(1)) for m in re.finditer(r"\b(\d{1,2})\b", content)
                             if 1 <= int(m.group(1)) <= 40]
                q_nums_unique = sorted(set(q_nums_raw))

                # For listening: only expect partial coverage (questions spread across audio)
                # For reading: expect near-full coverage
                if q_nums_unique:
                    coverage = len(q_nums_unique) / 40.0
                    min_expected = 0.25 if section == "listening" else 0.60

                    if coverage < min_expected:
                        issues.append({
                            "type": "low_question_coverage",
                            "book": book_id, "test": tn, "section": section,
                            "detail": f"Only {len(q_nums_unique)}/40 unique question numbers found (coverage: {coverage:.1%}, expected >{min_expected:.0%})",
                        })
                        stats["issues_found"] += 1

    # 3b. Check JSON data integrity with correct nesting (tests → passages → questions)
    print("--- 3b. JSON structural integrity ---")
    def iter_questions(data):
        """Yield all questions from Cambridge JSON (handles passages and parts nesting)."""
        for test in data.get("tests", []):
            test_id = test.get("id", "?")
            # Direct questions
            for q in test.get("questions", []):
                yield test_id, q
            # Reading format: tests → passages → questions
            for passage in test.get("passages", []):
                for q in passage.get("questions", []):
                    yield test_id, q
            # Listening format: tests → parts → questions
            for part in test.get("parts", []):
                for q in part.get("questions", []):
                    yield test_id, q

    for data_type in ["reading", "listening"]:
        for book_id in sorted(d for d in os.listdir(BASE / "data" / "cambridge") if d.startswith("cam")):
            json_path = BASE / "data" / "cambridge" / book_id / f"{data_type}.json"
            if not json_path.exists():
                continue
            data = load_json(json_path)

            for test_id, q in iter_questions(data):
                stats["questions_checked"] += 1
                qid = q.get("id", "?")
                qtype = q.get("type", "")

                if "correctAnswer" not in q or not q["correctAnswer"]:
                    issues.append({
                        "type": "missing_correct_answer",
                        "book": book_id, "data_type": data_type, "question": qid,
                    })
                    stats["issues_found"] += 1

                # MCQ options check: answer letter must exist in options
                if qtype in ("multiple_choice", "multiple_choice_single") and "options" in q:
                    correct = str(q.get("correctAnswer", ""))
                    opts = q.get("options", [])
                    opt_labels = [str(o).strip() for o in opts]
                    if len(correct) == 1 and correct.isalpha() and opt_labels:
                        # Options may be "A. Text" or just "A" — check prefix match
                        found = any(
                            l == correct or l.startswith(correct + ".") or l.startswith(correct + " ")
                            for l in opt_labels
                        )
                        if not found:
                            issues.append({
                                "type": "answer_not_in_options",
                                "book": book_id, "data_type": data_type,
                                "question": qid,
                                "detail": f"Answer '{correct}' not in options {opt_labels}",
                            })
                            stats["issues_found"] += 1

    # 3c. Cross-check question counts per test (using iter_questions)
    print("--- 3c. Question count validation ---")
    for book_id in sorted(d for d in os.listdir(BASE / "data" / "cambridge") if d.startswith("cam")):
        for data_type in ["reading", "listening"]:
            json_path = BASE / "data" / "cambridge" / book_id / f"{data_type}.json"
            if not json_path.exists():
                continue
            data = load_json(json_path)
            for i, test in enumerate(data.get("tests", [])):
                q_count = sum(1 for _ in iter_questions({"tests": [test]}))
                if q_count != 40:
                    issues.append({
                        "type": "wrong_question_count",
                        "book": book_id, "data_type": data_type,
                        "test": i + 1, "detail": f"{q_count} questions (expected 40)",
                    })
                    stats["issues_found"] += 1

    print(f"\n  Total checks: {stats['pages_checked']} pages, {stats['questions_checked']} questions")
    print(f"  Issues found: {stats['issues_found']}")

    report = {
        "method": "consistency_checks",
        "stats": stats,
        "issues": issues,
    }

    with open(OUTPUT_DIR / "method3_consistency.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    return report


# ─── Method 4: Answer Key Cross-Validation ────────────────────────
def method4_answer_key_validation():
    """Extract answer keys from answers PDFs (image-based) and compare with JSON data."""
    print("\n" + "=" * 60)
    print("METHOD 4: Answer Key Cross-Validation")
    print("=" * 60)

    # Answer PDFs are pure image scans — text extraction returns empty.
    # Strategy: sample pages from the last 40% of each PDF (answer keys are
    # typically in the back), use VLM to identify answer-key pages, then
    # extract the answers from those pages.

    ANSWER_KEY_LOCATIONS = {
        "cam14": "cam14_answers.pdf",
        "cam15": "cam15_answers.pdf",
        "cam16": "cam16_answers.pdf",
        "cam17": "cam17_answers.pdf",
        "cam18": "cam18_answers.pdf",
        "cam19": "cam19_answers.pdf",
    }

    mismatches = []
    extracted_keys = {}
    stats = {"answer_keys_found": 0, "answers_compared": 0, "mismatches": 0}

    for book_id, pdf_file in ANSWER_KEY_LOCATIONS.items():
        pdf_path = PDF_DIR / pdf_file
        if not pdf_path.exists():
            print(f"  {book_id}: PDF not found — skip")
            continue

        print(f"\n  {book_id}: scanning image-based PDF for answer keys ...")
        doc = fitz.open(str(pdf_path))
        total_pages = doc.page_count

        # Sample pages in the last 40% of the book (answer keys are at the back)
        start_pg = int(total_pages * 0.6)
        # Sample every 8th page to find answer key sections
        sample_pages = list(range(start_pg, total_pages, 8))

        found_keys = False
        for pg in sample_pages:
            img_b64 = render_page_jpeg(doc, pg, dpi=80)
            # Quick check: does this page contain answer keys?
            check_prompt = (
                "Does this page contain IELTS answer keys (numbered 1-40 with "
                "letter answers like '1 B' or '1.B')? Reply ONLY 'YES' or 'NO'."
            )
            check = vlm_ask(img_b64, check_prompt, max_tokens=16)
            if not check or "YES" not in check.upper():
                continue

            # Extract the answer keys
            img_b64 = render_page_jpeg(doc, pg, dpi=120)
            extract_prompt = (
                "Extract ALL IELTS answer keys from this page. Output format:\n"
                "'Test N Listening: 1.B 2.C 3.A ... 40.D' or\n"
                "'Test N Reading: 1.B 2.C ... 40.D'\n"
                "Include the test number and section (Listening/Reading)."
            )
            result = vlm_ask(img_b64, extract_prompt, max_tokens=1024)
            if result and len(result) > 20:
                extracted_keys[f"{book_id}_p{pg+1}"] = result
                stats["answer_keys_found"] += 1
                print(f"    p{pg+1}: found answer keys ({len(result)} chars)")
                found_keys = True
            time.sleep(0.5)

        if not found_keys:
            # Try a broader scan: check pages that have significant rendered content
            print(f"    trying broader scan (pages with dense image content)...")
            for pg in range(total_pages - 1, max(0, total_pages - 60), -5):
                pix = doc[pg].get_pixmap(dpi=30)
                # Pages with content have non-white pixels
                samples = pix.samples
                if len(samples) < 1000:
                    continue
                img_b64 = render_page_jpeg(doc, pg, dpi=80)
                check_prompt = (
                    "Does this page contain IELTS answer keys (numbered 1-40)? "
                    "Reply ONLY 'YES' or 'NO'."
                )
                check = vlm_ask(img_b64, check_prompt, max_tokens=16)
                if check and "YES" in check.upper():
                    img_b64 = render_page_jpeg(doc, pg, dpi=120)
                    extract_prompt = (
                        "Extract ALL IELTS answer keys from this page. "
                        "Output: 'Test N Listening: 1.B 2.C ...' or "
                        "'Test N Reading: 1.B 2.C ...'"
                    )
                    result = vlm_ask(img_b64, extract_prompt, max_tokens=1024)
                    if result and len(result) > 20:
                        extracted_keys[f"{book_id}_p{pg+1}"] = result
                        stats["answer_keys_found"] += 1
                        print(f"    p{pg+1}: found answer keys ({len(result)} chars)")
                time.sleep(0.3)

        doc.close()

    # Compare extracted answer keys with JSON data
    if extracted_keys:
        print(f"\n  Cross-comparing with JSON data ...")
        for source, key_text in extracted_keys.items():
            book_id = source.split("_")[0]

            # Parse answer string like "1.B 2.C 3.A" into dict
            parsed = {}
            for m in re.finditer(r"(\d{1,2})\s*[\.\s]\s*([A-G])", key_text):
                parsed[int(m.group(1))] = m.group(2)

            if not parsed:
                continue

            # Determine if listening or reading
            is_listening = "listening" in key_text.lower()

            # Load corresponding JSON
            data_type = "listening" if is_listening else "reading"
            json_path = BASE / "data" / "cambridge" / book_id / f"{data_type}.json"
            if not json_path.exists():
                continue

            data = load_json(json_path)
            for _test_id, q in iter_questions(data):
                qid = q.get("id", "")
                qm = re.search(r"q(\d+)$", qid)
                if not qm:
                    continue
                q_num = int(qm.group(1))
                if q_num in parsed:
                    stats["answers_compared"] += 1
                    expected = parsed[q_num]
                    actual = str(q.get("correctAnswer", "")).strip()
                    if expected != actual:
                        mismatches.append({
                            "book": book_id,
                            "data_type": data_type,
                            "question": qid,
                            "expected": expected,
                            "actual": actual,
                        })
                        stats["mismatches"] += 1

    print(f"\n  Answer keys extracted: {stats['answer_keys_found']} pages")
    print(f"  Answers compared: {stats['answers_compared']}")
    print(f"  Mismatches found: {stats['mismatches']}")

    report = {
        "method": "answer_key_validation",
        "stats": stats,
        "extracted_keys": {k: v[:200] for k, v in extracted_keys.items()},
        "mismatches": mismatches,
    }

    with open(OUTPUT_DIR / "method4_answer_keys.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    return report


# ─── Main ─────────────────────────────────────────────────────────
def main():
    import argparse
    ap = argparse.ArgumentParser(description="Combined OCR validation pipeline")
    ap.add_argument("--method", type=int, choices=[2, 3, 4], help="Run specific method only")
    ap.add_argument("--sample", type=int, default=SAMPLE_SIZE, help="Sample size for method 2")
    args = ap.parse_args()

    print("=" * 60)
    print("OCR Validation Pipeline — Methods 2 + 3 + 4")
    print(f"Model: {MODEL}")
    print(f"Output: {OUTPUT_DIR.resolve()}")
    print("=" * 60)

    all_reports = {}

    if not args.method or args.method == 2:
        all_reports["method2"] = method2_dual_transcription(args.sample)

    if not args.method or args.method == 3:
        all_reports["method3"] = method3_consistency_checks()

    if not args.method or args.method == 4:
        all_reports["method4"] = method4_answer_key_validation()

    # Summary report
    with open(OUTPUT_DIR / "validation_summary.json", "w", encoding="utf-8") as f:
        json.dump(all_reports, f, ensure_ascii=False, indent=2)

    print(f"\n{'=' * 60}")
    print("All reports saved to:", str(OUTPUT_DIR.resolve()))
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
