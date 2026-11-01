# Evaluation: thenwise

**Repo:** [dheerajponnaganti/thenwise](https://github.com/dheerajponnaganti/thenwise)
**Stars:** 29 | **Last updated:** 2026-11-01 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-11-01
**Last triaged:** 2026-11-01  <!-- triaged: bulk -->
**Dev loop stage:** Memory & Context
**Layer:** Infrastructure

---

## What it does

A local memory of past Claude Code work (Apache-2.0), searchable by date and link — recall what a past session did without re-scrolling scrollback.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell (claude-mem, jevmem, OMEGA). That is sufficient for a SKIP that turns on redundancy with a catalogued incumbent, not on the tool's behavior — a question the overlap answers directly. It would not support an ADOPT, and this eval offers none.

## Verdict

**SKIP** — redundant with `claude-mem` (ADOPT, MEASURED, in STACK). Both solve the same job — recalling what happened in past Claude Code sessions — and claude-mem already covers it with semantic search, timeline views, and knowledge-graph management. thenwise's feature set (searchable by date and link) is a strict subset of what claude-mem already does, with no differentiating angle stated.

_Triaged 2026-11-01 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [thenwise](https://github.com/dheerajponnaganti/thenwise) | MCP server | Local memory of past Claude Code work (Apache-2.0), searchable by date and link | Recalling what a past Claude Code session did on this machine means re-scrolling scrollback with nothing searchable | claude-mem, jevmem, OMEGA |
