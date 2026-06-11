#!/bin/bash
# Audio setup for IELTS Mock Exam
# Cambridge IELTS audio files are copyrighted and cannot be distributed.
# This script helps you copy them from your own source.
set -e
cd "$(dirname "$0")"

# ---- Configuration ----
# Set this to the directory containing your Cambridge IELTS audio files.
# Expected layout: SOURCE_DIR/cam14_s1.mp3, cam14_s2.mp3, etc.
SOURCE_DIR="${1:-}"

EXPECTED_DIR="data/cambridge/audio"
REQUIRED_COUNT=112

# ---- Functions ----
check_files() {
    local total=0 missing=0
    echo "=== Checking Cambridge audio files ==="
    for cam in 14 15 16 17 18 19 20; do
        local test_missing=0
        for s in $(seq 1 16); do
            local f="cam${cam}_s${s}.mp3"
            if [ ! -f "${EXPECTED_DIR}/${f}" ]; then
                test_missing=$((test_missing + 1))
                missing=$((missing + 1))
            fi
            total=$((total + 1))
        done
        if [ "$test_missing" -gt 0 ]; then
            echo "  cam${cam}: MISSING ${test_missing}/16 files"
        else
            echo "  cam${cam}: OK (16/16)"
        fi
    done
    echo ""
    echo "Found: $((total - missing))/${total} audio files"
    if [ "$missing" -eq 0 ]; then
        echo "All audio files present."
        return 0
    else
        echo "Missing ${missing} file(s)."
        return 1
    fi
}

copy_from_source() {
    local src="$1"
    if [ ! -d "$src" ]; then
        echo "ERROR: Source directory not found: $src"
        echo "Usage: $0 /path/to/your/audio/files"
        exit 1
    fi
    mkdir -p "$EXPECTED_DIR"
    local copied=0
    for cam in 14 15 16 17 18 19 20; do
        for s in $(seq 1 16); do
            local f="cam${cam}_s${s}.mp3"
            local dest="${EXPECTED_DIR}/${f}"
            if [ -f "$dest" ]; then
                continue  # already present
            fi
            # Try multiple source layouts
            local src_file=""
            for pattern in "$src/$f" "$src/cam${cam}/$f" "$src/cambridge${cam}/$f" "$src/Cambridge${cam}/$f"; do
                if [ -f "$pattern" ]; then
                    src_file="$pattern"
                    break
                fi
            done
            if [ -n "$src_file" ]; then
                cp -v "$src_file" "$dest"
                copied=$((copied + 1))
            fi
        done
    done
    echo "Copied ${copied} file(s)."
}

# ---- Main ----
if [ -n "$SOURCE_DIR" ]; then
    echo "=== Copying audio from: $SOURCE_DIR ==="
    copy_from_source "$SOURCE_DIR"
    echo ""
fi

check_files

if [ "$?" -ne 0 ] && [ -z "$SOURCE_DIR" ]; then
    echo ""
    echo "To set up audio, specify your audio source directory:"
    echo "  bash setup-audio.sh /path/to/your/audio/files"
    echo ""
    echo "Expected formats:"
    echo "  - Flat directory: cam14_s1.mp3, cam14_s2.mp3, ..."
    echo "  - Per-test subdirs: cam14/cam14_s1.mp3, ..."
    echo ""
    echo "Audio files are from Cambridge IELTS books 14-20."
    echo "Each test has 16 sections (4 parts x 4 tracks)."
fi
