"use strict";

const $ = (s) => document.querySelector(s);
const $$ = (s) => Array.from(document.querySelectorAll(s));
const NS = "http://www.w3.org/2000/svg";

const state = {
  meta: {},           // name -> {display, description, gated, supplemental, default}
  groups: [],
  formats: [],
  selectedFormat: "report",
  seated: new Set(),
  ws: null,
  reviseSlug: null,
  resultSlug: null,
};

// Constellation geometry.
const CX = 400, CY = 252, OUTER_RX = 312, OUTER_RY = 188, INNER_RX = 210, INNER_RY = 124;
const PROCESS_SLOTS = {
  "strategist": -90, "red-team": 90, "fact-checker": 30,
  "humanizer": 150, "editor": 210, "presentation-designer": -30,
};
const constellation = { nodes: {}, svg: null };

// ─────────────────────────── init ───────────────────────────
async function init() {
  const [agentsRes, metaRes] = await Promise.all([
    fetch("/api/agents").then((r) => r.json()),
    fetch("/api/meta").then((r) => r.json()),
  ]);
  state.groups = agentsRes.groups;
  agentsRes.groups.forEach((g) => g.members.forEach((m) => (state.meta[m.name] = m)));
  agentsRes.process.forEach((p) => (state.meta[p.name] = { ...p, process: true }));
  state.formats = metaRes.formats;
  state.authOk = metaRes.auth_ok;
  state.authMsg = metaRes.auth_message;
  state.sources = metaRes.sources || [];
  state.defaultBudget = metaRes.default_budget ?? 80;

  buildFormats();
  buildAgentGroups();
  applyPreset("default");
  wireUI();
  buildHeroDots();
  setHeroStats(agentsRes);
  await loadHome();
  nav("home");
}

// Real, concrete numbers — counted up for a bit of life.
function setHeroStats(agentsRes) {
  const members = agentsRes.groups.flatMap((g) => g.members);
  const lenses = members.filter((m) => !m.supplemental).length;
  const total = members.length + agentsRes.process.length;
  countUp($("#stat-agents"), total);
  countUp($("#stat-lenses"), lenses);
}
function countUp(el, target) {
  if (!el) return;
  const dur = 900, t0 = performance.now();
  function frame(t) {
    const p = Math.min(1, (t - t0) / dur);
    const e = 1 - Math.pow(1 - p, 3);
    el.textContent = Math.round(target * e);
    if (p < 1) requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
}

// Glowing dots that orbit the hero rings.
function buildHeroDots() {
  const root = $("#hero-dots");
  if (!root) return;
  const rings = [
    { r: 240, dur: 90, rev: false, color: "#4187f7" },
    { r: 170, dur: 140, rev: true, color: "#a78bfa" },
    { r: 105, dur: 90, rev: false, color: "#34d3c0" },
  ];
  rings.forEach((ring, i) => {
    const g = svg("g", { style: `transform-origin:260px 260px;animation:spin ${ring.dur}s linear infinite${ring.rev ? " reverse" : ""};` });
    const dot = svg("circle", { cx: 260, cy: 260 - ring.r, r: 4, fill: ring.color,
      style: `filter:drop-shadow(0 0 8px ${ring.color});` });
    g.appendChild(dot);
    root.appendChild(g);
  });
}

// ─────────────────────────── navigation ───────────────────────────
function nav(view) {
  ["home", "configure", "run", "result", "library", "audit"].forEach((v) =>
    $("#view-" + v).classList.toggle("hidden", v !== view)
  );
  $$(".nav-link").forEach((l) => l.classList.toggle("active", l.dataset.nav === view));
  window.scrollTo(0, 0);
  if (view === "library") loadLibrary();
  if (view === "audit") loadAudit();
}

function wireUI() {
  $$("[data-nav]").forEach((b) => (b.onclick = () => nav(b.dataset.nav)));
  $("#brand-home").onclick = () => nav("home");
  $("#home-new").onclick = () => nav("configure");
  $$("[data-preset]").forEach((b) => (b.onclick = () => applyPreset(b.dataset.preset)));
  $("#launch-btn").onclick = launchNew;
  $("#cancel-btn").onclick = () => state.ws?.send(JSON.stringify({ type: "cancel" }));
  $("#result-new").onclick = () => nav("configure");
  $("#result-revise").onclick = () => openReviseModal(state.resultSlug);
  $("#result-deck").onclick = () => startRun({ type: "start", mode: "deck", slug: state.resultSlug });
  $("#revise-cancel").onclick = () => $("#revise-overlay").classList.add("hidden");
  $("#revise-go").onclick = submitRevise;
  $("#log-toggle").onclick = () => {
    const log = $("#activity-log");
    const hidden = log.classList.toggle("hidden");
    $("#log-toggle").textContent = hidden ? "Show" : "Hide";
  };

  if (!state.authOk) {
    const b = $("#auth-banner");
    b.textContent = "⚠ " + state.authMsg + "  —  run `claude login` in your terminal, then reload.";
    b.classList.remove("hidden");
    $("#launch-btn").disabled = true;
  }
  if (state.sources.length) {
    const note = $("#sources-note");
    note.textContent = `📎 ${state.sources.length} source file(s) staged — they'll be attached: ` +
      state.sources.map((s) => s.name).join(", ");
    note.classList.remove("hidden");
  }
  $("#f-budget").value = state.defaultBudget;
}

// ─────────────────────────── home / library ───────────────────────────
async function loadHome() {
  const data = await fetch("/api/home").then((r) => r.json());
  state.home = data;
  const rb = $("#resume-banner");
  if (data.interrupted) {
    rb.innerHTML = `<div class="rb-text">⟳ An interrupted run is waiting — <b>${escapeHtml(data.interrupted.title)}</b> (${escapeHtml(data.interrupted.where)}, ${escapeHtml(data.interrupted.age || "")}).</div>`;
    const btn = document.createElement("button");
    btn.className = "launch-btn";
    btn.style.padding = "10px 22px";
    btn.textContent = "Resume →";
    btn.onclick = () => startRun({ type: "start", mode: "resume", slug: data.interrupted.slug, auto_approve: false, budget: state.defaultBudget });
    rb.appendChild(btn);
    rb.classList.remove("hidden");
  } else rb.classList.add("hidden");
  renderArchives($("#home-archives"), data.archives.slice(0, 6));
}

async function loadLibrary() {
  const data = state.home || (await fetch("/api/home").then((r) => r.json()));
  renderArchives($("#library-grid"), data.archives);
}

function renderArchives(root, archives) {
  root.innerHTML = "";
  if (!archives.length) {
    root.innerHTML = `<p class="muted">No completed reports yet. Begin your first one.</p>`;
    return;
  }
  root.classList.add("stagger");
  archives.forEach((a, idx) => {
    const card = document.createElement("div");
    card.className = "archive-card";
    card.style.animationDelay = (idx * 0.05).toFixed(2) + "s";
    const dls = a.downloads.map((d) => `<a class="ac-btn" href="${d.url}">⤓ ${escapeHtml(d.label)}</a>`).join("");
    const revBadge = a.revisions > 0 ? `<span class="ac-badge">v${a.revisions}</span>` : "";
    card.innerHTML = `
      <div class="ac-date">${escapeHtml(a.date)} · ${escapeHtml(a.format)}</div>
      <div class="ac-title">${escapeHtml(a.title)}${revBadge}</div>
      <div class="ac-actions">
        <button class="ac-btn" data-read="${a.slug}">Read</button>
        ${dls}
        <button class="ac-btn" data-revise="${a.slug}">Revise</button>
        ${a.has_deck ? "" : `<button class="ac-btn" data-deck="${a.slug}">Build deck</button>`}
      </div>`;
    card.querySelector("[data-read]").onclick = () => openReport(a.slug, a.title);
    card.querySelector("[data-revise]").onclick = () => openReviseModal(a.slug);
    const deckBtn = card.querySelector("[data-deck]");
    if (deckBtn) deckBtn.onclick = () => startRun({ type: "start", mode: "deck", slug: a.slug });
    root.appendChild(card);
  });
}

async function loadAudit() {
  $("#audit-body").innerHTML = `<p class="muted">Scanning archived runs…</p>`;
  const data = await fetch("/api/audit").then((r) => r.json());
  $("#audit-body").innerHTML = renderMarkdown(data.markdown);
}

async function openReport(slug, title) {
  state.resultSlug = slug;
  const data = await fetch(`/api/report/${slug}`).then((r) => r.json());
  $("#result-title").textContent = title;
  $("#result-cost").textContent = "Archived report";
  $("#result-body").innerHTML = renderMarkdown(data.markdown || "");
  renderDownloads(data.downloads);
  nav("result");
}

// ─────────────────────────── configure form ───────────────────────────
function buildFormats() {
  const row = $("#format-pills");
  row.innerHTML = "";
  state.formats.forEach((f, i) => {
    const pill = document.createElement("button");
    pill.className = "format-pill" + (i === 0 ? " active" : "");
    pill.textContent = f.label;
    pill.onclick = () => {
      $$(".format-pill").forEach((p) => p.classList.remove("active"));
      pill.classList.add("active");
      state.selectedFormat = f.key;
    };
    row.appendChild(pill);
  });
  state.selectedFormat = state.formats[0]?.key || "report";
}

function buildAgentGroups() {
  const root = $("#agent-groups");
  root.innerHTML = "";
  state.groups.forEach((g) => {
    const label = document.createElement("div");
    label.className = "agent-group-label";
    label.textContent = g.label;
    root.appendChild(label);
    const grid = document.createElement("div");
    grid.className = "agent-grid stagger";
    g.members.forEach((m, i) => {
      const chip = agentChip(m);
      chip.style.animationDelay = (i * 0.03).toFixed(2) + "s";
      grid.appendChild(chip);
    });
    root.appendChild(grid);
  });
}

function agentChip(m) {
  const chip = document.createElement("div");
  chip.className = "agent-chip";
  chip.dataset.name = m.name;
  chip.innerHTML = `<div class="agent-check">✓</div><div>
    <div class="agent-name">${escapeHtml(m.display)}${m.gated ? '<span class="agent-gated">needs OpenAI key</span>' : ""}</div>
    <div class="agent-desc">${escapeHtml(m.description)}</div></div>`;
  chip.onclick = () => {
    if (state.seated.has(m.name)) { state.seated.delete(m.name); chip.classList.remove("on"); }
    else { state.seated.add(m.name); chip.classList.add("on"); }
    updateCount();
  };
  return chip;
}

function setSeated(names) {
  state.seated = new Set(names);
  $$(".agent-chip").forEach((c) => c.classList.toggle("on", state.seated.has(c.dataset.name)));
  updateCount();
}
function applyPreset(which) {
  const all = Object.values(state.meta).filter((m) => !m.process);
  if (which === "none") return setSeated([]);
  if (which === "default") return setSeated(all.filter((m) => m.default).map((m) => m.name));
  if (which === "all") return setSeated(all.filter((m) => !m.gated && !m.supplemental).map((m) => m.name));
}
function updateCount() {
  $("#seated-count").textContent = `${state.seated.size} agent${state.seated.size === 1 ? "" : "s"} seated`;
}

// ─────────────────────────── launch ───────────────────────────
function launchNew() {
  const thesis = $("#f-thesis").value.trim();
  if (!thesis) { $("#f-thesis").focus(); $("#f-thesis").style.borderColor = "var(--red)"; return; }
  if (state.seated.size === 0) { alert("Seat at least one research agent."); return; }
  startRun({
    type: "start", mode: "new",
    spec: {
      title: $("#f-title").value.trim() || thesis.slice(0, 60),
      thesis, scope: linesOf($("#f-scope").value), avoid: linesOf($("#f-avoid").value),
      output_format: state.selectedFormat, agents: Array.from(state.seated),
      want_pptx: $("#f-pptx").checked, use_sources: true,
    },
    auto_approve: !$("#f-review").checked,
    budget: parseFloat($("#f-budget").value) || null,
  });
}

function startRun(payload) {
  nav("run");
  $("#cost-pill").classList.remove("hidden");
  $("#cost-pill").textContent = "$0.00";
  $("#activity-log").innerHTML = "";
  $("#run-title").textContent = payload.spec?.title || payload.slug || "Council run";
  buildStageRail();
  resetConstellation(payload.spec?.title || payload.slug || "");
  const proto = location.protocol === "https:" ? "wss" : "ws";
  const ws = new WebSocket(`${proto}://${location.host}/ws`);
  state.ws = ws;
  ws.onopen = () => ws.send(JSON.stringify(payload));
  ws.onmessage = (ev) => handleEvent(JSON.parse(ev.data));
  ws.onclose = () => log("Connection closed.", "warn");
}

// ─────────────────────────── stage rail ───────────────────────────
const STAGES = [
  { n: 1, label: "Research" }, { n: 2, label: "Synthesis & debate" },
  { n: 3, label: "Edit & verify" }, { n: 4, label: "Produce" },
];
function buildStageRail() {
  const rail = $("#stage-rail");
  rail.innerHTML = "";
  STAGES.forEach((s) => {
    const node = document.createElement("div");
    node.className = "stage-node";
    node.dataset.stage = s.n;
    node.innerHTML = `<div class="stage-dot"></div><div class="stage-label">${s.label}</div>`;
    rail.appendChild(node);
  });
}
function setStage(n) {
  $$(".stage-node").forEach((node) => {
    const sn = parseInt(node.dataset.stage);
    node.classList.toggle("active", sn === n);
    node.classList.toggle("done", sn < n);
  });
}

// ─────────────────────────── constellation ───────────────────────────
function svg(tag, attrs = {}) {
  const el = document.createElementNS(NS, tag);
  for (const [k, v] of Object.entries(attrs)) el.setAttribute(k, v);
  return el;
}
function initials(display) {
  const words = display.replace(/[()]/g, "").split(/\s+/).filter(Boolean);
  if (words.length === 1) return words[0].slice(0, 3).toUpperCase();
  return words.slice(0, 3).map((w) => w[0]).join("").toUpperCase();
}
function resetConstellation(title) {
  const root = $("#constellation");
  root.innerHTML = "";
  constellation.nodes = {};
  constellation.svg = root;

  const defs = svg("defs");
  const grad = svg("radialGradient", { id: "coreGrad", cx: "50%", cy: "42%", r: "62%" });
  grad.appendChild(svg("stop", { offset: "0%", "stop-color": "#6ea8ff" }));
  grad.appendChild(svg("stop", { offset: "55%", "stop-color": "#3b82f6" }));
  grad.appendChild(svg("stop", { offset: "100%", "stop-color": "#11305c" }));
  defs.appendChild(grad);
  root.appendChild(defs);

  // Starfield backdrop.
  const stars = svg("g");
  for (let i = 0; i < 46; i++) {
    const x = Math.random() * 800, y = Math.random() * 560;
    const dc = Math.hypot(x - CX, y - CY);
    if (dc < 80) continue; // keep clear of the core
    const s = svg("circle", { class: "star", cx: x.toFixed(0), cy: y.toFixed(0),
      r: (Math.random() * 1.3 + 0.4).toFixed(1),
      opacity: (Math.random() * 0.4 + 0.15).toFixed(2) });
    s.style.animation = `twinkle ${(Math.random() * 4 + 3).toFixed(1)}s ease-in-out ${(Math.random() * 4).toFixed(1)}s infinite`;
    stars.appendChild(s);
  }
  root.appendChild(stars);

  // Decorative rotating rings.
  root.appendChild(svg("circle", { class: "deco-ring r1", cx: CX, cy: CY, r: OUTER_RX - 6 }));
  root.appendChild(svg("circle", { class: "deco-ring r2", cx: CX, cy: CY, r: INNER_RX - 6 }));

  root.appendChild(svg("g", { id: "beam-layer" }));
  root.appendChild(svg("g", { id: "node-layer" }));

  // Core orb.
  const core = svg("g");
  core.appendChild(svg("circle", { class: "core-ring spin", cx: CX, cy: CY, r: 62 }));
  core.appendChild(svg("circle", { class: "core-orb", cx: CX, cy: CY, r: 46 }));
  const t1 = svg("text", { class: "core-label", x: CX, y: CY - 2 });
  t1.textContent = "THESIS";
  const t2 = svg("text", { class: "core-sub", x: CX, y: CY + 16 });
  t2.textContent = (title || "").slice(0, 16);
  core.appendChild(t1); core.appendChild(t2);
  root.appendChild(core);
}

// A glowing packet that flies from a node to the core when its work lands.
function flyEvidence(node) {
  const root = constellation.svg;
  if (!root) return;
  const dot = svg("circle", { class: "evidence", r: 4, cx: node.x, cy: node.y });
  root.appendChild(dot);
  const t0 = performance.now(), dur = 750;
  function frame(t) {
    const p = Math.min(1, (t - t0) / dur);
    const e = 1 - Math.pow(1 - p, 3); // ease-out cubic
    dot.setAttribute("cx", node.x + (CX - node.x) * e);
    dot.setAttribute("cy", node.y + (CY - node.y) * e);
    dot.setAttribute("opacity", (1 - p * 0.7).toFixed(2));
    dot.setAttribute("r", (4 - p * 2).toFixed(1));
    if (p < 1) requestAnimationFrame(frame);
    else dot.remove();
  }
  requestAnimationFrame(frame);
}

function placeNode(name) {
  if (constellation.nodes[name]) return constellation.nodes[name];
  const meta = state.meta[name] || { display: name };
  const isProc = name in PROCESS_SLOTS;
  let x, y;
  if (isProc) {
    const ang = (PROCESS_SLOTS[name] * Math.PI) / 180;
    x = CX + INNER_RX * Math.cos(ang);
    y = CY + INNER_RY * Math.sin(ang);
  } else {
    // Distribute research nodes on the outer ring by their order of placement.
    const researchNames = (state._researchOrder || []);
    const idx = researchNames.indexOf(name);
    const total = researchNames.length || 1;
    const ang = (idx / total) * 2 * Math.PI - Math.PI / 2;
    x = CX + OUTER_RX * Math.cos(ang);
    y = CY + OUTER_RY * Math.sin(ang);
  }

  const beam = svg("line", { class: "beam", x1: CX, y1: CY, x2: x, y2: y });
  $("#beam-layer").appendChild(beam);

  const g = svg("g", { class: "cnode queued appearing", transform: `translate(${x},${y})` });
  setTimeout(() => g.classList.remove("appearing"), 600);
  g.appendChild(svg("circle", { class: "pulse", r: 22, cx: 0, cy: 0 }));
  g.appendChild(svg("circle", { class: "ring", r: 21, cx: 0, cy: 0 }));
  const gl = svg("text", { class: "glyph", x: 0, y: 0 });
  gl.textContent = initials(meta.display || name);
  g.appendChild(gl);
  const lbl = svg("text", { class: "clabel", x: 0, y: 34 });
  lbl.textContent = (meta.display || name).slice(0, 16);
  g.appendChild(lbl);
  const cost = svg("text", { class: "ccost", x: 0, y: 47 });
  g.appendChild(cost);
  g.addEventListener("mouseenter", (e) => showTip(e, meta));
  g.addEventListener("mouseleave", hideTip);
  $("#node-layer").appendChild(g);

  const node = { g, beam, cost, x, y };
  constellation.nodes[name] = node;
  return node;
}

function buildConstellation(agentNames) {
  state._researchOrder = agentNames.filter((n) => !(n in PROCESS_SLOTS));
  state._researchOrder.forEach((n) => placeNode(n));
}

function nodeState(name, cls) {
  const node = placeNode(name);
  node.g.classList.remove("queued", "running", "done");
  node.g.classList.add(cls);
  if (cls === "running") node.beam.classList.add("active");
  if (cls === "done") { node.beam.classList.remove("active"); node.beam.classList.add("delivered"); }
}

function showTip(e, meta) {
  const tip = $("#node-tooltip");
  tip.innerHTML = `<div class="nt-name">${escapeHtml(meta.display || "")}</div><div class="nt-desc">${escapeHtml(meta.description || "")}</div>`;
  const wrap = $(".constellation-wrap").getBoundingClientRect();
  tip.style.left = (e.clientX - wrap.left + 14) + "px";
  tip.style.top = (e.clientY - wrap.top + 10) + "px";
  tip.classList.remove("hidden");
}
function hideTip() { $("#node-tooltip").classList.add("hidden"); }

// ─────────────────────────── event handling ───────────────────────────
function handleEvent(e) {
  switch (e.type) {
    case "run_start":
      buildConstellation(e.agents || []);
      log("Council convened: " + e.title, "ok");
      break;
    case "stage_start":
      setStage(e.stage);
      $("#run-stage").textContent = `Stage ${e.stage} · ${e.label}`;
      log(`▸ Stage ${e.stage}: ${e.label}`);
      break;
    case "agent_start":
      nodeState(e.agent, "running");
      log(`▶ ${e.display || e.agent} started`);
      break;
    case "agent_tool":
      if (e.target) log(`  ${e.tool}: ${shortPath(e.target)}`);
      break;
    case "agent_done": {
      const node = constellation.nodes[e.agent];
      if (node) { node.cost.textContent = "$" + e.cost.toFixed(2); flyEvidence(node); }
      nodeState(e.agent, "done");
      const pill = $("#cost-pill");
      pill.textContent = "$" + (e.total || 0).toFixed(2);
      pill.animate(
        [{ transform: "scale(1)" }, { transform: "scale(1.12)" }, { transform: "scale(1)" }],
        { duration: 360, easing: "cubic-bezier(0.16,1,0.3,1)" }
      );
      log(`✓ ${state.meta[e.agent]?.display || e.agent} — $${e.cost.toFixed(2)}`, "ok");
      break;
    }
    case "checkpoint": showCheckpoint(e); break;
    case "run_complete": showResult(e); break;
    case "run_error":
      log("Error: " + e.message, "err");
      alert("The run hit an error:\n\n" + e.message + "\n\nCompleted work is saved — you can resume from Home.");
      loadHome();
      break;
    case "run_stopped": log("Run stopped.", "warn"); break;
    case "stream_end": state.ws?.close(); break;
  }
}

function log(text, cls = "") {
  const line = document.createElement("div");
  line.className = "log-line " + cls;
  const t = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
  line.innerHTML = `<span class="lt">${t}</span>${escapeHtml(text)}`;
  const logEl = $("#activity-log");
  logEl.appendChild(line);
  logEl.scrollTop = logEl.scrollHeight;
}

// ─────────────────────────── checkpoint ───────────────────────────
function showCheckpoint(e) {
  state.currentCheckpoint = e;
  $("#cp-title").textContent = e.title;
  $("#cp-subtitle").textContent = e.subtitle;
  const tabs = $("#cp-tabs"), content = $("#cp-content");
  tabs.innerHTML = "";
  e.documents.forEach((doc, i) => {
    const tab = document.createElement("div");
    tab.className = "cp-tab" + (i === 0 ? " active" : "");
    tab.textContent = doc.name;
    tab.onclick = () => {
      $$(".cp-tab").forEach((t) => t.classList.remove("active"));
      tab.classList.add("active");
      content.innerHTML = renderMarkdown(doc.content);
      content.scrollTop = 0;
    };
    tabs.appendChild(tab);
  });
  content.innerHTML = renderMarkdown(e.documents[0]?.content || "");
  const notes = $("#cp-notes");
  notes.classList.add("hidden"); notes.value = "";
  const actions = $("#cp-actions");
  actions.innerHTML = "";
  const defs = {
    continue: { label: "Approve → continue", cls: "primary" },
    approve: { label: "Approve → produce documents", cls: "primary" },
    redo: { label: "Redo with notes", cls: "warn" },
    abort: { label: "Stop the run", cls: "ghost" },
  };
  e.actions.forEach((a) => {
    const btn = document.createElement("button");
    btn.className = "cp-btn " + (defs[a]?.cls || "ghost");
    btn.textContent = defs[a]?.label || a;
    btn.onclick = () => {
      if (a === "redo" && notes.classList.contains("hidden")) {
        notes.classList.remove("hidden"); notes.focus(); btn.textContent = "Submit redo"; return;
      }
      state.ws?.send(JSON.stringify({ type: "checkpoint", id: e.id, action: a, notes: notes.value.trim() }));
      $("#checkpoint-overlay").classList.add("hidden");
      log(a === "redo" ? "Redo requested." : a === "abort" ? "Aborted." : "Checkpoint approved.",
          a === "abort" ? "warn" : "ok");
    };
    actions.appendChild(btn);
  });
  $("#checkpoint-overlay").classList.remove("hidden");
}

// ─────────────────────────── revise ───────────────────────────
function openReviseModal(slug) {
  state.reviseSlug = slug;
  $("#revise-target").textContent = slug;
  $("#revise-feedback").value = "";
  $("#revise-overlay").classList.remove("hidden");
}
function submitRevise() {
  const feedback = $("#revise-feedback").value.trim();
  if (!feedback) { $("#revise-feedback").focus(); return; }
  $("#revise-overlay").classList.add("hidden");
  startRun({ type: "start", mode: "revise", slug: state.reviseSlug, feedback, auto_approve: false });
}

// ─────────────────────────── result ───────────────────────────
async function showResult(e) {
  setStage(5);
  state.resultSlug = e.slug;
  $("#result-title").textContent = e.title;
  $("#result-cost").textContent = `Total cost $${(e.total || 0).toFixed(2)} · archived to runs/`;
  try {
    const data = await fetch(`/api/report/${e.slug}`).then((r) => r.json());
    $("#result-body").innerHTML = renderMarkdown(data.markdown || "");
    renderDownloads(data.downloads);
  } catch (_) {
    $("#result-body").textContent = "Report saved to runs/.";
  }
  await loadHome();
  nav("result");
}
function renderDownloads(downloads) {
  const dl = $("#result-downloads");
  dl.innerHTML = "";
  (downloads || []).forEach((d) => {
    const a = document.createElement("a");
    a.className = "dl-btn"; a.href = d.url; a.textContent = "⤓ " + d.label;
    dl.appendChild(a);
  });
}

// ─────────────────────────── helpers ───────────────────────────
function linesOf(t) { return t.split("\n").map((s) => s.replace(/^[-*•]\s*/, "").trim()).filter(Boolean); }
function shortPath(p) { const x = String(p).split("/"); return x.length > 2 ? ".../" + x.slice(-2).join("/") : p; }
function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}
function renderMarkdown(md) {
  if (!md) return "";
  const lines = md.replace(/<!--[\s\S]*?-->/g, "").split("\n");
  let html = "", inList = false, inQuote = false;
  const inline = (t) => escapeHtml(t)
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/(^|[^*])\*([^*]+)\*/g, "$1<em>$2</em>")
    .replace(/`([^`]+)`/g, "<code>$1</code>");
  const closeList = () => { if (inList) { html += "</ul>"; inList = false; } };
  const closeQuote = () => { if (inQuote) { html += "</blockquote>"; inQuote = false; } };
  for (const raw of lines) {
    const line = raw.replace(/\s+$/, "");
    let m;
    if ((m = line.match(/^(#{1,4})\s+(.*)$/))) { closeList(); closeQuote(); html += `<h${m[1].length}>${inline(m[2])}</h${m[1].length}>`; }
    else if ((m = line.match(/^[-*]\s+(.*)$/))) { closeQuote(); if (!inList) { html += "<ul>"; inList = true; } html += `<li>${inline(m[1])}</li>`; }
    else if ((m = line.match(/^>\s?(.*)$/))) { closeList(); if (!inQuote) { html += "<blockquote>"; inQuote = true; } html += inline(m[1]) + " "; }
    else if (line.trim() === "") { closeList(); closeQuote(); }
    else { closeList(); closeQuote(); html += `<p>${inline(line)}</p>`; }
  }
  closeList(); closeQuote();
  return html;
}

init();
