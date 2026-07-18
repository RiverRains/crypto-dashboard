"""Step 4 — VIDEO: base renders via Fal.ai (model-agnostic).

The contract: give a text prompt (+ optional product image), get an mp4 path.
Nothing downstream cares which model rendered it — that is the swap point.

Mock mode (no FAL_KEY): renders an animated gradient + product image with
ffmpeg, so remix/assembly can be developed and demoed for free.
"""

import json
import subprocess
import time
import urllib.request
from pathlib import Path

from .config import BASE_CLIP_SECONDS, FAL_KEY, FAL_VIDEO_MODEL, VIDEO_H, VIDEO_W, ProductBrief


def _mock_render(brief: ProductBrief, out_path: Path, seed: int) -> Path:
    """Animated vertical background; overlays product image if available."""
    hue_speed = 10 + (seed % 5) * 7
    filters = (
        f"[0:v]scale={VIDEO_W}:{VIDEO_H},"
        f"hue=H=t*{hue_speed}:s=2[bg]"
    )
    inputs = ["-f", "lavfi", "-i",
              f"gradients=size={VIDEO_W}x{VIDEO_H}:speed=0.05:duration={BASE_CLIP_SECONDS}"]
    if brief.image_paths:
        inputs += ["-i", brief.image_paths[0]]
        filters += (
            f";[1:v]scale={VIDEO_W - 200}:-1[img];"
            f"[bg][img]overlay=(W-w)/2:(H-h)/2:eval=init[v]"
        )
        vmap = "[v]"
    else:
        vmap = "[bg]"
    cmd = ["ffmpeg", "-y", *inputs, "-filter_complex", filters, "-map", vmap,
           "-t", str(BASE_CLIP_SECONDS), "-r", "30", "-pix_fmt", "yuv420p", str(out_path)]
    subprocess.run(cmd, check=True, capture_output=True)
    return out_path


def render_base(brief: ProductBrief, prompt: str, out_path: Path, seed: int = 0) -> Path:
    """One base render. EUR ~2.50 in real mode — the metered unit."""
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if not FAL_KEY:
        return _mock_render(brief, out_path, seed)

    # Fal.ai queue API: submit -> poll -> download.
    submit = urllib.request.Request(
        f"https://queue.fal.run/{FAL_VIDEO_MODEL}",
        data=json.dumps({"prompt": prompt, "aspect_ratio": "9:16",
                         "duration": BASE_CLIP_SECONDS}).encode(),
        headers={"Authorization": f"Key {FAL_KEY}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(submit, timeout=60) as resp:
        job = json.loads(resp.read())
    status_url = job["status_url"]
    response_url = job["response_url"]

    for _ in range(120):  # up to ~10 min
        time.sleep(5)
        req = urllib.request.Request(status_url, headers={"Authorization": f"Key {FAL_KEY}"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            status = json.loads(resp.read())
        if status.get("status") == "COMPLETED":
            break
        if status.get("status") in ("FAILED", "CANCELLED"):
            raise RuntimeError(f"Fal render failed: {status}")
    else:
        raise TimeoutError("Fal render timed out")

    req = urllib.request.Request(response_url, headers={"Authorization": f"Key {FAL_KEY}"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read())
    video_url = result["video"]["url"]
    with urllib.request.urlopen(video_url, timeout=300) as resp:
        out_path.write_bytes(resp.read())
    return out_path
