# Evaluation: debroid

**Repo:** [PatilShreyas/debroid](https://github.com/PatilShreyas/debroid)
**Stars:** 32 | **Last updated:** 2026-08-06 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-08-06
**Last triaged:** 2026-08-06  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

Autonomous, headless Android debugger designed for AI coding agents — inspect runtime memory, set breakpoints, and debug live apps, rather than reading logcat after the fact.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata (README, topics, license) via the GitHub API, plus the CATALOG "Overlaps with" cell.

## Triage note

Left at `discovery-log`: no catalogued tool gives agents real breakpoint/runtime-memory
debugging for Android specifically — `DebugMCP` is VS Code/desktop debugging and
`dev3000` is web-app timeline capture. Genuinely differentiated capability; worth a
first-time eval rather than a mechanical SKIP.

_Triaged 2026-08-06 by the daily discovery routine._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [debroid](https://github.com/PatilShreyas/debroid) | tool | Autonomous, headless Android debugger for AI coding agents (Apache-2.0) — inspect runtime memory, set breakpoints, and debug live apps | Agents debugging Android apps can't set breakpoints or inspect runtime state, only read logs after the fact | DebugMCP, dev3000, chrome-devtools-mcp |
