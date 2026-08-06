# Evaluation: portly

**Repo:** [Melvynx/portly](https://github.com/Melvynx/portly)
**Stars:** 30 | **Last updated:** 2026-08-04 (pushed) | **License:** MIT
**Last verified:** 2026-08-06
**Last triaged:** 2026-08-06  <!-- triaged: bulk -->
**Dev loop stage:** Dev Workflow
**Layer:** Tooling

---

## What it does

Native macOS supervisor (Swift) for every local development server — start, stop, and monitor them from one place instead of hunting terminals.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata (README, topics, license) via the GitHub API, plus the CATALOG "Overlaps with" cell.

## Triage note

Left at `discovery-log`: no catalogued tool does exactly this job (macOS-native
supervision of many concurrent local dev servers), so there is no settled incumbent
to call it redundant with. Narrow but genuinely differentiated; worth a first-time
eval rather than a mechanical SKIP.

_Triaged 2026-08-06 by the daily discovery routine._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [portly](https://github.com/Melvynx/portly) | tool | Native macOS supervisor (MIT, Swift) for every local development server — start/stop/monitor from one place | Agents (and humans) spin up many local dev servers by hand across projects with no single place to see or manage them | claude-code-templates, dev3000 (complementary: portly = process supervision, dev3000 = debugging timeline) |
