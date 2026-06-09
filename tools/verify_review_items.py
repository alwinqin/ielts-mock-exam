#!/usr/bin/env python3
"""Targeted Qwen3.6-27B verification of review items."""
import json, os, re, sys, time
from pathlib import Path
import fitz
sys.path.insert(0, '.')
from vlm_client import PDF_DIR, render_jpeg

API = "http://100.114.112.77:8000/v1/chat/completions"
MODEL = "Qwen3.6-27B"

def vlm_call_simple(img_b64, prompt, max_tokens=512, timeout=120):
    import requests
    resp = requests.post(API,
        headers={"Content-Type": "application/json"},
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
            ]}],
            "max_tokens": max_tokens, "temperature": 0.0,
        }, timeout=timeout)
    if resp.status_code == 200:
        content = resp.json()["choices"][0]["message"]["content"]
        # Strip thinking
        if "<｜end▁of▁thinking｜>" in content:
            content = content.split(" response", 1)[-1]
        return content.strip()
    return None

# Known answer key pages (1-indexed)
# Maps book:test:section -> page number
PAGE_MAP = {
    "cam14": {
        (1, "listening"): 119, (1, "reading"): 120,
        (2, "listening"): 121, (2, "reading"): 122,
        (3, "listening"): 123, (3, "reading"): 124,
        (4, "listening"): 125, (4, "reading"): 126,
    },
    "cam15": {
        (1, "listening"): 120, (1, "reading"): 121,
        (2, "listening"): 122, (2, "reading"): 123,
        (3, "listening"): 124, (3, "reading"): 125,
        (4, "listening"): 126, (4, "reading"): 127,
    },
    "cam16": {
        (1, "listening"): 121, (1, "reading"): 122,
        (2, "listening"): 123, (2, "reading"): 124,
        (3, "listening"): 125, (3, "reading"): 126,
        (4, "listening"): 127, (4, "reading"): 128,
    },
    "cam17": {
        (1, "listening"): 119, (1, "reading"): 120,
        (2, "listening"): 121, (2, "reading"): 122,
        (3, "listening"): 123, (3, "reading"): 124,
        (4, "listening"): 125, (4, "reading"): 126,
    },
    "cam18": {
        (1, "listening"): 121, (1, "reading"): 122,
        (2, "listening"): 123, (2, "reading"): 124,
        (3, "listening"): 125, (3, "reading"): 126,
        (4, "listening"): 127, (4, "reading"): 128,
    },
    "cam19": {
        (3, "listening"): 124, (3, "reading"): 125,
        (4, "listening"): 126, (4, "reading"): 127,
        (1, "listening"): 120, (1, "reading"): 121,
        (2, "listening"): 122, (2, "reading"): 123,
    },
}

# Load review items
review = json.load(open('/tmp/review_items.json'))
need_vlm = review['need_vlm']

# Group by (book, test, section) -> page
from collections import defaultdict
page_groups = defaultdict(list)
for item in need_vlm:
    book = item['book']
    test = item['test']
    section = item['section']
    key = (book, test, section)
    page = PAGE_MAP.get(book, {}).get((test, section))
    if page:
        page_groups[(book, page)].append(item)
    else:
        print(f"WARNING: no page for {item['question']} ({book} t{test} {section})")

print(f"Pages to verify: {len(page_groups)}")
for (book, page), items in sorted(page_groups.items()):
    qs = sorted([i['q_num'] for i in items])
    print(f"  {book} p{page}: Q{qs}")

# Run verification
results = []
for (book, page), items in sorted(page_groups.items()):
    pdf_path = PDF_DIR / f"{book}_questions.pdf"
    if not pdf_path.exists():
        print(f"  {book}: PDF not found")
        continue

    doc = fitz.open(str(pdf_path))
    pg = page - 1
    if pg >= doc.page_count:
        doc.close()
        continue

    img = render_jpeg(doc, pg, dpi=200)
    doc.close()
    if not img:
        continue

    q_nums = sorted(set(i['q_num'] for i in items))
    q_list = ", ".join(str(q) for q in q_nums)

    # Build targeted prompt
    prompt = f"""Look at this IELTS answer key page. I need the EXACT answers for ONLY these question numbers: {q_list}

For each question, tell me the EXACT answer as printed in the answer key.
- If it's a letter (MC question), output just the letter
- If it's a word/phrase, output the full text
- For IN EITHER ORDER pairs, list all valid letters

Output format (one per line):
Q{{NUM}}: ANSWER

Example:
Q25: A
Q20: D
Q9: merchant

NO analysis. ONLY the Q:Answer lines."""

    print(f"  {book} p{page} Q{q_nums}: ", end="", flush=True)
    t0 = time.time()
    raw = vlm_call_simple(img, prompt, max_tokens=512)
    elapsed = time.time() - t0

    if not raw:
        print("FAILED")
        continue

    # Parse Qwen response
    qwen_answers = {}
    for line in raw.split("\n"):
        m = re.match(r"Q(\d{1,2})\s*[:.]\s*(.+)", line.strip(), re.I)
        if m:
            qn = int(m.group(1))
            ans = m.group(2).strip().rstrip(".,")
            qwen_answers[qn] = ans

    print(f"{len(qwen_answers)} answers, {elapsed:.1f}s")

    for item in items:
        qn = item['q_num']
        qwen_a = qwen_answers.get(qn, "NOT_FOUND")
        verdict = "?"

        # Compare Qwen vs JSON vs old key
        ka = item['extracted']
        ja = item['json']

        if qwen_a == "NOT_FOUND":
            verdict = "QWEN_NO_ANSWER"
        elif qwen_a.upper().replace(" ", "") == ja.upper().replace(" ", ""):
            verdict = "JSON_MATCHES_QWEN"
        elif qwen_a.upper().replace(" ", "") == ka.upper().replace(" ", ""):
            verdict = "KEY_MATCHES_QWEN"
        elif len(qwen_a) == 1 and ja and qwen_a.upper() == ja[0].upper():
            verdict = "JSON_MATCHES_QWEN"  # MC letter match
        elif len(qwen_a) == 1 and len(ka) == 1:
            verdict = "QWEN_DIFFERS_FROM_BOTH"
        else:
            verdict = "QWEN_DIFFERS_FROM_BOTH"

        results.append({
            **item,
            'qwen_answer': qwen_a,
            'verdict': verdict,
            'page': page,
        })
        print(f"    Q{qn}: Qwen='{qwen_a}' | old_key='{ka}' | JSON='{ja[:40]}' → {verdict}")

    time.sleep(0.3)

# Save results
with open('/tmp/vlm_verification.json', 'w') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

# Summary
matches_json = [r for r in results if r['verdict'] == 'JSON_MATCHES_QWEN']
matches_key = [r for r in results if r['verdict'] == 'KEY_MATCHES_QWEN']
differs = [r for r in results if r['verdict'] == 'QWEN_DIFFERS_FROM_BOTH']
no_answer = [r for r in results if r['verdict'] == 'QWEN_NO_ANSWER']

print(f"\n=== Verification Summary ===")
print(f"JSON matches Qwen: {len(matches_json)}")
print(f"Key matches Qwen (JSON wrong): {len(matches_key)}")
print(f"Qwen differs from both: {len(differs)}")
print(f"Qwen no answer: {len(no_answer)}")

if differs:
    print(f"\n── Qwen differs from both (needs human) ──")
    for r in differs:
        print(f"  {r['question']}: Qwen='{r['qwen_answer']}' old='{r['extracted']}' JSON='{r['json'][:40]}'")

if matches_key:
    print(f"\n── Key matches Qwen (JSON needs fixing) ──")
    for r in matches_key:
        print(f"  {r['question']}: Qwen='{r['qwen_answer']}' JSON='{r['json'][:40]}'")
