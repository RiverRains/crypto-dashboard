"""Step 2 — SCRIPT: Claude writes N ad scripts (hooks/angles/CTA) for the product.

With ANTHROPIC_API_KEY set -> real Claude call. Without -> deterministic mocks
so the pipeline is testable end-to-end for free.
"""

import json
import urllib.request

from .config import ANTHROPIC_API_KEY, CLAUDE_MODEL, AdScript, ProductBrief

ANGLES = ["problem-solution", "social-proof", "curiosity-hook", "before-after", "direct-offer"]

_PROMPT = """You write short-form video ad scripts (TikTok/Reels, 8-15 seconds) that convert.

Product: {title}
Description: {description}
Price: {price}
Audience: {audience}
Language: {lang_name}

Write {n} DIFFERENT ad scripts, one per angle: {angles}.
Rules:
- HOOK: max 8 words, on-screen text for the first 3 seconds. Must stop the scroll.
- VOICEOVER: 2-3 short sentences, spoken, conversational, no corporate speak.
- CTA: max 6 words.
- Everything in {lang_name}.

Return ONLY a JSON array: [{{"hook": "...", "voiceover": "...", "cta": "...", "angle": "..."}}]"""


def _mock_scripts(brief: ProductBrief, n: int) -> list[AdScript]:
    ru = brief.language == "ru"
    out = []
    for i in range(n):
        angle = ANGLES[i % len(ANGLES)]
        if ru:
            out.append(AdScript(
                hook=f"Это изменит твой {brief.title[:20]}…"[:60],
                voiceover=f"Смотри, что я нашёл: {brief.title}. {brief.description[:80]}. Попробуй сам — не пожалеешь.",
                cta="Закажи сегодня со скидкой",
                angle=angle,
            ))
        else:
            out.append(AdScript(
                hook=f"This changes everything about {brief.title[:20]}"[:60],
                voiceover=f"Look what I found: {brief.title}. {brief.description[:80]}. Try it yourself.",
                cta="Order today and save",
                angle=angle,
            ))
    return out


def generate_scripts(brief: ProductBrief, n: int = 5) -> list[AdScript]:
    if not ANTHROPIC_API_KEY:
        return _mock_scripts(brief, n)

    prompt = _PROMPT.format(
        title=brief.title, description=brief.description, price=brief.price or "-",
        audience=brief.audience or "general", n=n, angles=", ".join(ANGLES[:n]),
        lang_name="Russian" if brief.language == "ru" else "English",
    )
    body = json.dumps({
        "model": CLAUDE_MODEL,
        "max_tokens": 2000,
        "messages": [{"role": "user", "content": prompt}],
    }).encode()
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=body,
        headers={
            "Content-Type": "application/json",
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
        },
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read())
    text = data["content"][0]["text"]
    start, end = text.find("["), text.rfind("]") + 1
    items = json.loads(text[start:end])
    return [AdScript(**{k: it.get(k, "") for k in ("hook", "voiceover", "cta", "angle")}) for it in items[:n]]
