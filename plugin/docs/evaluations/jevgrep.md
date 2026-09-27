# Evaluation: jevgrep

**Repo:** [dzhng/jevgrep](https://github.com/dzhng/jevgrep)
**Stars:** 430 | **Last updated:** 2026-09-27 (pushed) | **License:** MIT
**Last verified:** 2026-09-27
**Last triaged:** 2026-09-27  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

A CLI for coding agents that finds relevant files and source context by asking what
code *does* rather than grepping for a filename or exact keyword. It routes the
natural-language query through Jev (TypeSafe's "System One" decision model) to return
candidate files, reading leads, and verbatim source excerpts.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the README's own description of the CLI's inputs/outputs. That is
sufficient for a discovery-log entry, not for an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`. It cites `serena` in Overlaps with, but the mechanism differs:
serena is IDE-grade, LSP-backed symbol navigation (find/reference/rename/refactor
across 40+ languages); jevgrep is a natural-language "what does this do" query routed
through a separate decision model, closer in spirit to `semble`/`trace-mcp`'s
retrieval-by-meaning than to symbol-level editing. Not clearly dominated by the
existing Code Understanding cluster, so left rather than SKIPped as redundant.

Also worth flagging for whoever runs a hands-on eval: `dzhng` (and `Jev`/"TypeSafe AI"
generally) has a wave of similarly-branded repos surfacing in discovery searches this
week (`jevcore`, `jev-judge-mcp`, `quicksilver`, `building-with-typesafe-jev`,
`awesome-jev`, `system1-agents`) — worth checking whether Jev is a real, independently
verifiable decision model before treating a cluster of these as a differentiated
category rather than one product's marketing surface.

_Triaged 2026-09-27 by the P2 challenger band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [jevgrep](https://github.com/dzhng/jevgrep) | tool | CLI for coding agents (MIT) that finds relevant files and source context by asking what code does, via Jev's decision model | Locating code in an unfamiliar codebase means grepping by filename or exact keyword instead of by what it actually does | serena, semble, trace-mcp |
