#!/usr/bin/env python3
"""Find actual answer key pages in Chinese study guide PDFs and test extraction."""

import base64
import io
import json
import time
from pathlib import Path

import fitz
import requests
from PIL import Image

API_URL = "http://100.114.112.77:8000/v1/chat/completions"
MODEL = "Gemma-4-26B-A4B-it"
PDF_DIR = Path(__file__).parent / "data" / "cambridge" / "pdf"
OUTPUT_DIR = Path(__file__).parent / "data" / "validation_reports" / "answer_key_samples"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def render_jpeg(doc, pg, dpi=200):
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = doc[pg].get_pixmap(matrix=mat)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return base64.b64encode(buf.getvalue()).decode(), len(buf.getvalue())

def vlm_call(img_b64, prompt, max_tokens=2048):
    for attempt in range(3):
        try:
            resp = requests.post(
                API_URL,
                headers={"Content-Type": "application/json"},
                json={
                    "model": MODEL,
                    "messages": [{"role": "user", "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}},
                    ]}],
                    "max_tokens": max_tokens,
                    "temperature": 0.0,
                },
                timeout=120,
            )
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"]
            time.sleep(min((attempt + 1) * 5, 30))
        except Exception:
            time.sleep(3)
    return None

# ── Strategy 1: Look at pages 119-126 for cam15 (as stated in README) ──
print("=" * 70)
print("Strategy 1: Check known answer key page ranges (cam15 p119-126)")
print("=" * 70)

cam15 = PDF_DIR / "cam15_answers.pdf"
doc = fitz.open(str(cam15))
total = doc.page_count
print(f"Total pages: {total}")

answer_key_results = []

for pg in range(118, min(130, total)):  # Pages 119-130 (0-indexed: 118-129)
    img_b64, img_bytes = render_jpeg(doc, pg, dpi=200)
    print(f"\np{pg+1} ({img_bytes//1024}KB JPEG @ 200DPI) ...")

    # Save a low-res copy for visual inspection
    mat_low = fitz.Matrix(1.5, 1.5)
    pix_low = doc[pg].get_pixmap(matrix=mat_low)
    img_path = OUTPUT_DIR / f"cam15_answer_p{pg+1}.jpg"
    Image.frombytes("RGB", [pix_low.width, pix_low.height], pix_low.samples).save(str(img_path), quality=80)

    # Test: quick check if this is an answer key page
    check = vlm_call(img_b64, "Does this page show a list of answers numbered 1-40 with letters (A-G) as answers? Reply 'YES' or 'NO' and briefly explain.", max_tokens=128)
    print(f"  Check: {check}")

    if check and "YES" in check.upper():
        # Full extraction
        extract_prompt = """Extract ALL the answer keys from this page. The answers are numbered 1-40 with letter answers (A, B, C, D, E, F, G).

Output format for EACH row:
Test N (Listening or Reading):
1.A  2.B  3.C  4.D  5.E  6.F  7.G  8.A  9.B  10.C
11.D  12.E  13.F  14.G  15.A  16.B  17.C  18.D  19.E  20.F
21.G  22.A  23.B  24.C  25.D  26.E  27.F  28.G  29.A  30.B
31.C  32.D  33.E  34.F  35.G  36.A  37.B  38.C  39.D  40.E

Extract EVERY answer exactly as shown. Do not skip any numbers."""
        result = vlm_call(img_b64, extract_prompt, max_tokens=2048)
        answer_key_results.append({
            "book": "cam15",
            "page": pg + 1,
            "extraction": result,
        })
        print(f"  EXTRACTION ({len(result)} chars):")
        print(f"  {result[:500]}")
        time.sleep(0.3)

    time.sleep(0.3)

doc.close()

# ── Strategy 2: Try a different prompt approach ──
print("\n" + "=" * 70)
print("Strategy 2: Grid-based extraction prompt")
print("=" * 70)

# The answer keys might be in a table format with columns
# Test: "Test 1 Listening | Section 1 | 1.B 2.C ..." type layout
doc = fitz.open(str(cam15))

# Try page 120 specifically (often the first answer key page)
for pg in [119, 120, 121, 122, 123, 124, 125]:
    img_b64, img_bytes = render_jpeg(doc, pg, dpi=200)
    print(f"\np{pg+1} — trying grid-aware extraction ...")

    grid_prompt = """Look VERY CAREFULLY at this page. I need to extract IELTS answer keys.

IELTS answer keys typically look like:
- A small table or list with numbers 1-40 down the left
- Letters (A, B, C, D, E, F, G) next to each number
- Headers like "Test 1 Listening" or "Test 1 Reading"

Please describe EXACTLY what you see on this page, line by line. Pay special attention to:
1. Any numbered lists (1-40)
2. Any letters (A-G) appearing next to numbers
3. Section headers mentioning "Test" or "Listening" or "Reading"
4. Table structures with multiple columns

Be specific: if you see "1 B" or "1.B" anywhere, report it."""

    result = vlm_call(img_b64, grid_prompt, max_tokens=1024)
    print(f"  {result[:600] if result else 'NO RESPONSE'}")
    time.sleep(0.5)

doc.close()

# ── Strategy 3: Check other books for known answer key locations ──
print("\n" + "=" * 70)
print("Strategy 3: Sample multiple books at varied page ranges")
print("=" * 70)

# Answer keys in these study guides are often around 50-65% of the book
# (after the test explanations, before appendices)
books_to_check = {
    "cam16": [145, 158, 170],  # try known-adjacent pages
    "cam17": [150, 165, 178],
    "cam18": [160, 180, 195],
    "cam19": [148, 162, 175],
}

for book_id, pages in books_to_check.items():
    pdf_path = PDF_DIR / f"{book_id}_answers.pdf"
    if not pdf_path.exists():
        continue
    this_doc = fitz.open(str(pdf_path))
    total = this_doc.page_count
    print(f"\n{book_id}: {total} pages total")

    for pg in pages:
        if pg >= total:
            continue
        img_b64, img_bytes = render_jpeg(this_doc, pg, dpi=200)
        check = vlm_call(img_b64, "Does this page show IELTS answer keys (numbers 1-40 with letter answers A-G)? Reply 'YES' or 'NO'.", max_tokens=32)
        print(f"  p{pg+1}: {check[:80] if check else 'FAIL'}")
        if check and "YES" in check.upper():
            # Found! Extract
            extract = vlm_call(img_b64, "Extract ALL IELTS answer keys from this page. Format: '1.A 2.B 3.C ... 40.D'. Include test number and section (Listening/Reading).", max_tokens=2048)
            answer_key_results.append({
                "book": book_id,
                "page": pg + 1,
                "extraction": extract,
            })
            print(f"  → FOUND! Extraction: {extract[:300] if extract else 'FAIL'}")
        time.sleep(0.3)
    this_doc.close()

# ── Save findings ──
report_path = OUTPUT_DIR / "answer_key_findings.json"
with open(report_path, "w", encoding="utf-8") as f:
    json.dump(answer_key_results, f, ensure_ascii=False, indent=2)

print(f"\n{'=' * 70}")
print(f"Total answer key pages found: {len(answer_key_results)}")
print(f"Report saved to: {report_path}")
for r in answer_key_results:
    print(f"  {r['book']} p{r['page']}: {len(r.get('extraction', '') or '')} chars")
