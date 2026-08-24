"use strict";

const $ = (s) => document.querySelector(s);
const $$ = (s) => Array.from(document.querySelectorAll(s));
const NS = "http://www.w3.org/2000/svg";

function tabClientId() {
  const key = "council-client-id";
  try {
    const existing = sessionStorage.getItem(key);
    if (/^[A-Za-z0-9_-]{16,128}$/.test(existing || "")) return existing;
    const generated = crypto.randomUUID();
    sessionStorage.setItem(key, generated);
    return generated;
  } catch (_) {
    // The ID separates browser tabs; the server token remains the credential.
    return `tab_${Date.now()}_${Math.random().toString(36).slice(2)}_${Math.random().toString(36).slice(2)}`;
  }
}

const state = {
  meta: {}, groups: [], formats: [], selectedFormat: "article",
  processAgents: [], agentCatalogFilter: "all", promptText: "", promptRequestId: 0,
  agentProfiles: new Map(), agentProfileRequestId: 0,
  promptDraft: null, promptDraftReview: [], promptAssistRequestId: 0,
  libraryEditArchive: null, libraryDeletePlan: null, libraryMutationRequestId: 0,
  libraryEditSaving: false, libraryDeleteCommitting: false, libraryToastTimer: null,
  seated: new Set(), ws: null, reviseSlug: null, resultSlug: null,
  argumentSeated: new Set(),
  sourceUploads: { report: [], scope: [], argument: [] },
  sourceUploading: { report: 0, scope: 0, argument: 0 },
  resultReviseSlug: null, resultMode: "report", step: 1, home: null,
  runBilling: "provider_subscriptions",
  promptCoachOk: false, promptCoachMsg: "", promptCoachModel: "gpt-5.6-sol",
  councilModels: [], defaultCouncilModel: "claude-fable-5",
  sessionToken: null, clientId: tabClientId(),
};

const SOURCE_UI = {
  report: { dropzone: "#report-dropzone", input: "#f-files", list: "#report-files" },
  scope: { dropzone: "#scope-dropzone", input: "#s-files", list: "#scope-files" },
  argument: { dropzone: "#argument-dropzone", input: "#a-files", list: "#argument-files" },
};

const CX = 400, CY = 252, OUTER_RX = 312, OUTER_RY = 188, INNER_RX = 210, INNER_RY = 124;
const PROCESS_SLOTS = {
  "airport-context-builder": -175, "evidence-curator": -145,
  "creative-director": -115, "strategist": -85,
  "evidence-prosecutor": -55, "airport-executive-reviewer": -20,
  "editor": 20, "humanizer": 55, "fact-checker": 90,
  "art-director": 125, "presentation-designer": 155, "red-team": 180,
};
const STAGE_FILL = { 1: 15, 2: 45, 3: 75, 4: 92 };
// Let the server's 90-second subscription-model timeout return a terminal
// response before the browser gives up, so a completed call is not retried.
const PROMPT_COACH_TIMEOUT_MS = 105_000;
const PROMPT_FIELD_DEFINITIONS = [
  { key: "title", label: "Title", selector: "#f-title", kind: "scalar" },
  { key: "thesis", label: "Thesis", selector: "#f-thesis", kind: "scalar" },
  { key: "operator_context", label: "Operator context", selector: "#f-operator-context", kind: "scalar" },
  { key: "decision_required", label: "Decision required", selector: "#f-decision", kind: "scalar", decision: true },
  { key: "decision_owner", label: "Decision owner", selector: "#f-owner", kind: "scalar", decision: true },
  { key: "time_horizon", label: "Time horizon", selector: "#f-horizon", kind: "scalar", decision: true },
  { key: "approval_path", label: "Approval path", selector: "#f-approval", kind: "scalar", decision: true },
  { key: "success_measure", label: "Success measure", selector: "#f-success-measure", kind: "scalar", decision: true },
  { key: "scope", label: "Lines of inquiry", selector: "#f-scope", kind: "list" },
  { key: "avoid", label: "Avoid", selector: "#f-avoid", kind: "list" },
];
const ARGUMENT_FAST_PRESET = [
  "contrarian", "quantitative-analyst", "airport-ceo", "airport-coo",
];
const constellation = { nodes: {}, svg: null };

// ─────────── init ───────────
async function init() {
  const [agentsRes, metaRes] = await Promise.all([
    fetch("/api/agents").then((r) => r.json()),
    fetch("/api/meta").then((r) => r.json()),
  ]);
  state.groups = agentsRes.groups;
  state.processAgents = agentsRes.process || [];
  agentsRes.groups.forEach((g) => g.members.forEach((m) => (state.meta[m.name] = m)));
  agentsRes.process.forEach((p) => (state.meta[p.name] = { ...p, process: true }));
  state.formats = metaRes.formats;
  state.authOk = metaRes.auth_ok; state.authMsg = metaRes.auth_message;
  state.codexOk = Boolean(metaRes.codex_subscription_ok);
  state.codexMsg = metaRes.codex_subscription_message || "Codex is not signed in with ChatGPT.";
  state.councilModels = metaRes.council_models || [];
  state.defaultCouncilModel = metaRes.default_council_model || "claude-fable-5";
  state.promptCoachOk = Boolean(metaRes.prompt_coach_ok);
  state.promptCoachMsg = metaRes.prompt_coach_message || "Prompt Coach is unavailable.";
  state.promptCoachModel = metaRes.prompt_coach_model || "gpt-5.6-sol";
  state.defaultBudget = metaRes.default_budget ?? 80;
  state.modelsCfg = metaRes.models || {};
  state.activeRun = Boolean(metaRes.active_run);
  state.sessionToken = metaRes.session_token || null;

  buildFormats(); buildAgentGroups(); buildArgumentAgentGroups(); buildAgentCatalog();
  applyPreset("default"); applyArgumentPreset("fast");
  wireUI(); buildHeroDots(); setHeroStats(agentsRes);
  await loadHome();
  if (state.activeRun) startRun({ type: "attach" });
  else nav("home");
}

function modelShort(id) {
  if (String(id || "") === "opus") return "Opus (latest)";
  return String(id || "").replace("claude-", "").replace("opus-5-0", "Opus (latest)")
    .replace("fable-5", "Fable 5").replace("sonnet-4-6", "Sonnet 4.6")
    .replace("o3-deep-research", "o3 DR").replace("o4-mini-deep-research", "o4-mini DR")
    .replace("gpt-5.6-sol", "GPT-5.6 Sol");
}
function setHeroStats(agentsRes) {
  const members = agentsRes.groups.flatMap((g) => g.members);
  const lenses = members.filter((m) => !m.supplemental).length;
  const outside = members.filter((m) => m.supplemental).length;
  const total = members.length + agentsRes.process.length;
  countUp($("#stat-agents"), total); countUp($("#stat-lenses"), lenses);
  countUp($("#stat-outside"), outside); countUp($("#stat-process"), agentsRes.process.length);
  $("#ss-agents").textContent = total;
  $("#ss-models").textContent = "Fable 5 / GPT-5.6 · selectable";
}

function selectedCouncilModel() {
  return document.querySelector('input[name="f-council-model"]:checked')?.value
    || state.defaultCouncilModel
    || "claude-fable-5";
}
function councilModelMeta(modelId = selectedCouncilModel()) {
  return state.councilModels.find((item) => item.id === modelId) || {
    id: modelId,
    label: modelShort(modelId),
    provider: modelId === "gpt-5.6-sol" ? "openai" : "anthropic",
  };
}
function councilModelReady(modelId = selectedCouncilModel()) {
  return councilModelMeta(modelId).provider === "openai" ? state.codexOk : state.authOk;
}
function planLabel(billing = state.runBilling) {
  if (billing === "chatgpt_subscription") return "ChatGPT plan";
  if (billing === "claude_subscription") return "Claude plan";
  if (billing === "provider_subscriptions") return "Subscription plans";
  return "";
}
function updateCouncilModelAvailability() {
  $$('[data-model-status]').forEach((status) => {
    const model = councilModelMeta(status.dataset.modelStatus);
    const ready = model.provider === "openai" ? state.codexOk : state.authOk;
    status.textContent = ready ? "Ready" : (model.provider === "openai" ? "ChatGPT login needed" : "Claude unavailable");
    status.classList.toggle("unavailable", !ready);
  });
  const banner = $("#auth-banner");
  const selected = councilModelMeta();
  const ready = councilModelReady();
  banner.classList.toggle("hidden", ready);
  if (!ready) {
    banner.textContent = selected.provider === "openai"
      ? "GPT-5.6 Sol uses your ChatGPT subscription. Run `codex login`, restart the Council, and reload."
      : state.authMsg;
  }
  if (state.step === 3) {
    $("#wiz-next").disabled = !ready || state.sourceUploading.report > 0;
    buildReview();
  }
  updateCount();
}
function countUp(el, target) {
  if (!el) return; const dur = 900, t0 = performance.now();
  (function f(t) { const p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3);
    el.textContent = Math.round(target * e); if (p < 1) requestAnimationFrame(f); })(t0);
}
function buildHeroDots() {
  const root = $("#hero-dots"); if (!root) return;
  [{ r: 240, d: 120, rev: 0, c: "#4f46e5" }, { r: 170, d: 180, rev: 1, c: "#aab3c2" }, { r: 105, d: 120, rev: 0, c: "#aab3c2" }].forEach((ring) => {
    const g = svg("g", { style: `transform-origin:260px 260px;animation:spin ${ring.d}s linear infinite${ring.rev ? " reverse" : ""};` });
    g.appendChild(svg("circle", { cx: 260, cy: 260 - ring.r, r: 3, fill: ring.c }));
    root.appendChild(g);
  });
}

// ─────────── navigation ───────────
function nav(view) {
  // Drive off the DOM rather than a hardcoded list: a view present in the
  // markup but missing here (or vice versa) must never blank the whole app.
  const views = $$(".workspace > .view");
  if (!views.some((el) => el.id === "view-" + view)) { console.warn("nav: unknown view", view); return; }
  views.forEach((el) => el.classList.toggle("hidden", el.id !== "view-" + view));
  $$(".side-link, .mobile-nav button").forEach((l) =>
    l.classList.toggle("active", l.dataset.nav === view)
  );
  $(".workspace").scrollTo(0, 0);
  if (view === "configure") goStep(1);
  if (view === "scope") prepScopeView();
  if (view === "strengthen") prepArgumentView();
  if (view === "library") loadLibrary();
  if (view === "audit") loadAudit();
}

function prepScopeView() {
  const auth = $("#scope-auth");
  auth.classList.toggle("hidden", Boolean(state.authOk));
  if (!state.authOk) auth.textContent = state.authMsg;
  updateSourceControls();
}

function prepArgumentView() {
  const auth = $("#argument-auth");
  auth.classList.toggle("hidden", Boolean(state.authOk));
  if (!state.authOk) auth.textContent = state.authMsg;
  updateSourceControls();
}

function wireUI() {
  $$("[data-nav]").forEach((b) => (b.onclick = () => nav(b.dataset.nav)));
  $("#home-new").onclick = () => nav("configure");
  $("#home-how").onclick = () => nav("how");
  $("#home-council").onclick = () => nav("agents");
  $$("[data-preset]").forEach((b) => (b.onclick = () => applyPreset(b.dataset.preset)));
  $$("[data-argument-preset]").forEach((b) => (b.onclick = () => applyArgumentPreset(b.dataset.argumentPreset)));
  $("#wiz-back").onclick = () => goStep(state.step - 1);
  $("#wiz-next").onclick = () => { if (state.step < 3) goStep(state.step + 1); else launchNew(); };
  $("#cancel-btn").onclick = () => sendControl({ type: "cancel" });
  $("#result-new").onclick = () => nav(state.resultMode === "strengthen" ? "strengthen" : "configure");
  $("#result-quality-save").onclick = saveFinalQuality;
  $("#result-revise").onclick = () => openReviseModal(state.resultReviseSlug || state.resultSlug);
  $("#result-deck").onclick = () => startRun({
    type: "start", mode: "deck", slug: state.resultSlug,
    budget: state.defaultBudget,
  });
  $("#revise-cancel").onclick = () => $("#revise-overlay").classList.add("hidden");
  $("#revise-go").onclick = submitRevise;
  $("#f-pptx").onchange = () => { if (state.step === 3) buildReview(); };
  $$('input[name="f-council-model"]').forEach((input) => {
    input.onchange = updateCouncilModelAvailability;
  });
  $("#f-decision-frame-enabled").onchange = updateDecisionFrameVisibility;
  $("#scope-launch").onclick = () => {
    const title = $("#s-title").value.trim();
    if (!title) { $("#s-title").focus(); $("#s-title").style.borderColor = "var(--red)"; return; }
    if (!state.sourceUploads.scope.length) { flash($(".scope-required-note"), "Add at least one scope document."); return; }
    startRun({
      type: "start", mode: "scope", title, notes: $("#s-notes").value.trim(),
      source_tokens: state.sourceUploads.scope.map((file) => file.token),
      auto_approve: !$("#s-review").checked,
      budget: readBudget("#s-budget"),
    });
  };
  Object.keys(SOURCE_UI).forEach(setupSourceUploader);
  $("#a-pptx").onchange = () => {
    $("#argument-slide-field").classList.toggle("hidden", !$("#a-pptx").checked);
    $("#a-pptx").closest(".argument-output-card").classList.toggle("selected", $("#a-pptx").checked);
    updateArgumentCount();
  };
  $("#argument-launch").onclick = launchArgument;
  $("#guide-btn").onclick = openGuide;
  $("#guide-close").onclick = () => $("#guide-overlay").classList.add("hidden");
  $("#guide-overlay").onclick = (e) => { if (e.target === $("#guide-overlay")) $("#guide-overlay").classList.add("hidden"); };
  $("#prompt-close").onclick = closePrompt;
  $("#prompt-overlay").onclick = (e) => { if (e.target === $("#prompt-overlay")) closePrompt(); };
  $("#prompt-copy").onclick = copyPrompt;
  $("#prompt-coach-draft").onclick = requestPromptDraft;
  $("#prompt-coach-apply").onclick = applyPromptDraft;
  $("#prompt-coach-discard").onclick = discardPromptDraft;
  $("#library-edit-close").onclick = closeLibraryEdit;
  $("#library-edit-cancel").onclick = closeLibraryEdit;
  $("#library-edit-save").onclick = saveLibraryDetails;
  $("#library-delete-close").onclick = closeLibraryDelete;
  $("#library-delete-cancel").onclick = closeLibraryDelete;
  $("#library-delete-go").onclick = commitLibraryDelete;
  $("#library-toast-close").onclick = closeLibraryToast;
  $("#agent-profile-close").onclick = closeAgentProfile;
  $("#agent-profile-overlay").onclick = (e) => { if (e.target === $("#agent-profile-overlay")) closeAgentProfile(); };
  $("#library-edit-overlay").onclick = (e) => { if (e.target === $("#library-edit-overlay")) closeLibraryEdit(); };
  $("#library-delete-overlay").onclick = (e) => { if (e.target === $("#library-delete-overlay")) closeLibraryDelete(); };
  $("#agent-search").oninput = buildAgentCatalog;
  $$('[data-agent-filter]').forEach((button) => {
    button.onclick = () => {
      state.agentCatalogFilter = button.dataset.agentFilter;
      $$('[data-agent-filter]').forEach((item) => item.classList.toggle("active", item === button));
      buildAgentCatalog();
    };
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Tab" && activeLibraryDialog()) {
      trapLibraryDialogFocus(e);
      return;
    }
    if (e.key === "Escape") {
      if (closeActiveLibraryDialog()) {
        e.preventDefault();
        return;
      }
      $("#guide-overlay").classList.add("hidden");
      closePrompt();
    }
  });
  document.addEventListener("click", (event) => {
    if (!(event.target instanceof Element) || !event.target.closest(".ac-manage-wrap")) {
      $$(".ac-menu").forEach((menu) => menu.classList.add("hidden"));
      $$(".ac-manage").forEach((button) => button.setAttribute("aria-expanded", "false"));
    }
  });
  $("#log-toggle").onclick = () => { const l = $("#activity-log"); const h = l.classList.toggle("hidden"); $("#log-toggle").textContent = h ? "Show" : "Hide"; };

  updateCouncilModelAvailability();
  if (!state.promptCoachOk) {
    $("#prompt-coach-draft").disabled = true;
    $("#prompt-coach-status").textContent = state.promptCoachMsg;
  } else {
    $("#prompt-coach-status").textContent = `${modelShort(state.promptCoachModel)} via your ChatGPT subscription · no report is started.`;
  }
  $("#f-budget").value = state.defaultBudget;
  $("#a-budget").value = Math.min(state.defaultBudget, 60);
  updateDecisionFrameVisibility();
  updateSourceControls();
}

// ─────────── prompt coach ───────────
function decisionFrameEnabled() {
  return Boolean($("#f-decision-frame-enabled")?.checked);
}

function updateDecisionFrameVisibility() {
  const enabled = decisionFrameEnabled();
  const fields = $("#decision-frame-fields");
  fields.disabled = !enabled;
  fields.classList.toggle("hidden", !enabled);
  if (state.promptDraft) renderPromptDraft(state.promptDraft);
  if (state.step === 3) buildReview();
}

function promptFormSnapshot() {
  const includeDecision = decisionFrameEnabled();
  return {
    title: $("#f-title").value.trim(),
    thesis: $("#f-thesis").value.trim(),
    scope: linesOf($("#f-scope").value),
    avoid: linesOf($("#f-avoid").value),
    operator_context: $("#f-operator-context").value.trim(),
    decision_required: includeDecision ? $("#f-decision").value.trim() : "",
    decision_owner: includeDecision ? $("#f-owner").value.trim() : "",
    time_horizon: includeDecision ? $("#f-horizon").value.trim() : "",
    approval_path: includeDecision ? $("#f-approval").value.trim() : "",
    success_measure: includeDecision ? $("#f-success-measure").value.trim() : "",
  };
}

function setPromptCoachBusy(busy) {
  const button = $("#prompt-coach-draft");
  button.disabled = busy || !state.promptCoachOk;
  button.textContent = busy ? "Drafting…" : (promptFormSnapshot().thesis ? "Improve current draft" : "Draft this form");
}

async function requestPromptDraft() {
  const brief = $("#prompt-coach-brief").value.trim();
  const current = promptFormSnapshot();
  const status = $("#prompt-coach-status");
  if (!brief && !current.thesis) {
    status.textContent = "Add a rough idea or an existing thesis first.";
    status.style.color = "var(--red)";
    $("#prompt-coach-brief").focus();
    return;
  }
  const requestId = ++state.promptAssistRequestId;
  state.promptDraft = null;
  state.promptDraftReview = [];
  $("#prompt-coach-preview").classList.add("hidden");
  status.style.color = "";
  status.textContent = "The coach is structuring the question. No report is running.";
  setPromptCoachBusy(true);
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), PROMPT_COACH_TIMEOUT_MS);
  try {
    const response = await fetch("/api/run-prompt/draft", {
      method: "POST",
      headers: sourceHeaders({ "content-type": "application/json" }),
      body: JSON.stringify({
        brief,
        current,
        output_format: state.selectedFormat,
        decision_frame_enabled: decisionFrameEnabled(),
      }),
      signal: controller.signal,
    });
    const data = await response.json().catch(() => ({}));
    if (requestId !== state.promptAssistRequestId) return;
    if (!response.ok) throw new Error(data.error || "The prompt coach could not draft this form.");
    state.promptDraft = data.draft || null;
    if (!state.promptDraft) throw new Error("The prompt coach returned no usable draft.");
    renderPromptDraft(state.promptDraft);
    const cost = Number(data.cost_usd);
    const costLabel = data.auth_mode === "chatgpt_subscription"
      ? " · ChatGPT plan"
      : (Number.isFinite(cost) ? ` · ≈$${cost.toFixed(2)}` : "");
    status.textContent = `Draft ready${data.model ? ` · ${modelShort(data.model)}` : ""}${costLabel}. Review before applying.`;
    $("#prompt-coach-preview").classList.remove("hidden");
  } catch (error) {
    if (requestId !== state.promptAssistRequestId) return;
    status.style.color = "var(--red)";
    status.textContent = error?.name === "AbortError"
      ? "The prompt coach timed out. Your form was not changed."
      : String(error.message || error);
  } finally {
    clearTimeout(timeout);
    if (requestId === state.promptAssistRequestId) setPromptCoachBusy(false);
  }
}

function fillTextList(root, values) {
  root.replaceChildren();
  (Array.isArray(values) ? values : []).forEach((value) => {
    const item = document.createElement("li");
    item.textContent = String(value);
    root.appendChild(item);
  });
}

function normalizedPromptFieldValue(definition, source) {
  if (definition.kind === "list") {
    return (Array.isArray(source?.[definition.key]) ? source[definition.key] : [])
      .map((value) => String(value).trim()).filter(Boolean).join("\n");
  }
  return typeof source?.[definition.key] === "string" ? source[definition.key].trim() : "";
}

function promptDraftReview(draft, current = promptFormSnapshot()) {
  return PROMPT_FIELD_DEFINITIONS
    .filter((definition) => !definition.decision || decisionFrameEnabled())
    .map((definition) => {
    const before = normalizedPromptFieldValue(definition, current);
    const proposed = normalizedPromptFieldValue(definition, draft);
    // A blank coach response is absence of a suggestion, never permission to
    // erase a value the operator entered by hand.
    const canApply = Boolean(proposed) && proposed !== before;
    return { ...definition, before, proposed, canApply };
    });
}

function promptValueNode(value, emptyLabel) {
  const node = document.createElement("p");
  node.textContent = value || emptyLabel;
  node.classList.toggle("empty", !value);
  return node;
}

function updatePromptDraftSelection() {
  const selected = $$("#coach-preview-fields input[data-prompt-field]:checked:not(:disabled)").length;
  const button = $("#prompt-coach-apply");
  button.disabled = selected === 0;
  button.textContent = selected === 1 ? "Apply 1 selected change" : `Apply ${selected} selected changes`;
  $("#coach-selection-summary").textContent = selected
    ? `${selected} of ${state.promptDraftReview.filter((item) => item.canApply).length} proposed changes selected`
    : "No changes selected";
}

function renderPromptDraft(draft) {
  state.promptDraftReview = promptDraftReview(draft);
  const fields = $("#coach-preview-fields");
  fields.replaceChildren();
  state.promptDraftReview.forEach((change) => {
    const row = document.createElement("div");
    row.className = `coach-diff-row${change.canApply ? " changed" : ""}`;
    row.setAttribute("role", "listitem");

    const choice = document.createElement("label");
    choice.className = "coach-diff-choice";
    const input = document.createElement("input");
    input.type = "checkbox";
    input.dataset.promptField = change.key;
    input.checked = change.canApply;
    input.disabled = !change.canApply;
    input.onchange = updatePromptDraftSelection;
    const label = document.createElement("span");
    label.textContent = change.label;
    choice.append(input, label);

    const before = document.createElement("div");
    before.className = "coach-diff-value";
    const beforeLabel = document.createElement("span"); beforeLabel.textContent = "Current";
    before.append(beforeLabel, promptValueNode(change.before, "Not set"));

    const arrow = document.createElement("span");
    arrow.className = "coach-diff-arrow";
    arrow.setAttribute("aria-hidden", "true");
    arrow.textContent = "→";

    const after = document.createElement("div");
    after.className = "coach-diff-value proposed";
    const afterLabel = document.createElement("span");
    afterLabel.textContent = change.canApply
      ? "Proposed"
      : change.proposed ? "No change" : change.before ? "Kept — coach left blank" : "Not proposed";
    after.append(afterLabel, promptValueNode(change.proposed, "No replacement"));

    row.append(choice, before, arrow, after);
    fields.appendChild(row);
  });
  fillTextList($("#coach-preview-uncertainties"), draft.uncertainties);
  $("#coach-uncertainties-wrap").classList.toggle("hidden", !(draft.uncertainties || []).length);
  updatePromptDraftSelection();
}

function applyPromptFieldValue(change) {
  $(change.selector).value = change.kind === "list"
    ? change.proposed.split("\n").join("\n")
    : change.proposed;
}

function applyPromptDraft() {
  const draft = state.promptDraft;
  if (!draft) return;
  const selected = new Set(
    $$("#coach-preview-fields input[data-prompt-field]:checked:not(:disabled)")
      .map((input) => input.dataset.promptField),
  );
  if (!selected.size) return;
  const live = promptFormSnapshot();
  const applied = [];
  const changedSinceReview = [];
  state.promptDraftReview.forEach((change) => {
    if (!selected.has(change.key) || !change.canApply || !change.proposed) return;
    if (normalizedPromptFieldValue(change, live) !== change.before) {
      changedSinceReview.push(change.label);
      return;
    }
    applyPromptFieldValue(change);
    applied.push(change.key);
  });
  const status = $("#prompt-coach-status");
  if (changedSinceReview.length) {
    status.style.color = "var(--amber)";
    status.textContent = `${applied.length ? `Applied ${applied.length}. ` : ""}Kept ${changedSinceReview.join(", ")} because you edited ${changedSinceReview.length === 1 ? "it" : "them"} after review.`;
    renderPromptDraft(draft);
  } else {
    status.style.color = "var(--green)";
    status.textContent = `Applied ${applied.length} selected ${applied.length === 1 ? "change" : "changes"}. Review the form before continuing.`;
    $("#prompt-coach-preview").classList.add("hidden");
    state.promptDraft = null;
    state.promptDraftReview = [];
  }
  setPromptCoachBusy(false);
}

function discardPromptDraft() {
  state.promptAssistRequestId += 1;
  state.promptDraft = null;
  state.promptDraftReview = [];
  $("#prompt-coach-preview").classList.add("hidden");
  $("#prompt-coach-status").style.color = "";
  $("#prompt-coach-status").textContent = "Draft discarded. Your form was not changed.";
  setPromptCoachBusy(false);
}

// ─────────── wizard ───────────
function goStep(n) {
  if (n < 1 || n > 3) return;
  if (n === 2 && !$("#f-thesis").value.trim()) { goStep(1); $("#f-thesis").focus(); $("#f-thesis").style.borderColor = "var(--red)"; return; }
  if (n === 3 && state.seated.size === 0) { goStep(2); flash($("#seated-count"), "Seat at least one agent."); return; }
  state.step = n;
  $$(".wiz-panel").forEach((p) => p.classList.toggle("hidden", +p.dataset.panel !== n));
  $$(".wiz-step").forEach((s) => { const sn = +s.dataset.step; s.classList.toggle("active", sn === n); s.classList.toggle("done", sn < n); });
  $$(".wiz-dots i").forEach((d) => d.classList.toggle("on", +d.dataset.dot === n));
  $("#wiz-back").style.visibility = n === 1 ? "hidden" : "visible";
  $("#wiz-next").textContent = n === 3 ? "🚀  Convene the Council" : "Next →";
  $("#wiz-next").disabled = n === 3 && (!councilModelReady() || state.sourceUploading.report > 0);
  if (n === 3) { updateCouncilModelAvailability(); buildReview(); }
}
function flash(el, msg) {
  const original = el.innerHTML; el.textContent = msg; el.style.color = "var(--red)";
  setTimeout(() => {
    el.style.color = "";
    if (el.id === "seated-count") updateCount();
    else if (el.id === "argument-seated-count") updateArgumentCount();
    else el.innerHTML = original;
  }, 1800);
}

function buildReview() {
  const fmtLabel = (state.formats.find((f) => f.key === state.selectedFormat) || {}).label || state.selectedFormat;
  const seated = Array.from(state.seated);
  const chips = seated.map((n) => `<span class="chip">${escapeHtml(state.meta[n]?.display || n)}</span>`).join("");
  const scope = linesOf($("#f-scope").value), avoid = linesOf($("#f-avoid").value);
  const rows = [
    ["Title", escapeHtml($("#f-title").value.trim() || "—")],
    ["Thesis", escapeHtml($("#f-thesis").value.trim() || "—")],
    ["Format", escapeHtml(fmtLabel)],
    ["Model", escapeHtml(councilModelMeta().label)],
    [`Council`, chips || "—"],
  ];
  if (scope.length) rows.push(["Scope", scope.map(escapeHtml).join(" · ")]);
  if (avoid.length) rows.push(["Avoid", avoid.map(escapeHtml).join(" · ")]);
  const decision = $("#f-decision").value.trim();
  const owner = $("#f-owner").value.trim();
  if (decisionFrameEnabled()) {
    rows.push(["Decision", escapeHtml(
      [decision || "To be established", owner ? `Owner: ${owner}` : ""]
        .filter(Boolean).join(" · ")
    )]);
  }
  if ($("#f-pptx").checked) {
    rows.push(["Deck", escapeHtml($("#f-deck-mode").selectedOptions[0]?.textContent || "Board decision")]);
  }
  if (state.sourceUploads.report.length) rows.push(["Sources", state.sourceUploads.report.map((s) => escapeHtml(s.name)).join(", ")]);
  rows.push(["Plan", `<span class="est">${escapeHtml(
    councilModelMeta().provider === "openai" ? "ChatGPT subscription" : "Claude subscription"
  )}</span><span class="est-note"> · no provider API key</span>`]);
  $("#review-summary").innerHTML = rows.map(([k, v]) =>
    `<div class="rs-row"><div class="rs-key">${k}</div><div class="rs-val">${v}</div></div>`).join("");
}

// ─────────── home / library ───────────
async function loadHome() {
  const data = await fetch("/api/home").then((r) => r.json());
  state.home = data;
  $("#ss-runs").textContent = data.archives.length;
  const rb = $("#resume-banner");
  rb.classList.toggle("recovery-error", Boolean(data.library_recovery_warning));
  if (data.library_recovery_warning) {
    rb.replaceChildren();
    const message = document.createElement("div");
    message.className = "rb-text";
    const heading = document.createElement("b");
    heading.textContent = "Library recovery needs attention. ";
    message.append(heading, document.createTextNode(
      `${data.library_recovery_warning.message} Read-only browsing remains available.`,
    ));
    rb.appendChild(message);
    rb.classList.remove("hidden");
  } else if (data.interrupted) {
    rb.innerHTML = `<div class="rb-text">⟳ An interrupted run is waiting — <b>${escapeHtml(data.interrupted.title)}</b> (${escapeHtml(data.interrupted.where)}, ${escapeHtml(data.interrupted.age || "")}).</div>`;
    const btn = document.createElement("button"); btn.className = "btn-primary"; btn.textContent = "Resume →";
    btn.onclick = () => startRun({ type: "start", mode: "resume", slug: data.interrupted.slug, auto_approve: false, budget: state.defaultBudget });
    rb.appendChild(btn); rb.classList.remove("hidden");
  } else rb.classList.add("hidden");
  renderArchives($("#home-archives"), data.archives.slice(0, 6));
}
async function loadLibrary() {
  const data = state.home || (await fetch("/api/home").then((r) => r.json()));
  renderArchives($("#library-grid"), data.archives);
}
function renderArchives(root, archives) {
  root.innerHTML = "";
  if (!archives.length) { root.innerHTML = `<p class="muted">No completed work yet. Begin your first Council run.</p>`; return; }
  const canManage = root.id === "library-grid";
  archives.forEach((a, idx) => {
    const card = document.createElement("div"); card.className = "archive-card";
    card.style.animationDelay = (idx * 0.05).toFixed(2) + "s";
    const dls = a.downloads.map((d) => `<a class="ac-btn" href="${d.url}">⤓ ${escapeHtml(d.label)}</a>`).join("");
    const rev = a.revisions > 0 ? `<span class="ac-badge">v${a.revisions}</span>` : "";
    const read = a.can_read === false ? "" : `<button class="ac-btn" data-read="${a.slug}">Read</button>`;
    const promptBadge = a.prompt?.provenance === "verified_archive"
      ? " ✓"
      : a.prompt?.provenance === "archived_unverified"
        ? " · archived"
        : " · legacy";
    const prompt = a.prompt?.available && ["report", "revision"].includes(a.mode || "report")
      ? `<button class="ac-btn ac-prompt" data-prompt="${a.slug}" title="${escapeHtml(a.prompt.notice || "View the run prompt")}">Prompt${promptBadge}</button>`
      : "";
    const revise = a.can_revise === false ? "" : `<button class="ac-btn" data-revise="${a.revise_slug || a.slug}">Revise</button>`;
    const deck = a.can_build_deck === false || a.has_deck ? "" : `<button class="ac-btn" data-deck="${a.slug}">Build deck</button>`;
    const summary = a.summary ? `<p class="ac-summary">${escapeHtml(a.summary)}</p>` : "";
    const tags = Array.isArray(a.tags) && a.tags.length
      ? `<div class="ac-tags">${a.tags.map((tag) => `<span class="ac-tag">${escapeHtml(tag)}</span>`).join("")}</div>`
      : "";
    const manage = canManage ? `<div class="ac-manage-wrap"><button class="ac-manage" type="button" aria-label="Manage ${escapeHtml(a.title)}" aria-expanded="false">•••</button>
      <div class="ac-menu hidden"><button type="button" data-library-edit>Edit details</button><button type="button" class="danger" data-library-delete>Delete report</button></div></div>` : "";
    card.innerHTML = `<div class="ac-head"><div class="ac-date">${escapeHtml(a.date)} · ${escapeHtml(a.format)}</div>${manage}</div>
      <div class="ac-title">${escapeHtml(a.title)}${rev}</div>${summary}${tags}
      <div class="ac-actions">${read}${prompt}${dls}${revise}${deck}</div>`;
    const reader = card.querySelector("[data-read]");
    if (reader) reader.onclick = () => openReport(
      a.slug, a.title, a.revise_slug || a.slug, a.can_build_deck !== false, a.mode || "report"
    );
    const promptButton = card.querySelector("[data-prompt]");
    if (promptButton) promptButton.onclick = () => openPrompt(a);
    const reviser = card.querySelector("[data-revise]");
    if (reviser) reviser.onclick = () => openReviseModal(a.revise_slug || a.slug);
    const dk = card.querySelector("[data-deck]"); if (dk) dk.onclick = () => startRun({
      type: "start", mode: "deck", slug: a.slug,
      budget: state.defaultBudget,
    });
    const manageButton = card.querySelector(".ac-manage");
    if (manageButton) manageButton.onclick = (event) => {
      event.stopPropagation();
      const menu = card.querySelector(".ac-menu");
      const willOpen = menu.classList.contains("hidden");
      $$(".ac-menu").forEach((item) => item.classList.add("hidden"));
      $$(".ac-manage").forEach((item) => item.setAttribute("aria-expanded", "false"));
      menu.classList.toggle("hidden", !willOpen);
      manageButton.setAttribute("aria-expanded", String(willOpen));
    };
    const editor = card.querySelector("[data-library-edit]");
    if (editor) editor.onclick = (event) => openLibraryEdit(a, event.currentTarget);
    const deleter = card.querySelector("[data-library-delete]");
    if (deleter) deleter.onclick = (event) => openLibraryDelete(a, event.currentTarget);
    root.appendChild(card);
  });
}

async function openPrompt(archive) {
  const requestId = ++state.promptRequestId;
  const overlay = $("#prompt-overlay");
  const mode = archive.mode === "revision" ? "revision" : "report";
  state.promptText = "";
  $("#prompt-title").textContent = archive.title;
  $("#prompt-provenance").textContent = "Loading prompt provenance…";
  $("#prompt-provenance").className = "prompt-provenance";
  $("#prompt-notice").textContent = "";
  $("#prompt-body").textContent = "Loading…";
  $("#prompt-copy").disabled = true;
  $("#prompt-copy-status").textContent = "";
  overlay.classList.remove("hidden");
  try {
    const response = await fetch(
      `/api/library/${mode}/${encodeURIComponent(archive.slug)}/prompt`,
      { method: "POST", headers: sourceHeaders() },
    );
    const data = await response.json();
    if (requestId !== state.promptRequestId) return;
    if (!response.ok) throw new Error(data.error || "Prompt unavailable.");
    state.promptText = String(data.markdown || "");
    $("#prompt-title").textContent = `${archive.title} — ${data.label || "Run prompt"}`;
    const provenance = data.provenance === "verified_archive"
      ? { label: "✓ Verified archived prompt", style: "exact" }
      : data.provenance === "archived_unverified"
        ? { label: "Archived prompt · no historical hash receipt", style: "archived" }
        : { label: "Legacy live prompt candidate", style: "legacy" };
    $("#prompt-provenance").textContent = provenance.label;
    $("#prompt-provenance").className = `prompt-provenance ${provenance.style}`;
    $("#prompt-notice").textContent = data.notice || "";
    // Prompts are evidence, not display markup. Keep the original text literal
    // so embedded HTML can never execute in the Library.
    $("#prompt-body").textContent = state.promptText;
    $("#prompt-copy").disabled = !state.promptText;
  } catch (error) {
    if (requestId !== state.promptRequestId) return;
    $("#prompt-provenance").textContent = "Prompt unavailable";
    $("#prompt-provenance").className = "prompt-provenance error";
    $("#prompt-notice").textContent = String(error.message || error);
    $("#prompt-body").textContent = "";
  }
}

function closePrompt() {
  state.promptRequestId += 1;
  $("#prompt-overlay")?.classList.add("hidden");
}

async function copyPrompt() {
  if (!state.promptText) return;
  try {
    await navigator.clipboard.writeText(state.promptText);
    $("#prompt-copy-status").textContent = "Copied";
  } catch (_) {
    $("#prompt-copy-status").textContent = "Copy failed — select the text instead.";
  }
}

function libraryItemPath(archive, suffix = "") {
  const mode = archive.mode || "report";
  return `/api/library/${encodeURIComponent(mode)}/${encodeURIComponent(archive.slug)}${suffix}`;
}

async function refreshLibrary() {
  state.home = null;
  await loadHome();
  if (!$("#view-library").classList.contains("hidden")) await loadLibrary();
}

const libraryDialogBackground = new Map();
let libraryDialogOverlay = null;
let libraryDialogReturnFocus = null;

function activeLibraryDialog() {
  return libraryDialogOverlay && !libraryDialogOverlay.classList.contains("hidden")
    ? libraryDialogOverlay
    : null;
}

function setLibraryDialogBackgroundInert(overlay, locked) {
  if (locked) {
    libraryDialogBackground.clear();
    Array.from(document.body.children).forEach((element) => {
      if (!(element instanceof HTMLElement) || element === overlay || element.tagName === "SCRIPT") return;
      libraryDialogBackground.set(element, {
        inert: element.inert,
        ariaHidden: element.getAttribute("aria-hidden"),
      });
      element.inert = true;
      element.setAttribute("aria-hidden", "true");
    });
    return;
  }
  libraryDialogBackground.forEach((previous, element) => {
    element.inert = previous.inert;
    if (previous.ariaHidden === null) element.removeAttribute("aria-hidden");
    else element.setAttribute("aria-hidden", previous.ariaHidden);
  });
  libraryDialogBackground.clear();
}

function openLibraryDialog(overlay, trigger, initialFocus) {
  const current = activeLibraryDialog();
  if (current === overlay) {
    requestAnimationFrame(() => {
      if (activeLibraryDialog() === overlay) (initialFocus || overlay.querySelector("[role=dialog]"))?.focus();
    });
    return;
  }
  if (current && current !== overlay) closeLibraryDialog(current, false);
  libraryDialogOverlay = overlay;
  libraryDialogReturnFocus = trigger instanceof HTMLElement
    ? trigger
    : document.activeElement instanceof HTMLElement ? document.activeElement : null;
  overlay.classList.remove("hidden");
  overlay.removeAttribute("aria-hidden");
  setLibraryDialogBackgroundInert(overlay, true);
  requestAnimationFrame(() => {
    if (activeLibraryDialog() === overlay) (initialFocus || overlay.querySelector("[role=dialog]"))?.focus();
  });
}

function closeLibraryDialog(overlay, restoreFocus = true) {
  if (!overlay || overlay.classList.contains("hidden")) return;
  overlay.classList.add("hidden");
  overlay.setAttribute("aria-hidden", "true");
  if (libraryDialogOverlay !== overlay) return;
  const returnFocus = libraryDialogReturnFocus;
  setLibraryDialogBackgroundInert(overlay, false);
  libraryDialogOverlay = null;
  libraryDialogReturnFocus = null;
  if (restoreFocus && returnFocus?.isConnected) returnFocus.focus();
}

function libraryDialogFocusable(overlay) {
  return Array.from(overlay.querySelectorAll(
    'button:not([disabled]), input:not([disabled]), textarea:not([disabled]), select:not([disabled]), a[href], [tabindex]:not([tabindex="-1"])',
  )).filter((element) => element instanceof HTMLElement && !element.closest(".hidden"));
}

function trapLibraryDialogFocus(event) {
  const overlay = activeLibraryDialog();
  if (!overlay) return;
  const focusable = libraryDialogFocusable(overlay);
  if (!focusable.length) {
    event.preventDefault();
    overlay.querySelector("[role=dialog]")?.focus();
    return;
  }
  const first = focusable[0];
  const last = focusable[focusable.length - 1];
  if (!overlay.contains(document.activeElement)) {
    event.preventDefault();
    (event.shiftKey ? last : first).focus();
  } else if (event.shiftKey && document.activeElement === first) {
    event.preventDefault();
    last.focus();
  } else if (!event.shiftKey && document.activeElement === last) {
    event.preventDefault();
    first.focus();
  }
}

function closeActiveLibraryDialog() {
  const overlay = activeLibraryDialog();
  if (overlay === $("#agent-profile-overlay")) {
    closeAgentProfile();
    return true;
  }
  if (overlay === $("#library-edit-overlay") && !state.libraryEditSaving) {
    closeLibraryEdit();
    return true;
  }
  if (overlay === $("#library-delete-overlay") && !state.libraryDeleteCommitting) {
    closeLibraryDelete();
    return true;
  }
  return false;
}

function closeLibraryEdit() {
  if (state.libraryEditSaving) return;
  state.libraryEditArchive = null;
  closeLibraryDialog($("#library-edit-overlay"));
  $("#library-edit-status").textContent = "";
}

function openLibraryEdit(archive, trigger = null) {
  state.libraryEditArchive = archive;
  state.libraryEditSaving = false;
  $("#library-edit-title").textContent = `Edit ${archive.title}`;
  $("#library-edit-name").value = archive.title || "";
  $("#library-edit-summary").value = archive.summary || "";
  $("#library-edit-tags").value = Array.isArray(archive.tags) ? archive.tags.join(", ") : "";
  $("#library-edit-status").textContent = "";
  $("#library-edit-save").disabled = false;
  $("#library-edit-close").disabled = false;
  $("#library-edit-cancel").disabled = false;
  openLibraryDialog($("#library-edit-overlay"), trigger, $("#library-edit-name"));
}

async function saveLibraryDetails() {
  const archive = state.libraryEditArchive;
  if (!archive) return;
  const status = $("#library-edit-status");
  const title = $("#library-edit-name").value.trim();
  if (!title) {
    status.style.color = "var(--red)";
    status.textContent = "Display title is required.";
    $("#library-edit-name").focus();
    return;
  }
  const tags = $("#library-edit-tags").value.split(",").map((tag) => tag.trim()).filter(Boolean);
  state.libraryEditSaving = true;
  $("#library-edit-save").disabled = true;
  $("#library-edit-close").disabled = true;
  $("#library-edit-cancel").disabled = true;
  status.style.color = "";
  status.textContent = "Saving display details…";
  try {
    const response = await fetch(libraryItemPath(archive), {
      method: "PATCH",
      headers: sourceHeaders({ "content-type": "application/json" }),
      body: JSON.stringify({ title, summary: $("#library-edit-summary").value.trim(), tags }),
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.error || "Could not save Library details.");
    state.libraryEditSaving = false;
    closeLibraryEdit();
    await refreshLibrary();
  } catch (error) {
    state.libraryEditSaving = false;
    status.style.color = "var(--red)";
    status.textContent = String(error.message || error);
    $("#library-edit-save").disabled = false;
    $("#library-edit-close").disabled = false;
    $("#library-edit-cancel").disabled = false;
  }
}

function formatBytes(bytes) {
  const value = Number(bytes) || 0;
  if (value < 1024) return `${value} B`;
  if (value < 1024 ** 2) return `${(value / 1024).toFixed(1)} KB`;
  if (value < 1024 ** 3) return `${(value / 1024 ** 2).toFixed(1)} MB`;
  return `${(value / 1024 ** 3).toFixed(2)} GB`;
}

const DELETE_GROUP_LABELS = {
  distribution_pointer: "Current release pointers",
  distribution_file: "Word, deck, and package files",
  release_bundle: "Immutable release bundles",
  metadata: "Library display details",
  prompt: "Run prompt",
  source_library: "Council-owned source copies",
  run_archive: "Run archives and revisions",
};

function renderLibraryDeletePlan(plan) {
  const summary = $("#library-delete-summary");
  summary.replaceChildren();
  [["Files", plan.file_count], ["Data", formatBytes(plan.total_bytes)], ["Revisions", plan.revision_count || 0]].forEach(([label, value]) => {
    const cell = document.createElement("div");
    const key = document.createElement("span"); key.textContent = label;
    const amount = document.createElement("b"); amount.textContent = String(value);
    cell.append(key, amount); summary.appendChild(cell);
  });
  const groups = $("#library-delete-groups"); groups.replaceChildren();
  Object.entries(plan.groups || {}).forEach(([name, values]) => {
    const row = document.createElement("div"); row.className = "delete-group";
    const label = document.createElement("span"); label.textContent = DELETE_GROUP_LABELS[name] || name.replaceAll("_", " ");
    const count = document.createElement("b"); count.textContent = `${values.files || values.targets || 0} file${(values.files || values.targets || 0) === 1 ? "" : "s"}`;
    row.append(label, count); groups.appendChild(row);
  });
  const familyNote = plan.family_mode === "report"
    ? "Revisions form one verified sequence. This preview covers the original report and every revision as one family."
    : "This preview covers every Council-owned artifact associated with this Library item.";
  $("#library-delete-explanation").textContent = `${familyNote} Confirming permanently deletes the verified files and reclaims approximately ${formatBytes(plan.total_bytes)}.`;
  $("#library-delete-go").textContent = `Permanently delete ${plan.file_count || 0} file${plan.file_count === 1 ? "" : "s"}`;
  $("#library-delete-status").style.color = "";
  $("#library-delete-status").textContent = "Inventory verified. Ready for confirmation.";
  updateLibraryDeleteButton();
}

async function openLibraryDelete(archive, trigger = null) {
  const requestId = ++state.libraryMutationRequestId;
  state.libraryDeletePlan = null;
  state.libraryDeleteCommitting = false;
  $("#library-delete-title").textContent = `Delete ${archive.title} permanently`;
  $("#library-delete-explanation").textContent = "Building an exact, hash-bound inventory before anything moves…";
  $("#library-delete-summary").replaceChildren();
  $("#library-delete-groups").replaceChildren();
  $("#library-delete-status").textContent = "";
  $("#library-delete-go").textContent = "Delete entire family permanently";
  $("#library-delete-close").disabled = false;
  $("#library-delete-cancel").disabled = false;
  openLibraryDialog($("#library-delete-overlay"), trigger, $("#library-delete-close"));
  updateLibraryDeleteButton();
  try {
    const response = await fetch(libraryItemPath(archive, "/delete-plan"), {
      method: "POST", headers: sourceHeaders(),
    });
    const data = await response.json().catch(() => ({}));
    if (requestId !== state.libraryMutationRequestId) return;
    if (!response.ok) throw new Error(data.error || "Could not preview this Library removal.");
    state.libraryDeletePlan = { archive, ...data };
    renderLibraryDeletePlan(state.libraryDeletePlan);
  } catch (error) {
    if (requestId !== state.libraryMutationRequestId) return;
    $("#library-delete-status").style.color = "var(--red)";
    $("#library-delete-status").textContent = String(error.message || error);
  }
}

function closeLibraryDelete() {
  if (state.libraryDeleteCommitting) return;
  state.libraryMutationRequestId += 1;
  state.libraryDeletePlan = null;
  closeLibraryDialog($("#library-delete-overlay"));
  $("#library-delete-status").textContent = "";
}

function updateLibraryDeleteButton() {
  const plan = state.libraryDeletePlan;
  $("#library-delete-go").disabled = !plan || state.libraryDeleteCommitting;
}

async function commitLibraryDelete() {
  const plan = state.libraryDeletePlan;
  if (!plan || state.libraryDeleteCommitting) return;
  const status = $("#library-delete-status");
  state.libraryDeleteCommitting = true;
  $("#library-delete-go").disabled = true;
  $("#library-delete-close").disabled = true;
  $("#library-delete-cancel").disabled = true;
  status.style.color = "";
  status.textContent = "Deleting the verified report family and reclaiming its storage…";
  try {
    const response = await fetch(libraryItemPath(plan.archive), {
      method: "DELETE",
      headers: sourceHeaders({ "content-type": "application/json" }),
      body: JSON.stringify({ plan_id: plan.plan_id, confirmation: plan.confirmation }),
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.error || "The Library family was not deleted.");
    const receipt = data.receipt || data;
    state.libraryDeleteCommitting = false;
    closeLibraryDelete();
    await refreshLibrary();
    if (receipt.recoverable) showLibraryUndo(receipt);
    else showLibraryDeletion(receipt);
  } catch (error) {
    state.libraryDeleteCommitting = false;
    status.style.color = "var(--red)";
    status.textContent = String(error.message || error);
    $("#library-delete-close").disabled = false;
    $("#library-delete-cancel").disabled = false;
    updateLibraryDeleteButton();
  }
}

function closeLibraryToast() {
  if (state.libraryToastTimer) clearTimeout(state.libraryToastTimer);
  state.libraryToastTimer = null;
  $("#library-toast").classList.add("hidden");
  $("#library-toast-undo").onclick = null;
}

function showLibraryUndo(receipt) {
  if (state.libraryToastTimer) clearTimeout(state.libraryToastTimer);
  state.libraryToastTimer = null;
  const toast = $("#library-toast");
  const button = $("#library-toast-undo");
  $("#library-toast-message").textContent = `${receipt.family_slug || "Library family"} moved to Council Trash.`;
  button.classList.remove("hidden");
  button.disabled = false;
  button.textContent = "Undo";
  button.onclick = () => restoreLibraryReceipt(receipt);
  toast.classList.remove("hidden");
}

function showLibraryDeletion(receipt) {
  if (state.libraryToastTimer) clearTimeout(state.libraryToastTimer);
  const button = $("#library-toast-undo");
  button.classList.add("hidden");
  button.disabled = true;
  button.onclick = null;
  const reclaimed = formatBytes(receipt.reclaimed_bytes || receipt.total_bytes || 0);
  $("#library-toast-message").textContent = receipt.cleanup_pending
    ? `Report deleted. ${reclaimed} of staged storage will finish clearing automatically.`
    : `Report permanently deleted. Approximately ${reclaimed} reclaimed.`;
  $("#library-toast").classList.remove("hidden");
  state.libraryToastTimer = setTimeout(closeLibraryToast, 7000);
}

async function restoreLibraryReceipt(receipt) {
  const button = $("#library-toast-undo");
  button.disabled = true;
  button.textContent = "Restoring…";
  try {
    const response = await fetch(`/api/library/trash/${encodeURIComponent(receipt.receipt_id)}/restore`, {
      method: "POST", headers: sourceHeaders(),
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.error || "Could not restore the Library family.");
    await refreshLibrary();
    $("#library-toast-message").textContent = "Library family restored.";
    button.classList.add("hidden");
    setTimeout(closeLibraryToast, 3000);
  } catch (error) {
    $("#library-toast-message").textContent = String(error.message || error);
    button.disabled = false;
    button.textContent = "Undo";
  }
}

async function loadAudit() {
  $("#audit-body").innerHTML = `<p class="muted">Scanning archived runs…</p>`;
  const data = await fetch("/api/audit").then((r) => r.json());
  $("#audit-body").innerHTML = renderMarkdown(data.markdown);
}
async function openReport(slug, title, reviseSlug = slug, canBuildDeck = true, mode = "report") {
  state.resultSlug = slug;
  state.resultReviseSlug = reviseSlug;
  const data = await fetch(`/api/report/${slug}`).then((r) => r.json());
  state.resultMode = data.mode || mode;
  state.resultReviseSlug = data.revise_slug || reviseSlug;
  $("#result-badge").textContent = state.resultMode === "strengthen" ? "Archived argument" : "Archived report";
  $("#result-title").textContent = title; $("#result-cost").textContent = "From the library";
  $("#result-revise").classList.toggle("hidden", state.resultMode === "strengthen");
  $("#result-deck").classList.toggle("hidden", !canBuildDeck || state.resultMode === "strengthen");
  $("#result-quality").classList.toggle("hidden", state.resultMode === "strengthen");
  $("#result-new").textContent = state.resultMode === "strengthen" ? "Strengthen another argument" : "New report";
  $("#result-body").innerHTML = renderMarkdown(data.markdown || ""); buildTOC();
  renderDownloads(data.downloads); nav("result");
}

// ─────────── form ───────────
function buildFormats() {
  const row = $("#format-pills"); row.innerHTML = "";
  const preferred = state.formats.some((format) => format.key === "article") ? "article" : state.formats[0]?.key;
  state.selectedFormat = preferred || "article";
  state.formats.forEach((f) => {
    const pill = document.createElement("button"); pill.className = "format-pill" + (f.key === state.selectedFormat ? " active" : ""); pill.textContent = f.label;
    pill.onclick = () => { $$(".format-pill").forEach((p) => p.classList.remove("active")); pill.classList.add("active"); state.selectedFormat = f.key; };
    row.appendChild(pill);
  });
}
function buildAgentGroups() {
  const root = $("#agent-groups"); root.innerHTML = "";
  state.groups.forEach((g) => {
    const label = document.createElement("div"); label.className = "agent-group-label"; label.textContent = g.label; root.appendChild(label);
    const grid = document.createElement("div"); grid.className = "agent-grid";
    g.members.forEach((m, i) => { const chip = agentChip(m, "report"); chip.style.animation = `itemin .5s var(--ease) ${(i * 0.03).toFixed(2)}s backwards`; grid.appendChild(chip); });
    root.appendChild(grid);
  });
}

function buildAgentCatalog() {
  const root = $("#agent-catalog");
  if (!root) return;
  const research = state.groups.flatMap((group) => group.members.map((member) => ({
    ...member,
    group: group.label,
    category: member.supplemental ? "outside" : "airport",
  })));
  const process = state.processAgents.map((member) => ({
    ...member,
    group: "Production workflow",
    category: "process",
  }));
  const query = String($("#agent-search")?.value || "").trim().toLowerCase();
  const filtered = [...research, ...process].filter((member) => {
    if (state.agentCatalogFilter !== "all" && member.category !== state.agentCatalogFilter) return false;
    if (!query) return true;
    return [member.display, member.name, member.description, member.group]
      .join(" ").toLowerCase().includes(query);
  });
  $("#agent-catalog-count").textContent = `${filtered.length} agent${filtered.length === 1 ? "" : "s"}`;
  root.innerHTML = "";
  filtered.forEach((member, index) => {
    const card = document.createElement("button");
    card.type = "button";
    card.className = "catalog-card";
    card.setAttribute("aria-haspopup", "dialog");
    card.setAttribute("aria-label", `Read the complete profile for ${member.display}`);
    card.style.animationDelay = `${Math.min(index, 12) * 0.025}s`;
    const type = member.category === "process"
      ? "Process agent"
      : member.category === "outside" ? "Outside perspective" : member.group;
    const flags = [
      member.default ? '<span class="catalog-tag default">Balanced roster</span>' : "",
      member.name === "deep-research" ? '<span class="catalog-tag gated">Long-horizon lens</span>' : "",
    ].filter(Boolean).join("");
    card.innerHTML = `<span class="catalog-card-top"><span class="catalog-kind">${escapeHtml(type)}</span>${flags}</span>
      <span class="catalog-card-title">${escapeHtml(member.display)}</span>
      <span class="catalog-card-description">${escapeHtml(String(member.description || "").replace(/\s+/g, " ").trim())}</span>
      <span class="catalog-card-open">Read full profile <i aria-hidden="true">→</i></span>`;
    card.onclick = () => openAgentProfile(member, card);
    root.appendChild(card);
  });
  if (!filtered.length) root.innerHTML = '<p class="muted catalog-empty">No agents match that search.</p>';
}

function agentProfileType(member) {
  if (member.category === "process") return "Process agent";
  if (member.category === "outside") return "Outside perspective";
  return "Airport research lens";
}

async function openAgentProfile(member, trigger) {
  const overlay = $("#agent-profile-overlay");
  const body = $("#agent-profile-body");
  const status = $("#agent-profile-status");
  const requestId = ++state.agentProfileRequestId;
  $("#agent-profile-kind").textContent = agentProfileType(member);
  $("#agent-profile-title").textContent = member.display;
  $("#agent-profile-description").textContent = member.description || "";
  $("#agent-profile-monogram").textContent = initials(member.display);
  $("#agent-profile-stage").textContent = member.category === "process"
    ? "Controlled process role"
    : "Independent research role";
  body.className = "agent-profile-body loading";
  body.textContent = "Loading the complete operational charter…";
  body.setAttribute("aria-busy", "true");
  body.scrollTop = 0;
  status.textContent = "Loading the complete agent profile.";
  openLibraryDialog(overlay, trigger, $("#agent-profile-close"));

  try {
    let profile = state.agentProfiles.get(member.name);
    if (!profile) {
      const response = await fetch(`/api/agents/${encodeURIComponent(member.name)}/profile`, {
        method: "POST",
        headers: sourceHeaders(),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || "Agent profile unavailable.");
      profile = String(data.profile || "");
      state.agentProfiles.set(member.name, profile);
    }
    if (requestId !== state.agentProfileRequestId || overlay.classList.contains("hidden")) return;
    body.className = "agent-profile-body";
    body.removeAttribute("aria-busy");
    body.innerHTML = renderMarkdown(normalizeAgentProfileMarkdown(profile), { stripInternal: false });
    status.textContent = "The complete agent profile is ready.";
  } catch (error) {
    if (requestId !== state.agentProfileRequestId || overlay.classList.contains("hidden")) return;
    body.className = "agent-profile-body error";
    body.removeAttribute("aria-busy");
    body.textContent = String(error.message || error);
    status.textContent = "The agent profile could not be loaded.";
  }
}

function closeAgentProfile() {
  state.agentProfileRequestId += 1;
  $("#agent-profile-status").textContent = "";
  closeLibraryDialog($("#agent-profile-overlay"));
}

function buildArgumentAgentGroups() {
  const root = $("#argument-agent-groups"); root.innerHTML = "";
  state.groups.forEach((g) => {
    const label = document.createElement("div"); label.className = "agent-group-label"; label.textContent = g.label; root.appendChild(label);
    const grid = document.createElement("div"); grid.className = "agent-grid";
    g.members.forEach((m, i) => { const chip = agentChip(m, "argument"); chip.style.animation = `itemin .5s var(--ease) ${(i * 0.03).toFixed(2)}s backwards`; grid.appendChild(chip); });
    root.appendChild(grid);
  });
}
function agentChip(m, picker = "report") {
  const chip = document.createElement("div"); chip.className = "agent-chip"; chip.dataset.name = m.name; chip.dataset.picker = picker;
  const needsSeparateOpenAI = picker === "argument" && m.gated;
  chip.innerHTML = `<div class="agent-check">✓</div><div><div class="agent-name">${escapeHtml(m.display)}${needsSeparateOpenAI ? '<span class="agent-gated">needs ChatGPT login</span>' : ""}</div><div class="agent-desc">${escapeHtml(m.description)}</div></div>`;
  chip.onclick = () => {
    if (needsSeparateOpenAI && !state.codexOk) {
      alert(`${m.display} uses your ChatGPT subscription. Run codex login, restart the Council, and reload.`);
      return;
    }
    const selected = picker === "argument" ? state.argumentSeated : state.seated;
    if (selected.has(m.name)) { selected.delete(m.name); chip.classList.remove("on"); }
    else { selected.add(m.name); chip.classList.add("on"); }
    if (picker === "argument") updateArgumentCount(); else updateCount();
  };
  return chip;
}
function setSeated(names) { state.seated = new Set(names); $$("#agent-groups .agent-chip").forEach((c) => c.classList.toggle("on", state.seated.has(c.dataset.name))); updateCount(); }
function applyPreset(which) {
  const all = Object.values(state.meta).filter((m) => !m.process);
  if (which === "none") return setSeated([]);
  if (which === "default") return setSeated(all.filter((m) => m.default).map((m) => m.name));
  if (which === "all") return setSeated(all.filter((m) => !m.gated && !m.supplemental).map((m) => m.name));
}
function setArgumentSeated(names) {
  state.argumentSeated = new Set(names);
  $$("#argument-agent-groups .agent-chip").forEach((c) => c.classList.toggle("on", state.argumentSeated.has(c.dataset.name)));
  updateArgumentCount();
}
function applyArgumentPreset(which) {
  const all = Object.values(state.meta).filter((m) => !m.process);
  if (which === "none") return setArgumentSeated([]);
  if (which === "fast") return setArgumentSeated(ARGUMENT_FAST_PRESET.filter((name) => state.meta[name]));
  if (which === "default") return setArgumentSeated(all.filter((m) => m.default).map((m) => m.name));
  if (which === "all") return setArgumentSeated(all.filter((m) => !m.gated && !m.supplemental).map((m) => m.name));
}
// Cost estimate — mirrors cli/menu.py estimate_cost so web and terminal agree.
function estimateCost(includeDeck) {
  const n = state.seated.size;
  let low = 1.5 * n + 14, high = 4.0 * n + 36;
  if (includeDeck) { low += 3; high += 8; }
  return { low: Math.round(low), high: Math.round(high), deep: false };
}
function updateCount() {
  const n = state.seated.size;
  let html = `<b>${n}</b> agent${n === 1 ? "" : "s"} seated`;
  if (n > 0) html += ` &middot; <span class="est">${escapeHtml(
    councilModelMeta().provider === "openai" ? "ChatGPT plan" : "Claude plan"
  )}</span>`;
  $("#seated-count").innerHTML = html;
}
function estimateArgumentCost() {
  const hasDeep = state.argumentSeated.has("deep-research");
  const n = state.argumentSeated.size - (hasDeep ? 1 : 0);
  let low = 1.1 * n + 7, high = 3.2 * n + 22;
  if ($("#a-pptx")?.checked) { low += 3; high += 9; }
  return { low: Math.round(low), high: Math.round(high), deep: hasDeep };
}
function updateArgumentCount() {
  const n = state.argumentSeated.size, e = estimateArgumentCost();
  let html = `<b>${n}</b> agent${n === 1 ? "" : "s"} seated`;
  if (n) html += ` &middot; est. <span class="est">$${e.low}–$${e.high}</span>`;
  if (e.deep) html += ` <span class="est-note">+ Deep Research on your ChatGPT plan</span>`;
  $("#argument-seated-count").innerHTML = html;
}

function sourceHeaders(extra = {}) {
  return {
    "x-council-session": state.sessionToken,
    "x-council-client": state.clientId,
    ...extra,
  };
}
function setupSourceUploader(purpose) {
  const ui = SOURCE_UI[purpose], dropzone = $(ui.dropzone), fileInput = $(ui.input);
  dropzone.onclick = () => fileInput.click();
  dropzone.onkeydown = (e) => {
    if (e.key === "Enter" || e.key === " ") { e.preventDefault(); fileInput.click(); }
  };
  fileInput.onchange = () => { uploadSourceFiles(purpose, fileInput.files); fileInput.value = ""; };
  ["dragenter", "dragover"].forEach((name) => dropzone.addEventListener(name, (e) => {
    e.preventDefault(); dropzone.classList.add("dragging");
  }));
  ["dragleave", "drop"].forEach((name) => dropzone.addEventListener(name, (e) => {
    e.preventDefault(); dropzone.classList.remove("dragging");
  }));
  dropzone.addEventListener("drop", (e) => uploadSourceFiles(purpose, e.dataTransfer.files));
}
function updateSourceControls() {
  if ($("#scope-launch")) {
    $("#scope-launch").disabled = !state.authOk || state.sourceUploading.scope > 0 || !state.sourceUploads.scope.length;
  }
  if ($("#argument-launch")) {
    $("#argument-launch").disabled = !state.authOk || state.sourceUploading.argument > 0;
  }
  if ($("#wiz-next") && state.step === 3) {
    $("#wiz-next").disabled = !councilModelReady() || state.sourceUploading.report > 0;
  }
}
function renderSourceFiles(purpose) {
  const root = $(SOURCE_UI[purpose].list); root.innerHTML = "";
  state.sourceUploads[purpose].forEach((file) => {
    const row = document.createElement("div"); row.className = "source-file";
    row.innerHTML = `<div><b>${escapeHtml(file.name)}</b><span>${escapeHtml(file.size || file.status || "")}</span></div>`;
    const remove = document.createElement("button"); remove.type = "button"; remove.className = "source-file-remove"; remove.textContent = "Remove";
    remove.onclick = () => removeSourceFile(purpose, file.token);
    row.appendChild(remove); root.appendChild(row);
  });
  if (state.sourceUploading[purpose]) {
    const pending = document.createElement("div"); pending.className = "source-file pending";
    pending.textContent = `Uploading ${state.sourceUploading[purpose]} file${state.sourceUploading[purpose] === 1 ? "" : "s"}…`;
    root.appendChild(pending);
  }
  updateSourceControls();
  if (purpose === "report" && state.step === 3) buildReview();
}
async function uploadSourceFiles(purpose, fileList) {
  const files = Array.from(fileList || []);
  if (!files.length) return;
  state.sourceUploading[purpose] += files.length; renderSourceFiles(purpose);
  for (const file of files) {
    try {
      if (file.size > 40 * 1024 * 1024) throw new Error(`${file.name} exceeds the 40 MB file limit.`);
      const query = new URLSearchParams({ purpose, name: file.name });
      const res = await fetch(`/api/source?${query}`, {
        method: "POST", headers: sourceHeaders({ "content-type": "application/octet-stream" }), body: file,
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || `Could not upload ${file.name}.`);
      state.sourceUploads[purpose].push(data);
    } catch (error) {
      alert(error.message || String(error));
    } finally {
      state.sourceUploading[purpose] -= 1; renderSourceFiles(purpose);
    }
  }
}
async function removeSourceFile(purpose, token) {
  try {
    const query = new URLSearchParams({ purpose, token });
    const res = await fetch(`/api/source?${query}`, {
      method: "DELETE", headers: sourceHeaders(),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Could not remove the file.");
    state.sourceUploads[purpose] = state.sourceUploads[purpose].filter((file) => file.token !== token);
    renderSourceFiles(purpose);
  } catch (error) { alert(error.message || String(error)); }
}
function clearSourceFiles(purpose) {
  state.sourceUploads[purpose] = [];
  state.sourceUploading[purpose] = 0;
  renderSourceFiles(purpose);
}
function launchArgument() {
  const title = $("#a-title").value.trim();
  const argumentText = $("#a-text").value.trim();
  if (!title) { $("#a-title").focus(); $("#a-title").style.borderColor = "var(--red)"; return; }
  if (!argumentText && !state.sourceUploads.argument.length) {
    $("#a-text").focus(); flash($(".argument-required-note"), "Paste text or attach a document."); return;
  }
  if (!state.argumentSeated.size) { flash($("#argument-seated-count"), "Seat at least one agent."); return; }
  const wantPptx = $("#a-pptx").checked;
  const slideCount = Number($("#a-slide-count").value);
  if (wantPptx && (!Number.isInteger(slideCount) || slideCount < 3 || slideCount > 30)) {
    $("#a-slide-count").focus(); $("#a-slide-count").style.borderColor = "var(--red)"; return;
  }
  startRun({
    type: "start", mode: "strengthen", title,
    argument_text: argumentText, research_goal: $("#a-goal").value.trim(),
    audience: $("#a-audience").value.trim(), agents: Array.from(state.argumentSeated),
    source_tokens: state.sourceUploads.argument.map((file) => file.token),
    want_pptx: wantPptx, slide_count: wantPptx ? slideCount : null,
    budget: readBudget("#a-budget"),
  });
}

// ─────────── launch ───────────
function launchNew() {
  const current = promptFormSnapshot();
  startRun({
    type: "start", mode: "new",
    spec: { title: $("#f-title").value.trim() || $("#f-thesis").value.trim().slice(0, 60), thesis: $("#f-thesis").value.trim(),
      scope: linesOf($("#f-scope").value), avoid: linesOf($("#f-avoid").value), output_format: state.selectedFormat,
      operator_context: current.operator_context,
      decision_frame_enabled: decisionFrameEnabled(),
      decision_required: current.decision_required, decision_owner: current.decision_owner,
      time_horizon: current.time_horizon, approval_path: current.approval_path,
      success_measure: current.success_measure,
      agents: Array.from(state.seated), want_pptx: $("#f-pptx").checked,
      council_model: selectedCouncilModel(),
      deck_mode: $("#f-deck-mode").value,
      source_tokens: state.sourceUploads.report.map((file) => file.token) },
    auto_approve: !$("#f-review").checked, budget: readBudget("#f-budget"),
  });
}

function readBudget(selector) {
  const raw = $(selector).value.trim();
  if (raw === "") return null;
  const value = Number(raw);
  return Number.isFinite(value) && value >= 0 ? value : null;
}
function authenticatedControl(payload) {
  return {
    ...payload,
    client_id: state.clientId,
    session_token: state.sessionToken,
  };
}
function sendControl(payload) {
  if (state.ws?.readyState === WebSocket.OPEN) {
    state.ws.send(JSON.stringify(authenticatedControl(payload)));
  }
}
function startRun(payload) {
  if (!state.sessionToken) {
    alert("The local Council session could not be authenticated. Reload the app and try again.");
    return;
  }
  nav("run");
  $("#side-run").classList.remove("hidden");
  $("#sr-fill").style.width = "0%"; $("#sr-cost").textContent = "Starting…"; $("#sr-stage").textContent = "Starting…";
  $("#activity-log").innerHTML = "";
  $("#tm-evidence").textContent = "—"; $("#tm-artifacts").textContent = "0";
  $("#tm-gaps").textContent = "—"; $("#tm-gate").textContent = "Pending";
  state.validatedArtifacts = 0;
  state.validatedArtifactPaths = new Set();
  state.lastEventSeq = 0;
  $("#run-title").textContent = payload.spec?.title || payload.title || payload.slug || "Council run";
  buildStageRail(); resetConstellation(payload.spec?.title || payload.title || payload.slug || "");
  state.runFinished = false;
  state.reconnectAttempt = 0;
  openSocket(payload);
}

// Connect, and keep connecting. A long run outlives browser crashes, sleeping
// laptops, and network blips; the server keeps a sequenced event log, so
// rejoining costs only the events this tab actually missed.
function openSocket(payload) {
  const proto = location.protocol === "https:" ? "wss" : "ws";
  const query = new URLSearchParams({
    token: state.sessionToken,
    client_id: state.clientId,
  });
  const ws = new WebSocket(`${proto}://${location.host}/ws?${query}`);
  state.ws = ws;
  state.lastPayload = payload;
  ws.onopen = () => {
    state.reconnectAttempt = 0;
    ws.send(JSON.stringify(authenticatedControl(payload)));
  };
  ws.onmessage = (ev) => handleEvent(JSON.parse(ev.data));
  ws.onclose = () => {
    if (state.runFinished) return;
    scheduleReconnect();
  };
}

function scheduleReconnect() {
  const attempt = (state.reconnectAttempt || 0) + 1;
  state.reconnectAttempt = attempt;
  if (attempt > 60) {
    log("Lost contact with the Council server. Reload once it is running again.", "err");
    setConnectionBanner("Disconnected — reload when the server is back.", "err");
    return;
  }
  const delay = Math.min(1000 * attempt, 5000);
  setConnectionBanner(`Reconnecting to the run… (attempt ${attempt})`, "warn");
  log(`Connection lost — reconnecting in ${Math.round(delay / 1000)}s…`, "warn");
  setTimeout(async () => {
    // Rejoin the live run from the last event this tab rendered. If the run
    // ended while we were away, fall back to the finished report.
    try {
      const meta = await fetch("/api/meta").then((r) => r.json());
      if (!meta.active_run) { await recoverFinishedRun(); return; }
    } catch (_) { /* server still down — the socket attempt will retry */ }
    openSocket({ type: "attach", after: state.lastEventSeq || 0 });
  }, delay);
}

async function recoverFinishedRun() {
  state.runFinished = true;
  setConnectionBanner("", "");
  log("The run finished while this tab was disconnected.", "ok");
  await loadHome();
  nav("home");
}

// A run has exactly one controlling tab. Extra tabs watch. If the controlling
// tab dies, the server hands control to the next tab that attaches, so a
// crashed browser can never strand a run at an unapprovable checkpoint.
function applyControlStatus(e) {
  const observing = !e.controls && e.run_active;
  document.body.dataset.observing = observing ? "1" : "";
  const cancel = $("#cancel-btn");
  if (cancel) cancel.disabled = observing;
  let note = $("#cp-observing");
  if (observing) {
    if (!note) {
      note = document.createElement("div");
      note.id = "cp-observing";
      note.className = "cp-observing";
      $("#cp-actions")?.parentElement?.insertBefore(note, $("#cp-actions"));
    }
    note.textContent = e.message || "Another tab is controlling this run.";
  } else if (note) {
    note.remove();
  }
}

function setConnectionBanner(text, kind) {
  let el = $("#conn-banner");
  if (!text) { if (el) el.remove(); return; }
  if (!el) {
    el = document.createElement("div");
    el.id = "conn-banner";
    el.className = "conn-banner";
    document.body.appendChild(el);
  }
  el.textContent = text;
  el.dataset.kind = kind || "warn";
}

// ─────────── stage rail ───────────
const STAGES = ["Research", "Synthesis & debate", "Edit & verify", "Produce"];
function buildStageRail(labels) {
  const rail = $("#stage-rail"); rail.innerHTML = "";
  (labels || STAGES).forEach((label, i) => { const node = document.createElement("div"); node.className = "stage-node"; node.dataset.stage = i + 1;
    node.innerHTML = `<div class="stage-dot"></div><div class="stage-label">${escapeHtml(label)}</div>`; rail.appendChild(node); });
}
function setStage(n) { $$(".stage-node").forEach((node) => { const sn = +node.dataset.stage; node.classList.toggle("active", sn === n); node.classList.toggle("done", sn < n); }); }

// ─────────── constellation ───────────
function svg(tag, attrs = {}) { const el = document.createElementNS(NS, tag); for (const [k, v] of Object.entries(attrs)) el.setAttribute(k, v); return el; }
function initials(d) { const w = d.replace(/[()]/g, "").split(/\s+/).filter(Boolean); return w.length === 1 ? w[0].slice(0, 3).toUpperCase() : w.slice(0, 3).map((x) => x[0]).join("").toUpperCase(); }
function resetConstellation(title) {
  const root = $("#constellation"); root.innerHTML = ""; constellation.nodes = {}; constellation.svg = root;
  const defs = svg("defs"); const grad = svg("radialGradient", { id: "coreGrad", cx: "50%", cy: "42%", r: "62%" });
  grad.appendChild(svg("stop", { offset: "0%", "stop-color": "#8b83f4" })); grad.appendChild(svg("stop", { offset: "55%", "stop-color": "#4f46e5" })); grad.appendChild(svg("stop", { offset: "100%", "stop-color": "#312e81" }));
  defs.appendChild(grad); root.appendChild(defs);
  const stars = svg("g");
  for (let i = 0; i < 46; i++) { const x = Math.random() * 800, y = Math.random() * 560; if (Math.hypot(x - CX, y - CY) < 80) continue;
    const s = svg("circle", { class: "star", cx: x.toFixed(0), cy: y.toFixed(0), r: (Math.random() * 1.3 + 0.4).toFixed(1), opacity: (Math.random() * 0.4 + 0.15).toFixed(2) });
    s.style.animation = `twinkle ${(Math.random() * 4 + 3).toFixed(1)}s ease-in-out ${(Math.random() * 4).toFixed(1)}s infinite`; stars.appendChild(s); }
  root.appendChild(stars);
  root.appendChild(svg("circle", { class: "deco-ring r1", cx: CX, cy: CY, r: OUTER_RX - 6 }));
  root.appendChild(svg("circle", { class: "deco-ring r2", cx: CX, cy: CY, r: INNER_RX - 6 }));
  root.appendChild(svg("g", { id: "beam-layer" })); root.appendChild(svg("g", { id: "node-layer" }));
  const core = svg("g");
  core.appendChild(svg("circle", { class: "core-ring spin", cx: CX, cy: CY, r: 62 }));
  core.appendChild(svg("circle", { class: "core-orb", cx: CX, cy: CY, r: 46 }));
  const t1 = svg("text", { class: "core-label", x: CX, y: CY - 2 }); t1.textContent = "THESIS";
  const t2 = svg("text", { class: "core-sub", x: CX, y: CY + 16 }); t2.textContent = (title || "").slice(0, 16);
  core.appendChild(t1); core.appendChild(t2); root.appendChild(core);
}
function flyEvidence(node) {
  const root = constellation.svg; if (!root) return;
  const dot = svg("circle", { class: "evidence", r: 4, cx: node.x, cy: node.y }); root.appendChild(dot);
  const t0 = performance.now(), dur = 750;
  (function fr(t) { const p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3);
    dot.setAttribute("cx", node.x + (CX - node.x) * e); dot.setAttribute("cy", node.y + (CY - node.y) * e);
    dot.setAttribute("opacity", (1 - p * 0.7).toFixed(2)); dot.setAttribute("r", (4 - p * 2).toFixed(1));
    if (p < 1) requestAnimationFrame(fr); else dot.remove(); })(t0);
}
function placeNode(name) {
  if (constellation.nodes[name]) return constellation.nodes[name];
  const meta = state.meta[name] || { display: name }; const isProc = name in PROCESS_SLOTS; let x, y;
  if (isProc) { const a = (PROCESS_SLOTS[name] * Math.PI) / 180; x = CX + INNER_RX * Math.cos(a); y = CY + INNER_RY * Math.sin(a); }
  else { const arr = state._researchOrder || []; const idx = arr.indexOf(name); const total = arr.length || 1;
    const a = (idx / total) * 2 * Math.PI - Math.PI / 2; x = CX + OUTER_RX * Math.cos(a); y = CY + OUTER_RY * Math.sin(a); }
  const beam = svg("line", { class: "beam", x1: CX, y1: CY, x2: x, y2: y }); $("#beam-layer").appendChild(beam);
  const g = svg("g", { class: "cnode queued appearing", transform: `translate(${x},${y})` }); setTimeout(() => g.classList.remove("appearing"), 600);
  g.appendChild(svg("circle", { class: "pulse", r: 22, cx: 0, cy: 0 }));
  g.appendChild(svg("circle", { class: "ring", r: 21, cx: 0, cy: 0 }));
  const gl = svg("text", { class: "glyph", x: 0, y: 0 }); gl.textContent = initials(meta.display || name); g.appendChild(gl);
  const lbl = svg("text", { class: "clabel", x: 0, y: 34 }); lbl.textContent = (meta.display || name).slice(0, 16); g.appendChild(lbl);
  const cost = svg("text", { class: "ccost", x: 0, y: 47 }); g.appendChild(cost);
  g.addEventListener("mouseenter", (e) => showTip(e, meta)); g.addEventListener("mouseleave", hideTip);
  $("#node-layer").appendChild(g);
  const node = { g, beam, cost, x, y }; constellation.nodes[name] = node; return node;
}
function buildConstellation(names) { state._researchOrder = names.filter((n) => !(n in PROCESS_SLOTS)); state._researchOrder.forEach((n) => placeNode(n)); }
function nodeState(name, cls) { const n = placeNode(name); n.g.classList.remove("queued", "running", "done", "error"); n.g.classList.add(cls);
  if (cls === "running") n.beam.classList.add("active"); else n.beam.classList.remove("active");
  if (cls === "done") n.beam.classList.add("delivered"); else n.beam.classList.remove("delivered"); }
function showTip(e, meta) {
  const tip = $("#node-tooltip"); tip.innerHTML = `<div class="nt-name">${escapeHtml(meta.display || "")}</div><div class="nt-desc">${escapeHtml(meta.description || "")}</div>`;
  const wrap = $(".constellation-wrap").getBoundingClientRect();
  tip.style.left = (e.clientX - wrap.left + 14) + "px"; tip.style.top = (e.clientY - wrap.top + 10) + "px"; tip.classList.remove("hidden");
}
function hideTip() { $("#node-tooltip").classList.add("hidden"); }

// ─────────── events ───────────
function handleEvent(e) {
  if (e.seq && e.seq <= (state.lastEventSeq || 0)) return;
  if (e.seq) state.lastEventSeq = e.seq;
  // Any delivered event proves the connection is healthy again.
  if (state.reconnectAttempt) { state.reconnectAttempt = 0; setConnectionBanner("", ""); }
  switch (e.type) {
    case "control_status":
      state.hasControl = Boolean(e.controls);
      applyControlStatus(e);
      return;
    case "run_start":
      state.runBilling = e.billing || "provider_subscriptions";
      if (e.stages) buildStageRail(e.stages);
      buildConstellation(e.agents || []);
      $("#run-title").textContent = e.title || e.slug || "Council run";
      $("#sr-cost").textContent = `${planLabel() || "Subscription"} usage`;
      log("Council convened: " + e.title, "ok"); break;
    case "preflight":
      log("✓ Preflight passed · authentication, document rendering, and storage ready", "ok"); break;
    case "deliverable_done":
      log(`📦 ${e.id} — ${e.title} → ${e.file}  (${e.done}/${e.total})`, "ok");
      $("#run-stage").textContent = `Building deliverables · ${e.done} of ${e.total} complete`;
      $("#sr-fill").style.width = (45 + Math.round((e.done / e.total) * 45)) + "%";
      break;
    case "stage_start":
      setStage(e.stage); $("#run-stage").textContent = `Stage ${e.stage} · ${e.label}`;
      $("#sr-stage").textContent = `Stage ${e.stage} · ${e.label}`; $("#sr-fill").style.width = (STAGE_FILL[e.stage] || 50) + "%";
      log(`▸ Stage ${e.stage}: ${e.label}`); break;
    case "agent_start": nodeState(e.agent, "running"); log(`▶ ${e.display || e.agent} started · ${modelShort(e.model)}`); break;
    case "agent_tool": if (e.target) log(`  ${e.tool}: ${shortPath(e.target)}`); break;
    case "agent_done": {
      const billedOn = planLabel(e.billing) || planLabel();
      const subscription = Boolean(billedOn);
      const separatelyBilled = e.billed_separately || e.cost == null;
      const costLabel = subscription ? billedOn : (separatelyBilled ? "separate billing" : "$" + Number(e.cost).toFixed(2));
      const node = constellation.nodes[e.agent]; if (node) { node.cost.textContent = subscription ? "plan" : (separatelyBilled ? "separate" : costLabel); flyEvidence(node); }
      nodeState(e.agent, "done"); $("#sr-cost").textContent = subscription ? `${billedOn} usage` : "Run $" + Number(e.total || 0).toFixed(2);
      log(`✓ ${state.meta[e.agent]?.display || e.agent} — ${costLabel}`, "ok"); break;
    }
    case "artifact_validated":
      if (!state.validatedArtifactPaths) state.validatedArtifactPaths = new Set();
      {
        const artifactKey = e.path || e.artifact || e.step || `event-${e.seq || 0}`;
        if (e.valid === false) state.validatedArtifactPaths.delete(artifactKey);
        else state.validatedArtifactPaths.add(artifactKey);
        state.validatedArtifacts = state.validatedArtifactPaths.size;
        $("#tm-artifacts").textContent = state.validatedArtifacts;
      }
      log(`${e.valid === false ? "⚠" : "✓"} Artifact validated · ${e.path || e.artifact || e.label || "output"}${e.word_count != null ? ` · ${e.word_count} words` : ""}`, e.valid === false ? "warn" : "ok"); break;
    case "evidence_update":
      $("#tm-evidence").textContent = e.record_count ?? "—";
      $("#tm-gaps").textContent = (e.agents_without_evidence || []).length;
      log(`◈ Evidence ledger · ${e.record_count ?? e.count ?? e.records ?? "updated"} records${e.invalid_record_count ? ` · ${e.invalid_record_count} invalid` : ""}`, e.invalid_record_count ? "warn" : "ok"); break;
    case "quality_gate":
      $("#tm-gate").textContent = e.passed ? "Passed" : "Failed";
      $("#tm-gate").className = e.passed ? "tm-pass" : "tm-fail";
      log(`${e.passed ? "✓" : "⚠"} Publishing gate · ${e.passed ? "passed" : "failed"} · ${e.error_count || 0} error(s), ${e.warning_count || 0} warning(s)`, e.passed ? "ok" : "err"); break;
    case "render_qa":
      log(`▣ Visual QA · ${e.status || "complete"}${e.issues != null ? ` · ${e.issues} issue(s)` : ""}`, e.status === "failed" ? "err" : "ok"); break;
    case "manifest_update": {
      const selectedCount = Array.isArray(e.selected_agents)
        ? e.selected_agents.length
        : Number(e.selected_agents || 0);
      log(`▤ Run manifest · ${selectedCount} research agents · ${e.artifact_count ?? 0} artifacts`, "ok"); break;
    }
    case "phase_start":
      log(`◇ ${e.label || e.phase}`); break;
    case "research_swarm_start":
      log(`⚡ Parallel research swarm · ${e.total} agents · ${e.concurrency}-wide`); break;
    case "research_swarm_complete":
      log(`✓ Research swarm complete · ${e.total} briefs`, "ok"); break;
    case "agent_retry":
      nodeState(e.agent, "running");
      log(`↻ ${state.meta[e.agent]?.display || e.agent} retry ${e.attempt || ""}/${e.max_attempts || ""}${e.delay_seconds ? ` in ${e.delay_seconds}s` : ""} · ${e.reason || "transient error"}`, "warn"); break;
    case "agent_skipped":
      nodeState(e.agent, "done"); log(`↷ ${state.meta[e.agent]?.display || e.agent} resumed from ${shortPath(e.path || "")}`); break;
    case "agent_error":
      nodeState(e.agent, "error");
      log(`✕ ${state.meta[e.agent]?.display || e.agent} — ${e.message || e.error_type || "agent failed"}`, "err"); break;
    case "checkpoint": showCheckpoint(e); break;
    case "checkpoint_skipped":
      log(`↷ ${e.kind || "Checkpoint"} approval restored for unchanged artifacts`, "ok"); break;
    case "checkpoint_invalidated":
      $("#checkpoint-overlay").classList.add("hidden");
      log(`↻ ${e.kind || "Checkpoint"} inputs changed · rebuilding verified work before review`, "warn"); break;
    case "run_complete": state.runFinished = true; setConnectionBanner("", ""); showResult(e); break;
    case "control_error":
      log("Control denied: " + e.message, "err"); break;
    case "run_error": log("Error: " + e.message, "err"); alert("The run hit an error:\n\n" + e.message + "\n\nCompleted work is saved — resume from Home."); loadHome(); break;
    case "run_stopped":
      state.runFinished = true; setConnectionBanner("", "");
      log("Run stopped.", "warn"); $("#side-run").classList.add("hidden"); break;
    case "stream_end": state.runFinished = true; setConnectionBanner("", ""); state.ws?.close(); break;
  }
}
function log(text, cls = "") {
  const line = document.createElement("div"); line.className = "log-line " + cls;
  const t = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
  line.innerHTML = `<span class="lt">${t}</span>${escapeHtml(text)}`;
  const l = $("#activity-log"); l.appendChild(line); l.scrollTop = l.scrollHeight;
}

// ─────────── checkpoint ───────────
function showCheckpoint(e) {
  state.currentCheckpoint = e; $("#cp-title").textContent = e.title; $("#cp-subtitle").textContent = e.subtitle;
  const tabs = $("#cp-tabs"), content = $("#cp-content"); tabs.innerHTML = "";
  e.documents.forEach((doc, i) => { const tab = document.createElement("div"); tab.className = "cp-tab" + (i === 0 ? " active" : ""); tab.textContent = doc.name;
    tab.onclick = () => { $$(".cp-tab").forEach((t) => t.classList.remove("active")); tab.classList.add("active"); content.innerHTML = renderMarkdown(doc.content); content.scrollTop = 0; }; tabs.appendChild(tab); });
  content.innerHTML = renderMarkdown(e.documents[0]?.content || "");
  const rubric = $("#cp-rubric"); rubric.innerHTML = "";
  if ((e.rubric || []).length) {
    rubric.innerHTML = `<div class="cp-rubric-title">Quick quality signal <span>optional · 1 weak, 5 exceptional</span></div>` +
      e.rubric.map((r) => `<label>${escapeHtml(r.label)}<select data-rating="${escapeHtml(r.key)}">
        <option value="">—</option><option value="1">1</option><option value="2">2</option>
        <option value="3">3</option><option value="4">4</option><option value="5">5</option>
      </select></label>`).join("");
    rubric.classList.remove("hidden");
  } else rubric.classList.add("hidden");
  const notes = $("#cp-notes"); notes.classList.add("hidden"); notes.value = "";
  const actions = $("#cp-actions"); actions.innerHTML = "";
  const defs = { continue: { label: "Approve → continue", cls: "primary" }, approve: { label: "Approve → produce documents", cls: "primary" }, redo: { label: "Redo with notes", cls: "warn" }, clear: { label: "Clear old outputs → start", cls: "warn" }, abort: { label: "Stop the run", cls: "ghost" } };
  e.actions.forEach((a) => { const btn = document.createElement("button"); btn.className = "cp-btn " + (defs[a]?.cls || "ghost"); btn.textContent = defs[a]?.label || a;
    btn.onclick = () => { if (a === "redo" && notes.classList.contains("hidden")) { notes.classList.remove("hidden"); notes.focus(); btn.textContent = "Submit redo"; return; }
      const ratings = {}; $$("[data-rating]").forEach((s) => { if (s.value) ratings[s.dataset.rating] = Number(s.value); });
      sendControl({ type: "checkpoint", id: e.id, action: a, notes: notes.value.trim(), ratings }); $("#checkpoint-overlay").classList.add("hidden");
      log(a === "redo" ? "Redo requested." : a === "abort" ? "Aborted." : "Checkpoint approved.", a === "abort" ? "warn" : "ok"); };
    actions.appendChild(btn); });
  $("#checkpoint-overlay").classList.remove("hidden");
}

// ─────────── writing guide ───────────
async function openGuide() {
  $("#guide-overlay").classList.remove("hidden");
  if (!state.guideMd) {
    try {
      const data = await fetch("/api/guide").then((r) => r.json());
      state.guideMd = data.markdown || "";
    } catch (_) { state.guideMd = "Could not load the guide. See docs/writing-effective-run-prompts.md in the repo."; }
  }
  const body = $("#guide-body");
  body.innerHTML = renderMarkdown(state.guideMd);
  body.scrollTop = 0;
}

// ─────────── revise / result ───────────
function openReviseModal(slug) { state.reviseSlug = slug; $("#revise-target").textContent = slug; $("#revise-feedback").value = ""; $("#revise-overlay").classList.remove("hidden"); }
function submitRevise() { const f = $("#revise-feedback").value.trim(); if (!f) { $("#revise-feedback").focus(); return; } $("#revise-overlay").classList.add("hidden"); startRun({ type: "start", mode: "revise", slug: state.reviseSlug, feedback: f, auto_approve: false }); }
async function showResult(e) {
  setStage(5); state.resultSlug = e.slug; state.resultMode = e.mode || "report";
  state.resultReviseSlug = e.revise_slug || e.slug;
  $("#side-run").classList.add("hidden");
  $("#result-badge").textContent = "✓ Complete"; $("#result-title").textContent = e.title;
  $("#result-cost").textContent = planLabel()
    ? `${planLabel()} usage · archived to ${e.archive || "runs/"}`
    : `Total cost $${(e.total || 0).toFixed(2)} · archived to ${e.archive || "runs/"}`;
  if (e.mode === "scope") {
    $("#result-new").textContent = "New report";
    $("#result-revise").classList.add("hidden");
    $("#result-deck").classList.add("hidden");
    $("#result-quality").classList.add("hidden");
    // Engagement result: the deliverable manifest + the zip.
    let md = `# Deliverables\n\n`;
    (e.deliverables || []).forEach((d) => { md += `- **${d.id}** — ${d.title} (\`${d.file}\`)\n`; });
    md += `\nAll files are in \`reports/scope-${e.slug}/\` alongside the QA report and manifest. `;
    md += `AI-produced engagement materials — subject-matter-expert review required before client delivery.`;
    $("#result-body").innerHTML = renderMarkdown(md);
    $("#result-toc").innerHTML = "";
    const dl = $("#result-downloads"); dl.innerHTML = "";
    if (e.zip) { const a = document.createElement("a"); a.className = "dl-btn"; a.href = e.zip; a.textContent = "⤓ All deliverables (.zip)"; dl.appendChild(a); }
    clearSourceFiles("scope");
    await loadHome(); nav("result"); return;
  }
  if (e.mode === "strengthen") {
    $("#result-revise").classList.add("hidden");
    $("#result-deck").classList.add("hidden");
    $("#result-quality").classList.add("hidden");
    $("#result-new").textContent = "Strengthen another argument";
    try {
      const data = await fetch(`/api/report/${e.slug}`).then((r) => r.json());
      $("#result-body").innerHTML = renderMarkdown(data.markdown || "");
      buildTOC(); renderDownloads(data.downloads);
    } catch (_) { $("#result-body").textContent = "One-page memo saved to the library."; }
    clearSourceFiles("argument");
    await loadHome(); nav("result"); return;
  }
  $("#result-new").textContent = "New report";
  $("#result-revise").classList.remove("hidden");
  $("#result-deck").classList.toggle("hidden", e.mode === "revision");
  $("#result-quality").classList.remove("hidden");
  try { const data = await fetch(`/api/report/${e.slug}`).then((r) => r.json()); state.resultReviseSlug = data.revise_slug || state.resultReviseSlug; $("#result-body").innerHTML = renderMarkdown(data.markdown || ""); buildTOC(); renderDownloads(data.downloads); }
  catch (_) { $("#result-body").textContent = "Report saved to runs/."; }
  clearSourceFiles("report");
  await loadHome(); nav("result");
}
async function saveFinalQuality() {
  if (!state.resultSlug) return;
  const ratings = {};
  $$("[data-final-rating]").forEach((s) => {
    if (s.value) ratings[s.dataset.finalRating] = Number(s.value);
  });
  const status = $("#result-quality-status");
  if (!Object.keys(ratings).length) {
    status.textContent = "Choose at least one score.";
    return;
  }
  status.textContent = "Saving…";
  try {
    const res = await fetch(`/api/review/${encodeURIComponent(state.resultSlug)}`, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "x-council-session": state.sessionToken,
        "x-council-client": state.clientId,
      },
      body: JSON.stringify({
        ratings,
        notes: $("#result-quality-notes").value.trim(),
      }),
    });
    if (!res.ok) throw new Error("save failed");
    status.textContent = "Saved.";
  } catch (_) {
    status.textContent = "Could not save.";
  }
}
function renderDownloads(downloads) { const dl = $("#result-downloads"); dl.innerHTML = ""; (downloads || []).forEach((d) => { const a = document.createElement("a"); a.className = "dl-btn"; a.href = d.url; a.textContent = "⤓ " + d.label; dl.appendChild(a); }); }
function buildTOC() {
  const toc = $("#result-toc"); toc.innerHTML = "";
  const heads = $$("#result-body h1, #result-body h2, #result-body h3");
  heads.forEach((h, i) => { const id = "h-" + i; h.id = id; const a = document.createElement("a"); a.href = "#" + id; a.textContent = h.textContent;
    if (h.tagName === "H3") a.className = "h3"; a.onclick = (ev) => { ev.preventDefault(); h.scrollIntoView({ behavior: "smooth", block: "start" }); }; toc.appendChild(a); });
  if (!heads.length) toc.innerHTML = `<span class="muted" style="font-size:12px;">—</span>`;
}

// ─────────── helpers ───────────
function linesOf(t) { return t.split("\n").map((s) => s.replace(/^[-*•]\s*/, "").trim()).filter(Boolean); }
function shortPath(p) { const x = String(p).split("/"); return x.length > 2 ? ".../" + x.slice(-2).join("/") : p; }
function escapeHtml(s) { return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])); }
function normalizeAgentProfileMarkdown(markdown) {
  const out = [];
  let inFence = false;
  const structural = (line) => /^(?:#{1,4}\s+|[-*]\s+|\d+[.)]\s+|>\s?|\|.*\|\s*$|---\s*$|\*\*\*\s*$|\[\^\d+\]:)/.test(line.trimStart());
  String(markdown || "").split("\n").forEach((raw) => {
    const line = raw.replace(/\s+$/, "");
    const trimmed = line.trim();
    if (/^```/.test(trimmed)) {
      inFence = !inFence;
      out.push(line);
      return;
    }
    if (inFence || !trimmed) {
      out.push(line);
      return;
    }
    const previous = out[out.length - 1] || "";
    const previousIsList = /^(?:[-*]\s+|\d+[.)]\s+)/.test(previous.trimStart());
    if (previous.trim() && !structural(line) && (!structural(previous) || previousIsList)) {
      out[out.length - 1] = `${previous.trimEnd()} ${trimmed}`;
      return;
    }
    out.push(line);
  });
  return out.join("\n");
}
function renderMarkdown(md, options = {}) {
  if (!md) return "";
  // Readers never see internal provenance tags from older runs.
  if (options.stripInternal !== false) {
    md = md.replace(/\s?\[[^\]]*\b(?:brief|Stage\s*1)\b[^\]]*\]/gi, "");
  }
  // Footnote definitions become a Notes section; markers become superscripts.
  const notes = [];
  md = md.split("\n").filter((ln) => {
    const m = ln.trim().match(/^\[\^(\d+)\]:\s*(.*)$/);
    if (m) { notes.push([m[1], m[2]]); return false; }
    return true;
  }).join("\n");
  const lines = md.replace(/<!--[\s\S]*?-->/g, "").split("\n");
  let html = "", listTag = null, inQuote = false, i = 0;
  const inline = (t) => escapeHtml(t).replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>").replace(/(^|[^*])\*([^*]+)\*/g, "$1<em>$2</em>").replace(/`([^`]+)`/g, "<code>$1</code>").replace(/\[\^(\d+)\]/g, '<sup class="fn">$1</sup>');
  const cl = () => { if (listTag) { html += `</${listTag}>`; listTag = null; } };
  const ol = (tag) => { if (listTag !== tag) { cl(); html += `<${tag}>`; listTag = tag; } };
  const cq = () => { if (inQuote) { html += "</blockquote>"; inQuote = false; } };
  const cells = (row) => row.replace(/^\||\|$/g, "").split("|").map((c) => c.trim());
  while (i < lines.length) {
    const line = lines[i].replace(/\s+$/, ""); let m;
    if (/^```/.test(line.trim())) {
      cl(); cq();
      const code = [];
      i += 1;
      while (i < lines.length && !/^```/.test(lines[i].trim())) { code.push(lines[i]); i += 1; }
      if (i < lines.length) i += 1;
      html += `<pre class="md-code"><code>${escapeHtml(code.join("\n"))}</code></pre>`;
      continue;
    }
    // Tables: a | row followed by a |---| separator row.
    if (line.startsWith("|") && i + 1 < lines.length && /^\|[\s:\-|]+\|?\s*$/.test(lines[i + 1])) {
      cl(); cq();
      const head = cells(line); i += 2;
      let body = "";
      while (i < lines.length && lines[i].trim().startsWith("|")) { body += "<tr>" + cells(lines[i]).map((c) => `<td>${inline(c)}</td>`).join("") + "</tr>"; i++; }
      html += `<table class="md-table"><thead><tr>${head.map((c) => `<th>${inline(c)}</th>`).join("")}</tr></thead><tbody>${body}</tbody></table>`;
      continue;
    }
    if ((m = line.match(/^(#{1,4})\s+(.*)$/))) { cl(); cq(); html += `<h${m[1].length}>${inline(m[2])}</h${m[1].length}>`; }
    else if (/^(---|\*\*\*)\s*$/.test(line)) { cl(); cq(); html += "<hr />"; }
    else if ((m = line.match(/^[-*]\s+\[([ xX])\]\s+(.*)$/))) { cq(); ol("ul"); html += `<li>${m[1].trim() ? "☑" : "☐"} ${inline(m[2])}</li>`; }
    else if ((m = line.match(/^[-*]\s+(.*)$/))) { cq(); ol("ul"); html += `<li>${inline(m[1])}</li>`; }
    else if ((m = line.match(/^\d+[.)]\s+(.*)$/))) { cq(); ol("ol"); html += `<li>${inline(m[1])}</li>`; }
    else if ((m = line.match(/^>\s?(.*)$/))) { cl(); if (!inQuote) { html += "<blockquote>"; inQuote = true; } html += inline(m[1]) + " "; }
    else if (line.trim() === "") { cl(); cq(); } else { cl(); cq(); html += `<p>${inline(line)}</p>`; }
    i++;
  }
  cl(); cq();
  if (notes.length) {
    html += `<div class="notes"><div class="notes-h">Notes</div>`;
    notes.forEach(([n, t]) => { html += `<div class="note"><sup>${n}</sup> ${inline(t)}</div>`; });
    html += `</div>`;
  }
  return html;
}
init().then(() => {
  $("#app-loading").classList.add("hidden");
}).catch((error) => {
  console.error(error);
  $("#app-loading").classList.add("failed");
  $("#app-loading-title").textContent = "The Council could not load";
  $("#app-loading-detail").textContent = "Refresh the page. If the problem continues, check the Council terminal.";
});
