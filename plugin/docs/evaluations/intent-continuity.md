# Evaluation: intent-continuity

**Repo:** [Emmimal/intent-continuity](https://github.com/Emmimal/intent-continuity)
**Stars:** 34 | **Last updated:** 2026-09-16 (pushed) | **License:** MIT
**Last verified:** 2026-09-17
**Last triaged:** 2026-09-17  <!-- triaged: bulk -->
**Dev loop stage:** Reflect
**Layer:** Infrastructure

---

## What it does

Pure-Python system (companion code for a Towards Data Science article) that automatically
discovers, verifies, and applies relevant historical requirements for coding agents — no
embeddings, no vector database, no LLM calls, so requirement resurfacing is deterministic rather
than semantic-similarity-based.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (mex, ownmem, okf-agent-memory). That is sufficient to
place the lead, not to judge the tool's behaviour hands-on.

## Triage note

Left at `discovery-log`. A small (★34), very new research-companion repo rather than a maintained
product; the no-embeddings/no-vector-DB/no-LLM-calls design is a genuinely different mechanism
from the catalog's existing memory tools (which mostly lean on semantic search or knowledge
graphs), so a mechanical redundancy SKIP against `mex`/`ownmem` would be premature. Worth a look
if the deterministic-retrieval approach holds up, but not yet enough signal (age, adoption) to
call it either way.

_Triaged 2026-09-17 by the P3 backlog band._
