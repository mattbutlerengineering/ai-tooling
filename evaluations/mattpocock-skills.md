# Evaluation: mattpocock/skills

**Repo:** [mattpocock/skills](https://github.com/mattpocock/skills)
**Stars:** 142,027 | **Last updated:** 2026-06-23 | **License:** MIT
**Last verified:** 2026-06-22
**Dev loop stage:** Implement
**Layer:** Process

---

## What it does

"Skills for Real Engineers. Straight from my .claude directory." — an installable Claude Code plugin of working engineering skills curated by Matt Pocock from his own daily-driver `.claude/` directory. Rather than a single mega-prompt, it ships a set of small, composable `SKILL.md` files that fire on natural-language triggers (the YAML `description` field) and hand off to each other: an `implement` orchestrator delegates to `tdd`, `codebase-design` supplies the shared vocabulary other skills reach for, `setup-matt-pocock-skills` scaffolds the per-repo config (issue tracker, triage labels, domain docs) the engineering skills assume, and `diagnosing-bugs` enforces a "build the feedback loop first" discipline before touching code.

Mechanically, each skill is a markdown file with frontmatter (`name`, `description`, optional `disable-model-invocation`) plus a body of process guidance. The model reads the descriptions, decides which skill is relevant to the current prompt, and pulls the body into context. Heavier detail lives in sibling files referenced by relative link (progressive disclosure) so the always-loaded surface stays small. Several of these skills are installed and active in this environment under `~/.claude/skills/`.

## How we tested it

**Evidence:** MEASURED

We verified the installed source on disk (not the README) and ran discriminating checks against the actual `SKILL.md` files: confirming claimed progressive-disclosure files exist, that triggering descriptions are well-formed, and that every skill respects a sane line budget. The canonical skill set was cross-checked against the live repo via `gh api`.

**1. Confirm the canonical skill set (live repo).** The repo organises skills under `skills/{engineering,productivity,misc,personal,deprecated,in-progress}/`:

```
$ gh api repos/mattpocock/skills/contents/skills/engineering --jq '.[]|select(.type=="dir").name'
ask-matt  codebase-design  diagnosing-bugs  domain-modeling  grill-with-docs
implement  improve-codebase-architecture  prototype  resolving-merge-conflicts
setup-matt-pocock-skills  tdd  to-issues  to-prd  triage          # 14 engineering
$ gh api repos/mattpocock/skills/contents/skills/productivity --jq '.[]|select(.type=="dir").name'
grill-me  grilling  handoff  teach  writing-great-skills           # 5 productivity
```

So ~19 active engineering+productivity skills (plus `misc/` and `personal/` helpers) — more than the catalog's "17 skills" one-liner, which is now slightly stale.

**2. Verify the locally-installed source.** Many of these skills are installed and active here. Inspecting `~/.claude/skills/`, all 18 active skills checked have an `SKILL.md`; line counts: `find-skills` 142, `diagnosing-bugs` 134, `codebase-design` 114, `tdd` 109, `triage` 103, `grill-with-docs` 88, `teach` 87, `to-issues`/`to-prd`/`domain-modeling` 74-83, down to thin orchestrators `implement` 15 / `handoff` 15. **0 of 18 exceed 500 lines** — the always-loaded surface is deliberately tiny.

**3. Discriminating check — does the SKILL.md's claimed behaviour match disk?** Two claims that a README-only review would miss, verified true:

- `codebase-design/SKILL.md` (114 lines) ends with a "Going deeper" section linking `DEEPENING.md` and `DESIGN-IT-TWICE.md`. Both files **exist on disk** (2559 B, 2712 B) — progressive disclosure is real, not aspirational.
- `diagnosing-bugs/SKILL.md` line 29 cites `scripts/hitl-loop.template.sh` as the "human-in-the-loop last resort" harness. That script **exists** (`~/.claude/skills/diagnosing-bugs/scripts/hitl-loop.template.sh`, 1164 B) — the skill ships the asset it references.

**4. Triggering descriptions are well-formed.** Each inspected skill uses the declarative "Use when …" pattern with concrete positive triggers, e.g.:

```yaml
# diagnosing-bugs
description: Diagnosis loop for hard bugs and performance regressions. Use when the
  user says "diagnose"/"debug this", or reports something broken/throwing/failing/slow.
# to-issues
description: Break a plan, spec, or PRD into independently-grabbable issues ... Use
  when user wants to convert a plan into issues, create implementation tickets ...
```

These are scoped (a verb + concrete trigger phrases) rather than vague — the main lever against the well-known skill *under*-triggering problem.

One member skill, **`resolving-merge-conflicts`, already has its own MEASURED A/B eval** in this repo (`evaluations/resolving-merge-conflicts.md`: baseline ships a semantically-broken-but-textually-clean merge 1/2, with-skill reaches 2/2). This eval covers the *collection's* structure and quality rather than re-running that case.

```
$ gh api repos/mattpocock/skills --jq '{stars,license:.license.spdx_id,desc}'
{"stars":142027,"license":"MIT","desc":"Skills for Real Engineers. Straight from my .claude directory."}
$ wc -l ~/.claude/skills/codebase-design/SKILL.md   #  114
$ ls ~/.claude/skills/codebase-design/              #  DEEPENING.md DESIGN-IT-TWICE.md SKILL.md
$ ls ~/.claude/skills/diagnosing-bugs/scripts/      #  hitl-loop.template.sh
```

## What worked

- **Progressive disclosure is genuine.** SKILL.md files stay small (all ≤142 lines, none near the 500-line ceiling) and offload depth to sibling files that actually exist — verified for `codebase-design` (DEEPENING.md/DESIGN-IT-TWICE.md) and the `diagnosing-bugs` HITL script.
- **Composable, not monolithic.** Thin orchestrators (`implement`, `handoff` at 15 lines) delegate to heavier skills (`tdd`, `codebase-design`), and `setup-matt-pocock-skills` wires per-repo config the others read. This repo itself adopted that pattern (its `docs/agents/` issue-tracker/triage/domain layout mirrors the setup skill's output).
- **Triggering descriptions are scoped and declarative**, listing concrete trigger phrases — reducing the under-trigger risk that plagues vague skills.
- **High-quality, opinionated vocabulary.** `codebase-design` defines a precise glossary (deep module, seam, adapter, leverage, locality) and even a "Rejected framings" section, which is exactly what gives multiple agents a consistent design language.

## What didn't work or surprised us

- **Catalog one-liner is stale on count.** The entry says "17 skills"; the live repo has ~19 active engineering+productivity skills plus misc/personal. Not wrong in spirit, but the number drifts as Matt edits his real `.claude/` dir (the repo updated the same day we verified).
- **Several skills assume the `setup-matt-pocock-skills` scaffold.** `triage`, `to-issues`, `diagnose`, `tdd` read `docs/agents/*` and `CONTEXT.md`; without running setup first they fall back to defaults or under-perform. The dependency is documented but easy to miss.
- **It's a moving target, not a versioned spec.** "Straight from my .claude directory" means skills can change or get deprecated (`deprecated/`, `in-progress/` dirs exist) without a release boundary — a maintainability cost for anyone pinning behaviour.
- We did not run a fresh triggering A/B across all 19 skills with `claude -p`; triggering quality is asserted from description structure plus the one already-measured member (`resolving-merge-conflicts`), not a full balanced should/shouldn't-fire prompt set.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | `diagnosing-bugs` enforces a tight pass/fail loop before code changes; `resolving-merge-conflicts` (member) measured 1/2→2/2 on a semantic-merge oracle. |
| Speed | neutral | Small SKILL.md surfaces load cheaply, but the skills add process discipline (TDD, diagnosis phases) that trades raw speed for fewer redo loops. |
| Maintainability | + | `codebase-design`/`domain-modeling` give a shared deep-module + ubiquitous-language vocabulary; ADR/CONTEXT discipline records decisions for future agents. |
| Safety | + | `implement` gates on typecheck + review before commit; `setup` confirms with the user before writing repo config. |
| Cost Efficiency | + | Progressive disclosure keeps always-loaded tokens small (≤142-line SKILL.md files); detail pulled only on demand. |

## Verdict

**ADOPT**

A genuinely well-engineered, composable skill collection from a practitioner's working setup — verified hands-on against the installed source, not the README. Progressive disclosure is real (referenced sibling files and scripts exist on disk), SKILL.md surfaces stay tiny (all ≤142 lines), triggering descriptions are scoped, and one member skill (`resolving-merge-conflicts`) is independently MEASURED at 1/2→2/2 on a semantic oracle. Run `setup-matt-pocock-skills` first so the issue-tracker/triage/domain-dependent skills have their context, and expect the set to drift (it tracks Matt's live `.claude/` dir). For most TypeScript/general engineering repos this is a strong default to install.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [mattpocock/skills](https://github.com/mattpocock/skills) | plugin | Skills for Real Engineers — installable plugin (~19 active skills) from a working dev's .claude directory | Need practical, composable, multi-agent skills from a working dev | agent-skills, ECC |
