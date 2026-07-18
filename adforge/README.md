# AdForge — AI Ad Generation Pipeline (Phase 0)

Turns a product URL or brief into a pack of short vertical video ads
(TikTok/Reels/marketplace format): AI scripts -> voiceover -> base video renders
-> cheap ffmpeg remix variants.

**Unit economics by design:** few expensive base renders (~EUR 2.50 each) are
remixed into many variants (~EUR 0.15 each). A 20-ad pack costs ~EUR 13 to
produce and sells for EUR 49+.

## Quick start

```bash
# Full mock mode — no API keys needed, placeholder visuals:
python3 cli.py demo

# From a product URL:
python3 cli.py url "https://example-shop.com/product" --lang ru

# From a manual brief (concierge mode):
python3 cli.py brief briefs/client1.json
```

Output lands in `output/batch/` with a `manifest.json` (files, hooks, cost estimate).

## Going live

Set keys in the environment (each one flips its pipeline stage from mock to real):

| Env var | Provider | Role |
|---|---|---|
| `ANTHROPIC_API_KEY` | Claude | Ad scripts (hooks, VO text, CTA) |
| `ELEVENLABS_API_KEY` | ElevenLabs | Voiceover (RU/EN) |
| `FAL_KEY` | Fal.ai | Base video renders (model set via `ADFORGE_FAL_MODEL`) |

Requires `ffmpeg` (and DejaVu fonts for Cyrillic drawtext) on the host.

## Architecture

```
cli.py                  orchestrator CLI
adforge/config.py       env, model registry, pricing constants
adforge/ingest.py       product URL/JSON -> ProductBrief
adforge/scripts_gen.py  Claude -> N AdScripts (angles/hooks/CTA)
adforge/voice.py        ElevenLabs TTS (mock: tone track)
adforge/video_gen.py    Fal.ai base renders (mock: animated gradient)
adforge/remix.py        ffmpeg variant engine: hook/caption/CTA overlays
adforge/pipeline.py     batch orchestration + manifest + cost estimate
landing/index.html      RU/EN landing page (static, deploy anywhere)
```

Design rules:
- **Model-agnostic:** video step takes prompt -> mp4; swap models in config only.
- **Mock-first:** every stage runs without keys so the pipeline is always testable.
- **Metered unit = base render.** Variants are near-free; never sell unlimited bases.

## Phase roadmap

- **Phase 0 (this):** CLI engine + landing. Concierge delivery by hand.
- **Phase 1:** 5-10 paid pilot packs (EUR 49-99) via Telegram seller communities.
- **Phase 2:** Self-serve SaaS (Next.js + Supabase + Stripe + queue) on this engine.
