# Evaluation: agent-flow

**Repo:** [Drix10/agent-flow](https://github.com/Drix10/agent-flow)
**Stars:** 10 | **Last updated:** 2026-09-26 (pushed) | **License:** MIT
**Last verified:** 2026-09-30
**Last triaged:** 2026-09-30  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Process

---

## What it does

A self-bootstrapping, self-healing agent-engineering skill enforcing an Implement → Review → QA
pipeline for AI coding agents (Claude Code, Codex, Gemini CLI), with context-drift detection and
guardrails.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP that turns on redundancy with
a catalogued incumbent, not on the tool's behavior — a question the overlap answers directly. It
would not support an ADOPT, and this eval offers none.

## Verdict

**SKIP** — redundant with `GSD` (STACK, MEASURED, `open-gsd/gsd-core`). GSD already covers a
context-engineering Discuss→Plan→Execute→Verify→Ship loop with restricted-tool subagents and
durable state, at measured adoption; agent-flow's Implement→Review→QA pipeline with context-drift
guardrails is the same job (workflow-discipline scaffolding for a coding agent) at 10 stars and
four days old, with no adoption or measurement signal distinguishing it. A second tool for this job
earns nothing until it demonstrates something GSD doesn't.

_Triaged 2026-09-30 by the P2 challenger band._
