# Evaluation: hoist-the-elephant

**Repo:** [jinhanbuilds/hoist-the-elephant](https://github.com/jinhanbuilds/hoist-the-elephant)
**Stars:** 29 | **Last updated:** 2026-08-24 (pushed) | **License:** MIT
**Last verified:** 2026-08-30
**Last triaged:** 2026-08-30  <!-- triaged: bulk -->
**Dev loop stage:** Reflect
**Layer:** Process

---

## What it does

A skill (MIT) that re-anchors a long conversation that has drifted through a series of repeated local corrections — reconciling the accumulated small fixes against the original intent instead of letting them compound silently.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell (`claude-reflect`, `ballast`, `claude-subconscious`). It would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log` (P2 challenger: cites `claude-reflect` in "Overlaps with"). Not SKIPped as redundant — `claude-reflect` persists corrections and preferences *across sessions* into CLAUDE.md, while this skill operates *within* one long-running conversation, re-anchoring against drift as it happens rather than learning for next time. Different mechanism and different moment of use; whether it earns a seat needs a real look.

_Triaged 2026-08-30 by the P2 challenger band ([#567](https://github.com/mattbutlerengineering/ai-tooling/issues/567))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [hoist-the-elephant](https://github.com/jinhanbuilds/hoist-the-elephant) | skill | Skill (MIT) re-anchoring long conversations that drift through repeated local corrections | Long sessions drift off-goal through a series of small local corrections that never get reconciled against the original intent | claude-reflect, ballast, claude-subconscious |
