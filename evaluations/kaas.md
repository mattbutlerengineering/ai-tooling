# Evaluation: kaas

**Repo:** [bybit-exchange/kaas](https://github.com/bybit-exchange/kaas)
**Stars:** 81 | **Last updated:** 2026-08-02 (pushed) | **License:** MIT
**Last verified:** 2026-08-03
**Last triaged:** 2026-08-03  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

LLM knowledge-base compiler that turns scattered notes, docs, and transcripts into a queryable
Markdown wiki via MCP, with no embeddings and a self-hosted deployment.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (mem0, cognee, memU, byterover-cli). That is sufficient to
place the lead and note none of its named overlaps is a STACK incumbent, not to support an ADOPT —
this eval offers none.

## Triage note

Left at `discovery-log`: none of mem0, cognee, memU, or byterover-cli is in STACK, and kaas's
differentiator (no-embedding, self-hosted Markdown wiki compiler vs. the vector/graph-DB memory
layers those tools are) is a real architectural distinction, not a clone. Left for the
P0/eval-runner lane.

_Triaged 2026-08-03 by today's discovery lead._
