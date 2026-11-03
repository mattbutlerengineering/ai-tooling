# Evaluation: opus-tuner-claude-skill

**Repo:** [YahyaLendani/opus-tuner-claude-skill](https://github.com/YahyaLendani/opus-tuner-claude-skill)
**Stars:** 14 | **Last updated:** 2026-11-03 (pushed) | **License:** MIT
**Last verified:** 2026-11-03
**Last triaged:** 2026-11-03  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Cost control for long-running Claude Code sessions on Windows, macOS, and Linux: tiered
context ceilings that trigger as a session grows, a blocking handoff gate at the
ceiling, and adjustable effort gears to trade thoroughness for cost.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner and repo metadata. Whether the tiered ceilings and handoff gate
actually prevent runaway context/cost growth in practice is untested here.

## Triage note

Left at `discovery-log` (P2 challenger — cites `headroom`). `headroom` compresses tool
outputs/logs before they reach the LLM; `opus-tuner-claude-skill` governs the session
itself (tiered context ceilings, a blocking handoff gate, effort gears) — a different
mechanism aimed at the same cost/context problem rather than a straight substitute.
Not examined further in this pass.

_Triaged 2026-11-03 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [opus-tuner-claude-skill](https://github.com/YahyaLendani/opus-tuner-claude-skill) | skill | Cost control (MIT) for long Claude Code sessions — tiered context ceilings, a blocking handoff gate, and effort gears | Long-running sessions blow through context and cost budgets with no ceiling, handoff gate, or effort throttle | compact-adviser, taskcut, headroom |
