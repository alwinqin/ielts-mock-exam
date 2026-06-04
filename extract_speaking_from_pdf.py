#!/usr/bin/env python3
"""Extract official Cambridge IELTS speaking test data from question PDFs.

Strategy:
- cam14, cam17: PyMuPDF text extraction (has text layer)
- cam15, cam16, cam18, cam19: VLM-based extraction (image-only PDFs)
"""
import json
import re
import sys
from pathlib import Path

import fitz

from vlm_client import PDF_DIR, render_jpeg, vlm_call

OUTPUT_DIR = Path(__file__).parent / "data" / "cambridge"


def extract_speaking_pages_text(doc):
    """Find all speaking section start pages in a PDF with text layer."""
    pages = []
    for pg in range(doc.page_count):
        text = doc[pg].get_text()
        if 'SPEAKING' in text and ('PART 1' in text or 'Part 1' in text):
            # Verify this is a test speaking section (not just the intro page)
            if 'You should say' in text or 'Describe a' in text or 'EXAMPLE' in text:
                pages.append(pg)
    return pages


def parse_speaking_section(text):
    """Parse a speaking section text into structured data."""
    result = {"part1": [], "part2": {}, "part3": []}

    # Extract Part 1 questions
    p1_match = re.search(r'PART 1.*?EXAMPLE\n(.+?)(?=PART 2)', text, re.DOTALL)
    if p1_match:
        p1_text = p1_match.group(1)
        # Extract topic name (first line after EXAMPLE)
        lines = p1_text.strip().split('\n')
        topic = lines[0].strip() if lines else ""
        # Extract questions (lines starting with bullet-like markers)
        questions = []
        for line in lines[1:]:
            line = line.strip()
            if line and not line.startswith('PART'):
                # Clean up OCR artifacts
                line = re.sub(r'[®©•⓫]', '', line).strip()
                line = re.sub(r'\s+', ' ', line)
                if len(line) > 10 and ('?' in line or 'Why' in line):
                    questions.append(line)
        result["part1"] = {"topic": topic, "questions": questions}

    # Extract Part 2
    p2_match = re.search(
        r'PART 2\n(.*?)(?=PART 3|You will have to talk)',
        text, re.DOTALL
    )
    if p2_match:
        p2_text = p2_match.group(1)
        lines = [l.strip() for l in p2_text.split('\n') if l.strip()]
        title = lines[0] if lines else ""
        # Find "You should say:" marker for bullet points
        ys_match = re.search(r'You should say:(.*?)(?=You will have|to two minutes|$)', text, re.DOTALL)
        prompts = []
        if ys_match:
            prompt_text = ys_match.group(1)
            for line in prompt_text.strip().split('\n'):
                line = line.strip()
                if line and len(line) > 5:
                    line = re.sub(r'\s+', ' ', line)
                    prompts.append(line)
        result["part2"] = {
            "title": title.strip(),
            "prompts": prompts,
        }

    # Extract Part 3
    p3_match = re.search(r'PART 3\n(.*)', text, re.DOTALL)
    if p3_match:
        p3_text = p3_match.group(1)
        # Parse discussion topics
        topics = []
        # Split by "Example questions:" pattern
        topic_blocks = re.split(r'\n([A-Za-z ]+)\nExample questions:', p3_text)
        # Simpler approach: find all "Example questions:" blocks
        current_topic = None
        for line in p3_text.split('\n'):
            line = line.strip()
            if not line:
                continue
            if 'Example questions' in line:
                continue
            if line[0].isupper() and not line.endswith('?') and len(line.split()) <= 6:
                # This is likely a topic name
                current_topic = line
                topics.append({"topic": current_topic, "questions": []})
            elif line.endswith('?') and current_topic and topics:
                line = re.sub(r'\s+', ' ', line)
                topics[-1]["questions"].append(line)

        if topics:
            result["part3"] = topics
        else:
            result["part3"] = [{"topic": "Discussion", "questions": []}]

    return result


def extract_cam_book_text(book_id):
    """Extract all speaking tests from a book using text-based method."""
    pdf_path = PDF_DIR / f"{book_id}_questions.pdf"
    if not pdf_path.exists():
        print(f"  PDF not found: {pdf_path}")
        return None

    doc = fitz.open(str(pdf_path))
    speaking_pages = extract_speaking_pages_text(doc)

    if len(speaking_pages) < 4:
        print(f"  Warning: only found {len(speaking_pages)} speaking sections (expected 4)")

    tests = []
    for i, pg in enumerate(speaking_pages):
        # Get this page + next page for complete content
        full_text = ""
        for offset in range(2):
            if pg + offset < doc.page_count:
                full_text += doc[pg + offset].get_text() + "\n"

        data = parse_speaking_section(full_text)
        tests.append({
            "id": f"{book_id}_test{i+1}",
            "testNumber": i + 1,
            "part1": data["part1"],
            "part2": data["part2"],
            "part3": {"topics": data["part3"]},
        })
        print(f"    Test {i+1}: Part1={len(data['part1'].get('questions',[]))}qs, "
              f"Part2={len(data['part2'].get('prompts',[]))}prompts, "
              f"Part3={len(data['part3'])}topics")

    doc.close()
    return tests


def extract_cam_book_vlm(book_id):
    """Extract all speaking tests from an image-only book using VLM."""
    pdf_path = PDF_DIR / f"{book_id}_questions.pdf"
    if not pdf_path.exists():
        print(f"  PDF not found: {pdf_path}")
        return None

    doc = fitz.open(str(pdf_path))
    total = doc.page_count

    # For image-only PDFs, we need to find speaking pages differently
    # Sample last 40% of pages (speaking sections are typically there)
    # We'll do a quick scan first to find candidate pages
    print(f"  Scanning {total} pages for speaking sections...")
    speaking_pages = []
    for pg in range(int(total * 0.6), total):
        img_b64 = render_jpeg(doc, pg, dpi=100)
        check = vlm_call(
            img_b64,
            "Does this page contain an IELTS Speaking test section with Part 1 questions? "
            "Look for headings like 'SPEAKING', 'PART 1', and questions about personal topics. "
            "Reply ONLY 'YES' or 'NO'.",
            max_tokens=8,
        )
        if check and 'YES' in check.upper():
            speaking_pages.append(pg)
            print(f"    Found speaking section on page {pg+1}")
        if len(speaking_pages) >= 4:
            break

    if len(speaking_pages) < 4:
        print(f"    Warning: only found {len(speaking_pages)} speaking sections")

    tests = []
    for i, pg in enumerate(speaking_pages):
        img_b64 = render_jpeg(doc, pg, dpi=200)

        # Also capture next page for Part 3
        next_b64 = None
        if pg + 1 < total:
            next_b64 = render_jpeg(doc, pg + 1, dpi=200)

        prompt = """Extract the COMPLETE IELTS Speaking test from this page as structured JSON.

Output exactly this JSON format:
{
  "part1": {
    "topic": "<Part 1 topic name>",
    "questions": ["<question 1>", "<question 2>", "<question 3>", "<question 4>"]
  },
  "part2": {
    "title": "<Describe a ...>",
    "prompts": ["<bullet point 1>", "<bullet point 2>", "<bullet point 3>", "<bullet point 4>"]
  },
  "part3": {
    "topics": [
      {"topic": "<discussion topic 1>", "questions": ["<q1>", "<q2>", "<q3>"]},
      {"topic": "<discussion topic 2>", "questions": ["<q1>", "<q2>", "<q3>"]}
    ]
  }
}

Extract ALL text exactly as printed, preserving the original wording.
For Part 3, there are typically 2 discussion topics with 3-4 questions each.
Output ONLY the JSON, no explanation."""

        result = vlm_call(img_b64, prompt, max_tokens=2048)
        if result:
            try:
                # Try to extract JSON from the response
                json_match = re.search(r'\{[\s\S]*\}', result)
                if json_match:
                    data = json.loads(json_match.group())
                    tests.append({
                        "id": f"{book_id}_test{i+1}",
                        "testNumber": i + 1,
                        "part1": data["part1"],
                        "part2": data["part2"],
                        "part3": data["part3"],
                    })
                    print(f"    Test {i+1}: OK")
                else:
                    print(f"    Test {i+1}: JSON parse failed — no JSON found in response")
            except (json.JSONDecodeError, KeyError) as e:
                print(f"    Test {i+1}: JSON parse failed — {e}")
        else:
            print(f"    Test {i+1}: VLM call failed")

    doc.close()
    return tests


def main():
    book_id = sys.argv[1] if len(sys.argv) > 1 else "cam14"
    method = sys.argv[2] if len(sys.argv) > 2 else "text"

    print(f"Extracting speaking data for {book_id} (method: {method})")

    if method == "text":
        tests = extract_cam_book_text(book_id)
    else:
        tests = extract_cam_book_vlm(book_id)

    if not tests:
        print("No tests extracted.")
        return

    # Write to Cambridge speaking.json (using cam17-style format)
    output = {
        "id": book_id,
        "title": f"Cambridge IELTS {book_id[3:]} Speaking",
        "tests": tests,
    }

    out_path = OUTPUT_DIR / book_id / "speaking.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"  Saved {len(tests)} tests to {out_path}")


if __name__ == "__main__":
    main()
