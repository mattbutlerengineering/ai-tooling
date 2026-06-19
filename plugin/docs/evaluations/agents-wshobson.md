# Evaluation: agents (wshobson)

**Repo:** [wshobson/agents](https://github.com/wshobson/agents)
**Stars:** 36,966 | **Last updated:** 2026-06-17 | **License:** MIT
**Dev loop stage:** Plan + Implement + Verify + Review + Ship + Reflect (a full-loop marketplace)
**Layer:** Tooling

---

## What it does

Catalog one-liner: "Multi-harness plugin marketplace — 84 plugins, 192 agents, 156 skills across 6 editors." It is an **agentic plugin marketplace** built from a single Markdown source-of-truth (`plugins/`) and shipped natively to six harnesses — Claude Code, OpenAI Codex CLI, Cursor, OpenCode, Gemini CLI, and GitHub Copilot. The repo's own headline numbers (84 plugins, 192 agents, 156 skills, 102 commands, 16 orchestrators) match the source tree exactly: 156 `SKILL.md`, 192 agent `.md` files, 82 local `plugin.json` (84 counting 2 external git-subdir entries), 102 command `.md`.

Mechanically, plugins are granular single-purpose installable units. For Claude Code you `/plugin marketplace add wshobson/agents` then `/plugin install python-development` (or any of 84) — installing a plugin loads only its components into context, not the whole marketplace. Each plugin auto-discovers agents/commands/skills from its directory structure (e.g. `plugins/python-development/` ships 3 agents, 1 command, 16 skills). Agents carry a **tiered model strategy** in frontmatter (Tier 0 Fable 5 for long-horizon autonomous work, Tier 1 Opus for architecture/security/review, Tier 2 inherit, Tier 3 Sonnet for docs/testing, Tier 4 Haiku for fast ops). The multi-harness story is the real differentiator: `make generate-all` emits harness-native artifacts per adapter (Codex respects an 8KB skill cap, OpenCode derives a `permission:` block from the `tools:` allowlist, Gemini emits TOML subagents, Copilot emits Markdown agent profiles) — not lowest-common-denominator translations. It also ships `plugin-eval`, a three-layer quality framework (Static structural <2s, LLM Judge across 4 dimensions, Monte Carlo 50-100 simulated runs) used to score/certify plugins.

## How we tested it

Repo, README, source-tree, and CI-workflow inspection via the GitHub API — **not a hands-on installed run**. Installing even one plugin mutates `~/.claude` and adds the marketplace; the full marketplace spans 156 skills + 192 agents with broad domain vocabulary, and would overlap the user's existing OMEGA + superpowers + skills setup — too invasive to install just to evaluate. Findings rest on the repo metadata, README, the recursive source tree (counts verified programmatically), the documented model-tier and multi-harness adapter design, the CI-workflow set, the `plugin-eval` framework presence, and the contributor/commit history.

```bash
gh api repos/wshobson/agents --jq '{stars,license,description,pushed_at,created_at,forks,open_issues}'
# 36,966 stars, MIT, 3,994 forks, 19 open issues, created 2025-07-24, pushed 2026-06-17
gh api repos/wshobson/agents/readme --jq '.content' | base64 -d
gh api "repos/wshobson/agents/git/trees/HEAD?recursive=1" --jq '[.tree[].path]'
# verified: 156 SKILL.md, 192 agents, 82 local plugin.json, 102 commands, 111 test paths
gh api repos/wshobson/agents/contributors --paginate --jq '.[].login' | wc -l   # 64
gh api 'repos/wshobson/agents/commits?per_page=1' -i | grep -i '^link:'          # ~455 commits
# CI: claude-code-review, claude, code-quality, eval-report, validate ; Makefile + CONTRIBUTING.md + plugin-eval present
```

## What worked

- **Counts are honest and the marketplace is genuinely modular.** Every headline number in the README matches the source tree exactly (156 skills, 192 agents, 102 commands), and the architecture is real opt-in: installing a plugin loads only its components, so the install footprint is per-plugin, not all-or-nothing. This is the same blast-radius-limiting posture that earned claude-night-market a credible CONDITIONAL.
- **The multi-harness adapter design is the standout differentiator.** One Markdown source generates harness-native artifacts for six editors (Claude Code, Codex, Cursor, OpenCode, Gemini, Copilot) with real per-harness constraints respected (Codex 8KB skill cap, OpenCode permission blocks from tool allowlists, Gemini TOML, Copilot model mapping). Nothing else in the user's catalog packages the same content across this many harnesses from a single source — that is additive, not redundant.
- **Real multi-contributor maturity.** 64 contributors and ~455 commits against 36,966 stars and 3,994 forks — a far healthier community-to-commit ratio than the solo-led bundles (claude-night-market: 2 contributors/311 stars; gstack: 9/111K). 19 open issues. This is one of the more community-validated entries among the plugin bundles.
- **A built-in quality-evaluation framework.** `plugin-eval` is a three-layer scorer (deterministic static checks, an LLM judge across 4 dimensions, and a Monte Carlo reliability run of 50-100 simulations) with `score` and `certify` commands. Most bundles assert quality; this one ships the apparatus to measure it — and uses it via an `eval-report` CI workflow.
- **Sensible CI and engineering hygiene.** 5 GitHub Actions workflows (claude-code-review, claude, code-quality, eval-report, validate), a `Makefile` (`make validate / garden / generate-all` for drift / dead-link / cap detection), `CONTRIBUTING.md`, and a `docs/` set (architecture, authoring, harnesses, round-trip-results). 111 test-related paths in the tree.
- **Tiered model strategy is explicit and cost-aware.** Each agent declares an intended tier (Opus for architecture/security, Sonnet for docs/testing, Haiku for fast ops, inherit for user choice, opt-in Fable 5 for long-horizon runs), mapping work to the cheapest capable model rather than defaulting everything to the top tier.

## What didn't work or surprised us

- **Massive surface that substantially overlaps tools the user already runs.** 84 plugins / 192 agents / 156 skills span architecture, every major language, infra, security, data, ML, docs, business, and SEO. Large fractions (code review, debugging, security scans, test generation, language experts) duplicate superpowers (TDD/review/debug/verification), the user's commit/review skills, and OMEGA. Installing broadly would be redundant bulk; only the genuinely additive, domain-specific plugins (a language stack the user lacks, the multi-harness packaging) are net-new.
- **Kitchen-sink breadth dilutes curation.** With 192 agents covering "business," "SEO," "content marketing," and "customer sales automation" alongside core engineering, this is closer to a comprehensive registry than a curated stack. Discoverability across 84 plugins is a real cost; the value is in cherry-picking, not adopting wholesale.
- **No neutral benchmark of agent quality.** `plugin-eval` measures structural and simulated quality, but there is no third-party evidence any given agent beats vanilla Claude Code (or the user's existing skill for the same task) on a real task. The value case rests on the (plausible) mechanics plus breadth, not proven per-agent lift.
- **Catalog naming collision to flag, not a defect of this tool.** The current catalog "Overlaps with" lists *everything-claude-code (now ECC)*. ECC is a **separately authored** project (renamed everything-claude-code) and is **not** wshobson/agents — they are distinct marketplaces that happen to occupy the same multi-harness-bundle niche. The overlap is thematic (both are large multi-harness plugin marketplaces), and that overlap is correct to record, but the two should not be conflated.
- **Multi-harness install paths vary in friction.** Claude Code, Codex, and Cursor install from committed registries, but Gemini and OpenCode require clone + `make generate` — a heavier path that needs the repo checked out locally and the toolchain run.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Domain-expert agents (security, architecture, language-specific) plus comprehensive-review / debugging / data-validation plugins target real review and defect-detection paths; `plugin-eval` certifies skill quality before use |
| Speed | +/- | Scaffolding/test-gen/infra-setup commands and 16 multi-agent orchestrators automate multi-step flows; offset by the discovery cost of 84 plugins and ceremony for small changes |
| Maintainability | + | `make garden` drift/dead-link/cap detection, `validate` structural checks, `code-quality` CI, code-documentation / code-refactoring / codebase-cleanup plugins, and a single-source authoring model reduce content rot |
| Safety | +/- | Security-focused plugins (backend-api-security, security scans) and OpenCode permission-block derivation help; offset by a large install surface of agents that can read/edit and run shell, from a marketplace too broad to fully vet before installing |
| Cost Efficiency | + | Explicit tiered model strategy (Opus/Sonnet/Haiku/inherit, opt-in Fable 5) routes each agent to the cheapest capable model rather than defaulting to the top tier |

## Verdict

**CONDITIONAL**

Adopt selectively — add the marketplace and install only the one or two plugins whose content is genuinely additive (most likely a language/domain stack the user lacks, e.g. a specific backend/data/ML plugin, or the multi-harness packaging if the user works across Codex/Cursor/Gemini/Copilot). The per-plugin install loads only that plugin's components, so a scoped trial is safe. It earns CONDITIONAL over SKIP on real merits the solo bundles lack: honest counts that match the tree exactly, a genuine 64-contributor community (vs 2 for claude-night-market, 9 for gstack), a built-in `plugin-eval` quality framework with CI enforcement, an explicit cost-aware model-tier strategy, and a multi-harness adapter design that is the most distinctive thing in this niche.

It is **not** ADOPT because the surface is a kitchen-sink registry (84 plugins / 192 agents / 156 skills spanning business, SEO, and marketing alongside engineering) that substantially **duplicates** tools the user already runs — superpowers (TDD/review/debug/verification), the user's commit/review skills, and OMEGA — so installing broadly is redundant bulk rather than addition. The sensible path mirrors claude-night-market and gstack: cherry-pick the few genuinely net-new plugins, do not adopt the marketplace wholesale. Note for the catalog: the listed overlap *everything-claude-code (ECC)* is a **separate** marketplace, not this repo — both are large multi-harness bundles in the same niche, so recording the overlap is right, but they are distinct projects and should not be merged. Re-evaluate toward ADOPT if a hands-on run shows a specific plugin's agents outperform the user's existing stack, or if the multi-harness packaging becomes load-bearing for the user's cross-editor workflow.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agents (wshobson)](https://github.com/wshobson/agents) | plugin | Multi-harness plugin marketplace built from one Markdown source: 84 plugins, 192 agents, 156 skills, 102 commands shipped natively to Claude Code, Codex, Cursor, OpenCode, Gemini, and Copilot | Want production-ready, per-plugin-installable agents/skills usable across six AI coding harnesses from a single source, with a built-in quality-eval framework | ECC (separate marketplace, same niche), claude-night-market, gstack, superpowers, oh-my-claudecode |
