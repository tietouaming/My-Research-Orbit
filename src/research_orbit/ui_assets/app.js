const stateUrl = "/api/state";

const formatLabel = (value) =>
  String(value)
    .replaceAll("_", " ")
    .replaceAll("-", " ")
    .replace(/\b\w/g, (match) => match.toUpperCase());

const text = (value, fallback = "-") => {
  if (value === null || value === undefined || value === "") {
    return fallback;
  }
  return String(value);
};

const el = (tag, className, content) => {
  const node = document.createElement(tag);
  if (className) {
    node.className = className;
  }
  if (content !== undefined) {
    node.textContent = content;
  }
  return node;
};

async function loadState() {
  const response = await fetch(stateUrl, { headers: { Accept: "application/json" } });
  if (!response.ok) {
    throw new Error(`Failed to load UI state: ${response.status}`);
  }
  return response.json();
}

function renderSummary(summary) {
  document.getElementById("metric-workflows").textContent = text(summary.workflow_count);
  document.getElementById("metric-providers").textContent = text(summary.provider_count);
  document.getElementById("metric-cards").textContent = text(summary.memory_card_count);
  document.getElementById("metric-redaction").textContent = text(summary.redaction_finding_count);
}

function renderPaths(paths) {
  const list = document.getElementById("path-list");
  list.replaceChildren();
  Object.entries(paths).forEach(([key, value]) => {
    const row = el("div");
    row.append(el("dt", null, formatLabel(key)));
    row.append(el("dd", null, value));
    list.append(row);
  });
}

function renderWorkflows(workflows) {
  const list = document.getElementById("workflow-list");
  list.replaceChildren();
  workflows.forEach((workflow) => {
    const row = el("article", "workflow-row");
    const name = el("div");
    name.append(el("h4", null, workflow.name));
    name.append(el("p", null, `v${workflow.version}`));

    const detail = el("div");
    detail.append(el("p", null, workflow.description));
    const pills = el("div", "pill-row");
    workflow.provider_requirements.slice(0, 3).forEach((item) => {
      pills.append(el("span", "pill", item));
    });
    detail.append(pills);

    const steps = el("div");
    steps.append(el("h4", null, `${workflow.steps.length} steps`));
    steps.append(el("p", null, workflow.evidence_materials.slice(0, 2).join(", ")));

    row.append(name, detail, steps);
    list.append(row);
  });
}

function renderMemoryCards(cards) {
  const list = document.getElementById("memory-card-list");
  list.replaceChildren();
  cards.forEach((card) => {
    const node = el("article", "memory-card");
    node.append(el("h4", null, card.title));
    node.append(el("p", null, card.problem));
    const pills = el("div", "pill-row");
    [card.category, card.risk_level, card.verification_status].forEach((item) => {
      pills.append(el("span", "pill", item));
    });
    card.tags.slice(0, 4).forEach((tag) => {
      pills.append(el("span", "pill", tag));
    });
    node.append(pills);
    list.append(node);
  });
}

function renderProviders(providers) {
  const table = document.getElementById("provider-table");
  table.replaceChildren();
  providers.forEach((provider) => {
    const row = el("tr");
    row.append(el("td", null, provider.name));

    const statusCell = el("td");
    statusCell.append(
      el("span", `status ${provider.configured ? "ready" : "missing"}`, provider.configured ? "Ready" : "Needs env"),
    );
    row.append(statusCell);

    row.append(el("td", null, provider.required_env.length ? provider.required_env.join(", ") : "-"));
    row.append(el("td", null, provider.capability));
    table.append(row);
  });
}

function renderFindings(findings) {
  const list = document.getElementById("finding-list");
  list.replaceChildren();
  if (!findings.length) {
    list.append(el("div", "empty-state", "No suspicious sensitive patterns were detected in examples."));
    return;
  }
  findings.forEach((finding) => {
    const node = el("article", `finding ${finding.severity}`);
    node.append(el("h4", null, `${finding.severity.toUpperCase()} · ${finding.finding_type}`));
    node.append(el("p", null, `${finding.source_path}:${finding.line_number}`));
    node.append(el("p", null, finding.message));
    const pills = el("div", "pill-row");
    pills.append(el("span", "pill", finding.excerpt));
    node.append(pills);
    list.append(node);
  });
}

function markActiveNav() {
  const links = Array.from(document.querySelectorAll(".nav-item"));
  links.forEach((link) => {
    link.addEventListener("click", () => {
      links.forEach((item) => item.classList.remove("active"));
      link.classList.add("active");
    });
  });
}

async function main() {
  markActiveNav();
  try {
    const state = await loadState();
    renderSummary(state.summary);
    renderPaths(state.paths);
    renderWorkflows(state.workflows);
    renderMemoryCards(state.memory_cards);
    renderProviders(state.providers);
    renderFindings(state.redaction_findings);
  } catch (error) {
    document.querySelector(".workspace").prepend(el("div", "empty-state", error.message));
  }
}

main();
