# Evaluation: conductor

**Repo:** [conductor-oss/conductor](https://github.com/conductor-oss/conductor)
**Stars:** 32,055  <!-- repo-metadata.json, fetched 2026-08-04 -->
**License:** Apache-2.0
**Last verified:** 2026-07-31
**Last triaged:** 2026-07-31  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

Event-driven agentic workflow engine (Netflix Conductor successor) for durable, highly
resilient AI agent execution — a substrate that survives failures and handles long-running
distributed tasks.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (inngest, agent-kit, LangGraph). That is sufficient to
place the lead and note none of its named overlaps are STACK incumbents, not to support an
ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: neither inngest, agent-kit, nor LangGraph is in STACK, and conductor's
job — a durable, distributed workflow substrate descended from Netflix's production Conductor,
at 32K stars — is materially different from LangGraph's in-process agent-graph framework. Not a
mechanical SKIP; deserves a real hands-on eval before any verdict. Left for the P0/eval-runner
lane.

_Triaged 2026-07-31 by the P3 backlog band._
