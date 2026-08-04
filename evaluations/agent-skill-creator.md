# Evaluation: agent-skill-creator

**Repo:** [francyjglisboa/agent-skill-creator](https://github.com/francyjglisboa/agent-skill-creator)
**Stars:** 2,135 | **Last updated:** 2026-07-22 (pushed) | **License:** MIT
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Reflect (skill authoring)
**Layer:** Tooling

---

## What it does

Turns a described workflow into one `SKILL.md` and installs it across 17 agent platforms — Claude
Code, Copilot, Cursor, Windsurf, Codex, Gemini, Kiro and others. Two jobs in one skill: author the
skill, then fan it out to every agent you run.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. This evaluation is source-grounded only: GitHub metadata plus
the CATALOG one-liner and "Overlaps with" cell (`skill-creator`, `SkillOpt`, `plugin-dev`). That is
sufficient for a SKIP that turns on *redundancy with catalogued incumbents* — a question the
overlap answers directly — and not sufficient for a positive verdict, which this eval does not
offer.

## Verdict

**SKIP** — redundant with
[`skill-creator`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator)
(STACK) on authoring and with `openskills`/`capa` on cross-platform install. Both halves of what it
does are already covered, and it is the weaker copy of each.

`skill-creator` is the first-party authoring toolkit and, uniquely, ships the eval/trigger-accuracy
harness that decides whether a skill actually fires — the thing this repo's own #38 backlog says
skill quality turns on. A third-party generator that emits `SKILL.md` without that measurement loop
is the part of the job that was never the hard part.

The 17-platform install fan-out is real, but it is `openskills`' entire premise and `capa`'s too;
both are catalogued and both do only that, which is the better factoring. Bundling authoring with
distribution means you take a weaker author to get a distributor you can have standalone.

Re-open if it grows a trigger-accuracy eval loop that `skill-creator` lacks.

_Triaged 2026-08-04 by the P2 challenger band ([#263](https://github.com/mattbutlerengineering/ai-tooling/issues/263))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agent-skill-creator](https://github.com/francyjglisboa/agent-skill-creator) | skill | Turn any workflow into one SKILL.md that installs across 17 agent platforms | Authoring a skill once and getting it into every agent you run, without hand-porting | skill-creator, SkillOpt, plugin-dev |
