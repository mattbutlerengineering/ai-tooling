# Evaluation: neuromesh

**Repo:** [pinoox/neuromesh](https://github.com/pinoox/neuromesh)
**Stars:** 72 | **Last updated:** 2026-08-28 (pushed) | **License:** MIT
**Last verified:** 2026-08-28
**Last triaged:** 2026-08-28  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

A context engine for AI coding assistants that "folds" large codebases into compact evidence packets — builds a neural graph in RAM, collapses unused functions into one-line markers, and expands them on demand, integrating with Cursor, VS Code, Claude, and Codex via CLI/MCP.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for the disposition below, which turns on *redundancy with a catalogued incumbent*, not on the tool's behaviour. It would not support an ADOPT, and this eval offers none.

## Triage note

Cites `serena` (a STACK pick) in its "Overlaps with" cell, putting this lead in the P2 challenger band. Left at `discovery-log` rather than SKIPped: the mechanism looks meaningfully different from serena's LSP symbol-level retrieval/editing — a compression/folding approach to context size rather than semantic navigation — so a redundancy claim is not clearly defensible without hands-on comparison. Significant enough (self-reported 97-99% token savings, multi-IDE integration) to deserve a real eval rather than a mechanical SKIP.

_Triaged 2026-08-28 by the P2 challenger band._
