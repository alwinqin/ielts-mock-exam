#!/usr/bin/env python3
"""Extract listening question content from Cambridge IELTS question PDFs.

For PDFs with extractable text (cam14), parses MC question stems/options
and fill-blank context, then updates listening.json.

For image-based PDFs (cam15/16/18/19/20), requires OCR (not yet implemented).
"""

import json
import os
import re
import fitz

DATA_DIR = "data/cambridge"
PDF_DIR = os.path.join(DATA_DIR, "pdf")


def get_listening_pages(pdf_path):
    """Return [(page_num, full_text)] for listening content pages."""
    doc = fitz.open(pdf_path)
    pages = []
    for i in range(doc.page_count):
        text = doc[i].get_text()
        head = text.strip()[:300]
        # Detect listening pages: "Listening" header, or "Test N" + "SECTION" combo
        is_listening = "Listening" in head
        if not is_listening:
            # Some pages start with "Test N" then have "SECTION X Questions"
            if "Test" in head[:20] and "SECTION" in head[:150]:
                is_listening = True
            # Also check for SECTION headers alone (partial pages)
            if re.search(r'SECT\w+\s+\d+\s+Questions?\s+\d+', head):
                is_listening = True
        if not is_listening:
            continue
        full_lower = text[:800].lower()
        if "answer key" in full_lower:
            continue
        if "test consists of four sections" in full_lower:
            continue
        if "sample answer" in full_lower:
            continue
        pages.append((i + 1, text.strip()))
    doc.close()
    return pages


def parse_header(text):
    """Return (section_num, q_start, q_end) or None."""
    clean = text[:300]
    m = re.search(r'SECT\w+\s+(\d+)\s+Questions?\s+(\d+)\D+(\d+)', clean)
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(3))
    m = re.search(r'Questions?\s+(\d+)\D+(\d+)', clean)
    if m:
        qs, qe = int(m.group(1)), int(m.group(2))
        if 1 <= qs <= 10: sec = 1
        elif 11 <= qs <= 20: sec = 2
        elif 21 <= qs <= 30: sec = 3
        elif 31 <= qs <= 40: sec = 4
        else: return None
        return sec, qs, qe
    return None


def is_mc_section(text):
    return bool(re.search(r'Choose\s+(\w+\s+)*letter', text, re.IGNORECASE))


def parse_mc_from_text(text):
    """Parse MC questions from section text.

    PDF format:
        21
        Question stem line 1
        Question stem line 2 (optional)
        A option text
        B option text
        C option text
        22
        ...

    Returns [{number, stem, options: ['A. text', ...]}]
    """
    questions = []
    lines = text.split('\n')

    # Find where questions start: first line that is just a number (1-40)
    start = 0
    for j, line in enumerate(lines):
        s = line.strip()
        if re.match(r'^\d{1,2}$', s) and 1 <= int(s) <= 40:
            start = j
            break

    if start == 0:
        return questions

    i = start
    while i < len(lines):
        s = lines[i].strip()

        # Standalone question number: "21"
        qm = re.match(r'^(\d{1,2})$', s)
        if not qm:
            i += 1
            continue

        q_num = int(qm.group(1))
        if not (1 <= q_num <= 40):
            i += 1
            continue

        # Collect stem lines (next lines until we hit an option line A-E or next question)
        i += 1
        stem_parts = []
        options = []
        while i < len(lines):
            ns = lines[i].strip()

            # Stop at next standalone question number
            if re.match(r'^\d{1,2}$', ns):
                break

            # Option line: "A text..."
            om = re.match(r'^([A-H])\s{1,3}(.+)', ns)
            if om:
                options.append(f"{om.group(1)}. {om.group(2).strip()}")
                i += 1
                continue

            # Continuation of stem (not empty, not option)
            if ns and not re.match(r'^(Listening|SECTION|SECT|Questions|Choose|Complete|Write|page)', ns):
                if not options:
                    # Still collecting stem
                    stem_parts.append(ns)
                # else: skip option continuations for now

            i += 1

        stem = ' '.join(stem_parts).strip()
        if stem and options:
            questions.append({'number': q_num, 'stem': stem, 'options': options})

    return questions


def parse_fill_from_text(text):
    """Parse fill-blank questions from section text.

    Handles:
      ... context text ... 31 ..............................
      ... context text ...
      32............................rest of line
      31 . .............................

    Returns [{number, context}]
    """
    items = []
    lines = text.split('\n')

    for i, line in enumerate(lines):
        s = line.strip()
        # Flexible dot pattern: number followed by spaces/dots
        # Handles: "31.......", "31 .......", "31 . ....."
        m = re.search(r'(\d{1,2})\s*[\.\s]{3,}', s)
        if m:
            q_num = int(m.group(1))
            if 1 <= q_num <= 40:
                ctx = s[:m.start()].strip()
                ctx = re.sub(r'[®•]\s*', '', ctx)

                # If context is empty, get it from previous non-empty lines
                if not ctx and i > 0:
                    for j in range(i - 1, max(i - 4, -1), -1):
                        prev = lines[j].strip()
                        # Skip empty, bullet-only, or header lines
                        prev_clean = re.sub(r'[®•@]\s*', '', prev).strip()
                        if not prev_clean:
                            continue
                        if len(prev_clean) <= 2:
                            continue
                        if re.match(r'^(\d{1,2}|Listening|SECTION|SECT|Questions|Choose|Complete|Write)', prev_clean):
                            break
                        ctx = prev
                        ctx = re.sub(r'[®•]\s*', '', ctx)
                        break

                if ctx:
                    items.append({'number': q_num, 'context': ctx})

    return items


def fix_book(book_id, dry_run=True):
    """Fix one book's listening.json using PDF extraction."""
    pdf_path = os.path.join(PDF_DIR, f"{book_id}_questions.pdf")
    json_path = os.path.join(DATA_DIR, book_id, "listening.json")

    if not os.path.exists(pdf_path) or not os.path.exists(json_path):
        return 0, 0

    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    pages = get_listening_pages(pdf_path)
    if not pages:
        return 0, 0

    # Parse sections from pages
    sections = []
    for pg, text in pages:
        hdr = parse_header(text)
        if hdr:
            sections.append((pg, hdr[0], hdr[1], hdr[2], text))

    sections.sort(key=lambda x: x[0])

    # Assign test numbers by detecting when section number wraps
    test_of_section = {}
    current_test = 1
    last_section = 0
    for pg, sec, qs, qe, text in sections:
        if sec < last_section:
            current_test += 1
        test_of_section[(pg, sec)] = current_test
        last_section = sec

    mc_fixed = 0
    fill_fixed = 0

    for test in data.get("tests", []):
        test_num = test.get("testNumber", 0)
        if isinstance(test_num, str):
            test_num = int(test_num)

        for part_idx, part in enumerate(test.get("parts", [])):
            section_num = part_idx + 1
            questions = part.get("questions", [])

            # Find matching PDF section (merge all pages for this test+section)
            pdf_texts = []
            for (pg, sec), tn in test_of_section.items():
                if tn == test_num and sec == section_num:
                    for p_pg, p_sec, p_qs, p_qe, p_text in sections:
                        if p_pg == pg and p_sec == sec:
                            pdf_texts.append(p_text)

            if not pdf_texts:
                continue

            # Merge text from all matching pages
            pdf_text = "\n".join(pdf_texts)

            # Run both parsers (sections can have mixed question types)
            parsed_mc = parse_mc_from_text(pdf_text)
            parsed_fill = parse_fill_from_text(pdf_text)

            # Fix MC questions
            if parsed_mc:
                mc_lookup = {q['number']: q for q in parsed_mc}
                for q in questions:
                    if q['type'] not in ('multiple_choice', 'multiple_choice_multi'):
                        continue
                    opts = q.get('options', [])
                    if not (opts and all(len(str(o).strip()) <= 2 for o in opts)):
                        continue  # already has good options
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
                        mc_fixed += 1
                        print(f"    MC {q['id']}: -> \"{parsed['stem'][:60]}...\"")

            # Fix fill-blank questions
            if parsed_fill:
                fill_lookup = {item['number']: item for item in parsed_fill}
                for q in questions:
                    if q['type'] not in ('notes_completion', 'form_completion',
                                        'summary_completion', 'sentence_completion'):
                        continue
                    qtext = q.get('question', '')
                    if 'Question' not in qtext:
                        continue
                    qm = re.search(r'Question\s+(\d+)', qtext)
                    if not qm:
                        continue
                    q_num = int(qm.group(1))
                    if q_num in fill_lookup:
                        q['question'] = fill_lookup[q_num]['context'] + ' _____'
                        fill_fixed += 1
                        print(f"    Fill {q['id']}: -> \"{fill_lookup[q_num]['context'][:60]}...\"")

    print(f"  → MC: {mc_fixed}, Fill-blank: {fill_fixed}")
    if (mc_fixed > 0 or fill_fixed > 0) and not dry_run:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  SAVED {json_path}")

    return mc_fixed, fill_fixed


def main():
    import sys
    dry_run = "--apply" not in sys.argv

    if dry_run:
        print("DRY RUN mode. Use --apply to actually save changes.\n")

    total_mc = 0
    total_fill = 0

    for book_id in sorted(os.listdir(DATA_DIR)):
        if not re.match(r'^cam\d+$', book_id):
            continue
        print(f"\n{'='*60}")
        print(f"{book_id}")
        print(f"{'='*60}")
        mc, fill = fix_book(book_id, dry_run=dry_run)
        total_mc += mc
        total_fill += fill

    print(f"\n{'='*60}")
    print(f"Total: {total_mc} MC fixed, {total_fill} fill-blanks fixed")
    if dry_run:
        print("DRY RUN — no changes saved. Use --apply to save.")
    print("Done!")


if __name__ == "__main__":
    main()
