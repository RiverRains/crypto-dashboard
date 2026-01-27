async function getMode(){
  const r = await fetch("/api/mode");
  return await r.json();
}

function updateModeUI(mode){
  const badge = document.getElementById("modeBadge");
  const btn = document.getElementById("toggleMode");
  if (!badge || !btn) return;

  badge.textContent = mode === "live" ? "LIVE" : "DEMO";
  badge.className = "badge " + (mode === "live" ? "text-bg-success" : "text-bg-secondary");
  btn.textContent = mode === "live" ? "Switch to DEMO" : "Switch to LIVE";
}

async function toggleMode(){
  const current = await getMode();
  const next = current.mode === "live" ? "demo" : "live";
  const r = await fetch(`/api/mode?set=${next}`);
  const data = await r.json();
  updateModeUI(data.mode);
  return data.mode;
}
