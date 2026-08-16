# Evaluation: opencode-cache-stats

**Repo:** [nmdra/opencode-cache-stats](https://github.com/nmdra/opencode-cache-stats)
**Stars:** 19 | **Last updated:** 2026-08-09 (pushed) | **License:** MIT
**Last verified:** 2026-08-16
**Last triaged:** 2026-08-16  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

Lightweight opencode TUI plugin showing live cache hit rate, per-model/subagent breakdown, and
associated costs.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (ccusage, tokentab, claude-monitor). That is sufficient to
place the lead and note the STACK incumbent it cites, not to support an ADOPT — this eval offers
none.

## Triage note

Left at `discovery-log`, not SKIPped as a P2 challenger: ccusage (STACK pick) reports Claude Code
session cost/usage; opencode-cache-stats is scoped to a different harness (opencode) with no
Claude Code equivalent doing this job. Different ecosystem, not redundant. Left for the
P0/eval-runner lane.

_Triaged 2026-08-16 by the P2 challenger band._
