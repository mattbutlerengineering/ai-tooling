# Evaluation: awesome-claude-code

**Repo:** [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)
**Stars:** 46,792 | **Last updated:** 2026-06-18 | **License:** NOASSERTION
**Dev loop stage:** Discover (outer loop)
**Layer:** Infrastructure

---

## What it does

A curated catalog of 226 Claude Code resources — skills, hooks, slash-commands, agent orchestrators, developer tooling, CLAUDE.md files, status lines, output styles, and alternative clients. The data lives in a structured CSV (`THE_RESOURCES_TABLE.csv`) with 20 columns per entry: display name, category, sub-category, primary/secondary links, author, license, description, activity flags (Active, Stale, Removed From Origin), and release metadata. Pre-rendered README variants in `README_ALTERNATIVES/` provide 48 different views: by category, sorted by name/creation-date/latest-release/last-updated.

The editorial voice is distinctive — each entry gets a hand-written review paragraph (not repo-scraped descriptions), often 2-3 sentences explaining *why* the tool is good, what makes it unique, or calling out specific standout features. This is unusual for awesome lists, which typically copy the repo tagline.

## How we tested it

**Evidence:** REVIEW

Fetched the CSV and README via GitHub API, counted entries by category, checked commit history for freshness, compared entry overlap with our catalog, and assessed editorial quality of descriptions.

```
gh api repos/hesreallyhim/awesome-claude-code --jq '.description, .stargazers_count, .updated_at'
gh api repos/hesreallyhim/awesome-claude-code/contents/THE_RESOURCES_TABLE.csv --jq '.content' | base64 -d | wc -l
gh api repos/hesreallyhim/awesome-claude-code/contents/THE_RESOURCES_TABLE.csv --jq '.content' | base64 -d | cut -d',' -f3 | sort | uniq -c | sort -rn
```

## What worked

- **Editorial quality is unusually high.** Every entry has a human-written review — not just the repo tagline. Descriptions are opinionated and evaluative ("really one of the best skills repos on GitHub", "well-organized, easy to read"), giving genuine signal about quality.
- **Structured CSV with rich metadata.** 20 columns including `Active`, `Stale`, `Removed From Origin`, license detection, release version tracking — this is a living database, not a markdown list.
- **48 pre-rendered views.** Category-specific flat lists sorted by name, creation date, release date, and last-updated. Makes discovery trivially easy from multiple angles.
- **Activity tracking.** 207/226 entries marked active, with stale/removed flags maintained. This is rare — most awesome lists accumulate dead links forever.
- **Coverage of categories our catalog doesn't track.** 59 slash-commands, 28 CLAUDE.md files, 13 hooks, 7 status lines, 4 output styles — these are Claude Code-specific categories that a generic AI tooling catalog wouldn't cover well.

## What didn't work or surprised us

- **Main README is gutted.** As of April 2026, the README just says "TODO" — a reorganization is in progress. The actual content lives in `THE_RESOURCES_TABLE.csv` and `README_ALTERNATIVES/`, which a visitor would only find by browsing the repo tree.
- **Last meaningful commit was April 27, 2026.** The daily SVG ticker updates inflate the "last updated" date, but no new entries have been added in ~2 months. For a fast-moving ecosystem, 2 months of stale data means dozens of significant new tools are missing.
- **Low overlap with our catalog by name (5/226).** Many entries exist under different names or are too small/niche for our catalog's scope. The CSV's tooling and slash-command categories cover a different granularity than our catalog's tool/skill/plugin taxonomy.
- **CSV parsing is fragile.** Descriptions contain embedded commas and newlines, making `cut`-based analysis unreliable. The data is well-structured but needs a proper CSV parser.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Reference list — doesn't affect code quality directly |
| Speed | + | High-quality editorial reviews save hours of repo-by-repo evaluation when scanning for tools |
| Maintainability | neutral | No impact on code |
| Safety | + | Activity tracking flags dead/stale repos; license detection catches unlicensed tools |
| Cost Efficiency | + | 48 pre-rendered views eliminate manual sorting; CSV structure enables programmatic querying |

## Verdict

**CONDITIONAL**

Use as a discovery source when scanning for Claude Code-specific resources, especially slash-commands, hooks, CLAUDE.md patterns, and status lines — categories our catalog doesn't deeply cover. The editorial quality is the highest of any awesome list in the catalog, and the structured CSV is uniquely useful for programmatic querying. However, the 2-month content freeze and gutted README drop it from ADOPT — it's not the live, always-current source it was. Re-evaluate if the reorganization completes and regular updates resume.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | reference | Curated skills, hooks, slash-commands, and agent orchestrators for Claude Code (46.8K stars) | Hard to discover what's available in the Claude Code ecosystem | awesome-claude-skills (travisvn), awesome-claude-skills (Composio) |
