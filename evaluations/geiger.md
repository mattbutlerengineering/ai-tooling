# Evaluation: geiger

**Repo:** [Atomburstofficial/geiger](https://github.com/Atomburstofficial/geiger)
**Stars:** 106 | **Last updated:** 2026-09-10 (pushed) | **License:** MIT
**Last verified:** 2026-09-11
**Last triaged:** 2026-09-11  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

A read-only CLI ("a Geiger counter for AI agents") that inventories every agent, MCP
server, plugin, and AI extension installed on a machine in one command — a discovery
scan, not a vulnerability scan.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to distinguish it
from its nearest catalogued neighbors by scope, not to judge accuracy or coverage of
its inventory — a question only a hands-on run could answer.

## Triage note

Left at `discovery-log` rather than SKIPped: `agent-scan` (Snyk) and `agnix` both cover
adjacent ground but as vulnerability/config scanners, not as a pure read-only inventory
of what's installed. `numbat` (Perplexity) does endpoint activity visibility, a
different job again. None of the three dominates geiger's narrower "just list
everything" niche closely enough to call this redundant. Significant enough to deserve
a real hands-on eval rather than a mechanical SKIP.

_Triaged 2026-09-11 — daily discovery pass._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [geiger](https://github.com/Atomburstofficial/geiger) | tool | Read-only inventory scanner (MIT) listing every AI agent, MCP server, plugin, and extension installed on a machine | Nobody has a single command that shows every agent/MCP/plugin footprint on a machine before auditing or removing anything | agent-scan, numbat, agnix |
