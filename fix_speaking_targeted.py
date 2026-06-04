#!/usr/bin/env python3
"""Quick targeted extraction of specific missing/corrupt speaking tests."""
import json, re, sys
from pathlib import Path
import fitz
from vlm_client import PDF_DIR, render_jpeg, vlm_call

OUTPUT_DIR = Path(__file__).parent / "data" / "cambridge"


def try_extract(doc, page_num, total):
    """Try to extract speaking content from a page. Returns dict or None."""
    if page_num >= total:
        return None

    img = render_jpeg(doc, page_num, dpi=200)
    next_img = render_jpeg(doc, page_num + 1, dpi=200) if page_num + 1 < total else None
    images = [img] + ([next_img] if next_img else [])

    # Check if this page has listening content first
    check = vlm_call(img, "Is this page showing IELTS Listening test content (gap-fills, multiple choice options A/B/C/D/E) or SPEAKING test content? Reply 'LISTENING' or 'SPEAKING' only.", max_tokens=12)
    if not check or 'LISTENING' in check.upper():
        return None

    prompt = """Extract this IELTS Speaking test page as JSON with these exact keys:
{"part1":{"topic":"...","questions":["q1","q2","q3","q4"]},"part2":{"title":"Describe...","prompts":["b1","b2","b3","b4"]},"part3":{"topics":[{"topic":"...","questions":["q1","q2","q3"]},{"topic":"...","questions":["q1","q2","q3"]}]}}
Copy text EXACTLY from page. Output only valid JSON."""

    result = vlm_call(images, prompt, max_tokens=2048)
    if not result:
        return None

    m = re.search(r'\{[\s\S]*\}', result)
    if not m:
        return None
    try:
        data = json.loads(m.group())
        # Basic validation
        p2 = data.get("part2", {})
        if p2.get("title", "").startswith("Describe") and p2.get("prompts"):
            return data
    except json.JSONDecodeError:
        pass
    return None


# Exactly which tests to fix and page candidates
FIX_PLAN = {
    "cam18": {
        "file": "cam18_questions.pdf",
        "tests": {
            1: [35, 55, 36, 56],  # Test 2 (0-indexed: 1)
        }
    },
    "cam19": {
        "file": "cam19_questions.pdf",
        "tests": {
            1: [35, 36, 37],  # Test 2
            2: [57, 58, 59],  # Test 3
            3: [101, 102, 103],  # Test 4
        }
    },
}

for book_id, config in FIX_PLAN.items():
    json_path = OUTPUT_DIR / book_id / "speaking.json"
    pdf_path = PDF_DIR / config["file"]

    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    doc = fitz.open(str(pdf_path))
    total = doc.page_count
    fixed = 0

    for test_idx, pages in config["tests"].items():
        extracted = None
        for pg in pages:
            if pg >= total:
                continue
            extracted = try_extract(doc, pg, total)
            if extracted:
                print(f"  {book_id} Test {test_idx+1}: Extracted from page {pg+1}")
                break

        if extracted:
            data["tests"][test_idx] = {
                "id": f"{book_id}_test{test_idx+1}",
                "testNumber": test_idx + 1,
                "part1": extracted["part1"],
                "part2": extracted["part2"],
                "part3": extracted.get("part3", {"topics": []}),
            }
            fixed += 1
            p1q = len(extracted["part1"].get("questions", []))
            p2p = len(extracted["part2"].get("prompts", []))
            p3t = len(extracted.get("part3", {}).get("topics", []))
            print(f"    P1={p1q}qs, P2={p2p}ps, P3={p3t}topics, title={extracted['part2']['title'][:60]}")
        else:
            print(f"  {book_id} Test {test_idx+1}: FAILED to extract from pages {pages}")

    doc.close()

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  {book_id}: Fixed {fixed} tests\n")
