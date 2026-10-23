# Evaluation: KLIDE

**Repo:** [pierreprudh/KLIDE](https://github.com/pierreprudh/KLIDE)
**Stars:** 6 | **Last updated:** 2026-10-23 (pushed) | **License:** MIT
**Last verified:** 2026-10-23
**Last triaged:** 2026-10-23  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A local-first agent IDE (TypeScript/Rust, Tauri) steering Codex, Claude Code, OpenCode,
and local models (Ollama) from one desktop app, with a Monaco-based diff/review surface
and git-worktree-backed sessions.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide the P2
disposition below, not to support any adoption verdict, and none is offered here.

## Triage note

Bands as **P2 challenger**: its "Overlaps with" cell names `claude-squad`, which is a
STACK pick (ADOPT, RUN, "TUI for managing parallel agent sessions"). Both tools let you
steer multiple coding-agent sessions from one place, but KLIDE's own description adds a
"visible review" surface (a Monaco-based diff view) that claude-squad's TUI does not
claim, and KLIDE is a desktop GUI app rather than a terminal TUI — a different interaction
model, not merely a reskin. That differentiation is enough to avoid a mechanical
"redundant with claude-squad" SKIP; whether the review surface is actually worth a second
tool for this job is a call for a real hands-on eval, not this bulk pass. Left at
`discovery-log`, not SKIPped. (Very low signal so far — ★6 — so this is not an urgent
P0 candidate either.)

_Triaged 2026-10-23 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [KLIDE](https://github.com/pierreprudh/KLIDE) | tool | Local-first agent IDE (MIT) steering Codex, Claude Code, OpenCode, and local models with visible review | Directing multiple coding-agent CLIs from one place means separate terminals with no shared review surface | claude-squad, orchestra, orca |
