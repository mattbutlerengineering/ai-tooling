# Evaluation: claude-code-agent-monitor

**Repo:** [hoangsonww/claude-code-agent-monitor](https://github.com/hoangsonww/claude-code-agent-monitor)
**Stars:** 781 | **Last updated:** 2026-07-10 (pushed) | **License:** MIT
**Last verified:** 2026-08-02
**Last triaged:** 2026-08-02  <!-- triaged: bulk -->
**Dev loop stage:** Observability
**Layer:** Tooling

---

## What it does

A real-time dashboard for Claude Code (Node/React/WebSockets) that tracks sessions, agent/tool activity, and subagent orchestration, with live analytics and a Kanban status board.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: CATALOG.md's existing one-liner plus `repo-metadata.json` (781 stars, MIT, pushed 2026-07-10).

## Triage note

Left at `discovery-log` rather than SKIPped: it overlaps `claude-code-hooks-multi-agent-observability` (higher-profile, ★1.5K, also unvalidated discovery-log) on the core "live dashboard of Claude Code session/tool/agent activity" job, and the Kanban status board is a real but narrow differentiator. Neither tool is a validated STACK incumbent, so calling this one "redundant" would be overreaching without a side-by-side hands-on comparison — left for a real eval to decide which (if either) is worth adopting.

_Triaged 2026-08-02 by the daily discovery routine (backlog band: P2 challenger)._
