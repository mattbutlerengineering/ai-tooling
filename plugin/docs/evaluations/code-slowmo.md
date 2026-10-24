# Evaluation: code-slowmo

**Repo:** [precious112/code-slowmo](https://github.com/precious112/code-slowmo)
**Stars:** 18 | **Last updated:** 2026-10-20 (pushed) | **License:** MIT
**Last verified:** 2026-10-24
**Last triaged:** 2026-10-24  <!-- triaged: bulk -->
**Dev loop stage:** Plan (codebase onboarding/comprehension before changing it)
**Layer:** Tooling

---

## What it does

A Claude Code skill that builds an interactive HTML explainer instead of a wall of
prose when asked how code works: a clickable system map, a step-by-step timeline
following one action end to end, and a line-by-line run showing the real functions
executing with live values.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell.

## Triage note

Triage banded this as P3 backlog (no overlap-pressure citation from another row).
It sits in the same niche as `rederive` (Socratic re-derivation), `codebase-to-course`
(interactive HTML course), and `PocketFlow-Tutorial-Codebase-Knowledge` (auto-generated
tutorial) — all three already catalogued, none a STACK pick — so there is no clear
incumbent to call this redundant against. Left at `discovery-log` for a real hands-on
eval rather than a mechanical SKIP.

_Triaged 2026-10-24 by the P3 backlog band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [code-slowmo](https://github.com/precious112/code-slowmo) | skill | Builds an interactive system map, step-by-step timeline, and line-by-line run explaining how code works (MIT) | Asking an agent how code works returns a wall of text instead of a navigable visual explainer | rederive, codebase-to-course, PocketFlow-Tutorial-Codebase-Knowledge |
