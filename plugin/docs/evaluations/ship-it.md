# Evaluation: ship-it

**Repo:** [LunkiBR/ship-it](https://github.com/LunkiBR/ship-it)
**Stars:** 17 | **Last updated:** 2026-08-09 (pushed) | **License:** MIT
**Last verified:** 2026-08-11
**Last triaged:** 2026-08-11  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Process

---

## What it does

A Claude Code skill (MIT) that catches commonly-forgotten UX/product details before shipping a screen or feature — an accessibility/UX checklist run as an agent skill rather than a human review pass.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata and README/topic description. Not enough to judge whether the checklist catches real issues versus generic boilerplate advice.

## Verdict

**discovery-log — tentative read**

## Triage note

Newly discovered and catalogued today. Left at `discovery-log` — a narrow, UX/product-checklist-specific Review skill, distinct enough from the code-focused `brooks-lint`/`vet`/`pristine-skill` cluster (which review code quality and completion honesty, not UX/accessibility detail) that a mechanical redundancy SKIP isn't warranted.

_Triaged 2026-08-11 by the daily discovery-and-triage pass._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ship-it](https://github.com/LunkiBR/ship-it) | skill | Claude Code skill (MIT) catching commonly-forgotten UX/product details before shipping a screen or feature | Agents ship screens missing routine UX/accessibility details a human reviewer would catch | brooks-lint, vet, pristine-skill |
