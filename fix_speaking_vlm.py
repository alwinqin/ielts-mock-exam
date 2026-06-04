#!/usr/bin/env python3
"""Fix VLM-extracted speaking data that captured listening content instead of speaking.

Strategy: Rescan the full PDF to find correct speaking pages, then re-extract.
"""
import json
import re
import sys
from pathlib import Path

import fitz

from vlm_client import PDF_DIR, render_jpeg, vlm_call

OUTPUT_DIR = Path(__file__).parent / "data" / "cambridge"


def find_speaking_pages(book_id):
    """Scan ALL pages of a PDF to find the 4 speaking sections."""
    pdf_path = PDF_DIR / f"{book_id}_questions.pdf"
    if not pdf_path.exists():
        print(f"  PDF not found: {pdf_path}")
        return []

    doc = fitz.open(str(pdf_path))
    total = doc.page_count
    print(f"  Scanning {total} pages in {book_id}_questions.pdf...")

    speaking_pages = []
    # Scan every page from the second half (speaking is typically after listening/reading/writing)
    for pg in range(int(total * 0.4), total):
        img_b64 = render_jpeg(doc, pg, dpi=80)
        check = vlm_call(
            img_b64,
            "Look at this page carefully. Is this an IELTS SPEAKING test page with Part 1 interview questions "
            "(personal questions like 'Do you like...', 'How often do you...', 'What do you think about...')? "
            "It should NOT be a listening test (with gap-fill answers like '1 .........'), "
            "NOT a reading test, and NOT a writing test. "
            "The page should have headings like 'SPEAKING', 'PART 1', and questions about the candidate's life/opinions. "
            "Reply ONLY 'YES' or 'NO'.",
            max_tokens=16,
        )
        if check and "YES" in check.upper() and "NO" not in check.upper().replace("NOTE", ""):
            speaking_pages.append(pg)
            print(f"    Found speaking page {pg+1}")
            if len(speaking_pages) >= 4:
                break

    doc.close()
    return speaking_pages


def extract_speaking_test_vlm(book_id, test_index, page_num):
    """Extract a single speaking test using VLM from a specific page."""
    pdf_path = PDF_DIR / f"{book_id}_questions.pdf"
    doc = fitz.open(str(pdf_path))
    total = doc.page_count

    img_b64 = render_jpeg(doc, page_num, dpi=200)
    next_b64 = render_jpeg(doc, page_num + 1, dpi=200) if page_num + 1 < total else None
    third_b64 = render_jpeg(doc, page_num + 2, dpi=200) if page_num + 2 < total else None

    prompt = """Extract the COMPLETE IELTS Speaking test from this page as structured JSON.

This is an official Cambridge IELTS book. The page should contain:
- PART 1: 4 interview questions about a specific topic (e.g., hobbies, habits, preferences)
- PART 2: A cue card with "Describe a..." and 4 bullet points starting with "what/why/how/and explain"
- PART 3: 2 discussion topics with 3-4 questions each (abstract, opinion-based questions)

Output exactly this JSON format:
{
  "part1": {
    "topic": "<Part 1 topic name - a short phrase like 'Shopping' or 'Music'>",
    "questions": ["<question 1 exactly as printed>", "<question 2>", "<question 3>", "<question 4>"]
  },
  "part2": {
    "title": "<Describe a ... exactly as printed>",
    "prompts": ["<bullet point 1>", "<bullet point 2>", "<bullet point 3>", "<bullet point 4 including 'and explain...'>"]
  },
  "part3": {
    "topics": [
      {"topic": "<discussion topic 1 name>", "questions": ["<q1>", "<q2>", "<q3>"]},
      {"topic": "<discussion topic 2 name>", "questions": ["<q1>", "<q2>", "<q3>"]}
    ]
  }
}

CRITICAL RULES:
1. Extract the EXACT text from the page - do not paraphrase or summarize
2. Each question should be copied word-for-word from the page
3. Part 1 must have exactly 4 questions (the exact number shown on the page)
4. Part 2 must have exactly 4 bullet prompts
5. Part 3 must have exactly 2 topics with 3-4 questions each
6. If Part 3 continues on a next page, the second image shows it
7. Do NOT include listening test content (gap-fills, multiple choice options A/B/C)
8. Do NOT include reading test content
9. Output ONLY valid JSON, no explanation whatsoever"""

    images = [img_b64]
    if next_b64:
        images.append(next_b64)
    if third_b64:
        images.append(third_b64)

    result = vlm_call(images, prompt, max_tokens=2048)

    doc.close()

    if not result:
        return None

    # Extract JSON from response
    json_match = re.search(r'\{[\s\S]*\}', result)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError as e:
            print(f"      JSON parse error: {e}")
            print(f"      Raw: {result[:200]}...")
            return None
    return None


def fix_book(book_id, test_indices=None):
    """Fix speaking data for a book. If test_indices is None, fix all tests."""
    json_path = OUTPUT_DIR / book_id / "speaking.json"
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    # Find correct speaking pages
    speaking_pages = find_speaking_pages(book_id)

    if len(speaking_pages) < 4:
        print(f"  WARNING: Only found {len(speaking_pages)} speaking pages (expected 4)")
        # Try to find more by scanning all pages
        pdf_path = PDF_DIR / f"{book_id}_questions.pdf"
        doc = fitz.open(str(pdf_path))
        # Scan pages we might have missed
        for pg in range(doc.page_count):
            if pg in speaking_pages:
                continue
            if len(speaking_pages) >= 4:
                break
            # Check if page has SPEAKING header via text
            text = doc[pg].get_text()
            if "SPEAKING" in text.upper() and ("PART 1" in text.upper()):
                speaking_pages.append(pg)
                print(f"    Text-based found speaking page {pg+1}")
        doc.close()
        speaking_pages = sorted(set(speaking_pages))

    # Ensure we have 4 pages (pad with the last found page + offsets if needed)
    while len(speaking_pages) < 4 and speaking_pages:
        speaking_pages.append(speaking_pages[-1] + 2)

    print(f"  Speaking pages: {[p+1 for p in speaking_pages[:4]]}")

    tests_to_fix = test_indices if test_indices is not None else range(len(data["tests"]))
    fixed_count = 0

    for i in tests_to_fix:
        if i >= len(speaking_pages) or i >= len(data["tests"]):
            continue

        stored = data["tests"][i]
        # Check if this test has corrupt data (listening content instead of speaking)
        p1 = stored.get("part1", {})
        p1_qs = p1.get("questions", [])
        is_corrupt = False

        # Detect listening content
        if p1_qs:
            first_q = p1_qs[0] if p1_qs else ""
            # Listening gap-fills have patterns like "1 ............................"
            if re.search(r'\d+\s+\.{3,}', first_q):
                is_corrupt = True
            # Listening content mentions specific test structures
            if re.search(r'Questions?\s+\d+.*\d+', first_q):
                is_corrupt = True
            # Listening content with form-filling
            if any(w in first_q.lower() for w in ['coordinator', 'ranger', 'teaching assistant', 'good morning']):
                is_corrupt = True

        # Also check Part 2
        p2 = stored.get("part2", {})
        p2_title = p2.get("title", "")
        if p2_title and re.search(r'Questions?\s+\d+', p2_title):
            is_corrupt = True

        # Check for missing data
        is_missing = not p2.get("prompts") or not p2_title

        if is_corrupt or is_missing:
            print(f"  Test {i+1}: {'CORRUPT (listening content)' if is_corrupt else 'MISSING data'} - re-extracting...")
            page_num = speaking_pages[i]
            extracted = extract_speaking_test_vlm(book_id, i, page_num)

            if extracted and extracted.get("part2", {}).get("title"):
                # Verify it's not listening content again
                new_p1_qs = extracted.get("part1", {}).get("questions", [])
                if new_p1_qs and not re.search(r'\d+\s+\.{3,}', new_p1_qs[0]):
                    data["tests"][i] = {
                        "id": f"{book_id}_test{i+1}",
                        "testNumber": i + 1,
                        "part1": extracted["part1"],
                        "part2": extracted["part2"],
                        "part3": extracted.get("part3", {"topics": []}),
                    }
                    fixed_count += 1
                    print(f"    ✓ Fixed Test {i+1}: P1={len(extracted['part1'].get('questions',[]))}qs, "
                          f"P2={len(extracted['part2'].get('prompts',[]))}prompts, "
                          f"P3={len(extracted.get('part3', {}).get('topics', []))}topics")
                else:
                    # Try next page
                    print(f"    Still got listening content, trying page {page_num+2}...")
                    extracted2 = extract_speaking_test_vlm(book_id, i, page_num + 1)
                    if extracted2 and extracted2.get("part2", {}).get("title"):
                        new_p1_qs2 = extracted2.get("part1", {}).get("questions", [])
                        if new_p1_qs2 and not re.search(r'\d+\s+\.{3,}', new_p1_qs2[0]):
                            data["tests"][i] = {
                                "id": f"{book_id}_test{i+1}",
                                "testNumber": i + 1,
                                "part1": extracted2["part1"],
                                "part2": extracted2["part2"],
                                "part3": extracted2.get("part3", {"topics": []}),
                            }
                            fixed_count += 1
                            print(f"    ✓ Fixed Test {i+1} from page {page_num+2}")
                        else:
                            print(f"    ✗ Still got invalid content")
                    else:
                        print(f"    ✗ Extraction failed")
            else:
                print(f"    ✗ Extraction failed or returned empty data")
        else:
            p1_topic = p1.get("topic", "")
            p3 = stored.get("part3", {})
            p3_topics = p3.get("topics", [])
            p3_issues = len(p3_topics) < 2

            # Check Part 1 topic missing
            p1_topic_missing = not p1_topic

            if p3_issues or p1_topic_missing:
                issues = []
                if p3_issues:
                    issues.append(f"P3={len(p3_topics)}topics")
                if p1_topic_missing:
                    issues.append("P1 topic missing")
                print(f"  Test {i+1}: Minor issues ({', '.join(issues)}) - re-extracting Part 3...")
                page_num = speaking_pages[i]
                extracted = extract_speaking_test_vlm(book_id, i, page_num)

                if extracted:
                    # Only update missing fields
                    if p1_topic_missing and extracted.get("part1", {}).get("topic"):
                        data["tests"][i]["part1"]["topic"] = extracted["part1"]["topic"]
                        print(f"    ✓ Added Part 1 topic: {extracted['part1']['topic']}")

                    if p3_issues:
                        new_topics = extracted.get("part3", {}).get("topics", [])
                        if len(new_topics) >= 2:
                            data["tests"][i]["part3"]["topics"] = new_topics
                            fixed_count += 1
                            print(f"    ✓ Updated Part 3: {len(new_topics)} topics")
                        elif len(new_topics) == 2:
                            data["tests"][i]["part3"]["topics"] = new_topics
                            fixed_count += 1
                            print(f"    ✓ Updated Part 3: {len(new_topics)} topics")

    # Save updated data
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"  Fixed {fixed_count} tests, saved to {json_path}")
    return fixed_count


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 fix_speaking_vlm.py <book_id> [test_index]")
        print("       python3 fix_speaking_vlm.py all")
        return

    target = sys.argv[1]

    if target == "all":
        books_to_fix = ["cam18", "cam19", "cam20"]
        total_fixed = 0
        for book_id in books_to_fix:
            print(f"\n{'='*50}")
            print(f"Fixing {book_id}...")
            print(f"{'='*50}")
            total_fixed += fix_book(book_id)
        print(f"\nTotal tests fixed: {total_fixed}")
    else:
        book_id = target
        test_idx = int(sys.argv[2]) if len(sys.argv) > 2 else None
        test_indices = [test_idx] if test_idx is not None else None
        fix_book(book_id, test_indices)


if __name__ == "__main__":
    main()
