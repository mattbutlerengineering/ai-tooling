# Evaluation: supabase

**Repo:** [supabase/mcp](https://github.com/supabase/mcp)
**Stars:** 2,796 | **Last updated:** 2026-07-09 (pushed) | **License:** Apache-2.0
**Dev loop stage:** MCP Servers (database)
**Layer:** Tooling
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

Official MCP server for Supabase — database and auth operations against your projects from an agent
session.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04) plus
the CATALOG one-liner and "Overlaps with" cell (`prisma`). Enough to place it in the DB cluster; not
enough for a positive verdict, and none is offered.

## Triage note

Left at `discovery-log`. First-party, Apache-2.0, pushed this week — a vendor integration of the
standard shape: worth a lot to teams on Supabase, worth nothing to everyone else, which is neither
ADOPT-everywhere nor SKIP.

The DB cluster was examined as a whole in this pass and left intact, because the four rows do genuinely
different things. `supabase` and `prisma` are the light per-stack options; `mcp-toolbox` (Google) covers
the broadest set of database types and doubles as a framework for building safe agent-facing DB tools;
`pg-aiguide` touches no database at all and improves the SQL the agent *writes*. The `mcp-toolbox` eval
explicitly recommends the lighter servers for a single local Postgres in development, which is a point
in this row's favour rather than against it.

The standing caveat for every member of the cluster applies here too and is the thing a promotion must
address: an agent with write access to a development database is a Safety surface, and least-privilege
scoping is the difference between a useful integration and a bad afternoon.

No eval file existed before this pass; this stub is the placeholder, not an evaluation.
_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [supabase](https://github.com/supabase/mcp) | MCP server | Supabase database and auth operations | Agent needs to interact with Supabase projects during development | prisma |
