# Evaluation: varve

**Repo:** [rittenpoems-beep/varve](https://github.com/rittenpoems-beep/varve)
**Stars:** 3 | **Last updated:** 2026-09-26 (pushed) | **License:** MIT
**Last verified:** 2026-09-30
**Last triaged:** 2026-09-30  <!-- triaged: bulk -->
**Dev loop stage:** Reflect
**Layer:** Infrastructure

---

## What it does

A zero-dependency, zero-LLM cross-session memory layer for coding agents — a three-layer
(environment/status/history) append-only injection with SQLite FTS5 recall.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead, not to support an
ADOPT, and none is offered here.

## Triage note

Left at `discovery-log`. `OMEGA` is not itself a STACK pick and `ownmem`/`okf-agent-memory` are
`discovery-log`, so this isn't a P2 redundancy call. Only 3 stars and days old — no adoption signal
— but the "zero LLM call to recall" design (plain SQLite FTS5, not an embeddings/vector store) is a
genuinely different mechanism from most of the Memory & Context cluster, worth a real look rather
than a mechanical dismissal.

_Triaged 2026-09-30 by the P3 backlog band (today's new lead)._
