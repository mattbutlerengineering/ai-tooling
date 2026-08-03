# Evaluation: autogen

**Repo:** [microsoft/autogen](https://github.com/microsoft/autogen)
**Stars:** 59,615 | **Last updated:** 2026-04-15 (pushed) | **License:** CC-BY-4.0
**Last verified:** 2026-08-03
**Last triaged:** 2026-08-03  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Process (framework)

---

## What it does

Microsoft's programming framework for agentic AI — conversational multi-agent orchestration with a
layered API (Core, AgentChat, Extensions) and a no-code Studio for prototyping.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (microsoft/agent-framework, langchain, crewAI, LangGraph,
semantic-kernel). That is sufficient to place the lead, not to support an ADOPT — this eval offers
none.

## Triage note

Left at `discovery-log`: at ~60K stars, autogen is a major first-party Microsoft multi-agent
framework, largely out of this catalog's dev-loop scope (general agent-backend framework rather
than a coding-agent tool) but too significant and too widely deployed to mechanically SKIP as
redundant. Note the unusual CC-BY-4.0 license (not a standard permissive code license) if this ever
reaches a real eval. Left for the P0/eval-runner lane.

_Triaged 2026-08-03 by today's discovery lead (5-oldest-untriaged pass)._
