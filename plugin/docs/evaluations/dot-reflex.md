# Evaluation: dot-reflex

**Repo:** [usedotai/dot-reflex](https://github.com/usedotai/dot-reflex)
**Stars:** 80 | **Last updated:** 2026-08-28 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-08-30
**Last triaged:** 2026-08-30  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

An open-source execution-recovery controller for coding and tool-using AI agents — detects a failed or stuck run and recovers it rather than leaving the run lost. Ships alongside a fine-tuned recovery model on Hugging Face.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell (`ralph-claude-code`, `claude-code-harness`, `proof-of-done-loop`). It would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log` — a first-time lead with no overlap pressure yet. The catalog's autonomous-loop tools (`ralph-claude-code`, `claude-code-harness`) bundle their own exit/review logic; this one is narrower and model-backed — a dedicated recovery controller rather than a full loop harness. Whether a separate, pluggable recovery layer is worth adopting over what's already bundled needs a real look.

_Triaged 2026-08-30 by the P3 backlog band ([#567](https://github.com/mattbutlerengineering/ai-tooling/issues/567))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [dot-reflex](https://github.com/usedotai/dot-reflex) | tool | Open-source execution-recovery controller (Apache-2.0) for coding and tool-using AI agents | Agents fail mid-task with no recovery path, losing the run instead of resuming it | ralph-claude-code, claude-code-harness, proof-of-done-loop |
