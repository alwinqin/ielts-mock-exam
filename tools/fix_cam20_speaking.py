#!/usr/bin/env python3
"""Fix cam20 speaking data using individual test PDFs."""
import json
import re
from pathlib import Path

import fitz

from vlm_client import PDF_DIR, render_jpeg, vlm_call

OUTPUT_DIR = Path(__file__).parent / "data" / "cambridge"


def extract_from_single_pdf(pdf_path):
    """Extract speaking test from a single-test PDF."""
    doc = fitz.open(str(pdf_path))
    total = doc.page_count

    # Find speaking page - scan from 60% onward
    speaking_page = None
    for pg in range(int(total * 0.5), total):
        img_b64 = render_jpeg(doc, pg, dpi=80)
        check = vlm_call(
            img_b64,
            "Does this page contain an IELTS SPEAKING test with Part 1 interview questions? "
            "Look for personal questions like 'Do you...', 'How often...', 'What do you think...'. "
            "Reply ONLY 'YES' or 'NO'.",
            max_tokens=8,
        )
        if check and "YES" in check.upper():
            speaking_page = pg
            break

    if speaking_page is None:
        # Try text-based detection
        for pg in range(total):
            text = doc[pg].get_text()
            if "SPEAKING" in text.upper() and "PART 1" in text.upper():
                speaking_page = pg
                break

    if speaking_page is None:
        doc.close()
        return None

    print(f"    Speaking on page {speaking_page+1}/{total}")

    # Extract with VLM
    img_b64 = render_jpeg(doc, speaking_page, dpi=200)
    next_b64 = render_jpeg(doc, speaking_page + 1, dpi=200) if speaking_page + 1 < total else None

    prompt = """Extract the COMPLETE IELTS Speaking test from this page as structured JSON.

Output exactly this JSON:
{
  "part1": {
    "topic": "<Part 1 topic - short phrase>",
    "questions": ["<q1>", "<q2>", "<q3>", "<q4>"]
  },
  "part2": {
    "title": "<Describe a ...>",
    "prompts": ["<bullet 1>", "<bullet 2>", "<bullet 3>", "<bullet 4 including 'and explain...'>"]
  },
  "part3": {
    "topics": [
      {"topic": "<discussion topic 1>", "questions": ["<q1>", "<q2>", "<q3>"]},
      {"topic": "<discussion topic 2>", "questions": ["<q1>", "<q2>", "<q3>"]}
    ]
  }
}

Copy ALL text EXACTLY as printed. Do not paraphrase.
Part 1: exactly 4 interview questions (personal topic)
Part 2: Cue card with "Describe..." + exactly 4 bullet prompts
Part 3: exactly 2 discussion topics with 3-4 questions each
Output ONLY valid JSON, no explanation."""

    images = [img_b64]
    if next_b64:
        images.append(next_b64)

    result = vlm_call(images, prompt, max_tokens=2048)
    doc.close()

    if not result:
        return None

    json_match = re.search(r'\{[\s\S]*\}', result)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            return None
    return None


def fix_cam20():
    """Fix cam20 by extracting from individual test PDFs."""
    json_path = OUTPUT_DIR / "cam20" / "speaking.json"
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    fixed = 0
    for i in range(4):
        test_num = i + 1
        pdf_path = PDF_DIR / f"cam20_test{test_num}_questions.pdf"

        if not pdf_path.exists():
            print(f"  Test {test_num}: PDF not found - skipping")
            continue

        stored = data["tests"][i]
        p2 = stored.get("part2", {})
        p3 = stored.get("part3", {})
        p3_topics = p3.get("topics", [])

        needs_full_extract = not p2.get("title") or not p2.get("prompts")
        needs_p3 = len(p3_topics) < 2
        needs_p1_topic = not stored.get("part1", {}).get("topic")

        if not needs_full_extract and not needs_p3 and not needs_p1_topic:
            print(f"  Test {test_num}: OK")
            continue

        issues = []
        if needs_full_extract:
            issues.append("Part2 missing")
        if needs_p3:
            issues.append(f"Part3={len(p3_topics)}topics")
        if needs_p1_topic:
            issues.append("Part1 topic missing")

        print(f"  Test {test_num}: {', '.join(issues)} - extracting...")

        extracted = extract_from_single_pdf(pdf_path)

        if extracted:
            if needs_full_extract:
                data["tests"][i]["part1"] = extracted.get("part1", data["tests"][i]["part1"])
                data["tests"][i]["part2"] = extracted.get("part2", data["tests"][i]["part2"])
                data["tests"][i]["part3"] = extracted.get("part3", data["tests"][i]["part3"])
                fixed += 1
                print(f"    ✓ Full extraction: P1={len(extracted.get('part1',{}).get('questions',[]))}qs, "
                      f"P2={len(extracted.get('part2',{}).get('prompts',[]))}prompts, "
                      f"P3={len(extracted.get('part3',{}).get('topics',[]))}topics")
            else:
                if needs_p1_topic and extracted.get("part1", {}).get("topic"):
                    data["tests"][i]["part1"]["topic"] = extracted["part1"]["topic"]
                    print(f"    ✓ Added P1 topic: {extracted['part1']['topic']}")
                if needs_p3:
                    new_topics = extracted.get("part3", {}).get("topics", [])
                    if len(new_topics) >= 2:
                        data["tests"][i]["part3"]["topics"] = new_topics
                        fixed += 1
                        print(f"    ✓ Updated P3: {len(new_topics)} topics")
        else:
            print(f"    ✗ Extraction failed")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Saved. Fixed: {fixed} tests")
    return fixed


if __name__ == "__main__":
    fix_cam20()
