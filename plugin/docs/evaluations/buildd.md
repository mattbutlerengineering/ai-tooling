# Evaluation: buildd

**Repo:** [buildd-ai/buildd](https://github.com/buildd-ai/buildd)
**Stars:** 1 | **Last updated:** recent (exact push date not captured from the repo page; checked 2026-09-04) | **License:** Apache-2.0
**Last verified:** 2026-09-04
**Last triaged:** 2026-09-04  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Task coordination platform for AI coding agents. Tasks are created via dashboard, CLI, or API; agents claim them, branch, write code, and open PRs. Adds "missions" (goal-based task grouping), agent "roles" (personas), scheduled automation, and shared memory across agent runs. MCP-native.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the repo's own README description fetched via the GitHub repo page. That is enough to place it in the catalog and check it against the P2 challenger band's flagged incumbent (`claude-squad`); it is not enough for a positive verdict, and none is offered.

## Triage note

Left at `discovery-log`. `triage.py` bands this as P2 (challenges `claude-squad`, pressure 1), but the two tools solve different problems: claude-squad manages parallel *terminal sessions* for agents a human is actively steering, while buildd is a *task-queue* model — tasks are created (dashboard/CLI/API) and agents pick them up asynchronously, closer to an issue-tracker-for-agents than a terminal multiplexer. Not clearly redundant enough for a mechanical SKIP; leaving it for a real hands-on eval to judge whether the task-queue model earns its own slot.

_Triaged 2026-09-04 by the P2 challenger band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [buildd](https://github.com/buildd-ai/buildd) | tool | Task coordination platform (Apache-2.0) — create/schedule tasks via dashboard, CLI, or API; agents claim them, branch, code, and open PRs, with missions, roles, and shared memory across runs | Coordinating which agent works on what, and tracking a task's lifecycle through to a PR, is ad hoc across tools | gastown, stargate, claude-squad |
