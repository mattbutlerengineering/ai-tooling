# Evaluation: pop-agent

**Repo:** [duzhenxun/pop-agent](https://github.com/duzhenxun/pop-agent)
**Stars:** 149 | **Last updated:** 2026-11-27 (pushed) | **License:** MIT
**Last verified:** 2026-11-27
**Last triaged:** 2026-11-27  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

A local web UI for watching a coding agent's reasoning stream live and cutting in
with a correction mid-turn, across pi, Codex, Claude Code, OpenCode, and DSH.
Sessions stay the engine's own files — no database, no account.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
the CATALOG one-liner plus repo metadata from GitHub's search API (this session's
GitHub access is scoped to this repo only, so a direct per-repo metadata fetch was
not available; stars/license/pushed-date come from the search endpoint instead).

## Triage note

Left at `discovery-log` — cites no STACK pick in its "Overlaps with" cell (`togo`,
`claude-super-sidebar`, `airoom` are catalogued peers but none is installed in STACK
today), so no mechanical P2 redundancy SKIP applies. Differentiated from those peers
by being cross-harness (pi/Codex/Claude Code/OpenCode/DSH, not just Claude Code/Codex)
and by supporting a live mid-turn correction rather than read-only status. Worth a
real hands-on eval rather than a mechanical disposition.

_Triaged 2026-11-27 by the daily discovery routine (new lead, same-day triage)._
