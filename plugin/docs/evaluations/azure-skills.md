# Evaluation: azure-skills

**Repo:** [microsoft/azure-skills](https://github.com/microsoft/azure-skills)
**Stars:** 1,220 | **Last updated:** 2026-06-18 (pushed; created 2026-02-26) | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Outer loop — Ship (deploy/validate) and Operate (diagnostics, monitoring, cost, compliance). Touches inner-loop Implement only for Azure-SDK wiring; its center of gravity is the cloud-operations end of the loop, not writing application code.
**Layer:** Tooling + Infrastructure — a packaged capability layer that pairs guidance *skills* (the "brain") with the Azure MCP Server and Foundry MCP (the "hands") that reach live Azure resources.

---

## What it does

Microsoft's official Azure agent plugin. The README frames Azure work as "a decision problem" — which service fits, what to validate before deploy, which guardrails matter — and packages **three layers in one install**: (1) **68 SKILL.md skills** (28 distinct skill directories, several with deep `references/`, `examples/`, and step-by-step `steps/` subtrees), (2) the **Azure MCP Server** advertising "200+ structured tools across 40+ Azure services" for live resource inventory, pricing, log queries, and diagnostics, and (3) **Foundry MCP** for Microsoft Foundry model discovery, deployment, and agent workflows. `.mcp.json` wires the execution layer; `plugin.json` (v1.1.71) declares it as a marketplace plugin named `azure`.

The skill set spans the operational arc: build/deploy/evolve (`azure-prepare`, `azure-validate`, `azure-deploy`, `azure-upgrade`, `azure-kubernetes`, `airunway-aks-setup`), troubleshoot/monitor/govern (`azure-diagnostics`, `appinsights-instrumentation`, `azure-compliance`, `azure-resource-lookup`, `azure-quotas`), optimize/cost (`azure-cost`, `azure-compute`, `azure-resource-visualizer`, `azure-cloud-migrate`), and data/AI/identity (`azure-ai`, `azure-aigateway`, `azure-storage`, `azure-kusto`, `azure-messaging`, `azure-rbac`, `entra-app-registration`, `entra-agent-id`, `microsoft-foundry`). It is explicitly **multi-host** — installable via Microsoft's APM (`apm install microsoft/azure-skills`) across GitHub Copilot, Claude Code, Cursor, OpenCode, Codex, and Gemini, with per-host hook configs (`copilot-hooks.json`, `cursor-hooks.json`, `hooks.json`) and a telemetry hook (`track-telemetry.sh`/`.ps1`).

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** Nothing was installed, no MCP server was started, no `az login` performed, and no skill activated. There is no Azure subscription in this environment, so the "200+ tools / 40+ services" and "258K installs" figures are the authors' README/marketplace claims, not anything observed. Every statement below comes from repository metadata, README, the recursive file tree, and `plugin.json`.

```bash
gh api repos/microsoft/azure-skills --jq '{desc,stars:.stargazers_count,forks:.forks_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'
gh api repos/microsoft/azure-skills/readme --jq '.content' | base64 -d | head -120
gh api "repos/microsoft/azure-skills/git/trees/HEAD?recursive=1" --jq '[.tree[]|select(.path|endswith("SKILL.md"))]|length'   # 68
gh api "repos/microsoft/azure-skills/git/trees/HEAD?recursive=1" --jq '.tree[].path' | grep -oE 'skills/[^/]+/SKILL.md' | sort -u   # 28 distinct dirs
gh api repos/microsoft/azure-skills/commits  --jq 'length'    # 30 (page-1 cap)
gh api repos/microsoft/azure-skills/releases --jq 'length'    # 19
gh api repos/microsoft/azure-skills/contents/.claude-plugin/plugin.json --jq '.content' | base64 -d   # v1.1.71, skills + mcpServers
```

## What worked

- **Vendor-authoritative and actively released.** First-party Microsoft, MIT-licensed, **19 tagged releases** at v1.1.71 — this is a maintained, versioned product, not a hobby skill dump. The release cadence and CODEOWNERS suggest ongoing official support.
- **Skill + MCP pairing is the right shape for cloud work.** The README's "brain vs hands" framing is sound: skills supply the decision trees and guardrails (what to validate before deploy, when to use which service), and the Azure MCP Server gives the agent live read/act tools instead of hallucinated `az` commands. This is meaningfully better than a prompt pack that only *describes* Azure.
- **Depth where it counts.** Several skills ship structured `references/`, `examples/` (e.g. `appinsights.bicep`), and ordered `steps/` subtrees (e.g. `airunway-aks-setup` has step-1 through step-6 plus troubleshooting). This is far past one-paragraph skills — it encodes real runbooks.
- **Genuinely multi-host.** APM-driven install across six harnesses with per-host hook configs makes the same Azure capability portable, not Claude-only.
- **Operational breadth.** Cost, quotas, RBAC, compliance, diagnostics, and migration cover the unglamorous govern/operate work most skill packs ignore.

## What didn't work or surprised us

- **Hard infrastructure prerequisites gate everything.** Requires an Azure subscription, Node 18+ for `npx`-launched MCP servers, `az login`, and `azd auth login` for deploy flows. Outside an Azure shop this plugin does nothing — the value is entirely conditional on already being on Azure.
- **Ships a telemetry hook.** `track-telemetry.sh`/`.ps1` runs on hook events. For a first-party Microsoft plugin this is unsurprising, but it is host-side script execution phoning home, which teams with egress/telemetry policies must review and likely disable before install.
- **Large live-tool surface = large blast radius.** "200+ tools across 40+ services" with credentials that can list, price, and *act on* real Azure resources is powerful and risky. RBAC scoping of the `az login` identity is the only thing standing between the agent and production infrastructure; the plugin doesn't constrain that for you.
- **Scope is narrow by design.** Every skill is Azure-specific. Zero relevance to non-Azure projects — this is the opposite of a general dev-loop skill pack.
- **Unverifiable headline metrics.** "258K installs" and "200+ tools" are marketing/marketplace numbers; nothing in the repo substantiates them, and none were exercised here.
- **Two Microsoft skill repos invite confusion.** It overlaps in name and origin with `microsoft/skills` (SDK *coding* patterns) — easy to install the wrong one. They are complementary, not interchangeable (see Verdict).

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + (Azure only) | Decision-tree skills plus live MCP tools reduce hallucinated `az`/Bicep and wrong-service choices; the agent can verify resource state instead of guessing. Zero effect off Azure. |
| Speed | + | Pre-built deploy/diagnose/cost runbooks and a 60-second multi-host install short-circuit the research-and-glue phase of Azure tasks. |
| Maintainability | neutral / + | Versioned (19 releases) and vendor-maintained, so the skills track Azure's API drift better than a static pack; no direct effect on your application's maintainability. |
| Safety | − (review required) | Live credentialed MCP tools that can act on production Azure, plus a telemetry hook. Safety depends entirely on RBAC scoping of the login identity and on auditing/disabling telemetry. |
| Cost Efficiency | + / − | `azure-cost`/`azure-quotas` skills actively target cloud spend (real savings); offset by extra token cost of large skill+tool context and the per-call latency of MCP round-trips. |

## Verdict

**CONDITIONAL — adopt if and only if you ship on Azure; otherwise SKIP.** azure-skills is the strongest *shape* of cloud skill pack in this catalog: first-party, versioned (v1.1.71, 19 releases), multi-host, and crucially pairing guidance skills with a live MCP execution layer rather than just prose. For an Azure team it is close to ADOPT for the Ship/Operate stages. But it is rigidly Azure-scoped, demands a subscription and authenticated CLIs, ships a telemetry hook, and hands the agent a large credentialed tool surface — so the conditions (Azure shop + RBAC-scoped identity + telemetry reviewed) are load-bearing, and it is worthless to anyone not on Azure.

Compared to neighbors: it is the operations counterpart to **microsoft/skills** (which teaches Azure-*SDK coding* patterns — Implement stage); install both for an Azure dev shop, neither alone is complete. **google/skills** is the analogous GCP/Workspace vendor pack; **gemini-skills** the Gemini-ecosystem one — all three are domain-locked and only earn their keep inside their vendor's cloud. Against general packs like **agent-skills** or **mattpocock/skills**, azure-skills trades breadth for depth and live execution: it does one cloud's operations work very well and everything else not at all.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [azure-skills](https://github.com/microsoft/azure-skills) | plugin | Official Microsoft Azure plugin pairing 68 decision-tree skills with the Azure + Foundry MCP servers (live tools across 40+ services) for deploy, diagnose, govern, and cost work — multi-host via APM | Need an agent that does real Azure operations (deploy/diagnose/cost/RBAC) with live tooling instead of generic cloud advice | microsoft/skills (Azure SDK *coding*), google/skills, gemini-skills (vendor cloud packs) |
