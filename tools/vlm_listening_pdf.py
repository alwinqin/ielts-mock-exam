#!/usr/bin/env python3
"""Use GLM-4.6V vision-language model to extract listening question content.

For cam15, cam16, cam18, cam19, cam20 — uses VLM for clean text transcription,
then parses with regex. Much better accuracy than Tesseract OCR.

Strategy:
1. For each test, render pages in the listening range as images
2. Send each page to GLM-4.6V for verbatim text transcription
3. Split transcribed text into sections by "PART X Questions" headers
4. Parse MC and fill-blank questions from each section
5. Match to JSON by test number and section number
6. Update listening.json files (only fix bad questions, preserve good ones)
"""

import json
import os
import re
import io
import time
import base64
import fitz
import requests

DATA_DIR = "data/cambridge"
PDF_DIR = os.path.join(DATA_DIR, "pdf")

API_KEY = "no-key-needed"
API_URL = "http://100.114.112.77:8000/v1/chat/completions"
MODEL = "Gemma-4-26B-A4B-it"

TOC = {
    "cam15": {"test_starts": [10, 31, 52, 74], "total_pages": 146},
    "cam16": {"test_starts": [10, 32, 55, 76], "total_pages": 144},
    "cam18": {"test_starts": [12, 34, 57, 80], "total_pages": 147},
    "cam19": {"test_starts": [10, 33, 55, 78], "total_pages": 139},
}


def render_page(doc, page_num, dpi=150):
    """Render a PDF page to base64 PNG."""
    page = doc[page_num]
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat)
    img_data = pix.tobytes("png")
    return base64.b64encode(img_data).decode()


def vlm_transcribe(img_b64):
    """Send page image to GLM-4.6V, get clean text transcription."""
    prompt = (
        "Transcribe ALL text from this IELTS listening test page verbatim. "
        "Preserve the exact layout: headers, question numbers, options (A/B/C/D/E/F/G/H), "
        "fill-blank dots (......), and all body text. "
        "Output the raw text only — no markdown, no explanations, no JSON."
    )

    for attempt in range(4):
        try:
            headers = {"Content-Type": "application/json"}
            if API_KEY != "no-key-needed":
                headers["Authorization"] = f"Bearer {API_KEY}"

            resp = requests.post(
                API_URL,
                headers=headers,
                json={
                    "model": MODEL,
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{img_b64}"
                                    },
                                },
                            ],
                        }
                    ],
                    "max_tokens": 4096,
                    "temperature": 0.1,
                },
                timeout=180,
            )

            if resp.status_code == 200:
                data = resp.json()
                return data["choices"][0]["message"]["content"]

            if resp.status_code == 429:
                wait = min((attempt + 1) * 10, 60)
                print(f"      Rate limited (429), waiting {wait}s...")
                time.sleep(wait)
                continue

            print(f"      API error {resp.status_code}: {resp.text[:150]}")
            if attempt < 3:
                time.sleep(3 * (attempt + 1))

        except requests.exceptions.Timeout:
            print(f"      Timeout (attempt {attempt + 1}/4)")
            time.sleep(5 * (attempt + 1))
        except requests.exceptions.ConnectionError as e:
            print(f"      Connection error (attempt {attempt + 1}/4): {str(e)[:100]}")
            time.sleep(5 * (attempt + 1))
        except Exception as e:
            print(f"      Error (attempt {attempt + 1}/4): {type(e).__name__}: {str(e)[:100]}")
            time.sleep(3 * (attempt + 1))

    return None


def split_into_sections(pages_text):
    """Split merged page texts into sections by PART headers.

    Returns dict: {section_num: text}
    """
    full_text = "\n".join(pages_text)
    sections = {}
    current_section = None
    current_lines = []

    for line in full_text.split("\n"):
        s = line.strip()

        part_match = re.search(r"PART\s+(\d+)\s+Questions?\s+(\d+)", s, re.IGNORECASE)
        if part_match:
            if current_section is not None and current_lines:
                sections[current_section] = "\n".join(current_lines)
            current_section = int(part_match.group(1))
            current_lines = [s]
            continue

        # Stop at Reading section or Writing
        if re.match(
            r"^\s*(READING|WRITING)\s*(PASSAGE|SECTION|TASK)?\s*\d*",
            s,
            re.IGNORECASE,
        ):
            if current_section is not None and current_lines:
                sections[current_section] = "\n".join(current_lines)
            return sections

        if current_section is not None:
            current_lines.append(s)

    if current_section is not None and current_lines:
        sections[current_section] = "\n".join(current_lines)

    return sections


def parse_mc_from_vlm(text):
    """Parse MC questions from clean VLM text.

    Two formats from VLM:
      Format A (standalone number): "21\\nStem text\\nA option\\nB option\\n22\\n..."
      Format B (inline number):     "11  Stem text\\nA option\\nB option\\n12  Stem..."
    Also handles multi-line stems.
    """
    questions = []
    lines = text.split("\n")

    i = 0
    while i < len(lines):
        s = lines[i].strip()

        q_num = None
        stem_start = ""

        # Format A: standalone "21" on its own line
        qm_a = re.match(r"^(\d{1,2})$", s)
        if qm_a:
            q_num = int(qm_a.group(1))
            if not (1 <= q_num <= 40):
                i += 1
                continue
            i += 1
            stem_parts = []

        # Format B: "11  According to the speaker, the company"
        else:
            qm_b = re.match(r"^(\d{1,2})\s{2,}(.+)", s)
            if qm_b:
                q_num = int(qm_b.group(1))
                if not (1 <= q_num <= 40):
                    i += 1
                    continue
                stem_parts = [qm_b.group(2).strip()]
                i += 1
            else:
                i += 1
                continue

        options = []

        while i < len(lines):
            ns = lines[i].strip()

            # Stop at next question number (either format)
            if re.match(r"^(\d{1,2})$|^\d{1,2}\s{2,}[A-Z]", ns):
                # Check if it looks like a new question (number + 2+ spaces + capital letter)
                if re.match(r"^\d{1,2}\s{2,}[A-Z]", ns):
                    break
                if re.match(r"^(\d{1,2})$", ns):
                    nxt = int(ns)
                    if 1 <= nxt <= 40:
                        break

            # Stop at section headers
            if re.match(r"^(PART|SECTION|Questions?\s+\d+)", ns, re.IGNORECASE):
                break

            # Option line: "A text..." or "A. text" or "A text"
            om = re.match(r"^([A-H])[\.\s]\s*(.+)", ns)
            if om:
                options.append(f"{om.group(1)}. {om.group(2).strip()}")
                i += 1
                continue

            # Non-option, non-empty: stem continuation
            if ns and not options:
                stem_parts.append(ns)

            i += 1

        stem = " ".join(stem_parts).strip()
        if stem and options:
            questions.append({"number": q_num, "stem": stem, "options": options})

    return questions


def parse_multi_select_from_vlm(text):
    """Parse multi-select MC questions from VLM text.

    Format: 'Questions 29 and 30\\nChoose TWO letters, A–E.\\nStem text\\nA opt\\nB opt\\n...'

    The question numbers appear in the header (shared), not before each stem.
    Creates one entry per question number with the same stem and options.
    """
    lines = text.split("\n")
    questions = []

    for i, line in enumerate(lines):
        s = line.strip()

        # Detect: "Questions 29 and 30" or "Questions 29–30"
        m = re.match(
            r"Questions?\s+(\d+)\s*(?:and|[-–])\s*(\d+)", s, re.IGNORECASE
        )
        if not m:
            continue

        q_start = int(m.group(1))
        q_end = int(m.group(2))

        # Check for multi-select indicator: "Choose N letters"
        # Look ahead for "Choose" within next few lines
        has_multi = False
        for j in range(i, min(i + 3, len(lines))):
            if re.search(r"Choose\s+\w+\s+letters?", lines[j], re.IGNORECASE):
                has_multi = True
                break
        if not has_multi:
            continue

        # Find the stem (next substantive line after "Choose..." line)
        stem = ""
        options = []
        j = i + 1
        while j < len(lines):
            ns = lines[j].strip()

            # Skip "Choose..." line, empty lines, question number lines
            if re.match(r"Choose\s+", ns, re.IGNORECASE):
                j += 1
                continue
            if not ns:
                j += 1
                continue

            # Option line
            om = re.match(r"^([A-H])[\.\s]\s*(.+)", ns)
            if om:
                if not stem:
                    # Collect stem lines (going backwards from the first option)
                    stem_lines = []
                    for k in range(j - 1, i, -1):
                        prev = lines[k].strip()
                        if not prev:
                            continue
                        if re.match(
                            r"^(Choose|Questions?\s+\d+)", prev, re.IGNORECASE
                        ):
                            continue
                        stem_lines.insert(0, prev)
                    stem = " ".join(stem_lines).strip()
                options.append(f"{om.group(1)}. {om.group(2).strip()}")
                j += 1
                continue

            # Stop at next section
            if re.match(r"^(PART|SECTION)", ns, re.IGNORECASE):
                break

            j += 1

        if stem and options:
            for q_num in range(q_start, q_end + 1):
                questions.append({
                    "number": q_num,
                    "stem": stem,
                    "options": list(options),
                })

    return questions


def parse_fill_from_vlm(text):
    """Parse fill-blank questions from clean VLM text.

    Patterns: "... context ... 31 ...................."
    Context = everything before the dots (including question number and suffix like currency).
    """
    items = []
    lines = text.split("\n")

    skip_prefixes = (
        "PART", "Questions", "SECTION", "SECT", "Listening",
        "Complete", "Write", "Choose", "Test",
    )

    for i, line in enumerate(lines):
        s = line.strip()
        if not s or s.startswith("|"):
            continue

        # Find question number followed (eventually) by 3+ dots
        # Use word boundaries to avoid matching "312" as "12"
        m = re.search(r"\b(\d{1,2})\b[^.]*[\.]{3,}", s)
        if not m:
            continue

        q_num = int(m.group(1))
        if not (1 <= q_num <= 40):
            continue

        # Context = everything before the dots (not the dots themselves)
        dots_start = s.index("...", m.start())

        # Get text before dots as context
        ctx = s[:dots_start].strip()
        ctx = re.sub(r"[®•@—\-]\s*", "", ctx)

        # Also capture text after dots for extra context
        after_dots = s[dots_start:].lstrip(".").strip()
        if after_dots and len(ctx) < 10:
            # When number is at the start (e.g., "37 ...... began to be added"),
            # combine: "37 _____ began to be added"
            ctx = f"{ctx} _____ {after_dots}"
            if len(ctx) > 2:
                items.append({"number": q_num, "context": ctx})
            continue

        # Skip if context is just a keyword or looks like a header
        if any(ctx.startswith(kw) for kw in skip_prefixes):
            continue

        if not ctx and i > 0:
            for j in range(i - 1, max(i - 4, -1), -1):
                prev = lines[j].strip()
                prev_clean = re.sub(r"[®•@—\-]\s*", "", prev).strip()
                if not prev_clean or len(prev_clean) <= 2:
                    continue
                if any(prev_clean.startswith(kw) for kw in skip_prefixes):
                    break
                if re.match(r"^\d{1,2}", prev_clean):
                    break
                ctx = prev_clean
                break

        if ctx and len(ctx) > 2:
            items.append({"number": q_num, "context": ctx})

    return items


def get_bad_sections(book_id):
    """Return {(test_num, section_num): [bad_question_ids]} for questions needing fix."""
    json_path = os.path.join(DATA_DIR, book_id, "listening.json")
    if not os.path.exists(json_path):
        return {}

    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    bad = {}
    for test in data.get("tests", []):
        tn = test.get("testNumber")
        if isinstance(tn, str):
            tn = int(tn)
        for part_idx, part in enumerate(test.get("parts", [])):
            sn = part_idx + 1
            bad_qids = []
            for q in part.get("questions", []):
                qt = q.get("type", "")
                if qt in ("multiple_choice", "multiple_choice_multi"):
                    opts = q.get("options", [])
                    if opts and all(len(str(o).strip()) <= 2 for o in opts):
                        bad_qids.append(q["id"])
                elif qt in (
                    "notes_completion",
                    "form_completion",
                    "summary_completion",
                    "sentence_completion",
                ):
                    qtext = q.get("question", "")
                    if "Question" in qtext and "ONE WORD" in qtext:
                        bad_qids.append(q["id"])
            if bad_qids:
                bad[(tn, sn)] = bad_qids
    return bad


def process_test_pages(doc, test_start, next_test_start):
    """Render and transcribe all listening pages for a test.

    Returns transcribed text for each page.
    """
    end_page = next_test_start if next_test_start else min(test_start + 18, doc.page_count)
    page_texts = []

    for pg in range(test_start - 1, end_page):
        if pg >= doc.page_count:
            break

        print(f"      Page {pg + 1}...", end=" ", flush=True)
        img_b64 = render_page(doc, pg)
        text = vlm_transcribe(img_b64)

        if text is None:
            print("FAILED")
            continue

        # Check if we've hit reading section (stop early)
        first_line = text.strip().split("\n")[0] if text else ""
        if re.match(r"^\s*READING", first_line, re.IGNORECASE):
            print("READING - stop")
            break

        print(f"OK ({len(text)} chars)")
        page_texts.append(text)

        time.sleep(2)

    return page_texts


def fix_test_sections(data, test_num, sections, bad_sections):
    """Fix bad questions in JSON data using VLM-transcribed sections."""
    total_mc = 0
    total_fill = 0

    test_data = None
    for t in data.get("tests", []):
        if t.get("testNumber") == test_num:
            test_data = t
            break
    if not test_data:
        return 0, 0

    for part_idx, part in enumerate(test_data.get("parts", [])):
        section_num = part_idx + 1
        key = (test_num, section_num)

        if key not in bad_sections:
            continue

        if section_num not in sections:
            print(f"      Part {section_num}: no VLM text found")
            continue

        section_text = sections[section_num]
        bad_qids = set(bad_sections[key])

        parsed_mc = parse_mc_from_vlm(section_text)
        parsed_mc += parse_multi_select_from_vlm(section_text)
        parsed_fill = parse_fill_from_vlm(section_text)

        print(f"      Part {section_num}: {len(parsed_mc)} MC, {len(parsed_fill)} fill parsed, {len(bad_qids)} bad Qs")

        if parsed_mc:
            mc_lookup = {q["number"]: q for q in parsed_mc}
            for q in part.get("questions", []):
                if q["id"] not in bad_qids:
                    continue
                qm = re.search(r"q(\d+)$", q["id"])
                if not qm:
                    continue
                q_num = int(qm.group(1))
                if q_num in mc_lookup:
                    parsed = mc_lookup[q_num]
                    q["question"] = parsed["stem"]
                    q["options"] = parsed["options"]
                    ans = q.get("correctAnswer", "").strip().upper()
                    for opt in parsed["options"]:
                        if opt.startswith(ans + "."):
                            q["correctAnswer"] = opt
                            break
                    total_mc += 1

        if parsed_fill:
            fill_lookup = {item["number"]: item for item in parsed_fill}
            for q in part.get("questions", []):
                if q["id"] not in bad_qids:
                    continue
                qm = re.search(r"Question\s+(\d+)", q.get("question", ""))
                if not qm:
                    continue
                q_num = int(qm.group(1))
                if q_num in fill_lookup:
                    q["question"] = fill_lookup[q_num]["context"] + " _____"
                    total_fill += 1

    return total_mc, total_fill


def fix_book_with_vlm(book_id):
    """Process one book with GLM-4.6V to fix bad listening questions."""
    if book_id == "cam20":
        return fix_cam20_with_vlm()

    if book_id not in TOC:
        return 0, 0

    json_path = os.path.join(DATA_DIR, book_id, "listening.json")
    if not os.path.exists(json_path):
        return 0, 0

    bad_sections = get_bad_sections(book_id)
    if not bad_sections:
        print(f"  No bad questions — all clean!")
        return 0, 0

    bad_tests = sorted(set(tn for tn, _ in bad_sections.keys()))
    print(f"  Tests with bad data: {bad_tests}")
    print(f"  Bad sections: {sorted(bad_sections.keys())}")

    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    test_starts = TOC[book_id]["test_starts"]
    pdf_path = os.path.join(PDF_DIR, f"{book_id}_questions.pdf")
    if not os.path.exists(pdf_path):
        return 0, 0

    doc = fitz.open(pdf_path)
    total_mc = 0
    total_fill = 0

    for test_num in bad_tests:
        test_start = test_starts[test_num - 1]
        next_start = (
            test_starts[test_num] if test_num < len(test_starts) else None
        )

        print(f"  Test {test_num}: pages {test_start}-{next_start or test_start + 16}")

        page_texts = process_test_pages(doc, test_start, next_start)
        if not page_texts:
            print(f"    No pages transcribed!")
            continue

        sections = split_into_sections(page_texts)
        print(f"    Found sections: {sorted(sections.keys())}")

        mc, fill = fix_test_sections(data, test_num, sections, bad_sections)
        total_mc += mc
        total_fill += fill

    doc.close()

    if total_mc > 0 or total_fill > 0:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  SAVED: {total_mc} MC + {total_fill} fill = {total_mc + total_fill} fixed")

    return total_mc, total_fill


def fix_cam20_with_vlm():
    """Handle cam20 which has separate PDFs per test."""
    json_path = os.path.join(DATA_DIR, "cam20", "listening.json")
    if not os.path.exists(json_path):
        return 0, 0

    bad_sections = get_bad_sections("cam20")
    if not bad_sections:
        print(f"  No bad questions — all clean!")
        return 0, 0

    bad_tests = sorted(set(tn for tn, _ in bad_sections.keys()))
    print(f"  Tests with bad data: {bad_tests}")

    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    mc_total = 0
    fill_total = 0

    for test_num in bad_tests:
        pdf_path = os.path.join(PDF_DIR, f"cam20_test{test_num}_questions.pdf")
        if not os.path.exists(pdf_path):
            continue

        doc = fitz.open(pdf_path)
        print(f"  Test {test_num}: {doc.page_count} pages")

        page_texts = []
        for pg in range(1, doc.page_count):
            print(f"      Page {pg + 1}...", end=" ", flush=True)
            img_b64 = render_page(doc, pg)
            text = vlm_transcribe(img_b64)
            if text is None:
                print("FAILED")
                continue
            print(f"OK ({len(text)} chars)")
            page_texts.append(text)
            time.sleep(2)

        doc.close()

        sections = split_into_sections(page_texts)
        print(f"    Found sections: {sorted(sections.keys())}")

        mc, fill = fix_test_sections(data, test_num, sections, bad_sections)
        mc_total += mc
        fill_total += fill

    if mc_total > 0 or fill_total > 0:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  SAVED: {mc_total} MC + {fill_total} fill = {mc_total + fill_total} fixed")

    return mc_total, fill_total


def main():
    import sys

    if "--book" in sys.argv:
        books = [sys.argv[sys.argv.index("--book") + 1]]
    elif "--test" in sys.argv:
        books = ["cam15"]
    else:
        books = ["cam15", "cam16", "cam18", "cam19", "cam20"]

    total_mc = 0
    total_fill = 0

    for book_id in books:
        print(f"\n{'=' * 60}")
        print(f"Processing {book_id} (GLM-4.6V)")
        print(f"{'=' * 60}")
        mc, fill = fix_book_with_vlm(book_id)
        total_mc += mc
        total_fill += fill

    print(f"\n{'=' * 60}")
    print(f"Total: {total_mc} MC fixed, {total_fill} fill-blanks fixed")
    print(f"{'=' * 60}")
    print("Done!")


if __name__ == "__main__":
    main()
