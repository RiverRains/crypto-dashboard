"""Central config: env keys, model registry, pricing constants."""

import os
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = Path(os.environ.get("ADFORGE_OUTPUT", ROOT / "output"))
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
FAL_KEY = os.environ.get("FAL_KEY", "")

# Model registry — swap models here, nothing downstream changes.
CLAUDE_MODEL = os.environ.get("ADFORGE_CLAUDE_MODEL", "claude-sonnet-5")
ELEVENLABS_MODEL = "eleven_multilingual_v2"
# Fal.ai model endpoint for base video renders (model-agnostic by design):
FAL_VIDEO_MODEL = os.environ.get("ADFORGE_FAL_MODEL", "fal-ai/kling-video/v2/master/text-to-video")

# Video output spec (TikTok/Reels vertical)
VIDEO_W, VIDEO_H = 1080, 1920
BASE_CLIP_SECONDS = 8

# Unit-economics guardrails (EUR) — used by cost estimator, keep honest.
COST_PER_BASE_RENDER = 2.50
COST_PER_VARIANT = 0.15
COST_PER_VOICEOVER = 0.20


@dataclass
class ProductBrief:
    """Normalized product info the whole pipeline consumes."""
    title: str
    description: str
    price: str = ""
    audience: str = ""
    language: str = "ru"  # "ru" | "en"
    image_paths: list[str] = field(default_factory=list)
    url: str = ""


@dataclass
class AdScript:
    """One ad angle produced by the script generator."""
    hook: str            # first-3-seconds on-screen hook text
    voiceover: str       # narration text
    cta: str             # call to action
    angle: str           # e.g. "problem-solution", "social-proof"


def mock_mode() -> dict[str, bool]:
    """Which providers run mocked (no key present)."""
    return {
        "claude": not ANTHROPIC_API_KEY,
        "elevenlabs": not ELEVENLABS_API_KEY,
        "fal": not FAL_KEY,
    }


def estimate_batch_cost(n_base: int, n_variants: int) -> float:
    """EUR cost estimate for a batch — the number that keeps pricing honest."""
    return round(
        n_base * (COST_PER_BASE_RENDER + COST_PER_VOICEOVER)
        + n_variants * COST_PER_VARIANT,
        2,
    )
