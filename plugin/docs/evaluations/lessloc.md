# Evaluation: lessloc

**Repo:** [rextail-ai/lessloc](https://github.com/rextail-ai/lessloc)
**Stars:** 101 | **Last updated:** 2026-10-23 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-10-23
**Last triaged:** 2026-10-23  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

An agent-hook gate (JavaScript) that keeps Claude Code, Codex, GitHub Copilot, Gemini CLI,
Cline, and Cursor to the least code that does the job and still works, flagging dead and
duplicate code as it's written.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead
against its closest catalog peers, not to support any verdict, and none is offered here.

## Triage note

Brand new (created 2026-10-19), pressure 0 — nothing in the catalog cites it yet. Its
"Overlaps with" cell names `skylos`, `ratchet`, and `cyclomatic-complexity-skill`, none of
which is a STACK pick, so this does not band as a P2 challenger. No archived flag, no
disqualifying license (Apache-2.0 is permissive and this is a `tool`, not a vendored
skill/plugin anyway), no `Ships inside` container. Differentiator over the existing
dead-code/complexity peers is that it runs as a live agent hook across six named
harnesses rather than a one-shot CLI scan. Left at `discovery-log`.

_Triaged 2026-10-23 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [lessloc](https://github.com/rextail-ai/lessloc) | tool | Agent-hook gate (Apache-2.0) keeping Claude Code, Codex, Copilot, Gemini CLI, and Cursor to the least code that does the job — flags dead and duplicate code as it's written | Coding agents accrete more code than a task needs, leaving dead/duplicate code behind with nothing gating it at write time | skylos, ratchet, cyclomatic-complexity-skill |
