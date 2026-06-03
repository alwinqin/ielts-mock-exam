#!/usr/bin/env python3
"""Targeted fix for cam20 listening data using Gemma VLM.

cam20 PDFs don't have "PART X Questions" headers like cam15-19.
Instead, questions are grouped by "Questions X-Y" or "Questions X and Y".
The listening section spans ~3 pages per test (pages 3-5).

Strategy:
1. Render listening pages (3-5) per test
2. VLM transcribe all text
3. Parse ALL MC and fill-blank from combined text
4. Match to JSON by question number (ignoring section boundaries)
5. Fix all bad questions in one pass per test
"""

import json
import os
import re
import sys
import time
import base64
import fitz
import requests

DATA_DIR = "data/cambridge"
PDF_DIR = os.path.join(DATA_DIR, "pdf")

API_URL = "http://100.114.112.77:8000/v1/chat/completions"
MODEL = "Gemma-4-26B-A4B-it"


def render_page(doc, page_num, dpi=150):
    page = doc[page_num]
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat)
    img_data = pix.tobytes("png")
    return base64.b64encode(img_data).decode()


def vlm_transcribe(img_b64):
    prompt = (
        "Transcribe ALL text from this IELTS listening test page verbatim. "
        "Preserve the exact layout: headers, question numbers, options (A/B/C/D/E/F/G/H), "
        "fill-blank dots (......), and all body text. "
        "Output the raw text only — no markdown, no explanations, no JSON."
    )

    for attempt in range(4):
        try:
            resp = requests.post(
                API_URL,
                headers={"Content-Type": "application/json"},
                json={
                    "model": MODEL,
                    "messages": [{"role": "user", "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}},
                    ]}],
                    "max_tokens": 4096,
                    "temperature": 0.1,
                },
                timeout=180,
            )
            if resp.status_code == 200:
                data = resp.json()
                return data["choices"][0]["message"]["content"]
            if resp.status_code == 429:
                time.sleep(min((attempt + 1) * 10, 60))
                continue
            print(f"      API error {resp.status_code}: {resp.text[:100]}")
            if attempt < 3:
                time.sleep(3 * (attempt + 1))
        except Exception as e:
            print(f"      Error (attempt {attempt + 1}/4): {type(e).__name__}: {str(e)[:100]}")
            time.sleep(3 * (attempt + 1))
    return None


def parse_all_mc(text):
    """Parse ALL MC questions from text using multiple strategies."""
    questions = []

    # Strategy 1: "11 Stem text\nA option\nB option" (number inline with 1+ spaces)
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        s = lines[i].strip()

        # Inline format: "11 According to..." or "22.Text..."
        qm = re.match(r"^(\d{1,2})[\.\s]([A-Z].+)", s)
        if not qm:
            # Standalone format: "11\n" then stem on next line
            qm2 = re.match(r"^(\d{1,2})$", s)
            if qm2:
                q_num = int(qm2.group(1))
                if 1 <= q_num <= 40:
                    i += 1
                    stem_parts = []
                    options = []
                    while i < len(lines):
                        ns = lines[i].strip()
                        if re.match(r"^\d{1,2}$", ns):
                            break
                        om = re.match(r"^([A-H])[\.\s]\s*(.+)", ns)
                        if om:
                            options.append(f"{om.group(1)}. {om.group(2).strip()}")
                        elif ns and not options:
                            stem_parts.append(ns)
                        i += 1
                    stem = " ".join(stem_parts).strip()
                    if stem and options:
                        questions.append({"number": q_num, "stem": stem, "options": options})
                    continue
            i += 1
            continue

        q_num = int(qm.group(1))
        if not (1 <= q_num <= 40):
            i += 1
            continue

        stem_parts = [qm.group(2).strip()]
        options = []
        i += 1

        while i < len(lines):
            ns = lines[i].strip()
            if re.match(r"^\d{1,2}[\.\s][A-Z]", ns) or re.match(r"^(\d{1,2})$", ns):
                break
            om = re.match(r"^([A-H])[\.\s]\s*(.+)", ns)
            if om:
                options.append(f"{om.group(1)}. {om.group(2).strip()}")
            elif ns and not options:
                stem_parts.append(ns)
            i += 1

        stem = " ".join(stem_parts).strip()
        if stem and options:
            questions.append({"number": q_num, "stem": stem, "options": options})

    return questions


def parse_multi_mc(text):
    """Parse multi-select MC (choose TWO from A-E, question numbers shared)."""
    questions = []
    lines = text.split("\n")

    for i, line in enumerate(lines):
        s = line.strip()

        # Detect: "Questions 19 and 20" or "17 - 18"
        m = re.match(r"(?:Questions?\s+)?(\d+)\s*(?:and|[-–])\s*(\d+)", s, re.IGNORECASE)
        if not m:
            # Also try: "Questions 25 and 26" on one line then "25 - 26" on next
            if re.match(r"Questions?\s+\d+\s+and\s+\d+", s, re.IGNORECASE):
                q_nums_match = re.findall(r"(\d+)", s)
                if len(q_nums_match) >= 2:
                    q_start, q_end = int(q_nums_match[0]), int(q_nums_match[1])
                else:
                    continue
            else:
                continue
        else:
            q_start, q_end = int(m.group(1)), int(m.group(2))

        # Check for multi-select indicator nearby
        has_multi = False
        for j in range(i, min(i + 3, len(lines))):
            if re.search(r"Choose\s+\w+\s+letters?", lines[j], re.IGNORECASE):
                has_multi = True
                break
        if not has_multi:
            continue

        # Find stem and options
        stem = ""
        options = []
        j = i + 1
        while j < len(lines):
            ns = lines[j].strip()
            if re.match(r"Choose\s+", ns, re.IGNORECASE):
                j += 1
                continue
            if not ns:
                j += 1
                continue

            om = re.match(r"^([A-H])[\.\s]\s*(.+)", ns)
            if om:
                if not stem:
                    for k in range(j - 1, i, -1):
                        prev = lines[k].strip()
                        if prev and not re.match(r"^(Choose|Questions?\s+\d+)", prev, re.IGNORECASE):
                            stem = prev
                            break
                options.append(f"{om.group(1)}. {om.group(2).strip()}")
                j += 1
                continue

            if re.match(r"^(Questions?\s+\d+|READING|Test\s*\d)", ns, re.IGNORECASE):
                break
            j += 1

        if stem and options:
            for q_num in range(q_start, q_end + 1):
                questions.append({"number": q_num, "stem": stem, "options": list(options)})

    return questions


def parse_all_fill(text):
    """Parse ALL fill-blank questions from text."""
    items = []
    seen = set()
    lines = text.split("\n")

    skip_prefixes = ("PART", "Questions", "SECTION", "READING", "Test", "Complete", "Choose")

    for i, line in enumerate(lines):
        s = line.strip()
        if not s or s.startswith("|"):
            continue

        # Strategy 0: "...... 38 ......" (number between two dot sequences)
        for m_dots in re.finditer(r"[\.]{3,}\s+(\d{1,2})\s+[\.]{3,}", s):
            q_num = int(m_dots.group(1))
            if 1 <= q_num <= 40 and q_num not in seen:
                ctx_before = s[:m_dots.start()].strip()
                ctx_before = re.sub(r"^[-•*]\s*", "", ctx_before)
                ctx_after = s[m_dots.end():].strip()
                ctx = f"{ctx_before} _____ {ctx_after}" if ctx_after else ctx_before
                if ctx and len(ctx) > 2:
                    items.append({"number": q_num, "context": ctx})
                    seen.add(q_num)
        if any(1 for _ in re.finditer(r"[\.]{3,}\s+(\d{1,2})\s+[\.]{3,}", s)):
            continue

        # Strategy 1: number before dots
        m = re.search(r"\b(\d{1,2})\b[^.]*[\.]{3,}", s)
        if not m:
            continue

        q_num = int(m.group(1))
        if not (1 <= q_num <= 40):
            continue

        dots_start = s.index("...", m.start())
        ctx = s[:dots_start].strip()
        ctx = re.sub(r"[®•@—\-]\s*", "", ctx)

        # After-dots context for short prefixes
        after_dots = s[dots_start:].lstrip(".").strip()
        if after_dots and len(ctx) < 10:
            ctx = f"{ctx} _____ {after_dots}"
            if len(ctx) > 2:
                items.append({"number": q_num, "context": ctx})
            continue

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


def fix_cam20_test(test_num):
    """Fix one cam20 test using VLM."""
    pdf_path = os.path.join(PDF_DIR, f"cam20_test{test_num}_questions.pdf")
    if not os.path.exists(pdf_path):
        print(f"  PDF not found: {pdf_path}")
        return 0, 0

    json_path = os.path.join(DATA_DIR, "cam20", "listening.json")
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    # Get bad Qs for this test
    test_data = None
    for t in data.get("tests", []):
        if t.get("testNumber") == test_num:
            test_data = t
            break
    if not test_data:
        return 0, 0

    bad_qids = set()
    for part in test_data.get("parts", []):
        for q in part.get("questions", []):
            qt = q.get("type", "")
            if qt in ("multiple_choice", "multiple_choice_multi"):
                opts = q.get("options", [])
                if opts and all(len(str(o).strip()) <= 2 for o in opts):
                    bad_qids.add(q["id"])
            elif qt in ("notes_completion", "form_completion", "summary_completion", "sentence_completion"):
                qtext = q.get("question", "")
                if "Question" in qtext and "ONE WORD" in qtext:
                    bad_qids.add(q["id"])

    if not bad_qids:
        print(f"  Test {test_num}: no bad questions")
        return 0, 0

    print(f"  Test {test_num}: {len(bad_qids)} bad Qs")

    # Render and transcribe listening pages (start from page 2, covers Q11+)
    doc = fitz.open(pdf_path)
    page_texts = []

    for pg in range(1, min(8, doc.page_count)):
        first_lines = []
        # Quick detection: use first 3 pages for listening
        print(f"    Page {pg + 1}...", end=" ", flush=True)
        img_b64 = render_page(doc, pg)
        text = vlm_transcribe(img_b64)
        if text is None:
            print("FAILED")
            continue

        # Stop at reading section
        if re.match(r"^\s*(Test\s*\d|READING|Reading)", text.strip(), re.IGNORECASE):
            # "Test1-reading-passage1" style
            if re.search(r"reading.?passage", text[:200], re.IGNORECASE):
                print("READING - stop")
                break

        if len(text) > 5000:
            print(f"HALLUCINATION ({len(text)} chars) - skip")
            continue
        print(f"OK ({len(text)} chars)")
        page_texts.append(text)
        time.sleep(1.5)

    doc.close()

    if not page_texts:
        print(f"    No pages transcribed")
        return 0, 0

    merged_text = "\n".join(page_texts)
    parsed_mc = parse_all_mc(merged_text)
    parsed_mc += parse_multi_mc(merged_text)
    parsed_fill = parse_all_fill(merged_text)

    print(f"    Parsed: {len(parsed_mc)} MC, {len(parsed_fill)} fill")
    if parsed_mc:
        for q in parsed_mc[:5]:
            print(f"      MC Q{q['number']}: {q['stem'][:80]}...")

    mc_fixed = 0
    fill_fixed = 0

    if parsed_mc:
        mc_lookup = {}
        for q in parsed_mc:
            qn = q["number"]
            mc_lookup[qn] = q

        for part in test_data.get("parts", []):
            for q in part.get("questions", []):
                if q["id"] not in bad_qids:
                    continue
                if q["type"] not in ("multiple_choice", "multiple_choice_multi"):
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
                    mc_fixed += 1
                    print(f"      Fixed MC Q{q_num}")

    if parsed_fill:
        fill_lookup = {item["number"]: item for item in parsed_fill}
        for part in test_data.get("parts", []):
            for q in part.get("questions", []):
                if q["id"] not in bad_qids:
                    continue
                if q["type"] not in ("notes_completion", "form_completion", "summary_completion", "sentence_completion"):
                    continue
                qm = re.search(r"Question\s+(\d+)", q.get("question", ""))
                if not qm:
                    continue
                q_num = int(qm.group(1))
                if q_num in fill_lookup:
                    q["question"] = fill_lookup[q_num]["context"] + " _____"
                    fill_fixed += 1
                    print(f"      Fixed Fill Q{q_num}")

    if mc_fixed > 0 or fill_fixed > 0:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"    SAVED: {mc_fixed} MC + {fill_fixed} fill")

    return mc_fixed, fill_fixed


def main():
    total_mc = 0
    total_fill = 0

    for test_num in range(1, 5):
        print(f"\n--- cam20 Test {test_num} ---")
        mc, fill = fix_cam20_test(test_num)
        total_mc += mc
        total_fill += fill

    print(f"\nTotal: {total_mc} MC + {total_fill} fill = {total_mc + total_fill} fixed")
    print("Done!")


if __name__ == "__main__":
    main()
