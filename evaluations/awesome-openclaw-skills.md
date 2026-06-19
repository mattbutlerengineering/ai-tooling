# Evaluation: awesome-openclaw-skills

**Repo:** [VoltAgent/awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills)
**Stars:** 50,368 | **Last updated:** 2026-06-16 | **License:** MIT
**Dev loop stage:** N/A (discovery reference)
**Layer:** N/A

---

## What it does

The largest curated skill catalog in the ecosystem: 5,198 skills across 30 categories, filtered from 12,400+ in the OpenClaw registry (ClawHub). Categories span coding agents (1,184), web development (920), DevOps/cloud (393), search/research (345), browser automation (323), and 25 more domains. Each entry links to its ClawHub page and includes a one-line description. Skills are installable via `openclaw skills install <slug>` or `npx clawhub install <slug>`.

The filtering is substantive — 7,215 entries excluded for spam (4,065), duplicates (1,040), low-quality (851), crypto/finance (886), and malicious content (373). VirusTotal partnership provides per-skill security scanning on ClawHub pages.

## How we tested it

Inspected the README structure, category organization, filtering methodology, and community engagement via GitHub API. Compared entry counts, curation depth, and update frequency against the other skill catalogs in the ai-tooling catalog.

```
gh api repos/VoltAgent/awesome-openclaw-skills --jq '.stargazers_count, .updated_at, .open_issues_count, .forks_count'
gh api repos/VoltAgent/awesome-openclaw-skills/readme --jq '.content' | base64 -d | grep -c '^\- \['
gh api repos/VoltAgent/awesome-openclaw-skills/commits --jq '.[0:3] | .[] | .commit.committer.date'
```

797 entries visible in the main README with "View all N skills" links to 30 category files containing the full 5,198. Repo has 4,904 forks, 18 open issues, 16 open PRs, last commit June 16 2026.

## What worked

- **Rigorous filtering**: 7,215/12,413 entries excluded with documented rationale (spam, dupes, malicious, crypto). The 373 malicious skills removed by security audit is a unique safety feature no other catalog offers
- **Scale**: 5,198 skills across 30 categories is 3-5× larger than any other skill catalog (antigravity has 1,595, awesome-agent-skills has 1,120)
- **Category depth**: "Coding Agents & IDEs" alone has 1,184 entries — more than entire competing catalogs
- **VirusTotal integration**: per-skill security scanning via ClawHub partnership adds a safety layer absent from GitHub-only catalogs
- **Community**: 50K stars, 4,900 forks, active PR flow indicates sustained community engagement

## What didn't work or surprised us

- **OpenClaw-centric**: all entries link to ClawHub (`clawskills.sh`), not GitHub. Many skills are OpenClaw-native and may not have a SKILL.md portable to Claude Code/Codex
- **No editorial commentary**: entries are name + one-liner, no ratings, no "recommended" flags, no quality tiers. Compare with awesome-claude-code's hand-written review paragraphs
- **No per-entry metadata**: no star counts, no activity flags, no install counts. Discovering which of 1,184 coding skills is actually good requires trying them
- **VoltAgent/Composio promotion**: ecosystem tools section is sponsor-heavy (Composio, MyClaw, SerpApi, trentclaw, LaunchKit) — typical for large awesome lists but dilutes signal
- **Portability uncertain**: skills published to ClawHub are in SKILL.md format (portable in theory), but the install flow (`openclaw skills install`) targets OpenClaw specifically

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Discovery tool — doesn't directly affect code quality |
| Speed | + | Largest catalog for finding skills by domain; 30 categories make narrowing fast |
| Maintainability | neutral | No direct impact |
| Safety | + | 373 malicious skills removed + VirusTotal integration is a unique safety signal |
| Cost Efficiency | neutral | Free discovery resource |

## Verdict

**CONDITIONAL**

Use for broad skill discovery across domains — especially non-engineering categories (transportation, health, smart home, media) where no other catalog has coverage. The malicious-skill filtering and VirusTotal partnership make it the safest large catalog. For Claude Code-specific engineering skills, prefer awesome-agent-skills (CONDITIONAL, editorial by publisher) or antigravity-awesome-skills (CONDITIONAL, installable bundles with CLI). The OpenClaw-native install flow limits direct utility for Claude Code users.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills) | reference | 5,400+ skills filtered and categorized from the official OpenClaw Skills Registry | Need the broadest possible skills discovery across the ecosystem | awesome-agent-skills, antigravity-awesome-skills |
