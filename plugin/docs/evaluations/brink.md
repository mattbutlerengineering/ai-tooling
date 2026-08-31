# Evaluation: brink

**Repo:** [semihtalii/brink](https://github.com/semihtalii/brink)
**Stars:** 50 | **Last updated:** 2026-08-30 (pushed) | **License:** MIT
**Last verified:** 2026-08-31
**Last triaged:** 2026-08-31  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop (Observability)
**Layer:** Tooling

---

## What it does

A native menu-bar (macOS) / taskbar (Windows) widget showing how close Claude Code, Codex, and Cursor sessions are to their usage limits, at a glance without opening a terminal.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a leave decision that turns on differentiation from existing observability entries, not on the tool's behaviour — a question the overlap answers directly. It would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped. The Observability category already carries several usage/cost-tracking tools that cite `ccusage` in their own "Overlaps with" cell (`claude-monitor`, `claude-statusline-burnrate`, `tokentab`, `peek`, `opencode-cache-stats`) without any of them being mechanically SKIPped as redundant — none has been, because each occupies a different form factor (CLI report, statusline, TUI, menu-bar) rather than competing for the same slot. brink's ambient system-tray widget is a form factor none of those cover, and multi-CLI scope (Claude Code + Codex + Cursor, not just one) is a differentiator worth a real look rather than a mechanical dismissal.

_Triaged 2026-08-31 by the P2 challenger band._
