# Evaluation: paranoid

**Repo:** [kulchankas/paranoid](https://github.com/kulchankas/paranoid)
**Stars:** 11 | **Last updated:** 2026-09-18 (pushed) | **License:** MIT
**Last verified:** 2026-09-18
**Last triaged:** 2026-09-18  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

An agent skill whose `/hack-me` command breaks into your own running app, proves each bug with a
real request, patches it, and re-verifies — for Claude Code, Codex, and Cursor.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (AXguard, cdmx-in/security-review, ghostsecurity/skills). Not
enough to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: no overlapping STACK pick (P3 backlog). Its self-pentest-prove-patch-
reverify loop is a distinct workflow shape from the scan-only tools in this cluster (`AXguard` finds
and fixes but doesn't loop through re-verification against a live request the same way this claims
to). 11 stars, three days old — worth a real eval if it keeps traction.

_Triaged 2026-09-18 by the daily discovery routine (today's new lead)._
