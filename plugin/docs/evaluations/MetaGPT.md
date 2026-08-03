# Evaluation: MetaGPT

**Repo:** [FoundationAgents/MetaGPT](https://github.com/FoundationAgents/MetaGPT)
**Stars:** ~69,000 | **License:** MIT
**Last verified:** 2026-08-03
**Last triaged:** 2026-08-03  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Process (framework)

---

## What it does

Multi-agent "AI software company" framework — assigns roles (PM, architect, engineer, QA) to LLM
agents that turn a one-line requirement into PRDs, designs, and code.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (gpt-engineer, crewAI, autogen, ChatDev-style). That is
sufficient to place the lead, not to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: at ~69K stars, MetaGPT is a major, well-known role-based multi-agent
framework with a real architectural identity (simulated software company with fixed roles) distinct
from the general-purpose multi-agent frameworks it's catalogued near. Too significant to SKIP as
"redundant" on a source-only read. Left for the P0/eval-runner lane.

_Triaged 2026-08-03 by today's discovery lead (5-oldest-untriaged pass)._
