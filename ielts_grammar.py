"""
IELTS Listening question type grammar.

Defines the structural rules for every IELTS listening question type:
- How questions are numbered and segmented
- How multi-select questions work (one stem → two question numbers)
- How matching questions relate to their option boxes
- Part-wide question ranges and sub-sections

Each rule is a dataclass with validation logic — parsers use these to verify
that extracted questions match the expected structure for their type.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from enum import Enum


class QType(Enum):
    FORM_COMPLETION = "form_completion"
    TABLE_COMPLETION = "table_completion"
    FLOW_CHART = "flow_chart"
    SUMMARY_COMPLETION = "summary_completion"
    SENTENCE_COMPLETION = "sentence_completion"
    MULTIPLE_CHOICE = "multiple_choice"
    MULTIPLE_CHOICE_MULTI = "multiple_choice_multi"
    MATCHING = "matching"
    MAP_LABELLING = "map_labelling"
    SHORT_ANSWER = "short_answer"


# ── Instruction text patterns for each question type ──
INSTRUCTION_PATTERNS = {
    QType.FORM_COMPLETION: [
        r"Complete\s+the\s+(notes|form)\s+below",
        r"Write\s+(ONE\s+WORD\s+ONLY|ONE\s+WORD\s+AND/OR\s+A\s+NUMBER|NO\s+MORE\s+THAN\s+\w+\s+WORDS?)",
    ],
    QType.TABLE_COMPLETION: [
        r"Complete\s+the\s+table\s+below",
    ],
    QType.FLOW_CHART: [
        r"Complete\s+the\s+flow.chart\s+below",
    ],
    QType.SUMMARY_COMPLETION: [
        r"Complete\s+the\s+summary\s+below",
    ],
    QType.SENTENCE_COMPLETION: [
        r"Complete\s+the\s+sentences?\s+below",
    ],
    QType.MULTIPLE_CHOICE: [
        r"Choose\s+the\s+correct\s+letter,\s*[A-C](?:,\s*[A-C])*",
    ],
    QType.MULTIPLE_CHOICE_MULTI: [
        r"Choose\s+(TWO|THREE)\s+letters?,\s*[A-H](?:[–-][A-H])?",
    ],
    QType.MATCHING: [
        r"Choose\s+(?:[A-Z]+\s+)?(?:answers?|letters?)\s+from\s+the\s+box",
        r"write\s+the\s+correct\s+letter",
    ],
    QType.MAP_LABELLING: [
        r"Label\s+the\s+(map|plan)",
    ],
    QType.SHORT_ANSWER: [
        r"Answer\s+the\s+questions?\s+below",
        r"Write\s+NO\s+MORE\s+THAN",
    ],
}


@dataclass
class QuestionBlock:
    """A contiguous block of questions of the same type within a part.

    Examples:
      - "Questions 1–10" (form completion, whole part)
      - "Questions 11–14" (MC single, 4 questions)
      - "Questions 15 and 16" (MC multi TWO, 1 stem → 2 question numbers)
      - "Questions 15–20" (matching, 6 items)
    """

    qtype: QType
    start_num: int
    end_num: int
    num_questions: int
    is_multi_select: bool = False
    multi_count: int = 1  # 2 for "Choose TWO", 3 for "Choose THREE"
    option_letters: List[str] = field(default_factory=list)
    instruction_lines: List[str] = field(default_factory=list)
    title: str = ""
    items: List[dict] = field(default_factory=list)

    @property
    def question_numbers(self) -> List[int]:
        """All question numbers in this block."""
        if self.is_multi_select:
            return list(range(self.start_num, self.end_num + 1))
        return list(range(self.start_num, self.end_num + 1))

    @property
    def stem_count(self) -> int:
        """Number of question stems (not answer slots)."""
        if self.is_multi_select:
            return self.num_questions // self.multi_count
        return self.num_questions


@dataclass
class PartStructure:
    """The expected structure of one Listening part (10 questions total)."""

    part_number: int
    test_number: int
    question_range: Tuple[int, int]  # e.g. (1, 10), (11, 20)
    blocks: List[QuestionBlock] = field(default_factory=list)
    audio_script_ref: str = ""
    title: str = ""

    def validate(self) -> List[str]:
        """Check that blocks sum to exactly 10 questions."""
        errors = []
        total = sum(b.num_questions for b in self.blocks)
        if total != 10:
            errors.append(
                f"Part {self.part_number}: blocks sum to {total} questions, expected 10"
            )
        start, end = self.question_range
        expected = list(range(start, end + 1))
        actual = []
        for b in self.blocks:
            actual.extend(b.question_numbers)
        if sorted(actual) != expected:
            errors.append(
                f"Part {self.part_number}: question numbers {sorted(actual)} != expected {expected}"
            )
        return errors


# ── Part-level structure templates from the official Cambridge books ──
#
# Each template maps a part number to its typical block layout.
# Used both for parsing (knowing what to look for) and validation
# (checking that extracted data matches expectation).

# cam17 Test 1 structure (verified from official PDF pages 10-15)
CAM17_TEST1 = [
    PartStructure(
        part_number=1,
        test_number=1,
        question_range=(1, 10),
        blocks=[
            QuestionBlock(
                qtype=QType.FORM_COMPLETION,
                start_num=1,
                end_num=10,
                num_questions=10,
            ),
        ],
        title="Buckworth Conservation Group",
    ),
    PartStructure(
        part_number=2,
        test_number=1,
        question_range=(11, 20),
        blocks=[
            QuestionBlock(
                qtype=QType.MULTIPLE_CHOICE,
                start_num=11,
                end_num=14,
                num_questions=4,
                option_letters=["A", "B", "C"],
            ),
            QuestionBlock(
                qtype=QType.MULTIPLE_CHOICE_MULTI,
                start_num=15,
                end_num=16,
                num_questions=2,
                is_multi_select=True,
                multi_count=2,
                option_letters=["A", "B", "C", "D", "E"],
            ),
            QuestionBlock(
                qtype=QType.MULTIPLE_CHOICE_MULTI,
                start_num=17,
                end_num=18,
                num_questions=2,
                is_multi_select=True,
                multi_count=2,
                option_letters=["A", "B", "C", "D", "E"],
            ),
            QuestionBlock(
                qtype=QType.MULTIPLE_CHOICE_MULTI,
                start_num=19,
                end_num=20,
                num_questions=2,
                is_multi_select=True,
                multi_count=2,
                option_letters=["A", "B", "C", "D", "E"],
            ),
        ],
        title="Boat trip round Tasmania",
    ),
    PartStructure(
        part_number=3,
        test_number=1,
        question_range=(21, 30),
        blocks=[
            QuestionBlock(
                qtype=QType.MULTIPLE_CHOICE,
                start_num=21,
                end_num=26,
                num_questions=6,
                option_letters=["A", "B", "C"],
            ),
            QuestionBlock(
                qtype=QType.MATCHING,
                start_num=27,
                end_num=30,
                num_questions=4,
                option_letters=["A", "B", "C", "D", "E", "F"],
            ),
        ],
        title="Work experience for veterinary science students",
    ),
    PartStructure(
        part_number=4,
        test_number=1,
        question_range=(31, 40),
        blocks=[
            QuestionBlock(
                qtype=QType.FORM_COMPLETION,
                start_num=31,
                end_num=40,
                num_questions=10,
            ),
        ],
        title="Labyrinths",
    ),
]


def get_structure(cam_id: str, test_num: int) -> List[PartStructure]:
    """Return the part structures for a given Cambridge book and test."""
    if cam_id == "cam17":
        return CAM17_TEST1  # All tests share this structure in cam17
    # For other books, use heuristics to detect structure from parsed text
    return []


def detect_block_type(text: str) -> Optional[QType]:
    """Detect question type from instruction text."""
    text_lower = text.lower()
    for qtype, patterns in INSTRUCTION_PATTERNS.items():
        for pattern in patterns:
            import re

            if re.search(pattern, text, re.IGNORECASE):
                return qtype
    return None


def detect_multi_count(text: str) -> int:
    """Detect how many letters to choose from instruction text."""
    import re

    m = re.search(r"Choose\s+(TWO|THREE)\s+letters?", text, re.IGNORECASE)
    if m:
        word = m.group(1).upper()
        return {"TWO": 2, "THREE": 3}.get(word, 1)
    return 1
