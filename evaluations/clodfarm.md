# Evaluation: clodfarm

**Repo:** [matank001/clodfarm](https://github.com/matank001/clodfarm)
**Stars:** 62 | **Last updated:** 2026-09-28 (pushed) | **License:** MIT
**Last verified:** 2026-09-28
**Last triaged:** 2026-09-28  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A farm of Claude Code sub-agents: plant a mission and it splits the work into sub-agents, opens the work, and paces each account's dispatch against its real 5-hour and weekly Claude usage limits. Steerable from the Claude mobile app.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a bulk-triage disposition, not for an ADOPT/KEEP call — this eval offers none.

## Triage note

Cites claude-squad (STACK ADOPT) in Overlaps with, which bands this P2 challenger. Not SKIPped as redundant: claude-squad is a parallel-session TUI for multiple agent CLIs, while clodfarm's stated differentiator is usage-limit-aware pacing of Claude Code sub-agents specifically (real 5-hour/weekly quota) plus mobile-app steering — neither of which claude-squad's own eval claims. Newly catalogued (added 2026-09-28) with only 62 stars against 42 forks, an unusual ratio worth a second look before a deeper eval. Left at discovery-log rather than SKIPped.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [clodfarm](https://github.com/matank001/clodfarm) | tool | Farm of Claude Code sub-agents (MIT) pacing themselves against each account's real 5-hour/weekly usage limits | Fanning a mission across sub-agents risks blowing through Claude usage limits with nothing pacing against the real quota | claude-squad, agent-of-empires, buildd |
