# Evaluation: assay

**Repo:** [metahub-ai/assay](https://github.com/metahub-ai/assay)
**Stars:** 3 | **License:** Apache-2.0
**Last verified:** 2026-08-05
**Last triaged:** 2026-08-05  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

A reproducible evaluation framework for AI artifacts — skills, MCP servers, agents, and
plugins — that reads what's inside them, optionally runs them in a sandbox and judges what
they did, and publishes a report a stranger can verify.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell (scenario, agnix, SkillSpector). That is
sufficient to place the lead, not to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: scenario tests *agent behavior* via user simulation; agnix lints
*config* well-formedness; SkillSpector scans skills for *malice*. None runs a skill/MCP
server/plugin sandboxed end-to-end and publishes a stranger-verifiable behavioral report the
way assay claims to — directly relevant to this repo's own evaluation methodology and worth
a hands-on look rather than a redundancy SKIP. Very early (3 stars, created two days ago).

_Triaged 2026-08-05 by the daily discovery routine (today's new lead)._
