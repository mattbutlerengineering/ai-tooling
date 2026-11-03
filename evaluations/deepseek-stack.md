# Evaluation: deepseek-stack

**Repo:** [aicodeking/deepseek-stack](https://github.com/aicodeking/deepseek-stack)
**Stars:** 145 | **Last updated:** 2026-10-28 (pushed) | **License:** MIT
**Last verified:** 2026-11-03
**Last triaged:** 2026-11-03  <!-- triaged: bulk -->
**Dev loop stage:** All stages (agent skills spanning planning, verification, and shipping)
**Layer:** Process

---

## What it does

An agent skill pack installed via `npx skills add aicodeking/deepseek-stack`, aimed at
giving DeepSeek-backed coding agents the plan/verify/ship discipline that frontier-model
skill packs (e.g. `mcode-stack`, `godmode`) assume the underlying model already has.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner and repo metadata. Whether the skill pack meaningfully closes the gap
for DeepSeek-class models versus frontier models is untested here.

## Triage note

Left at `discovery-log` (P2 challenger — cites `mattpocock/skills`). The incumbent is a
general harness-agnostic engineering skills pack, not scoped to any particular model;
`deepseek-stack` targets a specific gap (tuning DeepSeek-class models toward
frontier-model planning/verification discipline) the incumbent doesn't address. Same
shape as `mcode-stack` (MiniMax-specific), which was also left rather than SKIPped
against the same incumbent. Not examined further in this pass.

_Triaged 2026-11-03 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [deepseek-stack](https://github.com/aicodeking/deepseek-stack) | skill | Agent skill pack (MIT) making DeepSeek models plan, verify, and ship like frontier models | DeepSeek-backed coding agents lack the planning/verification discipline frontier-model skill packs assume | mcode-stack, godmode, mattpocock/skills |
