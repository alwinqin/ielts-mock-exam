#!/usr/bin/env python3
"""Rule-based classification of IELTS writing task types.
Adds 'type' field to all task1/task2 entries across cam14-20.
"""
import json, re
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data" / "cambridge"

# Priority-ordered rules for Task 1
TASK1_RULES = [
    # Combined/mixed charts
    (r"table.{0,100}(?:chart|graph|pie)", "mixed_chart"),
    (r"(?:chart|graph).{0,100}table", "mixed_chart"),
    (r"charts?.{0,100}table", "mixed_chart"),
    (r"pie.{0,100}(?:bar|column)", "mixed_chart"),
    # Map/plan
    (r"\b(?:maps?|plans?)\b.{0,80}(?:below|show|today)", "map_comparison"),
    (r"floor\s*plan", "floor_plan"),
    # Process diagram
    (r"(?:diagram|process).{0,60}(?:how|process|generated|produced|manufactur|makes?|made|making|recycl)", "process_diagram"),
    (r"manufacturing\s*process", "process_diagram"),
    # Line graph
    (r"line\s*graph", "line_graph"),
    (r"\bgraph\b.{0,30}(?:line|trend|change|increase|decrease|rise|fall)", "line_graph"),
    # Bar chart
    (r"\bbar\s*chart", "bar_chart"),
    # Pie chart
    (r"\bpie\s*chart", "pie_chart"),
    (r"percentages?.{0,40}(?:pie|chart)", "pie_chart"),
    # Table
    (r"\btables?\b.{0,40}(?:below|show|give)", "table"),
    # Generic chart
    (r"\bcharts?\b.{0,40}(?:below|show|give)", "bar_chart"),
    (r"\bchart\b", "bar_chart"),
    # Process/diagram (catch-all)
    (r"\bdiagram\b.{0,40}(?:below|show)", "diagram"),
    (r"\bdiagram\b", "process_diagram"),
    # Graph (generic, likely line)
    (r"\bgraph\b.{0,40}(?:below|show)", "line_graph"),
    # Map/plan (catch-all)
    (r"\bmaps?\b.{0,40}(?:show|illustrat)", "map_comparison"),
    (r"\bplans?\b.{0,40}(?:show|illustrat|compare)", "map_comparison"),
]

TASK2_RULES = [
    # Discussion essay (discuss both views)
    (r"discuss\s+both\s+(?:these\s+)?views", "discussion_essay"),
    # Two-part question (why + what/how question)
    (r"why.{10,60}\?(?:.{0,60}(?:what|how|do you think|positive|negative)\b)", "two_part_question"),
    (r"what\s+are\s+the\s+(?:reasons|arguments|causes).{10,60}\?", "two_part_question"),
    (r"how\s+(?:has|do|can|might).{10,60}\?(?:.{0,60}(?:what|why|do you|positive|negative)\b)", "two_part_question"),
    # Positive or negative development
    (r"positive\s+or\s+(?:a\s+)?negative\s+development", "positive_negative_development"),
    (r"positive\s+or\s+(?:a\s+)?negative.{0,20}(?:trend|change|thing)", "positive_negative_development"),
    # Advantages/disadvantages (without outweigh)
    (r"what\s+are\s+the\s+advantages.{0,80}disadvantages", "advantages_disadvantages"),
    # Opinion essay (agree/disagree)
    (r"(?:do\s+you\s+)?agree\s+or\s+disagree", "opinion_essay"),
    (r"to\s+what\s+extent\s+do\s+you\s+agree", "opinion_essay"),
    # Outweigh (opinion type)
    (r"outweigh", "opinion_essay"),
    # Problem/solution
    (r"what\s+(?:are|can|should).{0,60}(?:problem|issue|challenge|cause)", "problem_solution"),
    (r"(?:problem|issue|challenge).{0,40}solutions?", "problem_solution"),
    # Opinion statements
    (r"(?:do\s+you\s+think|do\s+you\s+believe|in\s+your\s+opinion|what\s+is\s+your\s+opinion)", "opinion_essay"),
    # Should/ought to (opinion)
    (r"\bshould\b.{0,120}(?:do\s+you\s+agree|your\s+opinion|what\s+do\s+you\s+think)", "opinion_essay"),
    # Two-part: question + "do you think"
    (r"\?\s*.{0,30}(?:do\s+you\s+think|do\s+you\s+believe)", "two_part_question"),
    (r"\?\s*.{0,30}(?:what|how|why)\b", "two_part_question"),
    # Generic - if text contains "do you think" it's likely opinion
    (r"do\s+you\s+think", "opinion_essay"),
    # Fallback for very clear patterns
    (r"(?:some\s+people|many\s+people|nowadays|in\s+many\s+countries).{0,100}(?:believe|think|argue|say)", "opinion_essay"),
]


def classify(instruction: str, task_num: int) -> str:
    """Classify a writing task based on instruction text."""
    text = (instruction or "").lower()
    rules = TASK1_RULES if task_num == 1 else TASK2_RULES
    for pattern, task_type in rules:
        if re.search(pattern, text, re.IGNORECASE | re.DOTALL):
            return task_type

    # Fallback
    return "other" if task_num == 1 else "opinion_essay"


def add_types_to_book(book_id: str):
    """Load writing.json, classify tasks, add type fields, save."""
    path = DATA_DIR / book_id / "writing.json"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    tasks = data.get("tasks", [])
    modified = False
    for t in tasks:
        tn = t["testNumber"]

        # Classify task1
        t1_type = classify(t["task1"].get("instruction", ""), 1)
        if t["task1"].get("type") != t1_type:
            t["task1"]["type"] = t1_type
            modified = True

        # Classify task2
        t2_type = classify(t["task2"].get("instruction", ""), 2)
        if t["task2"].get("type") != t2_type:
            t["task2"]["type"] = t2_type
            modified = True

        print(f"  T{tn}: T1={t1_type}, T2={t2_type}")

    if modified:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"  -> Updated {path}")
    else:
        print(f"  -> No changes needed")


def main():
    for book_id in ["cam14", "cam15", "cam16", "cam17", "cam18", "cam19", "cam20"]:
        print(f"\n{'='*50}")
        print(f"{book_id}")
        print("=" * 50)
        add_types_to_book(book_id)

    # Verify cam17 matches existing per-test types
    print(f"\n{'='*50}")
    print("Verification: cam17 types vs per-test files")
    print("=" * 50)
    with open(DATA_DIR / "cam17" / "writing.json") as f:
        main_data = json.load(f)

    for t in main_data["tasks"]:
        tn = t["testNumber"]
        test_path = DATA_DIR / "cam17" / f"writing_test{tn}.json"
        if test_path.exists():
            with open(test_path) as f:
                test_data = json.load(f)
            t1_expected = test_data.get("task1", {}).get("type", "")
            t2_expected = test_data.get("task2", {}).get("type", "")
            t1_actual = t["task1"].get("type", "")
            t2_actual = t["task2"].get("type", "")
            t1_match = "✓" if t1_actual == t1_expected else f"✗ ({t1_expected})"
            t2_match = "✓" if t2_actual == t2_expected else f"✗ ({t2_expected})"
            print(f"  T{tn}: T1={t1_actual} {t1_match}, T2={t2_actual} {t2_match}")

    print("\nDone!")


if __name__ == "__main__":
    main()
