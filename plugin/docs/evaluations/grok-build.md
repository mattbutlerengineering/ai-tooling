# Evaluation: Grok Build

**Repo:** [xai-org/grok-build](https://github.com/xai-org/grok-build)
**Stars:** 26.6K | **Last updated:** 2026-09-09 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-09-10
**Last triaged:** 2026-09-10  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

xAI's own open-sourced terminal coding agent (Rust) — a full-screen, mouse-interactive
TUI that reads/edits a repo and runs commands, with a plan mode that presents diffs for
approval, parallel subagents, a headless mode for CI, and editor embedding via the Agent
Client Protocol. Source (agent loop, tool layer, TUI, extension system) was opened up in
mid-2026; the CLI itself is free, model access is billed through an xAI account.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual behavior —
it would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped. `grok-cli` (superagent-ai) is already catalogued as
the unofficial community CLI wired to xAI's Grok API; grok-build is the different thing —
xAI's own first-party harness, source and all, on par with how deepseek-harness and codex
sit beside their respective community wrappers. Cites no STACK incumbent in its own
"Overlaps with" cell (P3, no overlap pressure), so nothing here to call redundant. Large,
first-party, actively developed (★26.6K, commits the day this was triaged) — worth a real
look once there's reason to add a third vendor-native harness to the rotation.

_Triaged 2026-09-10 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [grok-build](https://github.com/xai-org/grok-build) | harness | xAI's first-party open-source terminal coding agent (Apache-2.0, Rust, ★26.6K) — full-screen mouse-interactive TUI, plan mode with diff approval, parallel subagents, headless CI mode, and editor embedding via the Agent Client Protocol | Want xAI's own terminal coding-agent harness on par with Claude Code/Codex/deepseek-harness, not the unofficial community grok-cli wrapper | grok-cli, deepseek-harness, codex, opencode |
