# Evaluation: flawless-ui-ux

**Repo:** [smokeeaasd/flawless-ui-ux](https://github.com/smokeeaasd/flawless-ui-ux)
**Stars:** 186 | **Last updated:** 2026-11-06 (pushed) | **License:** MIT
**Last verified:** 2026-11-09
**Last triaged:** 2026-11-09  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Process

---

## What it does

A skill for coding agents that pushes generated UI/UX toward distinctive, usable designs
instead of the generic, interchangeable layouts agents default to.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner and its "Overlaps with" cell (`ui-ux-pro-max`, `frontend-design`,
`impeccable`). That is sufficient to check for a named STACK redundancy; it is not
sufficient to support an ADOPT, and this eval offers none.

## Verdict

**discovery-log — tentative read** — a fast-growing (186 stars in under a week) design
skill. It overlaps conceptually with `frontend-design` (an installed STACK pick) and
`ui-ux-pro-max`, but a bulk pass cannot judge whether its specific rules add anything over
the incumbent without actually comparing outputs — that comparison is a human/P2 call, not
a mechanical one, so it is left at `discovery-log` rather than SKIPped on overlap alone.

## Triage note

Left at `discovery-log` for the P0/eval-runner lane; a future P2 pass should compare its
design rules against `frontend-design`'s before any redundancy SKIP.

_Triaged 2026-11-09 by the daily discovery-and-triage routine._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [flawless-ui-ux](https://github.com/smokeeaasd/flawless-ui-ux) | skill | Skill (MIT) for coding agents to design distinctive, usable interfaces instead of generic AI-template UIs | Agent-built UIs default to bland, interchangeable layouts with nothing pushing toward distinctive, usable design | ui-ux-pro-max, frontend-design, impeccable |
