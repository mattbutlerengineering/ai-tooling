# Evaluation: landmines

**Repo:** [devanshranjan10/landmines](https://github.com/devanshranjan10/landmines)
**Stars:** 7 | **Last updated:** 2026-10-21 (pushed) | **License:** MIT
**Last verified:** 2026-10-22
**Last triaged:** 2026-10-22  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Known open bugs for a project's exact dependency versions (MIT), surfaced to a coding
agent via AGENTS.md/CLAUDE.md, a pre-edit hook (claims support for ~20 agents), and an
MCP server.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead
against its closest catalog peers, not to support any verdict, and none is offered here.

## Triage note

Brand new (created 2026-10-21, one day old). Targets *known open bugs in the pinned
version*, distinct from `stalemap`'s *breaking-change diff since training cutoff* — added
in this same pass; neither dominates the other. No archived flag, no disqualifying
license, no `Ships inside` container. Left at `discovery-log`; too new (★7, 1 day old) for
a confident SKIP or a hands-on eval yet.

_Triaged 2026-10-22 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [landmines](https://github.com/devanshranjan10/landmines) | tool | Known open bugs for your exact dependency versions (MIT), surfaced via AGENTS.md/CLAUDE.md, a pre-edit hook for ~20 agents, and an MCP server | An agent writes code against a dependency version with known open bugs it has no way to see before hitting them | stalemap, reporails/cli |
