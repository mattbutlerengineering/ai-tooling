# Evaluation: agentpace

**Repo:** [mohamedzhioua/agentpace](https://github.com/mohamedzhioua/agentpace)
**Stars:** 5 | **Last updated:** 2026-11-10 (pushed) | **License:** MIT
**Last verified:** 2026-11-11
**Last triaged:** 2026-11-11  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

A zero-dependency Python CLI that measures how long coding agents actually take on real
work — P50/P80/P90 ranges computed from real Claude Code and Codex runs, with the human
portion of any task stated apart rather than derived. Ships an open CC0 dataset and an
agent skill.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata (fetched 2026-11-11) plus the CATALOG one-liner and "Overlaps with" cell. That is
sufficient to decide whether this lead is clearly dominated by a cataloged incumbent, not to
judge the tool's actual behavior — it would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped as redundant with `ccusage` (STACK, MEASURED) despite
the P2 band pointing there. ccusage's job is token/dollar cost from session logs; agentpace's
stated job is wall-clock task *duration* (P50/P80/P90 of real runs), a different measurement
entirely with no cost component. The two answer different questions a reader of this catalog
would ask — "what did this cost" vs. "how long does this actually take" — so this is not the
identical-job overlap P2 exists to catch. The open CC0 dataset is also a differentiator ccusage
doesn't offer. Worth a closer look rather than a mechanical SKIP on a shared citation.

_Triaged 2026-11-11 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agentpace](https://github.com/mohamedzhioua/agentpace) | tool | Zero-dependency CLI (MIT) measuring how long coding agents actually take — P50/P80/P90 ranges from real Claude Code and Codex runs, human time stated apart | Estimating agent task duration relies on human-dev intuition baked into training data, with no measured, open dataset of real agent run times | ccusage, token-step-tracker, claude-monitor |
