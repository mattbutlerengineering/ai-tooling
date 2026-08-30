# Evaluation: rubber-duck

**Repo:** [centsandcode/rubber-duck](https://github.com/centsandcode/rubber-duck)
**Stars:** 14 | **Last updated:** 2026-08-21 (pushed) | **License:** MIT
**Last verified:** 2026-08-30
**Last triaged:** 2026-08-30  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Process

---

## What it does

A Socratic debugging skill for AI agents (MIT) that answers a debugging question with questions instead of the fix, on the premise that the developer should find the bug rather than be handed it.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell (`old-coder`, `vet`, `Assumptions`). It would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log` — a first-time lead with no overlap pressure yet. `old-coder` and `Assumptions` are evidence-first debugging skills in the same neighborhood but neither is Socratic in framing (guiding the developer to the answer rather than proving one); whether that framing is actually useful in an agentic context (vs. just slower) needs a real run.

_Triaged 2026-08-30 by the P3 backlog band ([#567](https://github.com/mattbutlerengineering/ai-tooling/issues/567))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [rubber-duck](https://github.com/centsandcode/rubber-duck) | skill | Socratic debugging skill (MIT) that answers with questions instead of the fix | Agents jump straight to a fix instead of building the developer's own understanding of the bug | old-coder, vet, Assumptions |
