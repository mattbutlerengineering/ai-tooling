# Evaluation: groundcrew

**Repo:** [ClipboardHealth/groundcrew](https://github.com/ClipboardHealth/groundcrew)
**Stars:** 66 | **Last updated:** not independently verified (GitHub API unavailable for this repo in this session) | **License:** MIT
**Last verified:** 2026-10-02
**Last triaged:** 2026-10-02  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Dispatches a task backlog (Linear, Jira, or local files) to local, interactive AI coding agents.
Creates one sandboxed git worktree per task and launches the agent CLI (`claude`, `codex`,
`cursor-agent`, or `pi`) in its own terminal pane, leaving each task's work on a PR-ready branch.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This session's GitHub API access is scoped to the
`ai-tooling` repo only, so repo facts came from the public repo page rather than `gh api`. This
is source-grounded only: the repo's own README description plus the CATALOG "Overlaps with" cell.
Sufficient to place the lead, not to support any verdict, and none is offered.

## Triage note

Left at `discovery-log`. Cites `claude-squad` (STACK) in "Overlaps with", which bands this P2, but
the job is different: `claude-squad` is a lean multi-session TUI manager you drive by hand, while
groundcrew's differentiator is automatic backlog-to-agent dispatch from Linear/Jira — a ticket
walks in, a worktree and an agent walk out. That is a different workflow, not a redundant
implementation of the same one, so it deserves a real hands-on look rather than a mechanical SKIP.

_Triaged 2026-10-02 by the P2 challenger band (daily discovery pass)._
