# Evaluation: ai-terminal-manager

**Repo:** [lyfuci/ai-terminal-manager](https://github.com/lyfuci/ai-terminal-manager)
**Stars:** 20 | **Last updated:** 2026-09-08 (pushed) | **License:** MIT
**Last verified:** 2026-09-08
**Last triaged:** 2026-09-08  <!-- triaged: bulk -->
**Dev loop stage:** Implement (cross-tool session management)
**Layer:** Tooling

---

## What it does

A tmux-based session manager ("atm") for AI coding CLIs — merges session history from Claude Code, Codex, Pi, Gemini CLI, and opencode into one searchable list, shows currently running panes in a persistent tmux sidebar, and integrates tmux-resurrect/continuum so sessions survive a reboot. It reads the session files these tools already write to disk rather than controlling them directly.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual behavior —
it would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`. None of its overlap citations (cli-continues, re_gent, claude-code-router) are STACK picks. It's also a different job from all three: cli-continues hands off conversation state *between* agents, re_gent tracks prompt-level provenance of edits, and claude-code-router customizes request routing — none of them is a tmux session/pane manager unifying history across five different CLIs. Worth a real look, not a mechanical SKIP.

_Triaged 2026-09-08 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ai-terminal-manager](https://github.com/lyfuci/ai-terminal-manager) | tool | tmux-based session manager (MIT) unifying session history across Claude Code, Codex, Gemini CLI, opencode, and Pi behind a persistent sidebar | Managing multiple AI coding CLIs over SSH/tmux means switching tools with no unified session view, search, or restore-after-reboot | cli-continues, re_gent, claude-code-router |
