# Software factories — what six vendors actually sell, and the workflow to derive from them

**What this is:** an evaluation of the six vendors named in
[#272](https://github.com/mattbutlerengineering/ai-tooling/issues/272) — what each one is, what
it does well, and what it is not — followed by the **ideal workflow** derived from all of them
plus the [practitioner corpus](software-factory-field-notes.md), mapped onto this repo's
[inner/outer dev loop](../WORKFLOW.md) and [six quality signals](../WORKFLOW.md#quality-signals).

**Scope and honesty.** Nothing here was run. This is vendor-material research — product pages,
documentation, press releases and funding coverage, read on **2026-08-05** — and every
performance figure in it is **self-reported and unaudited**. Where a vendor's own docs give
detail (Factory's Agent Readiness Model, 8090's five modules, Tembo's pricing) it is quoted;
where the marketing is thin, this says so rather than inflating it. Under
[ADR-0005](../docs/adr/0005-verdict-vocabulary.md) that makes this a *methodology reading*, not an evaluation: no verdict
here promotes anything into [STACK.md](../STACK.md). One of the six, 8090, already has both a
[hands-on-blocked evaluation](../evaluations/8090-software-factory.md) (**DEFER**) and a full
[stage-by-stage mapping](8090-software-factory-sdlc.md); this doc links to those rather than
restating them.

---

## The finding that reorganizes the list

The six names in #272 are not six competitors. They sit at **three different layers**, and two of
them are the same engine:

```
  L3  PORTFOLIO / MEASUREMENT      Planview (Viz, Hub, Portfolios, AgilePlace, Copilot,
      "is the system getting faster,             Agent Resource Management)
       and what is it costing?"

  L2  CONTROL PLANE / DISCIPLINE   8090 Software Factory ──────► EY.ai PDLC
      "what work, in what order,      (Requirements → Blueprints → Work Orders
       with what audit trail?"         → Tests → Feedback, over a knowledge graph)
                                     Qodo (review + governance slice only)

  L1  EXECUTION / RUNTIME          Factory (Droid: one agent across every surface)
      "who writes the code,          Tembo (cloud runtime for *other people's* agents)
       and where does it run?"
```

**EY.ai PDLC is 8090.** EY US launched it in March 2026 *"powered by 8090's Software Factory"* —
so of the six names, five are distinct products. EY's contribution is a methodology wrapper, a
compliance posture and a distribution channel into tens of thousands of consultants, not an
independent factory.

**Two of the six are not software factories at all.** Qodo is a code-review and governance
platform — one stage of the loop, done thoroughly. Planview is a portfolio and flow-metrics
layer that predates the AI cycle. Both are *in* a factory; neither *is* one. That is not a
criticism: as the practitioner corpus argues at length, the layers that get skipped are exactly
the ones that decide whether the factory works.

**Nobody sells all three layers.** The word "software factory" is being claimed at every layer by
vendors solving different problems, which is most of why the term is hard to pin down.

---

## The vendors

| Vendor | Layer | What it actually is | Access | Does well | Adoptability here |
|---|---|---|---|---|---|
| **[Factory](https://factory.ai)** | L1 + governance | Droid agents across every surface; a "self-improving system for your SDLC" from signal ingestion to incident monitoring | Commercial; SaaS / hybrid / on-prem / air-gapped | **Agent readiness grading**; surface-agnostic single agent; model independence | Proprietary — not adoptable in an open-tool stack; *the readiness model is free to copy* |
| **[8090](https://www.8090.ai/)** | L2 | AI-native SDLC control plane; 5 modules over a knowledge graph with a full audit trail; code generation is BYO agent | $200/user/mo self-serve, or managed from ~$1M/yr | Requirements-first discipline; artifact-per-stage; audit trail for regulated delivery | [Evaluated → **DEFER**](../evaluations/8090-software-factory.md); methodology is MIT as [`software-factory-plugin`](https://github.com/8090-inc/software-factory-plugin) |
| **[EY.ai PDLC](https://www.ey.com/en_us/newsroom/2026/03/ernst-young-llp-and-8090-launch-ey-ai-pdlc)** | L2 (channel) | EY's "collaborative mesh of AI agents with human oversight across the full software lifecycle" — **built on 8090** | Consulting engagement | Packaging a control plane with governance and change management for regulated enterprises | Not a product you install; the interesting artifact is its **claims** (below) |
| **[Tembo](https://www.tembo.io)** | L1 (runtime) | "Move coding agents to the cloud" — runs Claude Code, Codex, OpenCode, Cursor, Copilot in isolated cloud sandboxes with central audit logs | Free / $60 Pro / $200 Max / Enterprise; metered compute $0.11–$2.95/hr; self-host option | **Harness-neutral isolation at scale**; event-triggered automations; pausable/resumable/shareable sessions | Commercial SaaS, no eval yet; the *pattern* (sandbox-per-run) is free |
| **[Qodo](https://www.qodo.ai)** | L2 (review slice) | Code review + governance: IDE, PR (GitHub/GitLab/Bitbucket/Azure DevOps), post-merge portal; cross-repo Context Engine; auto-discovered Rules | Commercial; BYOK models; SOC 2 Type II, ZDR, single-tenant, on-prem | **Rules discovered from your codebase**, not authored; findings tracked as a portfolio, not per-PR | MIT [`pr-agent`](https://github.com/The-PR-Agent/pr-agent) already catalogued; [`qodo-cover`](../evaluations/qodo-cover.md) is **SKIP** (discontinued upstream) |
| **[Planview](https://www.planview.com/solutions/software-product-delivery/)** | L3 | Portfolio + flow layer: Viz, Hub, Portfolios, AgilePlace, Copilot; Flow Metrics and DORA over a connected toolchain | Enterprise licence | **Agent Resource Management** — the only vendor here planning and governing *agent* capacity alongside human capacity | Enterprise PPM; not adoptable solo — but the *metric set* is the one the corpus says is missing |

### Factory — the readiness model is the product worth stealing

Factory sells Droids: coding agents deployed across CLI, desktop, web, API, Slack and CI, with
the same agent, customization and governance on every surface. It raised a $150M Series C at a
$1.5B valuation in April 2026; named customers include NVIDIA, Adobe, EY and Adyen. The homepage
now frames the whole thing as a factory — signal ingestion, triage, code generation, PR
validation, release, documentation, incident monitoring — with an automation count per stage.
Deployment goes to air-gapped if you need it, and "model independence" is a headline feature
rather than a footnote.

All of which is standard enterprise positioning. **The part with no equivalent anywhere else in
this list is the [Agent Readiness Model](https://docs.factory.ai/web/agent-readiness/overview):**
a 1–5 grade for whether a repository can be worked on by an agent at all, assessed across nine
pillars — Style & Validation, Build System, Testing, Documentation, Development Environment,
Debugging & Observability, Security, Task Discovery, and Product & Experimentation.

| Level | Name | What it means | Representative criteria |
|---|---|---|---|
| 1 | Functional | "Code runs, but requires manual setup and lacks automated validation" | README, linter, type checker, unit tests |
| 2 | Documented | "Basic documentation and process exist" | `AGENTS.md`, devcontainers, pre-commit hooks, branch protection |
| 3 | Standardized | "Clear processes are defined, documented, and enforced through automation" | integration tests, secret scanning, distributed tracing |
| 4 | Optimized | "Fast feedback loops and data-driven improvement" | rapid CI feedback, flaky-test detection |
| 5 | Autonomous | "Systems are self-improving with sophisticated orchestration" | — |

Levels are **gated**: you must pass 80% of the previous level's criteria to unlock the next, so a
repo cannot buy its way to level 4 with one impressive capability. Scoring is per-repo or
per-app in a monorepo, and `/readiness-report` produces the graded list with prioritized fixes.

The claim that makes this worth acting on came from Factory's CEO
[in the corpus](software-factory-field-notes.md#eno-reyes-factory-ai--agent-readiness-and-the-deceleration-finding):
level 4–5 codebases show "massive acceleration of end-to-end product life cycles"; level 1–2
codebases show **"very active deceleration."** You can adopt every agent tool on the market and
slow your company down. That is a falsifiable, load-bearing claim, and it inverts the usual
adoption order — **grade the codebase before you buy the factory**.

### 8090 — requirements-first, with an audit trail

Covered in depth in [`8090-software-factory-sdlc.md`](8090-software-factory-sdlc.md); the short
version. Five modules — Requirements → Blueprints → Work Orders → **Tests** → **Feedback** —
each emitting a durable artifact, bound by a knowledge graph and an audit-trail control plane.
The middle is deliberately empty: code generation is *"IDE / Agent of choice… no lock-in."*
Founded by Chamath Palihapitiya, $135M Series A led by Salesforce Ventures in June 2026, aimed
squarely at regulated enterprises — healthcare, financial services, manufacturing, federal.

**What it does well:** it refuses to start at code. Business intent goes in as plain English,
becomes a PRD, becomes blueprints, becomes codebase-tied work orders — and every change
synchronizes back to a living requirements document, so the audit trail is a by-product of the
pipeline rather than a report generated after it. In regulated delivery that trail *is* the
product; the code is table stakes.

**What to take without buying it:** the methodology is open-sourced MIT as
[`software-factory-plugin`](https://github.com/8090-inc/software-factory-plugin), and this repo
already reconstructs the whole pipeline from open skills in
[`intent-to-production-recipe.md`](intent-to-production-recipe.md).

### EY.ai PDLC — the claims are the artifact

EY.ai itself is EY's consulting AI platform: EY.ai Value Blueprints, Responsible AI frameworks,
an Agentic Framework built on NVIDIA NeMo Guardrails / NIM / AI-Q Blueprints, and a curated
Model Catalog including domain-tuned EY models. Software delivery is one slice of it, and that
slice is **EY.ai PDLC** (Product Development Lifecycle), launched March 2026 and *"powered by
8090's Software Factory"* — orchestrating "a *collaborative mesh* of AI agents with human
oversight across the full software lifecycle — from requirements and architecture through code,
testing, infrastructure and ongoing operations."

The reason it belongs in this doc is the numbers, which are the most specific claims any vendor
in the set publishes:

> "a 70% increase in software development productivity and cost efficiency" · delivery "by 80
> times" · "95%+ automated test coverage and continuous validation" · "idea to production-ready
> software in days or weeks instead of months"

Treat these as the ceiling of vendor optimism, not as a target. The corpus's own practitioner
number for well-run agentic work is
[30–60%](software-factory-field-notes.md#zen-van-riel--against-the-framing-itself), and the "80×"
is delivery *speed* on a scope EY does not define. What is genuinely informative is the shape:
a Big Four firm's differentiator is **governance and oversight over a mesh of agents**, not the
agents. That is the same conclusion the practitioners reach from the opposite direction.

### Tembo — the sandbox layer, harness-neutral

Tembo is the outlier and the most directly useful of the five. It does not sell an agent; it
**runs yours** — Claude Code, Codex, OpenCode, Cursor, Copilot — in isolated cloud VMs (to 128GB
RAM / 500GB disk), with sessions that pause, resume and share, plus Tembo Review for PRs and
Automations that "kick off agent work from any event." Its stage model is four steps: **Context**
(repos, tickets, alerts, docs) → **Execution** (isolated VM with dependencies) → **Output** (a PR
or artifact) → **Approval** ("review, iterate, and approve changes before anything merges").
Integrations run to 150+ including GitHub, Linear, Jira, Slack and Sentry, and every foreground
session and background run is centrally logged.

Worth knowing for context: Tembo was a managed Postgres company that shut down its Postgres cloud
and pivoted into background coding agents in 2025 — so its infrastructure DNA (sandboxes,
metering, audit logs) is older than its agent product.

**What it does well:** it is the commercial form of the pattern the practitioners converged on
independently — [worktree-per-run escalating to VM/Docker sandbox](software-factory-field-notes.md#owain-lewis--a-factory-you-can-watch-run)
once runs go unattended — and it stays neutral about which harness you point at it. The pricing
is legible (Free / $60 / $200 / Enterprise, compute metered per second from $0.1066/hr), and a
self-host option exists.

### Qodo — rules you don't have to write

Qodo (formerly CodiumAI) covers one stage properly rather than the loop badly: **review and
governance**. It spans pre-commit (VS Code, JetBrains, Visual Studio), the PR itself (GitHub,
GitLab, Bitbucket, Azure DevOps), and post-merge governance through a portal tracking "critical
findings, resolution rates and open issues across every repo." A cross-repo **Context Engine**
surfaces breaking changes and dependency conflicts beyond the diff. Models are BYOK — OpenAI,
Anthropic, Azure OpenAI or self-hosted — with SOC 2 Type II, zero data retention, single-tenant
and on-prem options.

**What it does well:** two things worth copying. First, **Rules are discovered, not authored** —
the system "automatically discovers and enforces your team's unique coding standards" from the
codebase, which is the honest answer to why hand-written rule files decay. Second, findings are
tracked **as a portfolio across repos**, not as comments that die with the PR; resolution rate is
a first-class number. That is Ben Fellows's policy-as-code idea with the authoring burden removed.

**Open-source surface, with a caveat.** [`pr-agent`](https://github.com/The-PR-Agent/pr-agent)
(MIT) is catalogued here already and is now a community-maintained *legacy* project; Qodo Merge
is its hosted successor, and Qodo Command adds a CLI for building, scheduling and triggering
custom agents from a terminal or CI. [`qodo-cover`](../evaluations/qodo-cover.md) — the
test-generation agent — is **SKIP** in this repo: discontinued upstream, with the maintainer
explicitly declining to name a successor. A vendor's open-source tier turning over twice in two
years is itself a data point about depending on it.

### Planview — the only one counting agents as capacity

Planview is the enterprise portfolio layer: **Viz** (formerly Tasktop Viz) for flow visualization,
**Hub** (formerly Tasktop Hub) for toolchain integration, **Portfolios**, and **AgilePlace**,
measured with **Flow Metrics** — Flow Load (work in progress), Flow Velocity (delivery capacity) —
alongside DORA. **Planview Copilot** is a multi-agent layer (patent pending) with per-domain
agents: OKR agents surfacing objectives drifting out of sync, portfolio-health agents detecting
variance across cost, scope or resource allocation.

**What it does well, and why it made the list:** in May 2026 Planview announced **Agent Resource
Management** — planning, predicting, governing and optimizing *both human and AI agent
resources*, GA from Fall 2026. Every other vendor here treats agent capacity as unlimited and
priced by token. Planview treats it as a **capacity line item in a portfolio**, which is the only
framing in the set that can answer "should this work go to an agent or a person, and what did
that choice cost." It is also the answer to the cost problem Factory's CEO raises — bills
"instantly become hundreds of millions of dollars" at 45,000 engineers — from the planning side
rather than the routing side.

The caution is that Planview's own software-delivery guidance is tool-agnostic to a fault
(*"the process shouldn't depend on the tools"*), and its delivery material does not yet mention
agents doing the work at all. It measures the factory; it does not run one.

---

## What the vendors converge on

Reading five distinct products against
[the practitioner corpus](software-factory-field-notes.md#where-they-agree), the overlap is
narrow and specific:

1. **The pipeline is mostly not code.** Signals → triage → planning → code → validation → ship →
   monitor. Factory says it outright; 8090 built its whole product on the front half; Qodo owns
   the back half; Planview measures the loop. Nobody's differentiator is code generation.
2. **Bring your own agent.** 8090 retired its development module; Tembo never had one; Factory
   sells model independence; Qodo is BYOK. **The execution layer has commoditized** — which is
   also why the practitioners can run Codex and Claude Code in one pipeline.
3. **The artifact trail is the product.** 8090's knowledge graph, Tembo's central audit logs,
   Qodo's findings portal, EY's oversight mesh, Factory's air-gapped deployment. What is being
   sold is the ability to *answer for* what the agents did.
4. **Isolation per run** is assumed, not argued — Tembo's VMs commercialize what the
   practitioners do with worktrees.
5. **Governance scales worse than generation.** Every enterprise product's hard part is controls,
   audit, residency and cost attribution. The generation problem is considered solved.

And one thing they conspicuously **do not** agree on: whether the factory is a product you buy or
a pipeline you build. Factory and 8090 say buy; Tembo says buy the runtime and build the rest;
the practitioners
[split on it](software-factory-field-notes.md#where-they-disagree--and-which-side-to-take), and
the resolution that survives contact with both sets of evidence is **buy or adopt the harness,
own the pipeline**.

## Agent readiness is the prerequisite nobody sells you

Every vendor in this list assumes your codebase can be worked on by an agent. Only Factory
measures whether that is true, and its measurement says level 1–2 repos get *slower*.

That reframes the whole adoption question. A factory is a **multiplier on the signal quality your
repo already emits** — if an agent cannot get a deterministic answer to "did I break it," every
stage you add multiplies noise instead. Cross-referencing Factory's nine pillars with
[Zakariasson's four-layer checklist](software-factory-field-notes.md#eric-zakariasson-cursor--the-ladder-the-checklist-and-the-silo-problem)
gives a vendor-free version you can run against any repo today:

| Layer | Question | Evidence it's satisfied |
|---|---|---|
| **Primitives** | Can an agent find the relevant code by listing one directory, or must it grep the repo? | modular, co-located structure; a `CLAUDE.md`/`AGENTS.md` that routes |
| **Guardrails** | Can the agent verify its own work without a human? | one command that runs lint + types + tests and exits non-zero; secret scanning; branch protection |
| **Enablers** | What can the agent *do* that it couldn't out of the box? | skills/MCP for the repo's real operations — ship behind a flag, cut a release, query the tracker |
| **Environment** | Can an agent start the dev environment unattended? | devcontainer or one-command bootstrap; if no, this is the bottleneck, not the model |
| **Feedback speed** | How long until the agent learns it was wrong? | CI wall-clock, flaky-test detection |
| **Task discovery** | Can an agent find work without being told? | tickets with enough context to implement from; labels that trigger stages |

**This repo's own score — measured, not asserted.** See
[`spikes/agent-readiness-score.md`](../spikes/agent-readiness-score.md) (#385), which scored this
repo against the model rather than eyeballing it. The result is sharper than the guess that
originally stood here, and corrects it in two places:

- **Level 1, gate not cleared — 2/4.** README ✅ and 324 unit tests ✅, but **no linter and no
  type checker** for 8,223 lines of Python. The rigor here is aimed entirely at the *data*
  (`CATALOG.md`, the evals, the generated pages) and not at all at the *program* that enforces
  it. `audit-evals.py` is 2,411 lines that have never been linted. "Guardrails are strong" was
  true of the data plane and false of the code plane, and the distinction was invisible until
  something scored it.
- **Feedback speed was not the gap.** It was un-instrumented, not slow: CI runs a **median of
  34 seconds**, 20/20 green. One command settled it.

What the score does confirm: primitives are strong (one `CLAUDE.md` routes everything, artifacts
are flat files), enablers are real, task discovery is strong, and the orchestration is
**Level-5-shaped** — derived pages, self-merging routines, bands that declare what an unattended
pass may conclude. Level-5 orchestration on a Level-1 foundation is exactly the inversion a gated
model exists to catch.

## The ideal workflow

Derived from both inputs — five vendors and six practitioners — and stated so it can be adopted
incrementally rather than bought. Each rule names the stage of
[our loop](../WORKFLOW.md) it belongs to and the [quality signal](../WORKFLOW.md#quality-signals)
it moves.

**0. Grade the repo before adding a factory.** Run the readiness table above. Below the
guardrails line, fix guardrails — adding pipeline stages to a repo with no deterministic
correctness signal makes delivery *slower*, which is the one measured claim in the vendor
material. *(Prerequisite · Correctness, Verifiability)*

**1. Tickets are the queue; a label is the trigger.** Work enters as an issue and a label
advances it a stage. Nothing enters the pipeline by being typed into a terminal.
*(Outer **Decompose** · Speed, Verifiability)*

**2. Stages, each with a fresh context and a typed artifact handoff.** Plan, implement, verify,
review, ship — separate runs, not one long conversation, each emitting a validated artifact the
next stage reads. Not a compacted transcript: a structured file.
*(Whole inner loop · Correctness, Cost Efficiency)*

**3. A deterministic gate between every pair of stages.** Policy-as-code first (mechanical:
lint, types, format, structural rules), then tests (behavioral), then semantic review. A stage
that fails a gate hands back to the agent rather than proceeding. This is the single point every
source in both corpora agrees on. *(**Verify** · Correctness, Safety)*

**4. Isolation per run, escalating with autonomy.** Worktree-per-run while you are watching;
container or VM sandbox once runs go unattended. The pipeline owns its branch and commits each
step, so the git history *is* the audit trail. *(**Implement**/**Ship** · Safety)*

**5. Harness- and model-agnostic by construction.** Handoffs are files in the repo, so any agent
can take any stage; pick the model per **role** — expensive reasoning to plan, fast and cheap to
build — not by preference. This is both a cost lever and the only real hedge against a single
vendor's regression. *(All stages · Cost Efficiency, Correctness)*

**6. Feedback re-enters as tickets, and scheduled jobs open tickets rather than merging.** A
bug-finder that files an issue is compounding; a bug-finder that merges is a liability. This repo
already runs the strict form: an unattended lane may eliminate, never adopt.
*(**Reflect** / outer **Retrospect** · Safety, Verifiability)*

**7. Autonomy is earned by measurement, one rung at a time.** Instrument cycle time and a
defect-origin metric — bugs and incidents introduced by agents versus humans. Raise autonomy
only when the number supports it. Without that instrumentation there is no honest way to move up
the ladder, which is precisely why most adopters sit at level 2–3 and talk about level 5.
*(Outer **Retrospect** · All signals)*

**8. Review capacity is the binding constraint — design for it explicitly.** Generation is
solved; the ceiling is whether a human can still confirm the output is right at the rate it is
produced. Every stage should *shrink* what a human must read: smaller diffs, machine-checkable
claims, findings tracked as a portfolio rather than as comments that die with the PR.
*(**Review** · Verifiability)*

Rule 8 is the one no vendor in this set measures, and it is the reason this repo added
[Verifiability](../WORKFLOW.md#why-verifiability-is-its-own-signal) as a sixth signal
independently. Five of the six signals ask whether the output is good; Verifiability asks whether
anyone can still tell. A factory optimizes the first five by construction and can silently
destroy the sixth.

## What this repo already has, and what it doesn't

| Ideal-workflow rule | Here today | Gap |
|---|---|---|
| 0 · readiness grade | [**scored**](../spikes/agent-readiness-score.md): strong primitives, enablers, task discovery; CI median 34s | **Level 1, gate not cleared** — no linter, no type checker for 8,223 lines of Python |
| 1 · tickets as queue | GitHub Issues + `triage.py` bands + `/triage` | no label-triggered stage advance |
| 2 · staged fresh context | [`intent-to-production-recipe.md`](intent-to-production-recipe.md) stage skills | handoffs are prose artifacts, not validated typed ones |
| 3 · deterministic gates | **`make check` — 15 detectors, CI-gated, offline** | — (this is the repo's strongest asset) |
| 4 · isolation per run | worktrees available | not enforced by the pipeline; no sandbox tier |
| 5 · harness/model agnostic | Claude Code + opencode in lockstep (ADR-0002) | no per-role model routing |
| 6 · feedback as tickets | eliminate-only rule, `triage`, scan issues | — |
| 7 · autonomy by measurement | verdict/evidence data, Evidence tiers | **no cycle-time or defect-origin metric at all** |
| 8 · review capacity | Verifiability signal defined and required for new evals | measured per-tool, never for the pipeline itself |

The real gaps are **7** — no cycle-time or defect-origin metric — and, now that **0** has been
scored, the ungated code plane: the machinery that enforces everything is itself unlinted and
untyped. By the standards of the corpus the *process* machinery here is unusually good; what is
missing is the number that would say so, and a linter on the program that produces it.

## Next actions this research argues for

1. ~~**Score this repo against the readiness table.**~~ Done —
   [`spikes/agent-readiness-score.md`](../spikes/agent-readiness-score.md). It produced a sharper
   answer than expected and a concrete next step: add a linter and a type checker for this repo's
   own Python, which is the only thing standing between it and the Level 1 gate.
2. **Catalog the gap.** Factory, Tembo, Qodo (the platform) and Planview have no `CATALOG.md`
   rows; only 8090 and Qodo's open-source pieces do. Four commercial products that define the
   category are invisible to the catalog and therefore to `triage.py`.
3. **Leave the buy decisions alone.** All five products are commercial; 8090 is already **DEFER**
   pending authorized spend, and the others would land in the same place for the same reason.
   The adoptable output of this research is the workflow above, not a purchase.

## Sources

Read 2026-08-05. Vendor material is self-reported.

- Factory — [factory.ai](https://factory.ai), [Agent Readiness Model docs](https://docs.factory.ai/web/agent-readiness/overview), [Introducing Agent Readiness](https://factory.ai/news/agent-readiness)
- 8090 — [8090.ai](https://www.8090.ai/); this repo's [evaluation](../evaluations/8090-software-factory.md) and [stage mapping](8090-software-factory-sdlc.md)
- EY — [EY.ai](https://www.ey.com/en_us/services/ai), [Ernst & Young LLP and 8090 launch EY.ai PDLC](https://www.ey.com/en_us/newsroom/2026/03/ernst-young-llp-and-8090-launch-ey-ai-pdlc), [EY.ai Agentic Platform with NVIDIA](https://www.ey.com/en_us/newsroom/2025/03/ey-launching-ey-ai-agentic-platform-created-with-nvidia-ai-to-drive-multi-sector-transformation-starting-with-tax-risk-and-finance-domains)
- Tembo — [tembo.io](https://www.tembo.io), [pricing](https://www.tembo.io/pricing), [Autonomous Software Maintenance Has Arrived](https://www.tembo.io/blog/autonomous-software-maintenance-has-arrived)
- Qodo — [qodo.ai](https://www.qodo.ai), [Qodo Merge / PR-Agent docs](https://qodo-merge-docs.qodo.ai/qodo-merge-cli/)
- Planview — [Software Product Delivery](https://www.planview.com/solutions/software-product-delivery/), [Agent Resource Management announcement](https://newsroom.planview.com/planview-launches-agent-resource-management-redefining-portfolio-resource-management-for-the-ai-era/)
- Practitioner corpus — [`software-factory-field-notes.md`](software-factory-field-notes.md) (six talks, gathered for [#307](https://github.com/mattbutlerengineering/ai-tooling/issues/307))
