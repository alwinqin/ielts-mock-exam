#!/usr/bin/env python3
"""Batch OCR extraction of listening question content from image-based PDFs.

For cam15, cam16, cam18, cam19, cam20 — the PDFs are scanned images.
Uses Tesseract OCR to extract text, then parses MC and fill-blank content.

Strategy:
1. From TOC, find test starting pages
2. OCR pages between each test start and the next test (or reading section)
3. Identify listening sections by "PART X Questions" headers
4. Parse MC and fill-blank questions
5. Match to JSON by test number and section number
6. Update listening.json files
"""

import json
import os
import re
import io
import fitz
import pytesseract
from PIL import Image

DATA_DIR = "data/cambridge"
PDF_DIR = os.path.join(DATA_DIR, "pdf")

# TOC page numbers (0-indexed) for each book: list of test start pages
TOC = {
    "cam15": {"test_starts": [10, 31, 52, 74], "total_pages": 146},
    "cam16": {"test_starts": [10, 32, 55, 76], "total_pages": 144},
    "cam18": {"test_starts": [10, 32, 55, 78], "total_pages": 147},
    "cam19": {"test_starts": [10, 33, 55, 78], "total_pages": 139},
}


def ocr_page(doc, page_num, dpi=200):
    """OCR a single PDF page, return text."""
    page = doc[page_num]
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat)
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    return pytesseract.image_to_string(img)


def find_listening_sections(doc, test_start, next_test_start):
    """OCR pages between test_start and next_test_start, extract listening sections.

    Returns dict: {section_num: raw_text}
    """
    sections = {}
    current_section = None
    current_text_lines = []

    end_page = next_test_start if next_test_start else min(test_start + 20, doc.page_count)

    for pg in range(test_start - 1, end_page):
        if pg >= doc.page_count:
            break

        text = ocr_page(doc, pg)
        lines = text.split('\n')

        for line in lines:
            s = line.strip()

            # Detect section headers: "PART 1 Questions 1-10" or "PART 2 Questions 11-20"
            part_match = re.search(r'PART\s+(\d+)\s+Questions?\s+(\d+)', s, re.IGNORECASE)
            if part_match:
                # Save previous section
                if current_section is not None and current_text_lines:
                    sections[current_section] = '\n'.join(current_text_lines)

                current_section = int(part_match.group(1))
                current_text_lines = [s]
                continue

            # Stop at Reading section
            if re.match(r'^\s*READING\s*(PASSAGE|SECTION)?\s*\d*', s, re.IGNORECASE):
                if current_section is not None and current_text_lines:
                    sections[current_section] = '\n'.join(current_text_lines)
                return sections

            # Stop at next test
            if re.match(r'^\s*Test\s+\d+\s*$', s, re.IGNORECASE) and current_text_lines:
                # Might be the start of next test
                pass

            if current_section is not None:
                current_text_lines.append(s)

    # Save last section
    if current_section is not None and current_text_lines:
        sections[current_section] = '\n'.join(current_text_lines)

    return sections


def parse_mc_ocr(text):
    """Parse MC questions from OCR text.

    Handles two formats:
    Format A (cam14): "21 question stem\\nA opt\\nB opt\\nC opt\\n22 stem..."
    Format B (cam15+): Question numbers listed at top, then alternating stem/options:
        "11\\n12\\n13\\n14\\n<topic>\\nstem1\\nA opt\\nB opt\\nC opt\\nstem2..."
    """
    questions = []
    lines = text.split('\n')

    # --- Try Format A first: numbered stems ---
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        qm = re.match(r'^(\d{1,2})\s{1,3}([A-Z].+)', s)
        if qm:
            q_num = int(qm.group(1))
            if 1 <= q_num <= 40:
                stem = qm.group(2)
                options = []
                i += 1
                while i < len(lines):
                    ns = lines[i].strip()
                    if re.match(r'^(\d{1,2}\s{1,3}[A-Z]|Questions?\s+\d+|PART\s+\d)', ns):
                        break
                    om = re.match(r'^([A-H])\s{1,3}(.+)', ns)
                    if om:
                        options.append(f"{om.group(1)}. {om.group(2).strip()}")
                    elif ns and options:
                        options[-1] += ' ' + ns
                    i += 1
                if options:
                    questions.append({'number': q_num, 'stem': stem, 'options': options})
                continue
        i += 1

    if questions:
        return questions

    # --- Try Format B: alternating stems and options ---
    # First, find question numbers from header
    q_nums = []
    for line in lines:
        s = line.strip()
        m = re.search(r'Questions?\s+(\d+)[-=](\d+)', s)
        if m:
            q_start, q_end = int(m.group(1)), int(m.group(2))
            q_nums = list(range(q_start, q_end + 1))
            break

    # Collect question numbers scattered on separate lines
    if not q_nums:
        for line in lines:
            s = line.strip()
            if re.match(r'^\d{1,2}$', s) and 1 <= int(s) <= 40:
                q_nums.append(int(s))
            elif q_nums:
                break

    # Collect stems and option blocks
    stems = []
    option_blocks = []
    current_options = []
    in_options = False

    skip_keywords = ['Listening', 'PART', 'Questions', 'Choose', 'Complete', 'Write', 'Test']

    for line in lines:
        s = line.strip()
        if not s:
            continue

        # Skip headers
        if any(s.startswith(kw) for kw in skip_keywords):
            continue

        # Option line
        om = re.match(r'^([A-H])\s{1,3}(.+)', s)
        if om:
            current_options.append(f"{om.group(1)}. {om.group(2).strip()}")
            in_options = True
            continue

        # Non-option line - could be a new stem
        if in_options and current_options:
            # Save the options block
            option_blocks.append(current_options)
            current_options = []
            in_options = False

        # Skip standalone numbers or noise
        if re.match(r'^\d{1,2}$', s):
            continue
        if len(s) < 5:
            continue

        stems.append(s)

    # Save last option block
    if current_options:
        option_blocks.append(current_options)

    # Pair stems with option blocks
    # Skip the first stem if it's a section title (no matching options)
    start_idx = 0
    if len(stems) > len(option_blocks):
        start_idx = len(stems) - len(option_blocks)

    for idx in range(min(len(stems) - start_idx, len(option_blocks), len(q_nums))):
        stem = stems[start_idx + idx]
        opts = option_blocks[idx]
        q_num = q_nums[idx]
        questions.append({'number': q_num, 'stem': stem, 'options': opts})

    return questions


def parse_fill_ocr(text):
    """Parse fill-blank questions from OCR text.

    OCR formats:
        ... context ... 31 .. rest of line
        ... context ...
        32 without dots but on separate line
        context text 1 ..... (for Part 1 Q1-10)
    """
    items = []
    lines = text.split('\n')

    for idx, line in enumerate(lines):
        s = line.strip()
        # Flexible match: number followed by 2+ dots, or 3+ dots/spaces
        m = re.search(r'(\d{1,2})\s*[\.]{2,}', s)
        if not m:
            m = re.search(r'(\d{1,2})\s{3,}', s)
        if not m:
            # Number at end of line (no visible dots in OCR)
            m = re.search(r'\b(\d{1,2})\s*$', s)

        if m:
            q_num = int(m.group(1))
            if 1 <= q_num <= 40:
                ctx = s[:m.start()].strip()
                ctx = re.sub(r'[®•@—\-]\s*', '', ctx)

                # Multi-line fallback
                if not ctx and idx > 0:
                    for j in range(idx - 1, max(idx - 4, -1), -1):
                        prev = lines[j].strip()
                        prev_clean = re.sub(r'[®•@—\-]\s*', '', prev).strip()
                        if not prev_clean or len(prev_clean) <= 2:
                            continue
                        if re.match(r'^(\d{1,2}|Listening|PART|Questions|Complete|Write)', prev_clean):
                            break
                        ctx = prev_clean
                        break

                if ctx and len(ctx) > 2:
                    items.append({'number': q_num, 'context': ctx})

    return items


def fix_book_with_ocr(book_id):
    """OCR listening pages and fix listening.json for one book."""
    # For cam20, handle separately (separate per-test PDFs, not in TOC)
    if book_id == "cam20":
        json_path = os.path.join(DATA_DIR, book_id, "listening.json")
        if os.path.exists(json_path):
            with open(json_path, encoding="utf-8") as f:
                data = json.load(f)
            return fix_cam20_with_ocr(data)
        return 0, 0

    if book_id not in TOC:
        return 0, 0

    json_path = os.path.join(DATA_DIR, book_id, "listening.json")
    if not os.path.exists(json_path):
        return 0, 0

    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    test_starts = TOC[book_id]["test_starts"]

    pdf_path = os.path.join(PDF_DIR, f"{book_id}_questions.pdf")
    if not os.path.exists(pdf_path):
        return 0, 0

    doc = fitz.open(pdf_path)
    total_mc = 0
    total_fill = 0

    for test_idx, test_start in enumerate(test_starts):
        next_start = test_starts[test_idx + 1] if test_idx + 1 < len(test_starts) else None

        print(f"  OCR Test {test_idx+1} (pages {test_start}-{next_start or test_start+16})...")

        sections = find_listening_sections(doc, test_start, next_start)
        print(f"    Found sections: {sorted(sections.keys())}")

        # Find matching test in JSON
        test_data = None
        for t in data.get("tests", []):
            if t.get("testNumber") == test_idx + 1:
                test_data = t
                break

        if not test_data:
            continue

        for part_idx, part in enumerate(test_data.get("parts", [])):
            section_num = part_idx + 1
            if section_num not in sections:
                continue

            section_text = sections[section_num]

            # Parse MC and fill-blank from section text
            parsed_mc = parse_mc_ocr(section_text)
            parsed_fill = parse_fill_ocr(section_text)

            # Fix MC questions
            if parsed_mc:
                mc_lookup = {q['number']: q for q in parsed_mc}
                for q in part.get("questions", []):
                    if q['type'] not in ('multiple_choice', 'multiple_choice_multi'):
                        continue
                    opts = q.get('options', [])
                    if not (opts and all(len(str(o).strip()) <= 2 for o in opts)):
                        continue
                    qm = re.search(r'q(\d+)$', q['id'])
                    if not qm:
                        continue
                    q_num = int(qm.group(1))
                    if q_num in mc_lookup:
                        parsed = mc_lookup[q_num]
                        q['question'] = parsed['stem']
                        q['options'] = parsed['options']
                        ans = q.get('correctAnswer', '').strip().upper()
                        for opt in parsed['options']:
                            if opt.startswith(ans + '.'):
                                q['correctAnswer'] = opt
                                break
                        total_mc += 1

            # Fix fill-blank questions
            if parsed_fill:
                fill_lookup = {item['number']: item for item in parsed_fill}
                for q in part.get("questions", []):
                    if q['type'] not in ('notes_completion', 'form_completion',
                                        'summary_completion', 'sentence_completion'):
                        continue
                    if 'Question' not in q.get('question', ''):
                        continue
                    qm = re.search(r'Question\s+(\d+)', q.get('question', ''))
                    if not qm:
                        continue
                    q_num = int(qm.group(1))
                    if q_num in fill_lookup:
                        q['question'] = fill_lookup[q_num]['context'] + ' _____'
                        total_fill += 1

    doc.close()

    if total_mc > 0 or total_fill > 0:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  SAVED: {total_mc} MC, {total_fill} fill-blanks")

    return total_mc, total_fill


def fix_cam20_with_ocr(data):
    """Handle cam20 which has separate PDFs per test.

    Each PDF has: cover page, then listening sections starting at page 2.
    """
    mc_total = 0
    fill_total = 0

    for test_num in range(1, 5):
        pdf_path = os.path.join(PDF_DIR, f"cam20_test{test_num}_questions.pdf")
        if not os.path.exists(pdf_path):
            continue

        doc = fitz.open(pdf_path)
        print(f"  OCR cam20 Test {test_num} ({doc.page_count} pages)...")

        # OCR from page 2 (0-indexed: 1) - skip cover
        sections = {}
        current_section = None
        current_lines = []

        for pg in range(1, doc.page_count):  # Start from page 2
            text = ocr_page(doc, pg)
            lines = text.split('\n')

            for line in lines:
                s = line.strip()

                # Section header - also handle "Test1-listening—part1" style headers
                part_match = re.search(r'PART\s+(\d+)\s+Questions?\s+(\d+)', s, re.IGNORECASE)
                if not part_match:
                    part_match = re.search(r'[Pp]art\s*(\d+)', s)
                if part_match:
                    if current_section is not None and current_lines:
                        sections[current_section] = '\n'.join(current_lines)
                    current_section = int(part_match.group(1))
                    current_lines = [s]
                    continue

                # Stop at Reading or Writing
                if re.match(r'^\s*(READING|WRITING)\s*(PASSAGE|SECTION|TASK)?\s*\d*', s, re.IGNORECASE):
                    if current_section is not None and current_lines:
                        sections[current_section] = '\n'.join(current_lines)
                    current_section = None
                    current_lines = []
                    continue

                if current_section is not None:
                    current_lines.append(s)

        if current_section is not None and current_lines:
            sections[current_section] = '\n'.join(current_lines)

        doc.close()
        print(f"    Found sections: {sorted(sections.keys())}")

        # Match to JSON
        test_data = None
        for t in data.get("tests", []):
            if t.get("testNumber") == test_num:
                test_data = t
                break

        if not test_data:
            continue

        for part_idx, part in enumerate(test_data.get("parts", [])):
            section_num = part_idx + 1
            if section_num not in sections:
                continue

            section_text = sections[section_num]
            parsed_mc = parse_mc_ocr(section_text)
            parsed_fill = parse_fill_ocr(section_text)

            if parsed_mc:
                mc_lookup = {q['number']: q for q in parsed_mc}
                for q in part.get("questions", []):
                    if q['type'] not in ('multiple_choice', 'multiple_choice_multi'):
                        continue
                    opts = q.get('options', [])
                    if not (opts and all(len(str(o).strip()) <= 2 for o in opts)):
                        continue
                    qm = re.search(r'q(\d+)$', q['id'])
                    if not qm:
                        continue
                    q_num = int(qm.group(1))
                    if q_num in mc_lookup:
                        parsed = mc_lookup[q_num]
                        q['question'] = parsed['stem']
                        q['options'] = parsed['options']
                        ans = q.get('correctAnswer', '').strip().upper()
                        for opt in parsed['options']:
                            if opt.startswith(ans + '.'):
                                q['correctAnswer'] = opt
                                break
                        mc_total += 1

            if parsed_fill:
                fill_lookup = {item['number']: item for item in parsed_fill}
                for q in part.get("questions", []):
                    if q['type'] not in ('notes_completion', 'form_completion',
                                        'summary_completion', 'sentence_completion'):
                        continue
                    if 'Question' not in q.get('question', ''):
                        continue
                    qm = re.search(r'Question\s+(\d+)', q.get('question', ''))
                    if not qm:
                        continue
                    q_num = int(qm.group(1))
                    if q_num in fill_lookup:
                        q['question'] = fill_lookup[q_num]['context'] + ' _____'
                        fill_total += 1

    if mc_total > 0 or fill_total > 0:
        json_path = os.path.join(DATA_DIR, "cam20", "listening.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  SAVED: {mc_total} MC, {fill_total} fill-blanks")

    return mc_total, fill_total


def main():
    import sys

    if "--book" in sys.argv:
        books = [sys.argv[sys.argv.index("--book") + 1]]
    else:
        books = ["cam15", "cam16", "cam18", "cam19", "cam20"]

    total_mc = 0
    total_fill = 0

    for book_id in books:
        print(f"\n{'='*60}")
        print(f"Processing {book_id} (OCR)")
        print(f"{'='*60}")
        mc, fill = fix_book_with_ocr(book_id)
        total_mc += mc
        total_fill += fill

    print(f"\n{'='*60}")
    print(f"Total: {total_mc} MC fixed, {total_fill} fill-blanks fixed")
    print("Done!")


if __name__ == "__main__":
    main()
