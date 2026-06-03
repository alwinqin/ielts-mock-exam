#!/usr/bin/env python3
"""
Answer Key Extractor v3 — Question-type-guided VLM extraction.

Key insight: 70% of VLM errors are extracting single letters (A-G) for
fill-in-the-blank answers. Solution: use JSON question-type metadata
(MC/matching → letter, form/summary completion → word) to guide the VLM
without revealing the actual correct answers.

Strategy:
  1. Build question-type maps from JSON data
  2. Two-pass VLM: identify test+section, then extract with type hints
  3. Text-based extraction for PDFs with clean text layers (cam17)
  4. Cross-validate against JSON data with answer normalization
"""

import base64
import io
import json
import re
import time
from collections import defaultdict
from pathlib import Path
from typing import Optional

import fitz
import requests
from PIL import Image

API_URL = "http://100.114.112.77:8000/v1/chat/completions"
MODEL = "Gemma-4-26B-A4B-it"
BASE = Path(__file__).parent
PDF_DIR = BASE / "data" / "cambridge" / "pdf"
OUTPUT = BASE / "data" / "validation_reports" / "extracted_answer_keys.json"

ANSWER_KEY_PAGE_RANGE = range(118, 129)

# Types that produce LETTER answers in the answer key
LETTER_TYPES = {"multiple_choice", "matching", "matching_info",
                "matching_names", "multiple_choice_multi"}
# Types that produce WORD/PHRASE answers
WORD_TYPES = {"form_completion", "summary_completion", "sentence_completion",
              "short_answer", "table_completion", "note_completion",
              "flow_chart_completion", "label_completion", "diagram_completion"}
# Types that produce TRUE/FALSE/NOT GIVEN
TFNG_TYPES = {"tfng"}
# Types that produce YES/NO/NOT GIVEN
YNNG_TYPES = {"ynng"}
# Types that produce roman numerals
HEADING_TYPES = {"matching_headings"}


# ═══════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════

def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def render_jpeg(doc: fitz.Document, pg: int, dpi: int = 200) -> str:
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = doc[pg].get_pixmap(matrix=mat)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode()


def vlm_call(img_b64: str, prompt: str, max_tokens: int = 2048) -> Optional[str]:
    for attempt in range(3):
        try:
            resp = requests.post(
                API_URL,
                headers={"Content-Type": "application/json"},
                json={
                    "model": MODEL,
                    "messages": [{"role": "user", "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {
                            "url": f"data:image/jpeg;base64,{img_b64}"}},
                    ]}],
                    "max_tokens": max_tokens,
                    "temperature": 0.0,
                },
                timeout=120,
            )
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"]
            time.sleep(min((attempt + 1) * 10, 60))
        except Exception:
            time.sleep(3)
    return None


# ═══════════════════════════════════════════════════════════════
# ANSWER NORMALIZATION
# ═══════════════════════════════════════════════════════════════

NUMBER_WORDS = {
    "one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
    "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10",
    "eleven": "11", "twelve": "12", "thirteen": "13", "fourteen": "14",
    "fifteen": "15", "sixteen": "16", "seventeen": "17", "eighteen": "18",
    "nineteen": "19", "twenty": "20", "thirty": "30", "thirty five": "35",
    "forty": "40", "fifty": "50",
}


def normalize_answer(raw: str) -> str:
    s = str(raw).strip()
    s = re.sub(r'[;:,]+$', '', s)
    s = re.sub(r'\s+', ' ', s)
    if re.match(r'^[A-Ga-g]$', s):
        return s.upper()
    lower = s.lower()
    slash_parts = [p.strip() for p in s.split('/')]
    if len(slash_parts) == 2:
        for part in slash_parts:
            if re.match(r'^\d+$', part):
                return part
            if part.lower() in NUMBER_WORDS:
                return NUMBER_WORDS[part.lower()]
    s = re.sub(r'\(th\)', 'th', s)
    return s.strip()


def answers_match(a: str, b: str) -> bool:
    na = normalize_answer(a)
    nb = normalize_answer(b)
    if na == nb:
        return True
    if na.upper() == nb.upper():
        return True
    if na.replace(" ", "").upper() == nb.replace(" ", "").upper():
        return True
    # Handle "24(th)" vs "24th"
    na_clean = re.sub(r'\(th\)|th', '', na, flags=re.I)
    nb_clean = re.sub(r'\(th\)|th', '', nb, flags=re.I)
    if na_clean == nb_clean:
        return True
    # Number word alternatives
    if re.match(r'^\d+$', na) and nb.lower() in NUMBER_WORDS:
        if na == NUMBER_WORDS[nb.lower()]:
            return True
    if re.match(r'^\d+$', nb) and na.lower() in NUMBER_WORDS:
        if nb == NUMBER_WORDS[na.lower()]:
            return True
    # Multi-letter sets (IN EITHER ORDER): "A/E" vs "A,E" vs "E/A"
    na_letters = set(re.findall(r'[A-G]', na.upper()))
    nb_letters = set(re.findall(r'[A-G]', nb.upper()))
    if len(na_letters) >= 2 and na_letters == nb_letters:
        return True
    # MC: "C" vs "C. 1926." — single letter matches first letter of JSON option
    if re.match(r'^[A-Ga-g]$', na) and nb and na.upper() == nb[0].upper():
        return True
    if re.match(r'^[A-Ga-g]$', nb) and na and nb.upper() == na[0].upper():
        return True
    # TFNG abbreviations: "F" vs "FALSE", "T" vs "TRUE", "NOT" vs "NOT GIVEN", "NG" vs "NOT GIVEN"
    tfng_expansions = {
        "T": "TRUE", "F": "FALSE", "N": "NOT GIVEN", "NG": "NOT GIVEN",
        "Y": "YES", "NO": "NO", "NOT": "NOT GIVEN",
    }
    if na.upper() in tfng_expansions and tfng_expansions[na.upper()] == nb.upper():
        return True
    if nb.upper() in tfng_expansions and tfng_expansions[nb.upper()] == na.upper():
        return True
    # Partial word match: "leaves/bark" vs "leaves (and) bark"
    if "/" in na or "/" in nb:
        na_parts = set(re.split(r'[/()]|\band\b', na, flags=re.I))
        nb_parts = set(re.split(r'[/()]|\band\b', nb, flags=re.I))
        na_clean_set = {p.strip().lower() for p in na_parts if p.strip()}
        nb_clean_set = {p.strip().lower() for p in nb_parts if p.strip()}
        if na_clean_set and na_clean_set == nb_clean_set:
            return True
        # One is subset of the other
        if na_clean_set and nb_clean_set:
            if na_clean_set.issubset(nb_clean_set) or nb_clean_set.issubset(na_clean_set):
                return True
    return False


# ═══════════════════════════════════════════════════════════════
# QUESTION TYPE MAP FROM JSON
# ═══════════════════════════════════════════════════════════════

def build_type_map(book_id: str) -> dict:
    """Build {test_num: {section: {q_num: answer_category}}} from JSON data.

    Categories: "letter", "word", "tfng", "ynng", "heading"
    """
    type_map: dict = {}

    for data_type in ["listening", "reading"]:
        json_path = BASE / "data" / "cambridge" / book_id / f"{data_type}.json"
        if not json_path.exists():
            continue

        data = load_json(json_path)
        for test in data.get("tests", []):
            test_id = test.get("id", "")
            tm = re.search(r"t(\d)$", test_id)
            if not tm:
                continue
            test_num = int(tm.group(1))
            if test_num not in type_map:
                type_map[test_num] = {}

            qs = []
            for container in test.get("parts", test.get("passages", [])):
                qs.extend(container.get("questions", []))

            for q in qs:
                qid = q.get("id", "")
                qm = re.search(r"q(\d+)$", qid)
                if not qm:
                    continue
                q_num = int(qm.group(1))
                qtype = q.get("type", "")

                if qtype in LETTER_TYPES:
                    category = "letter"
                elif qtype in WORD_TYPES:
                    category = "word"
                elif qtype in TFNG_TYPES:
                    category = "tfng"
                elif qtype in YNNG_TYPES:
                    category = "ynng"
                elif qtype in HEADING_TYPES:
                    category = "heading"
                else:
                    category = "word"  # Default: treat as word answer

                type_map[test_num].setdefault(data_type, {})[q_num] = category

    return type_map


def format_type_hints(test_num: int, section: str, type_map: dict) -> str:
    """Format question-type hints for the VLM prompt."""
    if test_num not in type_map or section not in type_map[test_num]:
        return ""

    qtypes = type_map[test_num][section]
    letter_qs = sorted([n for n, t in qtypes.items() if t == "letter"])
    word_qs = sorted([n for n, t in qtypes.items() if t == "word"])
    tfng_qs = sorted([n for n, t in qtypes.items() if t in ("tfng", "ynng")])
    heading_qs = sorted([n for n, t in qtypes.items() if t == "heading"])

    parts = []
    if letter_qs:
        parts.append(f"Questions {_format_ranges(letter_qs)}: answer is a SINGLE LETTER (A-G)")
    if word_qs:
        parts.append(f"Questions {_format_ranges(word_qs)}: answer is a WORD/PHRASE (extract FULL text)")
    if tfng_qs:
        parts.append(f"Questions {_format_ranges(tfng_qs)}: answer is TRUE/FALSE/NOT GIVEN or YES/NO/NOT GIVEN")
    if heading_qs:
        parts.append(f"Questions {_format_ranges(heading_qs)}: answer is a ROMAN NUMERAL (i, ii, iii, iv, v, vi, vii, viii, ix, x)")

    return "\n".join(parts)


def _format_ranges(nums: list) -> str:
    """Format a list of numbers as compact ranges: [1,2,3,5,6,7] → '1-3,5-7'."""
    if not nums:
        return ""
    ranges = []
    start = nums[0]
    end = nums[0]
    for n in nums[1:]:
        if n == end + 1:
            end = n
        else:
            ranges.append((start, end))
            start = n
            end = n
    ranges.append((start, end))
    return ",".join(f"{s}-{e}" if s != e else str(s) for s, e in ranges)


# ═══════════════════════════════════════════════════════════════
# METHOD A: TEXT-BASED EXTRACTION (cam17)
# ═══════════════════════════════════════════════════════════════

def parse_answer_key_text(text: str) -> dict:
    """Parse raw PDF text from Cambridge answer key pages."""
    results: dict = {}
    lines = text.split("\n")
    current_test = None
    current_section = None
    pending_number = None

    for line in lines:
        line = line.strip()

        tm = re.match(r"TEST\s+(\d)", line, re.I)
        if tm:
            current_test = int(tm.group(1))
            results.setdefault(current_test, {})
            pending_number = None
            continue

        if re.match(r"LISTENI?N?G$", line, re.I):
            current_section = "listening"
            if current_test and current_section not in results.get(current_test, {}):
                if current_test in results:
                    results[current_test][current_section] = {}
            pending_number = None
            continue

        if re.match(r"READING$", line, re.I):
            current_section = "reading"
            if current_test and current_section not in results.get(current_test, {}):
                if current_test in results:
                    results[current_test][current_section] = {}
            pending_number = None
            continue

        if current_test is None or current_section is None:
            continue

        if re.match(r"(Section|Part|Reading Passage|Questions)\s+\d", line, re.I):
            pending_number = None
            continue

        if any(kw in line for kw in ["If you score", "you are unlikely", "you may get",
                                       "you are likely", "acceptable score",
                                       "examination conditions", "recommend"]):
            continue

        if "Answer key" in line or "Resource Bank" in line:
            continue

        if re.match(r"^\d{3,}$", line):
            continue

        if pending_number is None:
            tab_match = re.match(r"(\d{1,2})\s{2,}(.+)", line)
            if tab_match:
                q_num = int(tab_match.group(1))
                answer = tab_match.group(2).strip()
                if 1 <= q_num <= 40 and len(answer) <= 80:
                    results[current_test].setdefault(current_section, {})
                    results[current_test][current_section][q_num] = clean_answer(answer)
                    continue

            single_match = re.match(r"(\d{1,2})\s+([A-Ga-g]|\S.*)$", line)
            if single_match:
                q_num = int(single_match.group(1))
                answer = single_match.group(2).strip()
                if 1 <= q_num <= 40 and answer not in ("0", "o", "O", "巾", "．", ".", ","):
                    if len(answer) <= 80:
                        results[current_test].setdefault(current_section, {})
                        results[current_test][current_section][q_num] = clean_answer(answer)
                        continue

            solo_num = re.match(r"^(\d{1,2})$", line)
            if solo_num:
                q_num = int(solo_num.group(1))
                if 1 <= q_num <= 40:
                    pending_number = q_num
                    continue

        if pending_number is not None:
            if 1 <= len(line) <= 80:
                if not re.match(r"^(Section|Part|Reading|Questions|Test|If|you|LISTEN|READ)", line, re.I):
                    if not re.match(r"^\d{1,2}$", line):
                        results[current_test].setdefault(current_section, {})
                        results[current_test][current_section][pending_number] = clean_answer(line)
                        pending_number = None

    return results


def clean_answer(raw: str) -> str:
    s = str(raw).strip()
    s = s.replace('．', '').replace('巾', '').replace('\t', ' ').strip()
    s = re.sub(r'\s+', ' ', s)
    s = re.sub(r'\s*IN\s+EITHER\s+ORDER\s*', '', s, flags=re.I).strip()
    return s


def extract_text_based(book_id: str) -> dict:
    pdf_path = PDF_DIR / f"{book_id}_questions.pdf"
    if not pdf_path.exists():
        return {}
    doc = fitz.open(str(pdf_path))
    all_text = ""
    for pg in ANSWER_KEY_PAGE_RANGE:
        if pg < doc.page_count:
            all_text += doc[pg].get_text()
    doc.close()
    return parse_answer_key_text(all_text)


# ═══════════════════════════════════════════════════════════════
# METHOD B: VLM-BASED EXTRACTION (with question-type guidance)
# ═══════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════
# METHOD B: VLM-BASED EXTRACTION (single pass, post-processed)
# ═══════════════════════════════════════════════════════════════

EXTRACT_PROMPT = """Extract ALL IELTS answer keys from this page exactly as printed.

This page is from a Cambridge IELTS book. It contains answer keys numbered 1-40.

CRITICAL: Transcribe the answers EXACTLY. Do NOT shorten or interpret.
- If the printed answer is a LETTER (A, B, C, D, E, F, G), output just the letter: 11.A
- If the printed answer is a WORD like "creativity" or "furniture", output the FULL word: 1.creativity
- If the printed answer is TRUE/FALSE/NOT GIVEN, output the full phrase: 8.TRUE
- If the printed answer has a "/" (like "A/E" for IN EITHER ORDER), keep the "/": 23.A/E

Output format — ONE line per test+section with ALL 40 answers:
TestN Listening: 1.answer1 2.answer2 3.answer3 ... 40.answer40
TestN Reading: 1.answer1 2.answer2 3.answer3 ... 40.answer40

Examples of correct output:
Test1 Listening: 1.Canadian 2.furniture 3.Park 4.250 5.phone 6.10(th) September 7.museum 8.time 9.blond(e) 10.87954 82361 11.B 12.A 13.B 14.C 15.A ... 40.migration
Test1 Reading: 1.creativity 2.rules 3.cities 4.traffic 5.crime 6.competition 7.evidence 8.TRUE 9.FALSE 10.NOT GIVEN 11.FALSE 12.NOT GIVEN 13.TRUE 14.E 15.C ... 40.characteristics

For pages showing answers from both sections, output BOTH TestN Listening AND TestN Reading lines.
Do NOT add commentary — only output the answer key lines."""


def extract_vlm_based(book_id: str, type_map: dict) -> dict:
    """Extract answer keys using VLM with post-processing correction."""
    pdf_path = PDF_DIR / f"{book_id}_questions.pdf"
    if not pdf_path.exists():
        print(f"  {book_id}: questions PDF not found")
        return {}

    doc = fitz.open(str(pdf_path))
    total = doc.page_count
    results: dict = {}
    found_pages = []

    for pg in range(max(110, 0), min(total, 135)):
        img_b64 = render_jpeg(doc, pg, dpi=150)
        if not img_b64:
            continue

        # Quick detection
        check = vlm_call(img_b64,
            "Does this page contain IELTS answer keys (numbered 1-40 with answers)? Reply YES or NO.",
            max_tokens=16)

        if not check or "YES" not in check.upper():
            continue

        found_pages.append(pg + 1)
        print(f"    p{pg+1}: extracting...", end=" ", flush=True)

        # Full extraction at higher DPI
        img_hq = render_jpeg(doc, pg, dpi=200)
        extracted = vlm_call(img_hq, EXTRACT_PROMPT, max_tokens=2048)

        if extracted:
            parsed = parse_vlm_output(extracted)
            for test_num, sections in parsed.items():
                results.setdefault(test_num, {})
                for section, answers in sections.items():
                    results[test_num].setdefault(section, {}).update(answers)
            n_answers = sum(
                len(answers) for sections in parsed.values()
                for answers in sections.values()
            )
            print(f"{n_answers} answers")
        else:
            print("FAILED")

        time.sleep(0.3)

    doc.close()

    if not found_pages:
        print(f"    No answer key pages found in pages 111-134")
        return {}

    # Post-process: apply type-based corrections
    results = post_process_results(results, type_map)

    return results


def post_process_results(results: dict, type_map: dict) -> dict:
    """Apply question-type-based corrections to VLM output.

    Corrections:
    - MC/letter questions: if answer is "B. option text", extract just "B"
    - TFNG questions: expand "F" to "FALSE", "T" to "TRUE", "NG" to "NOT GIVEN"
    - YNNG questions: expand "Y" to "YES", "N" to "NO", "NG" to "NOT GIVEN"
    - Word questions: no correction (can't fix single-letter truncation without guessing)
    """
    tfng_expand = {"T": "TRUE", "F": "FALSE", "N": "NOT GIVEN", "NG": "NOT GIVEN",
                   "NOT": "NOT GIVEN"}
    ynng_expand = {"Y": "YES", "N": "NO", "NG": "NOT GIVEN", "NOT": "NOT GIVEN"}

    for test_num, sections in results.items():
        for section, answers in sections.items():
            if test_num not in type_map or section not in type_map[test_num]:
                continue
            qtypes = type_map[test_num][section]

            for q_num, answer in list(answers.items()):
                qtype = qtypes.get(q_num, "word")
                orig = str(answer).strip()

                if qtype == "letter":
                    # Extract just the letter from "B. option text" or "B option text"
                    letter_match = re.match(r'^([A-Ga-g])\b', orig)
                    if letter_match and len(orig) > 2:
                        answers[q_num] = letter_match.group(1).upper()

                elif qtype == "tfng":
                    upper = orig.upper()
                    if upper in tfng_expand:
                        answers[q_num] = tfng_expand[upper]

                elif qtype == "ynng":
                    upper = orig.upper()
                    if upper in ynng_expand:
                        answers[q_num] = ynng_expand[upper]

    return results


def parse_vlm_output(text: str) -> dict:
    """Parse VLM extraction output into structured answer dict."""
    results: dict = {}
    current_test = None
    current_section = None

    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue

        header_match = re.match(r"Test\s*(\d)\s+(Listening|Reading)\s*:?\s*(.*)", line, re.I)
        if header_match:
            current_test = int(header_match.group(1))
            current_section = header_match.group(2).lower()
            results.setdefault(current_test, {}).setdefault(current_section, {})
            tail = header_match.group(3)
            if tail:
                _parse_answer_tokens(tail, results[current_test][current_section])
            continue

        tm = re.match(r"Test\s*(\d)\s*$", line, re.I)
        if tm:
            current_test = int(tm.group(1))
            results.setdefault(current_test, {})
            continue

        if re.match(r"Listening\s*:?\s*$", line, re.I):
            current_section = "listening"
            if current_test and current_section not in results.get(current_test, {}):
                if current_test in results:
                    results[current_test][current_section] = {}
            continue
        if re.match(r"Reading\s*:?\s*$", line, re.I):
            current_section = "reading"
            if current_test and current_section not in results.get(current_test, {}):
                if current_test in results:
                    results[current_test][current_section] = {}
            continue

        ls_match = re.match(r"Listening\s*:?\s*(.+)", line, re.I)
        if ls_match:
            current_section = "listening"
            if current_test is not None:
                results.setdefault(current_test, {}).setdefault(current_section, {})
                _parse_answer_tokens(ls_match.group(1), results[current_test][current_section])
            continue
        rs_match = re.match(r"Reading\s*:?\s*(.+)", line, re.I)
        if rs_match:
            current_section = "reading"
            if current_test is not None:
                results.setdefault(current_test, {}).setdefault(current_section, {})
                _parse_answer_tokens(rs_match.group(1), results[current_test][current_section])
            continue

        if current_test is None or current_section is None:
            continue

        results.setdefault(current_test, {}).setdefault(current_section, {})
        _parse_answer_tokens(line, results[current_test][current_section])

    return results


def _parse_answer_tokens(text: str, target_dict: dict) -> None:
    """Parse tokens like '1.A 2.B 3.word 4.phrase ...' into target_dict."""
    tokens = re.findall(r"(\d{1,2})\s*[\.\s]\s*([A-Ga-g/]|[A-Ga-g]\S{0,3}|\S+)", text)
    for q_str, answer in tokens:
        q_num = int(q_str)
        if q_num < 1 or q_num > 40:
            continue
        answer = answer.strip().rstrip('.').rstrip(',')
        if re.match(r'^[A-Ga-g](/[A-Ga-g])?$', answer):
            answer = answer.upper()
        target_dict[q_num] = answer


# ═══════════════════════════════════════════════════════════════
# CROSS-VALIDATION
# ═══════════════════════════════════════════════════════════════

def cross_validate(extracted_keys: dict, book_id: str) -> tuple:
    """Compare extracted answer keys with JSON data."""
    mismatches = []
    stats = {"compared": 0, "matched": 0, "mismatched": 0}

    for data_type in ["listening", "reading"]:
        json_path = BASE / "data" / "cambridge" / book_id / f"{data_type}.json"
        if not json_path.exists():
            continue

        data = load_json(json_path)

        for test in data.get("tests", []):
            test_id = test.get("id", "")
            tm = re.search(r"t(\d)$", test_id)
            if not tm:
                continue
            test_num = int(tm.group(1))

            if test_num not in extracted_keys:
                continue
            if data_type not in extracted_keys[test_num]:
                continue

            expected = extracted_keys[test_num][data_type]

            qs = []
            for container in test.get("parts", test.get("passages", [])):
                qs.extend(container.get("questions", []))

            for q in qs:
                qid = q.get("id", "")
                qm = re.search(r"q(\d+)$", qid)
                if not qm:
                    continue
                q_num = int(qm.group(1))

                if q_num in expected:
                    stats["compared"] += 1
                    json_answer = str(q.get("correctAnswer", "")).strip()
                    key_answer = str(expected[q_num]).strip()

                    if answers_match(json_answer, key_answer):
                        stats["matched"] += 1
                    else:
                        stats["mismatched"] += 1
                        mismatches.append({
                            "book": book_id,
                            "test": test_num,
                            "section": data_type,
                            "question": qid,
                            "json_answer": json_answer,
                            "key_answer": key_answer,
                        })

    return stats, mismatches


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main() -> None:
    print("=" * 70)
    print("  ANSWER KEY EXTRACTOR v4 — Single-pass + post-processing")
    print("=" * 70)

    all_keys: dict = {}
    validation_results: dict = {}

    # ── Phase 1: Text-based (cam17) ──
    print("\n── Phase 1: Text-based extraction (cam17) ──")
    for book_id in ["cam17"]:
        print(f"\n  {book_id}...")
        keys = extract_text_based(book_id)
        if keys:
            total_ans = sum(len(a) for sections in keys.values() for a in sections.values())
            print(f"    Total answers: {total_ans}")
            all_keys[book_id] = keys
        else:
            print(f"    No answer keys extracted")

    # ── Phase 2: VLM-based with post-processing ──
    print("\n── Phase 2: VLM extraction with post-processing ──")
    for book_id in ["cam14", "cam15", "cam16", "cam18", "cam19"]:
        print(f"\n  {book_id} — building type map...")
        type_map = build_type_map(book_id)
        total_types = sum(
            len(qtypes) for tests in type_map.values()
            for qtypes in tests.values()
        )
        print(f"    Type map: {total_types} questions across {len(type_map)} tests")

        keys = extract_vlm_based(book_id, type_map)
        if keys:
            total_ans = sum(
                len(a) for sections in keys.values()
                for a in sections.values()
            )
            print(f"    Total answers: {total_ans}")
            all_keys[book_id] = keys
        else:
            print(f"    No answer keys extracted")

    # ── Phase 3: Cross-validate ──
    print("\n── Phase 3: Cross-validation against JSON data ──")
    for book_id, keys in sorted(all_keys.items()):
        print(f"\n  {book_id}...")
        stats, mismatches = cross_validate(keys, book_id)
        validation_results[book_id] = {"stats": stats, "mismatches": mismatches}
        total = stats["compared"]
        acc = f"{stats['matched'] / total * 100:.1f}%" if total > 0 else "N/A"
        print(f"    Compared: {total}, Matched: {stats['matched']}, "
              f"Mismatched: {stats['mismatched']} → Accuracy: {acc}")

        if mismatches:
            print(f"    Sample mismatches (first 6):")
            for m in mismatches[:6]:
                print(f"      {m['question']}: key='{m['key_answer'][:45]}' json='{m['json_answer'][:45]}'")

    # ── Save report ──
    report = {
        "version": "v3_type_guided",
        "extracted_keys": {
            book: {
                f"test{tn}": {
                    s: {str(q): a for q, a in sorted(answers.items())}
                    for s, answers in sorted(sections.items())
                }
                for tn, sections in sorted(keys.items())
            }
            for book, keys in sorted(all_keys.items())
        },
        "validation": validation_results,
        "summary": {
            "books_processed": len(all_keys),
            "total_compared": sum(v["stats"]["compared"] for v in validation_results.values()),
            "total_matched": sum(v["stats"]["matched"] for v in validation_results.values()),
            "total_mismatched": sum(v["stats"]["mismatched"] for v in validation_results.values()),
        },
    }

    total_c = report["summary"]["total_compared"]
    total_m = report["summary"]["total_matched"]
    acc = f"{total_m / total_c * 100:.1f}%" if total_c > 0 else "N/A"
    report["summary"]["overall_accuracy"] = acc

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n{'=' * 70}")
    print(f"  Report saved to: {OUTPUT}")
    print(f"  Books: {len(all_keys)} | Compared: {total_c} | "
          f"Matched: {total_m} | Mismatched: {report['summary']['total_mismatched']}")
    print(f"  Overall Accuracy: {acc}")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
