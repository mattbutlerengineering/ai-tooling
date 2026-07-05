# AI Developer Workflows

A running log of **common AI-assisted development workflows** observed in the wild, refreshed by a twice-daily web-research pass (≈08:30 and ≈20:30 PT).

Each run produces one dated file (`YYYY-MM-DD-<am|pm>.md`) that surveys the workflows developers are actually adopting, with a structured **evaluation** per workflow:

- **What it is** — the workflow in 1–2 sentences
- **Pros** — where it wins
- **Cons** — where it breaks down
- **Suggestions** — how to adopt it well, and which catalog tools support it

These are *workflow patterns* (how people sequence AI tools through the dev loop), distinct from:

- `evaluations/` — hands-on evaluations of individual tools
- `discovery/` — bulk triage logs of newly-found tools

When a workflow here proves durable, fold it into `WORKFLOW.md` (the canonical dev-loop map) and link the supporting tools from `CATALOG.md`.

## Promoted to WORKFLOW.md

Durable patterns that graduated from these logs into the canonical map. Add a row **in the same PR** that edits `WORKFLOW.md`, so the fold-in is never lost.

| Date | Pattern | Where it landed |
|------|---------|-----------------|

No promotions recorded yet — when a pattern from these logs proves durable, add a row here in the same PR that edits `WORKFLOW.md`.

## Index

| File | Theme |
|------|-------|
| [2026-06-19-am.md](2026-06-19-am.md) | Spec-driven development, plan→execute→verify, PR-review bots, multi-agent orchestration |
| [2026-06-19-pm.md](2026-06-19-pm.md) | From solo sessions to overnight fleets: the patterns developers are actually running in mid-2026 |
| [2026-06-20-am.md](2026-06-20-am.md) | Context is the new code: teams shipping reliable agents are winning on context management, verification checkpoints, and code health |
| [2026-06-20-pm.md](2026-06-20-pm.md) | Structure over model: standardizing AI configuration files, test coverage, and orchestration is the primary productivity variable in mid-2026 |
| [2026-06-21-am.md](2026-06-21-am.md) | Reliable by design: self-correcting loops, tool specialization, model cost discipline, long-running harness architecture, and human accountability convert agentic speed into production-safe delivery |
| [2026-06-21-pm.md](2026-06-21-pm.md) | Structured intent over raw prompts: spec files, verifier agents, parallel worktrees, context engineering, and PR governance are hardening agentic output into team-scale production practice |
| [2026-06-22-am.md](2026-06-22-am.md) | Infrastructure first: shadow testing, bounded loop discipline, cross-tool context coordination via AGENTS.md, and code health as AI readiness determine whether agentic development scales or stalls |
| [2026-06-22-pm.md](2026-06-22-pm.md) | From session to system: permission tiers, spec-centric quality control, A2A cross-agent interoperability, and PR governance convert individual agentic sessions into reproducible organizational infrastructure |
| [2026-06-23-am.md](2026-06-23-am.md) | Architecture over tooling: hub-and-spoke orchestration, AI-first SDLC redesign, ReAct execution loops, token-aware model tiering, and complexity-adjusted velocity as the honest measure of agentic productivity |
| [2026-06-23-pm.md](2026-06-23-pm.md) | From prompts to systems: task delegation discipline, spec-driven development convergence, loop engineering, context engineering, and role-specialized agent teams are the operational foundations separating reliable agentic workflows from one-off wins |
| [2026-06-24-am.md](2026-06-24-am.md) | Coordination over capability: conductor-to-orchestrator transition, git worktree isolation, architecture-fit code review, anticipatory human oversight, and workflow-complexity matching are the structural gaps defining agentic maturity in mid-2026 |
| [2026-06-24-pm.md](2026-06-24-pm.md) | Integration over isolation: spec-executable intent, test-woven verification loops, PR review bandwidth governance, full-SDLC coverage, and graph-based orchestration are the structural practices separating production-safe agentic delivery from isolated code-generation spot-use |
| [2026-06-25-am.md](2026-06-25-am.md) | Engineering over prompting: issue-driven delegation, context environments, supervisory governance, resilient orchestration, and usage-scenario verification are converting agentic AI from a code-completion accelerant into a reliable delivery component in mid-2026 |
| [2026-06-25-pm.md](2026-06-25-pm.md) | Discipline over autonomy: shared coding standards, spec-driven contracts, agentic first-pass code review, and plan-execute loop architecture are the workflow primitives separating reproducible team-scale AI delivery from individual speedups in mid-2026 |
| [2026-06-26-am.md](2026-06-26-am.md) | Calibration over automation: context engineering as primary craft, evaluator-optimizer quality loops, delegation depth calibration, and task-scope expansion economics are the operational disciplines that distinguish teams running agents at production scale from those still in the pilot phase in mid-2026 |
| [2026-06-26-pm.md](2026-06-26-pm.md) | Structural discipline over tactical prompting: spec-driven contracts, execution loop design, test-gated self-correction, and agentic SDLC redesign are replacing one-off prompt crafting as the workflow primitives that determine agentic output quality in mid-2026 |
| [2026-06-27-am.md](2026-06-27-am.md) | Governance before scale: the reflection pattern, graduated oversight tiers, ReAct execution discipline, and deliberate build-vs-buy orchestration selection are the structural primitives teams are standardizing before expanding their agentic footprint in mid-2026 |
| [2026-06-27-pm.md](2026-06-27-pm.md) | Task framing, targeted context, spec-driven coordination, and test-gated self-correction are replacing ambient prompting as the workflow primitives that determine agentic output reliability at team scale in mid-2026 |
| [2026-06-28-am.md](2026-06-28-am.md) | Concurrency and cost as the next frontier: parallel worktree fleets, token economy discipline, role-specialized agent pipelines, and PR governance are the structural investments that determine whether agentic throughput translates into delivered value at team scale in mid-2026 |
| [2026-06-28-pm.md](2026-06-28-pm.md) | Spec quality criteria, loop architecture discipline, instruction-file self-check protocols, and graduated oversight classification are the structural layer separating teams that scale agentic development reliably from teams accumulating rework and review debt in mid-2026 |
| [2026-06-29-am.md](2026-06-29-am.md) | Sequential chaining before orchestration, test-woven delegation, three-tier agent tooling, and PR throughput governance are the structural patterns that distinguish teams converting agentic AI into compounding productivity from teams accumulating unverified output and review backlogs in mid-2026 |
| [2026-06-29-pm.md](2026-06-29-pm.md) | Organizational infrastructure over individual practice: spec-executable intent, three-role agent coordination, shared convention files, and AI-first SDLC redesign are the structural investments that convert AI-assisted development from a personal productivity accelerant into a team-scale delivery system in mid-2026 |
| [2026-06-30-am.md](2026-06-30-am.md) | Verification-first design: test-driven delegation, evaluator-optimizer quality loops, least-privilege permission architecture, and sequential prompt chaining are converting agentic code generation from fast-but-opaque into auditable, production-safe delivery in mid-2026 |
| [2026-06-30-pm.md](2026-06-30-pm.md) | MCP standardization, persistent shared context, issue-quality task framing, and spec-first delegation contracts are converting multi-agent AI from bespoke pipeline experiments into production-ready coordination infrastructure in mid-2026 |
| [2026-07-01-am.md](2026-07-01-am.md) | Human oversight tiering, loop architecture as a designed artifact, worktree-isolated parallel execution, and agent-mode selection are the structural disciplines separating teams that scale agentic development reliably from those accumulating unverified output and coordination debt in July 2026 |
| [2026-07-01-pm.md](2026-07-01-pm.md) | Quality debt as the defining challenge: DORA's bug-rate and PR-size data, spec-driven contracts that anchor self-correction loops, coherence-first multi-agent orchestration, and self-correcting build-test-fix loops are the structural responses that distinguish teams converting AI coding volume into reliable output in mid-2026 |
| [2026-07-02-am.md](2026-07-02-am.md) | Context rot as the defining production failure: context engineering discipline, incremental scope bounding, test-suite AI readiness investment, long-running session architecture, and lightweight team governance documentation are the structural practices that separate teams operating agents within their reliable envelope from teams accumulating silent degradation and workflow variance in July 2026 |
| [2026-07-02-pm.md](2026-07-02-pm.md) | The vibe-to-spec transition and the economics of scale: spec-first contracts, tiered model routing, multi-agent fleet coordination, prompt chaining as a gateway architecture, and explicit coding-guideline infrastructure are replacing exploratory prompting as the structural production baseline in July 2026 |
| [2026-07-03-am.md](2026-07-03-am.md) | Loop discipline, delegation scope calibration, procedural memory systems, and three-layer stack architecture are the structural practices distinguishing teams that extract reliable throughput from AI agents from teams still iterating on individual session quality in July 2026 |
| [2026-07-03-pm.md](2026-07-03-pm.md) | Spec-first contracts, the verification tax, orchestration topology selection, and full-lifecycle agentic SDLC redesign are the structural practices separating teams that sustain production-safe agentic throughput from teams accumulating review debt and rework cycles in July 2026 |
| [2026-07-04-am.md](2026-07-04-am.md) | Loop engineering, code health as AI readiness, context engineering as primary craft, and role-specialized agent teams are the structural practices converting agentic AI from fast code generation into reliable, auditable delivery in July 2026 |
| [2026-07-04-pm.md](2026-07-04-pm.md) | Mode selection, spec-anchored delivery, two-layer code review, and orchestration topology design are the structural differentiators converting AI coding from fast generation into aligned, production-safe output in July 2026 |
| [2026-07-05-am.md](2026-07-05-am.md) | Instruction-file standardization, issue-quality task framing, code health as a delegation gate, and loop engineering as a designed artifact are the operational infrastructure practices converting agentic coding from individually configured to collectively reproducible in July 2026 |
