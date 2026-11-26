# Evaluation: inference-optimisation-skill

**Repo:** [sybil-solutions/inference-optimisation-skill](https://github.com/sybil-solutions/inference-optimisation-skill)
**Stars:** 2,777 | **Last updated:** 2026-11-16 (pushed) | **License:** MIT
**Last verified:** 2026-11-26
**Last triaged:** 2026-11-26  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Agent skill for hill-climbing local LLM serving speed — decode, speculative decoding,
prefill, KV cache, startup time, and time-to-first-token — across arbitrary hardware and
quantization setups.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this skill. This evaluation is source-grounded only: the
CATALOG one-liner and the "Overlaps with" cell.

## Triage note

Left at `discovery-log`, not SKIPped, despite citing STACK pick `caveman` in its "Overlaps
with" cell. `caveman` cuts **output tokens** in agent prose (a context-window/cost concern);
this skill tunes **local LLM serving-engine performance** (decode/prefill/KV/quantization) —
a different job that happens to share the loose "token/speed efficiency" neighborhood. Not
redundant, so no mechanical P2 SKIP applies. A real hands-on eval would need a GPU rig and a
disclosed before/after serving-speed benchmark to earn MEASURED evidence.

_Triaged 2026-11-26 by the daily discovery routine (new lead, same-day triage)._
