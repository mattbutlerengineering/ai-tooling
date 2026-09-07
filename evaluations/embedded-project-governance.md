# Evaluation: embedded-project-governance

**Repo:** [crichars/embedded-project-governance](https://github.com/crichars/embedded-project-governance)
**Stars:** 23 | **Last updated:** 2026-09-03 (pushed) | **License:** MIT
**Last verified:** 2026-09-07
**Last triaged:** 2026-09-07  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Process

---

## What it does

A lightweight, risk-graded governance skill for AI-assisted embedded firmware development — tiers changes by safety/risk rather than applying one blanket review policy.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual behavior —
it would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`. A narrow-domain (embedded firmware) governance skill; the generic governance skills already catalogued (governed-agent-skills) aren't risk-tiered for firmware-specific safety classes, so this isn't a clean redundancy call. Small (23★), one week old — worth a real look rather than a mechanical SKIP given the differentiated domain.

_Triaged 2026-09-07 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [embedded-project-governance](https://github.com/crichars/embedded-project-governance) | skill | Lightweight, risk-graded governance skill (MIT) for AI-assisted embedded firmware development | Firmware changes carry safety/risk tiers that generic AI-coding governance doesn't distinguish; want risk-graded gates for embedded work | governed-agent-skills, ACMM, claude-md-doctor |
