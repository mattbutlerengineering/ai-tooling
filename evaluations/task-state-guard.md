# Evaluation: task-state-guard

**Repo:** [MaxHu-xuan/task-state-guard](https://github.com/MaxHu-xuan/task-state-guard)
**Stars:** 73 | **Last updated:** 2026-08-25 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-08-29
**Last triaged:** 2026-08-29  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

A SQLite-backed reconciler for AI-agent task delivery state left stuck after a restart or timeout. It previews the changes it would make before closing a stale delivery state, rather than guessing at success and moving on.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell (`hermes-conductor`, `cee`, `agent-of-empires`). It would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log` — a first-time lead with no overlap pressure yet (added today, so no other catalog row cites it), landing it in P3 backlog rather than a structural band. Not SKIPped: the "reconcile stuck delivery state after a crash" problem is a real, narrow gap next to the existing Agent Orchestration entries, which mostly cover *running* agents in parallel (worktree lanes, kanban dispatch) rather than *recovering* their state afterward. Worth a real look rather than a mechanical dismissal.

_Triaged 2026-08-29 by the P3 backlog band ([#565](https://github.com/mattbutlerengineering/ai-tooling/issues/565))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [task-state-guard](https://github.com/MaxHu-xuan/task-state-guard) | tool | SQLite delivery-state reconciler (Apache-2.0) for AI-agent tasks stuck after restarts and timeouts, previewing every change before it closes a stale state | Agent orchestrators crash or time out mid-task, leaving delivery state stuck with no safe way to reconcile it without guessing | hermes-conductor, cee, agent-of-empires |
