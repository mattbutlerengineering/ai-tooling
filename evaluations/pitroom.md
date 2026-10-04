# Evaluation: pitroom

**Repo:** [ATASTECH/pitroom](https://github.com/ATASTECH/pitroom)
**Stars:** 24 | **Last updated:** 2026-10-04 (pushed) | **License:** MIT
**Last verified:** 2026-10-04
**Last triaged:** 2026-10-04  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A development tool (TypeScript, ★24, created 2026-09-30) that delegates code reading,
fixes, and reviews to parallel cheap AI workers, while the primary (expensive) agent
keeps the decision-making — pitched as "the superpowers development workflow, run by
cheap workers."

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead
against its closest catalog peers, not to support any verdict, and none is offered here.

## Triage note

Overlaps `opus-manager` (discovery-log — "delegating implementation to cheaper AI CLIs,
verifying results") most closely; neither is a STACK pick, so this does not band as a
P2 challenger. Its pitch explicitly references "the superpowers development workflow"
(GSD, a STACK ADOPT pick) as the pattern being run cheaply, but it does not replace GSD
itself — it is a cost-delegation layer that could sit alongside it, not a competing
Plan->Execute loop. No archived flag, no disqualifying license, no `Ships inside`
container. Left at `discovery-log`.

_Triaged 2026-10-04 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [pitroom](https://github.com/ATASTECH/pitroom) | tool | Pit crew (MIT) for your coding agent — delegates reading, fixes, and reviews to parallel cheap AI workers while your primary agent decides | Running every step on the expensive model wastes spend when cheaper workers can read, fix, and flag issues first | opus-manager, claude-octopus, cline-pilot |
