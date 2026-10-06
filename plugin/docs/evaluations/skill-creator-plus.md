# Evaluation: skill-creator-plus

**Repo:** [robonuggets/skill-creator-plus](https://github.com/robonuggets/skill-creator-plus)
**Stars:** 32 | **Last updated:** 2026-10-05 (pushed) | **License:** MIT
**Last verified:** 2026-10-06
**Last triaged:** 2026-10-06  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A Claude skill that audits, builds, and improves other skills against Anthropic's own
skill-writing rules, including guidance that changed across Opus 5.5, Sonnet 5.5, and Fable 5,
per the repo description.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the GitHub
repository description, topics, and metadata. That is sufficient to compare it against the
already-adopted incumbent's stated job, not to judge its audit output hands-on.

## Verdict

**SKIP** — redundant with [`skill-creator`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator) (STACK, `MEASURED`, ADOPT). `skill-creator` is the first-party meta-skill for the exact job this lead advertises — draft → eval → benchmark → triggering-optimization → package, i.e. authoring and improving skills against Anthropic's own guidance. A one-day-old, 32-star third-party skill claiming the identical audit/improve job over the same guidance, with no stated differentiator beyond tracking recent model names, does not clear the bar for a second tool in the same slot.

## Triage note

P2 challenger — the row's `Overlaps with` cell names `skill-creator`, a STACK pick. Unlike the
Jeffallan/claude-skills precedent (which named concrete axes where it beat its incumbent on release
discipline and reference depth), this lead states no differentiator beyond "tracks what changed for
recent model names," which `skill-creator`'s own eval/benchmark loop already absorbs as models
change. SKIP is the defensible, reversible call here.

_Triaged 2026-10-06 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [skill-creator-plus](https://github.com/robonuggets/skill-creator-plus) | skill | Claude skill (MIT) that audits, builds, and improves other skills against Anthropic's own skill-writing rules, tracking per-model guidance (Opus 5.5/Sonnet 5.5/Fable 5) | Hand-authored skills drift from Anthropic's own skill-writing guidance as models change, with nothing auditing or upgrading them against it | skill-creator, SkillOpt, skillfid |
