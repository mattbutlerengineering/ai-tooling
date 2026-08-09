# Evaluation: llm-safe-sql

**Repo:** [hyuga611/llm-safe-sql](https://github.com/hyuga611/llm-safe-sql)
**Stars:** 0 | **Last updated:** 2026-08-09 (pushed) | **License:** MIT
**Last verified:** 2026-08-09
**Last triaged:** 2026-08-09  <!-- triaged: bulk -->
**Dev loop stage:** Implement (safe database mutations)
**Layer:** Infrastructure

---

## What it does

Lets an LLM propose an UPDATE/DELETE, runs it for real inside a database transaction, measures the actual before/after diff, and always rolls back — so a human approves a measured fact instead of the model's claim about what the mutation would do. MySQL + PostgreSQL, MCP server, no runtime dependencies.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell.

## Verdict

**discovery-log — tentative read** — No STACK-pick overlap (prisma/agentlint/numbat are cited but none is an incumbent this challenges directly); left at discovery-log per the P3 default. The measured-diff-then-rollback approach to agent DB-mutation approval is a real, differentiated pattern worth a closer look.

_Triaged 2026-08-09 by the P3 backlog band._
