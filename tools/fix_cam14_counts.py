#!/usr/bin/env python3
"""Fix cam14 reading.json and listening.json to have exactly 40 questions per test.

For combined "Choose TWO" questions (e.g. Q19-20 with answer "B, D"),
split into separate question objects, each with a single-letter answer.
"""

import json
import copy
import os

DIR = "data/cambridge/cam14"


def split_multi_to_individual(q, id_prefix):
    """Split a multiple_choice_multi question into individual multiple_choice objects."""
    answers = [a.strip() for a in q["correctAnswer"].split(",")]
    results = []
    for ans in answers:
        nq = {
            "id": "",  # will be set by caller
            "type": "multiple_choice",
            "question": q["question"],
            "options": q["options"],
            "correctAnswer": ans,
        }
        results.append(nq)
    return results


def fix_reading():
    path = os.path.join(DIR, "reading.json")
    with open(path) as f:
        data = json.load(f)

    for test in data["tests"]:
        t_num = test["id"].split("_test")[1]
        for passage in test["passages"]:
            p_num = passage["id"].split("_p")[1]
            # Determine starting question number for this passage
            q_start = {"1": 1, "2": 14, "3": 27}[p_num]

            new_qs = []
            for q in passage["questions"]:
                if q["type"] == "multiple_choice_multi" and "," in q.get("correctAnswer", ""):
                    parts = split_multi_to_individual(q, q["id"])
                    new_qs.extend(parts)
                else:
                    new_qs.append(q)

            # Renumber questions sequentially
            for i, q in enumerate(new_qs):
                q["id"] = f"cam14_t{t_num}_r_q{q_start + i}"

            passage["questions"] = new_qs

    with open(path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    for t in data["tests"]:
        tq = sum(len(p["questions"]) for p in t["passages"])
        print(f"Reading Test {t['testNumber']}: {tq} questions")


def fix_listening():
    path = os.path.join(DIR, "listening.json")
    with open(path) as f:
        data = json.load(f)

    for test in data["tests"]:
        t_num = test["id"].split("_test")[1]

        for part in test["parts"]:
            new_qs = []
            for q in part["questions"]:
                if q["type"] == "multiple_choice_multi" and "," in q.get("correctAnswer", ""):
                    parts = split_multi_to_individual(q, q["id"])
                    new_qs.extend(parts)
                else:
                    new_qs.append(q)
            part["questions"] = new_qs

        # Renumber questions sequentially across all parts (1-40 per test)
        q_counter = 1
        for part in test["parts"]:
            for q in part["questions"]:
                q["id"] = f"cam14_lt{t_num}_q{q_counter}"
                q_counter += 1

    with open(path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    for t in data["tests"]:
        tq = sum(len(p["questions"]) for p in t["parts"])
        # Check question ordering/numbering
        qids = []
        for p in t["parts"]:
            for q in p["questions"]:
                qids.append(q["id"])
        print(f"Listening Test {t['testNumber']}: {tq} questions")


if __name__ == "__main__":
    fix_reading()
    print()
    fix_listening()
