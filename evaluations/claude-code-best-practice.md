# Evaluation: claude-code-best-practice

**Repo:** [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice)
**Stars:** 58,305 | **Last updated:** 2026-06-19 | **License:** MIT
**Dev loop stage:** All (reference)
**Layer:** Process

---

## What it does

A comprehensive, continuously-updated reference repository covering every Claude Code feature with three layers per concept: a "Best Practice" guide (how to use it well), an "Implementation" file (working example from the repo itself), and primary source links to official docs. The README serves as a navigable index with 600 files covering concepts (subagents, commands, skills, hooks, MCP, settings, memory, workflows), development workflow comparisons (12 major frameworks mapped with their skill/agent/command counts), cross-model workflows, skill/agent collections, and 83 curated tips from Boris Cherny, Thariq, Karpathy, and community practitioners.

## How we tested it

**Evidence:** REVIEW

Read the full README (30.5KB), sampled the `best-practice/claude-subagents.md` file for quality, and analyzed the repo structure (600 files across best-practice/, implementation/, reports/, tips/, orchestration-workflow/, changelog/).

```
gh api repos/shanraisshan/claude-code-best-practice --jq '.description, .stargazers_count, .updated_at, .license.spdx_id'
gh api repos/shanraisshan/claude-code-best-practice/contents/best-practice/claude-subagents.md --jq '.content' | base64 -d
gh api "repos/shanraisshan/claude-code-best-practice/git/trees/main?recursive=1" --jq '.tree | length'
```

## What worked

- **Three-layer documentation pattern**: each concept has a "Best Practice" (how), "Implemented" (example), and official docs link (source) — the most systematic coverage of Claude Code features in the ecosystem
- **Development workflow comparison table**: maps 12 major frameworks (Superpowers, ECC, Matt Pocock, Spec Kit, gstack, GSD, agent-skills, OpenSpec, BMAD-METHOD, oh-my-claudecode, Compound Engineering, HumanLayer) with their skill/agent/command counts and workflow stage diagrams — uniquely valuable for choosing between frameworks
- **Subagents best practice** is exceptionally detailed: all 16 frontmatter fields documented with types, defaults, and descriptions, plus the 5 official built-in agent types — more complete than the official docs
- **Cross-model workflows section**: documents how to bridge Claude Code with Codex, Gemini, GPT via plugins, MCP, and routers — a niche no other reference covers
- **83 curated tips** organized by category (prompting, planning, context, session, CLAUDE.md, agents, commands, skills, hooks, workflows, git, debugging, utilities, daily) with attribution to original sources
- **Updated same-day as Claude Code releases**: the version badge (v2.1.183, Jun 19 2026) shows real-time tracking

## What didn't work or surprised us

- **No installable component**: purely a reading resource — no skill, plugin, or CLI to integrate into your workflow
- **Heavy visual presentation**: SVG badges, animated GIFs, and emoji headers make GitHub rendering slow and distract from content on mobile
- **No SKILL.md or CLAUDE.md export**: the best practices aren't extractable as agent-consumable context — you read them yourself and apply manually
- **Star count partially reflects GitHub Trending virality** (#1 trending) rather than sustained daily utility — the repo is best visited when learning a new feature, not daily

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Subagent frontmatter documentation is more complete than official docs; version-tracked against Claude Code releases |
| Speed | + | Development workflow comparison table saves hours of research when choosing between frameworks |
| Maintainability | neutral | Reference only — doesn't affect code quality directly |
| Safety | neutral | No executable components |
| Cost Efficiency | neutral | No token impact |

## Verdict

**CONDITIONAL**

Use as the primary reference when learning a new Claude Code feature (subagents, hooks, skills, MCP, settings) or when comparing development workflow frameworks. The three-layer pattern (best practice + implementation + source) and the 12-framework comparison table are uniquely valuable — no other catalog entry covers this breadth. Skip for daily use — once you've internalized a concept, the official docs are faster for lookups. The lack of an installable component means this competes with bookmarks, not tools.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) | reference | From vibe coding to agentic engineering — comprehensive best practices with workflow framework comparisons (58K stars) | Want proven patterns for getting the most out of Claude Code | claude-howto, claude-code-tips |
