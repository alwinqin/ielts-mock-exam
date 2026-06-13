#!/usr/bin/env python3
"""Speech recognition server for IELTS Speaking mock exam.
Uses local whisper.cpp + ggml-small.bin (465MB) for high-accuracy offline transcription.
Runs on port 8081.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from http.server import HTTPServer, BaseHTTPRequestHandler

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
WHISPER_BIN = os.path.join(PROJECT_DIR, "src-tauri", "binaries", "whisper-cli")
MODEL_PATH = os.path.expanduser("~/whisper-models/ggml-small.bin")

if not os.path.exists(WHISPER_BIN):
    WHISPER_BIN = shutil.which("whisper-cli") or ""
if not os.path.exists(MODEL_PATH):
    MODEL_PATH = os.path.expanduser("~/.cache/whisper/tiny.pt")  # fallback unlikely to work with whisper-cli


def transcribe_audio(input_path: str) -> str:
    """Convert audio to 16kHz mono WAV, then transcribe via whisper.cpp."""
    # Step 1: normalize audio via ffmpeg
    tmp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    tmp_wav.close()
    try:
        result = subprocess.run(
            ["ffmpeg", "-y", "-i", input_path, "-ar", "16000", "-ac", "1",
             "-sample_fmt", "s16", "-f", "wav", tmp_wav.name],
            capture_output=True, timeout=30,
        )
        audio_path = tmp_wav.name if result.returncode == 0 else input_path
    except Exception:
        audio_path = input_path

    # Step 2: run whisper-cli
    try:
        result = subprocess.run(
            [WHISPER_BIN, "-m", MODEL_PATH, "-f", audio_path,
             "--language", "en", "--no-timestamps", "-oj"],
            capture_output=True, text=True, timeout=60,
        )
        if result.returncode != 0:
            return f"[whisper-cli error: {result.stderr.strip()}]"

        # whisper-cli -ojson writes {input}.json
        json_path = audio_path + ".json" if audio_path != tmp_wav.name else tmp_wav.name + ".json"
        # Actually whisper-cli always writes next to the input file. Let's parse stdout instead.
        # stdout contains the transcribed text line by line
        lines = [l.strip() for l in result.stdout.strip().split("\n") if l.strip()]
        # Also try reading the JSON output file
        if os.path.exists(json_path):
            with open(json_path) as f:
                data = json.load(f)
            os.unlink(json_path)
            text = data.get("text", "").strip()
            if text:
                return text

        # Fallback: parse from stdout
        text = " ".join(lines)
        return text if text else "(no speech detected)"
    except Exception as e:
        return f"[error: {e}]"
    finally:
        for p in [tmp_wav.name, tmp_wav.name + ".json", audio_path + ".json"]:
            if os.path.exists(p) and p != input_path:
                try:
                    os.unlink(p)
                except OSError:
                    pass


class TranscriptionHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        if self.path == "/transcribe":
            self.handle_transcribe()
        else:
            self.send_response(404)
            self.end_headers()

    def handle_transcribe(self):
        content_length = int(self.headers.get("Content-Length", 0))
        if not content_length:
            self._json_response({"error": "No audio data received"}, 400)
            return

        audio_data = self.rfile.read(content_length)
        if not audio_data:
            self._json_response({"error": "Empty audio data"}, 400)
            return

        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".webm")
        try:
            tmp.write(audio_data)
            tmp.close()
            text = transcribe_audio(tmp.name)
            self._json_response({"text": text})
        except Exception as e:
            self._json_response({"error": str(e)}, 500)
        finally:
            if os.path.exists(tmp.name):
                os.unlink(tmp.name)

    def do_GET(self):
        if self.path == "/health":
            self._json_response({
                "status": "ok",
                "whisper_bin": os.path.exists(WHISPER_BIN),
                "model": os.path.exists(MODEL_PATH),
            })
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"IELTS Speech Server running on port 8081")

    def _json_response(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())


if __name__ == "__main__":
    print(f"Whisper binary: {WHISPER_BIN} ({'OK' if os.path.exists(WHISPER_BIN) else 'MISSING'})")
    print(f"Model:          {MODEL_PATH} ({'OK' if os.path.exists(MODEL_PATH) else 'MISSING'})")
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8081
    server = HTTPServer(("0.0.0.0", port), TranscriptionHandler)
    print(f"Server:         http://localhost:{port}")
    server.serve_forever()
