# Evaluation: pm-manager

**Repo:** [wei63w/pm-manager](https://github.com/wei63w/pm-manager)
**Stars:** 69 | **Last updated:** 2026-08-04 (pushed) | **License:** MIT
**Dev loop stage:** Plan (spec-driven development)
**Layer:** Process
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

A local `.pm` governance skill pack that gives an agent a lightweight backlog and priority system so
it can decide what to work on next.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata fetched fresh for this pass on
2026-08-04 (the slug had no cached record) plus the CATALOG one-liner and "Overlaps with" cell
(`spec-kit`, `OpenSpec`, `planning-with-files`). Sufficient for a SKIP that turns on being derivative of a
catalogued incumbent; not sufficient for a positive verdict, and none is offered.

## Verdict

**SKIP** — derivative of a lead it does not improve on. The CATALOG one-liner describes it as *"Spec
Kit-inspired"*, and [`spec-kit`](https://github.com/github/spec-kit) is a **P0 lead** in this queue with
GitHub behind it and the largest ecosystem in the spec-driven-development cluster.

Nothing here names a capability the source lacks. A local `.pm` directory holding backlog and priority is
what `planning-with-files` already does for plan persistence, and deciding what to work on next is the job
`beads` models as a dependency graph.

★69 and pushed today, so this is a new and actively-developed project — the disposition is about position
in an over-supplied cluster, not effort. The Plan stage carries nine-plus spec-driven workflow entries
(recorded in full on `spec_driven_develop`); the ones worth keeping are those with a named independent
design, and self-describing as inspired by a P0 lead is the opposite of that.

MIT, so the ideas are freely borrowable regardless of the verdict, which is the useful outcome for a small
skill pack.

Re-open if it develops something spec-kit does not do.
_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [pm-manager](https://github.com/wei63w/pm-manager) | skill | Local `.pm` governance skill pack (Spec Kit-inspired) that tells agents what to fix next | Agents lack a lightweight, local backlog/priority system to decide what to work on next | spec-kit, OpenSpec, planning-with-files |
