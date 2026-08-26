# Evaluation: AgentSeed

**Repo:** [Morningstar202604/AgentSeed](https://github.com/Morningstar202604/AgentSeed)
**Stars:** 11 | **Last updated:** 2026-08-25 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-08-26
**Last triaged:** 2026-08-26  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

Anti-hallucination guardrails for AI coding agents — a hybrid Skill + MCP server
(6 tools) that verifies code before it is marked done. Works with Claude Code,
Cursor, VS Code, and Copilot.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell.

## Triage note

Very new (created 2026-08-25, one day old) and very low stars (11) — too early to
judge against the established evidence-before-done cluster (`vet`, `tdd-guard`,
`godkiller-mcp`, `prove-it`). Not SKIPped as redundant because a same-job tool this
young hasn't earned a redundancy verdict yet; left at `discovery-log` to re-surface
once it has more signal (adoption, a real README beyond the pitch) to evaluate against.
