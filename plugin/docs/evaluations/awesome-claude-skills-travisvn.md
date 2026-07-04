# Evaluation: awesome-claude-skills (travisvn)

**Repo:** [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills)
**Stars:** 13,578 | **Last updated:** 2026-06-19 | **License:** none
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** N/A (reference)
**Layer:** N/A (reference)

---

## What it does

A curated awesome-list of Claude Skills, organized by Official (Anthropic) and Community categories, with supplementary educational content — tutorials, comparisons (Skills vs MCP, Skills vs System Prompts), security guidelines, FAQ, and troubleshooting. 83 linked entries across 45 sections. The README doubles as a beginner-friendly introduction to the Skills ecosystem.

## How we tested it

**Evidence:** REVIEW

Read the full README, counted entries, checked commit history and contributor count, assessed organization quality, and compared coverage against our catalog and competing awesome lists.

```bash
gh api repos/travisvn/awesome-claude-skills --jq '.stargazers_count, .updated_at'
gh api repos/travisvn/awesome-claude-skills/readme --jq '.content' | base64 -d | wc -l
gh api repos/travisvn/awesome-claude-skills/commits --jq '.[0:5] | .[] | .commit.committer.date'
```

## What worked

- **Educational framing** — the Skills vs MCP, Skills vs System Prompts comparison tables are the best concise explanation in any catalog. Useful for onboarding developers who don't yet understand the distinction.
- **Official skills coverage** — lists all 17 anthropics/skills entries with accurate descriptions, organized by domain (Document, Design, Development, Communication, Skill Creation).
- **Security section** — links the "Weaponizing Claude Code Skills" medium article and provides concrete vetting guidelines. Most awesome lists ignore security entirely.
- **Progressive disclosure explanation** — the three-tier loading model (~100 tokens → <5K tokens → resources) is clearly documented.

## What didn't work or surprised us

- **Stale** — last commit was April 28, 2026 (~2 months ago). The "Last Updated: Feb 2026" badge is even older than the actual content. Major skills collections released since (addyosmani/agent-skills 62.9K stars, everything-claude-code 217K stars) are absent.
- **Only 2 contributors** for a 13.5K-star repo — essentially a solo-maintained list. 535 open issues suggest unmerged PRs or unanswered questions are piling up.
- **Narrow community section** — only ~15 community skills listed (in a single flat table) despite 1,500+ installable skills existing across the ecosystem. awesome-agent-skills (25.8K stars, 1,120+ entries) and antigravity-awesome-skills (41K stars, 1,595 entries) dwarf the coverage.
- **No per-entry metadata** — no star counts, activity flags, install counts, or editorial commentary. Just name + one-line description.
- **No license** — unusual for an awesome list; most use CC0 or MIT.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Accurate descriptions but stale — recent ecosystem changes not reflected |
| Speed | + | Educational content helps newcomers get oriented faster than competing lists |
| Maintainability | neutral | No direct code impact |
| Safety | + | Security section with vetting guidelines is unique among awesome lists |
| Cost Efficiency | neutral | No direct impact |

## Verdict

**SKIP**

The educational content (Skills vs MCP comparisons, progressive disclosure explanation, security guidelines) is genuinely useful for beginners, but as a discovery tool it's superseded by awesome-agent-skills (25.8K stars, 1,120+ entries, active community), awesome-claude-code (46.8K stars, editorial commentary), and antigravity-awesome-skills (41K stars, installable bundles). With only 2 contributors, 535 open issues, and no commits since April 2026, the maintenance trajectory doesn't support reliance. The educational framing could be extracted into a standalone guide rather than depending on this list staying current.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [awesome-claude-skills (travisvn)](https://github.com/travisvn/awesome-claude-skills) | reference | Curated Claude Skills and customization tools | Need a catalog of available skills to evaluate | awesome-claude-code, awesome-claude-skills (Composio) |
