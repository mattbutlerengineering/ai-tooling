# Evaluation: durable-harness

**Repo:** [vercel-labs/durable-harness](https://github.com/vercel-labs/durable-harness)
**Stars:** 180 | **Last updated:** 2026-10-19 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-10-22
**Last triaged:** 2026-10-22  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling (harness)

---

## What it does

Durable, crash-resumable coding-agent harness runners (Claude Code, Codex, OpenCode,
Pi, fx) built on Vercel's Workflow SDK, so a long-running agent run survives a crash
or restart instead of losing its place.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead
against its closest catalog peers, not to support any verdict, and none is offered here.

## Triage note

Brand new (created 2026-10-16, Vercel Labs). Its differentiator over `ralph`/`eca` is
the durability layer itself — a Workflow-SDK-backed resumable execution model across
several harnesses, rather than a single harness's own loop. No archived flag, no
disqualifying license, no `Ships inside` container, and zero overlap pressure (no STACK
pick names it back). Left at `discovery-log` for a real hands-on eval rather than SKIPped
as redundant — durable/resumable execution across providers is a distinct mechanism from
either peer.

_Triaged 2026-10-22 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [durable-harness](https://github.com/vercel-labs/durable-harness) | tool | Durable, crash-resumable coding-agent harness runners (Apache-2.0) for Claude Code, Codex, OpenCode, Pi, and fx on Vercel's Workflow SDK | A harness run that crashes or restarts mid-task loses its place with no durable, resumable execution across providers | ralph, ralph-claude-code, eca |
