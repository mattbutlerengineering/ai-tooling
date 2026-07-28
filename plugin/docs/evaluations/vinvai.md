# Evaluation: VinvAI

**Repo:** [VinvAI/VinvAI](https://github.com/VinvAI/VinvAI)
**Stars:** 31 | **Last updated:** 2026-07-28 | **License:** Apache-2.0
**Last verified:** 2026-07-28
**Last triaged:** 2026-07-28  <!-- triaged: bulk -->
**Dev loop stage:** Reflect (agent-code verification / Outer Loop)
**Layer:** Infrastructure

---

## What it does

Zero-edit runtime tracing that joins every agent-written call back to its source, building one context graph served to Claude Code and Cursor over MCP. Runs, benchmarks, and optimizes agent-written Python code, with every fix verified against tests the agent never sees.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata (GitHub API: 31 stars, Apache-2.0, pushed 2026-07-28, 15 open issues suggesting active early development) plus the CATALOG "Overlaps with" cell against claude-devtools/harbor/code-review/vet. Sufficient to catalog and note the gap (runtime-traced root-cause + held-out test verification), not to judge tracing overhead or verification robustness hands-on.

## Triage note

Distinct from claude-devtools (session-log visual debugger) and harbor (whole-agent benchmarking) by tracing actual runtime execution back to source and verifying fixes against tests the agent itself never sees — a genuine anti-overfitting angle. 15 open issues on a 5-day-old repo signal early-stage churn; worth watching before a hands-on eval. Left at discovery-log.
