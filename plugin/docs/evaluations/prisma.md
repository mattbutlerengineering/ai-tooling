# Evaluation: prisma

**Repo:** [prisma/prisma](https://github.com/prisma/prisma)
**Stars:** 46,945 | **Last updated:** 2026-07-09 (pushed) | **License:** Apache-2.0
**Dev loop stage:** MCP Servers (database)
**Layer:** Tooling
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

Database operations through the Prisma ORM — migrations, Studio, status — exposed to an agent over
MCP.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04) plus
the CATALOG one-liner and "Overlaps with" cell (`supabase`, `mcp-toolbox`). Enough to place it; not
enough for a positive verdict, and none is offered.

## Triage note

Left at `discovery-log`, with one row-shape observation worth recording.

The CATALOG entry links to `prisma/prisma` — the whole ORM, ★46.9K — while the catalogued artifact is
the **MCP server that ships inside it**. The star count therefore measures the ORM's adoption, not the
MCP server's, and reading it as evidence about this integration would be a mistake. It is a milder
instance of the pattern this triage lane keeps finding (`diagnosing-bugs` and `implement` inside
`mattpocock/skills`; `confluence` and `jira` inside `mcp-atlassian`): a facet of a larger artifact
entered as an independent lead.

That is not a reason to SKIP it. If you already use Prisma, the MCP server comes with the tooling you
have, which makes it the lowest-friction option in the DB cluster — and the `mcp-toolbox` eval says as
much, naming prisma and supabase as the smaller lift for a single local database.

Left because the promotion question ("does agent-driven migration actually help, and how badly can it
go wrong") needs a hands-on run against a real schema, and because whether the row should point at the
ORM or a narrower MCP path is a catalog-shape decision rather than a verdict.

No eval file existed before this pass; this stub is the placeholder, not an evaluation.
_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [prisma](https://github.com/prisma/prisma) | MCP server | Database operations via Prisma ORM (migrations, studio, status) | Agent needs to interact with databases during development | supabase, mcp-toolbox |
