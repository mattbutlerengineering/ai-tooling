# Evaluation: better-skill-creator

**Repo:** [rolling-codes/better-skill-creator](https://github.com/rolling-codes/better-skill-creator)
**Stars:** 4 | **Last updated:** 2026-10 (recently active; exact push date not independently verifiable this session — see below) | **License:** Apache-2.0
**Last verified:** 2026-10-20
**Last triaged:** 2026-10-20  <!-- triaged: bulk -->
**Dev loop stage:** Reflect
**Layer:** Tooling

---

## What it does

A Claude Code skill-authoring system: multi-angle design review, adversarial
testing against the written skill, quality gates, and a description optimizer,
aimed at skills that actually trigger reliably instead of ones assumed to.

## How we tested it

**Evidence:** SOURCE-ONLY

**Source-grounded review — not run hands-on.** This session's GitHub access is
scoped to `mattbutlerengineering/ai-tooling` only; arbitrary-repo API lookups and
installs are not available without an explicit `add_repo` grant, which an
unattended discovery pass does not request. This read comes from the repo's public
GitHub page (About text, README) via a web fetch, not from running the tool.

## What worked

- N/A — not run.

## What didn't work or surprised us

- N/A — not run.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Not exercised. |
| Speed | neutral | Not exercised. |
| Maintainability | neutral | Not exercised. |
| Safety | neutral | Not exercised. |
| Cost Efficiency | neutral | Not exercised. |
| Verifiability | neutral | Not exercised. |

## Verdict

**SKIP** — redundant with `skill-creator` (already ADOPTed as a STACK pick).
Anthropic's first-party `skill-creator` already runs the same job this tool claims —
draft → eval (with-skill vs baseline) → benchmark → triggering-optimization →
package — and is the catalog's measured, installed incumbent for skill authoring.
`better-skill-creator` (4 stars, Apache-2.0) states no concrete advantage over it in
its own description beyond overlapping review/quality-gate language; a second,
far-lower-adoption tool for the same job earns nothing here. Revisit if a future
hands-on look finds a specific capability `skill-creator` lacks.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [better-skill-creator](https://github.com/rolling-codes/better-skill-creator) | plugin | Claude Code skill-authoring system (Apache-2.0) with multi-angle design review, adversarial testing, quality gates, and a description optimizer | Hand-written skills often fail to trigger reliably and nobody measures whether they work | skill-creator, SkillOpt |
