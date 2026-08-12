# Evaluation: KADATH

**Repo:** [i3T4AN/KADATH](https://github.com/i3T4AN/KADATH)
**Stars:** 165 | **Last updated:** 2026-08-09 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-08-12
**Last triaged:** 2026-08-12  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

An evolutionary multi-agent runtime that breeds, evaluates, and improves autonomous agents across
reproducible epochs to converge on a goal.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: repo metadata plus the CATALOG
"Overlaps with" cell. Enough to place it against nearby self-improving agent harnesses, not enough
for any verdict, and none is offered.

## Triage note

Left at `discovery-log`. Its self-evolving-agent framing echoes `praisonai`/`CowAgent`/`Hermes
Agent`, but KADATH's genetic/epoch-based breeding mechanism is a different technique from those
tools' memory-and-reflection style self-improvement — not clearly redundant, and genuinely novel
enough in this catalog to deserve a real look rather than a mechanical dispose.

_Triaged 2026-08-12 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [KADATH](https://github.com/i3T4AN/KADATH) | framework | Evolutionary multi-agent runtime (Apache-2.0) that breeds, evaluates, and improves autonomous agents across reproducible epochs | Hand-tuning agent configurations doesn't converge on a goal; want agents that evolve toward one across generations | praisonai, CowAgent, Hermes Agent |
