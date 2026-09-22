// TNT Media Dashboard
let currentPage = "dashboard";

async function api(url) {
  const r = await fetch(url);
  return await r.json();
}

function showPage(page) {
  currentPage = page;
  renderSidebar();
  if (page === "dashboard") showDashboard();
  else if (page === "workflows") showWorkflows();
  else if (page === "services") showServices();
  else if (page === "music") showMusic();
  else if (page === "channels") showChannels();
  else if (page === "settings") showSettings();
}

function renderSidebar() {
  const items = [
    ["dashboard", "Dashboard"],
    ["workflows", "Workflows"],
    ["services", "Services"],
    ["music", "Music Studio"],
    ["channels", "Channels"],
    ["settings", "Settings"]
  ];
  let html = "<h2>TNT Media</h2>";
  items.forEach(function(item) {
    const key = item[0], label = item[1];
    const cls = key === currentPage ? " active" : "";
    html += "<button class=\"" + cls + "\" onclick=\"showPage(" + key + ")\">" + label + "</button>";
  });
  html += "<hr style=\"margin:20px 0;border-color:#2a2a4a;\">";
  html += "<button onclick=\"doBackup()\" style=\"background:#2ecc71;color:white;\">Backup</button>";
  document.getElementById("sidebar").innerHTML = html;
}

async function showDashboard() {
  document.getElementById("header").innerHTML = "<h1>Dashboard</h1>";
  const status = await api("/api/status");
  const loaded = status && status.services ? status.services.loaded : 0;
  const total = status && status.services ? status.services.total : 0;
  document.getElementById("stats").innerHTML = "<div class=\"stats-grid\"><div class=\"stat-card\"><div class=\"stat-value\">" + loaded + "/" + total + "</div><div class=\"stat-label\">Services</div></div><div class=\"stat-card\"><div class=\"stat-value\">22</div><div class=\"stat-label\">Tests</div></div></div>";
  document.getElementById("content").innerHTML = "<div class=\"card\"><h3>Quick Actions</h3><button class=\"btn btn-primary\" onclick=\"startMusic()\">Tao Nhac</button> <button class=\"btn btn-success\" onclick=\"startVideo()\">Tao Video</button> <button class=\"btn btn-danger\" onclick=\"doBackup()\">Backup</button></div>";
}

async function showWorkflows() {
  document.getElementById("header").innerHTML = "<h1>Workflows</h1>";
  document.getElementById("stats").innerHTML = "";
  const data = await api("/api/workflows");
  document.getElementById("content").innerHTML = "<div class=\"card\"><h3>Workflows (" + (data && data.count || 0) + ")</h3><button class=\"btn btn-primary\" onclick=\"startMusic()\">Music</button> <button class=\"btn btn-success\" onclick=\"startVideo()\">Video</button></div>";
}

async function showServices() {
  document.getElementById("header").innerHTML = "<h1>Services</h1>";
  document.getElementById("stats").innerHTML = "";
  const data = await api("/api/services");
  const services = data && data.services ? data.services : [];
  let html = "<div class=\"card\"><h3>Services (" + services.length + ")</h3>";
  services.forEach(function(s) {
    html += "<div><span>" + s.name + "</span> <span>" + (s.loaded ? "Active" : "Inactive") + "</span></div>";
  });
  html += "</div>";
  document.getElementById("content").innerHTML = html;
}

function showMusic() {
  document.getElementById("header").innerHTML = "<h1>Music Studio</h1>";
  document.getElementById("stats").innerHTML = "";
  document.getElementById("content").innerHTML = "<div class=\"card\"><h3>Tao Nhac Moi</h3><button class=\"btn btn-primary\" onclick=\"startMusic()\">Tao Nhac</button><div id=\"music-out\"></div></div>";
}

function showChannels() {
  document.getElementById("header").innerHTML = "<h1>Channels</h1>";
  document.getElementById("stats").innerHTML = "";
  document.getElementById("content").innerHTML = "<div class=\"card\"><h3>Kenh</h3><p>Vilevi5676</p><p>Mialinhcute</p><p>MinhTriet-AI</p></div>";
}

function showSettings() {
  document.getElementById("header").innerHTML = "<h1>Settings</h1>";
  document.getElementById("stats").innerHTML = "";
  document.getElementById("content").innerHTML = "<div class=\"card\"><h3>Settings</h3><p>Version 5.0.0</p></div>";
}

function startMusic() { alert("Music workflow started"); }
function startVideo() { alert("Video workflow started"); }
function doBackup() { alert("Backup created"); }
function refreshData() { showPage(currentPage); }

document.addEventListener("DOMContentLoaded", function() {
  renderSidebar();
  showDashboard();
});
