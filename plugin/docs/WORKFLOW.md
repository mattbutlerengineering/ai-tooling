# AI Development Workflow

An operating manual for AI-assisted development that produces high-quality code — and keeps getting better.

This isn't a tool list. It's a workflow: the dev loop you run every session, the tools that improve each stage, the infrastructure that measures whether it's working, and the feedback arcs that make the next cycle better than the last.

## Design Principles

1. **Fewer tools, more feedback loops.** Five overlapping memory systems don't beat one with acceptance rate tracking.
2. **Each tool earns its slot.** If two tools solve the same problem, pick one. The overlap markers in [CATALOG.md](CATALOG.md) show where to consolidate.
3. **No context-switching tax.** If a tool pulls you out of flow to use it, it's not earning its slot. The best tools are invisible — they trigger automatically or integrate into commands you already run.
4. **Process + Tooling + Infrastructure.** Process alone is hope. Tooling alone is shelfware. Infrastructure alone is dashboards nobody reads. All three, connected by feedback arcs, is how quality compounds.

## Quality Signals

Every tool recommendation is justified by which of these signals it moves. If a tool doesn't improve at least one, it doesn't belong in the workflow.

| Signal | What it measures | Example metrics |
|--------|-----------------|-----------------|
| **Correctness** | Does the code do what it's supposed to? | Test pass rate on first run, bugs caught before merge, production incidents |
| **Speed** | How fast from prompt to merged PR? | Time-to-merge, review round-trips, rework rate |
| **Maintainability** | Can someone else work with this code? | File size discipline, review simplification trends, no unnecessary abstraction |
| **Safety** | Does it avoid breaking things — and recover fast when it does? | Security findings per PR, CI gate pass rate, rollback frequency, mean time to recovery |
| **Cost Efficiency** | Does the workflow avoid wasting tokens and money? | Tokens per session, redundant tool calls, agent invocations per task |

---

## The Inner Loop

For a single task — one issue, one bug, one feature. This is what you run every session.

```
Plan → Implement → Verify → Review → Ship
        ↑                              |
        └──────── Reflect ─────────────┘
```

### Plan

*Prevents: building the wrong thing, touching code you don't understand*

Understand the codebase and task before writing a line of code. Break the work into verifiable steps. Surface assumptions early — they're cheaper to fix now than after implementation.

| Layer | What | Signals |
|-------|------|---------|
| **Process** | Read the relevant code. State assumptions. Define what "done" means before starting. | Speed |
| **Tooling** | [graphify](https://github.com/safishamsi/graphify) — deep structural analysis into architecture diagrams ([eval](evaluations/graphify.md)) | Correctness |
| | [codegraph](https://github.com/colbymchenry/codegraph) — always-on code knowledge graph, auto-syncs on changes ([eval](evaluations/codegraph.md)) | Speed, Cost Efficiency |
| | [context7](https://github.com/upstash/context7) — live documentation lookup, current APIs not stale training data ([eval](evaluations/recommended-tools.md#context7)) | Correctness |
| | [markitdown](https://github.com/microsoft/markitdown) — converts PDF/Office/images/audio/HTML to clean Markdown so agents can actually read binary docs ([eval](evaluations/markitdown.md)) | Correctness, Cost Efficiency |
| | [codebase-design](https://github.com/mattpocock/skills) — shared vocabulary for deep modules: interfaces, seams, depth, leverage, locality | Maintainability |
| | [domain-modeling](https://github.com/mattpocock/skills) — build CONTEXT.md glossaries and ADRs as designs evolve | Correctness, Maintainability |
| **Infrastructure** | [github-mcp-server](https://github.com/github/github-mcp-server) — GitHub's official MCP: search repos, read issues/PRs, browse code during planning ([eval](evaluations/github-mcp-server.md)) | Speed, Correctness |

**Feedback arc:** If you frequently discover mid-implementation that your plan was wrong, your Plan stage is too shallow. Track how often you restart or significantly change direction — that's the signal.

### Implement

*Prevents: bugs at the source, stale API usage, wasted tokens*

Write code test-first. Use current docs, not training data. Minimize token waste — cheaper sessions mean more iterations.

| Layer | What | Signals |
|-------|------|---------|
| **Process** | TDD: write test first (RED), implement (GREEN), refactor. Use current library docs for every API call. | Correctness |
| **Tooling** | [superpowers](https://github.com/obra/superpowers) — TDD enforcement, systematic debugging, verification-before-completion ([eval](evaluations/agent-harnesses.md)) | Correctness, Maintainability |
| | [mattpocock/skills](https://github.com/mattpocock/skills) — engineering conventions, grilling, architecture improvement ([eval](evaluations/skills-collections.md)) | Maintainability |
| | [agent-skills](https://github.com/addyosmani/agent-skills) — lifecycle structure with verification gates at each step ([eval](evaluations/skills-collections.md)) | Correctness |
| | [context7](https://github.com/upstash/context7) — live docs during coding ([eval](evaluations/recommended-tools.md#context7)) | Correctness |
| | [caveman](https://github.com/JuliusBrussee/caveman) — cuts ~75% of agent output tokens ([eval](evaluations/caveman.md)) | Cost Efficiency |
| | [context-mode](https://github.com/mksglu/context-mode) — 98% input token reduction via MCP-layer sandboxing ([eval](evaluations/context-mode.md)) | Cost Efficiency |
| | [headroom](https://github.com/headroomlabs-ai/headroom) — compresses tool outputs 60-95% before they reach the LLM ([eval](evaluations/headroom.md)) | Cost Efficiency |
| | [typescript-mcp-server-generator](https://github.com/github/awesome-copilot) — skill-driven MCP server scaffolding: generates working TypeScript MCP project from a description ([eval](evaluations/typescript-mcp-server-generator.md)) | Speed |
| | [fastmcp](https://github.com/PrefectHQ/fastmcp) — build MCP servers in Python: decorator API, auth, middleware, incorporated into official MCP SDK ([eval](evaluations/fastmcp.md)) | Speed |
| **Infrastructure** | Coverage gating in CI — reject PRs below threshold so coverage never regresses | Correctness |

**Feedback arc:** If test pass rate on first run is declining, you're either writing shallow tests or skipping TDD for "simple" changes. Neither is simple.

### Verify

*Prevents: code that "seems to work" but doesn't*

Does it actually work? Tests passing is necessary but not sufficient — run the code, check the behavior, confirm the output matches intent. "Seems right" is never evidence.

| Layer | What | Signals |
|-------|------|---------|
| **Process** | Run tests, build, verify behavior matches intent. Evidence required: test output, build output, runtime data. | Correctness |
| **Tooling** | superpowers verification-before-completion — blocks claiming "done" without running verification commands | Correctness |
| **Infrastructure** | CI pipeline — automated test runs on every push | Correctness, Safety |
| | [stryker-js](https://github.com/stryker-mutator/stryker-js) — mutation testing: tests the quality of your tests, not just whether they pass ([eval](evaluations/stryker-js.md)) | Correctness |
| | [agent-browser](https://github.com/vercel-labs/agent-browser) — browser automation for verifying UI changes visually, not just via tests ([eval](evaluations/agent-browser.md)) | Correctness |
| | [diagnosing-bugs](https://github.com/mattpocock/skills) — structured diagnosis loop: build feedback loop first, then bisect and instrument | Correctness, Speed |
| | [web-quality-skills](https://github.com/addyosmani/web-quality-skills) — six domain-reference skills (accessibility, SEO, performance, Core Web Vitals, best practices, audit) loaded on demand for web quality checks ([eval](evaluations/web-quality-skills.md)) | Correctness, Maintainability |
| | [playwright](https://github.com/microsoft/playwright-mcp) — MCP-based browser automation: agents drive real browsers to verify UI changes and run E2E flows ([eval](evaluations/playwright-mcp.md)) | Correctness |

**Feedback arc:** If bugs regularly escape Verify and get caught in Review or production, your verification step is too shallow. Are you verifying the golden path but not edge cases?

### Review

*Prevents: bugs that pass tests but break in production, silent failures masked by catch blocks, security holes, unnecessary complexity*

Is the code good? This is where maintainability and safety get their primary check. Multi-perspective review catches what single-perspective testing misses.

| Layer | What | Signals |
|-------|------|---------|
| **Process** | Run automated review before committing. Review the diff yourself — tools catch patterns, you catch intent. | Maintainability, Safety |
| **Tooling** | [code-review plugin](evaluations/recommended-tools.md#code-review-plugin-anthropic) — multi-agent review with confidence scoring, filters noise ([eval](evaluations/recommended-tools.md#code-review-plugin-anthropic)) | Correctness, Maintainability |
| | [pr-review-toolkit](evaluations/recommended-tools.md#pr-review-toolkit-anthropic) — dimension-specific agents: silent failure hunting, type design, test coverage ([eval](evaluations/recommended-tools.md#pr-review-toolkit-anthropic)) | Maintainability, Safety |
| | [trailofbits/skills](https://github.com/trailofbits/skills) — professional security audit methodology ([eval](evaluations/trailofbits-skills.md)) | Safety |
| | [shadcn/improve](https://github.com/shadcn/improve) — two-model codebase audit: expensive model plans, cheap model executes ([eval](evaluations/shadcn-improve.md)) | Maintainability |
| | [PR-Agent](https://github.com/The-PR-Agent/pr-agent) — CI-native PR reviewer: auto-describe, review, improve on every push, works for non-Claude-Code users ([eval](evaluations/pr-agent.md)) | Correctness, Speed |
| **Infrastructure** | Review findings tracked by category — are "simplify this" comments decreasing over time? | Maintainability |

**Feedback arc:** If the same category of review finding keeps appearing (e.g., "missing error handling"), that's a CLAUDE.md rule waiting to be written. claude-reflect captures these automatically.

### Ship

*Prevents: broken deploys, unreviewed merges, regressions that slip through*

Commit, push, pass CI, merge. This stage is where infrastructure earns its keep — automated gates prevent human oversight failures.

| Layer | What | Signals |
|-------|------|---------|
| **Process** | Conventional commits. PR with summary and test plan. Never skip CI. | Speed |
| **Tooling** | [claude-code-action](https://github.com/anthropics/claude-code-action) — `@claude` in PRs/issues for async review and fixes ([eval](evaluations/claude-code-action.md)) | Speed |
| | [worktrunk](https://github.com/max-sixty/worktrunk) — git worktree management for parallel branches ([eval](evaluations/worktrunk.md)) | Speed |
| **Infrastructure** | PR acceptance rate tracking — merged vs. closed by category reveals what AI does well vs. poorly | Speed, Correctness |
| | Flaky test detection — weekly analysis removes non-determinism that corrupts results | Correctness |
| | Error monitoring → issues — production errors auto-create GitHub issues | Safety |

**Feedback arc:** If PR acceptance rate is low for a category (e.g., refactoring PRs keep getting closed), either the AI needs better instructions for that category or you're assigning it work it can't do well yet. Also watch **AI code churn rate** — how much recently merged code gets rewritten within 7 days. [Research shows](https://oobeya.io/blog/dora-metrics-not-enough-2026) AI can push throughput up 30-40% while doubling churn and dropping delivery stability by 7.2%. High speed + high churn = generating throwaway code.

### Reflect (the feedback arc)

*Prevents: repeating the same mistakes, losing context between sessions*

Reflect isn't a stage with a "done" moment — it's the arc that connects the end of one loop to the start of the next. What went wrong? What went right? Update the instructions so the next session is better.

| Layer | What | Signals |
|-------|------|---------|
| **Process** | End each session by reviewing what was corrected. Commit with conventional commits — the commit log is a feedback loop too. | All |
| **Tooling** | [claude-reflect](https://github.com/BayramAnnakov/claude-reflect) — captures corrections and preferences, syncs to CLAUDE.md ([eval](evaluations/recommended-tools.md#claude-reflect)) | Correctness, Speed |
| | [claude-mem](https://github.com/thedotmack/claude-mem) — persistent cross-session memory with semantic search ([eval](evaluations/memory-systems.md)) | Speed |
| | [documentation-writer](https://github.com/github/awesome-copilot) — Diátaxis-framework documentation expert: clarify, outline, generate purpose-specific docs ([eval](evaluations/documentation-writer.md)) | Maintainability |
| | [documentation-and-adrs](https://github.com/addyosmani/agent-skills) — ADR templates and decision-recording guidelines for architectural choices ([eval](evaluations/documentation-and-adrs.md)) | Maintainability |
| **Infrastructure** | Track whether the same correction recurs — if it does, the learning failed | All |

---

## The Outer Loop

For larger work — an epic, a new feature that spans multiple sessions, a project. The outer loop produces tasks that the inner loop executes.

```
Discover → Architect → Decompose → [inner loop per task] → Integrate → Retrospect
```

### Discover

*Prevents: building the wrong product, missing requirements, solving a problem nobody has*

What are we building and why? Research, requirements, stakeholder interviews. This is where you figure out whether the work is worth doing at all.

| Layer | What |
|-------|------|
| **Process** | Define the problem before proposing solutions. Interview stakeholders. Write a spec or PRD. |
| **Tooling** | GSD `new-project` — deep context gathering ([eval](evaluations/recommended-tools.md#gsd-get-shit-done)) |
| | agent-skills `spec-driven-development` — requirements as living specs ([eval](evaluations/skills-collections.md)) |
| | mattpocock `grill-me` / `grill-with-docs` — stress-test the plan against existing domain language ([eval](evaluations/skills-collections.md)) |
| | [last30days](https://github.com/mvanhorn/last30days-skill) — engagement-weighted research across Reddit, X, YouTube, HN, Polymarket — 15+ real scrapers with synthesis contract ([eval](evaluations/last30days.md)) |
| **Infrastructure** | Requirements churn tracking — measure how often specs change after sign-off | Speed, Correctness |
| | [Apache DevLake](https://github.com/apache/incubator-devlake) — track issue creation rate and requirements-to-code lead time ([eval](evaluations/apache-devlake.md)) | Speed |

### Architect

*Prevents: wrong technical decisions that are expensive to reverse, spaghetti across components*

How do we build it? Solution design, technology choices, interface boundaries. Architecture decisions made here constrain every inner-loop iteration that follows.

| Layer | What |
|-------|------|
| **Process** | Map the codebase before proposing changes. Design interfaces before implementations. Record non-obvious decisions in ADRs. |
| **Tooling** | GSD `map-codebase` + `plan-phase` — parallel mapper agents produce structured analysis ([eval](evaluations/recommended-tools.md#gsd-get-shit-done)) |
| | [feature-dev](https://github.com/anthropics/claude-plugins-official) `code-architect` — architecture design with codebase awareness ([eval](evaluations/recommended-tools.md#feature-dev-anthropic)) |
| | graphify — architecture visualization for understanding component relationships ([eval](evaluations/graphify.md)) |
| **Infrastructure** | ADR count and staleness tracking — flag decisions older than 90 days with no review | Maintainability |
| | Architecture fitness functions in CI — automated checks that dependencies respect module boundaries | Maintainability, Safety |

### Decompose

*Prevents: monolithic PRs, blocked dependencies, unclear scope, multi-day branches that diverge*

Break the architecture into independently shippable tasks. Each task should be one inner-loop iteration — small enough to plan, implement, verify, review, and ship in a single session.

| Layer | What |
|-------|------|
| **Process** | Epic → issues with dependency ordering. Each issue has clear acceptance criteria. |
| **Tooling** | GSD milestone/phase breakdown — structured decomposition with verification at each phase ([eval](evaluations/recommended-tools.md#gsd-get-shit-done)) |
| | mattpocock `to-issues` / `to-prd` — convert plans into issue tracker tickets ([eval](evaluations/skills-collections.md)) |
| **Infrastructure** | Task estimation accuracy — compare planned vs. actual session count per issue | Speed |
| | Issue dependency cycle detection — flag circular or stalled chains before work starts | Speed, Correctness |

### Integrate

*Prevents: merge conflicts, divergent implementations, "it worked on my branch" failures*

Merge branches, resolve conflicts, verify end-to-end. This matters most when multiple agents or sessions produce parallel work.

| Layer | What |
|-------|------|
| **Process** | Merge frequently. Run E2E verification after integration, not just unit tests. |
| **Tooling** | [claude-squad](https://github.com/smtg-ai/claude-squad) — manage multiple parallel agent sessions ([eval](evaluations/recommended-tools.md#claude-squad)) |
| | worktrunk — worktree management prevents branch conflicts ([eval](evaluations/worktrunk.md)) |
| **Infrastructure** | Merge conflict frequency per branch — rising conflicts signal architectural coupling | Maintainability |
| | E2E integration test suite in CI — runs after merge, not just per-branch unit tests | Correctness, Safety |

### Retrospect

*Prevents: repeating systemic mistakes, drifting architecture, accumulated technical debt*

What worked across the whole epic? What didn't? Retrospect operates at a higher level than Reflect — it's about patterns across multiple inner-loop iterations, not individual session corrections.

| Layer | What |
|-------|------|
| **Process** | Review the full epic: which tasks went smoothly, which required rework, which assumptions were wrong. Update architecture docs and CLAUDE.md rules. |
| **Tooling** | claude-mem timeline views — see patterns across sessions ([eval](evaluations/memory-systems.md)) |
| | [engram](https://github.com/Gentleman-Programming/engram) — agent-agnostic memory with topic-key upserts and conflict surfacing, portable across 7+ agents ([eval](evaluations/engram.md)) |
| | [mem0](https://github.com/mem0ai/mem0) — relationship-aware memory with entity linking and published retrieval benchmarks, cross-editor support ([eval](evaluations/mem0.md)) |
| | mattpocock `improve-codebase-architecture` — systematic architecture improvement ([eval](evaluations/skills-collections.md)) |
| **Infrastructure** | Retro action completion rate — track whether retrospective actions actually get implemented | All |
| | [Apache DevLake](https://github.com/apache/incubator-devlake) — DORA metrics trend over epics: is lead time/MTTR improving? ([eval](evaluations/apache-devlake.md)) | Speed, Safety |

**Feedback arc:** If retrospective actions consistently don't convert to completed issues, the retro process has failed. Track retro → issue → close rate.

---

## Cross-Cutting: Cost Efficiency

Cost efficiency isn't a stage — it's a property of every stage. A cluster of tools all claim to "save tokens," and the catalog's flat overlap markers make them look interchangeable. They aren't. Map them onto one agent turn — **read inputs → think → write a response → build a solution** — and each attacks a different point. Picking by layer matters: stacking two tools in the same layer is redundant; one from each layer composes.

**Layer 1 — model *input*** (compress/structure tool output *before* it enters the context window):

| Tool | Mechanism & reduction |
|------|----------------------|
| [context-mode](https://github.com/mksglu/context-mode) | MCP-layer sandbox of tool output (~98%) ([eval](evaluations/context-mode.md)) |
| [headroom](https://github.com/headroomlabs-ai/headroom) | Compresses tool output/logs/file reads, reversible via local cache (60–95%) ([eval](evaluations/headroom.md)) |
| [token-optimizer-mcp](https://github.com/ooples/token-optimizer-mcp) | MCP that reduces tool outputs (95%+) ([eval](evaluations/token-optimizer-mcp.md)) |
| [rtk](https://github.com/rtk-ai/rtk) | CLI proxy trimming verbose dev-command output (60–90%) ([eval](evaluations/rtk.md)) |
| [claw-compactor](https://github.com/open-compress/claw-compactor) | Deterministic AST/JSON/log compression, **no LLM inference cost**, reversible (15–82%) ([eval](evaluations/claw-compactor.md)) |
| [lean-ctx](https://github.com/yvgude/lean-ctx) | Local Rust binary, 10 read modes, ~13-tok re-reads, signed savings ledger ([eval](evaluations/lean-ctx.md)) |
| [Pare](https://github.com/Dave-London/Pare) | *Structures* (vs. compresses) git/test/npm/Docker tool interfaces to be compact ([eval](evaluations/pare.md)) |
| [claude-context-optimizer](https://github.com/egorfedorov/claude-context-optimizer) | Diagnostic — flags which high-token files are wasted and prescribes fixes (no live compression) |

**Layer 2 — agent *prose output*** (trim what the model writes back):

| Tool | Mechanism & reduction |
|------|----------------------|
| [caveman](https://github.com/JuliusBrussee/caveman) | Drops filler/articles/pleasantries from responses (~65–75%) ([eval](evaluations/caveman.md)) |

**Layer 3 — what gets *built*** (code restraint — a *different axis*: this isn't a token tool, the savings are a side effect of writing less code):

| Tool | Mechanism |
|------|-----------|
| [ponytail](https://github.com/DietrichGebert/ponytail) | "Lazy senior dev" pre-write decision ladder (YAGNI → stdlib → native → dep → one-liner) with explicit safety carve-outs; benchmarked ([eval](evaluations/ponytail.md)) |
| [andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | CLAUDE.md guidelines derived from known LLM coding pitfalls ([eval](evaluations/andrej-karpathy-skills.md)) |

**Layer 4 — avoid the read entirely** — semantic code search returns the few relevant snippets instead of loading whole files, cutting Layer-1 input at the source. These live under [Code Understanding](CATALOG.md) (`semble`, [serena](https://github.com/oraios/serena), `claude-context`, `cocoindex-code`, `gortex`, `code-context-engine`).

> **Why the distinction bites:** Layers 1–2 are *token-efficiency* plays — same work, smaller bill. Layer 3 is a *code-quality* play whose token savings are incidental. `ponytail`'s own benchmark uses `caveman` as the baseline and beats it on every code metric, precisely because `caveman` only changes how work is *described* while `ponytail` changes what gets *built*. Your global `implementation-discipline.md` already encodes much of Layer 3 by default.

---

## Cross-Cutting: Token tooling — four jobs, four picks

"Monitor token usage" and "optimize token usage" aren't one job — they're **four distinct jobs**, and the [Cost Efficiency](#cross-cutting-cost-efficiency) section above (reduction) and the [Observability](#observability) section below (measurement) each cover some of them without ever connecting the two. Map "which tool do I use?" onto what you actually want to do, pick the one tool for that job, and stop — stacking two tools in the same job is redundant; one per job composes.

| Job | Pick | What you get | Install | Eval |
|-----|------|--------------|---------|------|
| **Monitor — live** | abtop (CONDITIONAL · MEASURED, in STACK) | htop-style TUI showing per-session tokens, cost, context %, and rate limits in real time | `curl --proto '=https' --tlsv1.2 -LsSf https://github.com/graykode/abtop/releases/latest/download/abtop-installer.sh \| sh` | [abtop.md](evaluations/abtop.md) |
| **Monitor — historical** | [ccusage](https://github.com/ccusage/ccusage) (ADOPT · MEASURED, in STACK) | Daily/monthly/session/model token & cost reports parsed from local session logs | `npx ccusage@latest` | [ccusage.md](evaluations/ccusage.md) |
| **Attribute spend / find waste** | codeburn (ADOPT · MEASURED) | Breaks spend down by task/model/tool/project across ~30 tools and emits ranked waste fixes; logged-excluded from STACK — pull in for multi-tool bills (needs Node ≥ 22.13). Secondary: tokencost (CONDITIONAL · RUN) for per-call cost estimation in Python pipelines you control. | `npx codeburn@latest` · `pip install tokencost` | [codeburn.md](evaluations/codeburn.md) · [cost-observability.md](evaluations/cost-observability.md#tokencost) |
| **Reduce / optimize** | caveman (ADOPT · MEASURED, in STACK) | Compresses agent *prose output* (~49–59% measured) with no accuracy loss. For *tool-output* compression, use the [Layer-1 table](#cross-cutting-cost-efficiency) (headroom is the in-STACK pick). | `claude install-skill JuliusBrussee/caveman` | [caveman.md](evaluations/caveman.md) |

**I want to…**

- **…watch a running session burn tokens right now** → abtop (live TUI).
- **…see what last week or month actually cost** → ccusage (historical reports).
- **…find *where* the money went, or what spend never shipped** → codeburn (cross-tool attribution + waste fixes).
- **…price a prompt before I send it**, in a Python pipeline I control → tokencost.
- **…make the model write fewer tokens back** → caveman (prose-output compression).
- **…shrink tool output before it reaches the context window** → the [Layer-1 compression family](#cross-cutting-cost-efficiency) (headroom in STACK; context-mode, token-optimizer-mcp, claw-compactor, lean-ctx as alternatives).

**Evidence honesty.** abtop, ccusage, codeburn, and caveman were all run **hands-on (MEASURED)** — install them with confidence. tokencost was **smoke-tested (RUN)** on its offline OpenAI path (Claude costing routes to Anthropic's API and needs a key). The Layer-1 tool-output compressors other than headroom (context-mode, token-optimizer-mcp, claw-compactor, lean-ctx) are **REVIEW-only** — evaluated from docs/source, not run; try them at your own risk. This mirrors STACK.md's [Tier 1 / Tier 2](STACK.md#evidence-tiers) split.

**Verifying the claims.** Almost every Optimize-cluster entry above advertises a headline % (60–95% fewer tokens, 96% reduction, 50× token reduction) the catalog has *not* reproduced — the loudest claims on the softest evidence. `python3 audit-evals.py --savings-claims` lists every such unverified savings claim across the whole catalog (an in-row `self-reported` disclaimer is bucketed apart as the honest path), turning the backlog into a number to shrink. The [token-savings verification protocol](evaluations/token-savings-protocol.md) is the standard A/B method to reproduce one claim on a fixed corpus and graduate its eval **REVIEW → MEASURED**, promoting the tool toward [STACK Tier 1](STACK.md#evidence-tiers). `caveman` is the worked exemplar — its eval reports a *measured* 49–59% against the vendor's looser headline, which is exactly why it sits in STACK and the REVIEW-only compressors don't.

---

## Cross-Cutting: Security & Supply Chain

Safety runs through every stage, but supply chain security is its own concern — especially as the skill ecosystem grows:

| Tool | What it does |
|------|-------------|
| [SkillSpector](https://github.com/NVIDIA/SkillSpector) — scans skills for prompt injection, data exfiltration, malicious commands ([eval](evaluations/recommended-tools.md#skillspector)) |
| [hol-guard](https://github.com/hashgraph-online/hol-guard) — AI antivirus: 6-step detection pipeline scans plugins, skills, MCP servers before execution ([eval](evaluations/hol-guard.md)) |
| [reporails/cli](https://github.com/reporails/cli) — validates instruction files for conflicts and anti-patterns ([eval](evaluations/recommended-tools.md#reporailscli)) |
| **Agent bounding** — set explicit stop rules: token budgets per task, scope limits, auto-termination conditions. Prevents runaway agents from burning tokens or making unbounded changes. |

---

## Autonomy Tools

These tools don't fit a single stage — they change *how much human involvement* the workflow requires. Adopt when you trust the process and infrastructure enough to reduce your oversight.

| Tool | What it enables |
|------|----------------|
| [ralph-claude-code](https://github.com/frankbria/ralph-claude-code) | Unattended autonomous dev loop with intelligent exit detection and Docker sandboxing ([eval](evaluations/ralph-claude-code.md)) |
| [bernstein](https://github.com/sipyourdrink-ltd/bernstein) | Audit-grade orchestration with tamper-proof logs for autonomous merges ([eval](evaluations/recommended-tools.md#bernstein)) |
| [beads](https://github.com/gastownhall/beads) | Work coordination ledger — prevents duplicate effort across agent fleets ([eval](evaluations/beads.md)) |
| [deer-flow](https://github.com/bytedance/deer-flow) | ByteDance's long-horizon agent runtime: sandboxed execution, sub-agent orchestration, persistent memory (71.5K stars) ([eval](evaluations/deer-flow.md)) |
| [plannotator](https://github.com/backnotprop/plannotator) | Visual review of agent proposals — for when raw diffs aren't enough ([eval](evaluations/recommended-tools.md#plannotator)) |

---

## Observability

Knowing what your agents are doing and whether the workflow is improving requires observability infrastructure:

| Tool | What it provides |
|------|-----------------|
| [langfuse](https://github.com/langfuse/langfuse) | LLM tracing, evals, cost tracking, latency monitoring — production-grade observability ([eval](evaluations/recommended-tools.md#langfuse)) |
| [tokencost](https://github.com/AgentOps-AI/tokencost) | Per-call LLM cost tracking for 400+ models ([eval](evaluations/cost-observability.md#tokencost)) |
| [Infracost](https://github.com/infracost/infracost) | Cloud infrastructure cost estimates — catch expensive Terraform/CDK before deploy ([eval](evaluations/cost-observability.md#infracost)) |
| [abtop](https://github.com/graykode/abtop) | Real-time multi-session agent monitor — htop for AI coding agents ([eval](evaluations/cost-observability.md#abtop)) |
| [Apache DevLake](https://github.com/apache/incubator-devlake) | DORA metrics, engineering throughput, delivery performance dashboards |

---

## Adopting This Workflow

Don't install everything at once. Adopt in layers:

### Start here: Process

Install the skills that enforce discipline. No infrastructure needed — just better habits.

- **CLAUDE.md + rules/** — encode conventions, coding style, commit format, security checks
- **mattpocock/skills** — engineering conventions, grilling, architecture improvement
- **agent-skills** — lifecycle structure with verification gates
- **superpowers** — TDD enforcement, systematic debugging
- **caveman** — reduce token waste from day one

This alone will improve your output. You're running the inner loop with process discipline.

### Add when you want data: Infrastructure

Build the infrastructure that tells you whether the process is working.

- **code-review plugin + pr-review-toolkit** — automated multi-perspective review
- **claude-reflect** — capture corrections, turn them into persistent rules
- **trailofbits/skills** — security audit methodology
- **Coverage gating in CI** — coverage never regresses
- **PR acceptance rate tracking** — reveals what AI does well vs. poorly
- **Flaky test detection** — removes non-determinism

Now you can answer: "Is the workflow producing better code this month than last month?"

### Add when you want autonomy: Orchestration

Once you trust the process and the data confirms it's working, reduce human involvement.

- **claude-mem** — cross-session memory so agents carry context forward
- **GSD** — structured project orchestration for multi-phase work
- **claude-squad** — manage parallel agent sessions
- **worktrunk** — worktree management for concurrent branches
- **headroom + context-mode** — token compression for longer autonomous sessions
- **ralph-claude-code** — unattended autonomous dev loop
- **SkillSpector** — security scanning for skills the system proposes to install

And eventually, when agents merge autonomously:

- **bernstein** — audit-grade orchestration with tamper-proof logs
- **beads** — work coordination to prevent duplicate effort

### Learn the why behind the loop

Tools are only half of it — the mental models matter as much. [LEARNING.md](LEARNING.md)
curates AI/AI-coding YouTube channels and standout videos mapped onto these stages:
foundations (how LLMs work), technique (AI-assisted coding), concepts (RAG/agents/MCP
explainers), and production talks for the outer loop.

---

## Tools Deliberately Excluded

| Tool | Why excluded |
|------|-------------|
| gstack, ECC, ruflo, oh-my-openagent | Overlap with superpowers. Superpowers is the only one with TDD enforcement and auto-triggering ([eval](evaluations/agent-harnesses.md)). |
| compound-engineering | Runner-up harness — lighter weight, good compounding philosophy. Consider if superpowers feels too heavy ([eval](evaluations/compound-engineering.md)). |
| claude-code-staff-engineer | Copy of superpowers with renamed directories and no upstream sync ([eval](evaluations/claude-code-staff-engineer.md)). |
| agentmemory | Overlap with claude-mem. Pick one memory system. Conflicting context is worse than no memory. |
| everything-claude-code (251+ skills) | Too broad. Use targeted skills (mattpocock, agent-skills) instead of a kitchen-sink plugin ([eval](evaluations/everything-claude-code.md)). |
| Flowise, LangGraph | Visual/programmatic agent builders — for building AI products, not for your own dev workflow. |
| OpenHands | Full platform replacement — you're augmenting Claude Code, not replacing it. |
| sandcastle, gastown | Overlap with claude-squad for orchestration. |
| Understand-Anything | Prettier dashboard but no live sync. codegraph ([eval](evaluations/codegraph.md)) + graphify ([eval](evaluations/graphify.md)) cover both live and deep analysis. |
| repomix | Different approach (serialization vs. graph) — useful for feeding code to non-agent LLMs, not needed when agents have file access. |

---

## Evaluations

All recommendations are backed by evidence. See the full evaluations:

**Overlap groups** (compared competitors, picked a winner):
- [Code Understanding](evaluations/code-understanding.md) — graphify + codegraph > Understand-Anything > repomix
- [Agent Harnesses](evaluations/agent-harnesses.md) — superpowers > compound-engineering > gstack > ECC > ruflo
- [Memory Systems](evaluations/memory-systems.md) — claude-mem > agentmemory > OMEGA
- [Skills Collections](evaluations/skills-collections.md) — mattpocock/skills + agent-skills > everything-claude-code
- [Agent Skills (deep dive)](evaluations/agent-skills-addyosmani.md) — full lifecycle ADOPT with doubt-driven-development

**Individual tools** (justified their slot, no direct competitor):
- [Recommended Tools](evaluations/recommended-tools.md) — individual evaluations for tools with no direct competitor

**New tool evaluations** (from catalog scans):
- [Loop 1](discovery/new-tools-loop1.md) — caveman, trailofbits/skills, book-to-skill, humanizer
- [Loop 2](discovery/new-tools-loop2.md) — claude-code-action, shadcn/improve, design-council
- [Loop 3](discovery/new-tools-loop3.md) — CLI-Anything, chrome-devtools-mcp, claude-subconscious, tokencost
- [Loop 4](discovery/new-tools-loop4.md) — Fabric, claude-task-master, scorecard, SimpleMem
- [Loop 5](discovery/new-tools-loop5.md) — andrej-karpathy-skills, autoresearch, google/skills, impeccable
- [Loop 6](discovery/new-tools-loop6.md) — opencode, dify, goose, agentskills
- [Loop 7](discovery/new-tools-loop7.md) — docmd, agent-rules-books, ralph-claude-code, ghostsecurity/skills
- [Loop 8](discovery/new-tools-loop8.md) — last30days-skill, Agent-Reach, llm-council
- [Loop 9](discovery/new-tools-loop9.md) — context-mode, planning-with-files, cognee, ponytail
