# Evaluation: ACE (agentic-context-engine)

**Repo:** [kayba-ai/agentic-context-engine](https://github.com/kayba-ai/agentic-context-engine)
**Stars:** 2,600 | **Last updated:** 2026-09-23 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-10-01
**Last triaged:** 2026-10-01  <!-- triaged: bulk -->
**Dev loop stage:** Reflect
**Layer:** Infrastructure

---

## What it does

A persistent learning loop with Agent/Reflector/SkillManager roles that curate a "Skillbook" of
strategies extracted from execution traces — no fine-tuning, no vector DB. Claims 2x consistency
on Tau2 and 49% fewer tokens; works across LiteLLM/100+ providers, not tied to one harness.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead, not to support an
ADOPT, and none is offered here.

## Triage note

Left at `discovery-log`. Cites `claude-reflect` (STACK, KEEP) in "Overlaps with", which bands
this P2, but the two differ in scope and maturity: `claude-reflect` is a Claude-Code-specific
plugin that captures corrections/preferences and syncs them to `CLAUDE.md`; `ACE` is a provider-
agnostic framework (LiteLLM/100+ providers) with a structured three-role architecture (Agent /
Reflector / SkillManager) curating a persistent "Skillbook," and ships its own benchmark claims
(2x consistency on Tau2, 49% fewer tokens). No eval existed before this pass. The structured,
cross-provider design and the stated benchmark are different enough from `claude-reflect`'s
simpler correction-capture model to deserve a real hands-on look rather than a mechanical SKIP.

_Triaged 2026-10-01 by the P2 challenger band._
