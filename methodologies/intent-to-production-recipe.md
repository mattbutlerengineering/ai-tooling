# Recipe: intent → production, assembled from open skills

**What this is:** a runnable, end-to-end pipeline that reconstructs an [8090-style Software Factory](8090-software-factory-sdlc.md) from skills and tools we already have — no commercial platform required. Follow it top to bottom and a plain-language idea becomes a merged PR. Each step names the skill, the artifact it produces, a concrete invocation, and the [8090 stage](8090-software-factory-sdlc.md) it stands in for.

```
intent ─▶ /to-prd ─▶ PRD
       ─▶ brainstorming + writing-plans ─▶ plan/spec
       ─▶ /to-issues (+ beads) ─▶ tracer-bullet issues
       ─▶ /implement-issue ─▶ merged PR  ─┐
       ─▶ /triage ◀── feedback/bugs ──────┘   (closes the loop)
       … graphify + claude-mem + CONTEXT.md keep it all linked (cross-cutting)
```

## 1. Intent → PRD  ·  *8090 Requirements*

State the idea in plain language; produce a Product Requirements Document on the issue tracker. This is the front of the loop 8090 argues single-player tools skip.

- **Skill:** `to-prd`
- **Artifact:** a PRD issue (problem, goals, scope, success criteria)
- **Invoke:** `/to-prd` (run against the conversation where you described the intent)
- **8090 stage:** Requirements module → PRD. See the [mapping](8090-software-factory-sdlc.md#mapping-8090-stage--our-dev-loop--our-stack).

## 2. PRD → spec / blueprint  ·  *8090 Blueprints*

Expand the PRD into a concrete plan grounded in the actual codebase — 8090's Feature Nodes. Do it in two moves: explore the design space, then commit a structured plan.

- **Skills:** `brainstorming` (surface intent, options, assumptions) → `writing-plans` (commit a phased plan); optionally the `feature-dev` code-architect agent to anchor the plan in existing patterns.
- **Artifact:** a written plan/spec with phases, risks, and "done" criteria
- **Invoke:** `/brainstorming` → `/writing-plans` (and/or dispatch the `feature-dev:code-architect` agent for an architecture blueprint)
- **8090 stage:** Blueprints / Feature Extraction Agent → Feature Nodes.

## 3. Spec → work orders  ·  *8090 Work Orders / Planner*

Cut the plan into independently-grabbable, codebase-tied tasks — 8090's Work Orders. Use vertical (tracer-bullet) slices so each task is demoable on its own.

- **Skills:** `to-issues` (plan → tracer-bullet issues on the tracker); `beads` to record the dependency graph between them.
- **Artifact:** a set of `ready-for-agent` issues with explicit "Blocked by" links
- **Invoke:** `/to-issues`; track dependencies with the `bd` CLI (`beads`)
- **8090 stage:** Planner → codebase-tied tasks.

## 4. Work order → implementation  ·  *8090 Development*

Take one issue from intent to merged PR. This is the inner loop itself — TDD, verification, review, and ship in one pipeline.

- **Skill:** `implement-issue`
- **Artifact:** a merged PR closing the issue (code, tests, docs)
- **Invoke:** `/implement-issue <issue-number>` (reads the issue → branch → TDD → quality gates → review → PR → CI → merge)
- **8090 stage:** Development (code, tests, docs, infra).
- *Repeat for each work order, blockers first — exactly the loop that produced [#172](https://github.com/mattbutlerengineering/ai-tooling/issues/172)/[#173](https://github.com/mattbutlerengineering/ai-tooling/issues/173)/#174.*

## 5. Feedback → tasks (Validator)  ·  *8090 Validator*

Convert what comes back — user feedback, bug reports, review findings — into new, agent-ready work. This is what closes the loop instead of letting feedback rot.

- **Skill:** `triage`
- **Artifact:** new triaged issues with the right labels, ready to re-enter step 4
- **Invoke:** `/triage` (routes incoming feedback/bugs through the triage state machine)
- **8090 stage:** Validator → new development tasks.

## 6. Knowledge graph (cross-cutting)  ·  *8090 Knowledge Graph*

8090's binding idea is a single source of truth that links requirements ↔ specs ↔ tasks ↔ code and propagates changes. We approximate it with three layers running alongside every step above:

- **Skills/tools:** `graphify` (structure → graph), `claude-mem` (cross-session memory + semantic recall), and a hand-maintained `CONTEXT.md`/ADRs via `domain-modeling`.
- **Artifact:** a queryable graph + durable memory + a glossary/decision record the whole pipeline reads from
- **Invoke:** `/graphify` on demand; `claude-mem` runs passively; edit `CONTEXT.md` and `docs/adr/` as designs evolve
- **8090 stage:** Knowledge Graph (single source of truth).

## Worked example (this repo)

The three issues that built these very docs ran the recipe end to end: an intent ("document 8090's AI SDLC, with steps we can implement ourselves") became a PRD-like plan, was cut by `to-issues` into [#172](https://github.com/mattbutlerengineering/ai-tooling/issues/172) → [#173](https://github.com/mattbutlerengineering/ai-tooling/issues/173) → #174 (blockers first), and each was driven to a merged PR by `implement-issue` under a `/loop`. The control-plane analog — `make check` — gated every merge.

## Gaps vs. 8090

This assembly is honest about where it falls short of an integrated commercial control plane:

- **No unified, auto-propagating graph.** Steps 1–5 produce separate artifacts (PRD, plan, issues, code); the step-6 tools index them but a change does **not** automatically ripple across all of them the way 8090 claims. Re-linking is manual.
- **Coordination is single-player.** The pipeline is one operator running skills in sequence, coordinated through the issue tracker — not 8090's real-time multiplayer mesh with synchronized shared context.
- **Audit = consistency, not decision-capture.** `make check` proves the artifacts are consistent and the git/PR history is the log, but neither records *why* each decision was made the way 8090's control plane claims to. ADRs are the manual stand-in.
- **No turnkey integration.** You wire the steps together yourself. The trade is transparency, adoptability, and zero licensing for the seamlessness of a single product.

See the full stage-by-stage comparison in the [8090 mapping doc](8090-software-factory-sdlc.md).
