#!/bin/bash
# IELTS Mock Exam System — Startup Script (macOS/Linux)
# Usage: ./start.sh          → main server only (port 8080)
#        ./start.sh speech   → main server + speech server (ports 8080, 8081)

set -e

PORT=${PORT:-8080}
SPEECH_PORT=${SPEECH_PORT:-8081}
DIR="$(cd "$(dirname "$0")" && pwd)"

cd "$DIR"

echo "============================================"
echo "  IELTS Mock Exam System"
echo "============================================"

# Check Python3 availability
if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 not found. Please install Python 3."
    exit 1
fi

echo ""
echo "Starting main server at http://localhost:$PORT ..."
python3 -m http.server "$PORT" &
MAIN_PID=$!
echo "  Main server PID: $MAIN_PID"

SPEECH_PID=""
if [ "$1" = "speech" ]; then
    echo ""
    echo "Starting speech recognition server at http://localhost:$SPEECH_PORT ..."

    # Check if openai-whisper is installed
    if ! python3 -c "import whisper" 2>/dev/null; then
        echo "  WARNING: openai-whisper not installed."
        echo "  Install with: pip3 install openai-whisper"
        echo "  Speech recognition will NOT work."
    else
        python3 speech-server.py "$SPEECH_PORT" &
        SPEECH_PID=$!
        echo "  Speech server PID: $SPEECH_PID"
    fi
fi

echo ""
echo "============================================"
echo "  Open in browser: http://localhost:$PORT"
echo "  Press Ctrl+C to stop all servers."
echo "============================================"

cleanup() {
    echo ""
    echo "Stopping servers..."
    kill "$MAIN_PID" 2>/dev/null
    [ -n "$SPEECH_PID" ] && kill "$SPEECH_PID" 2>/dev/null
    echo "All servers stopped."
    exit 0
}

trap cleanup INT TERM

wait
