#!/usr/bin/env python3
"""
Parse VLM-extracted IELTS Markdown into structured question data.

Pure functions — no file I/O, no side effects. Each parser accepts a text string
and returns list[dict] with {number, stem, options, qtype}.
Returns empty list when it cannot parse with high confidence.
"""

import re
from typing import List, Dict, Optional

# ── Shared regex patterns (proven in vlm_listening_pdf.py / fix_cam20_vlm.py) ──

MC_INLINE = re.compile(r"^(\d{1,2})\s+(.+)")                # "11 Stem text" (1+ spaces; dot filter blocks fill-in-blank)
MC_STANDALONE = re.compile(r"^(\d{1,2})$")                    # Bare number line
MC_OPTION = re.compile(r"^\s{2,}([A-H])\s{2,}(.+)")       # "      A    option"
MC_OPTION_DOT = re.compile(r"^\s{0,4}([A-H])[\.\)_]\s+(.+)")  # "A. option", "A) option", "A_ option"
MC_OPTION_FLAT = re.compile(r"^([A-H])\s+(.+)")              # "A option text"
MC_OPTION_LETTER = re.compile(r"^([A-H])$")                   # Bare "A" line (text extraction artifact)
MC_NEXT_Q = re.compile(r"^\d{1,2}\s+")                          # Next MC question start
FILL_DOTS = re.compile(r".*\b(\d{1,2})\b[^.]*[\.]{3,}")       # "1 ......" (rightmost number before dots)
FILL_CENTERED = re.compile(r"[\.]{3,}\s+(\d{1,2})\s+[\.]{3,}")  # "...... 38 ......"
MATCH_ITEM_DOTS = re.compile(r"^(\d+)\s+(.+?)\s+[\.]{3,}$")   # "16 Fundraising ......"
MULTI_SELECT_HDR = re.compile(r"Questions?\s+(\d+)\s*(?:and|[-–])\s*(\d+)", re.I)
PART_HDR = re.compile(r"(PART|SECTION)\s+(\d+)", re.I)
SECTION_HDR = re.compile(r"^(PART|SECT[A-Z]{1,4}N|SECTION|Questions?\s+\d+|READING PASSAGE)", re.I)
CHOOSE_MULTI = re.compile(r"Choose\s+(TWO|THREE)\s+letters?", re.I)
READING_PASSAGE_HDR = re.compile(r"READING PASSAGE\s+(\d+)", re.I)
BOX_HDR = re.compile(r"^\[Box[^\]]*\]", re.I)
PAGE_HDR = re.compile(r"^## Page\s+\d+", re.I)

SKIP_PREFIXES = (
    "PART", "Questions", "SECTION", "SECT", "Listening",
    "Complete", "Write", "Choose", "Test", "READING",
    "->", "=>",
)


def _clean_line(s: str) -> str:
    """Remove OCR noise characters from a line."""
    return re.sub(r"[®•@—\-–一]\s*", "", s).strip()


def _qnum(qn: int) -> bool:
    """Check if a number looks like a valid question number."""
    return 1 <= qn <= 40


# ═══════════════════════════════════════════════════════════════════════════════
# Listening question type parsers
# ═══════════════════════════════════════════════════════════════════════════════

def parse_notes_completion(text: str) -> List[Dict]:
    """Parse fill-in-the-blank questions from notes/table/form/summary sections.

    Handles: "Complete the notes/table/form/flow-chart below."
    Patterns:
      - "1 ................................" (dots after number on same line)
      - "...... 38 ......" (dots surrounding number)
      - "Postcode: 1 ......" (inline number with preceding context)

    Hierarchical context: looks backwards for section headings and shared lead-in
    phrases so that question stems are informative enough to answer independently.
    """
    items = []
    seen = set()
    lines = text.split("\n")

    # Bullet / marker prefixes used in notes layout
    _bullet_re = re.compile(r"^[®◎•一\-–—]\s*")
    # Lines that are purely instructions / headers (should not be used as context)
    _skip_context = re.compile(
        r"^(Choose|Write|Complete|Questions?\s+\d|Test\s*\d|READING|LISTENING"
        r"|PART\s|SECTION|SECT|## Page|\[Box)"
        r"|^\d{1,2}\s*$", re.I
    )

    for i, line in enumerate(lines):
        s = line.strip()

        # Strategy 0: dots surrounding number "...... 38 ......"
        m = FILL_CENTERED.search(s)
        if m:
            q_num = int(m.group(1))
            if _qnum(q_num) and q_num not in seen:
                seen.add(q_num)
                ctx = _gather_context(lines, i, s)
                items.append({"number": q_num, "stem": ctx, "options": [], "qtype": "notes_completion"})
            continue

        # Strategy 1: number followed eventually by 3+ dots
        m = FILL_DOTS.search(s)
        if not m:
            continue

        q_num = int(m.group(1))
        if not _qnum(q_num) or q_num in seen:
            continue

        # Find dots after the question number
        q_pos = m.start(1)
        try:
            dots_start = s.index("...", q_pos)
        except ValueError:
            dots_start = s.index("...")
        ctx = s[:dots_start].strip()
        ctx = _clean_line(ctx)

        after_dots = s[dots_start:].lstrip(".").strip()
        # Replace the question number with _____ for a readable blank
        ctx = re.sub(rf"\b{q_num}\b", "_____", ctx, count=1)
        if after_dots:
            ctx = f"{ctx} {after_dots}".strip()

        if any(ctx.startswith(kw) for kw in SKIP_PREFIXES):
            continue

        # Gather hierarchical context from surrounding lines
        ctx = _gather_context(lines, i, ctx, _skip_context)

        if ctx and len(ctx) > 1:
            seen.add(q_num)
            items.append({"number": q_num, "stem": ctx, "options": [], "qtype": "notes_completion"})

    return items


def _gather_context(lines, i, immediate_ctx, skip_re=None):
    """Look backwards from line i to build a meaningful question stem.

    Collects:
    1. Immediate line text (already in immediate_ctx)
    2. Shared lead-in phrase (a line that introduces bullet items)
    3. Section heading (title-like line further above)
    """
    if skip_re is None:
        skip_re = re.compile(r"^(Choose|Write|Complete|Questions?\s+\d|Test\s*\d|READING|LISTENING|PART\s|SECTION|SECT|## Page|\[Box)|^\d{1,2}\s*$", re.I)

    _bullet_re = re.compile(r"^[®◎•\-–—一]\s*")
    immediate_clean = _clean_line(immediate_ctx) if immediate_ctx else ""

    # Collect backward context: heading + lead-in
    heading = ""
    lead_in = ""
    found_lead = False
    # Track heading-like lines to detect section boundaries
    last_heading_candidate = ""

    for j in range(i - 1, max(i - 12, -1), -1):
        prev = lines[j].strip()
        if not prev or len(prev) <= 1:
            continue
        if skip_re.match(prev):
            break
        if FILL_DOTS.search(prev) or FILL_CENTERED.search(prev):
            continue  # skip other question lines but keep looking for shared context

        clean = _clean_line(prev)

        # Bullet line → keep looking
        if _bullet_re.match(prev):
            continue

        # Detect heading-like lines (short, capitalized, not a full sentence)
        is_heading_like = (
            len(clean) < 60
            and clean
            and clean[0].isupper()
            and not clean.endswith(".")
            and "......" not in clean
        )

        # Section boundary: we have the full context and hit another heading
        if is_heading_like and heading:
            break

        # Short title-like line → heading (closest context, stop scan)
        if not found_lead and is_heading_like:
            heading = clean
            break

        # Shared lead-in phrase
        if not found_lead and clean:
            lead_in = clean
            found_lead = True
            continue

        # Heading found after lead-in — keep lead_in as it sits between heading and question
        if found_lead and not heading and is_heading_like:
            heading = clean
            continue

    # Build final stem
    parts = []
    if heading and heading not in immediate_clean:
        parts.append(heading)
    if lead_in and lead_in not in immediate_clean:
        parts.append(lead_in)
    if immediate_clean and immediate_clean not in parts:
        parts.append(immediate_clean)

    return " | ".join(parts) if len(parts) > 1 else (parts[0] if parts else "")


def parse_multiple_choice(text: str) -> List[Dict]:
    """Parse single-answer MC questions.

    Matches: "Choose the correct letter, A, B or C."
    Format:  "11  Stem text\n    A   option text\n    B   option text\n    C   option text"
    """
    questions = []
    lines = text.split("\n")

    # Detect preamble options: shared options listed BEFORE individual question numbers
    # Pattern: "Questions 15-20" / "Choose ... A, B or C" / then A/B/C options / then "15 item..."
    preamble_opts = []
    found_letter_opts = False
    _re_letter_junk = re.compile(r"[B-H]\s+\w")  # "A. B c D E" → option text starts with another letter
    for j, line in enumerate(lines):
        s = line.strip()
        om = MC_OPTION_FLAT.match(s) or MC_OPTION_DOT.match(s)
        slm = MC_OPTION_LETTER.match(s)
        if om:
            opt_text = om.group(2).strip()
            # Filter corrupted combined-option lines like "A. B c D E"
            if not _re_letter_junk.match(opt_text):
                preamble_opts.append(f"{om.group(1)}. {opt_text}")
                found_letter_opts = True
        elif slm and j + 1 < len(lines):
            next_s = lines[j + 1].strip()
            if next_s and not SECTION_HDR.match(next_s) and not _re_letter_junk.match(next_s):
                preamble_opts.append(f"{slm.group(1)}. {next_s}")
                found_letter_opts = True
        elif found_letter_opts and (MC_STANDALONE.match(s) or MC_INLINE.match(s)):
            break  # options block ended, question numbers started
        elif s and not found_letter_opts:
            preamble_opts = []  # non-option line before any options found, reset

    i = 0

    while i < len(lines):
        s = lines[i].strip()

        q_num = None

        # Format A: standalone number on its own line (e.g. "11\nStem...\nA opt\nB opt")
        qm_a = MC_STANDALONE.match(s)
        if qm_a:
            q_num = int(qm_a.group(1))
            if not _qnum(q_num):
                i += 1
                continue
            # Skip page numbers: bare number right after ## Page header
            prev_line = lines[i - 1].strip() if i > 0 else ""
            if PAGE_HDR.match(prev_line):
                i += 1
                continue
            # Peek ahead: at least one option-like line within next 8 lines
            # MC_OPTION needs leading whitespace — use raw line
            has_opts = any(
                MC_OPTION.match(lines[j]) or MC_OPTION_DOT.match(lines[j])
                or MC_OPTION_FLAT.match(lines[j].strip()) or MC_OPTION_LETTER.match(lines[j].strip())
                for j in range(i + 1, min(i + 9, len(lines)))
            )
            if not has_opts and not preamble_opts:
                i += 1
                continue  # skip bare numbers that aren't MC question starts
            i += 1
            stem_parts = []
        else:
            # Format B: "11  Stem text..."
            qm_b = MC_INLINE.match(s)
            if qm_b:
                q_num = int(qm_b.group(1))
                if not _qnum(q_num):
                    i += 1
                    continue
                raw_stem = qm_b.group(2).strip()
                # Skip navigational references like "30 -> p. 128"
                if raw_stem.startswith("->") or raw_stem.startswith("=>"):
                    i += 1
                    continue
                # Skip if the line is mostly dots (fill-in-blank, not MC)
                if raw_stem.count(".") > len(raw_stem) * 0.3:
                    i += 1
                    continue
                stem_parts = [raw_stem]
                i += 1
            else:
                i += 1
                continue

        options = []

        while i < len(lines):
            raw_ns = lines[i]
            ns = raw_ns.strip()

            # Next question boundary
            if MC_NEXT_Q.match(ns) or MC_STANDALONE.match(ns):
                nxt_match = MC_STANDALONE.match(ns)
                if nxt_match and _qnum(int(nxt_match.group(1))):
                    break
                if MC_NEXT_Q.match(ns):
                    break

            # Section boundary
            if SECTION_HDR.match(ns):
                break

            # Option line: try indented first (needs raw), then dot/paren (works stripped)
            om = MC_OPTION.match(raw_ns) or MC_OPTION_DOT.match(ns) or MC_OPTION_FLAT.match(ns)
            if om:
                letter = om.group(1)
                opt_text = om.group(2).strip()
                # Normalize: strip existing letter prefix if present
                if opt_text.startswith(letter + ".") or opt_text.startswith(letter + " "):
                    options.append(opt_text)
                else:
                    options.append(f"{letter}. {opt_text}")
                i += 1
                continue

            # Standalone letter on its own line — peek at next line for option text
            slm = MC_OPTION_LETTER.match(ns)
            if slm and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line and not SECTION_HDR.match(next_line) and not MC_STANDALONE.match(next_line):
                    letter = slm.group(1)
                    options.append(f"{letter}. {next_line}")
                    i += 2
                    continue

            # Non-option, non-empty line before options => stem continuation
            if ns and not options and not ns.startswith("Choose") and not ns.startswith("Which"):
                stem_parts.append(ns)

            i += 1

        stem = " ".join(stem_parts).strip()
        final_opts = options if options else preamble_opts
        if stem and final_opts:
            questions.append({"number": q_num, "stem": stem, "options": final_opts, "qtype": "multiple_choice"})

    return questions


def parse_multi_select(text: str) -> List[Dict]:
    """Parse multi-select MC questions ("Choose TWO/THREE letters").

    Detected by headers like "Questions 21 and 22" + "Choose TWO letters" nearby.
    Returns one entry per question number, sharing stem and options.
    """
    questions = []
    lines = text.split("\n")

    # Find multi-select question blocks
    for i, line in enumerate(lines):
        s = line.strip()
        m = MULTI_SELECT_HDR.search(s)
        if not m:
            continue

        q1, q2 = int(m.group(1)), int(m.group(2))

        # Look for "Choose TWO/THREE letters" within next 3 lines
        has_choose = False
        for j in range(i + 1, min(i + 4, len(lines))):
            if CHOOSE_MULTI.search(lines[j]):
                has_choose = True
                break
        if not has_choose:
            continue

        # Find the stem text: from after the Questions header to first option
        stem_start = i + 1
        stem_lines = []
        options = []
        opts_started = False

        for j in range(stem_start, len(lines)):
            raw_ns = lines[j]
            ns = raw_ns.strip()
            if SECTION_HDR.match(ns) and "Questions" not in ns:
                break

            om = MC_OPTION.match(raw_ns) or MC_OPTION_DOT.match(ns) or MC_OPTION_FLAT.match(ns)
            if om:
                opts_started = True
                letter = om.group(1)
                opt_text = om.group(2).strip()
                if opt_text.startswith(letter + ".") or opt_text.startswith(letter + " "):
                    options.append(opt_text)
                else:
                    options.append(f"{letter}. {opt_text}")
                continue

            if opts_started and ns:
                break  # non-option after options started = end

            if not opts_started and ns:
                # Skip "Choose TWO letters" instruction lines
                if not CHOOSE_MULTI.search(ns):
                    stem_lines.append(ns)

        stem = " ".join(stem_lines).strip()
        if stem and options:
            for qn in range(q1, q2 + 1):
                if _qnum(qn):
                    questions.append({"number": qn, "stem": stem, "options": options, "qtype": "multiple_choice"})

    return questions


def parse_matching(text: str) -> List[Dict]:
    """Parse matching questions (box of options, numbered items with dots).

    Patterns:
      - "[Box containing text:]" or "Ways of reducing staff turnover" + options
      - Numbered items: "16 Fundraising ........................."
      - Map labeling: "15 coffee room ........................."
    """
    items = []
    lines = text.split("\n")

    # First pass: find option boxes
    # Options are lettered items (A-G or A-H) appearing before numbered dot-items
    box_options = []
    in_box = False
    for line in lines:
        s = line.strip()
        if BOX_HDR.search(s):
            in_box = True
            continue
        if in_box:
            m = re.match(r"^([A-Z])\s+(.+)", s)
            if m:
                box_options.append(f"{m.group(1)}. {m.group(2).strip()}")
            elif s and not re.match(r"^[A-Z]\s", s) and MATCH_ITEM_DOTS.match(s):
                in_box = False
            elif s and re.match(r"^\d+\s", s):
                in_box = False

    # If no [Box] header found, look for option-list patterns
    if not box_options:
        # Look for lines like "A experience on stage" before numbered items
        for i, line in enumerate(lines):
            s = line.strip()
            m = re.match(r"^([A-Z])\s+(.+)", s)
            if not m:
                continue
            # Check if subsequent lines also have letter prefixes
            letter_count = 1
            for j in range(i + 1, min(i + 12, len(lines))):
                ns = lines[j].strip()
                if re.match(r"^([A-Z])\s+(.+)", ns):
                    letter_count += 1
                else:
                    break
            if letter_count >= 3:
                for j in range(i, i + letter_count):
                    ls = lines[j].strip()
                    lm = re.match(r"^([A-Z])\s+(.+)", ls)
                    if lm:
                        box_options.append(f"{lm.group(1)}. {lm.group(2).strip()}")
                break

    # Second pass: find numbered items with dots
    for line in lines:
        s = line.strip()
        m = MATCH_ITEM_DOTS.match(s)
        if not m:
            continue
        q_num = int(m.group(1))
        if not _qnum(q_num):
            continue
        item_text = m.group(2).strip()
        items.append({
            "number": q_num,
            "stem": item_text,
            "options": list(box_options) if box_options else [],
            "qtype": "matching",
        })

    return items


# ═══════════════════════════════════════════════════════════════════════════════
# Reading question type parsers
# ═══════════════════════════════════════════════════════════════════════════════

def parse_tfng(text: str) -> List[Dict]:
    """Parse True/False/Not Given statements."""
    items = []
    lines = text.split("\n")

    in_tfng = False
    for line in lines:
        s = line.strip()
        if re.search(r"Do the following statements agree", s, re.I):
            in_tfng = True
            continue
        if not in_tfng:
            continue
        # Skip setup lines (instructions, answer boxes, TRUE/FALSE definitions)
        if re.match(r"^(In boxes|Write|TRUE|FALSE|NOT GIVEN|\d{1,2}\s*$)", s):
            continue
        m = re.match(r"^(\d{1,2})\s+(.+)", s)
        if m and _qnum(int(m.group(1))):
            items.append({
                "number": int(m.group(1)),
                "stem": m.group(2).strip(),
                "options": ["TRUE", "FALSE", "NOT GIVEN"],
                "qtype": "tfng",
            })
        elif s and re.match(r"^(Questions?\s+\d+|READING)", s, re.I):
            in_tfng = False

    return items


def parse_ynng(text: str) -> List[Dict]:
    """Parse Yes/No/Not Given statements."""
    items = []
    lines = text.split("\n")

    in_ynng = False
    for line in lines:
        s = line.strip()
        if re.search(r"Do the following statements agree with the claims", s, re.I):
            in_ynng = True
            continue
        if not in_ynng:
            continue
        # Skip setup lines
        if re.match(r"^(In boxes|Write|YES|NO|NOT GIVEN|\d{1,2}\s*$)", s):
            continue
        m = re.match(r"^(\d{1,2})\s+(.+)", s)
        if m and _qnum(int(m.group(1))):
            items.append({
                "number": int(m.group(1)),
                "stem": m.group(2).strip(),
                "options": ["YES", "NO", "NOT GIVEN"],
                "qtype": "ynng",
            })
        elif s and re.match(r"^(Questions?\s+\d+|READING)", s, re.I):
            in_ynng = False

    return items


def parse_matching_info(text: str) -> List[Dict]:
    """Parse paragraph/section information matching.

    Matches: "Which paragraph/section contains the following information?"
    Format: "14 description text ..."
    """
    items = []
    lines = text.split("\n")

    in_section = False
    opt_letters = []
    for line in lines:
        s = line.strip()
        if re.search(r"Which (paragraph|section) contains", s, re.I):
            in_section = True
            continue
        if in_section:
            # Extract option letters from "Write the correct letter, A-G, in boxes..."
            m = re.search(r"letter,?\s*([A-Z])[-–]([A-Z])", s)
            if m:
                start, end = ord(m.group(1)), ord(m.group(2))
                opt_letters = [chr(c) for c in range(start, end + 1)]
                continue
            if re.match(r"^(NB|You may use)", s):
                continue
            if re.match(r"^(In boxes|Write)", s):
                continue
            m = re.match(r"^(\d{1,2})\s+(.+)", s)
            if m and _qnum(int(m.group(1))):
                items.append({
                    "number": int(m.group(1)),
                    "stem": m.group(2).strip(),
                    "options": list(opt_letters) if opt_letters else [],
                    "qtype": "matching_info",
                })
            elif s and not m and not re.match(r"^(A-Z|Choose|Write|NB|In boxes)", s):
                in_section = False

    return items


def parse_matching_headings(text: str) -> List[Dict]:
    """Parse heading matching ("Choose the correct heading for each paragraph/section").

    Options are roman numerals (i, ii, iii...).
    """
    items = []
    lines = text.split("\n")

    # Find heading options (roman numeral list)
    roman_options = []
    in_options = False
    for line in lines:
        s = line.strip()
        if re.search(r"List of Headings", s, re.I):
            in_options = True
            continue
        if in_options:
            m = re.match(r"^([ivx]+)\.?\s+(.+)", s, re.I)
            if m:
                roman_options.append(f"{m.group(1).lower()}. {m.group(2).strip()}")
            elif s and not re.match(r"^[ivx]+", s, re.I):
                in_options = False

    # Find numbered items
    in_section = False
    for line in lines:
        s = line.strip()
        if re.search(r"Choose the correct heading for", s, re.I):
            in_section = True
            continue
        if in_section:
            if re.match(r"^(Reading Passage|List of|Write)", s, re.I):
                continue
            if re.match(r"^(In boxes|Choose)", s):
                continue
            m = re.match(r"^(\d{1,2})\s+(.+)", s)
            if m and _qnum(int(m.group(1))):
                items.append({
                    "number": int(m.group(1)),
                    "stem": m.group(2).strip(),
                    "options": list(roman_options) if roman_options else [],
                    "qtype": "matching_headings",
                })
            elif s and not re.match(r"^[ivx]+\b", s, re.I):
                in_section = False

    return items


def parse_matching_names(text: str) -> List[Dict]:
    """Parse person/name matching ("Match each statement with the correct person").

    Format: List of People with lettered names, then numbered statements.
    """
    items = []
    lines = text.split("\n")

    # Find name options
    people_options = []
    in_list = False
    for line in lines:
        s = line.strip()
        if re.search(r"List of (People|Researchers|Scientists|Thinkers)", s, re.I):
            in_list = True
            continue
        if in_list:
            m = re.match(r"^([A-Z])\s+(.+)", s)
            if m:
                people_options.append(f"{m.group(1)}. {m.group(2).strip()}")
            elif s and not re.match(r"^[A-Z]\s", s):
                in_list = False

    # Find numbered statements
    in_match = False
    for line in lines:
        s = line.strip()
        if re.search(r"Match each statement with the correct (person|researcher)", s, re.I):
            in_match = True
            continue
        if in_match:
            if re.match(r"^(NB|List of|Write|In boxes|Choose)", s, re.I):
                continue
            m = re.match(r"^(\d{1,2})\s+(.+)", s)
            if m and _qnum(int(m.group(1))):
                items.append({
                    "number": int(m.group(1)),
                    "stem": m.group(2).strip(),
                    "options": list(people_options) if people_options else [],
                    "qtype": "matching_names",
                })
            elif s and re.match(r"^(READING|Questions?\s+\d+)", s, re.I):
                in_match = False

    return items


def parse_summary_completion(text: str) -> List[Dict]:
    """Parse summary completion (gap-fill paragraph).

    Matches: "Complete the summary below."
    Format: "32 ........................................ of space can be achieved."
    """
    items = []
    lines = text.split("\n")

    in_summary = False
    for i, line in enumerate(lines):
        s = line.strip()
        if re.match(r"^Complete the (summary|sentences) below", s, re.I):
            in_summary = True
            continue
        if in_summary:
            if re.match(r"^Choose (NO MORE THAN|ONE WORD)", s, re.I):
                continue
            if re.match(r"^Write your answers", s, re.I):
                continue
            m = FILL_DOTS.search(s)
            if m:
                q_num = int(m.group(1))
                if _qnum(q_num):
                    q_pos = m.start(1)  # position of the matched question number
                    try:
                        dots_start = s.index("...", q_pos)
                    except ValueError:
                        dots_start = s.index("...")
                    ctx = s[:dots_start].strip()
                    after = s[dots_start:].lstrip(".").strip()
                    ctx = re.sub(rf"\b{q_num}\b", "_____", ctx, count=1)
                    if after:
                        ctx = f"{ctx} {after}".strip()
                    ctx = _gather_context(lines, i, ctx)
                    if ctx and len(ctx) > 1:
                        items.append({
                            "number": q_num, "stem": ctx,
                            "options": [], "qtype": "summary_completion",
                        })
            elif s and re.match(r"^(Questions?\s+\d+|READING)", s, re.I):
                in_summary = False

    return items


def parse_reading_multiple_choice(text: str) -> List[Dict]:
    """Parse reading MC questions (letter-only options in JSON).

    Same parsing as listening MC but options are stored as bare letters.
    """
    questions = parse_multiple_choice(text)
    for q in questions:
        # Extract just the letters from option text
        letters = [o[0].upper() for o in q["options"] if o]
        q["options"] = letters
        q["qtype"] = "multiple_choice"
    return questions


# ═══════════════════════════════════════════════════════════════════════════════
# High-level dispatch
# ═══════════════════════════════════════════════════════════════════════════════

def parse_listening_section(text: str) -> Dict[int, List[Dict]]:
    """Parse one listening section text, returning {qnumber: [parsed_question, ...]}.

    Each value is a list because some parsers return multiple entries for one
    logical question group (e.g. multi-select).
    """
    result = {}

    # Try each parser; parsers are conservative and return [] on no match
    parsers = [
        parse_multiple_choice,
        parse_multi_select,
        parse_matching,
        parse_notes_completion,
    ]

    for parser in parsers:
        parsed = parser(text)
        for item in parsed:
            # Filter navigational references like "30 -> p. 128"
            stem = item.get("stem", "")
            if isinstance(stem, str) and (stem.startswith("->") or stem.startswith("=>")):
                continue
            qn = item["number"]
            if qn not in result:
                result[qn] = []
            result[qn].append(item)

    return result

def parse_reading_passage(text: str) -> Dict[int, List[Dict]]:
    """Parse one reading passage's question text.

    Reading passages contain passage prose followed by questions. The prose is
    skipped; only question patterns are extracted.
    """
    result = {}

    parsers = [
        parse_notes_completion,
        parse_summary_completion,
        parse_tfng,
        parse_ynng,
        parse_reading_multiple_choice,
        parse_matching_info,
        parse_matching_headings,
        parse_matching_names,
        parse_matching,
    ]

    for parser in parsers:
        parsed = parser(text)
        for item in parsed:
            # Filter navigational references like "30 -> p. 128"
            stem = item.get("stem", "")
            if isinstance(stem, str) and (stem.startswith("->") or stem.startswith("=>")):
                continue
            qn = item["number"]
            if qn not in result:
                result[qn] = []
            result[qn].append(item)

    return result