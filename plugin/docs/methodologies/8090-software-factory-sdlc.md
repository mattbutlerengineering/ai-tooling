# 8090 Software Factory — an AI-native SDLC, mapped to our dev loop

**What this is:** a stage-by-stage reading of [8090's Software Factory](https://www.8090.ai/) — a commercial *"AI-native SDLC control plane"* (co-launched with EY as the EY.ai PDLC) — translated into this repo's [inner/outer dev loop](../WORKFLOW.md) and the catalogued tools/skills that fill each role. The product itself is closed and unadoptable (see the [catalog entry](../CATALOG.md) and the [evaluation](../evaluations/8090-software-factory.md), verdict **SKIP**); the *methodology* is the takeaway. This doc maps it; the companion recipe ([#174](https://github.com/mattbutlerengineering/ai-tooling/issues/174)) operationalizes it from open skills.

## The 8090 pipeline

8090's thesis is that "single-player" AI coding tools are fast but sloppy because they skip the front of the lifecycle (requirements, architecture, planning) and leave no auditable trail. Software Factory orchestrates the whole loop instead, as a chain of modules that each emit a durable artifact, all bound by a knowledge graph and an audit-trail control plane:

```
Business intent
   → Requirements (PRD)
   → Blueprints / Feature Extraction Agent (Feature Nodes)
   → Work Orders / Planner (codebase-tied tasks)
   → Development (code, tests, docs, infra)
   → Validator (feedback → new tasks)  ─┐
   ↑                                     │  knowledge graph = single source of truth
   └──────── closes the loop ────────────┘  control plane = audit / visibility / oversight
```

## Mapping: 8090 stage → our dev loop → our stack

| 8090 stage | Artifact | Our loop stage | Catalogued tool / skill |
|---|---|---|---|
| Requirements | PRD | Outer **Discover/Architect** → inner **Plan** | mattpocock `to-prd` ([eval](../evaluations/skills-collections.md)) |
| Blueprints (Feature Extraction Agent) | Feature Nodes / specs | inner **Plan** (outer **Architect**) | `brainstorming` + `writing-plans` ([superpowers eval](../evaluations/agent-harnesses.md)); `feature-dev` code-architect ([eval](../evaluations/feature-dev.md)) |
| Work Orders / Planner | codebase-tied tasks | outer **Decompose** | mattpocock `to-issues` ([eval](../evaluations/skills-collections.md)); `beads` for dependency tracking ([eval](../evaluations/beads.md)) |
| Development | code, tests, docs, infra | inner **Implement → Verify → Review → Ship** | `implement-issue` (the issue→merge pipeline skill — composes TDD, review, CI, merge) |
| Validator | feedback → new tasks | inner **Reflect** / outer **Retrospect** | `triage` (feedback/bugs → agent-ready issues) |
| Knowledge Graph *(cross-cutting)* | linked, propagating artifacts | spans **Plan** + **Reflect** | `graphify` ([eval](../evaluations/graphify.md)); `claude-mem` ([eval](../evaluations/memory-systems.md)); `codegraph` ([eval](../evaluations/codegraph.md)); CONTEXT.md via `domain-modeling`/`codebase-design` ([eval](../evaluations/domain-modeling.md)) |
| Control plane *(cross-cutting)* | audit trail / visibility | **Ship/Verify** gates | this repo's integrity gates — `make check` / `audit-evals.py` (deterministic, CI-gated) |

## Stage notes

- **Requirements → `to-prd`.** 8090 has business leaders state intent in plain language, producing a PRD before code. `to-prd` does exactly this against our issue tracker — intent in, a published PRD out. This is the outer-loop **Discover/Architect** work feeding the inner-loop **Plan**.
- **Blueprints → brainstorming + writing-plans + feature-dev.** 8090's Feature Extraction Agent expands a PRD into structured Feature Nodes. Our equivalent is the **Plan** stage: `brainstorming` to explore intent and surface assumptions, `writing-plans` to commit a structured plan, and `feature-dev`'s code-architect to ground specs in existing codebase patterns.
- **Work Orders → to-issues + beads.** 8090's Planner turns specs into codebase-tied tasks naming files to touch. `to-issues` cuts a plan into tracer-bullet vertical slices on the tracker (outer **Decompose**); `beads` tracks the dependency graph between them.
- **Development → implement-issue.** 8090's agents write code/tests/docs/infra. Our `implement-issue` skill is the inner loop itself — it wraps TDD (**Implement**), behavior checks (**Verify**), dual-axis review (**Review**), and PR/CI/merge (**Ship**) into one issue→merge pipeline.
- **Validator → triage.** 8090 converts user feedback into new development work, closing the loop. `triage` does this: it routes feedback and bugs through a state machine into agent-ready issues — the inner-loop **Reflect** arc / outer-loop **Retrospect**.

## Cross-cutting: knowledge graph & control plane

- **Knowledge graph as single source of truth.** 8090's strongest idea: link requirements↔architecture↔implementation so a change propagates and specification drift is caught. We approximate this with `graphify` (structure → graph), `claude-mem` (cross-session memory), `codegraph` (always-on code graph), and hand-maintained `CONTEXT.md`/ADRs via `domain-modeling`. The honest gap: these are *separate* stores, not one auto-propagating graph spanning every artifact (see "Where we diverge").
- **Control plane / audit trail.** 8090 keeps "full control, visibility, and auditability over every decision." Our analog is this repo's deterministic integrity suite — `make check` (`audit-evals.py` detectors A/B/D/G/J/K, plus reconcile/backfill/tier-stack/sync) gates every change in CI, and the git/PR history is the decision log. It enforces consistency rather than narrating intent, but it is auditable and reproducible.

## Where our open-tool stack diverges from 8090

- **No unified, auto-propagating knowledge graph.** Our memory/graph tools are independent; a requirement change does not automatically ripple into specs, tasks, and code the way 8090 claims. Propagation is manual (re-run, re-link).
- **Coordination is manual / single-player.** 8090 sells "multiplayer" real-time co-creation with synchronized context across PM/eng/business. Our pipeline is one operator driving skills in sequence, coordinated through the issue tracker — not a live shared mesh.
- **Audit is consistency-enforcement, not decision-capture.** Our gates prove the artifacts are *consistent*; they don't record *why* each decision was made the way 8090's control plane claims to. ADRs + commit history are the manual stand-in.
- **No SLA / commercial guarantees.** 8090's "80x faster / 95%+ coverage" are vendor claims for an integrated product; an assembled open-tool pipeline trades that integration for transparency, adoptability, and zero licensing.
