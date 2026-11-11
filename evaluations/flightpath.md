# Evaluation: flightpath

**Repo:** [dk-labs-dev/flightpath](https://github.com/dk-labs-dev/flightpath)
**Stars:** 4 | **Last updated:** 2026-11-10 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-11-11
**Last triaged:** 2026-11-11  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

Records every Claude Code session live, draws the journey as a map, and — per the repo's own
description — coaches the next session.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata (fetched 2026-11-11) plus the CATALOG one-liner and "Overlaps with" cell. That is
sufficient to decide whether this lead is clearly dominated by a cataloged incumbent, not to
judge the tool's actual behavior — it would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped as redundant with `claude-reflect` (STACK, MEASURED)
despite the P2 band pointing there. claude-reflect's mechanism is capturing corrections and
preferences into persistent CLAUDE.md rules; flightpath's stated mechanism is a visual replay
of the session (drawing the journey as a map) with coaching as a described side effect — a
different artifact (a map/replay) toward a related but not identical goal (carrying something
forward into the next session). The overlap is thematic, not a same-job duplicate, so this
isn't the clean P2 case; worth a closer look at what "coaches" actually means in practice
before concluding either way.

_Triaged 2026-11-11 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [flightpath](https://github.com/dk-labs-dev/flightpath) | tool | Records every Claude Code session live (Apache-2.0), draws the journey as a map, and coaches the next session | A finished agent session leaves no visual record of its path, and no coaching carried forward into the next session | tracecrate, bar-observatory, claude-reflect |
