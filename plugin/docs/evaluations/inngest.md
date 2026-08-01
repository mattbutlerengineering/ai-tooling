# Evaluation: inngest

**Repo:** [inngest/inngest](https://github.com/inngest/inngest)
**License:** NOASSERTION
**Last verified:** 2026-07-31
**Last triaged:** 2026-07-31  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

Workflow orchestration platform for durable, resumable step functions and AI workflows — lets
agent/AI workflows survive failures and resume without managing the underlying infrastructure.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
(`repo-metadata.json` records `license_spdx: NOASSERTION`) plus the CATALOG "Overlaps with" cell
(conductor, agent-kit, LangGraph). That is sufficient to apply this repo's license bar, not to
judge the tool's behavior — this eval offers no ADOPT/KEEP/CONDITIONAL opinion.

## Verdict

**SKIP** — license is `NOASSERTION` (GitHub cannot confirm a permissive license from the repo's
LICENSE file), failing this repo's license bar: "copyleft or missing license ⇒ SKIP (only
permissive MIT-like OSS is adoptable)." conductor (Apache-2.0) and LangGraph already cover the
durable-agent-workflow job with a clear license. Re-evaluate if the repo publishes an
unambiguous permissive license.

_Triaged 2026-07-31 by the P3 backlog band._
