# Evaluation: coding.sh

**Repo:** [jackulau/coding.sh](https://github.com/jackulau/coding.sh)
**Stars:** 7 | **Last updated:** 2026-11-11 (pushed) | **License:** MIT
**Last verified:** 2026-11-11
**Last triaged:** 2026-11-11  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

An open-source, local-first observability and evals layer for AI agents — per the repo's own
description, it shows what Claude Code, Codex, Cursor, and other coding agents did and what it
cost.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata (fetched 2026-11-11) plus the CATALOG one-liner and "Overlaps with" cell. That is
sufficient to decide whether this lead is clearly dominated by a cataloged incumbent, not to
judge the tool's actual behavior — it would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped as redundant with `ccusage` (STACK, MEASURED) despite the
P2 band pointing there. ccusage's job is narrowly cost reports from session logs; coding.sh's
own description adds an "evals" dimension ccusage does not attempt, on top of cost and
cross-tool (Claude Code/Codex/Cursor) observability. Broader stated scope than the incumbent
it was banded against, so this is not a clean identical-job overlap — worth a closer,
differentiated look rather than a mechanical SKIP on the shared cost-tracking citation.

_Triaged 2026-11-11 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [coding.sh](https://github.com/jackulau/coding.sh) | tool | Open-source, local-first observability and evals (MIT) showing what Claude Code, Codex, Cursor, and others did and what it cost | Seeing what a coding agent actually did and what it cost means parsing raw session logs by hand, with no local observability/evals layer | ccusage, peek, tracecrate |
