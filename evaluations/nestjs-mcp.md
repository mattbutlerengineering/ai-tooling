# Evaluation: nestjs/mcp

**Repo:** [nestjs/mcp](https://github.com/nestjs/mcp)
**Stars:** 14 | **Last updated:** 2026-11-09 (pushed) | **License:** MIT
**Last verified:** 2026-11-09
**Last triaged:** 2026-11-09  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

An official NestJS module for building MCP servers and clients inside a Nest application,
with minimal boilerplate — the NestJS-idiomatic equivalent of `fastmcp` (Python) for
Node/TypeScript shops already using Nest's module/DI system.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
repo's own description and the CATALOG "Overlaps with" cell (`fastmcp`, `mcp-use`,
`typescript-mcp-server-generator`). That is sufficient to check for a named STACK
redundancy; it is not sufficient to support an ADOPT, and this eval offers none.

## Verdict

**discovery-log — tentative read** — small (14 stars) but from the official `nestjs` org,
which carries real maintenance weight for Nest shops. None of its cited peers is a STACK
pick (`fastmcp`/`mcp-use`/`typescript-mcp-server-generator` are all `discovery-log`
themselves), so no mechanical SKIP applies. Worth a first look for teams already standing
up MCP servers in NestJS rather than a generic Node framework.

## Triage note

Left at `discovery-log` for the P0/eval-runner lane.

_Triaged 2026-11-09 by the daily discovery-and-triage routine._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [nestjs/mcp](https://github.com/nestjs/mcp) | framework | NestJS module (MIT) for building MCP servers and clients inside a Nest app with minimal boilerplate | Building an MCP server in a NestJS app means bolting on a separate library with no idiomatic Nest module/DI integration | fastmcp, mcp-use, typescript-mcp-server-generator |
