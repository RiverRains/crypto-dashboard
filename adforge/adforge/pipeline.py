"""Orchestrator: brief -> scripts -> voice -> base renders -> variant matrix.

The batch strategy encodes the unit economics:
  few expensive base renders x many cheap remixes = a 15-20 ad pack for ~EUR 13.
"""

import json
from dataclasses import asdict
from pathlib import Path

from .config import OUTPUT_DIR, ProductBrief, estimate_batch_cost, mock_mode
from .remix import CAPTION_STYLES, VariantSpec, make_variant
from .scripts_gen import generate_scripts
from .video_gen import render_base
from .voice import synthesize


def run_batch(brief: ProductBrief, n_base: int = 3, styles: list[str] | None = None,
              out_dir: Path | None = None) -> dict:
    """Generate an ad pack. Returns a manifest dict (also written to disk)."""
    out = Path(out_dir or OUTPUT_DIR) / "batch"
    out.mkdir(parents=True, exist_ok=True)
    styles = styles or list(CAPTION_STYLES)

    scripts = generate_scripts(brief, n=n_base)

    variants, base_files = [], []
    for i, script in enumerate(scripts[:n_base]):
        base_path = out / f"base_{i}.mp4"
        prompt = (
            f"Vertical 9:16 product ad footage: {brief.title}. {brief.description[:150]}. "
            f"Angle: {script.angle}. Clean, bright, commercial look, no text."
        )
        render_base(brief, prompt, base_path, seed=i)
        base_files.append(str(base_path))

        vo_path = out / f"vo_{i}.mp3"
        synthesize(script.voiceover, vo_path, language=brief.language)

        # Variant matrix: this base x every caption style (+ hook swaps across scripts)
        for style in styles:
            v_path = out / f"ad_{i}_{style}.mp4"
            make_variant(Path(base_path), VariantSpec(
                hook=script.hook, cta=script.cta,
                caption_style=style, voiceover_path=str(vo_path),
            ), v_path)
            variants.append({"file": str(v_path), "base": i, "style": style,
                             "hook": script.hook, "angle": script.angle})

    manifest = {
        "product": brief.title,
        "language": brief.language,
        "mock_mode": mock_mode(),
        "bases": base_files,
        "variants": variants,
        "estimated_cost_eur": estimate_batch_cost(n_base, len(variants)),
        "scripts": [asdict(s) for s in scripts],
    }
    (out / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest
