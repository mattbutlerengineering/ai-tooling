# Evaluation: skillfid

**Repo:** [waldekmastykarz/skillfid](https://github.com/waldekmastykarz/skillfid)
**Stars:** 1 | **Last updated:** 2026-09-07 (pushed) | **License:** MIT
**Last verified:** 2026-09-07
**Last triaged:** 2026-09-07  <!-- triaged: bulk -->
**Dev loop stage:** Skills & Plugins
**Layer:** Tooling

---

## What it does

A CLI that evaluates how faithfully an agent skill's actual execution follows its own SKILL.md source documentation.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual behavior —
it would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped as redundant with `skill-creator` despite the overlap citation. `skill-creator` is an authoring meta-skill (draft → eval → package a *new* skill); skillfid instead audits an *existing* skill's execution against its own docs for drift — a verification job, not an authoring one. Different job in the skill lifecycle, so no incumbent dominates it. 1★, hours old — a genuinely fresh idea worth a real look rather than a same-day disposal.

_Triaged 2026-09-07 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [skillfid](https://github.com/waldekmastykarz/skillfid) | tool | CLI (MIT) evaluating how faithfully an agent skill's execution follows its own SKILL.md source documentation | A skill can silently drift from what its documentation promises with nothing checking the two still agree | skill-creator, SkillOpt, oil-skill-creator |
