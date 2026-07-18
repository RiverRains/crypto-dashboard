"""Step 1 — INGEST: turn a product URL or manual input into a ProductBrief.

Phase 0 keeps scraping minimal: og:title/og:description/og:image + heuristics.
Marketplace-specific extractors (Wildberries/Ozon/Kaspi) come in Phase 2 —
they are JS-heavy and need either their public card APIs or a headless browser.
"""

import json
import re
import urllib.request
from pathlib import Path

from .config import OUTPUT_DIR, ProductBrief

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36"


def _fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8", errors="replace")


def _meta(html: str, prop: str) -> str:
    m = re.search(
        rf'<meta[^>]+(?:property|name)=["\']{re.escape(prop)}["\'][^>]+content=["\']([^"\']+)',
        html, re.I,
    ) or re.search(
        rf'<meta[^>]+content=["\']([^"\']+)["\'][^>]+(?:property|name)=["\']{re.escape(prop)}["\']',
        html, re.I,
    )
    return m.group(1).strip() if m else ""


def brief_from_url(url: str, language: str = "ru") -> ProductBrief:
    html = _fetch(url)
    title = _meta(html, "og:title") or (re.search(r"<title[^>]*>([^<]+)", html, re.I) or [None, ""])[1]
    description = _meta(html, "og:description") or _meta(html, "description")
    image = _meta(html, "og:image")

    image_paths: list[str] = []
    if image:
        try:
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            dest = OUTPUT_DIR / "product_image.jpg"
            req = urllib.request.Request(image, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=20) as resp:
                dest.write_bytes(resp.read())
            image_paths.append(str(dest))
        except Exception:
            pass  # image is nice-to-have; the pipeline works without it

    return ProductBrief(
        title=(title or "").strip()[:200],
        description=(description or "").strip()[:1000],
        language=language,
        image_paths=image_paths,
        url=url,
    )


def brief_from_json(path: str) -> ProductBrief:
    """Manual brief (concierge mode): a JSON file the operator fills in."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return ProductBrief(**data)
