# Evaluation: hubo

**Repo:** [h0ngcha0/hubo](https://github.com/h0ngcha0/hubo)
**Stars:** 26 | **Last updated:** 2026-07-28 | **License:** MIT
**Last verified:** 2026-07-28
**Last triaged:** 2026-07-28  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

An agent skill where two agents spar over one codebase — one reviews, the other defends/fixes — until every review finding raised is reconciled, rather than left as an unresolved comment thread. Works with Claude Code, Codex, and Copilot.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata (GitHub API: 26 stars, MIT, pushed 2026-07-28) plus the CATALOG "Overlaps with" cell against claude-octopus/code-review/PR-Agent. Sufficient to catalog and note the gap (adversarial reconciliation loop vs. those tools' single-pass or consensus review), not to judge how well the loop actually converges.

## Triage note

Distinct from claude-octopus (multi-LLM consensus gate) and code-review/PR-Agent (single-pass structured review) in explicitly looping two agents until findings are *resolved*, not just raised — a real gap in the Code Review & Quality category. Left at discovery-log for a future hands-on eval.
