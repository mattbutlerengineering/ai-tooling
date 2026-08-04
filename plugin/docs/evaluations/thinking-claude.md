# Evaluation: thinking-claude

**Repo:** [richards199999/thinking-claude](https://github.com/richards199999/thinking-claude)
**Stars:** 17,066 | **Last updated:** 2026-04-07 (pushed) | **License:** MIT
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Plan (reasoning quality)
**Layer:** Process

---

## What it does

A prompt framework that pushes Claude to reason more deliberately before answering — an instruction
layer that shapes *how* the model thinks rather than what tools it can reach.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata fetched 2026-08-04 plus
the CATALOG one-liner and "Overlaps with" cell (`andrej-karpathy-skills`, `ponytail`, `caveman`).
Enough to place it against the STACK incumbent it names; not enough for a positive verdict, and
none is offered.

## Triage note

Left at `discovery-log`, not SKIPped, on two grounds.

The overlap is thin. The STACK pick it cites is
[`caveman`](https://github.com/JuliusBrussee/caveman), an output-compression skill that shortens
the agent's prose for token savings. thinking-claude works the opposite direction — more
deliberation before the answer. They are not substitutes, and 17K stars is not a tool this lane
should dispose as "redundant" with something it does not resemble.

The real question is a different one, and it is not a redundancy question: extended thinking is now
native to the model, so a prompt framework for "think harder" may be substantially obsoleted by the
harness rather than by any catalogued tool. The repo has not been pushed since 2026-04, which is
consistent with that. Deciding it needs a with/without read on current models — a measured call,
which is P0 work.

Worth flagging for the successor/obsolescence lane rather than the challenger lane: "the platform
absorbed it" is a disposition this catalog does not yet have vocabulary for.

_Triaged 2026-08-04 by the P2 challenger band ([#263](https://github.com/mattbutlerengineering/ai-tooling/issues/263))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [thinking-claude](https://github.com/richards199999/thinking-claude) | framework | Reasoning prompt framework that makes Claude think more deliberately before answering | Shallow first-pass answers on problems that need deliberation | andrej-karpathy-skills, ponytail, caveman |
