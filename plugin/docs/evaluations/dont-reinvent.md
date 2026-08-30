# Evaluation: dont-reinvent

**Repo:** [Emanuelel/dont-reinvent](https://github.com/Emanuelel/dont-reinvent)
**Stars:** 25 | **Last updated:** 2026-08-28 (pushed) | **License:** MIT
**Last verified:** 2026-08-30
**Last triaged:** 2026-08-30  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Process

---

## What it does

A Claude Skill that checks Free vs. Build vs. Buy before an agent writes new code — and actually vets what it finds (license, maintenance activity, security posture) rather than stopping at a star count.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. It would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log` — a first-time lead with no overlap pressure yet. Nothing else in the catalog turns pre-build dependency vetting (license/maintenance/security, not just stars) into a Skill an agent invokes before writing code; whether it does that reliably enough to earn a seat needs a real run.

_Triaged 2026-08-30 by the P3 backlog band ([#567](https://github.com/mattbutlerengineering/ai-tooling/issues/567))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [dont-reinvent](https://github.com/Emanuelel/dont-reinvent) | skill | Claude Skill (MIT) checking Free vs. Build vs. Buy before writing code, vetting license, maintenance, and security beyond star count | Agents default to writing code from scratch instead of vetting whether an existing library already solves it safely | — (unique: pre-build dependency vetting) |
