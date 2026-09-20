# Evaluation: oh-my-fable

**Repo:** [Junhan2/oh-my-fable](https://github.com/Junhan2/oh-my-fable)
**Stars:** 50 | **Last updated:** 2026-09-03 (pushed) | **License:** MIT
**Last verified:** 2026-09-06
**Last triaged:** 2026-09-06  <!-- triaged: bulk -->
**Dev loop stage:** Skills & Plugins
**Layer:** Process

---

## What it does

A Claude Fable 5.1 prompting guide packaged as installable Claude Code skills (KO/EN/ZH). Codifies
Fable-generation prompting know-how the author says also improves output quality on Opus 5 and
Sonnet 5.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead and check whether the
band's structural reason holds, not to judge the skill's prompting guidance hands-on.

## Triage note

Left at `discovery-log`. This row is banded P2 challenger because its own "Overlaps with" cell
names `agent-skills`, `documentation-and-adrs`, and `mattpocock/skills` — but those are broad,
general-purpose engineering skill packs, and oh-my-fable is a narrow, model-specific prompting
guide for Fable 5.1 generation. It is not doing the same job as any of the three cited incumbents,
so `SKIP "redundant with <incumbent>"` would misstate the overlap as competition rather than the
loose "same category, different job" citation it actually is (overlap pressure on this row is 0 —
no other catalog row cites it back). A model-specific prompting skill is differentiated enough to
deserve a real eval rather than a mechanical redundancy SKIP; left for the P0/eval-runner lane.

_Triaged 2026-09-06 by the P2 challenger band._
