# Evaluation: offload-mcp-server

**Repo:** [tailucanh/offload-mcp-server](https://github.com/tailucanh/offload-mcp-server)
**Stars:** 8 | **Last updated:** 2026-11-08 (pushed) | **License:** MIT
**Last verified:** 2026-11-08
**Last triaged:** 2026-11-08  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

An MCP server that lets a main coding agent delegate heavy reading to a second agent and read
back only the extracted answer, so the primary agent's context budget is not spent on the raw
material.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the CATALOG
one-liner and its "Overlaps with" cell (`pitroom`, `foreman (ilkemerol)`, `opus-manager`). That is
sufficient to check for a named STACK redundancy; it is not sufficient to support an ADOPT, and
this eval offers none.

## Verdict

**discovery-log — tentative read** — a very small (8-star), brand-new MCP server. None of its
cited peers is a STACK pick, so there is no named incumbent to call this redundant with. The
context-offload pattern it implements is a real, recurring need (see `pitroom`, `foreman
(ilkemerol)`), but at this size it deserves a real hands-on eval rather than a mechanical SKIP.

## Triage note

Left at `discovery-log` for the P0/eval-runner lane.

_Triaged 2026-11-08 by the daily discovery-and-triage routine._
