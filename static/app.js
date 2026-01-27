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

const WATCH_KEY = "cg_watchlist";
const getWatch = () => new Set(JSON.parse(localStorage.getItem(WATCH_KEY) || "[]"));
const setWatch = (set) => localStorage.setItem(WATCH_KEY, JSON.stringify([...set]));

let marketData = [];
let sortKey = "market_cap";
let sortDir = "desc";
let selectedCoinId = "bitcoin";
let selectedDays = 30;
let chart;

let currentMode = "demo";
let refreshTimer = null;

async function fetchJSON(url){
  const r = await fetch(url);
  if (!r.ok) {
    let msg = `HTTP ${r.status}`;
    try {
      const j = await r.json();
      if (j && j.detail) msg = j.detail;
    } catch(e) {}
    throw new Error(msg);
  }
  return await r.json();
}

function setChartError(message){
  const el = document.getElementById("chartError");
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

  refreshTimer = setInterval(async () => {
    try {
      await loadMarket(true);
      await loadSelectedCoin(true);
    } catch (e) {
      console.error(e);
    }
  }, 30000);
}

function renderKPIs(global){
  const data = global?.data;
  if (!data) return;

  const totalCap = data.total_market_cap?.usd;
  const totalVol = data.total_volume?.usd;
  const btcDom = data.market_cap_percentage?.btc;
  const capCh = data.market_cap_change_percentage_24h_usd;

  const kpis = [
    { label: "Total Market Cap", value: "$" + fmtCompact(totalCap) },
    { label: "24h Volume", value: "$" + fmtCompact(totalVol) },
    { label: "BTC Dominance", value: (btcDom ?? 0).toFixed(2) + "%" },
    { label: "Market Mood (Cap 24h)", value: (capCh ?? 0).toFixed(2) + "%", cls: (capCh ?? 0) >= 0 ? "pos":"neg" },
  ];

  const el = document.getElementById("kpis");
  el.innerHTML = kpis.map(k => `
    <div class="col-6 col-lg-3">
      <div class="kpi">
        <div class="label">${k.label}</div>
        <div class="value ${k.cls || ""}">${k.value}</div>
      </div>
    </div>
  `).join("");
}

function renderWatchlist(){
  const watch = getWatch();
  const el = document.getElementById("watchlist");
  const items = marketData.filter(x => watch.has(x.id)).slice(0, 20);

  if (!items.length){
    el.innerHTML = `<div class="text-secondary small py-2">No coins starred yet.</div>`;
    return;
  }

  el.innerHTML = items.map(x => {
    const ch = x.price_change_percentage_24h;
    const cls = (ch ?? 0) >= 0 ? "pos" : "neg";
    return `
      <a href="#" class="list-group-item list-group-item-action bg-transparent text-light border-secondary d-flex justify-content-between align-items-center"
         data-id="${x.id}">
        <span>${x.name} <span class="text-secondary">(${x.symbol.toUpperCase()})</span></span>
        <span class="${cls}">${pct(ch)}</span>
      </a>
    `;
  }).join("");

  el.querySelectorAll("a[data-id]").forEach(a => {
    a.addEventListener("click", (e) => {
      e.preventDefault();
      selectCoin(a.dataset.id);
    });
  });
}

function starCell(coin){
  const watch = getWatch();
  const on = watch.has(coin.id);
  return `<span class="star ${on ? "on" : ""}" title="Add to watchlist" data-star="${coin.id}">${on ? "★" : "☆"}</span>`;
}

function renderTable(){
  const q = (document.getElementById("search").value || "").toLowerCase().trim();
  const filtered = marketData.filter(x =>
    x.name.toLowerCase().includes(q) || x.symbol.toLowerCase().includes(q)
  );

  filtered.sort((a,b) => {
    const av = a[sortKey];
    const bv = b[sortKey];
    if (av === bv) return 0;
    const dir = sortDir === "asc" ? 1 : -1;
    return (av > bv ? 1 : -1) * dir;
  });

  const tbody = document.getElementById("marketBody");
  tbody.innerHTML = filtered.map(c => {
    const ch = c.price_change_percentage_24h;
    const cls = (ch ?? 0) >= 0 ? "pos" : "neg";
    return `
      <tr data-id="${c.id}" class="coin-row">
        <td>${starCell(c)}</td>
        <td>
          <div class="d-flex align-items-center gap-2">
            <img src="${c.image}" width="18" height="18" alt="" />
            <div>
              <div class="fw-semibold">${c.name}</div>
              <div class="text-secondary small">${c.symbol.toUpperCase()}</div>
            </div>
          </div>
        </td>
        <td class="text-end">${fmtUsd(c.current_price)}</td>
        <td class="text-end ${cls}">${pct(ch)}</td>
        <td class="text-end">$${fmtCompact(c.market_cap)}</td>
        <td class="text-end">$${fmtCompact(c.total_volume)}</td>
      </tr>
    `;
  }).join("");

  tbody.querySelectorAll("tr.coin-row").forEach(tr => {
    tr.addEventListener("click", (e) => {
      if (e.target && e.target.dataset && e.target.dataset.star) return;
      selectCoin(tr.dataset.id);
    });
  });

  tbody.querySelectorAll("[data-star]").forEach(star => {
    star.addEventListener("click", (e) => {
      e.stopPropagation();
      const id = star.dataset.star;
      const watch = getWatch();
      if (watch.has(id)) watch.delete(id); else watch.add(id);
      setWatch(watch);
      renderTable();
      renderWatchlist();
    });
  });
}

async function loadMarket(isBackground=false){
  const limit = document.getElementById("limit").value;
  document.getElementById("limitLabel").textContent = limit;
  const res = await fetchJSON(`/api/market?limit=${limit}`);
  marketData = res.items || [];
  renderTable();
  renderWatchlist();
  if (!marketData.find(x => x.id === selectedCoinId)) selectedCoinId = marketData[0]?.id || "bitcoin";
  if (!isBackground) setLastUpdated(res.ts || Date.now());
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

async function loadSelectedCoin(isBackground=false){
  const coin = marketData.find(x => x.id === selectedCoinId) || marketData[0];
  if (!coin) return;

  setChartError("");
  document.getElementById("selectedTitle").textContent = `${coin.name} (${coin.symbol.toUpperCase()})`;
  document.getElementById("selectedPrice").textContent = fmtUsd(coin.current_price);
  const ch = coin.price_change_percentage_24h;
  const cls = (ch ?? 0) >= 0 ? "pos" : "neg";
  const chEl = document.getElementById("selected24h");
  chEl.textContent = pct(ch);
  chEl.className = cls;
  document.getElementById("selectedCap").textContent = "$" + fmtCompact(coin.market_cap);
  document.getElementById("coinPageLink").href = `/coin/${coin.id}`;

  try {
    const data = await fetchJSON(`/api/coin/${encodeURIComponent(coin.id)}?days=${selectedDays}`);
    const prices = data.chart?.prices || [];
    const labels = makeLabels(prices, selectedDays);
    const values = prices.map(p => p[1]);
    buildChart(document.getElementById("priceChart"), labels, values);
    if (!isBackground) setLastUpdated(data.ts || Date.now());
  } catch (e) {
    setChartError(`Chart failed to load (${e.message}). If LIVE is blocked, switch to DEMO.`);
  }
}

async function selectCoin(id){
  selectedCoinId = id;
  await loadSelectedCoin();
}

function wireUI(){
  fetchJSON("/api/global").then((g) => { renderKPIs(g); setLastUpdated(g.ts || Date.now()); }).catch(console.error);

  document.getElementById("search").addEventListener("input", () => renderTable());
  document.getElementById("limit").addEventListener("change", async () => {
    await loadMarket();
    await loadSelectedCoin();
  });

  document.querySelectorAll(".sortable").forEach(th => {
    th.addEventListener("click", () => {
      const key = th.dataset.key;
      if (sortKey === key){
        sortDir = sortDir === "asc" ? "desc" : "asc";
      } else {
        sortKey = key;
        sortDir = "desc";
      }
      renderTable();
    });
  });

  document.querySelectorAll(".range-btn").forEach(btn => {
    btn.addEventListener("click", async () => {
      document.querySelectorAll(".range-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      selectedDays = parseInt(btn.dataset.days, 10);
      await loadSelectedCoin();
    });
  });

  document.getElementById("clearWatchlist").addEventListener("click", () => {
    localStorage.removeItem(WATCH_KEY);
    renderTable();
    renderWatchlist();
  });

  document.getElementById("toggleMode").addEventListener("click", async () => {
    currentMode = await toggleMode();
    configureLiveRefresh();
    await loadMarket();
    await loadSelectedCoin();
  });
}

(async function main(){
  const m = await getMode();
  currentMode = m.mode;
  updateModeUI(currentMode);
  configureLiveRefresh();
  wireUI();
  await loadMarket();
  await loadSelectedCoin();
})().catch(err => {
  console.error(err);
  const tbody = document.getElementById("marketBody");
  if (tbody) tbody.innerHTML = `<tr><td colspan="6" class="text-warning">JS error: ${err.message}</td></tr>`;
});
