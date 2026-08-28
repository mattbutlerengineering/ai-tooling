# Evaluation: CoordClaw

**Repo:** [CoordClaw/CoordClaw](https://github.com/CoordClaw/CoordClaw)
**Stars:** 61 | **Last updated:** 2026-08-01 (pushed) | **License:** MIT
**Last verified:** 2026-08-28
**Last triaged:** 2026-08-28  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A multi-agent system that runs AI like a one-person company — natural-language-defined teams, message-loop collaboration instead of hard-coded DAGs, and auditable work logs with human oversight.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for the disposition below, which turns on *redundancy with a catalogued incumbent*, not on the tool's behaviour. It would not support an ADOPT, and this eval offers none.

## Triage note

Cites `claude-squad` (a STACK pick) in its "Overlaps with" cell, putting this lead in the P2 challenger band. Left at `discovery-log` rather than SKIPped: claude-squad is a tmux/git-worktree session manager for running parallel agent instances, while CoordClaw is an org-theory-driven multi-agent coordination framework (natural-language team definitions, message-loop collaboration, audit logs) — a different mechanism and scope, not a clear substitute. Not confidently redundant enough for a mechanical SKIP.

_Triaged 2026-08-28 by the P2 challenger band._
