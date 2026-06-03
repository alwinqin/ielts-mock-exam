#!/usr/bin/env python3
"""Batch runner: process all IELTS PDFs sequentially, book by book.

Usage:
  python3 run_extraction.py                  # questions PDFs only (fast, high value)
  python3 run_extraction.py --with-answers   # include answers PDFs (Chinese study guides, slow)
  python3 run_extraction.py --only cam15     # single book
  python3 run_extraction.py --start cam16    # resume from a book

Resumes from cache automatically — interrupted runs pick up where they left off.
"""

import sys
import time
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from extract_all_pdfs import (
    PDF_INVENTORY, OUTPUT_DIR, CACHE_DIR, stats,
    process_questions_pdf, process_answers_pdf,
)

BOOK_ORDER = ["cam14", "cam15", "cam16", "cam17", "cam18", "cam19", "cam20"]


def main():
    start_book = None
    only_book = None
    with_answers = False

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--start" and i + 1 < len(args):
            start_book = args[i + 1]
            i += 2
        elif args[i] == "--only" and i + 1 < len(args):
            only_book = args[i + 1]
            i += 2
        elif args[i] == "--with-answers":
            with_answers = True
            i += 1
        else:
            i += 1

    books = [only_book] if only_book else BOOK_ORDER
    if start_book and start_book in BOOK_ORDER:
        books = [b for b in books if BOOK_ORDER.index(b) >= BOOK_ORDER.index(start_book)]

    print("=" * 60)
    print("IELTS PDF Extraction — Batch Runner")
    print(f"Books: {books}")
    print(f"Mode: {'questions + answers' if with_answers else 'questions only'}")
    print(f"Output: {OUTPUT_DIR.resolve()}")
    print(f"Cache: {CACHE_DIR.resolve()} ({len(list(CACHE_DIR.glob('*.txt')))} files)")
    print("=" * 60)

    if not with_answers:
        print("Note: Answers PDFs are Chinese study guides (not official answer keys).")
        print("     Use --with-answers to process them anyway (very slow, ~15-30s/page).")
        print()

    start_time = time.time()

    for book_id in books:
        print(f"\n{'#' * 50}")
        print(f"# {book_id.upper()}")
        print(f"{'#' * 50}")

        book_info = PDF_INVENTORY.get(book_id, {})
        for key, info in book_info.items():
            is_questions = "questions" in key or "test" in key
            is_answers = "answers" in key

            if is_answers and not with_answers:
                print(f"  SKIP answers: {info['path']} (Chinese study guide)")
                continue

            try:
                if is_questions:
                    process_questions_pdf(book_id, info)
                elif is_answers:
                    process_answers_pdf(book_id, info)
            except Exception as e:
                print(f"  ERROR in {book_id}/{key}: {e}")
                traceback.print_exc()

        elapsed = time.time() - start_time
        print(f"\n  [{book_id} done] Elapsed: {elapsed / 60:.1f} min")

    elapsed = time.time() - start_time
    print(f"\n{'=' * 60}")
    print(f"ALL DONE!")
    print(f"  Time:     {elapsed / 60:.1f} min")
    print(f"  Processed:{stats['pages_processed']}")
    print(f"  Cached:   {stats['pages_cached']}")
    print(f"  Failed:   {stats['pages_failed']}")
    print(f"  VLM calls:{stats['vlm_calls']}")
    print(f"  Output:   {OUTPUT_DIR.resolve()}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
