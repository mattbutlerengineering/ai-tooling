# Evaluation: open-skill-sunset

**Repo:** [ooocooc/open-skill-sunset](https://github.com/ooocooc/open-skill-sunset)
**Stars:** 84 | **Last updated:** 2026-08-30 (pushed) | **License:** MIT
**Last verified:** 2026-08-30
**Last triaged:** 2026-08-30  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

A local, read-only audit CLI (npm: `skill-sunset`) for stale `AGENTS.md`, `CLAUDE.md`, and generic `SKILL.md` instructions — flags dead references and drift without writing anything back.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell (`claude-md-doctor`, `reporails/cli`, `agnix`). It would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log` — a first-time lead with no overlap pressure yet. `claude-md-doctor` already covers a similar checkup (size vitals, dead references, drifted claims, rule backtesting) and is the closer read-only auditor of the two; whether this tool's narrower "read-only, staleness only" scope is differentiated enough to be worth a second eval, or is redundant with `claude-md-doctor`, needs a real comparison rather than a mechanical guess.

_Triaged 2026-08-30 by the P3 backlog band ([#567](https://github.com/mattbutlerengineering/ai-tooling/issues/567))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [open-skill-sunset](https://github.com/ooocooc/open-skill-sunset) | tool | Local, read-only audit (MIT) for stale AGENTS.md, CLAUDE.md, and generic SKILL.md instructions | Instruction files accumulate stale references and dead guidance with nothing flagging which lines rotted | claude-md-doctor, reporails/cli, agnix |
