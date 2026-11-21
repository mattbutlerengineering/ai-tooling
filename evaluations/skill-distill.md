# Evaluation: skill-distill

**Repo:** [sybil-solutions/skill-distill](https://github.com/sybil-solutions/skill-distill)
**Stars:** 157 | **Last updated:** 2026-11-21 (pushed) | **License:** MIT
**Last verified:** 2026-11-21
**Last triaged:** 2026-11-21  <!-- triaged: bulk -->
**Dev loop stage:** Skills & Plugins
**Layer:** Tooling

---

## What it does

Distills a good Claude Code or Codex session into a skill that an open-weight model
can follow to reproduce the task — a session-to-skill extraction step, narrower
than general skill authoring from scratch.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
the CATALOG one-liner plus repo metadata. Sufficient to place the lead, not to
confirm the extraction quality or how it compares hands-on to `skill-creator`.

## Triage note

Banded P2 (challenges `skill-creator`). `skill-creator` is a general
draft -> eval -> benchmark -> package authoring meta-skill; skill-distill's job —
deriving a skill from one specific past session, targeted at open-weight-model
reproducibility — isn't a capability `skill-creator`'s own description claims.
Differentiated enough to withhold a redundancy SKIP. Left at discovery-log.

_Triaged 2026-11-21 by the P2 challenger band._
