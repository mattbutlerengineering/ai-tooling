# Evaluation: loopy

**Repo:** [forward-future/loopy](https://github.com/Forward-Future/loopy)
**Stars:** 2,965 | **Last updated:** 2026-07-26 (pushed) | **License:** MIT
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Plan / Reflect (workflow design)
**Layer:** Process

---

## What it does

A library of practical AI-agent loops, plus an installable skill for finding, adapting and
designing repeatable agent workflows. The catalogue of patterns is the artifact; the skill is the
way an agent reaches into it.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata fetched 2026-08-04 plus
the CATALOG one-liner and "Overlaps with" cell (`softaworks/agent-toolkit`, `harness`,
`superpowers`). Enough to place it against the STACK incumbent it names; not enough for a positive
verdict, and none is offered.

## Triage note

Left at `discovery-log`, not SKIPped. It was banded against
[`GSD`/superpowers](https://github.com/obra/superpowers) (STACK), but the two do different things:
superpowers *enforces* a structured workflow (milestones, phases, discovery discussion), while
loopy is a *catalogue of loop patterns* you choose from and adapt. An enforcer and a pattern
library are complements — you consult one to decide what the other should run.

It is also unusually on-topic for this repo specifically. `WORKFLOW.md` is itself a hand-maintained
library of dev-loop stages and the feedback arcs between them; an externally maintained catalogue
of agent loops is either a source to reconcile against or a competitor to it, and both readings are
worth a real look rather than a mechanical SKIP.

The open question is whether the patterns are substantive or a listicle — which is exactly what a
bulk pass has not read. P0/reference work.

_Triaged 2026-08-04 by the P2 challenger band ([#263](https://github.com/mattbutlerengineering/ai-tooling/issues/263))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [loopy](https://github.com/Forward-Future/loopy) | skill | Library of practical AI-agent loops (MIT, ★2.3K) + installable skill for finding and designing agent workflows | Knowing which agent loop to reach for, instead of reinventing a workflow per task | softaworks/agent-toolkit, harness, superpowers |
