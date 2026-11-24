# Evaluation: joggernaut

**Repo:** [usejog/joggernaut](https://github.com/usejog/joggernaut)
**Stars:** 47 | **Last updated:** 2026-11-24 (pushed) | **License:** MIT
**Last verified:** 2026-11-24
**Last triaged:** 2026-11-24  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Agent skills that find why a PR is waiting on GitHub Actions CI, fix the cause you pick, and measure the fix — built from fixes other teams measured plus first-principles checks.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell.

## Verdict

**discovery-log — tentative read** — a CI-failure diagnosis skill, distinct from running Claude Code itself as a GitHub Action.

## Triage note

Left at `discovery-log`, not SKIPped. It cites `claude-code-action` in Overlaps, but that's infrastructure for running Claude Code inside CI, while joggernaut diagnoses *why* a PR is stuck on CI and proposes/measures a fix — a different job that could run alongside it. Left for a real eval.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [joggernaut](https://github.com/usejog/joggernaut) | skill | Agent skills (MIT) that find why a PR is waiting on GitHub Actions CI, fix the chosen cause, and measure the fix | CI failures get re-run or guessed at instead of diagnosed; want a skill that finds the actual cause and verifies the fix worked | turboship, claude-code-action, commit-commands |
