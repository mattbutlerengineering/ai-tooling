# Evaluation: claudes-workbench

**Repo:** [a-schaefers/claudes-workbench](https://github.com/a-schaefers/claudes-workbench)
**Stars:** 11 | **Last updated:** 2026-11-20 (pushed) | **License:** MIT
**Last verified:** 2026-11-20
**Last triaged:** 2026-11-20  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A Claude Code plugin that pairs Claude (as planner/reviewer) with a local OpenCode
LLM running on your own GPU (as the coder), connecting the two inside a normal
Claude Code session.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
the repo's own description plus the CATALOG "Overlaps with" cell. That is
sufficient to place the lead against its closest catalog peers, not to support any
verdict, and none is offered here.

## Triage note

Newly catalogued from today's discovery pass. No structural signal (STACK
overlap, archived status, disqualifying license) bands this lead for a mechanical
disposition — its closest catalog peers (`orca`, `cedr`) are broader
orchestration/routing tools, while this is specifically a Claude-plans /
local-model-codes pairing. Left at `discovery-log` for a first-time hands-on eval.

_Triaged 2026-11-20 by the daily discovery-and-triage routine (bulk,
eliminate-only). Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claudes-workbench](https://github.com/a-schaefers/claudes-workbench) | plugin | Claude Code plugin (MIT) pairing Claude as planner/reviewer with a local OpenCode LLM on your GPU as the coder | Running a capable cloud model for planning and a free local model for coding means switching tools by hand; want them paired inside one Claude Code session | orca, cedr, claude-antigravity |
