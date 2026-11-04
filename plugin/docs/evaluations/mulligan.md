# Evaluation: mulligan

**Repo:** [stanczykwyatt/mulligan](https://github.com/stanczykwyatt/mulligan)
**Stars:** 1 | **Last updated:** 2026-11-03 (pushed) | **License:** MIT
**Last verified:** 2026-11-04
**Last triaged:** 2026-11-04  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

An undo CLI that snapshots a project at every prompt and tool call (shell commands
included), so a coding-agent session can be listed, diffed, and undone to any earlier
point. Works across Codex, Claude Code, Gemini CLI, OpenCode, and Aider; never touches
the git repo and makes no network calls.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner and repo metadata. Snapshot overhead/storage cost on a large repo
across a long session is untested here.

## Triage note

Left at `discovery-log` (P3 backlog) — newly catalogued today. Cites no STACK pick in
`Overlaps with` (filesnap, oops, opendot are catalogued leads, not STACK picks). Not
examined further in this pass.

_Triaged 2026-11-04 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [mulligan](https://github.com/stanczykwyatt/mulligan) | tool | Undo CLI (MIT) that snapshots a project at every prompt and tool call — list, diff, and undo to any point, across several agent harnesses, without touching git | Rolling an agent session back to an arbitrary earlier point means digging through git history or losing the checkpoint entirely | filesnap, oops, opendot |
