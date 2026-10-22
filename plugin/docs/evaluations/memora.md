# Evaluation: memora

**Repo:** [Codrihub/memora](https://github.com/Codrihub/memora)
**Stars:** 7 | **Last updated:** 2026-10-21 (pushed) | **License:** MIT
**Last verified:** 2026-10-22
**Last triaged:** 2026-10-22  <!-- triaged: bulk -->
**Dev loop stage:** Reflect
**Layer:** Infrastructure

---

## What it does

A self-hosted memory vault (MIT) agents read and write over MCP — install with npm,
Docker, or one command.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead
against its closest catalog peers, not to support any verdict, and none is offered here.

## Triage note

Bands as a P2 challenger against `claude-mem` (ADOPT, pressure 0), but the two differ in
architecture: `claude-mem` is a Claude-Code-specific plugin with semantic search and
timeline views, while this is a generic, harness-agnostic self-hosted vault reachable
over plain MCP. Too new (★7, 4 days old) and too thinly documented from source alone to
call redundant with confidence. No archived flag, no disqualifying license, no
`Ships inside` container. Left at `discovery-log` for a real hands-on eval.

_Triaged 2026-10-22 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [memora](https://github.com/Codrihub/memora) | tool | Self-hosted memory vault (MIT) agents read and write over MCP — install with npm, Docker, or one command | Agent memory layers require either a hosted service or hand-rolled infra; want a simple self-hosted vault reachable over MCP | OMEGA, claude-mem, ownmem |
