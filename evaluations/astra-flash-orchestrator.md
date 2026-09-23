# Evaluation: astra-flash-orchestrator

**Repo:** [ethanplusai/astra-flash-orchestrator](https://github.com/ethanplusai/astra-flash-orchestrator)
**Stars:** 613 | **Last updated:** 2026-09-20 (pushed) | **License:** MIT
**Last verified:** 2026-09-23
**Last triaged:** 2026-09-23  <!-- triaged: bulk -->
**Dev loop stage:** Plan + Implement
**Layer:** Process

---

## What it does

A native Codex workflow (Python, MIT) that splits planning/review from implementation across two
models: "Astra" plans and reviews phased tasks while DeepSeek Flash writes the code. Ships phased-task
scaffolding, a verification step, and a documented safe-install/reversible-setup path.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata and
the README's description of the phased-task/verification workflow. That is sufficient to catalog it
and place it relative to existing peers, not to support an ADOPT.

## Verdict

**discovery-log — tentative read**

## Triage note

P3 backlog. Same cross-vendor plan/build split as `architect-loop` (Fable-as-architect,
Codex-as-builder) and `sol-skill` (Claude plans, Sol via Codex writes), but tied to DeepSeek Flash as
the builder specifically. Star count (613 in ~6 days) is unusually fast for a 2-contributor repo and
worth a skeptical look before any hands-on eval — flagging rather than assuming organic. Left at
`discovery-log` rather than SKIPped; no STACK incumbent covers this exact cross-model split.

_Triaged 2026-09-23 by the P3 backlog band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [astra-flash-orchestrator](https://github.com/ethanplusai/astra-flash-orchestrator) | tool | Cross-model plan/build split (MIT) as a native Codex workflow — Astra plans and reviews, DeepSeek Flash implements, with phased tasks and reversible setup | A single model plans and implements with no adversarial check; want a cheaper builder model gated by a separate planning/review model | architect-loop, sol-skill, agy-staff |  |
