"""Step 3 — VOICE: ElevenLabs TTS for the voiceover track.

Mock mode (no key): synthesizes a quiet placeholder tone track with ffmpeg so
the assembly step always has a real audio file to work with.
"""

import json
import subprocess
import urllib.request
from pathlib import Path

from .config import ELEVENLABS_API_KEY, ELEVENLABS_MODEL

# Default voices (multilingual model handles RU and EN)
VOICE_IDS = {"ru": "EXAVITQu4vr4xnSDxMaL", "en": "EXAVITQu4vr4xnSDxMaL"}


def synthesize(text: str, out_path: Path, language: str = "ru", duration_hint: float = 8.0) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if not ELEVENLABS_API_KEY:
        # Placeholder: soft 220Hz tone at low volume, correct duration.
        subprocess.run(
            ["ffmpeg", "-y", "-f", "lavfi", "-i",
             f"sine=frequency=220:duration={duration_hint}",
             "-filter:a", "volume=0.05", str(out_path)],
            check=True, capture_output=True,
        )
        return out_path

    body = json.dumps({
        "text": text,
        "model_id": ELEVENLABS_MODEL,
        "voice_settings": {"stability": 0.45, "similarity_boost": 0.75},
    }).encode()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_IDS.get(language, VOICE_IDS['en'])}",
        data=body,
        headers={"Content-Type": "application/json", "xi-api-key": ELEVENLABS_API_KEY},
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        out_path.write_bytes(resp.read())
    return out_path
