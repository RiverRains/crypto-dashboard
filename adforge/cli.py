#!/usr/bin/env python3
"""AdForge CLI — Phase 0 concierge tool.

Usage:
  python3 cli.py demo                          # run full pipeline on a demo product (mock-safe)
  python3 cli.py url https://... --lang ru     # brief from a product URL
  python3 cli.py brief my_product.json         # brief from a JSON file (concierge mode)

Brief JSON shape:
  {"title": "...", "description": "...", "price": "19.99", "audience": "...", "language": "ru"}
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from adforge.config import ProductBrief, mock_mode  # noqa: E402
from adforge.ingest import brief_from_json, brief_from_url  # noqa: E402
from adforge.pipeline import run_batch  # noqa: E402

DEMO = ProductBrief(
    title="Умная бутылка HydraSmart",
    description="Бутылка напоминает пить воду, светится и считает выпитое. Держит температуру 12 часов.",
    price="29.99",
    audience="Люди 20-40, следящие за здоровьем",
    language="ru",
)


def main() -> None:
    p = argparse.ArgumentParser(description="AdForge pipeline")
    p.add_argument("mode", choices=["demo", "url", "brief"])
    p.add_argument("target", nargs="?", help="URL or brief.json path")
    p.add_argument("--lang", default="ru", choices=["ru", "en"])
    p.add_argument("--bases", type=int, default=3, help="number of base renders (the metered unit)")
    args = p.parse_args()

    if args.mode == "demo":
        brief = DEMO
    elif args.mode == "url":
        if not args.target:
            p.error("url mode needs a URL")
        brief = brief_from_url(args.target, language=args.lang)
    else:
        if not args.target:
            p.error("brief mode needs a JSON path")
        brief = brief_from_json(args.target)

    mocks = mock_mode()
    live = [k for k, v in mocks.items() if not v]
    print(f"Product: {brief.title}")
    print(f"Providers live: {live or 'NONE (full mock mode — outputs are placeholders)'}")

    manifest = run_batch(brief, n_base=args.bases)

    print(f"\nDone: {len(manifest['bases'])} base renders -> {len(manifest['variants'])} ad variants")
    print(f"Estimated real-mode cost: EUR {manifest['estimated_cost_eur']}")
    for v in manifest["variants"]:
        print(f"  {v['file']}  [{v['style']}] {v['hook'][:40]}")


if __name__ == "__main__":
    main()
