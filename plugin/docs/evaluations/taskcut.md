# Evaluation: taskcut

**Repo:** [wasd96040501/taskcut](https://github.com/wasd96040501/taskcut)
**Stars:** 6 | **Last updated:** 2026-09-24 (pushed) | **License:** MIT
**Last verified:** 2026-09-24
**Last triaged:** 2026-09-24  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A Claude Code plugin that compacts the conversation at sub-task boundaries — as a task tree finishes
a branch — instead of waiting for the context window to hit its limit.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus
the CATALOG "Overlaps with" cell (compact-adviser, headroom). That is sufficient to place the lead
against its incumbents, not to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped as redundant with `headroom` (the STACK incumbent triage.py
matched on). headroom compresses verbose tool output/logs before they reach the model; taskcut
instead decides *when* to trigger a `/compact`, using sub-task completion as the trigger — the same
job `compact-adviser` already does with a Jev-judged "work appears completed" signal. taskcut's own
closest peer is compact-adviser (a non-STACK lead, so it never tripped the P2 flag), not headroom —
compression amount and compaction timing are complementary mechanisms, not competing ones. At 6
stars and 2 days old there is no measured comparison against either peer yet.

_Triaged 2026-09-24 by the daily discovery routine (today's new lead)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [taskcut](https://github.com/wasd96040501/taskcut) | plugin | Claude Code plugin (MIT) compacting the conversation at sub-task boundaries instead of waiting for the context limit | Context only compacts once the limit is hit, losing the sub-task boundary as a natural point to summarize and reset | compact-adviser, headroom |
