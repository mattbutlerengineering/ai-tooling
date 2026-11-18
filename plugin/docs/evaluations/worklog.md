# Evaluation: worklog

**Repo:** [Abdoul-sudo/worklog](https://github.com/Abdoul-sudo/worklog)
**Stars:** 16 | **Last updated:** 2026-11-18 (pushed) | **License:** MIT
**Last verified:** 2026-11-18
**Last triaged:** 2026-11-18  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

A Claude Code mod that automatically tracks time, tokens, and API price for each project,
rendered as a yearly activity heatmap with 8 selectable themes.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the CATALOG
one-liner plus repo metadata. Sufficient for a redundancy-based SKIP, not for an ADOPT, which
this eval does not offer.

## Verdict

**SKIP** — redundant with `ccusage` (STACK, ADOPT, MEASURED): both turn Claude Code session logs
into per-project time/token/cost reporting. The yearly heatmap and theming are presentation, not
a new capability `ccusage` (or the surrounding `tokentab`/`peek`/`codeburn` reporting cluster)
doesn't already provide.

_Triaged 2026-11-18 by the P2 challenger band._
