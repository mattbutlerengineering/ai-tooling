# Evaluation: stalemap

**Repo:** [Umair/stalemap](https://github.com/Umair/stalemap)
**Stars:** 99 | **Last updated:** 2026-10-21 (pushed) | **License:** MIT
**Last verified:** 2026-10-22
**Last triaged:** 2026-10-22  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Diffs a project's dependency types and changelogs against the coding agent's training
cutoff (MIT, CLI + MCP server) and writes a short, targeted note into AGENTS.md/CLAUDE.md
so the agent knows which APIs changed since it was trained.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead
against its closest catalog peers, not to support any verdict, and none is offered here.

## Triage note

Brand new (created 2026-10-19). `landmines` (added in this same pass) targets an
adjacent but distinct problem — known *bugs* in the pinned dependency version vs.
stalemap's *breaking-change/changelog diff since training cutoff*. Neither dominates the
other. No archived flag, no disqualifying license, no `Ships inside` container, minimal
overlap pressure. Left at `discovery-log` for a real hands-on eval rather than SKIPped.

_Triaged 2026-10-22 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [stalemap](https://github.com/Umair/stalemap) | tool | Diffs a project's dependency types and changelogs against the agent's training cutoff (MIT), writing a short note into AGENTS.md/CLAUDE.md | Coding agents assume dependency APIs still match their training data and miss breaking changes shipped since the cutoff | landmines, agents-contract, reporails/cli |
