# Evaluation: Antigravity Awesome Skills

**Repo:** [sickn33/antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills)
**Stars:** 41,059 | **Last updated:** 2026-06-18 | **License:** MIT
**Dev loop stage:** All (reference + installable catalog)
**Layer:** Tooling

---

## What it does

An installable library of 1,595 SKILL.md files covering development, testing, security, infrastructure, product, and marketing — with an npm CLI installer, 51 specialized plugin bundles, role-based bundles, and ordered workflow playbooks. Skills are sourced from ~20 official vendors (Anthropic, Apify, Expo, Hugging Face, Microsoft, Supabase, etc.) and community contributors, with provenance tracked in a full attribution ledger. The installer supports 10+ agent runtimes: Claude Code, Codex CLI, Cursor, Gemini CLI, Kiro, OpenCode, and more.

The distinguishing feature versus other awesome lists is that this is *installable*, not just browsable. `npx antigravity-awesome-skills --claude` places skills where Claude Code expects them. Specialized plugin bundles (AAS Web App Builder, AAS Security Engineer, AAS DevOps & Cloud, etc.) let users install domain-focused subsets of 8–10 skills rather than the full 1,595.

## How we tested it

**Evidence:** REVIEW

Checked repo metadata, read the full README (529 lines), examined the repo structure (14 top-level directories, 2,237 skill directories, 1,595 SKILL.md files), and spot-checked skill quality across different sources.

```bash
gh api repos/sickn33/antigravity-awesome-skills --jq '.stargazers_count, .updated_at'
# 41059, 2026-06-18

gh api "repos/sickn33/antigravity-awesome-skills/git/trees/main?recursive=1" \
  --jq '[.tree[] | select(.path | endswith("SKILL.md"))] | length'
# 1595
```

Spot-checked three skills for quality:

1. **brainstorming** (237 lines) — structured design facilitation skill with operating mode, multi-phase process (understand context → understand idea → brainstorm solutions → compare and select → produce output), and explicit prohibition on implementation during active brainstorming. Substantive and well-written.

2. **apify-actor-development** — official Apify skill with concrete setup steps, Docker Actor model explanation, input schema patterns, deployment workflow. Genuine practitioner-level content, not a summary.

3. **CATALOG.md** — generated registry with 1,595 entries organized into categories (architecture: 101, security: ~80, etc.) with tags and trigger keywords per skill.

Also checked the 51 specialized plugin bundles — they're real Claude Code/Codex plugins (plugin.json manifests, skills/ directories) packaged for marketplace distribution.

## What worked

- **Installable, not just browsable**: `npx antigravity-awesome-skills --claude` is a genuine npm installer that places skills in the right directory per runtime — the only catalog in this class that does this
- **Scale with curation layers**: 1,595 skills is massive, but the specialized plugin bundles (8–10 skills each) and role-based bundles provide curated entry points so users don't drown in the full catalog
- **Official vendor sourcing**: ~20 official skill repositories (Anthropic, Microsoft, Google, Supabase, Expo, Hugging Face, Apify, etc.) with attribution ledger — not anonymous aggregation
- **Cross-runtime support**: 10+ agent runtimes with per-runtime install flags and documented paths — the broadest multi-editor support of any skills catalog
- **Active maintenance**: v12.8.0 released 2026-06-17, daily star-chart updates, 41K stars indicate strong community traction

## What didn't work or surprised us

- **Bulk quantity includes padding**: many skills in the 1,595 are platform-specific vendor content (30+ Apify skills, 20+ Hugging Face skills) that most users won't need — the high count is partly vendor catalog aggregation
- **No per-skill quality ratings**: unlike awesome-claude-code (which has editorial commentary per entry), there's no signal for which of the 1,595 are high-quality vs filler
- **Full install is heavy**: installing all 1,595 skills floods the agent's skill discovery with noise — the specialized bundles are the right entry point, but the README leads with the full install
- **Skill provenance can be unclear**: some community skills lack clear authorship in the SKILL.md frontmatter (only `source: community`), though the central attribution ledger documents sources

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Official vendor skills (Apify, Supabase, Expo) provide accurate, current platform guidance |
| Speed | + | One-command installer for any runtime; specialized bundles skip the discovery step entirely |
| Maintainability | neutral | Skills themselves don't affect code maintainability; the catalog is well-maintained |
| Safety | neutral | No security scanning of skill content (unlike SkillSpector or hol-guard) |
| Cost Efficiency | neutral | Skill discovery saves time, but bulk install wastes context tokens if too many load |

## Verdict

**CONDITIONAL**

Use when you need broad skill coverage across multiple domains or runtimes — the specialized plugin bundles (AAS Web App Builder, AAS Security Engineer, etc.) are the right entry point, not the full 1,595-skill install. For focused Claude Code work, curated collections like mattpocock/skills (ADOPT) or trailofbits/skills (ADOPT) offer higher signal-to-noise. Antigravity wins on breadth, cross-runtime support, and installable packaging — it's the best choice when onboarding a team that uses mixed editors.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills) | reference | 1,595 installable agentic skills with npm CLI, 51 plugin bundles, and 10+ runtime support (41K stars) | Hard to discover and install skills across multiple AI editors; need a single installable catalog | awesome-agent-skills, awesome-openclaw-skills |
