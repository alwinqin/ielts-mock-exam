#!/usr/bin/env python3
"""Inspect answer key PDF pages to understand why VLM fails to detect them."""

import json
import time
from pathlib import Path

import fitz
from PIL import Image

from vlm_client import PDF_DIR, render_jpeg, vlm_call

OUTPUT_DIR = Path(__file__).parent / "data" / "validation_reports" / "answer_key_samples"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Step 1: Extract sample pages from answer PDFs as actual JPEG files ──
print("=" * 60)
print("Extracting sample pages from answer PDFs for visual inspection...")
print("=" * 60)

samples = {}
for book_id in ["cam15", "cam16", "cam17", "cam18", "cam19"]:
    pdf_path = PDF_DIR / f"{book_id}_answers.pdf"
    if not pdf_path.exists():
        continue
    doc = fitz.open(str(pdf_path))
    total = doc.page_count
    print(f"\n{book_id}: {total} pages")

    # Extract pages from the last 30% (where answer keys typically are)
    # Also extract a few from the first pages for comparison
    pages_to_sample = []
    # First page
    pages_to_sample.append(0)
    # Pages from 60%-95% range
    for ratio in [0.60, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95]:
        p = int(total * ratio)
        if p < total and p not in pages_to_sample:
            pages_to_sample.append(p)

    for pg in pages_to_sample:
        # Save as JPEG for manual inspection
        mat = fitz.Matrix(1.0, 1.0)  # 72 DPI for fast extraction
        pix = doc[pg].get_pixmap(matrix=mat)
        out_path = OUTPUT_DIR / f"{book_id}_p{pg+1}.jpg"
        Image.frombytes("RGB", [pix.width, pix.height], pix.samples).save(str(out_path), quality=70)
        print(f"  Saved p{pg+1} → {out_path.name}")

        # Also save a high-res version for VLM testing
        img_b64 = render_jpeg(doc, pg, dpi=150)
        samples[f"{book_id}_p{pg+1}"] = img_b64

    doc.close()

# ── Step 2: Test diverse prompts on answer pages ──
print("\n" + "=" * 60)
print("Testing diverse prompts on answer key pages...")
print("=" * 60)

prompts = [
    ("detect", "Does this page contain IELTS answer keys (numbered 1-40 with letters A-G)? Reply ONLY 'YES' or 'NO'."),
    ("list_all", "List everything you see on this page. Be specific about numbers, letters, and their arrangement."),
    ("grid_check", "Describe the structure of this page. Is it a grid/table? How many columns and rows? What do the cells contain?"),
    ("raw_ocr", "Transcribe ALL text from this page verbatim. Do not skip anything."),
    ("high_res", "This is a high-resolution scan. Look at it very carefully and transcribe ALL text, especially small numbers and letters."),
]

results = {}
for page_key, img_b64 in list(samples.items())[:5]:  # Test on first 5 sample pages
    print(f"\n--- {page_key} ---")
    results[page_key] = {}
    for prompt_key, prompt_text in prompts:
        print(f"  [{prompt_key}] ", end="", flush=True)
        start = time.time()
        answer = vlm_call(img_b64, prompt_text, max_tokens=512 if prompt_key == "detect" else 2048)
        elapsed = time.time() - start
        results[page_key][prompt_key] = {
            "elapsed": round(elapsed, 1),
            "response": answer[:500] if answer else "NO RESPONSE",
        }
        print(f"{elapsed:.1f}s → {answer[:120] if answer else 'FAIL'}")
        time.sleep(0.5)

# ── Step 3: Analyze why detection fails ──
print("\n" + "=" * 60)
print("Analysis: Why does answer key detection fail?")
print("=" * 60)

detect_results = [(k, v["detect"]["response"]) for k, v in results.items() if "detect" in v]
yes_count = sum(1 for _, r in detect_results if "YES" in r.upper())
no_count = sum(1 for _, r in detect_results if "NO" in r.upper())
print(f"  Detection results: {yes_count} YES, {no_count} NO, {len(detect_results) - yes_count - no_count} unclear")

for k, r in detect_results:
    print(f"    {k}: {r[:100]}")

# ── Save results ──
report_path = OUTPUT_DIR / "answer_key_inspection.json"
with open(report_path, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nFull report saved to: {report_path}")
print(f"Sample images saved to: {OUTPUT_DIR}")
