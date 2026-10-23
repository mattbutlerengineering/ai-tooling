# Evaluation: oops

**Repo:** [lintsinghua/oops](https://github.com/lintsinghua/oops)
**Stars:** 14 | **Last updated:** 2026-10-14 (pushed) | **License:** MIT
**Last verified:** 2026-10-23
**Last triaged:** 2026-10-23  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A CLI (Go) giving Claude Code, Codex, Gemini CLI, and Cursor CLI a one-step precise
undo/redo via snapshots — a Ctrl+Z for agent file/shell actions.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead
against its closest catalog peers, not to support any verdict, and none is offered here.

## Triage note

Pressure 0 — nothing in the catalog cites it yet. Its "Overlaps with" cell names
`filesnap`, `opendot`, and `Jixu`, none of which is a STACK pick, so this does not band
as a P2 challenger. No archived flag, no disqualifying license (MIT), no `Ships inside`
container. Differentiator over `filesnap` (git-free snapshot/rewind CLI) is the explicit
undo/*redo* pairing and multi-harness framing (four CLIs named); differentiator over
`opendot`/`Jixu` is that it's a standalone add-on rather than a full harness. Left at
`discovery-log`.

_Triaged 2026-10-23 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [oops](https://github.com/lintsinghua/oops) | tool | CLI (MIT, Go) giving Claude Code, Codex, Gemini CLI, and Cursor CLI a one-step precise undo/redo via snapshots | Agent file/shell actions are hard to cleanly roll back; want a Ctrl+Z that works across harnesses without a full git repo | filesnap, opendot, Jixu |
