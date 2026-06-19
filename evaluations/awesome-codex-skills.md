# Evaluation: awesome-codex-skills

**Repo:** [ComposioHQ/awesome-codex-skills](https://github.com/ComposioHQ/awesome-codex-skills)
**Stars:** 13,932 | **Created:** 2026-01-12 | **Last updated:** 2026-05-15 | **License:** none (no LICENSE file)
**Dev loop stage:** Discover (outer loop)
**Layer:** Infrastructure

---

## What it does

A curated awesome-list of practical **Codex** skills — instruction bundles for OpenAI's Codex CLI/API, packaged as folders each containing a `SKILL.md` (name + description frontmatter, then step-by-step body). Codex reads the metadata to decide when to trigger a skill and loads the body only after it fires, keeping context lean — the same progressive-disclosure model as Claude skills.

Roughly 69 link entries are organized into five categories — Development & Code Tools, Productivity & Collaboration, Communication & Writing, Data & Analysis, Meta & Utilities. Entries split between **in-repo skills** (`./codebase-migrate/`, `./gh-fix-ci/`, `./connect/`, `./paperjsx/`, …) hosted by Composio directly, and **external links** to third-party repos. A `skill-installer` Python script (`install-skill-from-github.py`) fetches any skill into `$CODEX_HOME/skills/` (default `~/.codex/skills/`); each external entry carries its own copy-paste install command. The list is run by Composio (a commercial app-connection platform) and threads its product — `connect/`, `connect-apps/`, the Composio CLI — through the productivity entries.

## How we tested it

Reference-list evaluation, modeled on `evaluations/awesome-claude-code.md`. We fetched metadata, read the README, counted entries, and checked freshness via the latest commit date. We did not install Codex or run any skill.

```
gh api repos/ComposioHQ/awesome-codex-skills --jq '{desc,stars:.stargazers_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'
# => {desc:null, stars:13932, created:2026-01-12, pushed:2026-05-15, license:null}
gh api repos/ComposioHQ/awesome-codex-skills/commits --jq '.[0].commit.committer.date'
# => 2026-05-15T06:24:46Z  (last content commit ~5 weeks stale as of eval)
gh api repos/ComposioHQ/awesome-codex-skills/readme --jq '.content' | base64 -d | grep -cE '^- \['
# => 69 link entries
```

We did not verify that linked repos are live, correctly licensed, or that install commands succeed.

## What worked

- **The only Codex-scoped list in our catalog.** Every other awesome-list we track (awesome-claude-skills ×2, awesome-agent-skills, awesome-openclaw-skills, antigravity-awesome-skills) is Claude- or cross-editor-scoped. This fills a genuine gap: skills written/tested specifically against the Codex CLI's trigger model and `$CODEX_HOME` layout.
- **One-click install per entry.** Most external entries ship a ready-to-paste `install-skill-from-github.py` command with `--repo`/`--path`/`--name`. Discovery and install are a single copy.
- **Sensible five-category taxonomy** with descriptive one-liners — easy to scan, and the descriptions are written, not scraped taglines (e.g. brooks-lint's "AI code reviews grounded in six classic engineering books").
- **Mix of first-party and community skills.** Composio maintains a solid in-repo core (mcp-builder, deploy-pipeline, sentry-triage, gh-fix-ci, paperjsx) alongside curated external links, so it is both a usable skill source and a discovery index.
- **High visibility.** ~14K stars in five months signals the Codex-skills ecosystem is real and this is its default landing page.

## What didn't work or surprised us

- **No LICENSE file** (`license: null`). For a list whose own `./skills/` folders you are meant to copy into your environment, the absence of an explicit license is a real adoption caveat — vendor-in at your own risk and check each external repo's license individually.
- **~5 weeks stale at eval time.** Last content commit 2026-05-15; for a fast-moving ecosystem that is borderline, though far fresher than awesome-claude-code's 2-month freeze. Worth re-checking before relying on it as "current."
- **Commercial-vendor editorial bias.** Composio runs the list and seeds it with its own product (`connect`, `connect-apps`, Composio CLI). The curation is useful but not neutral — productivity/collaboration entries skew toward "do this with Composio."
- **No description set** (`desc: null`) and no activity/staleness flags on entries — unlike awesome-claude-code's CSV with Active/Stale/Removed columns, this is a plain markdown list, so dead links will accrue silently.
- **Variable entry quality.** Several external entries read as self-promotional ("46 modes, 23 sub-agents, ~55% token savings", "340+ skills") with claims we did not verify. Treat the more grandiose taglines as marketing.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Reference list — does not touch code quality directly |
| Speed | + | Per-entry one-click install and a scannable taxonomy cut Codex-skill discovery from hours to minutes |
| Maintainability | neutral | No effect on code; no activity flags so link rot is on the reader |
| Safety | − | No repo license + vendor bias + unverified third-party install commands; treat copied skills as untrusted code |
| Cost Efficiency | + | Progressive-disclosure skills keep Codex context lean; free to browse |

## Verdict

**CONDITIONAL**

The single best entry point for Codex-specific skills, and the only Codex-scoped list in the catalog — that scope is its whole justification. Use it as a Discover-stage source when working in the Codex CLI, especially the Composio-maintained in-repo skills (mcp-builder, deploy-pipeline, gh-fix-ci). Versus its neighbors: **awesome-claude-skills** (Composio's own Claude analogue) and **awesome-agent-skills** (VoltAgent, cross-editor) are broader but Claude/multi-editor-first; this is the place to look when you specifically need the Codex trigger model and `$CODEX_HOME` layout. It misses ADOPT for two reasons: no repository license (vendor-in at your own legal risk) and a ~5-week content freeze with no staleness tracking. It also lacks the hand-written, opinionated review depth and the activity-tracking CSV that make awesome-claude-code the gold standard among lists. Re-evaluate if a license lands and updates resume; until then, trust the curation but verify each linked repo's license and freshness yourself.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [awesome-codex-skills](https://github.com/ComposioHQ/awesome-codex-skills) | reference | Curated ~69 Codex CLI/API skills in 5 categories with per-entry installers (13.9K stars, Composio-run, no license) | Need a Codex-scoped catalog of skills to discover and install | awesome-claude-skills (Composio), awesome-agent-skills, antigravity-awesome-skills |
