#!/usr/bin/env python3
"""Targeted extraction of missing/corrupt speaking tests using nearby page scanning."""
import json, re, sys
from pathlib import Path
import fitz
from vlm_client import PDF_DIR, render_jpeg, vlm_call

OUTPUT_DIR = Path(__file__).parent / "data" / "cambridge"


def extract_one_test(doc, page_num, total_pages):
    """Try to extract a speaking test from a specific page. Returns parsed dict or None."""
    # Try current page + next 2 pages
    images = [render_jpeg(doc, page_num, dpi=200)]
    if page_num + 1 < total_pages:
        images.append(render_jpeg(doc, page_num + 1, dpi=200))
    if page_num + 2 < total_pages:
        images.append(render_jpeg(doc, page_num + 2, dpi=200))

    prompt = """Extract the IELTS Speaking test from this image into JSON.

Format:
{
  "part1": {"topic": "topic name", "questions": ["q1", "q2", "q3", "q4"]},
  "part2": {"title": "Describe a ...", "prompts": ["bullet1", "bullet2", "bullet3", "bullet4"]},
  "part3": {"topics": [{"topic": "topic1", "questions": ["q1","q2","q3"]}, {"topic": "topic2", "questions": ["q1","q2","q3"]}]}
}

CRITICAL: Copy text EXACTLY as printed. Part 1 must have 4 interview questions. Part 2 must have 4 bullet prompts. Part 3 must have 2 topics with 3-4 questions each. If you see listening test content (gap-fills, A/B/C choices), report only the SPEAKING section. Output ONLY the JSON object."""

    result = vlm_call(images, prompt, max_tokens=2048)
    if not result:
        return None

    m = re.search(r'\{[\s\S]*\}', result)
    if not m:
        return None
    try:
        data = json.loads(m.group())
        # Validate it's speaking (not listening)
        p1_qs = data.get("part1", {}).get("questions", [])
        if p1_qs and not re.search(r'\d+\s+\.{3,}', str(p1_qs[0])):
            if data.get("part2", {}).get("title", "").startswith("Describe"):
                return data
    except json.JSONDecodeError:
        pass
    return None


def fix_book_smart(book_id):
    """Smart fix: scan around known speaking pages for missing tests."""
    json_path = OUTPUT_DIR / book_id / "speaking.json"
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    pdf_path = PDF_DIR / f"{book_id}_questions.pdf"
    doc = fitz.open(str(pdf_path))
    total = doc.page_count

    # First find ALL pages in the PDF that might be speaking pages
    # Use coarse scan (80 DPI) of every 2nd page from 40% onward
    candidate_pages = []
    print(f"  Coarse scan for speaking pages...")
    for pg in range(int(total * 0.3), total, 2):
        img = render_jpeg(doc, pg, dpi=80)
        check = vlm_call(
            img,
            "Does this page show an IELTS Speaking test with an interview topic (Part 1) like hobbies/family/work/studies? "
            "Reply 'YES' or 'NO' only.",
            max_tokens=8
        )
        if check and "YES" in check.upper() and "NO" not in check.upper().replace("NOTE", "").replace("NOSE", ""):
            candidate_pages.append(pg)
            print(f"    Candidate: page {pg+1}")

    print(f"  Candidates: {[p+1 for p in candidate_pages]}")

    fixed = 0
    for i in range(min(4, len(data["tests"]))):
        stored = data["tests"][i]
        p2 = stored.get("part2", {})
        p2_title = p2.get("title", "")
        p2_prompts = p2.get("prompts", [])
        p1_topic = stored.get("part1", {}).get("topic", "")
        p3_topics = stored.get("part3", {}).get("topics", [])

        # Check if corrupt
        is_corrupt = False
        if p2_prompts:
            first_prompt = p2_prompts[0] if p2_prompts else ""
            if re.search(r'Questions?\s+\d+.*\d+', p2_title) or re.search(r'Questions?\s+\d+.*\d+', first_prompt):
                is_corrupt = True
            if re.search(r'Choose.*letters?.*A.*E', first_prompt):
                is_corrupt = True
        if p2_title and re.search(r'Questions?\s+\d+.*\d+', p2_title):
            is_corrupt = True

        needs_fix = is_corrupt or not p2_title or not p2_prompts or len(p3_topics) < 2 or not p1_topic

        if not needs_fix:
            print(f"  Test {i+1}: OK")
            continue

        reasons = []
        if is_corrupt: reasons.append("corrupt")
        if not p2_title or not p2_prompts: reasons.append("missing Part2")
        if len(p3_topics) < 2: reasons.append(f"Part3={len(p3_topics)}topics")
        if not p1_topic: reasons.append("no P1 topic")
        print(f"  Test {i+1}: {', '.join(reasons)} - extracting...")

        # Try to extract from each candidate page near where we expect this test
        extracted = None
        # Use candidate pages or nearby pages
        pages_to_try = []
        if i < len(candidate_pages):
            pages_to_try.append(candidate_pages[i])
            # Also try +1
            pages_to_try.append(candidate_pages[i] + 1)
        # Fallback: try a range of pages
        for fallback in range(int(total * 0.3 + i * 15), min(int(total * 0.3 + (i+1) * 18), total)):
            if fallback not in pages_to_try:
                pages_to_try.append(fallback)

        for pg in pages_to_try:
            if pg >= total:
                continue
            extracted = extract_one_test(doc, pg, total)
            if extracted:
                print(f"    ✓ Extracted from page {pg+1}")
                break

        if extracted:
            data["tests"][i] = {
                "id": f"{book_id}_test{i+1}",
                "testNumber": i + 1,
                "part1": extracted["part1"],
                "part2": extracted["part2"],
                "part3": extracted.get("part3", {"topics": []}),
            }
            fixed += 1
            p1 = extracted.get("part1", {})
            p2 = extracted.get("part2", {})
            p3 = extracted.get("part3", {}).get("topics", [])
            print(f"    P1={len(p1.get('questions',[]))}qs, P2={len(p2.get('prompts',[]))}prompts, P3={len(p3)}topics")
        else:
            print(f"    ✗ Could not extract from any page")

    doc.close()

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Fixed: {fixed} tests")
    return fixed


def main():
    book_id = sys.argv[1] if len(sys.argv) > 1 else "cam18"
    fix_book_smart(book_id)


if __name__ == "__main__":
    main()
