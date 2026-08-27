# Evaluation: cyclomatic-complexity-skill

**Repo:** [saurabhkumar8112/cyclomatic-complexity-skill](https://github.com/saurabhkumar8112/cyclomatic-complexity-skill)
**Stars:** 103 | **Last updated:** 2026-08-26 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-08-27
**Last triaged:** 2026-08-27  <!-- triaged: bulk -->
**Dev loop stage:** Review (code-quality refactor of changes/codebase)
**Layer:** Tooling

---

## What it does

A Claude skill that refactors code to reduce cyclomatic complexity — the agent
reads a function/module, identifies complexity hot spots, and rewrites toward a
lower branch/decision count while preserving behavior.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata (description, license, star count) plus the CATALOG "Overlaps with"
cell. That is sufficient to place the lead and check it against catalogued
incumbents, not to judge refactor quality or false-positive rate.

## Verdict

**discovery-log — tentative read**

## Triage note

Left at `discovery-log`. `triage.py` places this in P3 backlog — no catalogued
STACK pick's "Overlaps with" cell names it, so there is no structural redundancy
signal. It is a narrowly-scoped, single-purpose skill (cyclomatic complexity only)
distinct from the broader multi-book review skill `brooks-lint` and the local
static-analysis gate `skylos`; worth a real hands-on eval rather than a mechanical
SKIP, but not urgent enough to escalate ahead of this pass's other work.

_Triaged 2026-08-27 by the daily discovery pass (P3 backlog band)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [cyclomatic-complexity-skill](https://github.com/saurabhkumar8112/cyclomatic-complexity-skill) | skill | Claude skill (Apache-2.0) that refactors code to reduce cyclomatic complexity | Linters report complexity metrics but don't fix them; want an agent skill that actively refactors code down to a lower complexity | brooks-lint, ratchet, skylos |
