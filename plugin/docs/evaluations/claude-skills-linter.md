# Evaluation: claude-skills-linter

**Repo:** [shinytoyrobots/claude-skills-linter](https://github.com/shinytoyrobots/claude-skills-linter)
**Stars:** 2 | **Last updated:** 2026-11-08 (pushed) | **License:** MIT
**Last verified:** 2026-11-09
**Last triaged:** 2026-11-09  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

A deterministic structural linter and token-efficiency auditor for Claude Code skills,
published to npm as `claude-skill-lint` — catches broken references, orphaned files, and
dependency cycles that an LLM reviewing a skill directory won't reliably flag.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the npm
package metadata, the repo's own description, and the CATALOG "Overlaps with" cell
(`skillfid`, `skilldiff`, `oil-skill-creator`). That is sufficient to check for a named
STACK redundancy; it is not sufficient to support an ADOPT, and this eval offers none.

## Verdict

**discovery-log — tentative read** — tiny (2 stars) and brand new, but fills a real,
narrow gap: `skillfid` checks execution-vs-documentation drift and `skilldiff` checks
behavioral regressions, while this is the only cataloged tool doing plain structural
linting (broken refs, orphans, cycles) of a skill directory — a mechanical check, not an
LLM judgment call. Worth a first look rather than a mechanical SKIP despite the low star
count.

## Triage note

Left at `discovery-log` for the P0/eval-runner lane.

_Triaged 2026-11-09 by the daily discovery-and-triage routine._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-skills-linter](https://github.com/shinytoyrobots/claude-skills-linter) | tool | Deterministic structural linter (MIT) catching broken refs, orphans, and cycles in Claude Code skills that LLMs silently tolerate | Skill files accumulate broken references, orphaned files, or dependency cycles that an LLM reviewing them won't reliably flag | skillfid, skilldiff, oil-skill-creator |
