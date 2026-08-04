# Evaluation: ralph

**Repo:** [snarktank/ralph](https://github.com/snarktank/ralph)
**Stars:** 21,379 | **Last updated:** 2026-02-02 (pushed) | **License:** MIT
**Dev loop stage:** Implement (autonomous agent loop)
**Layer:** Harness
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

An autonomous agent loop — the "Ralph" pattern of running a coding agent repeatedly against a task
until it converges, rather than a single interactive session.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04) plus
the `CATALOG.md` one-liner and "Overlaps with" cell. Enough to place and band it; not enough for a
positive verdict, and none is offered.

## Triage note

Left at `discovery-log`. Two checks, and the second is the reason it survives where `plandex` did not.

**Maintenance.** Last push 2026-02-02, ~6 months. That is old for this category but well short of
`plandex`'s 13-months-since-release dormancy, and an *autonomous loop* ages differently from a coding
agent: the loop is a pattern over whatever harness you point it at, so it does not rot when model APIs
turn over the way a harness with its own provider integrations does. Worth re-checking, not disposing.

**Redundancy.** Its `Overlaps with` cell names `ralph-claude-code`, `claude-code-harness` and
`Continuous-Claude-v3` — three rows implementing the same Ralph pattern, none of them in STACK, and
this row appears to be the pattern's namesake. That is a cluster with no incumbent, so there is no
redundancy SKIP available; picking a winner among four implementations of one idea needs a measured
comparison, which is P0 work.

Recorded so it is not re-derived: this is the fourth un-adjudicated cluster this triage lane has found
(after the SDD tools, the presentation skills, and the multi-model deliberation CLIs), and the second
in the Implement stage alone.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ralph](https://github.com/snarktank/ralph) | harness | The original autonomous "Ralph" loop — re-runs a coding agent repeatedly until all PRD items are complete (MIT, ★21K) | Want the canonical minimal autonomous agent loop that self-terminates when the PRD is done | ralph-claude-code, claude-code-harness, Continuous-Claude-v3 |
