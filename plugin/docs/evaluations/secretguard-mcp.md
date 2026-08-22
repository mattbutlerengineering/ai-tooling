# Evaluation: secretguard-mcp

**Repo:** [vladimirbakalov/secretguard-mcp](https://github.com/vladimirbakalov/secretguard-mcp)
**Stars:** 0 | **Last updated:** 2026-08-13 (pushed) | **License:** MIT
**Last verified:** 2026-08-22
**Last triaged:** 2026-08-22  <!-- triaged: bulk -->
**Dev loop stage:** Review (Security & Safety)
**Layer:** Tooling

---

## What it does

A zero-config MCP server that catches hardcoded secrets before a coding agent writes or commits them — no API key, runs locally over stdio.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a leave decision, not on the tool's behaviour. It would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped. `cc-safety-net` and `toolpermit` are pre-execution guardrails but target destructive commands and tool-call policy respectively, not secret-in-diff detection specifically; `envlatch` addresses credential storage, not detection. secretguard-mcp's specific angle — an MCP server gating the write/commit step itself, rather than a CLI hook or filesystem tool — plus its "catch it before CI" framing makes a mechanical redundancy call unsafe from metadata alone. Zero stars and no activity since creation (2026-08-12); worth a real look once it shows more traction.

_Triaged 2026-08-22 by the P3 backlog band._
