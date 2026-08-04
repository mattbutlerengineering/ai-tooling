# Evaluation: mcp-migrate

**Repo:** [dheerajjha/mcp-migrate](https://github.com/dheerajjha/mcp-migrate)
**Stars:** 4 | **License:** Apache-2.0
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** MCP Servers
**Layer:** Tooling (CLI linter/codemod)

---

## What it does

Finds and fixes what the MCP 2026-07-28 spec revision breaks in an MCP server: 21 rules,
5 autofixers, and a readiness board.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell (skylos, typescript-mcp-server-generator,
openrewrite). That is sufficient to place the lead, not to support an ADOPT — this eval
offers none.

## Triage note

Left at `discovery-log`: none of skylos, typescript-mcp-server-generator, or openrewrite
targets MCP spec-revision compliance specifically — this is a narrow, novel niche (a linter +
autofixer for one protocol's breaking changes) with no catalogued incumbent. Low star count
(4) and 55 open issues suggest early-stage; worth a lightweight hands-on look before any
stronger call.

_Triaged 2026-08-04 by the daily discovery routine (today's new lead)._
