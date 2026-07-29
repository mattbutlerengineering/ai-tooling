# Evaluation: SaveContext

**Repo:** [AlexanderBoger/SaveContext](https://github.com/AlexanderBoger/SaveContext)
**Stars:** 5 | **Last updated:** 2026-07-23 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-07-29
**Last triaged:** 2026-07-29  <!-- triaged: bulk -->
**Dev loop stage:** MCP Servers (infrastructure)
**Layer:** Infrastructure (MCP server)

---

## What it does

An MCP server described as "Git LFS for your LLM context" — keeps big documents out of the model
and returns byte-exact quotes for a fraction of the tokens. Surfaced in the 2026-07-29 daily
discovery scan.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (`headroom`, `token-optimizer-mcp`, `context-mode`,
`claw-compactor`). `headroom` is KEEP in STACK.md and compresses tool outputs/logs/files broadly,
but SaveContext's specific claim — byte-exact quote retrieval from large documents kept entirely
out of context — is a narrower, document-specific mechanism none of the four overlaps make
explicit, so a mechanical SKIP isn't defensible from metadata alone.

## Triage note

Left at `discovery-log`: very early (5 stars, days old) but a specific enough mechanism
(byte-exact quoting, not just compression) to deserve a real eval rather than a redundancy SKIP.

_Triaged 2026-07-29 by the daily discovery scan's same-day triage pass._
