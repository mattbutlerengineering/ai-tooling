# Evaluation: awesome-agent-skills (libukai)

**Repo:** [libukai/awesome-agent-skills](https://github.com/libukai/awesome-agent-skills)
**Stars:** 4,737 | **Last updated:** 2026-03-26 | **License:** none declared (README badge claims Apache-2.0)
**Dev loop stage:** Discover (outer loop)
**Layer:** Infrastructure

---

## What it does

A Chinese-language (简体中文-first, with English and Japanese README variants) curated guide to Agent Skills. Unlike most awesome-lists, it is structured as a *guide* rather than a flat link dump: it opens with a conceptual quickstart (what a Skill is, the standard `SKILL.md` folder layout), then walks through installing Skills across three distinct ecosystems — Claude-style apps, Claude Code-style IDE/CLI, and OpenClaw-style harnesses — each with its own CLI cheat sheet (`npx skills`, `npx clawhub`, Tencent's `skillhub`).

The curated content is deliberately small ("少而精" — few but fine). It covers official tutorials (Anthropic/Google design-pattern docs translated to Chinese), a table of ~30 first-party vendor skill repos (anthropics, openai, gemini, cloudflare, stripe, vercel, notion, etc.), and a hand-picked "精选技能" (selected skills) section grouped into coding, content creation, product control, and misc. It closes with a security-review section recommending SlowMist's agent-security auditing skill — a safety angle most awesome-lists omit.

## How we tested it

Source-grounded inspection only — we did not install or run anything. We pulled metadata and the full README via the GitHub API and read the curated sections directly.

```
gh api repos/libukai/awesome-agent-skills --jq '{desc,stars:.stargazers_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'
gh api repos/libukai/awesome-agent-skills/commits --jq '.[0].commit.committer.date'
gh api repos/libukai/awesome-agent-skills/readme --jq '.content' | base64 -d | head -260
```

## What worked

- **Genuinely distinctive: Chinese-language and China-ecosystem coverage.** This is the only Skills list in our catalog written for the Chinese-speaking developer. It surfaces tools the English lists never mention — Tencent's SkillHub store, WPS office-automation skills, NotebookLM control, WeChat-公众号 publishing skills — that are invisible to VoltAgent/travisvn/Composio.
- **Guide structure, not a link dump.** The install-by-ecosystem walkthrough (App vs Claude Code vs OpenClaw, each with CLI commands) is more useful for a newcomer than an alphabetized table.
- **Safety section is rare and welcome.** Explicitly warns about Skills running silent scripts/external API calls and points to a concrete auditing skill (SlowMist) plus an OpenClaw hardening guide.
- **Editorial restraint.** The "few but fine" principle keeps the curated list short and opinionated rather than exhaustive — each entry has a one-line Chinese annotation explaining what it is for.

## What didn't work or surprised us

- **Stale by ~3 months.** Last commit 2026-03-26. In a fast-moving Skills ecosystem that is several model releases and many new vendor repos behind; the first-party table will already be missing entrants.
- **No license file.** The README shows an Apache-2.0 badge but the repo has no `LICENSE` (`license: null` from the API). For a content list this is low-risk, but it is technically unlicensed.
- **Small scope and a sponsor banner.** The README leads with a Composio banner/affiliate link and the curated skill list is short — for breadth you still need the larger English lists.
- **Language barrier cuts both ways.** Excellent if you read Chinese; the English/Japanese mirrors exist but the primary curation energy is in the Chinese doc, and broken/duplicated URLs appear in a couple of entries (e.g. a `hhttps://` typo).

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Reference list — no direct effect on code quality |
| Speed | + | Ecosystem-by-ecosystem install guide gets a newcomer productive faster than a flat list |
| Maintainability | neutral | No impact on code |
| Safety | + | Dedicated security-review section pointing to a concrete Skill auditing tool — rare among these lists |
| Cost Efficiency | neutral | Small curated set; saves little scanning time over the larger lists |

## Verdict

**CONDITIONAL**

Adopt as a discovery source specifically for Chinese-language and China-ecosystem Skills coverage (SkillHub, WPS, WeChat publishing) — a niche no other list in the catalog fills, plus a safety angle the siblings lack. But it is stale (~3 months), small, sponsor-fronted, and unlicensed, so it is not a primary, always-current source the way the larger English lists aim to be. Use it as a complement to awesome-claude-skills (travisvn) / awesome-agent-skills (VoltAgent), not a replacement. Re-evaluate if updates resume.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [awesome-agent-skills (libukai)](https://github.com/libukai/awesome-agent-skills) | reference | Chinese-language guide to Agent Skills with install-by-ecosystem walkthroughs and a security section (4.7K stars) | Chinese-speaking devs lack a curated Skills guide covering China-specific stores (SkillHub, WPS) | awesome-agent-skills (VoltAgent), awesome-claude-skills (travisvn), awesome-claude-skills (Composio), buildwithclaude |
