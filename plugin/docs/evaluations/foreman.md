# Evaluation: Foreman

**Repo:** [Turki-Sh/Foreman](https://github.com/Turki-Sh/Foreman)
**Stars:** 15 | **Last updated:** 2026-08-11 (pushed) | **License:** MIT
**Last verified:** 2026-08-11
**Last triaged:** 2026-08-11  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Process

---

## What it does

A build playbook (MIT, Markdown-only, no scripts) shipped as a Claude Code plugin and Agent Skill that turns a coding agent into the foreman of a website build: interviews the user, forces design/scope decisions, locks a visual system, writes a build brief, then verifies, ships, and indexes the site.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata and README/topic description. Whether the interview-driven process actually produces better site builds than ad-hoc prompting is untested here.

## Verdict

**discovery-log — tentative read**

## Triage note

Newly discovered and catalogued today. Left at `discovery-log`, not SKIPped as redundant with `GSD` — Foreman is narrowly scoped to a single artifact type (website builds: design-system lock, build brief, ship, index) rather than GSD's general-purpose Discuss→Plan→Execute→Verify→Ship loop for arbitrary codebases. Worth a real look given the narrower, more concrete scope, but too early (15 stars, 1 day old) to weigh further today.

_Triaged 2026-08-11 by the daily discovery-and-triage pass._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Foreman](https://github.com/Turki-Sh/Foreman) | plugin | Build playbook (MIT) turning a coding agent into the foreman of a website build — interview, lock a visual system, brief, verify, ship, index | Ad-hoc site builds skip design/scope decisions and consistency checks; want an interviewed, gated build process | GSD, spec-kit, claude-code-spec-workflow |
