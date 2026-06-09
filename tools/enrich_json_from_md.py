#!/usr/bin/env python3
"""
Enrich Cambridge IELTS JSON data with options and question text parsed from
VLM-extracted Markdown files.

Strategy: Parse MD files to extract structured question data (options, stems),
then match to existing JSON by question number. Preserve correctAnswer and
reading passage text. Create .bak backup before writing.

Usage:
  python3 enrich_json_from_md.py              # All 7 books
  python3 enrich_json_from_md.py cam19        # Single book
  python3 enrich_json_from_md.py --dry-run    # Report only, no write
"""

import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

from md_question_parser import (
    parse_listening_section,
    parse_reading_passage,
    SECTION_HDR,
    READING_PASSAGE_HDR,
)

BASE = Path(__file__).parent
EXTRACTED_DIR = BASE / "data" / "extracted"
CAMBRIDGE_DIR = BASE / "data" / "cambridge"


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def extract_q_number(qid):
    """Extract question number from ID like 'cam19_lt1_q11' -> 11."""
    m = re.search(r"q(\d+)$", qid)
    return int(m.group(1)) if m else None


def _pick_best_item(items, answer=None):
    """Pick the best parsed item: most options, then answer-in-options as tiebreaker."""
    if len(items) == 1:
        return items[0]
    best = items[0]
    best_score = len(best.get("options", []))
    for item in items[1:]:
        score = len(item.get("options", []))
        if score > best_score:
            best = item
            best_score = score
        elif score == best_score and answer:
            if answer in item.get("options", []):
                best = item
    return best


def _options_are_garbage(options):
    """Reject obviously corrupted options like ['A', 'A'] or ['A. B c D E']."""
    if not options or len(options) < 2:
        return False
    # Duplicate option labels
    seen = set()
    for o in options:
        letter = o[0] if o else ""
        if letter in seen:
            return True
        seen.add(letter)
    # All-in-one-line corruption: "A. B c D E" where text starts with another letter
    if len(options) == 1 and re.match(r"[A-H][\.\)_]\s+[B-H]\s", options[0]):
        return True
    return False


def _stem_is_garbage(stem):
    """Reject stems that are clearly page headers or navigational references."""
    if not stem:
        return True
    if stem.startswith("## Page"):
        return True
    if stem.startswith("->") or stem.startswith("=>"):
        return True
    return False


def segment_listening_md(text):
    """Split listening MD text into {part_num: text} chunks."""
    lines = text.split("\n")
    parts = {}
    current_part = None
    current_lines = []

    for line in lines:
        s = line.strip()
        m = re.match(r"(?:PART|SECT[A-Z]{1,4}N|SECTION)\s+(\d+)", s, re.I)
        if not m:
            m = re.match(r"Test\d+-listening-part(\d+)", s, re.I)
        if m:
            if current_part is not None and current_lines:
                parts[current_part] = "\n".join(current_lines)
            current_part = int(m.group(1))
            current_lines = [line]
        elif current_part is not None:
            current_lines.append(line)

    if current_part is not None and current_lines:
        parts[current_part] = "\n".join(current_lines)

    return parts


def segment_reading_md(text):
    """Split reading MD text into {passage_num: text} chunks.
    Stops at answer key sections to avoid overwriting passage content."""
    lines = text.split("\n")
    passages = {}
    current_passage = None
    current_lines = []

    for line in lines:
        s = line.strip()
        # Stop at answer key sections — they contain "Reading Passage N," headers
        # that would overwrite real passage content
        if re.match(r"Listening and Reading answer keys?", s, re.I):
            break

        m = READING_PASSAGE_HDR.match(s)
        if not m:
            m = re.match(r"Test\d+-reading-passage(\d+)", s, re.I)
        if m:
            if current_passage is not None and current_lines:
                passages[current_passage] = "\n".join(current_lines)
            current_passage = int(m.group(1))
            current_lines = [line]
        elif current_passage is not None:
            current_lines.append(line)

    if current_passage is not None and current_lines:
        passages[current_passage] = "\n".join(current_lines)

    return passages


def enrich_listening_test(data, test_num, md_text):
    """Enrich one listening test's parts from MD transcription."""
    sections = segment_listening_md(md_text)
    if not sections:
        print(f"    No PART/SECTION headers found in MD")
        return 0

    test = None
    for t in data.get("tests", []):
        if t.get("testNumber") == test_num:
            test = t
            break

    if not test:
        print(f"    Test {test_num} not found in JSON")
        return 0

    enriched_count = 0

    for part in test.get("parts", []):
        part_id = part.get("id", "")
        pm = re.search(r"p(\d+)$", part_id)
        part_num = int(pm.group(1)) if pm else None

        if part_num not in sections:
            continue

        section_text = sections[part_num]
        parsed = parse_listening_section(section_text)
        # parsed is {q_num: [parsed_items...]}

        for q in part.get("questions", []):
            q_num = extract_q_number(q.get("id", ""))
            if q_num is None or q_num not in parsed:
                continue

            qtype = q.get("type", "")
            items = parsed[q_num]
            if not items:
                continue

            # Use the best parsed item
            item = _pick_best_item(items, q.get("correctAnswer"))

            # Skip garbage parsed items that would corrupt existing data
            if _options_are_garbage(item.get("options", [])):
                continue
            if _stem_is_garbage(item.get("stem", "")):
                continue

            # MC / multi-select: enrich options AND question text
            if qtype in ("multiple_choice",) and item.get("options"):
                new_opts = item["options"]
                if new_opts:
                    q["options"] = new_opts
                    enriched_count += 1

                if item.get("stem"):
                    q["question"] = item["stem"]

            # Matching: enrich options
            elif qtype in ("matching",) and item.get("options"):
                new_opts = item["options"]
                if new_opts:
                    q["options"] = new_opts
                    enriched_count += 1

                if item.get("stem"):
                    q["question"] = item["stem"]

            # Notes/form/table completion: enrich question text
            elif qtype in ("notes_completion", "form_completion",
                          "table_completion", "sentence_completion",
                          "summary_completion", "flowchart_completion"):
                if item.get("stem"):
                    q["question"] = item["stem"]
                    enriched_count += 1

    return enriched_count


def enrich_reading_test(data, test_num, md_text):
    """Enrich one reading test's passages from MD transcription."""
    passages_md = segment_reading_md(md_text)
    if not passages_md:
        print(f"    No READING PASSAGE headers found in MD")
        return 0

    test = None
    for t in data.get("tests", []):
        if t.get("testNumber") == test_num:
            test = t
            break

    if not test:
        print(f"    Test {test_num} not found in JSON")
        return 0

    enriched_count = 0

    for passage in test.get("passages", []):
        p_id = passage.get("id", "")
        pm = re.search(r"p(\d+)$", p_id)
        p_num = int(pm.group(1)) if pm else None

        if p_num not in passages_md:
            continue

        passage_text = passages_md[p_num]
        parsed = parse_reading_passage(passage_text)
        # parsed is {q_num: [parsed_items...]}

        for q in passage.get("questions", []):
            q_num = extract_q_number(q.get("id", ""))
            if q_num is None or q_num not in parsed:
                continue

            qtype = q.get("type", "")
            items = parsed[q_num]
            if not items:
                continue

            item = _pick_best_item(items, q.get("correctAnswer"))

            # Skip garbage parsed items that would corrupt existing data
            if _options_are_garbage(item.get("options", [])):
                continue
            if _stem_is_garbage(item.get("stem", "")):
                continue

            # MC: enrich options
            if qtype in ("multiple_choice",) and item.get("options"):
                new_opts = item["options"]
                if new_opts:
                    q["options"] = new_opts
                    enriched_count += 1

                if item.get("stem"):
                    q["question"] = item["stem"]

            # TFNG/YNNG: enrich question statement text
            elif qtype in ("tfng", "ynng", "matching_info",
                          "matching_headings", "matching_names", "matching"):
                if item.get("options"):
                    new_opts = item["options"]
                    if new_opts:
                        q["options"] = new_opts
                        enriched_count += 1

                if item.get("stem"):
                    q["question"] = item["stem"]
                    enriched_count += 1

            # Completion types: enrich question text
            elif qtype in ("notes_completion", "summary_completion",
                          "table_completion", "sentence_completion",
                          "flowchart_completion", "diagram_labeling"):
                if item.get("stem"):
                    q["question"] = item["stem"]
                    enriched_count += 1

    return enriched_count


def enrich_book(book_id, dry_run=False):
    """Enrich one book's listening.json and reading.json from MD files."""
    print(f"\n{'=' * 50}")
    print(f"Processing {book_id}")
    print(f"{'=' * 50}")

    for section in ["listening", "reading"]:
        json_path = CAMBRIDGE_DIR / book_id / f"{section}.json"
        if not json_path.exists():
            print(f"  {section}.json not found — skip")
            continue

        data = load_json(json_path)
        total_enriched = 0

        for test_num in range(1, 5):
            md_path = EXTRACTED_DIR / book_id / f"test{test_num}" / f"{section}.md"
            if not md_path.exists():
                print(f"  test{test_num} {section}.md not found — skip")
                continue

            md_text = md_path.read_text(encoding="utf-8")
            print(f"  test{test_num} {section}: MD={len(md_text)} chars", end="")

            if section == "listening":
                enriched = enrich_listening_test(data, test_num, md_text)
            else:
                enriched = enrich_reading_test(data, test_num, md_text)

            total_enriched += enriched
            print(f" -> {enriched} questions enriched")

        # Also handle cam17 per-test JSON files
        if book_id == "cam17":
            for test_num in range(1, 5):
                per_test_path = CAMBRIDGE_DIR / book_id / f"{section}_test{test_num}.json"
                if not per_test_path.exists():
                    continue

                md_path = EXTRACTED_DIR / book_id / f"test{test_num}" / f"{section}.md"
                if not md_path.exists():
                    continue

                per_test_data = load_json(per_test_path)
                md_text = md_path.read_text(encoding="utf-8")

                print(f"  test{test_num} {section} (per-test): MD={len(md_text)} chars", end="")

                # cam17 per-test JSON has a different structure — test is at top level
                ptest_num = per_test_data.get("testNumber", test_num)
                if section == "listening":
                    enriched = enrich_listening_test(
                        {"tests": [per_test_data]}, ptest_num, md_text
                    )
                else:
                    enriched = enrich_reading_test(
                        {"tests": [per_test_data]}, ptest_num, md_text
                    )

                total_enriched += enriched
                print(f" -> {enriched} questions enriched")

                if not dry_run and enriched > 0:
                    backup = str(per_test_path) + ".bak"
                    if not os.path.exists(backup):
                        os.rename(str(per_test_path), backup)
                    save_json(per_test_path, per_test_data)

        print(f"  TOTAL {section}: {total_enriched} questions enriched")

        if not dry_run:
            backup = str(json_path) + ".bak"
            if not os.path.exists(backup):
                os.rename(str(json_path), backup)
            save_json(json_path, data)

    return total_enriched


def main():
    dry_run = "--dry-run" in sys.argv

    # Determine which books to process
    books = ["cam14", "cam15", "cam16", "cam17", "cam18", "cam19", "cam20"]
    for arg in sys.argv[1:]:
        if arg.startswith("cam"):
            books = [arg]
            break

    print("=" * 60)
    print("JSON Enrichment from VLM Markdown")
    if dry_run:
        print("DRY RUN — no files will be modified")
    print(f"Books: {', '.join(books)}")
    print("=" * 60)

    grand_total = 0
    for book_id in books:
        enriched = enrich_book(book_id, dry_run=dry_run)
        grand_total += enriched

    print(f"\n{'=' * 60}")
    print(f"Grand total: {grand_total} questions enriched across {len(books)} books")
    if dry_run:
        print("DRY RUN — no files written")
    else:
        print("Backups saved as .json.bak")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
