const fmtUsd = (n) => {
  if (n === null || n === undefined) return "—";
  return new Intl.NumberFormat(undefined, { style: "currency", currency: "USD", maximumFractionDigits: n < 1 ? 6 : 2 }).format(n);
};
const fmtCompact = (n) => {
  if (n === null || n === undefined) return "—";
  return new Intl.NumberFormat(undefined, { notation: "compact", maximumFractionDigits: 2 }).format(n);
};
const pct = (n) => {
  if (n === null || n === undefined) return "—";
  return (Math.round(n * 100) / 100).toFixed(2) + "%";
};

let days = 30;
let chart;
let currentMode = "demo";
let refreshTimer = null;

async function fetchJSON(url){
  const r = await fetch(url);
  if (!r.ok) {
    let msg = `HTTP ${r.status}`;
    try { const j = await r.json(); if (j && j.detail) msg = j.detail; } catch(e) {}
    throw new Error(msg);
  }
  return await r.json();
}

function setCoinError(message){
  const el = document.getElementById("coinError");
  if (!el) return;
  if (!message){
    el.classList.add("d-none");
    el.textContent = "";
    return;
  }
  el.textContent = message;
  el.classList.remove("d-none");
}

function setLastUpdated(tsMs){
  const wrap = document.getElementById("lastUpdatedWrap");
  const text = document.getElementById("lastUpdatedText");
  if (!wrap || !text) return;
  wrap.classList.remove("d-none");
  const d = new Date(tsMs || Date.now());
  const hh = String(d.getHours()).padStart(2,"0");
  const mm = String(d.getMinutes()).padStart(2,"0");
  const ss = String(d.getSeconds()).padStart(2,"0");
  text.textContent = `${hh}:${mm}:${ss}`;
}

function configureLiveRefresh(){
  if (refreshTimer) clearInterval(refreshTimer);
  if (currentMode !== "live") return;
  refreshTimer = setInterval(() => load().catch(console.error), 30000);
}

function buildChart(ctx, labels, values){
  if (chart) chart.destroy();
  chart = new Chart(ctx, {
    type: "line",
    data: { labels, datasets: [{ label: "Price (USD)", data: values, tension: 0.25, pointRadius: 0 }] },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        x: { ticks: { color: "#9aa4b2" }, grid: { color: "rgba(255,255,255,0.06)" } },
        y: { ticks: { color: "#9aa4b2" }, grid: { color: "rgba(255,255,255,0.06)" } },
      }
    }
  });
}

function makeLabels(prices, days){
  const includeTime = days <= 7;
  return prices.map(p => {
    const d = new Date(p[0]);
    return includeTime
      ? d.toLocaleString(undefined, { month: "short", day: "2-digit", hour: "2-digit" })
      : d.toLocaleDateString(undefined, { month: "short", day: "2-digit" });
  });
}

async function load(){
  const id = window.__COIN_ID__;
  setCoinError("");
  try {
    const data = await fetchJSON(`/api/coin/${encodeURIComponent(id)}?days=${days}`);
    const m = data.market || {};
    document.getElementById("coinName").textContent = m.name || id;
    document.getElementById("coinSymbol").textContent = (m.symbol || "").toUpperCase();

    document.getElementById("price").textContent = fmtUsd(m.current_price);
    const ch = m.price_change_percentage_24h;
    const cls = (ch ?? 0) >= 0 ? "pos" : "neg";
    const chEl = document.getElementById("ch24");
    chEl.textContent = pct(ch);
    chEl.className = cls;

    document.getElementById("cap").textContent = "$" + fmtCompact(m.market_cap);
    document.getElementById("vol").textContent = "$" + fmtCompact(m.total_volume);

    const prices = data.chart?.prices || [];
    const labels = makeLabels(prices, days);
    const values = prices.map(p => p[1]);
    buildChart(document.getElementById("coinChart"), labels, values);

    setLastUpdated(data.ts || Date.now());
  } catch (e) {
    setCoinError(`Chart failed to load (${e.message}). If LIVE is blocked, switch to DEMO.`);
  }
}

document.getElementById("toggleMode").addEventListener("click", async () => {
  currentMode = await toggleMode();
  configureLiveRefresh();
  await load();
});

document.querySelectorAll(".range-btn").forEach(btn => {
  btn.addEventListener("click", async () => {
    document.querySelectorAll(".range-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    days = parseInt(btn.dataset.days, 10);
    await load();
  });
});

(async function main(){
  const m = await getMode();
  currentMode = m.mode;
  updateModeUI(currentMode);
  configureLiveRefresh();
  await load();
})().catch(console.error);
