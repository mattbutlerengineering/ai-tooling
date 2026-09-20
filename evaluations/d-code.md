# Evaluation: d-code

**Repo:** [HutsuliakDmytro/d-code](https://github.com/HutsuliakDmytro/d-code)
**Stars:** 7 | **Last updated:** 2026-09-06 (pushed) | **License:** MIT
**Last verified:** 2026-09-07
**Last triaged:** 2026-09-07  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

An unofficial Electron desktop client for the Claude Code CLI, wrapping session history, live chat, an LSP/debugger-equipped editor, git, and plan-limit tracking into one IDE-like shell.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual behavior —
it would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`. Very early (7★, created this week) but a broader surface than the session-replay/observability tools it overlaps with (claude-devtools, roundtable read logs after the fact; this wraps live interaction too). Too new and too small to call redundant with any one incumbent yet.

_Triaged 2026-09-07 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [d-code](https://github.com/HutsuliakDmytro/d-code) | tool | Unofficial desktop client (MIT) for the Claude Code CLI — session history, live chat, an LSP/debugger editor, git, and plan-limit tracking | Claude Code is terminal-only; want a full IDE-like desktop shell around sessions, editing, and usage limits | claude-devtools, roundtable, Continuous-Claude-v3 |
