# Plan 012: Software-factory survey — six platforms, one methodology doc (#272)

> **Executor instructions**: Follow step by step; verify each step. On any
> STOP condition, stop and report. Update this plan's row in `plans/README.md`
> when done.
>
> **Drift check (run first)**: `git diff --stat 1bb538f..HEAD -- methodologies/ evaluations/8090-software-factory.md evaluations/pr-agent.md sync-plugin-docs.sh`
> On drift, re-verify "Current state" before proceeding.

## Status

- **Priority**: P2
- **Effort**: M
- **Risk**: LOW (one new doc + README row + two follow-up issues; no code, no catalog rows, no verdicts)
- **Depends on**: none
- **Category**: docs / methodology
- **Planned at**: commit `1bb538f`, 2026-07-11, via `make-plan` from [issue #272](https://github.com/mattbutlerengineering/ai-tooling/issues/272)
- **Research basis**: four web-research subagent reports (primary sources read 2026-07-11); the per-platform fact sheets in Step 3 are their consolidated output. Source URLs are inlined so the doc can be written without redoing the research.

## Why this matters

Issue #272 asks: evaluate six "software factory" platforms (factory.ai, 8090.ai, tembo.io, EY.ai, Qodo, Planview Software Product Delivery), document features/functionality and what each does well, and derive the ideal workflow. **The deliverable is one md file.** Per [ADR-0003](../docs/adr/0003-methodologies-directory.md), external-methodology writeups live in `methodologies/` — auto-synced to the plugin, exempt from catalog drift detectors (no counts, verdicts, or Evidence fields). The repo already has deep 8090 coverage; this doc is the *category survey* that positions all six against our [inner/outer dev loop](../WORKFLOW.md) and says which ideas the ideal workflow steals from which platform.

The research also surfaced **stale facts in existing docs** (8090 availability + pipeline names; pr-agent org/license). Correcting evaluations means re-verification passes — out of scope here; this plan files them as follow-up issues.

## Current state

- **Existing 8090/EY coverage** (do not duplicate — link): `evaluations/8090-software-factory.md` (verdict SKIP, Last verified 2026-06-29), `evaluations/software-factory-plugin.md`, `methodologies/8090-software-factory-sdlc.md`, `methodologies/intent-to-production-recipe.md`.
- **Qodo partial coverage**: `qodo-cover` CATALOG row; `evaluations/pr-agent.md` says "the commercial Qodo 2.0 offering is a fork/superset; the OSS tool is independent" — now stale (see Step 6).
- **Zero coverage**: factory.ai, tembo.io, Planview (only an incidental "Factory Droid" mention in the flow-next CATALOG row).
- **Stale facts found 2026-07-11** (basis for Step 6 follow-ups, and MUST be reflected accurately in the new doc):
  1. 8090 is now **self-serve at $200/user/mo** (factory.8090.ai + public `/pricing`; 8090 Enterprise "Starting at $1M/yr") — the eval's "no self-serve trial, unevaluable hands-on" is no longer true. $135M Series A announced 2026-06-29 (Salesforce Ventures-led; Palihapitiya full-time CEO).
  2. 8090's marketed pipeline is now **5 core modules: Requirements, Blueprints, Work Orders, Tests, Feedback** — "Development" dropped as a named module (execution is "IDE / Agent of choice — no lock-in", BYO coding agent), "Validator" renamed to Feedback. Our methodology doc records the old shape.
  3. **pr-agent transferred out of qodo-ai** to community org [The-PR-Agent/pr-agent](https://github.com/The-PR-Agent/pr-agent) (12,053★); current LICENSE is **MIT (c) 2026 The PR Agent** (was recorded as Apache-2.0 under qodo-ai); README: "community-maintained legacy project of Qodo… not the Qodo free tier"; docs moved to docs.pr-agent.ai.

## Commands you will need

| Purpose | Command | Expected |
|---------|---------|----------|
| Full gate | `make check` | exit 0 |
| Sync only | `./sync-plugin-docs.sh` | exit 0; mirrors `methodologies/` → `plugin/docs/methodologies/` |
| Follow-up issues | `gh issue create --title … --body … --label ready-for-agent` | issue URL |
| Link check (manual) | `grep -o '](\.\./[^)]*' methodologies/software-factories.md` | every relative target exists |

## Scope

**In scope**:
- `methodologies/software-factories.md` (create — the deliverable of #272)
- `plans/README.md` (add row 012)
- Two follow-up issues via `gh` (8090 refresh; pr-agent org/license fact fix)
- `plugin/` via sync only

**Out of scope** (do NOT do these here):
- New CATALOG.md rows, COMPARISON.md rows, or `evaluations/*.md` files for factory.ai / tembo / Qodo-platform / Planview — these are closed commercial platforms; a survey doc is what #272 asks for. If a later hands-on eval is wanted (8090 is now $200 self-serve; factory.ai from $20; tembo has a free tier), that's the follow-up issue's call.
- Editing `evaluations/8090-software-factory.md`, `evaluations/pr-agent.md`, or `methodologies/8090-software-factory-sdlc.md` — verdict/fact changes require their own re-verification pass (Last-verified discipline). File the issues instead.
- WORKFLOW.md / STACK.md changes.

## Git workflow

- Branch: `advisor/012-software-factories`
- Commit: `docs(methodologies): software-factory survey — six platforms, ideal workflow (#272)`

## Steps

### Step 1: Documentation discovery (read before writing)

Read, in this order:
1. `methodologies/8090-software-factory-sdlc.md` + `methodologies/intent-to-production-recipe.md` — the house style for methodology docs (stage table mapped to our loop, honest "where we diverge" section) and the existing 8090 mapping the new doc must link to, not restate.
2. `evaluations/8090-software-factory.md` — the "Source-grounded review — not run hands-on" framing and vendor-claim discipline to copy.
3. `WORKFLOW.md` (Inner Loop `Plan → Implement → Verify → Review → Ship` + `Reflect`; outer loop `Discover/Architect/Decompose/Retrospect` sections) — the stage vocabulary the synthesis maps onto.
4. Spot-check currency of the highest-risk external facts (the web moves; research date was 2026-07-11): `https://factory.ai/news/software-factory`, `https://www.8090.ai/pricing`, `https://www.qodo.ai/` (hero positioning), `https://www.tembo.io/`. If any contradicts a Step 3 fact sheet, prefer the live page and note the correction in the doc.

**Verify**: you can state from memory (a) the six inner/outer loop stage names, (b) the 8090 five-module pipeline (new names), (c) which of the six platforms writes code vs. governs it.

**Anti-pattern guards**: do not skip the spot-check and trust this plan's fact sheets blind — they are research output, not scripture.

### Step 2: Create `methodologies/software-factories.md` — frame and skeleton

Header block copying the house style of `8090-software-factory-sdlc.md:1-4`: a "**What this is:**" paragraph stating this is a source-grounded survey (read, not run) of six commercial "software factory" platforms, produced for [#272], with research date 2026-07-11 and a pointer to the existing 8090 docs for depth on that platform.

Then a category definition section: a *software factory* = a system that turns continuous inbound signals (intent, tickets, alerts, feedback) into shipped, validated software through a pipeline of agent-executed stages, each emitting a durable, traceable artifact, under human oversight. Note the term is used at three altitudes by the six vendors — **code-side factory** (factory.ai, 8090), **agent orchestration layer** (tembo), **verification/governance layer** (Qodo), **portfolio/VSM layer** (Planview), **services wrapper** (EY) — this taxonomy is the doc's organizing spine.

Sections (H2): one per platform (order: factory.ai, 8090+EY.ai combined or adjacent, tembo.io, Qodo, Planview), then "Stage-coverage matrix", then "The ideal workflow", then "Sources".

**Verify**: file exists; H2 skeleton matches; header links to `8090-software-factory-sdlc.md`, `intent-to-production-recipe.md`, and issue #272 resolve.

**Anti-pattern guards**: no verdicts, Evidence fields, or star-count tables — this is a methodologies doc, not an eval (ADR-0003 exempts it from detectors precisely because it carries none).

### Step 3: Write the six platform sections

Each section = **What it is** (2-3 sentences) · **Pipeline** (named modules → artifacts, as a table or tight list) · **What it does well** (3-6 bullets) · **Openness** (OSS components / self-serve / gated) · vendor claims quoted only with explicit "vendor claim, unverified" flags. Write from the fact sheets below; cite the listed primary URLs inline.

#### 3a. factory.ai (Factory)

- **Is**: agent-native development platform; one model-agnostic agent brand **Droid** (CLI, desktop/web app, IDEs, Slack, CI via `droid exec`); since "Factory 2.0" (2026-06-15, factory.ai/news/software-factory) the umbrella is the **Software Factory**: a 24/7 automation layer across the SDLC. Self-serve $20/$100/$200/mo; enterprise on-prem/air-gapped; closed-source core (README: "All rights reserved"), small OSS periphery (factory-plugins, droid-action, legacy-bench).
- **Pipeline**: Signals → **Triage** (classify/dedupe/route inbound tickets, alerts, feedback) → **Code-gen** (Droid sessions; Missions multi-agent orchestration; Specification Mode plan-first) → **Validate** (Automated Code Review; STRIDE-based Security Review; Droid Control browser/terminal QA) → **Release** (weakest stage — "as they become available" per vendor's own table) → **Document** (AutoWiki, CI-refreshed) → **Monitor** (Incident Response: alert → autonomous RCA, incidents correlate back to causing PRs).
- **Does well**: widest surface coverage (interactive/headless/persistent Droid Computers); true model-agnosticism (native multi-vendor catalog + BYOK + Factory Router + Mixed Models); **Agent Readiness Model** — scores repos for autonomy-readiness with `/readiness-fix` remediation (no competitor documents this formally); tiered autonomy (`droid exec` read-only by default, `--auto low|medium|high`); benchmark-forward culture (Terminal-Bench 63.1% vendor-claimed but on third-party leaderboard; Legacy-Bench is vendor-authored — flag both).
- **Sources**: factory.ai/, docs.factory.ai/welcome + /pricing.md + /web/software-factory.md + /models.md + /features/missions/overview.md + /cli/droid-exec/overview.md + /benchmarks/*, factory.ai/news/software-factory, github.com/factory-ai.
- **Guard**: the 2024 taxonomy "Code Droid / Knowledge Droid / Reliability Droid / Product Droid" is HISTORICAL — absent from all current docs. One Droid + Custom Droids (subagents) + per-stage Automations. Homepage dashboard numbers ("57k lines/day", "98.7% pass rate") are an animated mockup, not metrics.

#### 3b. 8090.ai + EY.ai PDLC (adjacent sections or one combined section — executor's call, but keep them distinguishable)

- **8090**: link-first — the depth lives in `evaluations/8090-software-factory.md` and `methodologies/8090-software-factory-sdlc.md`. This section carries only (a) a two-sentence summary, (b) the **2026-07 delta**: pipeline now marketed as 5 core modules **Requirements, Blueprints, Work Orders, Tests, Feedback** (Development de-named — "IDE / Agent of choice, no lock-in"; "Forward + backward pass" context propagation; "Multi-Player Collaboration"); **self-serve $200/user/mo** via factory.8090.ai (Enterprise "Starting at $1M/yr"); $135M Series A 2026-06-29 (Salesforce Ventures-led, Palihapitiya full-time CEO). Note explicitly the existing eval predates these facts and a refresh issue is filed (Step 6).
- **EY.ai PDLC**: consulting offering (launched 2026-03-18) — EY provides methodology, consultants, delivery teams; **the engine IS 8090 Software Factory** ("Built on 8090"); EY names no modules of its own. Adds: transformation consulting, Responsible-AI governance framing, delivery capacity, "open ecosystem" promise. Fully sales-gated, no pricing. Claims "80x faster / 70% productivity / 95%+ coverage" come from **one unnamed internal EY US use case** — quote as vendor claims.
- **Sources**: 8090.ai/ + /pricing + /software-factory + /blog/series-a; ey.com service page + 2026-03-18 press release.
- **Guard**: do not restate the old Requirements→Blueprints→Work Orders→Development→Validator shape as current; do not present EY.ai as an independent platform.

#### 3c. tembo.io (Tembo)

- **Is**: cloud **orchestration layer for third-party coding agents** — runs Claude Code, Codex, Cursor, OpenCode, Amp, Pi in isolated cloud sandboxes, triggered from Slack/Linear/Jira/GitHub/Sentry/schedules/webhooks; returns reviewable PRs, human-only merge. Explicitly NOT another proprietary coding agent. Pivoted from managed Postgres 2025-05-05 (vendor blog). Free tier (1 repo, OSS models); $60/$200/mo; self-hosted NixOS appliance; **zero public repos** — legacy OSS (pgmq) spun out.
- **Pipeline**: **Sessions** (Plan → Execute in sandbox → Verify: runs *your* tests/builds → Review → Ship, human-gated) · **Agents** (scheduled + event-driven automations from templates; `@tembo` macros) · **Reviews** (PR review with inline comments) · **Feedback Loop** (iterate on its PRs via review comments) · Sandbox/Snapshots/Hooks/`tembo.nix`.
- **Does well**: harness/model agnosticism as the thesis (per-task agent/model switching, BYOK); **production-telemetry-to-PR loop** (Sentry webhook → stack-trace analysis → fix PR, deduped); meet-devs-where-they-are triggering with live logs streamed back into Slack/Linear/PR threads; every session runs repo tests before output; serious self-hosted story for a young pivot.
- **Sources**: tembo.io/ + /agents + /pricing + /customers, docs.tembo.io (features/agents.md, integrations/sentry.md, resources/pricing.md, features/self-hosted/overview.md), tembo.io/blog/autonomous-software-maintenance-has-arrived, github.com/tembo-io (empty).
- **Guard**: no requirements/PRD or deploy automation — do not credit it with front-of-loop or ship-stage coverage. Customer metrics ("98% dep upgrades automated", "16% of PRs") are vendor-page claims, unverified. Datadog/PostHog appear only in the pricing table, not docs — unconfirmed.

#### 3d. Qodo

- **Is**: **AI code review and governance platform** — "the layer between AI wrote it and production". Formally deprecated its code generation (CEO post 2026-04-23: "the tool generating code should not be the same tool reviewing it") and repositioned as the independent verification layer over code from ANY agent. 14-day self-serve trial, Pro Team ~$30 + credits, no permanent free tier; enterprise on-prem/air-gapped/BYOK.
- **Pipeline**: **Qodo Code Review v2** (multi-agent PR review: critical-issue, duplicated-logic, ticket-compliance, standards agents) · **Code Governance / Rules System** (**Rule Miner** turns PR-comment history into enforceable rules with provenance; rule health + analytics) · **Cross-Repository Review** (beta: auto-discovered repo relationships, breaking-change detection across repos AND Git providers) · **Qodo IDE plugin** (local pre-PR review; ex-"Qodo Gen") · **Agent Skills** (MIT `qodo-ai/qodo-skills`: qodo-get-rules, qodo-pr-resolver — inject org rules into third-party coding agents) · **Context Engine** (ex-"Aware": multi-repo retrieval substrate, MCP/API) · Command + Cover (de-emphasized, legacy doc paths).
- **Does well**: independent-verification stance (architecturally clean role in a multi-vendor AI SDLC); self-learning standards loop (Rule Miner); cross-repo impact analysis pre-merge; same rules enforced on every surface (IDE, in-agent via skills, PR); governance system-of-record for leaders; published reproducible benchmark (HuggingFace `Qodo/PR-Review-Bench`) — self-serving but auditable.
- **Sources**: qodo.ai/ + /pricing + /ai-code-review-platform + /ai-code-review-benchmark + codegen-deprecation blog; docs.qodo.ai (llms.txt, whats-new, agent-skills, on-prem); github.com/qodo-ai; github.com/The-PR-Agent/pr-agent.
- **Guard**: the lineup "Qodo Gen / Merge / Cover / Command / Aware" is OBSOLETE — Gen→IDE plugin (codegen removed), Merge→legacy v1 name, Aware→Context Engine, Command/Cover demoted. pr-agent no longer lives under qodo-ai and is MIT under The-PR-Agent (Step 6 files the eval fix). "Highest F1" is Qodo's own benchmark. Marquee features (cross-repo, self-learning, custom agentic workflows) are Enterprise-only — say so.

#### 3e. Planview Software Product Delivery

- **Is**: one of five named solutions on Planview's portfolio platform — a **strategy-and-visibility layer that "sits above the tools where work happens"** (Jira/ADO/GitHub/ServiceNow). VSM + lean-agile portfolio governance: it does not write software; it funds, plans, governs, measures, and traces it. Buyer: Office of the CTO/CPO, EPMO. Fully proprietary, sales-gated, no public pricing.
- **Pipeline** (capability areas, verbatim from the solution page): Planning & Funding · Financials · Team Delivery · Toolchain Integration (60+ connectors, common data model) · Performance Analytics (Flow Framework® flow metrics + DORA) · Governance & Compliance (cross-tool traceability for audits) · **Planview Anvi™** AI layer (formerly Copilot, rebranded Oct 2025): custom agents, **Outcome Intelligence Graph** (2026-06-16), Connected Work Graph, **Anvi MCP server** (external agents can query the portfolio graph), **Agent Resource Management** — AI agents governed as first-class capacity alongside humans. Mark the SKU composition (Viz/AgilePlace/Hub/Portfolios ± Release/Verify) as [INFERENCE] — the solution page never enumerates SKUs.
- **Does well**: toolchain-neutral visibility; Flow Framework pedigree (Tasktop/Kersten lineage); **investment-to-outcome traceability** — ties features and *AI-agent spend* to the OKR they were funded to move (the sharpest differentiator vs. every code-side platform); agentic-era governance ahead of peers (agents as governed capacity; MCP surface).
- **Sources**: planview.com/products-solutions/solutions/digital-product-development/ (the SPD page), planview.com/ai/, newsroom.planview.com 2026-06-16 release, planview.com/products-solutions/.
- **Guard**: implement/verify/ship stages are deliberately NOT owned — do not describe it as a code factory. Customer outcomes (Huntington "32% revenue growth", Vanguard "75% fewer major incidents") and analyst placements are vendor-published.

**Verify (whole step)**: each section has all four blocks; every vendor metric in the doc carries a "vendor claim"/"unverified" flag or [INFERENCE] marker (`grep -in "80x\|95%\|98%\|63.1\|F1\|32% revenue" methodologies/software-factories.md` — every hit sits in flagged context); every named module traces to a URL listed in the section's sources.

### Step 4: Stage-coverage matrix

One table: rows = the six platforms; columns = Requirements/Intent · Plan/Architecture · Implement · Verify/Review · Ship/Release · Operate/Feedback · Portfolio/Funding. Cell values: ✓ core / ~ partial / ✗ delegated-or-absent, with a word of nuance (e.g. tembo Ship = "human-gated merge only"; factory.ai Release = "weakest stage, vendor's own admission"; Planview Implement = "observes flow only"; Qodo Ship = "merge gate only"). The matrix is the evidence base the ideal-workflow section argues from — it must show that no single platform covers all columns and that the six cluster into the taxonomy from Step 2.

**Verify**: matrix present; every ✓/~/✗ consistent with the platform sections above it (no cell contradicting its section's prose).

### Step 5: "The ideal workflow" synthesis

The section #272 exists for. Structure:

1. **Derivation** — what the six converge on despite different altitudes. From the research, the convergent skeleton is: *continuous signal intake* (factory.ai Triage; tembo triggers; 8090 Feedback) → *intent captured as durable, traceable artifacts before code* (8090 Requirements/Blueprints; EY intent-driven front; factory.ai Specification Mode) → *codebase-tied work units* (8090 Work Orders) → *BYO/model-agnostic execution* (8090's own de-naming of Development; tembo's whole thesis; factory.ai BYOK/Router) → *independent, multi-dimensional verification* (Qodo's generation/review separation; factory.ai Validate; tembo sandbox test runs) → *human-gated ship* (universal: no platform auto-merges) → *production telemetry closing the loop* (factory.ai Monitor/Incident→PR correlation; tembo Sentry→PR) → all bound by *a traceability spine* (8090 knowledge graph; Qodo rules provenance; Planview cross-tool traceability) and — the layer only Planview adds — *portfolio governance treating agents as funded, measured capacity*.
2. **Distinctive ideas worth stealing, one line each, attributed**: Agent Readiness maturity scoring (factory.ai); tiered autonomy defaults (factory.ai `droid exec`); generation/verification separation of powers (Qodo); rules mined from review history with provenance (Qodo); telemetry-to-PR reflex arc (tembo); tests as a first-class pipeline module (8090); agents as governed capacity with outcome accounting (Planview).
3. **Mapping to our loop** — a table mapping each ideal-workflow stage onto the inner/outer loop stages and the catalogued skills that fill them today, in the exact style of `8090-software-factory-sdlc.md:20-31`; link `intent-to-production-recipe.md` as the runnable open-tool assembly rather than restating it.
4. **Honest gaps** — what none of our open tools replicate (auto-propagating artifact graph, agents-as-funded-capacity accounting, cross-repo pre-merge impact analysis), in the style of the existing "Where we diverge" sections.

**Verify**: every claim in the derivation names at least one platform section as its source (internal consistency — no idea appears here that has no home above); the mapping table's skill links resolve to real files.

**Anti-pattern guards**: the ideal workflow is *derived from the survey*, not this repo's WORKFLOW.md restated with new labels — the derivation must cite the platforms, and divergences from our current loop (e.g. portfolio layer, readiness scoring: things WORKFLOW.md lacks) must be stated, not smoothed over.

### Step 6: File the two follow-up issues

1. `gh issue create --title "Refresh 8090 Software Factory eval: self-serve pricing, Series A, renamed module pipeline" --label ready-for-agent` — body: the three deltas from "Current state" with source URLs; note the SKIP rationale ("no self-serve access, unevaluable hands-on") is partially invalidated at $200/user/mo, so the refresh may warrant a hands-on re-evaluation decision; affected files `evaluations/8090-software-factory.md`, `methodologies/8090-software-factory-sdlc.md`, CATALOG row.
2. `gh issue create --title "pr-agent moved to The-PR-Agent org; license now MIT — update eval" --label ready-for-agent` — body: transfer facts + LICENSE quote from "Current state"; affected files `evaluations/pr-agent.md`, CATALOG row.

**Verify**: both issue URLs exist; each cross-references #272.

### Step 7: Sync, gate, README row

1. `./sync-plugin-docs.sh` — mirrors the new file into `plugin/docs/methodologies/`.
2. `make check` → exit 0.
3. Add row 012 to `plans/README.md` (status DONE with date + this issue link, matching the table's existing format).
4. Comment on #272 linking the doc and both follow-up issues (do not close unless you have permission conventions say otherwise — the issue author closes).

**Verify**: `git status` shows the new file, its plugin mirror, and README change only (plus nothing else unexpected); `make check` exit 0.

## Test plan

No unit-testable surface. Verification = per-step checks + `make check` (guards plugin sync integrity; ADR-0003 confirms methodology docs carry no detector-gated fields).

## Done criteria

- [ ] `methodologies/software-factories.md` exists with six platform sections, stage-coverage matrix, and ideal-workflow synthesis
- [ ] Every vendor metric flagged; Planview SKU mapping marked [INFERENCE]; obsolete taxonomies (2024 Droids, Qodo Gen/Merge/Aware, old 8090 pipeline) absent or explicitly marked historical
- [ ] Two follow-up issues filed and cross-referenced to #272
- [ ] `./sync-plugin-docs.sh` mirrored the doc; `make check` → exit 0
- [ ] `plans/README.md` row 012 added; #272 commented with links

## STOP conditions

- Step 1 spot-check contradicts a fact sheet on something structural (a platform repositioned again, a pipeline renamed) → update the affected section from the live source and note the correction; if more than two platforms have drifted structurally, stop and report — the research basis is stale.
- You feel pulled to edit `evaluations/8090-software-factory.md` or `evaluations/pr-agent.md` "while you're in there" → stop; that work is the follow-up issues' scope (Last-verified discipline).
- `make check` fails on something unrelated to your change → stop and report; do not fix drive-by.

## Maintenance notes

- The doc records "research date 2026-07-11"; these vendors pivot fast (three of six repositioned within the last 14 months). The staleness sweep will not gate it (methodologies are exempt), so revisit when a follow-up issue or scan touches any of the six.
- If the 8090 refresh (follow-up 1) changes the module names in `8090-software-factory-sdlc.md`, the survey's 8090 section stays consistent automatically only if it links rather than restates — keep it link-first.
