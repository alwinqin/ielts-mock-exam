#!/usr/bin/env python3
"""Generalized fix for Cambridge reading.json and listening.json question counts.

Splits multiple_choice_multi ("Choose TWO") questions into individual
multiple_choice objects, then renumbers all questions sequentially.
Usage: python3 fix_counts.py [book_id]
  e.g. python3 fix_counts.py cam15
If no book_id given, processes all cam14-cam20.
"""

import json
import os
import sys

DATA_DIR = "data/cambridge"


def split_multi_to_individual(q):
    answers = [a.strip() for a in q["correctAnswer"].split(",")]
    results = []
    for ans in answers:
        nq = {
            "id": "",
            "type": "multiple_choice",
            "question": q["question"],
            "options": q["options"],
            "correctAnswer": ans,
        }
        results.append(nq)
    return results


def fix_reading(book_id):
    path = os.path.join(DATA_DIR, book_id, "reading.json")
    if not os.path.exists(path):
        print(f"  SKIP: {path} not found")
        return
    with open(path) as f:
        data = json.load(f)

    for test in data["tests"]:
        t_id = test["id"]
        t_num = t_id.split("_test")[1] if "_test" in t_id else t_id.split("test")[1]

        for passage in test["passages"]:
            p_id = passage["id"]
            # Determine passage number from ID like camXX_tY_pZ
            parts = p_id.split("_p")
            p_num = parts[-1]

            new_qs = []
            for q in passage["questions"]:
                if q["type"] == "multiple_choice_multi" and "," in q.get("correctAnswer", ""):
                    parts_split = split_multi_to_individual(q)
                    new_qs.extend(parts_split)
                else:
                    new_qs.append(q)

            # Renumber questions sequentially within passage
            q_start = {"1": 1, "2": 14, "3": 27}.get(p_num, 1)
            for i, q in enumerate(new_qs):
                q["id"] = f"{book_id}_t{t_num}_r_q{q_start + i}"

            passage["questions"] = new_qs

    with open(path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    for t in data["tests"]:
        tq = sum(len(p["questions"]) for p in t["passages"])
        print(f"  Reading Test {t['testNumber']}: {tq} questions")


def fix_listening(book_id):
    path = os.path.join(DATA_DIR, book_id, "listening.json")
    if not os.path.exists(path):
        print(f"  SKIP: {path} not found")
        return
    with open(path) as f:
        data = json.load(f)

    for test in data["tests"]:
        t_id = test["id"]
        t_num = t_id.split("_test")[1] if "_test" in t_id else t_id[-1]

        for part in test.get("parts", test.get("sections", [])):
            new_qs = []
            for q in part["questions"]:
                if q["type"] == "multiple_choice_multi" and "," in q.get("correctAnswer", ""):
                    split_qs = split_multi_to_individual(q)
                    new_qs.extend(split_qs)
                else:
                    new_qs.append(q)
            part["questions"] = new_qs

        # Renumber sequentially 1-40 across all parts
        q_counter = 1
        for part in test.get("parts", test.get("sections", [])):
            for q in part["questions"]:
                q["id"] = f"{book_id}_lt{t_num}_q{q_counter}"
                q_counter += 1

    with open(path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    for t in data["tests"]:
        tq = sum(len(p["questions"]) for p in t.get("parts", t.get("sections", [])))
        print(f"  Listening Test {t['testNumber']}: {tq} questions")


def process_book(book_id):
    print(f"\n{'='*60}")
    print(f"Processing {book_id}")
    print(f"{'='*60}")
    fix_reading(book_id)
    fix_listening(book_id)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        process_book(sys.argv[1])
    else:
        for bid in ["cam14", "cam15", "cam16", "cam17", "cam18", "cam19", "cam20"]:
            process_book(bid)
