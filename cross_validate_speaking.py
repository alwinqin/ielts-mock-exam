#!/usr/bin/env python3
"""Cross-validate speaking data against source PDFs.

For text-based books (cam14, cam17): extract text and compare verbatim.
For VLM-based books (cam15, cam16, cam18, cam19, cam20): verify via VLM re-check.
"""
import json
import re
import sys
from pathlib import Path

import fitz

from vlm_client import PDF_DIR, render_jpeg, vlm_call

OUTPUT_DIR = Path(__file__).parent / "data" / "cambridge"
REPORT_FILE = Path(__file__).parent / "data" / "validation_reports" / "speaking_cross_validation.json"


def audit_json_file(book_id):
    """Audit a speaking.json file for completeness."""
    path = OUTPUT_DIR / book_id / "speaking.json"
    if not path.exists():
        return {"error": f"File not found: {path}"}

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    tests = data.get("tests", [])
    report = {"book": book_id, "test_count": len(tests), "tests": []}

    for t in tests:
        t_report = {"id": t["id"], "testNumber": t.get("testNumber")}

        # Part 1
        p1 = t.get("part1", {})
        t_report["part1_topic"] = p1.get("topic", "")
        t_report["part1_questions"] = len(p1.get("questions", []))

        # Part 2
        p2 = t.get("part2", {})
        t_report["part2_title"] = p2.get("title", "")
        t_report["part2_prompts"] = len(p2.get("prompts", []))

        # Part 3
        p3 = t.get("part3", {})
        topics = p3.get("topics", [])
        t_report["part3_topics"] = len(topics)
        t_report["part3_questions"] = sum(len(tp.get("questions", [])) for tp in topics)

        # Completeness check
        issues = []
        if t_report["part1_questions"] < 4:
            issues.append(f"Part 1 only has {t_report['part1_questions']} questions (expected 4)")
        if t_report["part2_prompts"] < 4:
            issues.append(f"Part 2 only has {t_report['part2_prompts']} prompts (expected 4)")
        if t_report["part3_topics"] < 2:
            issues.append(f"Part 3 only has {t_report['part3_topics']} topics (expected 2)")
        if not t_report["part1_topic"]:
            issues.append("Part 1 topic is empty")
        if not t_report["part2_title"]:
            issues.append("Part 2 title is empty")

        t_report["issues"] = issues
        t_report["complete"] = len(issues) == 0
        report["tests"].append(t_report)

    report["complete_tests"] = sum(1 for t in report["tests"] if t["complete"])
    report["total_issues"] = sum(len(t["issues"]) for t in report["tests"])
    return report


def verify_text_extraction(book_id):
    """For text-based PDFs, re-extract and compare with stored JSON."""
    pdf_path = PDF_DIR / f"{book_id}_questions.pdf"
    if not pdf_path.exists():
        return {"error": f"PDF not found: {pdf_path}"}

    doc = fitz.open(str(pdf_path))

    # Find speaking pages
    speaking_pages = []
    for pg in range(doc.page_count):
        text = doc[pg].get_text()
        if "SPEAKING" in text and ("PART 1" in text or "Part 1" in text):
            if "You should say" in text or "Describe a" in text or "EXAMPLE" in text:
                speaking_pages.append(pg)

    # Load stored JSON
    json_path = OUTPUT_DIR / book_id / "speaking.json"
    with open(json_path, encoding="utf-8") as f:
        stored = json.load(f)

    results = {"book": book_id, "speaking_pages": speaking_pages, "tests": []}

    for i, pg in enumerate(speaking_pages):
        if i >= len(stored["tests"]):
            break

        stored_test = stored["tests"][i]
        # Get text from this page + next page
        full_text = ""
        for offset in range(3):
            if pg + offset < doc.page_count:
                full_text += doc[pg + offset].get_text() + "\n"

        t_result = {"id": stored_test["id"], "checks": []}

        # Check Part 1 topic in extracted text
        p1 = stored_test.get("part1", {})
        p1_topic = p1.get("topic", "")
        if p1_topic and p1_topic in full_text:
            t_result["checks"].append({"field": "part1.topic", "status": "ok"})
        else:
            t_result["checks"].append({"field": "part1.topic", "status": "not_found", "expected": p1_topic})

        # Check Part 2 title
        p2 = stored_test.get("part2", {})
        p2_title = p2.get("title", "")
        # Try matching key words from the title
        title_words = [w for w in p2_title.split() if len(w) > 4]
        title_found = any(w in full_text for w in title_words) if title_words else False
        if title_found or p2_title[:30] in full_text:
            t_result["checks"].append({"field": "part2.title", "status": "ok"})
        else:
            t_result["checks"].append({"field": "part2.title", "status": "partial", "expected": p2_title[:80]})

        # Check a sample of Part 1 questions
        for j, q in enumerate(p1.get("questions", [])[:2]):
            key_words = " ".join(q.split()[:5])
            if key_words[:30] in full_text:
                t_result["checks"].append({"field": f"part1.q{j+1}", "status": "ok"})
            else:
                t_result["checks"].append({"field": f"part1.q{j+1}", "status": "partial", "expected": q[:80]})

        # Check Part 2 prompts
        for j, prompt in enumerate(p2.get("prompts", [])[:2]):
            key_words = " ".join(prompt.split()[:4])
            if key_words[:25] in full_text:
                t_result["checks"].append({"field": f"part2.prompt{j+1}", "status": "ok"})
            else:
                t_result["checks"].append({"field": f"part2.prompt{j+1}", "status": "partial", "expected": prompt[:80]})

        results["tests"].append(t_result)

    doc.close()
    return results


def vlm_verify_test(book_id, test_index, stored_test):
    """Use VLM to verify a single test's extracted data against the PDF."""
    pdf_path = PDF_DIR / f"{book_id}_questions.pdf"
    if not pdf_path.exists():
        return {"error": f"PDF not found: {pdf_path}"}

    doc = fitz.open(str(pdf_path))

    # Find speaking pages via VLM scan
    total = doc.page_count
    speaking_pages = []
    for pg in range(int(total * 0.5), total):
        img_b64 = render_jpeg(doc, pg, dpi=80)
        check = vlm_call(
            img_b64,
            "Does this page contain an IELTS Speaking test section with Part 1 questions? "
            "Reply ONLY 'YES' or 'NO'.",
            max_tokens=8,
        )
        if check and "YES" in check.upper():
            speaking_pages.append(pg)
            if len(speaking_pages) > test_index:
                break

    if test_index >= len(speaking_pages):
        doc.close()
        return {"error": f"Could not find speaking page for test {test_index+1}"}

    pg = speaking_pages[test_index]

    # Render at high DPI for verification
    img_b64 = render_jpeg(doc, pg, dpi=200)
    next_b64 = render_jpeg(doc, pg + 1, dpi=200) if pg + 1 < total else None

    # Build verification prompt with stored data
    stored_json = json.dumps({
        "part1_topic": stored_test.get("part1", {}).get("topic", ""),
        "part1_questions": stored_test.get("part1", {}).get("questions", [])[:2],
        "part2_title": stored_test.get("part2", {}).get("title", ""),
        "part2_prompts": stored_test.get("part2", {}).get("prompts", [])[:2],
    }, ensure_ascii=False, indent=2)

    prompt = f"""Compare this stored IELTS speaking test data against what's visible in the page image.

STORED DATA:
{stored_json}

For each field, reply with ONE word:
- "MATCH" if the stored text exactly matches what's printed on the page
- "CLOSE" if the meaning is the same but wording differs slightly
- "WRONG" if the stored text is significantly different from the page

Reply in this format:
part1_topic: MATCH/CLOSE/WRONG
part1_q1: MATCH/CLOSE/WRONG
part1_q2: MATCH/CLOSE/WRONG
part2_title: MATCH/CLOSE/WRONG
part2_prompt1: MATCH/CLOSE/WRONG
part2_prompt2: MATCH/CLOSE/WRONG

If WRONG, add a brief note of what's actually on the page."""

    result = vlm_call([img_b64] + ([next_b64] if next_b64 else []), prompt, max_tokens=512)

    doc.close()
    return {"test": stored_test["id"], "verification": result}


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "audit"

    if mode == "audit":
        print("=" * 60)
        print("SPEAKING DATA AUDIT")
        print("=" * 60)
        all_reports = []
        for book_id in sorted([d.name for d in OUTPUT_DIR.iterdir() if d.is_dir() and d.name.startswith("cam")]):
            report = audit_json_file(book_id)
            all_reports.append(report)
            print(f"\n--- {book_id} ---")
            print(f"  Tests: {report['test_count']}")
            for t in report["tests"]:
                status = "✓" if t["complete"] else "✗"
                print(f"  {status} Test {t['testNumber']}: P1={t['part1_questions']}qs P2={t['part2_prompts']}prompts P3={t['part3_topics']}topics/{t['part3_questions']}qs")
                for issue in t["issues"]:
                    print(f"    ⚠ {issue}")
            print(f"  Complete: {report['complete_tests']}/{report['test_count']}")

        # Save report
        REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            json.dump(all_reports, f, ensure_ascii=False, indent=2)
        print(f"\nReport saved to {REPORT_FILE}")

    elif mode == "verify_text":
        book_id = sys.argv[2] if len(sys.argv) > 2 else "cam14"
        print(f"Verifying text extraction for {book_id}...")
        results = verify_text_extraction(book_id)
        print(json.dumps(results, ensure_ascii=False, indent=2))

    elif mode == "verify_vlm":
        book_id = sys.argv[2] if len(sys.argv) > 2 else "cam15"
        test_idx = int(sys.argv[3]) if len(sys.argv) > 3 else 0

        json_path = OUTPUT_DIR / book_id / "speaking.json"
        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)

        if test_idx >= len(data["tests"]):
            print(f"Test index {test_idx} out of range")
            return

        print(f"VLM verifying {book_id} test {test_idx+1}...")
        result = vlm_verify_test(book_id, test_idx, data["tests"][test_idx])
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
