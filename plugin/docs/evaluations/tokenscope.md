# Evaluation: TokenScope

**Repo:** [AviVAvi/TokenScope](https://github.com/AviVAvi/TokenScope)
**Stars:** 6 | **Last updated:** 2026-07-23 (pushed) | **License:** MIT
**Last verified:** 2026-07-29
**Last triaged:** 2026-07-29  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling (local CLI)

---

## What it does

Profiles the session logs Claude Code already writes and scores each project's context hygiene
0-100, generating fixes backed by measured numbers; local, zero deps, no telemetry. Surfaced in
the 2026-07-29 daily discovery scan.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (`ccusage`, `claude-monitor`, `abtop`, `codeburn`). `ccusage`
is ADOPT/KEEP in STACK.md, but ccusage's job is token/cost *reporting* from session logs, while
TokenScope's job is a *context-hygiene score* (0-100) with prescriptive fixes — a diagnostic
angle none of the four named overlaps provide, so a mechanical SKIP isn't defensible from
metadata alone.

## Triage note

Left at `discovery-log`: very low stars (6, 6 days old) but a distinct diagnostic job from the
cost-reporting incumbents. Worth a real eval once it has more signal of traction.

_Triaged 2026-07-29 by the daily discovery scan's same-day triage pass._
