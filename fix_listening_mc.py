#!/usr/bin/env python3
"""Fix listening MC question options and fill-blank questions.

Two issues:
1. MC options embedded in question text → parse them out into proper options array
2. MC and fill-blank questions with placeholder/missing text → need PDF extraction

This script handles issue 1. Issue 2 requires PDF extraction (separate script).
"""

import json
import os
import re

DATA_DIR = "data/cambridge"

total_embedded_fixed = 0
total_missing_mc = 0
total_placeholder_fill = 0

for book_id in sorted(os.listdir(DATA_DIR)):
    path = os.path.join(DATA_DIR, book_id, "listening.json")
    if not os.path.exists(path):
        continue

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    embedded_fixed = 0
    missing_mc = 0
    placeholder_fill = 0
    fix_log = []

    for test in data.get("tests", []):
        for part in test.get("parts", []):
            for q in part.get("questions", []):
                qtype = q.get("type", "")
                opts = q.get("options", [])
                qtext = q.get("question", "")

                # --- Fix 1: embedded MC options ---
                if qtype in ("multiple_choice", "multiple_choice_multi"):
                    if opts and all(len(str(o).strip()) <= 2 for o in opts):
                        lines = qtext.split("\n")
                        # Find option lines: start with a letter followed by . or space, and longer than 2 chars
                        option_lines = []
                        stem_lines = []
                        for line in lines:
                            stripped = line.strip()
                            if (
                                len(stripped) > 2
                                and stripped[0].isalpha()
                                and stripped[0].isupper()
                                and len(stripped) > 1
                                and stripped[1] in ". "
                            ):
                                option_lines.append(stripped)
                            else:
                                stem_lines.append(stripped)

                        # Need at least as many option lines as options
                        if len(option_lines) >= len(opts):
                            # Build new options array with full text
                            new_opts = option_lines[: len(opts)]
                            # Clean question text (stem only)
                            new_question = "\n".join(stem_lines).strip()

                            old_answer = q.get("correctAnswer", "").strip()
                            # Find the matching option for the answer letter
                            answer_letter = old_answer.upper()
                            new_answer = old_answer  # default
                            for opt in new_opts:
                                if opt[0].upper() == answer_letter:
                                    new_answer = opt
                                    break

                            q["options"] = new_opts
                            q["question"] = new_question
                            q["correctAnswer"] = new_answer
                            embedded_fixed += 1
                            fix_log.append(
                                f"  {q['id']}: embedded MC fixed, answer {old_answer} → {new_answer}"
                            )
                        else:
                            missing_mc += 1
                    else:
                        # Good options already (like cam17)
                        pass

                # --- Fix 2: placeholder fill-blank detection ---
                if qtype in (
                    "notes_completion",
                    "form_completion",
                    "summary_completion",
                    "sentence_completion",
                ):
                    if "Question" in qtext and "ONE WORD" in qtext:
                        placeholder_fill += 1

    if embedded_fixed > 0:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n{book_id}: fixed {embedded_fixed} embedded MC options")
        for log in fix_log:
            print(log)

    total_embedded_fixed += embedded_fixed
    total_missing_mc += missing_mc
    total_placeholder_fill += placeholder_fill

    if missing_mc or placeholder_fill:
        print(
            f"{book_id}: {missing_mc} MC still missing options (need PDF), "
            f"{placeholder_fill} fill-blanks need context (need PDF)"
        )

print(f"\n=== Summary ===")
print(f"Embedded MC fixed: {total_embedded_fixed}")
print(f"MC still missing (need PDF): {total_missing_mc}")
print(f"Fill-blanks needing context (need PDF): {total_placeholder_fill}")
print(f"\nDone!")
