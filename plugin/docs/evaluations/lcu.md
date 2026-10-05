# Evaluation: lcu

**Repo:** [amontlabs/lcu](https://github.com/amontlabs/lcu)
**Stars:** 296 | **Last updated:** 2026-10-05 (pushed) | **License:** MIT
**Last verified:** 2026-10-05
**Last triaged:** 2026-10-05  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Decouples Codex's computer-use capability from the Codex app so any harness can drive
accessibility-based desktop/browser automation.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. ★296 and actively pushed, which is
real traction for a repo created 2026-09-22, but outside this pass's scope to verify
hands-on.

## Triage note

Left at `discovery-log`, stamped only (P3 backlog — no STACK pick cited). Decent early
traction (★296, 11 forks) for a two-week-old repo, which argues for a real hands-on
eval over a mechanical disposition either way. Sits beside `typesafe-computer-use`,
`cua`, and `nuphus-mcp` as another computer-use capability; worth a closer look in a
future P0 pass given the star growth rather than disposing it here.

_Triaged 2026-10-05 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [lcu](https://github.com/amontlabs/lcu) | tool | Decouples Codex's computer-use capability from the app (MIT) so any harness can drive accessibility-based desktop/browser automation | Computer-use automation is locked inside the Codex app; want the same capability usable from any coding-agent harness | typesafe-computer-use, cua, nuphus-mcp |
