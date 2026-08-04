# Evaluation: Finn-loop

**Repo:** [finna/Finn-loop](https://github.com/finna/Finn-loop)
**Stars:** 290 | **Last updated:** 2026-07-23 (pushed) | **License:** MIT
**Dev loop stage:** Plan (spec-driven development)
**Layer:** Process
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

A three-skill software-factory loop for Claude Code — spec, build, review — with humans doing the
merge.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata fetched fresh for this pass on
2026-08-04 (the slug had no cached record) plus the CATALOG one-liner and "Overlaps with" cell
(`spec-kit`, `ccpm`, `flow-next`, `OpenSpec`). Enough to place it in the cluster; not enough for a positive
verdict, and none is offered.

## Triage note

Left at `discovery-log`. It sits in the spec-driven cluster whose scale is recorded on `spec_driven_develop`
in this pass — nine-plus entries answering one question, resolvable by one measured comparison rather than
nine eliminations.

Two things keep it out of the disposal that `pm-manager` received. It does not describe itself as derived
from a catalogued lead; three skills covering spec, build and review is a small independent design rather
than a reimplementation. And the **human merge checkpoint** is a named position, not a missing feature: most
of this cluster optimizes for how much the agent can carry unattended, and deliberately putting a person at
the merge is the opposite bet. Whether that bet is right is a question about how you want to work, and this
lane does not answer those.

At ★290 it is small, and MIT, and pushed 2026-07-23 — active. The honest read is that there is not yet
enough signal in either direction, which is what leaving a lead at `discovery-log` is for.

No eval file existed before this pass; this stub is the placeholder, not an evaluation.
_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Finn-loop](https://github.com/finna/Finn-loop) | skill | 3-skill AI software factory for Claude Code — spec, build, review, humans merge | Ad-hoc "vibe coding" skips spec and review gates; want a lightweight scaffolded loop with a human merge checkpoint | spec-kit, ccpm, flow-next, OpenSpec |
