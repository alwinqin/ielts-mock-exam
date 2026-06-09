"""Shared VLM client configuration and utilities.

Usage:
    from vlm_client import VLM_API_URL, VLM_MODEL, vlm_call, render_jpeg

Environment variables:
    VLM_API_URL  — override the default API endpoint
    VLM_MODEL    — override the default model name
"""

import base64
import io
import os
import time
from pathlib import Path
from typing import Optional

import fitz
import requests
from PIL import Image

VLM_API_URL = os.environ.get(
    "VLM_API_URL",
    "http://100.114.112.77:8000/v1/chat/completions",
)
VLM_MODEL = os.environ.get("VLM_MODEL", "Qwen3.6-27B")

PDF_DIR = Path(__file__).parent / "data" / "cambridge" / "pdf"


def render_jpeg(doc: fitz.Document, pg: int, dpi: int = 200) -> str:
    """Render a PDF page as a base64-encoded JPEG string."""
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = doc[pg].get_pixmap(matrix=mat)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode()


def vlm_call(
    img_b64: str,
    prompt: str,
    max_tokens: int = 2048,
    temperature: float = 0.0,
    retries: int = 3,
    timeout: int = 120,
) -> Optional[str]:
    """Call the VLM API with retry logic.

    Args:
        img_b64: Base64-encoded JPEG image.
        prompt: Text prompt to send with the image.
        max_tokens: Maximum completion tokens.
        temperature: Sampling temperature (0.0 = deterministic).
        retries: Number of retry attempts on failure.
        timeout: HTTP request timeout in seconds.

    Returns:
        The model's text response, or None if all attempts fail.
    """
    for attempt in range(retries):
        try:
            resp = requests.post(
                VLM_API_URL,
                headers={"Content-Type": "application/json"},
                json={
                    "model": VLM_MODEL,
                    "messages": [{
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {
                                "url": f"data:image/jpeg;base64,{img_b64}"}},
                        ],
                    }],
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                },
                timeout=timeout,
            )
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"]
            time.sleep(min((attempt + 1) * 10, 60))
        except (requests.ConnectionError, requests.Timeout):
            time.sleep(3)
        except Exception:
            time.sleep(3)
    return None
