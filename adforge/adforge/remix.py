"""Step 5 — REMIX: the margin engine.

Takes ONE expensive base render and produces MANY cheap variants:
different hook text (first 3s), caption styles, CTA end text, voiceover mix.
Each variant is an ffmpeg re-encode (~cents), not a new AI render (~euros).

drawtext uses textfile= to sidestep escaping issues (works with Cyrillic).
"""

import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

from .config import FONT_BOLD, VIDEO_H, VIDEO_W

HOOK_SECONDS = 3.0

# Caption styles: (box color, text color, y-position factor)
CAPTION_STYLES = {
    "classic": ("black@0.55", "white", 0.78),
    "brand":   ("0x7C3AED@0.75", "white", 0.78),
    "top":     ("black@0.55", "white", 0.10),
}


@dataclass
class VariantSpec:
    hook: str
    cta: str
    caption_style: str = "classic"
    voiceover_path: str | None = None


def _textfile(text: str) -> str:
    f = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8")
    f.write(text)
    f.close()
    return f.name


def _wrap(text: str, width: int = 22) -> str:
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        lines.append(cur)
    return "\n".join(lines)


def make_variant(base_video: Path, spec: VariantSpec, out_path: Path) -> Path:
    """Render one variant from a base video. Cost: ~EUR 0.02-0.15 of compute."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    box, color, ypos = CAPTION_STYLES.get(spec.caption_style, CAPTION_STYLES["classic"])

    hook_file = _textfile(_wrap(spec.hook, 18))
    cta_file = _textfile(_wrap(spec.cta, 20))

    draw_hook = (
        f"drawtext=fontfile={FONT_BOLD}:textfile='{hook_file}':"
        f"fontsize=88:fontcolor=white:borderw=6:bordercolor=black:"
        f"x=(w-text_w)/2:y=h*0.30:line_spacing=16:"
        f"enable='lt(t,{HOOK_SECONDS})'"
    )
    draw_cta = (
        f"drawtext=fontfile={FONT_BOLD}:textfile='{cta_file}':"
        f"fontsize=64:fontcolor={color}:box=1:boxcolor={box}:boxborderw=24:"
        f"x=(w-text_w)/2:y=h*{ypos}:line_spacing=12:"
        f"enable='gte(t,{HOOK_SECONDS})'"
    )
    vf = f"scale={VIDEO_W}:{VIDEO_H},{draw_hook},{draw_cta}"

    cmd = ["ffmpeg", "-y", "-i", str(base_video)]
    if spec.voiceover_path:
        cmd += ["-i", spec.voiceover_path,
                "-map", "0:v", "-map", "1:a", "-shortest"]
    cmd += ["-vf", vf, "-c:v", "libx264", "-preset", "fast", "-crf", "21",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out_path)]
    subprocess.run(cmd, check=True, capture_output=True)
    return out_path
