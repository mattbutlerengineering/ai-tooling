# Evaluation: cospan

**Repo:** [keli-wen/cospan](https://github.com/keli-wen/cospan)
**Stars:** 44 | **Last updated:** 2026-11-21 (pushed) | **License:** MIT
**Last verified:** 2026-11-21
**Last triaged:** 2026-11-21  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

An async delegation protocol connecting several coding-agent CLIs — Antigravity,
Codex, Claude Code, and DeepSeek Harness — so work can be handed off between them
through one shared layer instead of a per-pair integration.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
the CATALOG one-liner plus repo metadata. That is sufficient to place the lead and
note its closest catalogued peers, not to judge its behaviour, and it would not
support an ADOPT.

## Triage note

Landed in P3 backlog (zero overlap pressure — no catalog row currently cites it).
Its closest catalogued peers (`agent-dispatcher`, `cedr`, `orchestra`) each route
tasks to agents rather than delegate between agent *CLIs themselves*, so a
redundancy SKIP isn't well-supported from the README alone. Left at discovery-log
for a real hands-on look if cross-harness delegation protocols become a priority.

_Triaged 2026-11-21 by the P3 backlog band._
