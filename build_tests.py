#!/usr/bin/env python3
"""Build IELTS test JSON files."""
import json

def save_test(test_id, title, passages):
    test = {
        "id": test_id,
        "title": title,
        "totalQuestions": sum(len(p["questions"]) for p in passages),
        "passages": [{"id": p["id"], "title": p["title"], "text": p["text"], "questions": p["questions"]} for p in passages]
    }
    path = f"data/{test_id}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(test, f, ensure_ascii=False, indent=2)
    total = test["totalQuestions"]
    print(f"Saved {path}: {total} questions")
    for p in passages:
        print(f"  {p['id']}: {p['title'][:50]}... ({len(p['questions'])} Qs)")
    return total

# ===== TEST 13: Cambridge 17 =====
# Passage texts imported from separate file to keep this script manageable
print("Loading test 13 data...")
from test13_data import passages as t13_passages
save_test("test13", "Test 13 (Cambridge 17)", t13_passages)
