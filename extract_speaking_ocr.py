#!/usr/bin/env python3
"""Extract speaking data via VLM OCR (transcribe text, parse locally)."""
import json, re, sys
from pathlib import Path
import fitz
from vlm_client import PDF_DIR, render_jpeg, vlm_call

OUTPUT_DIR = Path(__file__).parent / "data" / "cambridge"


def ocr_page(doc, page_num, total):
    """Use VLM to transcribe all text on a page."""
    if page_num >= total:
        return ""

    img = render_jpeg(doc, page_num, dpi=200)
    next_img = render_jpeg(doc, page_num + 1, dpi=200) if page_num + 1 < total else None
    images = [img] + ([next_img] if next_img else [])

    prompt = """Transcribe ALL text from this IELTS Speaking test page. Include ALL questions, headings, bullet points, and instructions.
Just transcribe the text exactly as it appears, preserving the layout and order. Do not summarize or paraphrase.
Include: PART 1 heading, topic, all 4 questions, PART 2 heading, cue card title, all bullet points, PART 3 heading, all discussion topics and questions."""

    result = vlm_call(images, prompt, max_tokens=2048)
    return result if result else ""


def parse_transcript(text, test_id, test_num):
    """Parse transcribed speaking test text into structured data."""
    result = {
        "id": test_id,
        "testNumber": test_num,
        "part1": {"topic": "", "questions": []},
        "part2": {"title": "", "prompts": []},
        "part3": {"topics": []},
    }

    lines = text.strip().split('\n')

    # Find Part 1 section
    in_part1 = in_part2 = in_part3 = False
    current_p3_topic = None
    p1_lines = []
    p2_lines = []
    p3_sections = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        upper = line.upper()

        # Detect section boundaries
        if 'PART 1' in upper and not in_part2 and not in_part3:
            in_part1 = True
            continue
        elif 'PART 2' in upper:
            in_part1 = False
            in_part2 = True
            continue
        elif 'PART 3' in upper:
            in_part2 = False
            in_part3 = True
            continue

        if in_part1:
            p1_lines.append(line)
        elif in_part2:
            p2_lines.append(line)
        elif in_part3:
            # Check if this line is a topic heading (short, capitalized, not a question)
            words = line.split()
            is_question = '?' in line
            is_topic = (len(words) <= 8 and not is_question and
                       (line[0].isupper() or line.isupper()) and
                       not line.startswith(('what', 'why', 'how', 'when', 'where', 'who', 'do', 'is', 'are', 'can', 'should', 'will', 'would', 'could', 'has', 'have', 'did', 'does')))

            if is_topic and not current_p3_topic:
                current_p3_topic = {"topic": line, "questions": []}
                p3_sections.append(current_p3_topic)
            elif is_topic and current_p3_topic and current_p3_topic["questions"]:
                current_p3_topic = {"topic": line, "questions": []}
                p3_sections.append(current_p3_topic)
            elif '?' in line or len(line) > 20:
                # This is a question
                if current_p3_topic is None:
                    current_p3_topic = {"topic": "Discussion", "questions": []}
                    p3_sections.append(current_p3_topic)
                # Clean up question
                q = re.sub(r'\s+', ' ', line)
                current_p3_topic["questions"].append(q)

    # Parse Part 1
    if p1_lines:
        # First non-empty line is usually the topic
        result["part1"]["topic"] = p1_lines[0]
        for line in p1_lines[1:]:
            if '?' in line or ('why' in line.lower() and len(line) > 15):
                q = re.sub(r'\s+', ' ', line).strip()
                result["part1"]["questions"].append(q)
        # Limit to 4 questions
        if len(result["part1"]["questions"]) > 4:
            # Remove non-question lines
            result["part1"]["questions"] = [q for q in result["part1"]["questions"] if '?' in q or 'why' in q.lower()][:4]
        # If topic looks like a question, it's not a topic
        if '?' in result["part1"]["topic"]:
            result["part1"]["questions"].insert(0, result["part1"]["topic"])
            result["part1"]["topic"] = result["part1"]["topic"].split('?')[0].strip()[:50]

    # Parse Part 2
    if p2_lines:
        # First line is the cue card title ("Describe a ...")
        title_candidates = [l for l in p2_lines if l.lower().startswith('describe')]
        if title_candidates:
            result["part2"]["title"] = title_candidates[0]
        else:
            result["part2"]["title"] = p2_lines[0]

        # Find bullet points
        for line in p2_lines:
            clean = re.sub(r'^[•\-\*\s]+', '', line).strip()
            if clean.lower().startswith(('what', 'why', 'how', 'when', 'where', 'who', 'and explain', 'explain')):
                if clean not in result["part2"]["prompts"]:
                    result["part2"]["prompts"].append(clean)
            elif len(clean) > 10 and (clean.lower().startswith('you should say') or 'you should' in clean.lower()):
                continue  # Skip instructions

    # Parse Part 3
    if p3_sections:
        # Merge adjacent topics with very few questions
        merged = []
        for section in p3_sections:
            if merged and len(merged[-1]["questions"]) < 2:
                merged[-1]["questions"].extend(section["questions"])
                if section["topic"] != "Discussion":
                    merged[-1]["topic"] = section["topic"]
            else:
                merged.append(section)

        # Limit to 2 topics with reasonable questions
        result["part3"]["topics"] = merged[:2]
        for topic in result["part3"]["topics"]:
            topic["questions"] = topic["questions"][:4]

    return result


def main():
    book_id = sys.argv[1] if len(sys.argv) > 1 else "cam18"

    if book_id == "cam20":
        # Handle individual test PDFs
        results = []
        for test_num in range(1, 5):
            pdf_path = PDF_DIR / f"cam20_test{test_num}_questions.pdf"
            if not pdf_path.exists():
                continue

            doc = fitz.open(str(pdf_path))
            total = doc.page_count

            # Find speaking page - scan last 12 pages
            speaking_page = None
            for pg in range(max(0, total - 12), total):
                img = render_jpeg(doc, pg, dpi=80)
                check = vlm_call(img, "Does this page contain an IELTS SPEAKING test with Part 1 interview questions? Reply YES or NO.", max_tokens=8)
                if check and 'YES' in check.upper():
                    speaking_page = pg
                    break

            if speaking_page is None:
                print(f"cam20 Test {test_num}: No speaking page found")
                doc.close()
                continue

            print(f"cam20 Test {test_num}: OCR from page {speaking_page+1}/{total}...")
            transcript = ocr_page(doc, speaking_page, total)
            doc.close()

            if transcript:
                parsed = parse_transcript(transcript, f"cam20_test{test_num}", test_num)
                results.append(parsed)
                print(f"  P1={len(parsed['part1']['questions'])}qs, P2={len(parsed['part2']['prompts'])}ps, P3={len(parsed['part3']['topics'])}topics")
            else:
                print(f"  OCR failed")

        if results:
            json_path = OUTPUT_DIR / "cam20" / "speaking.json"
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump({
                    "id": "cam20",
                    "title": "Cambridge IELTS 20 Speaking",
                    "tests": results
                }, f, ensure_ascii=False, indent=2)
            print(f"Saved {len(results)} tests")
    else:
        pdf_path = PDF_DIR / f"{book_id}_questions.pdf"
        doc = fitz.open(str(pdf_path))
        total = doc.page_count

        # We need to fix specific tests. Find speaking pages.
        # Use text search first, then VLM
        speaking_pages = []
        for pg in range(total):
            text = doc[pg].get_text()
            if 'SPEAKING' in text.upper() and 'PART 1' in text.upper():
                speaking_pages.append(pg)

        if len(speaking_pages) < 4:
            # VLM scan - check every 3rd page from 30% onward
            print(f"Text found {len(speaking_pages)} pages, VLM scanning...")
            for pg in range(int(total * 0.3), total, 3):
                if pg in speaking_pages:
                    continue
                img = render_jpeg(doc, pg, dpi=60)
                check = vlm_call(img, "Does this page have an IELTS SPEAKING test heading? Reply YES or NO only.", max_tokens=8)
                if check and 'YES' in check.upper():
                    speaking_pages.append(pg)
                    print(f"  VLM found page {pg+1}")
                if len(speaking_pages) >= 4:
                    break

        speaking_pages = sorted(set(speaking_pages))[:4]
        print(f"Speaking pages: {[p+1 for p in speaking_pages]}")

        if len(speaking_pages) < 4:
            print(f"WARNING: Only found {len(speaking_pages)} pages")
            doc.close()
            return

        # Load existing data
        json_path = OUTPUT_DIR / book_id / "speaking.json"
        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)

        fixed = 0
        for i in range(min(4, len(data["tests"]))):
            stored = data["tests"][i]
            p2 = stored.get("part2", {})
            p2_title = p2.get("title", "")
            is_corrupt = bool(p2_title and re.search(r'Questions?\s+\d+', p2_title))

            if not is_corrupt and p2_title and p2.get("prompts"):
                print(f"Test {i+1}: OK")
                continue

            print(f"Test {i+1}: {'CORRUPT' if is_corrupt else 'MISSING'} — extracting from page {speaking_pages[i]+1}...")
            transcript = ocr_page(doc, speaking_pages[i], total)

            if transcript:
                parsed = parse_transcript(transcript, f"{book_id}_test{i+1}", i + 1)
                if parsed["part2"]["title"] and parsed["part2"]["prompts"]:
                    data["tests"][i] = parsed
                    fixed += 1
                    print(f"  ✓ P1={len(parsed['part1']['questions'])}qs, P2={len(parsed['part2']['prompts'])}ps, P3={len(parsed['part3']['topics'])}topics")
                    print(f"    Title: {parsed['part2']['title'][:80]}")
                else:
                    print(f"  ✗ Parsed but missing Part 2 data")
            else:
                print(f"  ✗ OCR failed")

        doc.close()

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Fixed {fixed} tests")


if __name__ == "__main__":
    main()
