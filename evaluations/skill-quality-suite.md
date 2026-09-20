# Evaluation: skill-quality-suite

**Repo:** [letsloose501/skill-quality-suite](https://github.com/letsloose501/skill-quality-suite)
**Stars:** 2 | **Last updated:** 2026-09-19 (pushed) | **License:** MIT
**Last verified:** 2026-09-20
**Last triaged:** 2026-09-20  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A lint, secret-scan, and prompt-injection-scan toolkit that also validates SKILL.md
portability across Claude Code, Codex, Cursor, and Gemini CLI.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell (SkillSpector, skill-scanner,
skilldoctor). That is sufficient to place the lead and note `SkillSpector` is the one
named STACK incumbent, not to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: SkillSpector is a security scanner alone, and skill-quality-suite
bundles lint + security + cross-harness portability checking in one toolkit — a broader
scope than the incumbent, so a redundancy call would be premature. Also very new (2 stars,
3 days old); worth a first-time look before any disposition stronger than "watch." Left
for the P0/eval-runner lane.

_Triaged 2026-09-20 by today's discovery lead._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [skill-quality-suite](https://github.com/letsloose501/skill-quality-suite) | tool | Lint, secret-scan, and prompt-injection-scan toolkit validating SKILL.md portability across Claude Code, Codex, Cursor, and Gemini CLI | Skills ship with no combined quality/security lint or cross-harness compatibility check before install | SkillSpector, skill-scanner, skilldoctor |
