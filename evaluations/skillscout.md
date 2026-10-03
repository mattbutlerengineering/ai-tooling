# Evaluation: skillscout

**Repo:** [flaviocopes/skillscout](https://github.com/flaviocopes/skillscout)
**Stars:** 50 | **Last updated:** 2026-10-03 (pushed) | **License:** MIT
**Last verified:** 2026-10-03
**Last triaged:** 2026-10-03  <!-- triaged: bulk -->
**Dev loop stage:** Plan (skill management)
**Layer:** Tooling

---

## What it does

A macOS app (Swift, ★50, created 2026-09-30) that shows which skills your coding agents
load, which agents can use each one, and how often you actually use them.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead
against its closest catalog peers, not to support any verdict, and none is offered here.

## Triage note

Brand new today (created 2026-09-30). Its "Overlaps with" cell names `skills-hub`,
`skill_manager`, and `agent-skill-sync` — none of which is a STACK pick, so this does not
band as a P2 challenger. No archived flag, no disqualifying license, no `Ships inside`
container. Those peers manage/sync skill *files* across tools; this one's differentiator is
usage analytics (which skills actually load, and how often), a job none of the existing
peers does. Left at `discovery-log` for a real hands-on eval.

_Triaged 2026-10-03 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [skillscout](https://github.com/flaviocopes/skillscout) | tool | macOS app (MIT) showing which skills your coding agents load, which agents can use each one, and how often | Can't tell which installed skills your agents actually load or use without inspecting each config by hand | skills-hub, skill_manager, agent-skill-sync |
