# Evaluation: vuln-report-skill

**Repo:** [v-yun/vuln-report-skill](https://github.com/v-yun/vuln-report-skill)
**Stars:** 48 | **Last updated:** 2026-08-21 (pushed) | **License:** MIT
**Last verified:** 2026-08-21
**Last triaged:** 2026-08-21  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Process

---

## What it does

A Claude Code skill that turns a confirmed vulnerability into a submission-ready DOCX bug-bounty/CVE report, with a layered verification gate and a step-structured PoC section.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for the
triage note below, not for an ADOPT, and this eval offers none.

## Triage note

Cited as overlapping `SkillSpector` by category proximity (both Security & Safety),
but the jobs don't match — SkillSpector scans skills for malicious patterns before
install, this generates a submission report *after* a vulnerability is already
confirmed. Not redundant; left at discovery-log rather than SKIPped.

_Triaged 2026-08-21 by the P2 challenger band._
