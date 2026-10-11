# Evaluation: OpenLtm

**Repo:** [RohiRIK/OpenLtm](https://github.com/RohiRIK/OpenLtm)
**Stars:** 27 | **Last updated:** 2026-10-11 (pushed) | **License:** MIT
**Last verified:** 2026-10-11
**Last triaged:** 2026-10-11  <!-- triaged: bulk -->
**Dev loop stage:** Memory & Context
**Layer:** Tooling

---

## What it does

A long-term memory layer for AI coding agents — stores project decisions, preferences,
and gotchas in a local SQLite file, then injects relevant memories back into future
sessions. Supports Claude Code, OpenCode, Pi, OpenClaw, and Hermes.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP
that turns on *redundancy with a catalogued incumbent*, not on the tool's behaviour —
a question the overlap answers directly. It would not support an ADOPT, and this eval
offers none.

## Catalog entry

| [OpenLtm](https://github.com/RohiRIK/OpenLtm) | tool | Long-term memory layer (MIT) storing project decisions, preferences, and gotchas in local SQLite, injected back into future sessions | Agent memory of project decisions and known gotchas doesn't persist or carry across Claude Code, OpenCode, Pi, OpenClaw, and Hermes | claude-mem, ownmem, daidocs |  |

## Verdict

**SKIP** — redundant with `claude-mem`, STACK's already-adopted persistent-memory tool.
claude-mem covers the same job (project memory that persists and is retrieved across
sessions) with semantic search, timeline views, and knowledge-graph management;
OpenLtm's cross-harness reach (OpenCode/Pi/OpenClaw/Hermes) doesn't offset giving up
that depth for a 27-star, SQLite-only store on a single harness most users already run.

_Triaged 2026-10-11 by the P2 challenger band._
