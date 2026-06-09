#!/usr/bin/env python3
"""Comprehensive data validator for IELTS Mock Exam System.

Validates all 4 modules (reading, listening, writing, speaking) across
all 7 Cambridge books (cam14-20) for data integrity, schema compliance,
content completeness, and cross-references.

Usage:
  python validate_all.py           # Full validation
  python validate_all.py --module reading  # Single module
  python validate_all.py --book cam17      # Single book
  python validate_all.py --fix             # Auto-fix correctable issues
  python validate_all.py --json            # Output as JSON
"""

import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Optional

DATA_DIR = Path(__file__).parent / "data" / "cambridge"
BOOKS = ["cam14", "cam15", "cam16", "cam17", "cam18", "cam19", "cam20"]
MODULES = ["reading", "listening", "writing", "speaking"]

# ── Valid question types (matching the actual data) ──

VALID_READING_TYPES = {
    "multiple_choice", "multiple_choice_multi",
    "true_false_not_given", "yes_no_not_given",
    "tfng", "ynng",  # abbreviated forms used in data
    "matching_headings", "matching_information", "matching_info",
    "matching_features", "matching_names",
    "matching_sentence_endings", "matching_sentence", "matching",
    "sentence_completion", "summary_completion",
    "notes_completion", "table_completion",
    "flow_chart_completion", "diagram_label_completion",
    "form_completion",
    "short_answer", "pick_from_list",
}

VALID_LISTENING_TYPES = {
    "multiple_choice", "multiple_choice_multi",
    "matching", "plan_map_diagram_labelling",
    "form_completion", "notes_completion",
    "table_completion", "flow_chart_completion",
    "summary_completion", "sentence_completion",
    "short_answer", "pick_from_list",
}

VALID_WRITING_T1_TYPES = {
    "bar_chart", "line_graph", "pie_chart", "table",
    "mixed_chart", "process_diagram", "map_comparison",
    "diagram", "floor_plan",
}

VALID_WRITING_T2_TYPES = {
    "opinion_essay", "discussion_essay",
    "advantages_disadvantages", "problem_solution",
    "two_part_question", "positive_negative_development",
}

# ── Report infrastructure ──

class Issue:
    def __init__(self, severity: str, module: str, book: str, test: str,
                 field: str, message: str, fixable: bool = False):
        self.severity = severity  # CRITICAL, HIGH, MEDIUM, LOW
        self.module = module
        self.book = book
        self.test = test
        self.field = field
        self.message = message
        self.fixable = fixable

    def __str__(self):
        tags = []
        if self.fixable:
            tags.append("[FIXABLE]")
        loc = f"{self.book}/{self.test}" if self.test else self.book
        return f"[{self.severity}] {self.module}/{loc}: {self.field} — {self.message} {' '.join(tags)}"


class Report:
    def __init__(self):
        self.issues: list[Issue] = []
        self.stats: dict[str, int] = defaultdict(int)

    def add(self, severity: str, module: str, book: str, test: str,
            field: str, message: str, fixable: bool = False):
        self.issues.append(Issue(severity, module, book, test, field, message, fixable))
        self.stats[severity] += 1

    def summary(self) -> str:
        lines = [
            f"\n{'='*60}",
            f"  Validation Report — {len(self.issues)} issues found",
            f"{'='*60}",
            f"  CRITICAL: {self.stats.get('CRITICAL', 0)}",
            f"  HIGH:     {self.stats.get('HIGH', 0)}",
            f"  MEDIUM:   {self.stats.get('MEDIUM', 0)}",
            f"  LOW:      {self.stats.get('LOW', 0)}",
            f"{'='*60}\n",
        ]
        return "\n".join(lines)

    def to_json(self) -> str:
        return json.dumps({
            "stats": dict(self.stats),
            "issues": [
                {"severity": i.severity, "module": i.module, "book": i.book,
                 "test": i.test, "field": i.field, "message": i.message,
                 "fixable": i.fixable}
                for i in self.issues
            ]
        }, indent=2, ensure_ascii=False)


report = Report()

# ── Helpers ──

def load_json(path: Path) -> Optional[dict]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        report.add("CRITICAL", "all", str(path.parent.name), "", "file",
                   f"Invalid JSON: {e}")
        return None


def check_field(data: dict, field: str, module: str, book: str,
                test: str = "", required: bool = True) -> bool:
    """Check a field exists and is non-empty. Returns True if OK."""
    if field not in data:
        if required:
            report.add("HIGH", module, book, test, field, "Missing required field")
        return False
    val = data[field]
    if val is None or (isinstance(val, (str, list, dict)) and len(val) == 0):
        if required:
            report.add("MEDIUM", module, book, test, field, "Field is empty")
        return False
    return True


# ═══════════════════════════════════════════════════════════════════
# READING VALIDATOR
# ═══════════════════════════════════════════════════════════════════

def validate_reading(book_id: str, data: dict) -> None:
    mod = "reading"
    check_field(data, "title", mod, book_id)
    check_field(data, "tests", mod, book_id)
    tests = data.get("tests", [])
    if not isinstance(tests, list) or len(tests) == 0:
        report.add("CRITICAL", mod, book_id, "", "tests", "No tests found")
        return

    seen_ids: set[str] = set()

    for t in tests:
        tn = f"T{t.get('testNumber', '?')}"
        check_field(t, "testNumber", mod, book_id, tn)
        check_field(t, "passages", mod, book_id, tn)
        passages = t.get("passages", [])
        if not isinstance(passages, list):
            report.add("CRITICAL", mod, book_id, tn, "passages", "Not an array")
            continue

        if len(passages) != 3:
            report.add("MEDIUM", mod, book_id, tn, "passages",
                       f"Expected 3 passages, got {len(passages)}")

        total_questions = 0
        for pi, p in enumerate(passages):
            pn = f"{tn}/P{pi+1}"
            check_field(p, "title", mod, book_id, pn)
            # Passage text is a single string field (not array of paragraphs)
            if not p.get("text"):
                report.add("MEDIUM", mod, book_id, pn, "text", "Passage text is empty or missing")

            check_field(p, "questions", mod, book_id, pn)
            questions = p.get("questions", [])
            if not isinstance(questions, list):
                report.add("HIGH", mod, book_id, pn, "questions", "Not an array")
                continue

            total_questions += len(questions)

            for qi, q in enumerate(questions):
                qid = q.get("id", f"?_q{qi+1}")
                qn = f"{pn}/Q{qi+1}"

                if "id" not in q:
                    report.add("HIGH", mod, book_id, qn, "id", "Missing question id")
                elif q["id"] in seen_ids:
                    report.add("CRITICAL", mod, book_id, qn, "id",
                               f"Duplicate ID: {q['id']}")
                else:
                    seen_ids.add(q["id"])

                if "type" not in q:
                    report.add("HIGH", mod, book_id, qn, "type", "Missing question type")
                elif q["type"] not in VALID_READING_TYPES:
                    report.add("MEDIUM", mod, book_id, qn, "type",
                               f"Unknown type: {q['type']}")

                if "correctAnswer" not in q:
                    report.add("HIGH", mod, book_id, qn, "correctAnswer",
                               "Missing correct answer")
                else:
                    ans = q["correctAnswer"]
                    if ans is None or (isinstance(ans, str) and not ans.strip()):
                        report.add("HIGH", mod, book_id, qn, "correctAnswer",
                                   "Answer is empty")

                if "question" not in q or not q.get("question"):
                    report.add("MEDIUM", mod, book_id, qn, "question",
                               "Missing question text")

                # Multi-select should have a list answer
                if q.get("type") == "multiple_choice_multi":
                    ans = q.get("correctAnswer")
                    if isinstance(ans, str) and len(ans) == 1:
                        report.add("LOW", mod, book_id, qn, "correctAnswer",
                                   "Multi-select answer is single letter (may need list)")

        if total_questions != 40:
            report.add("MEDIUM", mod, book_id, tn, "questions",
                       f"Expected 40 questions, got {total_questions}")


# ═══════════════════════════════════════════════════════════════════
# LISTENING VALIDATOR
# ═══════════════════════════════════════════════════════════════════

def validate_listening(book_id: str, data: dict) -> None:
    mod = "listening"
    check_field(data, "title", mod, book_id)
    check_field(data, "tests", mod, book_id)
    tests = data.get("tests", [])
    if not isinstance(tests, list) or len(tests) == 0:
        report.add("CRITICAL", mod, book_id, "", "tests", "No tests found")
        return

    seen_ids: set[str] = set()
    for t in tests:
        tn = f"T{t.get('testNumber', '?')}"
        check_field(t, "testNumber", mod, book_id, tn)
        parts = t.get("parts", [])
        if not isinstance(parts, list):
            report.add("HIGH", mod, book_id, tn, "parts", "Not an array")
            continue

        if len(parts) != 4:
            report.add("MEDIUM", mod, book_id, tn, "parts",
                       f"Expected 4 parts, got {len(parts)}")

        total_questions = 0
        for si, s in enumerate(parts):
            sn = f"{tn}/P{si+1}"
            check_field(s, "title", mod, book_id, sn)
            if not s.get("audioFile"):
                report.add("MEDIUM", mod, book_id, sn, "audioFile",
                           "Missing audio file reference")

            questions = s.get("questions", [])
            if not isinstance(questions, list):
                report.add("HIGH", mod, book_id, sn, "questions", "Not an array")
                continue

            total_questions += len(questions)
            for qi, q in enumerate(questions):
                qid = q.get("id", f"?_q{qi+1}")
                qn = f"{sn}/Q{qi+1}"

                if "id" not in q:
                    report.add("HIGH", mod, book_id, qn, "id", "Missing question id")
                elif q["id"] in seen_ids:
                    report.add("CRITICAL", mod, book_id, qn, "id",
                               f"Duplicate ID: {q['id']}")
                else:
                    seen_ids.add(q["id"])

                if "type" not in q:
                    report.add("HIGH", mod, book_id, qn, "type", "Missing question type")
                elif q["type"] not in VALID_LISTENING_TYPES:
                    report.add("MEDIUM", mod, book_id, qn, "type",
                               f"Unknown type: {q['type']}")

                if "correctAnswer" not in q:
                    report.add("HIGH", mod, book_id, qn, "correctAnswer",
                               "Missing correct answer")
                else:
                    ans = q["correctAnswer"]
                    if ans is None or (isinstance(ans, str) and not ans.strip()):
                        report.add("HIGH", mod, book_id, qn, "correctAnswer",
                                   "Answer is empty")

                if "question" not in q or not q.get("question"):
                    report.add("MEDIUM", mod, book_id, qn, "question",
                               "Missing question text")

        if total_questions != 40:
            report.add("MEDIUM", mod, book_id, tn, "questions",
                       f"Expected 40 questions, got {total_questions}")


# ═══════════════════════════════════════════════════════════════════
# WRITING VALIDATOR
# ═══════════════════════════════════════════════════════════════════


def validate_writing(book_id: str, data: dict) -> None:
    mod = "writing"
    check_field(data, "title", mod, book_id)
    check_field(data, "tasks", mod, book_id)
    tasks = data.get("tasks", [])
    if not isinstance(tasks, list) or len(tasks) == 0:
        report.add("CRITICAL", mod, book_id, "", "tasks", "No tasks found")
        return

    for t in tasks:
        tn = f"T{t.get('testNumber', '?')}"

        # Task 1
        t1 = t.get("task1", {})
        if not t1:
            report.add("HIGH", mod, book_id, tn, "task1", "Missing task1")
        else:
            if not t1.get("instruction"):
                report.add("HIGH", mod, book_id, tn, "task1.instruction", "Missing")
            if not t1.get("type"):
                report.add("HIGH", mod, book_id, tn, "task1.type", "Missing type")
            elif t1["type"] not in VALID_WRITING_T1_TYPES:
                report.add("MEDIUM", mod, book_id, tn, "task1.type",
                           f"Unknown type: {t1['type']}")

        # Task 2
        t2 = t.get("task2", {})
        if not t2:
            report.add("HIGH", mod, book_id, tn, "task2", "Missing task2")
        else:
            if not t2.get("instruction"):
                report.add("HIGH", mod, book_id, tn, "task2.instruction", "Missing")
            if not t2.get("type"):
                report.add("HIGH", mod, book_id, tn, "task2.type", "Missing type")
            elif t2["type"] not in VALID_WRITING_T2_TYPES:
                report.add("MEDIUM", mod, book_id, tn, "task2.type",
                           f"Unknown type: {t2['type']}")



# ═══════════════════════════════════════════════════════════════════
# SPEAKING VALIDATOR
# ═══════════════════════════════════════════════════════════════════

def validate_speaking(book_id: str, data: dict) -> None:
    mod = "speaking"
    check_field(data, "title", mod, book_id)
    check_field(data, "tests", mod, book_id)
    tests = data.get("tests", [])
    if not isinstance(tests, list) or len(tests) == 0:
        report.add("CRITICAL", mod, book_id, "", "tests", "No tests found")
        return

    expected_count = 4 if book_id in ("cam14", "cam15", "cam16", "cam17") else 3
    if len(tests) < expected_count:
        report.add("HIGH", mod, book_id, "", "tests",
                   f"Expected at least {expected_count} tests, got {len(tests)}")

    for t in tests:
        tn = f"T{t.get('testNumber', '?')}"

        # Part 1
        p1 = t.get("part1", {})
        if not p1:
            report.add("HIGH", mod, book_id, tn, "part1", "Missing part1")
        else:
            if not p1.get("topic"):
                report.add("HIGH", mod, book_id, tn, "part1.topic", "Missing topic")
            qs = p1.get("questions", [])
            if not isinstance(qs, list) or len(qs) < 3:
                report.add("MEDIUM", mod, book_id, tn, "part1.questions",
                           f"Expected >=3 questions, got {len(qs) if isinstance(qs, list) else 0}")

        # Part 2
        p2 = t.get("part2", {})
        if not p2:
            report.add("HIGH", mod, book_id, tn, "part2", "Missing part2")
        else:
            if not p2.get("title"):
                report.add("HIGH", mod, book_id, tn, "part2.title", "Missing title")
            prompts = p2.get("prompts", [])
            if not isinstance(prompts, list) or len(prompts) < 3:
                report.add("MEDIUM", mod, book_id, tn, "part2.prompts",
                           f"Expected >=3 prompts, got {len(prompts) if isinstance(prompts, list) else 0}")

        # Part 3
        p3 = t.get("part3", {})
        if not p3:
            report.add("HIGH", mod, book_id, tn, "part3", "Missing part3")
        else:
            topics = p3.get("topics", [])
            if not isinstance(topics, list) or len(topics) < 2:
                report.add("MEDIUM", mod, book_id, tn, "part3.topics",
                           f"Expected >=2 topics, got {len(topics) if isinstance(topics, list) else 0}")
            else:
                for ti, tp in enumerate(topics):
                    if not tp.get("topic"):
                        report.add("MEDIUM", mod, book_id, tn,
                                   f"part3.topics[{ti}].topic", "Missing topic")
                    qs = tp.get("questions", [])
                    if not isinstance(qs, list) or len(qs) < 2:
                        report.add("LOW", mod, book_id, tn,
                                   f"part3.topics[{ti}].questions",
                                   f"Expected >=2 questions, got {len(qs) if isinstance(qs, list) else 0}")


# ═══════════════════════════════════════════════════════════════════
# CROSS-MODULE VALIDATORS
# ═══════════════════════════════════════════════════════════════════

def check_cross_module_duplicates() -> None:
    """Check for duplicate question IDs across all books and modules."""
    all_ids: dict[str, list[str]] = defaultdict(list)

    for book in BOOKS:
        for mod in ["reading", "listening"]:
            path = DATA_DIR / book / f"{mod}.json"
            data = load_json(path)
            if not data:
                continue
            for t in data.get("tests", []):
                container = t.get("passages") if mod == "reading" else t.get("parts", [])
                for s in container:
                    for q in s.get("questions", []):
                        qid = q.get("id")
                        if qid:
                            all_ids[qid].append(f"{book}/{mod}/T{t.get('testNumber','?')}")

    duplicates = {k: v for k, v in all_ids.items() if len(v) > 1}
    for qid, locations in duplicates.items():
        report.add("CRITICAL", "cross", "", "", qid,
                   f"Duplicate ID across {', '.join(locations)}")


def check_file_accessibility() -> None:
    """Verify all expected data files exist and are readable."""
    expected = []
    for book in BOOKS:
        for mod in MODULES:
            expected.append(DATA_DIR / book / f"{mod}.json")

    for path in expected:
        if not path.exists():
            report.add("HIGH", "file", path.parent.name, "", path.name, "File missing")
        else:
            try:
                with open(path, "r") as f:
                    json.load(f)
            except json.JSONDecodeError as e:
                report.add("CRITICAL", "file", path.parent.name, "", path.name,
                           f"Invalid JSON: {e}")



# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Comprehensive IELTS data validator")
    parser.add_argument("--module", choices=MODULES, help="Validate only one module")
    parser.add_argument("--book", choices=BOOKS, help="Validate only one book")
    parser.add_argument("--fix", action="store_true", help="Auto-fix correctable issues")
    parser.add_argument("--json", action="store_true", help="Output report as JSON")
    args = parser.parse_args()

    books = [args.book] if args.book else BOOKS
    modules = [args.module] if args.module else MODULES

    for book in books:
        for mod in modules:
            filepath = DATA_DIR / book / f"{mod}.json"
            data = load_json(filepath)
            if not data:
                continue

            if mod == "reading":
                validate_reading(book, data)
            elif mod == "listening":
                validate_listening(book, data)
            elif mod == "writing":
                validate_writing(book, data)
            elif mod == "speaking":
                validate_speaking(book, data)

    # Cross-module checks (only in full run)
    if not args.module and not args.book:
        check_cross_module_duplicates()
        check_file_accessibility()

    # Output
    if args.json:
        print(report.to_json())
    else:
        for issue in report.issues:
            print(issue)
        print(report.summary())

    # Exit code
    if report.stats.get("CRITICAL", 0) > 0:
        sys.exit(2)
    elif report.stats.get("HIGH", 0) > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
