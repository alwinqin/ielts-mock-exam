#!/usr/bin/env python3
"""Final cleanup: replace corrupted Cambridge speaking tests with standalone fallback data."""
import json, re
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "data" / "cambridge"
SPEAKING_DIR = Path(__file__).parent / "data" / "speaking"


def is_corrupt(stored):
    """Check if a stored test has listening content instead of speaking."""
    p2 = stored.get("part2", {})
    p2_title = p2.get("title") or ""
    p2_prompts = p2.get("prompts", [])

    # Check Part 2 title for listening markers
    if re.search(r'Questions?\s+\d+.*\d+', p2_title):
        return True

    # Check prompts for listening markers
    if p2_prompts:
        first = p2_prompts[0]
        if re.search(r'Choose.*letters?', first, re.IGNORECASE):
            return True
        if re.search(r'Questions?\s+\d+.*\d+', first):
            return True

    # Check Part 1 for listening transcripts
    p1 = stored.get("part1", {})
    p1_qs = p1.get("questions", [])
    if p1_qs:
        first = p1_qs[0]
        # Listening transcripts often start with interviewer introductions
        if re.search(r'good morning|hello.*name.*is|ranger|teaching assistant', first, re.IGNORECASE):
            return True
        if re.search(r'\d+\s+\.{3,}', first):  # Gap-fill format
            return True

    return False


def is_missing(stored):
    """Check if test is missing critical data."""
    p2 = stored.get("part2", {})
    return not p2.get("title") or not p2.get("prompts")


def load_standalone(test_id):
    """Load standalone speaking file and convert to Cambridge format."""
    path = SPEAKING_DIR / f"{test_id}.json"
    if not path.exists():
        return None

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    # Convert standalone format to Cambridge format
    p1_qs = []
    if isinstance(data.get("part1"), list):
        for item in data["part1"]:
            if isinstance(item, dict):
                p1_qs.append(item.get("question", ""))
            else:
                p1_qs.append(str(item))

    p2 = data.get("part2", {})
    if isinstance(p2, dict):
        p2_title = p2.get("cueCard", "")
        p2_prompts = p2.get("bulletPoints", [])
    else:
        p2_title = ""
        p2_prompts = []

    p3 = data.get("part3", [])
    if isinstance(p3, list):
        p3_topics = []
        for item in p3:
            if isinstance(item, dict):
                p3_topics.append({
                    "topic": item.get("topic", "Discussion"),
                    "questions": item.get("questions", [])
                })
    else:
        p3_topics = []

    return {
        "part1": {"topic": "", "questions": p1_qs[:4]},
        "part2": {"title": p2_title, "prompts": p2_prompts[:4]},
        "part3": {"topics": p3_topics[:2]},
    }


def main():
    books = ["cam18", "cam19", "cam20"]
    total_fixed = 0

    for book_id in books:
        json_path = OUTPUT_DIR / book_id / "speaking.json"
        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)

        fixed = 0
        for i, test in enumerate(data["tests"]):
            test_id = test["id"]
            test_num = test["testNumber"]

            if is_corrupt(test) or is_missing(test):
                reason = "CORRUPT" if is_corrupt(test) else "MISSING"
                print(f"  {test_id}: {reason} - loading fallback...")

                fallback = load_standalone(test_id)
                if fallback:
                    # Keep the test ID and number, replace the data
                    data["tests"][i] = {
                        "id": test_id,
                        "testNumber": test_num,
                        "part1": fallback["part1"],
                        "part2": fallback["part2"],
                        "part3": fallback["part3"],
                    }
                    # Try to preserve Part 1 topic if it looked valid
                    old_topic = test.get("part1", {}).get("topic", "")
                    if old_topic and old_topic not in ("Not specified", "Guitar Group", "Local food shops", "Working at Milo's Restaurants"):
                        data["tests"][i]["part1"]["topic"] = old_topic

                    fixed += 1
                    print(f"    → Replaced with standalone data")
                else:
                    print(f"    → No fallback available!")
            else:
                # Minor fixes: clean up "Not specified" topics
                p1_topic = test.get("part1", {}).get("topic", "")
                if p1_topic in ("Not specified", None, ""):
                    # Try to infer topic from questions
                    pass  # Leave as is for now

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        total_fixed += fixed
        print(f"  {book_id}: Fixed {fixed} tests")

    print(f"\nTotal tests fixed: {total_fixed}")


if __name__ == "__main__":
    main()
