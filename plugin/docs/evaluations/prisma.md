# Evaluation: prisma

**Repo:** [prisma/prisma](https://github.com/prisma/prisma)
**Stars:** 46,900 | **Last updated:** 2026-09-04 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-09-05
**Last triaged:** 2026-09-05  <!-- triaged: bulk -->
**Dev loop stage:** MCP Servers
**Layer:** Infrastructure

---

## What it does

`prisma mcp` — a subcommand of the Prisma ORM CLI exposing database migrations, Prisma Studio,
and status operations to an agent, so it can operate on a project's database during development.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Ships inside" cell. That is sufficient to place the lead, not to judge the
MCP subcommand's behaviour hands-on.

## Triage note

Left at `discovery-log`. This row's `Ships inside` cell names `prisma/prisma` as its container,
which bands it P5 — but that container is not itself a candidate for this catalog: the ★46.9K
measures the Prisma **ORM**, an application-development dependency, not an AI-tooling artifact,
and it has no business getting its own catalog row here (CLAUDE.md's own note on this exact
case). So "settle the container" is not an available move — there is no container row to add,
and none should be added. The only two honest options are leaving this row at `discovery-log`
(what an agent using Prisma actually gets by installing the ORM) or a human deciding the row
itself is out of place. Neither is a bulk-lane call: settling *whether the row should exist* is
a judgement about scope, not a mechanical disposition eliminate-only triage may make.

_Triaged 2026-09-05 by the P5 ships-inside band._
