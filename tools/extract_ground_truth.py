"""
Extract ground-truth question structure and answer keys from official Cambridge IELTS PDFs.

Works with native digital PDFs (cam14, cam17) — not scanned images.

Usage:
  python3 extract_ground_truth.py              # Extract all
  python3 extract_ground_truth.py --cam cam17  # Specific book
  python3 extract_ground_truth.py --dry-run    # Show without saving
  python3 extract_ground_truth.py --show-raw   # Debug: show raw PDF lines
"""

import json
import re
import sys
from collections import OrderedDict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import fitz

DATA_DIR = Path("data/cambridge")
PDF_DIR = DATA_DIR / "pdf"
OUTPUT_DIR = Path("data/extracted")

BOOK_PAGES = {
    "cam17": {
        1: (10, 15), 2: (31, 36), 3: (53, 58), 4: (75, 80),
        "answers": list(range(119, 127)),
    },
    "cam14": {
        1: (10, 16), 2: (32, 37), 3: (53, 59), 4: (75, 81),
        "answers": list(range(119, 127)),
    },
}

# ── Regex patterns ──
_RE_Q_RANGE = re.compile(r"^Questions?\s+(\d{1,2})[–\-]\s*(\d{1,2})")
_RE_Q_AND = re.compile(r"^Questions?\s+(\d{1,2})\s+and\s+(\d{1,2})")
_RE_CHOOSE_TWO = re.compile(r"Choose\s+(TWO|THREE)\s+letters?", re.I)
_RE_CHOOSE_CORRECT = re.compile(r"Choose\s+the\s+correct\s+letter", re.I)
_RE_FROM_BOX = re.compile(r"from\s+the\s+box", re.I)
_RE_WRITE_LETTER = re.compile(r"Write\s+the\s+correct\s+letter", re.I)
_RE_COMPLETE = re.compile(r"Complete\s+the\s+(notes|table|form|flow.chart|summary|sentences?)", re.I)
_RE_PART = re.compile(r"^(?:PART|SECTION|SECT(?:S|B)ON)\s+(\d+)")
_RE_SKIP = re.compile(
    r"^(Questions?\s+\d|Choose\s+|Write\s+(ONE|NO\s+MORE)|p\.\s+\d|"
    r"Test\s+\d|LISTENING|Listening|READING|Sample|Audioscripts|"
    r"If\s+you\s+score|you\s+are|acceptable|-{2,})$"
)
_RE_BARE_NUM = re.compile(r"^(\d{1,2})$")
_RE_INLINE_Q = re.compile(r"^(\d{1,2})\s+(.+)")
_RE_BARE_LETTER = re.compile(r"^([A-H])$")
_RE_LETTER_TEXT = re.compile(r"^([A-H])\s{2,}(.+)")
_RE_NUM_IN_TEXT = re.compile(r"\b(\d{1,2})\b")


# ── PDF text extraction ──

def extract_lines(doc: fitz.Document, first_page: int, last_page: int) -> List[str]:
    """Extract and normalize text lines from a page range."""
    raw = []
    for pg in range(first_page - 1, min(last_page, len(doc))):
        for line in doc[pg].get_text("text").split("\n"):
            s = line.strip()
            # Normalize unicode spaces but keep structure
            s = s.replace(" ", " ").replace(" ", " ").replace(" ", " ")
            s = s.replace("\xa0", " ").replace("\x07", "")
            s = re.sub(r"\s+", " ", s).strip()
            raw.append(s)
    return raw


def is_skip(s: str) -> bool:
    return not s or _RE_SKIP.match(s)


# ── Data classes ──

@dataclass
class ParsedQ:
    number: int
    stem: str
    qtype: str
    options: List[Tuple[str, str]] = field(default_factory=list)


@dataclass
class ParsedSection:
    qtype: str
    start_num: int
    end_num: int
    is_multi: bool = False
    multi_count: int = 1
    option_box: Dict[str, str] = field(default_factory=dict)
    questions: List[ParsedQ] = field(default_factory=list)


# ── Top-level parsing ──

def parse_test(lines: List[str], test_num: int) -> List[ParsedSection]:
    """Parse a full test into sections."""
    sections = []

    # Find PART boundaries
    part_bounds = []
    for i, line in enumerate(lines):
        m = _RE_PART.match(line)
        if m and 1 <= int(m.group(1)) <= 4:
            part_bounds.append((int(m.group(1)), i))

    for idx, (part_num, start_i) in enumerate(part_bounds):
        end_i = part_bounds[idx + 1][1] if idx + 1 < len(part_bounds) else len(lines)
        part_lines = lines[start_i:end_i]
        sections.extend(_parse_part(part_lines, part_num))

    return sections


def _parse_part(lines: List[str], part_num: int) -> List[ParsedSection]:
    """Parse one part into question sections."""
    # Find sub-headers
    sub_headers = []  # [(start_q, end_q, index, is_multi)]
    for i, line in enumerate(lines):
        range_m = _RE_Q_RANGE.match(line)
        if range_m:
            sub_headers.append((int(range_m.group(1)), int(range_m.group(2)), i, False))
        and_m = _RE_Q_AND.match(line)
        if and_m:
            sub_headers.append((int(and_m.group(1)), int(and_m.group(2)), i, True))

    # Remove overlapping outer headers (e.g. "Questions 11-20" when "Questions 11-14" exists)
    filtered = _remove_outer_headers(sub_headers, lines)

    if not filtered:
        # No sub-sections → entire part is one block
        return [_parse_block(lines, part_num, None, None)]

    sections = []
    for idx, (start_q, end_q, header_i, is_multi) in enumerate(filtered):
        next_i = filtered[idx + 1][2] if idx + 1 < len(filtered) else len(lines)
        block_lines = lines[header_i:next_i]
        section = _parse_block(block_lines, part_num, start_q, end_q)
        if section:
            sections.append(section)

    # Merge back into parts if needed (match expected 4-part structure)
    return sections


def _remove_outer_headers(headers, lines):
    """Remove outer/duplicate question range headers.

    1. Remove outer headers whose ranges are fully covered by inner ones
    2. Merge duplicate adjacent headers with the same range (page header repeats)
    """
    if len(headers) <= 1:
        return headers

    # Step 1: remove outer headers covered by inner ranges
    stage1 = []
    for i, (start, end, idx, is_multi) in enumerate(headers):
        covered = set()
        for j, (s2, e2, idx2, is_m2) in enumerate(headers):
            if i != j and s2 >= start and e2 <= end and (s2 > start or e2 < end):
                for n in range(s2, e2 + 1):
                    covered.add(n)
        expected = set(range(start, end + 1))
        if covered == expected:
            continue
        stage1.append((start, end, idx, is_multi))

    # Step 2: merge duplicates — if two adjacent headers have the same range,
    # keep only the first (page-continuation headers repeat the range)
    result = []
    for i, (start, end, idx, is_multi) in enumerate(stage1):
        if result and start == result[-1][0] and end == result[-1][1]:
            continue  # skip duplicate
        result.append((start, end, idx, is_multi))

    return result


# ── Block parsing ──

def _parse_block(
    lines: List[str], part_num: int, start_q: Optional[int], end_q: Optional[int]
) -> Optional[ParsedSection]:
    """Parse one question block, dispatching to type-specific parsers."""
    full_text = " ".join(lines)

    # Detect type
    is_multi = bool(_RE_CHOOSE_TWO.search(full_text))
    multi_count = 2
    m = _RE_CHOOSE_TWO.search(full_text)
    if m and m.group(1).upper() == "THREE":
        multi_count = 3

    if _RE_CHOOSE_CORRECT.search(full_text) or _RE_CHOOSE_TWO.search(full_text):
        qtype = "multiple_choice_multi" if is_multi else "multiple_choice"
    elif _RE_FROM_BOX.search(full_text) or _RE_WRITE_LETTER.search(full_text):
        qtype = "matching"
    elif _RE_COMPLETE.search(full_text):
        qtype = "form_completion"
    else:
        qtype = "form_completion"

    if qtype in ("multiple_choice", "multiple_choice_multi"):
        questions = _parse_mc(lines, start_q, end_q)
    elif qtype == "matching":
        questions, option_box = _parse_matching(lines, start_q, end_q)
        return ParsedSection(
            qtype=qtype,
            start_num=start_q or (questions[0].number if questions else 0),
            end_num=end_q or (questions[-1].number if questions else 0),
            is_multi=is_multi,
            multi_count=multi_count,
            option_box=option_box,
            questions=questions,
        )
    else:
        questions = _parse_completion(lines, start_q, end_q, part_num)

    if not questions:
        return None

    return ParsedSection(
        qtype=qtype,
        start_num=start_q or questions[0].number,
        end_num=end_q or questions[-1].number,
        is_multi=is_multi,
        multi_count=multi_count,
        questions=questions,
    )


# ── MC parser ──

def _parse_mc(
    lines: List[str], start_q: Optional[int], end_q: Optional[int]
) -> List[ParsedQ]:
    """Parse MC questions from normalized lines.

    Handles:
      - Standard MC: '11' bare number → stem → 'A' → text → 'B' → text...
      - Inline MC: '12 What colour...' → 'A' → 'dark red'...
      - Multi-select: no question numbers in text; stem is the first content line
        after the instruction, options follow. Question numbers from start_q/end_q.
    """
    questions = []
    i = 0

    # Find the first non-header content line (used for multi-select stem)
    content_start = 0
    for j, line in enumerate(lines):
        if not is_skip(line) and not _RE_BARE_LETTER.match(line) and not _RE_BARE_NUM.match(line):
            content_start = j
            break

    while i < len(lines):
        line = lines[i]

        # Try bare number: "11" (was "11\t")
        bare_m = _RE_BARE_NUM.match(line)
        if bare_m:
            qnum = int(bare_m.group(1))
            if start_q and end_q and not (start_q <= qnum <= end_q):
                i += 1
                continue

            stem_parts = []
            i += 1
            while i < len(lines):
                nl = lines[i]
                if _RE_BARE_LETTER.match(nl) or _RE_BARE_NUM.match(nl) or _RE_INLINE_Q.match(nl):
                    break
                if nl and not is_skip(nl):
                    stem_parts.append(nl)
                i += 1

            stem = " ".join(stem_parts).strip()
            options, i = _parse_mc_options(lines, i)
            if stem:
                questions.append(ParsedQ(number=qnum, stem=stem, qtype="multiple_choice", options=options))
            continue

        # Try inline: "12 What colour are the tour boats?"
        inline_m = _RE_INLINE_Q.match(line)
        if inline_m:
            qnum = int(inline_m.group(1))
            if start_q and end_q and not (start_q <= qnum <= end_q):
                i += 1
                continue

            stem = inline_m.group(2).strip()
            i += 1
            if i < len(lines) and _RE_BARE_LETTER.match(lines[i]):
                options, i = _parse_mc_options(lines, i)
            else:
                options = []
            questions.append(ParsedQ(number=qnum, stem=stem, qtype="multiple_choice", options=options))
            continue

        i += 1

    # Multi-select fallback: if no questions found but we have a range,
    # the stem is the first content line and options follow
    if not questions and start_q and end_q:
        # Find stem: first content line after skipping headers/instructions
        stem = ""
        option_start = 0
        for j in range(content_start, len(lines)):
            l = lines[j]
            if is_skip(l) or _RE_BARE_NUM.match(l) or _RE_INLINE_Q.match(l):
                continue
            if _RE_BARE_LETTER.match(l):
                option_start = j
                break
            if not stem:
                stem = l
            else:
                stem += " " + l

        if stem:
            options, _ = _parse_mc_options(lines, option_start)
            for num in range(start_q, end_q + 1):
                questions.append(
                    ParsedQ(number=num, stem=stem, qtype="multiple_choice_multi", options=options)
                )

    return questions


def _line_is_option_start(s: str) -> bool:
    """Check if a line starts an option: bare letter or letter+text."""
    return bool(_RE_BARE_LETTER.match(s) or _RE_LETTER_TEXT.match(s))


def _parse_mc_options(lines: List[str], start: int) -> Tuple[List[Tuple[str, str]], int]:
    """Parse option letters and their text. Returns (options, new_index)."""
    options = []
    i = start
    while i < len(lines):
        line = lines[i]

        # Bare option letter: "A"
        bare_letter = _RE_BARE_LETTER.match(line)
        if bare_letter:
            letter = bare_letter.group(1)
            opt_text_parts = []
            i += 1
            while i < len(lines):
                nl = lines[i]
                # Stop at next option letter, next question number, or skip line
                if _RE_BARE_LETTER.match(nl) or _RE_BARE_NUM.match(nl) or _RE_INLINE_Q.match(nl):
                    break
                if nl and not is_skip(nl):
                    opt_text_parts.append(nl)
                i += 1
            opt_text = " ".join(opt_text_parts).strip()
            if opt_text:
                options.append((letter, opt_text))
            continue

        # Letter with inline text: "A  shopping"
        letter_text = _RE_LETTER_TEXT.match(line)
        if letter_text:
            options.append((letter_text.group(1), letter_text.group(2).strip()))
            i += 1
            continue

        break
    return options, i


# ── Matching parser ──

def _parse_matching(
    lines: List[str], start_q: Optional[int], end_q: Optional[int]
) -> Tuple[List[ParsedQ], Dict[str, str]]:
    """Parse matching questions.

    After "from the box" instruction, there's an option box section
    followed by numbered items.
    """
    questions = []
    option_box = OrderedDict()

    # Find the option box start and items start
    box_start = None
    items_start = None
    for i, line in enumerate(lines):
        if _RE_FROM_BOX.search(line) or _RE_WRITE_LETTER.search(line):
            box_start = i + 1
        if box_start and _RE_INLINE_Q.match(line):
            # First numbered item line starts the items section
            items_start = i
            break

    if box_start and items_start:
        # Parse option box: bare letter then text, or letter+text inline
        j = box_start
        while j < items_start:
            bare = _RE_BARE_LETTER.match(lines[j])
            if bare:
                letter = bare.group(1)
                j += 1
                text_parts = []
                while j < items_start:
                    if _RE_BARE_LETTER.match(lines[j]) or _RE_INLINE_Q.match(lines[j]):
                        break
                    if lines[j] and not is_skip(lines[j]):
                        text_parts.append(lines[j])
                    j += 1
                option_box[letter] = " ".join(text_parts).strip()
            else:
                lt = _RE_LETTER_TEXT.match(lines[j])
                if lt:
                    option_box[lt.group(1)] = lt.group(2).strip()
                j += 1

    # Parse items from items_start onwards
    for line in lines[items_start:]:
        inline = _RE_INLINE_Q.match(line)
        if inline:
            num = int(inline.group(1))
            if start_q and end_q and not (start_q <= num <= end_q):
                continue
            stem = inline.group(2).strip()
            questions.append(ParsedQ(
                number=num, stem=stem, qtype="matching",
                options=[(l, d) for l, d in option_box.items()],
            ))

    return questions, dict(option_box)


# ── Completion parser ──

def _parse_completion(
    lines: List[str], start_q: Optional[int], end_q: Optional[int], part_num: int
) -> List[ParsedQ]:
    """Parse form/table/notes completion questions."""
    questions = []
    seen = set()

    # Pre-filter: remove "Questions X–Y" headers from lines to avoid false matches
    clean_lines = []
    for line in lines:
        if _RE_Q_RANGE.match(line) or _RE_Q_AND.match(line):
            continue
        clean_lines.append(line)

    # Build paragraphs from contiguous non-skip lines
    paragraphs = []
    current = []
    for line in clean_lines:
        if is_skip(line):
            if current:
                paragraphs.append(" ".join(current))
                current = []
        else:
            current.append(line)
    if current:
        paragraphs.append(" ".join(current))

    # Find question numbers in paragraphs
    for para in paragraphs:
        for m in re.finditer(r"\b(\d{1,2})\b", para):
            num = int(m.group(1))
            if start_q and end_q and not (start_q <= num <= end_q):
                continue
            if num in seen:
                # Already found this number; skip duplicates
                continue
            seen.add(num)

            pos = m.start()
            ctx_start = max(0, pos - 100)
            ctx_end = min(len(para), pos + 100)
            ctx = para[ctx_start:ctx_end]
            stem = re.sub(rf"\b{num}\b\s*", f"{num}. _____ ", ctx)
            stem = re.sub(r"\s{2,}", " ", stem).strip()
            stem = re.sub(r"^[•\-−]\s*", "", stem)
            questions.append(ParsedQ(number=num, stem=stem, qtype="form_completion"))

    # Fallback: line-by-line for missed numbers
    if start_q and end_q:
        expected = set(range(start_q, end_q + 1))
        missing = expected - seen
        if missing:
            for line in clean_lines:
                if is_skip(line):
                    continue
                for m in re.finditer(r"\b(\d{1,2})\b", line):
                    num = int(m.group(1))
                    if num not in missing or num in seen:
                        continue
                    seen.add(num)
                    stem = f"{num}. _____ {line}"
                    questions.append(ParsedQ(number=num, stem=stem, qtype="form_completion"))

    questions.sort(key=lambda q: q.number)
    return questions


# ── Answer keys ──

def extract_answer_keys(doc: fitz.Document, answer_pages: List[int], cam_id: str) -> Dict[str, str]:
    """Extract answer keys from the PDF's answer pages."""
    answers = {}
    all_lines = []
    for pg in answer_pages:
        if pg - 1 < len(doc):
            all_lines.extend(doc[pg - 1].get_text("text").split("\n"))

    current_test = None
    in_listening = False

    for raw_line in all_lines:
        s = raw_line.strip()
        if not s:
            continue

        test_m = re.match(r"^TEST\s+(\d+)", s)
        if test_m:
            current_test = int(test_m.group(1))
            continue

        if s == "LISTENING":
            in_listening = True
            continue
        if s == "READING" or re.match(r"^(If you score|you are|acceptable|Sample|Listening and Reading)", s):
            in_listening = False
            continue

        if not current_test or not in_listening:
            continue

        # Skip part headers
        if re.match(r"Part\s+\d", s):
            continue

        # Single answer: "1  litter" or "11  A"
        single_m = re.match(r"^(\d{1,2})\s{2,}(.+)$", s)
        if single_m:
            qnum = int(single_m.group(1))
            answer = single_m.group(2).strip()
            answers[f"{cam_id}_t{current_test}_l_q{qnum}"] = answer
            continue

        # Multi answer: "15&16  IN EITHER ORDER  A  D"
        multi_m = re.match(r"^(\d{1,2})&(\d{1,2})\s+IN\s+EITHER\s+ORDER\s+(.+)$", s)
        if multi_m:
            q1, q2 = int(multi_m.group(1)), int(multi_m.group(2))
            letters = re.findall(r"\b([A-H])\b", multi_m.group(3))
            if len(letters) >= 2:
                ans = ",".join(letters)
                for qnum in (q1, q2):
                    answers[f"{cam_id}_t{current_test}_l_q{qnum}"] = ans
            continue

    return answers


# ── Output assembly ──

def _sections_to_parts(sections: List[ParsedSection], test_num: int, cam_id: str) -> List[dict]:
    """Group sections into 4 parts (10 questions each)."""
    parts = []
    for part_num in range(1, 5):
        part_start = (part_num - 1) * 10 + 1
        part_end = part_num * 10
        part_sections = [
            s for s in sections
            if s.start_num >= part_start and s.end_num <= part_end
        ]

        if not part_sections:
            continue

        questions = []
        for section in part_sections:
            for q in section.questions:
                questions.append({
                    "id": f"{cam_id}_t{test_num}_l_q{q.number}",
                    "type": section.qtype,
                    "question": q.stem,
                    "options": [f"{l}. {t}" for l, t in q.options] if q.options else [],
                    "section_type": section.qtype,
                    "section_range": f"{section.start_num}-{section.end_num}",
                    "option_box": section.option_box,
                    "is_multi_group": section.is_multi,
                })

        parts.append({
            "id": f"{cam_id}_t{test_num}_l_p{part_num}",
            "part_number": part_num,
            "questions": questions,
        })

    return parts


def extract_book(cam_id: str) -> Optional[dict]:
    """Extract ground truth for one book."""
    book_info = BOOK_PAGES.get(cam_id)
    if not book_info:
        return None

    questions_path = PDF_DIR / f"{cam_id}_questions.pdf"
    if not questions_path.exists():
        return None

    doc = fitz.open(str(questions_path))

    # Check for native text
    first_test_page = book_info[1][0] - 1
    test_text = doc[first_test_page].get_text().strip()
    if len(test_text) < 50:
        print(f"  [SKIP] {cam_id}_questions.pdf is scanned (no native text)")
        doc.close()
        return None

    result = {"id": cam_id, "tests": {}}

    for test_num in [1, 2, 3, 4]:
        first_page, last_page = book_info[test_num]
        lines = extract_lines(doc, first_page, last_page)
        sections = parse_test(lines, test_num)
        parts = _sections_to_parts(sections, test_num, cam_id)
        result["tests"][f"test{test_num}"] = {
            "test_number": test_num,
            "parts": parts,
        }

    # Merge answer keys
    answers = extract_answer_keys(doc, book_info.get("answers", []), cam_id)
    for test_key, test_data in result["tests"].items():
        for part in test_data["parts"]:
            for q in part["questions"]:
                qid = q["id"]
                if qid in answers:
                    q["correct_answer_from_book"] = answers[qid]

    doc.close()
    return result


# ── CLI ──

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Extract ground truth from official IELTS PDFs")
    parser.add_argument("--cam", type=str, default="all")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--show-answers", action="store_true")
    parser.add_argument("--show-raw", action="store_true")
    args = parser.parse_args()

    books = list(BOOK_PAGES.keys()) if args.cam == "all" else [args.cam]

    for cam_id in books:
        print(f"\n{'='*60}")
        print(f"  Extracting {cam_id}")
        print(f"{'='*60}")

        if args.show_raw:
            book_info = BOOK_PAGES[cam_id]
            doc = fitz.open(str(PDF_DIR / f"{cam_id}_questions.pdf"))
            for test_num in [1, 2, 3, 4]:
                first_page, last_page = book_info[test_num]
                lines = extract_lines(doc, first_page, last_page)
                print(f"\n  --- Test {test_num} ---")
                for i, line in enumerate(lines[:60]):
                    print(f"  L{i:03d}: {repr(line)}")
            doc.close()
            continue

        result = extract_book(cam_id)
        if not result:
            continue

        if args.dry_run:
            for test_key, test_data in result["tests"].items():
                print(f"\n  {test_key.upper()}:")
                for part in test_data["parts"]:
                    types = set(q["type"] for q in part["questions"])
                    print(f"    {part['id']}: {len(part['questions'])} questions, types={types}")
                    for q in part["questions"]:
                        ans = q.get("correct_answer_from_book", "?")
                        print(f"      Q{q['id'].rsplit('_q',1)[-1]:>3s}: {q['type']:25s} ans={str(ans):20s} | {q['question'][:100]}")
        else:
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            out_path = OUTPUT_DIR / f"{cam_id}_ground_truth.json"
            with open(out_path, "w") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"  -> Saved to {out_path}")

    print("\nDone.")
