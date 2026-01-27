# Crypto Market Dashboard (Demo + Live) — Fix #5

Fixes:
- **Top 50 now works**: demo dataset expanded to 50 coins (top10 real + 40 synthetic)
- `/api/market` returns `{ items, ts, mode }`
- "Last updated" now shows **HH:MM:SS** timestamp (instead of "Xs ago")
- LIVE mode still refreshes every 30 seconds (LIVE affects top10; synthetic coins remain demo)

## Run
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```
Open: http://127.0.0.1:8000
