# Evaluation: kubai-icons

**Repo:** [kubai087/kubai-icons](https://github.com/kubai087/kubai-icons)
**Stars:** 489 | **Last updated:** 2026-11-09 (pushed) | **License:** NOASSERTION (mixed — see below)
**Last verified:** 2026-11-09
**Last triaged:** 2026-11-09  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Process

---

## What it does

An agent skill that draws animated icons in one consistent style for Claude Code, Codex,
and other coding agents, bundled with 2,800+ open-source icons for React, Vue, plain
JS/web components, and static SVG.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: GitHub
reports the repo's license as `NOASSERTION` (no single detectable root LICENSE), so we
read the repo's own README license table directly. It splits licensing per component:

- The icon assets (`icons/`, `badges/`, and the four generated packages) are **MIT**.
- **The skill itself** (`SKILL.md`/`PROMPT.md` — the artifact this catalog entry is
  about) is under a custom "Kubai Icons License": source-available, but it explicitly
  forbids distributing a *modified or translated version* of the skill, selling it, or
  presenting it under another name — i.e. not a permissive OSS license.
- The website (`site/`, `tools/`, `tests/`, `docs/`) is All Rights Reserved.

That is sufficient to apply this repo's license bar; it is not sufficient to support an
ADOPT, and this eval offers none.

## Verdict

**SKIP** — no permissive license on the vendored artifact. The entry is of Type `skill`,
which is copied (vendored) into the consuming repo's own skill directory — exactly the
case this routine's license bar exists for. While the bundled icon *assets* are MIT, the
*skill* a user would actually vendor is licensed under a bespoke source-available license
that disallows redistributing a modified copy, which fails the "only permissive MIT-like
OSS is adoptable" bar regardless of star count (489).

_Triaged 2026-11-09 by the daily discovery-and-triage routine — license bar (vendored
skill under a non-permissive, source-available license; GitHub reports NOASSERTION at
the repo root)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [kubai-icons](https://github.com/kubai087/kubai-icons) | skill | Skill (⚠️ no license) drawing animated icons in one consistent style for coding agents, with 2,600+ open-source icons for React/Vue/SVG | Agent-built UIs need a consistent icon set, but hand-sourcing or one-off generating icons breaks visual consistency | ui-ux-pro-max, flawless-ui-ux, oa-design |
