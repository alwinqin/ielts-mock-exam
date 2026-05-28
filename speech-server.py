#!/usr/bin/env python3
"""Speech recognition server for IELTS Speaking mock exam.
Runs on port 8081, accepts WAV audio via POST /transcribe, returns transcription text.
"""

import json
import os
import sys
import tempfile
import warnings
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

warnings.filterwarnings("ignore")

# Lazy-load whisper model
_model = None

def get_model():
    global _model
    if _model is None:
        print("Loading Whisper tiny model...", flush=True)
        import whisper
        _model = whisper.load_model("tiny")
        print("Whisper model loaded.", flush=True)
    return _model

class TranscriptionHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)

        if parsed.path == "/transcribe":
            self.handle_transcribe()
        else:
            self.send_response(404)
            self.end_headers()

    def handle_transcribe(self):
        content_length = int(self.headers.get("Content-Length", 0))
        audio_data = self.rfile.read(content_length)

        if not audio_data:
            self._json_response({"error": "No audio data received"}, 400)
            return

        # Save to temp file
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        try:
            tmp.write(audio_data)
            tmp.close()

            model = get_model()
            result = model.transcribe(tmp.name, language="en")
            text = result.get("text", "").strip()

            self._json_response({"text": text, "segments": result.get("segments", [])})
        except Exception as e:
            self._json_response({"error": str(e)}, 500)
        finally:
            os.unlink(tmp.name)

    def do_GET(self):
        if self.path == "/health":
            self._json_response({"status": "ok", "model_loaded": _model is not None})
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
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8081
    server = HTTPServer(("0.0.0.0", port), TranscriptionHandler)
    print(f"Speech recognition server running on http://localhost:{port}")
    print("Endpoints: POST /transcribe, GET /health")
    server.serve_forever()
