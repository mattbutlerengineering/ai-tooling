# Bushido Collective AI-DLC 2026 — an AI-native SDLC, mapped to our dev loop

**What this is:** a reading of [TheBushidoCollective/ai-dlc](https://github.com/TheBushidoCollective/ai-dlc)'s
**AI-DLC 2026** — a community-authored, open-source (Apache-2.0) Claude Code plugin and
[methodology paper](https://github.com/TheBushidoCollective/ai-dlc/blob/main/website/content/papers/ai-dlc-2026.md)
that explicitly extends AWS's own AI-DLC (see [`aws-ai-dlc.md`](aws-ai-dlc.md)) — same core vocabulary
(Intent, Unit, Bolt, Mob Elaboration), credited in the paper's own "Foundational Work" section to *"Raja
SP, Amazon Web Services — AI-Driven Development Lifecycle (AI-DLC) Method Definition (July 2025)."*
Where AWS's public reference implementation (`awslabs/aidlc-workflows`, evaluated here as **SKIP**,
redundant at the task level) leaves Operations "just a directory structure and a TODO note" per our own
evaluation, this fork fills that gap in concretely — which is the main reason it earns a place here rather
than being folded into the existing AWS doc as a footnote. Small project (13 stars as of 2026-08-07,
forked from [`gigsmart/haiku-method`](https://github.com/gigsmart/haiku-method), 24 stars) — cite it as a
methodology reading, not as a popularity signal.

## The AI-DLC 2026 pipeline

Same three phases AWS defined, renamed and filled in:

```
Intent
   → Inception   (Mob Elaboration: decompose Intent into Units, DAG of depends_on,
                   Completion Criteria — specific/measurable/verifiable/independent)
   → Execution   (Bolts, one of three operating modes per Unit — see below)
   → Operations  (file-based specs: Scheduled / Reactive / Process, agent- or human-owned,
                   driven through a unified `/ai-dlc:operate` command)
```

Two ideas run across all three phases rather than living in one of them:

- **Three operating modes (HITL / OHOTL / AHOTL).** Not a ladder — a per-Unit choice. **HITL**
  (Human-in-the-Loop): human approves each major step — novel domains, architectural decisions,
  production-data risk. **OHOTL** (Observed Human-on-the-Loop): *"synchronous awareness with
  asynchronous control — they see what's happening and can redirect, but progress isn't blocked waiting
  for approval"* — subjective/creative work, onboarding, medium-risk iteration. **AHOTL** (Autonomous
  Human-on-the-Loop): runs inside defined boundaries until Completion Criteria are met, human checks in
  periodically — well-defined, programmatically verifiable, batch/overnight work. The paper credits Steve
  Wilson (OWASP) for the HITL/HOTL vocabulary split.
- **Backpressure over prescription.** *"Don't prescribe how; create gates that reject bad work"*
  (attributed to Geoffrey Huntley, creator of the Ralph Wiggum technique — already catalogued here).
  Quality gates (tests, types, lint, security scan, coverage, perf budget) are declared as
  harness-enforced YAML frontmatter on Intent/Unit files; the harness, not the agent, blocks advancement.
  The paper's stated alternative it's reacting against is the *"19-Agent Trap"* — *"as agents accumulate
  tools, they get dumber"* — an explicit argument for fewer, better-scoped agents over elaborate
  multi-agent scaffolding.

## Mapping: AI-DLC 2026 phase → our dev loop → our stack

| AI-DLC 2026 concept | Artifact | Our loop stage | Catalogued tool / skill |
|---|---|---|---|
| Inception (Mob Elaboration) | Units (DAG via `depends_on`), Completion Criteria | Outer **Discover/Architect** → inner **Plan** | `to-prd`, `brainstorming` + `writing-plans` ([superpowers eval](../evaluations/agent-harnesses.md)); `to-issues`/`beads` for the Unit DAG |
| Execution — HITL mode | supervised Bolt | inner **Implement** with human gate each step | `implement-issue` run interactively |
| Execution — AHOTL mode | autonomous Bolt to Completion Criteria | inner **Implement → Verify**, unattended | `implement-issue` run unattended against `tdd` + `code-review`'s gates; this repo's own routines (`docs/agents/routines.md`) already run this mode in production |
| Backpressure gates | YAML-declared quality gates, harness-enforced | **Verify** | `make check` / `audit-evals.py` — the same "harness enforces, agent can't skip" shape, already deterministic and CI-gated here |
| Operations (Scheduled/Reactive/Process specs) | `.ai-dlc/{intent}/operations/*.md`, `/ai-dlc:operate` | outer **Ship**/ongoing — no formalized stage in our loop today | none — see "Where we diverge" |
| Passes (design/product/dev, pass-backs) | typed re-iteration through Inception→Execution by discipline | spans **Plan**/**Review** | no direct analog — closest is re-running `brainstorming` after a `code-review` finding sends work back |

## Stage notes

- **Inception → to-prd/brainstorming/to-issues, same as the AWS mapping.** AI-DLC 2026 keeps AWS's Unit
  decomposition idea and adds an explicit DAG (`depends_on`) enabling fan-out/fan-in parallel execution,
  plus a four-way Completion Criteria bar (Specific/Measurable/Verifiable/Independent) that is stricter
  than what our own `to-issues`/`writing-plans` skills require today — worth stealing as a checklist even
  without adopting the framework.
- **Execution's mode split is the one idea with no equivalent vocabulary in our own docs.** We already
  *practice* the HITL/AHOTL split — an interactive `implement-issue` run vs. an unattended routine per
  `docs/agents/routines.md` — but we have never named the choice as a per-task decision with its own
  criteria the way this paper does. The [practitioner field notes](software-factory-field-notes.md) cover
  a *ladder* of autonomy (Zakariasson's six levels); this is a *mode selector*, not a ladder — the same
  Unit could run AHOTL today and HITL next week depending on risk, not on a team's overall maturity.
  That framing is closer to how `docs/agents/routines.md`'s eliminate-only rule already works: autonomy is
  granted per action-type (SKIP, never ADOPT), not per team level.
- **Backpressure over prescription is precisely this repo's own `make check` philosophy**, independently
  arrived at — declared gates a harness enforces rather than an agent narrating steps it might skip. The
  [software-factories.md](software-factories.md) synthesis already names this as rule 3 of "the ideal
  workflow" (*"a deterministic gate between every pair of stages"*) and credits the same convergence
  across the five vendors and six practitioners it reads; this paper is a seventh, independent source
  landing on the identical shape, credited explicitly to Huntley's Ralph Wiggum philosophy rather than to
  any vendor.
- **Operations is the gap AWS's own reference implementation leaves open, and this fork answers it.**
  Concrete example from the paper — a reactive, agent-owned operation:
  ```yaml
  name: scale-api
  type: reactive
  owner: agent
  trigger: "p99_latency > 150ms for 5m"
  ```
  and a scheduled, human-owned one (`type: process`, quarterly, checklist-based). This is a genuinely
  filled-in answer to the "no formalized Operations phase" gap `aws-ai-dlc.md` calls out — see the
  amendment there.

## Where we diverge

- **No Operations-phase equivalent at all.** Neither `aws-ai-dlc.md`'s mapping nor this repo's own stack
  has a slot for "AI-owned, spec-declared, continuously-running maintenance work." CI/CD and `make check`
  cover **Ship**-time gates, not standing operational rules that fire on a schedule or a metric threshold.
  This is a bigger gap than the one AWS's own doc names, because AI-DLC 2026 actually specifies the shape
  (declarative spec, `agent`/`human` ownership, `/ai-dlc:operate` as a single interface) rather than
  leaving it a placeholder.
- **Passes and pass-backs assume a design/product/dev split this repo doesn't have.** We are a
  single-operator, single-discipline pipeline (as the AWS mapping already notes for AI-DLC generally);
  the Pass mechanism is built for teams with a UX/product/eng split working the same Intent through
  different lenses. Not adoptable here as designed, though the underlying idea — a typed re-entry into
  the same loop from a different angle, with an explicit "this is normal iteration, not failure" framing
  for pass-backs — is a useful reframe of what a `code-review` finding sending work back already does.
- **Small project, not yet battle-tested at scale.** 13 stars, no case study, no measured throughput
  claim of its own (unlike 8090's or EY's vendor numbers, or the practitioner corpus's honest 30–60%).
  Treat the ideas as worth stealing individually — the mode-selection framing, the Operations spec shape,
  the backpressure vocabulary — not as a package to adopt wholesale.

## Sources

Read 2026-08-07 via the repository's own files (README, LICENSE, and the methodology paper at
`website/content/papers/ai-dlc-2026.md`), fetched directly — GitHub content, not third-party coverage.

- [TheBushidoCollective/ai-dlc](https://github.com/TheBushidoCollective/ai-dlc) — Apache-2.0, 13 stars
- [AI-DLC 2026 methodology paper](https://github.com/TheBushidoCollective/ai-dlc/blob/main/website/content/papers/ai-dlc-2026.md)
- [gigsmart/haiku-method](https://github.com/gigsmart/haiku-method) — the fork parent (Studio > Stage >
  Unit > Bolt hierarchy), 24 stars
