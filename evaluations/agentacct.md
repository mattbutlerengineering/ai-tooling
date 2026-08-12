# Evaluation: agentacct

**Repo:** [mikehasa/agentacct](https://github.com/mikehasa/agentacct)
**Stars:** 534 | **Last updated:** 2026-07-30 (pushed) | **License:** MIT
**Last verified:** 2026-08-12
**Last triaged:** 2026-08-12  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

Local-first dashboard that breaks each coding-agent task into its work steps — tools used, files
changed, tests run, time and tokens spent — for Claude Code, Codex, OpenCode, and more. No login,
no telemetry.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (codeburn, agentsview, ccusage). That is sufficient to
place the lead and note its differentiation (task/step-level breakdown vs. plain token/cost
totals), not to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log` rather than SKIPped: `ccusage` (STACK, MEASURED) and `codeburn` report
cost totals, but agentacct's pitch is a step-by-step task breakdown (tools/files/tests per task)
across multiple coding-agent CLIs, which is a materially different artifact, not a rehash of an
existing STACK pick. 534 stars in under a week also signals real momentum. Deserves a real
hands-on eval rather than a mechanical SKIP; left for the P0/eval-runner lane.

_Triaged 2026-07-30 as part of a new discovery-log intake, not a P1/P2/P3 bulk-band pass._
