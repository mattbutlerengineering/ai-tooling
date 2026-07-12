# Software factories — six platforms, one category, and the workflow they converge on

**What this is:** a source-grounded survey — **read, not run** — of six commercial platforms that market themselves as (or around) a *software factory*: [factory.ai](https://factory.ai/), [8090.ai](https://www.8090.ai/), [EY.ai PDLC](https://www.ey.com/en_us/services/consulting/ai-native-pdlc-reinventing-software-delivery), [tembo.io](https://www.tembo.io/), [Qodo](https://www.qodo.ai/), and [Planview Software Product Delivery](https://www.planview.com/products-solutions/solutions/digital-product-development/). Produced for [#272](https://github.com/mattbutlerengineering/ai-tooling/issues/272); research date **2026-07-11** (vendor pages read directly on that date; three of the six repositioned within the last 14 months, so expect drift). We did not install, log into, or run any of these platforms — every quantitative figure below is the vendor's claim, flagged as such. For depth on 8090 specifically, this doc links rather than restates: see the [8090 SDLC mapping](8090-software-factory-sdlc.md), the [open-skills recipe](intent-to-production-recipe.md), and the [evaluation](../evaluations/8090-software-factory.md).

## What a "software factory" is — and the five altitudes vendors sell it at

Across all six vendors, a *software factory* is a system that turns **continuous inbound signals** (intent, tickets, alerts, customer feedback) into **shipped, validated software** through a pipeline of agent-executed stages, each emitting a durable, traceable artifact, under human oversight. That definition is the common core; what differs is the altitude at which each vendor builds it:

| Altitude | What it owns | Platforms |
|---|---|---|
| **Code-side factory** | The full intent→code pipeline: specs, work units, execution, tests | factory.ai, 8090 |
| **Services wrapper** | Methodology + consultants around someone else's factory engine | EY.ai PDLC (engine: 8090) |
| **Agent orchestration layer** | Runs *other vendors'* coding agents in sandboxes, ticket→PR | tembo.io |
| **Verification / governance layer** | Reviews and governs code that *any* agent wrote; deliberately no codegen | Qodo |
| **Portfolio / VSM layer** | Funds, plans, measures, and traces delivery it deliberately does not perform | Planview |

This taxonomy is the doc's organizing spine: the six are mostly **complements, not competitors**, and the [stage-coverage matrix](#stage-coverage-matrix) below shows no single platform covers the whole lifecycle.

## factory.ai (Factory)

**What it is.** An "agent-native software development platform" whose single agent brand is **Droid** — one model-agnostic agent that runs in a CLI, a desktop/web app, IDEs, Slack, and CI (`droid exec` + GitHub Action). Since the "Factory 2.0" announcement ([2026-06-15](https://factory.ai/news/software-factory)) the umbrella product is the **Software Factory**: a 24/7 automation layer connecting agents across the whole SDLC with a self-improving feedback loop. Self-serve plans at $20/$100/$200/mo ([docs.factory.ai/pricing](https://docs.factory.ai/pricing.md)); enterprise runs on-prem/air-gapped. Note the 2024-era taxonomy of specialized "Code Droid / Knowledge Droid / Reliability Droid / Product Droid" is **historical** — it is absent from all current docs, collapsed into one Droid plus user-defined Custom Droids (subagents) and per-stage Automations.

**Pipeline** ([docs.factory.ai/web/software-factory](https://docs.factory.ai/web/software-factory.md); dashboard in private preview):

| Stage | What runs | Artifact |
|---|---|---|
| **Triage** | Classify/dedupe/route inbound signals (tickets, alerts, feedback) | Routed, triaged tickets |
| **Plan** | Specification Mode (plan-before-code), [Missions](https://docs.factory.ai/features/missions/overview.md) planning | Approved spec / mission plan |
| **Code-gen** | Droid sessions; Missions multi-agent orchestration; Custom Droids | Code changes / PRs |
| **Validate** | Automated Code Review; STRIDE-based Security Review; Droid Control browser/terminal QA | Review comments, security findings, QA evidence |
| **Release** | Deployment gates and ship workflows — "as they become available": the weakest stage by the vendor's own table | Releases |
| **Document** | AutoWiki, refreshed by CI on every push | Browsable repo wiki |
| **Monitor** | Incident Response: alert → autonomous RCA; incidents correlate back to the causing PR | Incident analyses, new signals |

**What it does well.**

- **Widest surface coverage** in the category: interactive (CLI/desktop/IDE), headless in CI ([`droid exec`](https://docs.factory.ai/cli/droid-exec/overview.md)), persistent remote machines (Droid Computers), Slack/Linear.
- **Model-agnosticism as a first-class feature**: native multi-vendor catalog ([docs.factory.ai/models](https://docs.factory.ai/models.md)), BYOK, Factory Router auto-selection, Mixed Models (different models for planning vs. execution).
- **Agent Readiness Model** — scores repos for autonomy-readiness with `/readiness-fix` remediation. No competitor in this survey documents a repo-maturity model this formally.
- **Tiered autonomy defaults**: `droid exec` is read-only unless escalated (`--auto low|medium|high`), failing fast on permission violations.
- **Verification depth**: user-level QA in real browsers/terminals (Droid Control), STRIDE/OWASP security review on PRs, secret scanning (Droid Shield).
- **Benchmark-forward culture**: publishes methodology pages and results — Terminal-Bench 2.0 63.1% (vendor-claimed, on a third-party leaderboard we did not independently confirm; [source](https://docs.factory.ai/benchmarks/terminal-bench.md)), and Legacy-Bench 42.5% (a **vendor-authored** benchmark Factory both designed and ranks first on — self-reported, though the harness is public).

**Openness.** Proprietary, closed-source core — the main GitHub repo ([Factory-AI/factory](https://github.com/Factory-AI/factory)) is a distribution/issue hub whose README reads "All rights reserved." Small OSS periphery (factory-plugins, droid-action, eslint-plugin, legacy-bench; licenses unverified). Fully self-serve individual plans; the Software Factory dashboard itself is private-preview, sales-gated.

**Flagged claims.** The homepage dashboard's throughput numbers ("57k lines of code/day", a "98.7% pass rate") are an **animated marketing mockup, not metrics**. Customer-outcome figures (e.g. "Empower decreased incident response times by 40%") are vendor case studies, unverified.

## 8090.ai (8090 Software Factory)

The depth on 8090 lives in this repo already — [evaluation](../evaluations/8090-software-factory.md) (source-grounded, verdict SKIP as of 2026-06-29) and the [stage-by-stage mapping to our loop](8090-software-factory-sdlc.md) — so this section is deliberately thin. In two sentences: 8090's Software Factory is an "AI-native SDLC control plane" that drives business intent to production code through a chain of modules that each emit a durable artifact, bound by a knowledge graph and an audit-trail control plane; its methodology is separately published as the MIT [software-factory-plugin](../evaluations/software-factory-plugin.md).

**What changed since our docs were last verified (2026-07 delta).** Three material facts postdate the eval's 2026-06-29 verification, so read it with these corrections; the refresh is filed as [#273](https://github.com/mattbutlerengineering/ai-tooling/issues/273):

1. **Self-serve launch.** [8090.ai/pricing](https://www.8090.ai/pricing) (read live 2026-07-11) now offers Software Factory **self-serve at $200/user/month** (tokens billed separately; >50 seats → sales) via factory.8090.ai, plus "8090 Enterprise" at custom pricing "Starting at $1M/yr". The eval's "no self-serve trial, unevaluable hands-on" no longer holds.
2. **The marketed pipeline is now 5 core modules: Requirements, Blueprints, Work Orders, Tests, Feedback** ([8090.ai/software-factory](https://www.8090.ai/software-factory)). "Development" is no longer a named module — execution is positioned as "IDE / Agent of choice — no lock-in" (BYO coding agent), "Validator" became **Feedback**, and **Tests** is promoted to a first-class module ("every feature is validated against its requirements"). New named capabilities: "Forward + backward pass" context propagation and "Multi-Player Collaboration". The Requirements → Blueprints → Work Orders → Development → Validator shape recorded in our [mapping doc](8090-software-factory-sdlc.md) is the **old** naming.
3. **$135M Series A** announced 2026-06-29 ([blog](https://www.8090.ai/blog/series-a)), led by Salesforce Ventures; Chamath Palihapitiya moved to full-time CEO.

Two design choices worth naming here because the synthesis below leans on them: **Tests as a named pipeline module** (validation is a stage with an artifact, not a hope), and the vendor's own **de-naming of Development** — even the platform that owns the most of the front-of-loop treats code execution as a commodity slot for whatever agent you prefer.

## EY.ai PDLC — a services wrapper, not an independent platform

**What it is.** EY.ai PDLC (Product Development Lifecycle) is an AI-native software-delivery **framework + consulting offering** from Ernst & Young LLP, [launched 2026-03-18](https://www.ey.com/en_us/newsroom/2026/03/ernst-young-llp-and-8090-launch-ey-ai-pdlc) — and its engine **is 8090's Software Factory** (the [service page](https://www.ey.com/en_us/services/consulting/ai-native-pdlc-reinventing-software-delivery)'s own "Built on 8090" section). EY provides the methodology, consultants, and delivery teams; 8090 provides the platform. EY names **no pipeline modules of its own** — the modules are 8090's five, above.

**What EY adds over raw 8090.**

- Transformation consulting: packaged adoption offerings and role-reshaping guidance ("traditional roles converge").
- Responsible-AI guardrails and governance framing as a first-class pillar (depth unverifiable from public material).
- Delivery capacity: EY US digital-engineering teams run the platform for clients, targeting the two hardest enterprise jobs — legacy modernization/decommissioning and governed new-product builds.
- An "open ecosystem" promise: 8090 is the founding partner, with more technology partners expected.

**Openness.** Fully sales-gated: no pricing, no trial, no OSS under the EY.ai PDLC name — access is a demo-request form leading to a consulting engagement. (The 8090 substrate is now self-serve, but that is 8090's channel, not EY's.)

**Flagged claims.** The headline figures — "shippable products up to 80x sooner", "70% increase in software development productivity", "95%+ automated test coverage" — all trace to **one unnamed internal EY US use case** cited in the launch press release: vendor claims, no published methodology, unverified. Treat this section as a lens on how 8090 gets packaged for regulated enterprises, not as a seventh platform.

## tembo.io (Tembo)

**What it is.** A cloud **orchestration layer for third-party coding agents** — "Move coding agents to the cloud" ([tembo.io](https://www.tembo.io/), read live 2026-07-11). Tembo runs Claude Code, Codex, Cursor, OpenCode, Amp, and Pi in isolated cloud sandboxes, triggered from the tools teams already use (Slack, Linear, Jira, GitHub, Sentry, schedules, webhooks), and returns reviewable PRs with human-only merge. It is explicitly *not* another proprietary coding agent. The company pivoted from managed Postgres on [2025-05-05](https://www.tembo.io/blog/autonomous-software-maintenance-has-arrived).

**Pipeline** ([tembo.io/agents](https://www.tembo.io/agents), [docs.tembo.io](https://docs.tembo.io/)):

| Module | What it produces |
|---|---|
| **Sessions** | A reviewable PR per session: Plan → Execute (sandbox) → Verify (runs *your* tests/builds) → Review → Ship (human merge only) |
| **Agents** | Scheduled + event-driven automations (Sentry error, Linear issue, PR opened, `@tembo` mention, webhook) built from templates |
| **Reviews** | Automated PR review with inline comments |
| **Feedback Loop** | Iterate on Tembo's PRs via review comments, like a teammate |
| **Sandbox / Snapshots / Hooks / `tembo.nix`** | Isolated execution environments, preloaded repos, lifecycle hooks, custom deps |

**What it does well.**

- **Harness/model agnosticism as the product thesis**: per-task agent and model switching, BYOK — no proprietary wrapper.
- **Production-telemetry-to-PR loop**: Sentry webhook → stack-trace/breadcrumb analysis → fix PR, with dedupe of already-fixed errors ([docs](https://docs.tembo.io/integrations/sentry.md)). The sharpest closed-loop reflex in this survey.
- **Meet-devs-where-they-are triggering**, with live session logs streamed back into Slack threads, Linear comments, and PRs.
- **Verification in the session contract**: every session runs the repo's own tests/builds before returning output; nothing ships without a human merge.
- **Serious self-hosted story** for a young pivot: a NixOS single-instance appliance of the whole platform.

**Openness.** Genuinely self-serve: free tier (no card, OSS models, 1 repo), $60/$200 tiers with publicly documented credit mechanics ([docs](https://docs.tembo.io/resources/pricing.md)); Enterprise adds SSO/BYOK. But **zero public repositories** today — the [tembo-io GitHub org](https://github.com/tembo-io) is empty; legacy Postgres-era OSS (pgmq) was spun out to its own org, and the self-hosted product is a licensed proprietary appliance.

**What it does not do.** No requirements/PRD authoring (it consumes existing tickets) and no deploy/release automation (merge is where it stops) — do not credit it with front-of-loop or ship-stage coverage. Customer metrics on [tembo.io/customers](https://www.tembo.io/customers) — "98% of dependency upgrades automated", "16% of all pull requests opened by Tembo" — are vendor-page claims, unverified. Datadog/PostHog integrations appear only in the pricing table, not the docs — unconfirmed.

## Qodo

**What it is.** An **AI code review and governance platform** — the live hero ([qodo.ai](https://www.qodo.ai/), read 2026-07-11): "Govern code at the speed AI writes it", positioned as "the layer between AI wrote it and production". In April 2026 Qodo **formally deprecated its code generation** (CEO post, [2026-04-23](https://www.qodo.ai/blog/an-update-on-code-generation-at-qodo/): "the tool generating code should not be the same tool reviewing it") and repositioned as the independent verification layer over code from *any* agent — Copilot, Cursor, Claude Code, or a factory.

**Pipeline** ([docs.qodo.ai](https://docs.qodo.ai/), [platform page](https://www.qodo.ai/ai-code-review-platform/)):

| Module | What it does |
|---|---|
| **Qodo Code Review (v2)** | Multi-agent PR review: specialized agents for critical issues, duplicated logic, ticket compliance, standards |
| **Code Governance / Rules System** | **Rule Miner** turns PR-comment history into enforceable rules with provenance links; rule health (duplicates, conflicts, decay) + adoption analytics |
| **Cross-Repository Review** (beta) | Auto-discovered repo relationships; flags breaking changes across repos *and* Git providers before merge |
| **Qodo IDE plugin** (formerly "Qodo Gen") | Local pre-PR review in the editor; codegen features removed |
| **Agent Skills** (MIT, [qodo-ai/qodo-skills](https://github.com/qodo-ai/qodo-skills)) | `qodo-get-rules` / `qodo-pr-resolver`: inject org rules and findings into third-party coding agents |
| **Context Engine** (formerly "Aware") | Multi-repo retrieval substrate powering all review agents; exposed via MCP/API |
| Command + Cover | Legacy CLI agent-runner and test-gen — demoted to legacy doc paths [INFERENCE from doc placement; no official EOL statement found] |

The historical lineup "Qodo Gen / Merge / Cover / Command / Aware" is **obsolete naming**: Gen → IDE plugin, Merge → the legacy v1 name for Code Review, Aware → Context Engine. Relatedly, the open-source **pr-agent no longer lives under qodo-ai**: the repo was transferred to the community org [The-PR-Agent/pr-agent](https://github.com/The-PR-Agent/pr-agent) and its LICENSE is now MIT ("community-maintained legacy project of Qodo… not the Qodo free tier") — our [pr-agent eval](../evaluations/pr-agent.md) predates this; the fact fix is filed as [#274](https://github.com/mattbutlerengineering/ai-tooling/issues/274).

**What it does well.**

- **Independent-verification stance**: deliberately decoupling review from generation gives it an architecturally clean role in a multi-vendor AI SDLC — it governs everyone else's output instead of competing with it.
- **Self-learning standards loop**: Rule Miner converts review history into living, measured rules with provenance — standards as a system, not a wiki.
- **Cross-repo, cross-provider impact analysis** pre-merge — a genuinely differentiated review capability.
- **Same rules on every surface**: one Context Engine and one rules system enforced in the IDE, inside third-party coding agents (via the MIT skills), and on the PR.
- **Governance system-of-record for leaders**: findings, risk analytics, audit trail, and skill-file governance across repos.
- Published a **reproducible public benchmark** (HuggingFace [`Qodo/PR-Review-Bench`](https://huggingface.co/datasets/Qodo/PR-Review-Bench)) rather than only claiming numbers — self-serving but auditable.

**Openness.** 14-day self-serve trial (no card); Pro Team at ~$30 + pooled credits; **no permanent free tier** ([pricing](https://www.qodo.ai/pricing/)). MIT OSS at the edges (qodo-skills, open-aware, agents playbooks); the platform itself is proprietary, with on-prem/air-gapped/BYOK on Enterprise. Note the marquee differentiators — cross-repo review, the self-learning system, custom agentic workflows — are **Enterprise-only** per the pricing matrix.

**Flagged claims.** "Highest F1-score" among AI code review tools is Qodo's **own benchmark** ([methodology page](https://www.qodo.ai/ai-code-review-benchmark/)) — vendor-run, dataset public, results not independently reproduced by us. "~1 hour saved per PR" and "90% of initial review handled before a human steps in" are homepage FAQ / customer-quote claims, unverified.

## Planview Software Product Delivery

**What it is.** One of five named solutions on Planview's portfolio platform — a **strategy-and-visibility layer that "sits above the tools where work happens"** (Jira, Azure DevOps, GitHub, ServiceNow; [solution page](https://www.planview.com/products-solutions/solutions/digital-product-development/)). It is value-stream management plus lean-agile portfolio governance: it does **not write software** — it funds, plans, governs, measures, and traces it. Buyer: Office of the CTO/CPO, EPMO. Its pitch is answering the board's question "what did engineering deliver and what did it return?" — explicitly including proving ROI on **AI-agent spend**.

**Pipeline** (capability areas, named on the solution page):

- **Planning & Funding** — scenario planning, OKRs, lean business cases, product/value-stream funding, capacity planning, roadmaps
- **Financials** — portfolio financials, forecasting, ROI/NPV/IRR analysis, agile costing & capitalization
- **Team Delivery** — PI/quarterly planning, enterprise Kanban, WIP limits, dependency management
- **Toolchain Integration** — 60+ out-of-box connectors over a common data model
- **Performance Analytics** — Flow Framework® flow metrics + DORA signals, normalized across teams regardless of tool
- **Governance & Compliance** — automated cross-tool traceability links for audits
- **Planview Anvi™** (AI layer; formerly Planview Copilot, rebranded Oct 2025) — custom agents, the **Outcome Intelligence Graph** ([announced 2026-06-16](https://newsroom.planview.com/planview-closes-the-gap-between-strategic-intent-and-business-outcomes-in-the-age-of-ai/)): a semantic graph linking decisions→resources→outcomes; Connected Work Graph (cross-team dependency map); an **Anvi MCP server** so external agents (Claude, ChatGPT, Copilot) can query the portfolio graph; and **Agent Resource Management** — AI agents governed as first-class capacity alongside humans, with cost visibility and guardrails.

[INFERENCE] The SKU composition behind this solution — Planview Viz (ex-Tasktop), AgilePlace (ex-LeanKit), Hub, Portfolios, Anvi, plus adjacent Release/Verify (ex-Plutora) — is our mapping from capability descriptions to the [product catalog](https://www.planview.com/products-solutions/); the solution page never enumerates SKUs. Per that catalog, Planview Release orchestrates release calendars and approvals (no deploy execution) and Planview Verify manages test *environments* (no test generation) — the basis for the ~ cells in the matrix below.

**What it does well.**

- **Toolchain-neutral visibility**: the picture assembles across mixed/legacy stacks without forcing migration.
- **Flow/VSM measurement pedigree**: the Flow Framework® (Tasktop / Mik Kersten lineage) normalized across every delivery tool.
- **Investment-to-outcome traceability** — its sharpest differentiator against every code-side platform in this survey: ties each feature and each unit of *AI-agent spend* to the OKR it was funded to move, with planned-vs-realized benefits closing the loop.
- **Agentic-era governance ahead of peers**: agents as governed, costed capacity (Agent Resource Management) and the portfolio graph exposed to external agents over MCP — both official 2026 announcements.

**Openness.** Fully proprietary, enterprise-sales: no OSS components found, no visible free tier or self-serve trial, pricing unpublished. The Anvi MCP server is an integration surface for customers, not an open artifact.

**What it does not do.** Implement, verify, and ship are **deliberately not owned** — Planview observes flow in the tools that do those jobs. Do not read it as a code factory; it wraps the outer loop (fund → plan → govern → measure → re-fund) around an inner loop it never executes. Customer outcomes — Huntington National Bank's "32% revenue growth", Vanguard's "75% reduction in major incidents" — are vendor-published case-study claims, unverified.

## Stage-coverage matrix

✓ core capability · ~ partial · ✗ delegated or absent. Cell notes give the nuance; every cell is consistent with the platform sections above.

| Platform | Requirements / Intent | Plan / Architecture | Implement | Verify / Review | Ship / Release | Operate / Feedback | Portfolio / Funding |
|---|---|---|---|---|---|---|---|
| **factory.ai** | ~ triage intake, not authoring | ✓ Specification Mode, Missions | ✓ Droid sessions | ✓ review + security + QA | ~ weakest stage, vendor's own admission | ✓ incident→PR correlation | ✗ readiness/agent metrics only |
| **8090** | ✓ Requirements module | ✓ Blueprints | ~ BYO agent (Development de-named) | ✓ Tests module | ~ user-directed handoff | ✓ Feedback module | ✗ audit trail only |
| **EY.ai PDLC** | ✓ intent-driven (via 8090) | ✓ via 8090 | ~ via 8090 + EY teams | ✓ via 8090 | ~ via 8090 + delivery teams | ✓ via 8090 | ✗ consulting, not tooling |
| **tembo.io** | ✗ consumes tickets only | ~ per-task plan only | ✓ core: agent sessions | ✓ runs your tests + PR review | ✗ human-gated merge only | ✓ Sentry→PR reflex | ✗ none |
| **Qodo** | ~ ticket-compliance checks only | ✗ DIY via legacy Command | ~ rules injected into others' agents; no codegen by design | ✓ core: multi-agent review | ~ merge gate only | ~ review-history learning, no runtime signal | ✗ governance analytics only |
| **Planview** | ~ portfolio intake, not specs | ✓ strongest: scenario/capacity/PI | ✗ observes flow only | ~ test environments, no test gen | ~ release calendars, no deploy | ✓ flow/DORA + benefits realization | ✓ core: funding→outcome |

Two readings fall out. First, **no platform covers every column** — even the code-side factories stop at the portfolio line, and the portfolio layer never touches code. Second, the ✓ clusters reproduce the five-altitude taxonomy: factory.ai/8090 own the middle, tembo owns execution-plus-feedback, Qodo owns verification, Planview owns the ends nobody else touches.

## The ideal workflow

This is the section [#272](https://github.com/mattbutlerengineering/ai-tooling/issues/272) exists for: not what any one vendor sells, but what the six **converge on** despite operating at different altitudes.

### The convergent skeleton

Every step below names the platform sections above that it is derived from:

1. **Continuous signal intake.** Work enters as signals, not sprint tickets: factory.ai's Triage stage, tembo's event/schedule/webhook triggers, 8090's Feedback module all make intake a running process with an artifact (a routed ticket / a structured work item).
2. **Intent captured as durable, traceable artifacts before code.** 8090's Requirements → Blueprints chain, EY's intent-driven front of loop, and factory.ai's Specification Mode agree: a spec artifact precedes code, and later stages trace back to it.
3. **Codebase-tied work units.** 8090's Work Orders are the clearest form: tasks scoped narrow, naming the code they touch, linked upward to requirements.
4. **Execution is a commodity slot — BYO, model-agnostic.** The strongest signal in the survey: 8090 *de-named* its Development module ("IDE / Agent of choice — no lock-in"), tembo's entire thesis is orchestrating other vendors' agents, and factory.ai leads with BYOK + Router + Mixed Models. Nobody credible claims the coding agent itself is the moat.
5. **Independent, multi-dimensional verification.** Qodo's generation/review separation of powers is the purest statement; factory.ai's Validate stage (review + security + QA as distinct dimensions) and tembo's run-your-own-tests session contract make the same move: verification is a separate system from generation, with its own artifacts.
6. **Human-gated ship.** Universal — factory.ai's Release is its self-admitted weakest stage, tembo and Qodo stop at the merge gate, 8090 keeps version control user-directed. No platform in this survey auto-merges to production.
7. **Production telemetry closes the loop.** factory.ai's Monitor stage correlates incidents back to the causing PR; tembo turns a Sentry alert into a fix PR. Operate-stage signals re-enter step 1 as new work.
8. **A traceability spine binds it all.** 8090's knowledge graph, Qodo's rule provenance, and Planview's cross-tool traceability are the same idea at three altitudes: every artifact links to what caused it, so drift is detectable and audits are answerable.
9. **The layer only Planview adds: portfolio governance.** Fund the work, measure whether the funded outcome materialized, and — new in 2026 — govern **AI agents as costed, first-class capacity**. The code-side factories have no answer to "was this worth it?"

### Distinctive ideas worth stealing

- **Agent Readiness maturity scoring** — score a repo for autonomy-readiness before raising autonomy (factory.ai).
- **Tiered autonomy defaults** — read-only unless explicitly escalated, per task (factory.ai `droid exec`).
- **Generation/verification separation of powers** — the reviewer must not be the author (Qodo).
- **Rules mined from review history, with provenance** — standards that learn and cite their sources (Qodo).
- **Telemetry-to-PR reflex arc** — production error to deduped fix-PR without a human dispatcher (tembo).
- **Tests as a first-class pipeline module** — validation has its own stage and artifact, not a checkbox inside "dev" (8090).
- **Agents as governed capacity with outcome accounting** — agent spend funded, measured, and traced like headcount (Planview).

### Mapping onto our loop

The ideal-workflow stages map onto this repo's [inner/outer dev loop](../WORKFLOW.md) and the catalogued skills that fill them today — the same exercise the [8090 mapping doc](8090-software-factory-sdlc.md) does for one platform, generalized to the survey. The [intent-to-production recipe](intent-to-production-recipe.md) is the runnable open-tool assembly of rows 2–7; it is not restated here.

| Ideal-workflow stage | Derived from | Our loop stage | Catalogued tool / skill |
|---|---|---|---|
| Signal intake | factory.ai Triage; tembo triggers; 8090 Feedback | inner **Reflect** / outer **Discover** | `triage` (feedback/bugs → agent-ready issues) |
| Intent → artifacts | 8090 Requirements/Blueprints; factory.ai Specification Mode | outer **Discover/Architect** → inner **Plan** | `to-prd` ([eval](../evaluations/skills-collections.md)); `brainstorming` + `writing-plans` ([superpowers eval](../evaluations/agent-harnesses.md)); `feature-dev` code-architect ([eval](../evaluations/feature-dev.md)) |
| Codebase-tied work units | 8090 Work Orders | outer **Decompose** | `to-issues` ([eval](../evaluations/skills-collections.md)); `beads` ([eval](../evaluations/beads.md)) |
| BYO execution | 8090 de-named Development; tembo sessions; factory.ai BYOK/Router | inner **Implement** | `implement-issue` (harness-agnostic by construction — the skill, not the agent, is the asset) |
| Independent verification | Qodo review separation; factory.ai Validate; tembo test runs | inner **Verify → Review** | `implement-issue`'s TDD + dual-axis review; `pr-agent` for independent PR review ([eval](../evaluations/pr-agent.md)) |
| Human-gated ship | universal (all six) | inner **Ship** | `implement-issue` PR/CI/merge; `make check` as the deterministic gate |
| Telemetry closes the loop | factory.ai Monitor; tembo Sentry→PR | inner **Reflect** / outer **Retrospect** | `triage` (manual intake — see gaps below) |
| Traceability spine | 8090 knowledge graph; Qodo rule provenance; Planview traceability | cross-cutting **Plan + Reflect** | `graphify` ([eval](../evaluations/graphify.md)); `claude-mem` ([eval](../evaluations/memory-systems.md)); `codegraph` ([eval](../evaluations/codegraph.md)); CONTEXT.md/ADRs via `domain-modeling` ([eval](../evaluations/domain-modeling.md)) |
| Portfolio / funding | Planview (alone) | *no equivalent stage* | — (see gaps) |

### Honest gaps

Where the survey's ideal exceeds both our open-tool stack and our [WORKFLOW.md](../WORKFLOW.md) loop itself — stated, not smoothed over:

- **No auto-propagating artifact graph.** Our graph/memory tools index artifacts; none makes a requirement change ripple into specs, tasks, and code the way 8090's knowledge graph and Planview's Outcome Intelligence Graph claim to. Re-linking is manual (same gap the [8090 mapping](8090-software-factory-sdlc.md) records).
- **No portfolio layer at all.** WORKFLOW.md has no Fund/Measure stage; nothing in the catalog ties work — let alone agent spend — to a funded outcome. Planview's agents-as-costed-capacity accounting has no open-tool equivalent we know of.
- **No repo-readiness scoring.** We adopt autonomy by judgment; factory.ai's Agent Readiness Model makes it a measured maturity gate. WORKFLOW.md's "adopt in layers" section is the informal cousin.
- **No cross-repo pre-merge impact analysis.** Our review skills see one repo's diff; Qodo's cross-repository review flags breaking changes across repos and Git providers before merge.
- **No automated telemetry-to-PR reflex.** tembo's Sentry→fix-PR arc is a running process; our Reflect arc needs a human to carry the alert into `triage`.
- **Rules don't learn.** Our standards live in docs and review skills; Qodo's Rule Miner turns review history into enforced, provenance-linked rules automatically.

The counter-trade, as with [8090](8090-software-factory-sdlc.md): every platform above is closed and priced; the assembled open-skill pipeline is transparent, adoptable, and license-free.

## Sources

All read directly on **2026-07-11**. Live spot-checks of the four highest-risk pages (factory.ai/news/software-factory, 8090.ai/pricing, qodo.ai hero, tembo.io) were re-done at writing time and matched the research; no corrections were needed.

- **factory.ai**: [factory.ai](https://factory.ai/) · [Factory 2.0 announcement](https://factory.ai/news/software-factory) · [docs.factory.ai](https://docs.factory.ai/welcome) ([pricing](https://docs.factory.ai/pricing.md), [software-factory](https://docs.factory.ai/web/software-factory.md), [models](https://docs.factory.ai/models.md), [missions](https://docs.factory.ai/features/missions/overview.md), [droid exec](https://docs.factory.ai/cli/droid-exec/overview.md), [benchmarks](https://docs.factory.ai/benchmarks/terminal-bench.md)) · [github.com/Factory-AI](https://github.com/Factory-AI)
- **8090**: [8090.ai](https://www.8090.ai/) · [pricing](https://www.8090.ai/pricing) · [software-factory](https://www.8090.ai/software-factory) · [Series A](https://www.8090.ai/blog/series-a) · plus this repo's [eval](../evaluations/8090-software-factory.md) and [mapping](8090-software-factory-sdlc.md)
- **EY.ai PDLC**: [service page](https://www.ey.com/en_us/services/consulting/ai-native-pdlc-reinventing-software-delivery) · [launch press release, 2026-03-18](https://www.ey.com/en_us/newsroom/2026/03/ernst-young-llp-and-8090-launch-ey-ai-pdlc)
- **tembo.io**: [tembo.io](https://www.tembo.io/) · [agents](https://www.tembo.io/agents) · [pricing](https://www.tembo.io/pricing) · [customers](https://www.tembo.io/customers) · [pivot post](https://www.tembo.io/blog/autonomous-software-maintenance-has-arrived) · [docs.tembo.io](https://docs.tembo.io/) · [github.com/tembo-io](https://github.com/tembo-io) (empty)
- **Qodo**: [qodo.ai](https://www.qodo.ai/) · [pricing](https://www.qodo.ai/pricing/) · [platform](https://www.qodo.ai/ai-code-review-platform/) · [benchmark](https://www.qodo.ai/ai-code-review-benchmark/) · [codegen deprecation](https://www.qodo.ai/blog/an-update-on-code-generation-at-qodo/) · [docs.qodo.ai](https://docs.qodo.ai/) · [github.com/qodo-ai](https://github.com/qodo-ai) · [The-PR-Agent/pr-agent](https://github.com/The-PR-Agent/pr-agent)
- **Planview**: [Software Product Delivery solution page](https://www.planview.com/products-solutions/solutions/digital-product-development/) · [Planview Anvi](https://www.planview.com/ai/) · [2026-06-16 announcement](https://newsroom.planview.com/planview-closes-the-gap-between-strategic-intent-and-business-outcomes-in-the-age-of-ai/) · [product catalog](https://www.planview.com/products-solutions/)
