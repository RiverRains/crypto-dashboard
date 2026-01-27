from __future__ import annotations

import asyncio
import json
import time
from typing import Any, Dict, List, Optional, Tuple

import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

app = FastAPI(title="Crypto Market Dashboard (Demo + Live)")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

DATA_MODE: str = "demo"  # demo | live

_cache: Dict[str, Tuple[float, Any]] = {}

def cache_get(key: str) -> Optional[Any]:
    entry = _cache.get(key)
    if not entry:
        return None
    exp, val = entry
    if time.time() > exp:
        _cache.pop(key, None)
        return None
    return val

def cache_set(key: str, val: Any, ttl: int) -> None:
    _cache[key] = (time.time() + ttl, val)

# ----------------------------
# Demo data (offline-safe)
# ----------------------------
TOP10: List[Dict[str, Any]] = [
    {"id":"bitcoin","symbol":"btc","name":"Bitcoin","image":"https://assets.coingecko.com/coins/images/1/large/bitcoin.png","current_price": 0,"price_change_percentage_24h": 0,"market_cap": 1450000000000,"total_volume": 28000000000},
    {"id":"ethereum","symbol":"eth","name":"Ethereum","image":"https://assets.coingecko.com/coins/images/279/large/ethereum.png","current_price": 0,"price_change_percentage_24h": 0,"market_cap": 450000000000,"total_volume": 16000000000},
    {"id":"solana","symbol":"sol","name":"Solana","image":"https://assets.coingecko.com/coins/images/4128/large/solana.png","current_price": 0,"price_change_percentage_24h": 0,"market_cap": 75000000000,"total_volume": 3500000000},
    {"id":"binancecoin","symbol":"bnb","name":"BNB","image":"https://assets.coingecko.com/coins/images/825/large/binance-coin-logo.png","current_price": 0,"price_change_percentage_24h": 0,"market_cap": 82000000000,"total_volume": 1200000000},
    {"id":"ripple","symbol":"xrp","name":"XRP","image":"https://assets.coingecko.com/coins/images/44/large/xrp-symbol-white-128.png","current_price": 0,"price_change_percentage_24h": 0,"market_cap": 65000000000,"total_volume": 2500000000},
    {"id":"cardano","symbol":"ada","name":"Cardano","image":"https://assets.coingecko.com/coins/images/975/large/cardano.png","current_price": 0,"price_change_percentage_24h": 0,"market_cap": 18000000000,"total_volume": 550000000},
    {"id":"dogecoin","symbol":"doge","name":"Dogecoin","image":"https://assets.coingecko.com/coins/images/5/large/dogecoin.png","current_price": 0,"price_change_percentage_24h": 0,"market_cap": 24000000000,"total_volume": 900000000},
    {"id":"polkadot","symbol":"dot","name":"Polkadot","image":"https://assets.coingecko.com/coins/images/12171/large/polkadot.png","current_price": 0,"price_change_percentage_24h": 0,"market_cap": 9000000000,"total_volume": 280000000},
    {"id":"chainlink","symbol":"link","name":"Chainlink","image":"https://assets.coingecko.com/coins/images/877/large/chainlink-new-logo.png","current_price": 0,"price_change_percentage_24h": 0,"market_cap": 11000000000,"total_volume": 520000000},
    {"id":"matic-network","symbol":"matic","name":"Polygon","image":"https://assets.coingecko.com/coins/images/4713/large/matic-token-icon.png","current_price": 0,"price_change_percentage_24h": 0,"market_cap": 6500000000,"total_volume": 310000000},
]

def placeholder_svg(letter: str) -> str:
    letter = (letter[:1] or "?").upper()
    svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='64' height='64'>
    <rect width='100%' height='100%' rx='14' ry='14' fill='#1f2a44'/>
    <text x='50%' y='54%' dominant-baseline='middle' text-anchor='middle'
      font-family='Arial' font-size='30' fill='#e7eefc'>{letter}</text>
    </svg>"""
    return "data:image/svg+xml;utf8," + svg.replace("#", "%23").replace("\n", "")

DEMO_MARKET: List[Dict[str, Any]] = []
DEMO_MARKET.extend(TOP10)
for i in range(11, 51):
    sym = f"c{i}"
    DEMO_MARKET.append({
        "id": f"demo-coin-{i}",
        "symbol": sym,
        "name": f"Demo Coin {i}",
        "image": placeholder_svg(sym[0]),
        "current_price": 0,
        "price_change_percentage_24h": 0,
        "market_cap": 0,
        "total_volume": 0,
    })

def _demo_prices(seed: int, days: int) -> List[List[float]]:
    import math, random
    rng = random.Random(seed)
    now_ms = int(time.time() * 1000)

    if days <= 7:
        points, step_ms = 7 * 24, 60 * 60 * 1000
    elif days <= 30:
        points, step_ms = 30 * 6, 4 * 60 * 60 * 1000
    else:
        points, step_ms = min(days, 180), 24 * 60 * 60 * 1000

    base = rng.uniform(0.5, 50000)
    drift = rng.uniform(-0.02, 0.03)
    vol = rng.uniform(0.01, 0.06)

    out: List[List[float]] = []
    price = base
    for i in range(points):
        t = now_ms - (points - 1 - i) * step_ms
        wave = math.sin(i / 6.0) * vol * base
        noise = rng.uniform(-1, 1) * vol * base * 0.35
        price = max(0.0001, price * (1 + drift / points) + wave + noise)
        out.append([t, float(price)])
    return out

DEMO_CHARTS: Dict[str, Dict[int, Dict[str, Any]]] = {}
for idx, c in enumerate(DEMO_MARKET):
    DEMO_CHARTS[c["id"]] = {
        7: {"prices": _demo_prices(1000 + idx, 7)},
        30: {"prices": _demo_prices(2000 + idx, 30)},
        90: {"prices": _demo_prices(3000 + idx, 90)},
    }
    p = DEMO_CHARTS[c["id"]][30]["prices"]
    cur = p[-1][1] if p else 0.0
    c["current_price"] = round(cur, 6 if cur < 1 else 3)
    if len(p) >= 2 and p[-2][1] != 0:
        c["price_change_percentage_24h"] = round(((p[-1][1] - p[-2][1]) / p[-2][1]) * 100.0, 3)
    else:
        c["price_change_percentage_24h"] = 0.0
    rank = idx + 1
    cap_base = 1_500_000_000_000 if rank == 1 else max(50_000_000, int(600_000_000_000 / (rank ** 1.2)))
    vol_base = max(10_000_000, int(cap_base * 0.02))
    c["market_cap"] = cap_base
    c["total_volume"] = vol_base

# ----------------------------
# Live mode (Binance) - no key
# ----------------------------
BINANCE = "https://api.binance.com"
UA = "Mozilla/5.0 (PortfolioDashboard/1.0)"
BINANCE_MAP = {
    "bitcoin": "BTCUSDT",
    "ethereum": "ETHUSDT",
    "solana": "SOLUSDT",
    "binancecoin": "BNBUSDT",
    "ripple": "XRPUSDT",
    "cardano": "ADAUSDT",
    "dogecoin": "DOGEUSDT",
    "polkadot": "DOTUSDT",
    "chainlink": "LINKUSDT",
    "matic-network": "MATICUSDT",
}

async def bn_get(path: str, params: Dict[str, Any] | None = None, retries: int = 2) -> Any:
    url = f"{BINANCE}{path}"
    backoff = 0.4
    async with httpx.AsyncClient(timeout=20, headers={"accept":"application/json","user-agent":UA}) as client:
        for attempt in range(retries + 1):
            r = await client.get(url, params=params)
            if r.status_code == 200:
                return r.json()
            if r.status_code in (418, 429, 503) and attempt < retries:
                await asyncio.sleep(backoff)
                backoff *= 1.8
                continue
            raise HTTPException(status_code=502, detail=f"Binance error {r.status_code}: {(r.text or '')[:220]}")

def _interval_for_days(days: int) -> tuple[str, int]:
    if days <= 7:
        return ("1h", 7*24)
    if days <= 30:
        return ("4h", 30*6)
    return ("1d", min(days, 180))

async def live_market_patch(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    symbols = [BINANCE_MAP[it["id"]] for it in items if it["id"] in BINANCE_MAP]
    if not symbols:
        return items

    symbols_param = json.dumps(symbols, separators=(",", ":"))

    key = "bn:ticker24:" + symbols_param
    cached = cache_get(key)
    if cached is None:
        data = await bn_get("/api/v3/ticker/24hr", params={"symbols": symbols_param})
        cache_set(key, data, ttl=20)
    else:
        data = cached

    by_sym = {d["symbol"]: d for d in data} if isinstance(data, list) else {}
    out: List[Dict[str, Any]] = []
    for it in items:
        sym = BINANCE_MAP.get(it["id"])
        it2 = dict(it)
        if sym and sym in by_sym:
            t = by_sym[sym]
            it2["current_price"] = float(t.get("lastPrice", it2["current_price"]))
            it2["price_change_percentage_24h"] = float(t.get("priceChangePercent", it2["price_change_percentage_24h"]))
            it2["total_volume"] = float(t.get("quoteVolume", it2["total_volume"]))
        out.append(it2)
    return out

async def live_chart(coin_id: str, days: int) -> Dict[str, Any]:
    sym = BINANCE_MAP.get(coin_id)
    if not sym:
        return DEMO_CHARTS.get(coin_id, {}).get(days, DEMO_CHARTS["bitcoin"][30])

    interval, limit = _interval_for_days(days)
    key = f"bn:klines:{sym}:{interval}:{limit}"
    cached = cache_get(key)
    if cached is None:
        kl = await bn_get("/api/v3/klines", params={"symbol": sym, "interval": interval, "limit": limit})
        cache_set(key, kl, ttl=30)
    else:
        kl = cached

    prices: List[List[float]] = []
    for row in kl:
        prices.append([int(row[0]), float(row[4])])
    return {"prices": prices, "meta": {"interval": interval, "symbol": sym}}

# ----------------------------
# Routes
# ----------------------------
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/coin/{coin_id}", response_class=HTMLResponse)
async def coin_page(request: Request, coin_id: str):
    return templates.TemplateResponse("coin.html", {"request": request, "coin_id": coin_id})

@app.get("/api/mode")
async def mode(set: Optional[str] = None):
    global DATA_MODE
    if set:
        v = set.strip().lower()
        if v not in ("demo", "live"):
            raise HTTPException(status_code=400, detail="mode must be demo or live")
        DATA_MODE = v
    return {"mode": DATA_MODE, "live_provider": "binance", "currency": "USD (USDT≈USD)"}

@app.get("/api/global")
async def global_data():
    return {
        "data": {
            "total_market_cap": {"usd": 2500000000000},
            "total_volume": {"usd": 95000000000},
            "market_cap_percentage": {"btc": 53.2},
            "market_cap_change_percentage_24h_usd": 0.45,
        },
        "note": "Demo KPIs (stable)",
        "ts": int(time.time() * 1000),
    }

@app.get("/api/market")
async def market(limit: int = Query(10, ge=1, le=250)):
    items = DEMO_MARKET[: min(limit, len(DEMO_MARKET))]
    if DATA_MODE == "live":
        items = await live_market_patch(items)
    return {"items": items, "ts": int(time.time() * 1000), "mode": DATA_MODE}

@app.get("/api/coin/{coin_id}")
async def coin(coin_id: str, days: int = Query(30, ge=1, le=365)):
    d = 7 if days <= 7 else 30 if days <= 30 else 90
    if DATA_MODE == "live":
        chart = await live_chart(coin_id, d)
        patched = await live_market_patch(DEMO_MARKET[:50])
        m = next((x for x in patched if x["id"] == coin_id), None)
        return {"chart": chart, "market": m, "mode": "live", "ts": int(time.time() * 1000)}
    chart = DEMO_CHARTS.get(coin_id, {}).get(d) or DEMO_CHARTS["bitcoin"][30]
    m = next((x for x in DEMO_MARKET if x["id"] == coin_id), None)
    return {"chart": chart, "market": m, "mode": "demo", "ts": int(time.time() * 1000)}
