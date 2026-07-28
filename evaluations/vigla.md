# Evaluation: Vigla

**Repo:** [Kilbex/Vigla](https://github.com/Kilbex/Vigla)
**Stars:** 29 | **Last updated:** 2026-07-27 | **License:** Apache-2.0
**Last verified:** 2026-07-28
**Last triaged:** 2026-07-28  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

An open-source Rust/Tauri "mission control" desktop app for coding agents — runs cross-vendor workers (Claude Code, Codex, Antigravity, etc.) in isolated git worktrees, audits every submission, and can revert an entire mission in one step.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata (GitHub API: 29 stars, Apache-2.0, pushed 2026-07-27) plus the CATALOG "Overlaps with" cell against claude-squad/orca/dmux/agent-of-empires. Sufficient to catalog and note the gap (whole-mission audit + one-step revert), not to judge the revert mechanism's safety hands-on.

## Triage note

The "audit every submission, revert an entire mission" framing is a genuine differentiator versus dmux/claude-squad (which isolate and merge per-task, not per-mission), and none of its catalog overlaps is a STACK pick — no incumbent to SKIP against. Left at discovery-log for a future hands-on eval.
