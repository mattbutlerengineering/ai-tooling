# Evaluation: blitzstrike

**Repo:** [shinthink/blitzstrike](https://github.com/shinthink/blitzstrike)
**Stars:** 634 | **Last updated:** 2026-09-17 (pushed) | **License:** MIT
**Last verified:** 2026-09-17
**Last triaged:** 2026-09-17  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Infrastructure

---

## What it does

Universal MCP penetration-testing toolbelt — structured methodology across three phases
(reconnaissance/attack-surface mapping, source-to-sink analysis, live validation), a 130-tool
catalog, 57 documented escalation chains, and an intelligence data layer any MCP-speaking agent
can drive for authorized security testing.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (pentest-ai, cve-mcp-server, OpenOSINT). That is sufficient
to place the lead, not to judge the tool's behaviour hands-on.

## Triage note

Left at `discovery-log`. A newly-created (2026-09-12), fast-growing (★634 in under a week)
challenger to the catalog's existing offensive-security MCP servers (`pentest-ai`, `OpenOSINT`).
Whether it's redundant with the incumbent `pentest-ai` or differentiated (its own escalation-chain
methodology and 130-tool catalog) needs an actual look at both tool surfaces, not a mechanical
SKIP on overlap alone — a significant, fast-moving lead deserves a real eval rather than being
dismissed as "another pentest MCP server."

_Triaged 2026-09-17 by the P3 backlog band._
