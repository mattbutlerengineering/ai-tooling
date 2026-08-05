# Evaluation: gospect-mcp

**Repo:** [backendArchitect/gospect-mcp](https://github.com/backendArchitect/gospect-mcp)
**Stars:** 2 | **License:** MIT
**Last verified:** 2026-08-05
**Last triaged:** 2026-08-05  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Infrastructure (MCP server)

---

## What it does

A Go-only, report-first code scanner exposed as an MCP server — indexes a module, runs
deterministic analyzers, and reports genuine bugs, dead code, stale docs, and outdated APIs
without editing code until asked.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell (skylos, openrewrite, cc-skills-golang). That
is sufficient to place the lead, not to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: skylos is multi-language and CLI-first, not MCP-native; openrewrite
does deterministic *refactoring* recipes, not read-only reporting; cc-skills-golang is a
skill collection, not a scanner. A Go-specific, MCP-native, read-only report generator is a
narrow gap worth a hands-on look rather than a redundancy SKIP. Very early (2 stars).

_Triaged 2026-08-05 by the daily discovery routine (today's new lead)._
