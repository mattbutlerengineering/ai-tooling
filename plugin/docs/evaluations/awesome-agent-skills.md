# Evaluation: awesome-agent-skills (VoltAgent)

**Repo:** [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills)
**Stars:** 25,784 | **Last updated:** 2026-06-18 | **License:** MIT
**Dev loop stage:** Discover (outer loop)
**Layer:** Infrastructure

---

## What it does

The largest curated collection of AI agent skills, with 1,120+ entries organized by publisher across 40+ official sections (Anthropic, Google, Stripe, Vercel, Cloudflare, Trail of Bits, Sentry, Expo, HashiCorp, etc.) plus community contributions. Each entry is a one-line link with short description. Compatible with Claude Code, Codex, Antigravity, Gemini CLI, Cursor, GitHub Copilot, OpenCode, Windsurf, and more.

The repo claims "hand-picked, not AI-slop generated" and enforces this via a quality gate in CONTRIBUTING.md: "don't submit skills you created 3 hours ago" — the focus is community-adopted skills from known teams. 583 entries link to officialskills.sh (VoltAgent's companion platform) rather than directly to GitHub, making VoltAgent's registry a significant distribution channel.

## How we tested it

Fetched the README via GitHub API and counted entries, sections, and link targets. Checked commit history for freshness and contributor activity. Compared organizational quality and coverage with awesome-claude-code (CONDITIONAL), antigravity-awesome-skills, and awesome-openclaw-skills from the catalog.

```bash
gh api repos/VoltAgent/awesome-agent-skills --jq '.description, .stargazers_count, .updated_at'
gh api repos/VoltAgent/awesome-agent-skills/readme --jq '.content' | base64 -d | grep -c '^\- \*\*\['
gh api 'repos/VoltAgent/awesome-agent-skills/commits?per_page=10' --jq '.[].commit | "\(.author.date[:10]) — \(.message | split("\n")[0])"'
```

## What worked

- **Organization by publisher is the right taxonomy.** Grouping by official team (Stripe, Supabase, HashiCorp, Trail of Bits, etc.) signals authority — you trust a skill from the platform vendor more than a random community submission. 40+ official sections cover a wide ecosystem.
- **Active community contributions.** 618+ merged PRs, multiple community PRs merged weekly, last commit 2 days ago. Far more contributor-driven than awesome-claude-code (which appears more single-maintainer).
- **Cross-editor compatibility.** Explicitly documents which editors support which skill formats, making this useful beyond Claude Code. Covers 9+ editors.
- **Quality standards documented.** Explicit criteria for descriptions, progressive disclosure, no absolute paths, scoped tools — sets a bar for submissions.
- **Scale.** 1,120+ entries is the largest skill catalog in the ecosystem. Even filtering to official-team skills yields ~300+ entries from major vendors.

## What didn't work or surprised us

- **No editorial commentary.** Unlike awesome-claude-code (which hand-writes 2-3 sentence reviews per entry), this list uses one-line descriptions that are often just the repo tagline. Discovery requires clicking through to each link — there's no "why should I care" signal.
- **VoltAgent platform promotion is heavy.** 583 of 1,120 entries (52%) link to officialskills.sh rather than directly to GitHub repos. The banner ads, sponsor placeholders, and ecosystem tools section make the commercial interest visible.
- **Community skills section is a quality grab-bag.** While official sections are well-curated, the community section accepts a wider range of quality. The "no 3-hour-old skills" gate helps, but doesn't enforce depth or substantive testing.
- **No per-entry metadata.** No star counts, install counts, activity indicators, or compatibility matrix per entry. awesome-claude-code tracks Active/Stale/Removed flags in a structured CSV — this list doesn't distinguish maintained from abandoned entries.
- **Flat README format.** All 1,120+ entries in one README means loading the full page is required for discovery. No search, no structured data export, no install-count ranking.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Discovery tool — doesn't directly affect code correctness |
| Speed | + | Fastest way to find official vendor skills for a specific technology |
| Maintainability | neutral | No direct impact on code maintainability |
| Safety | neutral | No security scanning or vetting of listed skills |
| Cost Efficiency | neutral | Free to use |

## Verdict

**CONDITIONAL**

Use as the primary discovery source when searching for official vendor skills — the publisher-organized taxonomy makes it the fastest way to find "does Stripe/Supabase/HashiCorp have an agent skill?" When the answer matters for a specific platform integration, start here. For general Claude Code ecosystem discovery with editorial guidance, awesome-claude-code (also CONDITIONAL) has better signal-to-noise per entry despite fewer total entries and staler updates.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | reference | 1000+ agent skills from official dev teams and community, cross-editor compatible | Need a comprehensive skills catalog across all major AI editors | awesome-claude-skills, antigravity-awesome-skills |
