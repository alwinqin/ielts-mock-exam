#!/usr/bin/env python3
"""Verify VLM (Gemma-4-26B-A4B-it) capabilities for OCR tasks."""

import base64
import io
import json
import time
import random
from pathlib import Path

import fitz
import requests
from PIL import Image

from vlm_client import VLM_API_URL, VLM_MODEL
BASE = Path(__file__).parent
PDF_DIR = BASE / "data" / "cambridge" / "pdf"
OUTPUT = BASE / "data" / "validation_reports" / "vlm_capability_report.json"

PROMPTS = {
    # ── Test 1: Pure OCR transcription (English) ──
    "ocr_pure_en": (
        "Transcribe ALL visible text from this IELTS exam page verbatim. "
        "Include EVERY word you see — questions, options, instructions, headings, page numbers. "
        "Preserve the original formatting as much as possible. "
        "Output raw text only, no commentary."
    ),
    # ── Test 2: Structured extraction ──
    "ocr_structured": (
        "Extract all IELTS questions from this page as a JSON array. "
        "For each question include: number, type, question text, options (if any). "
        'Format: [{"number": 1, "type": "multiple_choice", "question": "...", "options": ["A. ...", "B. ..."]}]'
    ),
    # ── Test 3: Layout understanding ──
    "layout_check": (
        "Analyze this IELTS page and describe its layout structure: "
        "1) How many columns? 2) Where are the questions located? "
        "3) Is there a passage/text body? 4) Any tables, diagrams, or special formatting? "
        "5) What section does this appear to be (Listening/Reading/Writing)?"
    ),
    # ── Test 4: Answer key extraction ──
    "answer_key": (
        "Does this page contain IELTS answer keys (numbered 1-40 with letter answers "
        "like '1 B' or '1.B')? If YES, extract ALL answers in format: "
        "'1.A 2.B 3.C ... 40.D'. If NO, reply ONLY 'NO'."
    ),
    # ── Test 5: Chinese+English mixed content ──
    "bilingual": (
        "This is an IELTS study page. Extract ALL text, both English AND Chinese. "
        "If there are explanatory notes in Chinese, include them fully. "
        "Preserve the language of each section."
    ),
    # ── Test 6: Fine-grained detail ──
    "fine_detail": (
        "Look at this page carefully. Report: "
        "1) The test number and section (e.g., 'Test 1, Reading Passage 1') "
        "2) All question numbers you can see "
        "3) Any images, graphs, or diagrams present? "
        "4) The font characteristics (bold/italic text, different sizes) "
        "5) Any footnotes or page numbers"
    ),
}

# ── Sample pages from different books ──
SAMPLE_PAGES = [
    # (book_id, test_num, page)
    ("cam15", 1, 8),   # Reading passage
    ("cam15", 1, 16),  # Reading questions
    ("cam16", 2, 25),  # Reading
    ("cam18", 3, 55),  # Listening
    ("cam19", 1, 10),  # Reading
]


def render_page_jpeg(pdf_path, page_num, dpi=120):
    """Render PDF page as base64 JPEG."""
    doc = fitz.open(str(pdf_path))
    if page_num >= doc.page_count:
        doc.close()
        return None
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = doc[page_num].get_pixmap(matrix=mat)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=80)
    doc.close()
    return base64.b64encode(buf.getvalue()).decode()


def vlm_call(img_b64, prompt, max_tokens=1024, temperature=0.0):
    """Single VLM call with timing."""
    start = time.time()
    try:
        resp = requests.post(
            VLM_API_URL,
            headers={"Content-Type": "application/json"},
            json={
                "model": VLM_MODEL,
                "messages": [{"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}},
                ]}],
                "max_tokens": max_tokens,
                "temperature": temperature,
            },
            timeout=120,
        )
        elapsed = time.time() - start
        if resp.status_code == 200:
            content = resp.json()["choices"][0]["message"]["content"]
            usage = resp.json().get("usage", {})
            return {
                "success": True,
                "latency_s": round(elapsed, 2),
                "tokens_prompt": usage.get("prompt_tokens", 0),
                "tokens_completion": usage.get("completion_tokens", 0),
                "content": content,
                "content_length": len(content),
            }
        else:
            return {"success": False, "latency_s": round(elapsed, 2), "error": f"HTTP {resp.status_code}", "body": resp.text[:200]}
    except Exception as e:
        return {"success": False, "latency_s": round(time.time() - start, 2), "error": str(e)[:200]}


def test_consistency(img_b64, prompt_key, prompt, n=3):
    """Run same prompt N times to measure output consistency."""
    results = []
    for i in range(n):
        print(f"    run {i+1}/{n}...", end=" ", flush=True)
        r = vlm_call(img_b64, prompt)
        results.append(r)
        print(f"{r['latency_s']}s" if r["success"] else f"FAIL: {r.get('error')}")
        if i < n - 1:
            time.sleep(0.3)
    return results


def test_token_limits(img_b64):
    """Test how context length affects response quality."""
    print("\n  Testing token limits...")
    results = {}
    for max_tok in [256, 512, 1024, 2048]:
        print(f"    max_tokens={max_tok} ...", end=" ", flush=True)
        r = vlm_call(img_b64, PROMPTS["ocr_pure_en"], max_tokens=max_tok)
        if r["success"]:
            results[max_tok] = {
                "latency_s": r["latency_s"],
                "content_length": r["content_length"],
                "tokens_completion": r.get("tokens_completion", 0),
            }
            print(f"output={r['content_length']} chars, {r['latency_s']}s")
        else:
            results[max_tok] = {"error": r.get("error")}
            print(f"FAIL: {r.get('error')}")
    return results


def test_multi_image():
    """Test if VLM supports multiple images in one request."""
    print("\n  Testing multi-image support...")
    pdf1 = PDF_DIR / "cam15_questions.pdf"
    pdf2 = PDF_DIR / "cam16_questions.pdf"
    if not pdf1.exists() or not pdf2.exists():
        return {"supported": False, "reason": "PDFs not found"}

    img1 = render_page_jpeg(pdf1, 8)
    img2 = render_page_jpeg(pdf2, 25)
    if not img1 or not img2:
        return {"supported": False, "reason": "Failed to render pages"}

    try:
        resp = requests.post(
            VLM_API_URL,
            headers={"Content-Type": "application/json"},
            json={
                "model": VLM_MODEL,
                "messages": [{"role": "user", "content": [
                    {"type": "text", "text": "Describe these two pages briefly — what test and section is each?"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img1}"}},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img2}"}},
                ]}],
                "max_tokens": 512,
                "temperature": 0.0,
            },
            timeout=120,
        )
        if resp.status_code == 200:
            content = resp.json()["choices"][0]["message"]["content"]
            return {"supported": True, "response": content[:300]}
        return {"supported": False, "error": f"HTTP {resp.status_code}"}
    except Exception as e:
        return {"supported": False, "error": str(e)[:200]}


def main():
    print("=" * 70)
    print("  VLM CAPABILITY VERIFICATION — Gemma-4-26B-A4B-it")
    print("=" * 70)

    report = {
        "model": VLM_MODEL,
        "endpoint": VLM_API_URL,
        "tests": {},
    }

    # ── Find a good test page ──
    test_pdf = PDF_DIR / "cam15_questions.pdf"
    if not test_pdf.exists():
        print("ERROR: cam15_questions.pdf not found!")
        return

    img_b64 = render_page_jpeg(test_pdf, 8)  # Reading passage page
    if not img_b64:
        print("ERROR: Failed to render page 8")
        return

    print(f"\n  Test page: cam15_questions.pdf page 9 (0-indexed: 8)")
    print(f"  Image size: ~{len(img_b64) // 1024} KB base64")

    # ═══ Test 1: OCR Raw Transcription ═══
    print("\n── Test 1: Pure OCR Transcription ──")
    r = vlm_call(img_b64, PROMPTS["ocr_pure_en"], max_tokens=2048)
    report["tests"]["1_ocr_pure"] = {
        "latency_s": r["latency_s"],
        "content_length": r["content_length"],
        "preview": r["content"][:500] if r["success"] else r.get("error"),
    }
    print(f"    Latency: {r['latency_s']}s, Output: {r['content_length']} chars")
    if r["success"]:
        print(f"    Preview: {r['content'][:200]}...")

    time.sleep(0.3)

    # ═══ Test 2: Structured JSON Extraction ═══
    print("\n── Test 2: Structured JSON Extraction ──")
    r = vlm_call(img_b64, PROMPTS["ocr_structured"], max_tokens=2048)
    report["tests"]["2_ocr_structured"] = {
        "latency_s": r["latency_s"],
        "content_length": r["content_length"],
        "preview": r["content"][:800] if r["success"] else r.get("error"),
    }
    # Validate JSON
    try:
        extracted = json.loads(r["content"]) if r["success"] else None
        report["tests"]["2_ocr_structured"]["json_valid"] = True
        report["tests"]["2_ocr_structured"]["question_count"] = len(extracted)
        print(f"    Latency: {r['latency_s']}s, Valid JSON: YES, Questions: {len(extracted)}")
    except (json.JSONDecodeError, TypeError):
        report["tests"]["2_ocr_structured"]["json_valid"] = False
        print(f"    Latency: {r['latency_s']}s, Valid JSON: NO")
        if r["success"]:
            print(f"    Raw: {r['content'][:300]}...")

    time.sleep(0.3)

    # ═══ Test 3: Layout Understanding ═══
    print("\n── Test 3: Layout Understanding ──")
    r = vlm_call(img_b64, PROMPTS["layout_check"], max_tokens=1024)
    report["tests"]["3_layout"] = {
        "latency_s": r["latency_s"],
        "preview": r["content"][:600] if r["success"] else r.get("error"),
    }
    print(f"    Latency: {r['latency_s']}s")
    if r["success"]:
        print(f"    {r['content'][:300]}...")

    time.sleep(0.3)

    # ═══ Test 4: Consistency (same prompt x3) ═══
    print("\n── Test 4: Output Consistency (3 runs) ──")
    short_prompt = "Transcribe the first 3 questions you see on this page, verbatim."
    cons_results = test_consistency(img_b64, "consistency", short_prompt, n=3)
    successes = [c for c in cons_results if c["success"]]
    if len(successes) >= 2:
        contents = [s["content"] for s in successes]
        from difflib import SequenceMatcher
        sim_01 = SequenceMatcher(None, contents[0], contents[1]).ratio() if len(successes) >= 2 else 0
        sim_12 = SequenceMatcher(None, contents[1], contents[2]).ratio() if len(successes) >= 3 else 0
        report["tests"]["4_consistency"] = {
            "runs": len(successes),
            "avg_latency_s": round(sum(s["latency_s"] for s in successes) / len(successes), 2),
            "similarity_run0_vs_run1": round(sim_01, 4),
            "similarity_run1_vs_run2": round(sim_12, 4),
            "contents": [c["content"][:200] for c in successes],
        }
        print(f"    Similarities: {sim_01:.3f}, {sim_12:.3f}")
    else:
        report["tests"]["4_consistency"] = {"error": "Not enough successful runs"}

    # ═══ Test 5: Token limit scaling ═══
    print("\n── Test 5: Token Limit Scaling ──")
    report["tests"]["5_token_limits"] = test_token_limits(img_b64)

    # ═══ Test 6: Multi-image support ═══
    print("\n── Test 6: Multi-Image Support ──")
    report["tests"]["6_multi_image"] = test_multi_image()

    # ═══ Test 7: Answer key detection (on answer PDF) ═══
    print("\n── Test 7: Answer Key Detection ──")
    answer_pdf = PDF_DIR / "cam15_answers.pdf"
    if answer_pdf.exists():
        doc = fitz.open(str(answer_pdf))
        found_answers = False
        for pg in range(doc.page_count - 1, max(0, doc.page_count - 30), -3):
            ans_img = render_page_jpeg(answer_pdf, pg, dpi=100)
            if not ans_img:
                continue
            r = vlm_call(ans_img, PROMPTS["answer_key"], max_tokens=64)
            if r["success"] and "YES" in r["content"].upper():
                # Found answer key page, extract full
                r2 = vlm_call(ans_img, PROMPTS["answer_key"], max_tokens=1024)
                report["tests"]["7_answer_key"] = {
                    "detected_page": pg + 1,
                    "detection_latency_s": r["latency_s"],
                    "extraction": r2["content"][:500] if r2["success"] else "N/A",
                }
                print(f"    Found answer keys on page {pg+1}!")
                found_answers = True
                break
            print(f"    p{pg+1}: {r['content'][:60] if r['success'] else 'FAIL'}")
            time.sleep(0.3)
        if not found_answers:
            report["tests"]["7_answer_key"] = {"detected": False, "reason": "No answer key pages found"}
            print("    No answer key pages detected")
        doc.close()
    else:
        report["tests"]["7_answer_key"] = {"error": "cam15_answers.pdf not found"}

    # ═══ Test 8: Different DPI sensitivity ═══
    print("\n── Test 8: DPI Sensitivity ──")
    dpi_results = {}
    for dpi in [60, 80, 100, 120, 150]:
        img = render_page_jpeg(test_pdf, 8, dpi=dpi)
        if not img:
            continue
        prompt = "Transcribe the first sentence of this page."
        print(f"    DPI {dpi} ({len(img)//1024}KB) ...", end=" ", flush=True)
        r = vlm_call(img, prompt, max_tokens=128)
        dpi_results[str(dpi)] = {
            "latency_s": r["latency_s"],
            "image_size_kb": len(img) // 1024,
            "output": r["content"][:200] if r["success"] else r.get("error"),
        }
        print(f"{r['latency_s']}s")
        time.sleep(0.2)
    report["tests"]["8_dpi_sensitivity"] = dpi_results

    # ═══ Test 9: Latency benchmark ═══
    print("\n── Test 9: Latency Benchmark (10 quick calls) ──")
    latencies = []
    short_prompt = "What number is at the top left of this page? Reply with just the number."
    for i in range(10):
        r = vlm_call(img_b64, short_prompt, max_tokens=16)
        latencies.append(r["latency_s"])
        print(f"    call {i+1}: {r['latency_s']}s" + (" FAIL" if not r["success"] else ""))
        if r["success"]:
            time.sleep(0.1)
    report["tests"]["9_latency_benchmark"] = {
        "calls": 10,
        "min_s": round(min(latencies), 2),
        "max_s": round(max(latencies), 2),
        "avg_s": round(sum(latencies) / len(latencies), 2),
        "p50_s": round(sorted(latencies)[len(latencies)//2], 2),
    }
    print(f"    Min: {min(latencies):.2f}s, Max: {max(latencies):.2f}s, Avg: {sum(latencies)/len(latencies):.2f}s")

    # ═══ Save report ═══
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n{'=' * 70}")
    print(f"  Report saved to: {OUTPUT}")
    print(f"{'=' * 70}")

    # Print summary
    print("\n── SUMMARY ──")
    print(f"  OCR accuracy: Test 1 output length = {report['tests']['1_ocr_pure']['content_length']} chars")
    print(f"  JSON extraction: {'PASS' if report['tests'].get('2_ocr_structured', {}).get('json_valid') else 'FAIL'}")
    print(f"  Consistency: {report['tests'].get('4_consistency', {}).get('similarity_run0_vs_run1', 'N/A')}")
    print(f"  Multi-image: {report['tests']['6_multi_image'].get('supported', 'N/A')}")
    print(f"  Avg latency (10 calls): {report['tests']['9_latency_benchmark']['avg_s']}s")
    print(f"  Min/Max latency: {report['tests']['9_latency_benchmark']['min_s']}s / {report['tests']['9_latency_benchmark']['max_s']}s")


if __name__ == "__main__":
    main()
