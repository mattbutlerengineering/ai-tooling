# Evaluation: pm-skills

**Repo:** [phuryn/pm-skills](https://github.com/phuryn/pm-skills)
**Stars:** 19,769 | **Last updated:** 2026-06-06 (pushed; created 2026-03-01) | **License:** MIT
**Dev loop stage:** Mostly *outside* the software dev loop — it targets the product-management workflow (discovery → strategy → execution → launch → growth). The exception is the `pm-ai-shipping` plugin, which lands squarely in our **Verify/Review** stages: it audits AI-built code for the gap between documented intent and actual implementation (`intended-vs-implemented`, `ship-check`, static security/performance audits).
**Layer:** Process (a Claude Code plugin *marketplace* of `SKILL.md` files + `/slash` command workflows; no runtime, no executing code)

---

## What it does

The catalog one-liner: "100+ agentic skills for product management (discovery, strategy, execution, launch)." As inspected, the repo is a **marketplace of 9 plugins** (`pm-toolkit`, `pm-product-strategy`, `pm-product-discovery`, `pm-market-research`, `pm-data-analytics`, `pm-marketing-growth`, `pm-go-to-market`, `pm-execution`, `pm-ai-shipping`) shipping **68 `SKILL.md` files and 42 command (`/slash`) workflows** — the README's "68 skills and 42 chained workflows across 9 plugins." Each skill encodes a named PM framework (Teresa Torres opportunity-solution trees, Marty Cagan, Alberto Savoia pretotyping); commands *chain* skills into an end-to-end process (e.g. `/discover` = brainstorm-ideas → identify-assumptions → prioritize-assumptions → brainstorm-experiments), and commands suggest the next command on completion.

The mechanism is a real Claude Code plugin marketplace (`.claude-plugin/marketplace.json`): `claude plugin marketplace add phuryn/pm-skills` then install plugins individually. Skills auto-load on relevant conversation; commands are user-triggered. It's explicitly built for Claude Code and Cowork, with Codex reading the same marketplace file (skills install; the `/slash` commands don't expose as Codex commands), and other tools getting skills-only via folder copy. The standout for *this* catalog is `pm-ai-shipping`: its `intended-vs-implemented` skill is a sharp method for auditing AI-generated code against written intent (permissions docs, architecture docs) — the class of bug generic linters miss — paired with `ship-check`, `security-audit-static`, `performance-audit-static`, and `derive-tests` commands.

## How we tested it

**Source-grounded inspection — not installed, not run.** No plugin was installed, no marketplace was added, and no command was executed. Every claim comes from the repository (GitHub metadata, README, full recursive file tree, two sampled `SKILL.md` files), not from observed behavior. The "proven frameworks / better decisions" language and the named-thinker pedigree are the author's README framing, not anything measured here.

```bash
gh api repos/phuryn/pm-skills --jq '{desc,stars:.stargazers_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'
gh api repos/phuryn/pm-skills/readme --jq '.content' | base64 -d | head -120
gh api "repos/phuryn/pm-skills/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api "...trees/HEAD?recursive=1" --jq '[.tree[]|select(.path|endswith("SKILL.md"))]|length'                       # 68 skills
gh api "...trees/HEAD?recursive=1" --jq '[.tree[]|select(.path|test("/commands/")and endswith(".md"))]|length'      # 42 commands
gh api "...trees/HEAD?recursive=1" --jq '.tree[].path|select(test("plugin.json"))'                                  # 9 plugins
gh api repos/phuryn/pm-skills/contents/pm-ai-shipping/skills/intended-vs-implemented/SKILL.md --jq '.content' | base64 -d | head -25
gh api repos/phuryn/pm-skills/contributors --jq '[.[].login]|length'   # 2
```

## What worked

- **Real marketplace + chained commands, not a flat skill dump.** 9 installable plugins, and commands that *compose* skills into a guided workflow with next-step suggestions — meaningfully more structured than agency-agents' "activate one persona by hand." This is closer to a workflow than most domain collections.
- **`pm-ai-shipping` is genuinely dev-relevant.** `intended-vs-implemented` is a well-articulated audit method ("a linter scans code in a vacuum… it cannot tell you the code does what you meant") that fills the Verify/Review gap for AI-built code. Cherry-picking this one plugin is the strongest reason a software team would touch this repo.
- **Framework pedigree gives the skills substance.** Discovery/strategy skills encode recognized PM methods (opportunity-solution trees, pretotyping, assumption mapping) rather than generic advice.
- **Strong traction and cross-tool install.** 19.8K stars, ~2K forks, native Claude Code/Cowork install plus Codex marketplace compatibility and skills-only paths for Gemini/OpenCode/Cursor/Kiro.

## What didn't work or surprised us

- **Mostly out of scope for a software-dev catalog.** 8 of 9 plugins are PM work (PRDs, OKRs, launches, cohort analysis, competitor research) — they don't produce or improve code and move none of our code-quality signals. The catalog row sits in "Skills & Plugins" but the fit is "if you are also the PM," not "if you ship code."
- **Two-author project.** Only 2 contributors — this is essentially one maintainer's curated marketplace, not a community-fed one (contrast the 23 contributors on marketingskills). Bus-factor and long-term maintenance risk are real.
- **No releases; pinned to `main`.** 0 tagged releases — `claude plugin install` pulls whatever `main` is, with no stable, versioned bundle.
- **Cross-tool degradation.** On Codex the `/slash` workflows don't run as commands (best-effort manual conversion); on Gemini/OpenCode/Cursor/Kiro you get skills only. The composed-command experience is Claude-Code/Cowork-specific.
- **"Better decisions" is author framing.** No evidence in the repo substantiates outcome claims; they're PM-domain copy, and unlike marketingskills there are *no eval files* to back trigger/behavior quality.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + (one plugin) / neutral (rest) | `pm-ai-shipping`'s `intended-vs-implemented` + `ship-check`/`security-audit-static` can catch real intent-vs-code bugs in AI-built software; the other 8 plugins judge PM artifacts, not code. |
| Speed | neutral | Speeds *PM* tasks (PRDs, discovery); the shipping audits add a Verify step rather than accelerating coding. |
| Maintainability | neutral | Pure markdown skills/commands; no effect on a codebase's structure. |
| Safety | + | No code executes — markdown-only, no network/host reach; the static-audit commands *read* code without running it. Lowest-risk install class. |
| Cost Efficiency | neutral | Per-task cost of loading a skill or running a chained command; no structural cost effect on dev work. |

## Verdict

**CONDITIONAL — install `pm-ai-shipping` only if you ship AI-built code; SKIP the rest unless you also do PM.** pm-skills is a well-structured plugin marketplace with composed command workflows, which puts it a notch above flat persona/skill dumps. But 8 of its 9 plugins are product-management work that doesn't intervene in the software dev loop. The lone bridge into our catalog is `pm-ai-shipping` — `intended-vs-implemented` is a sharp, genuinely useful Verify/Review method for auditing generated code against documented intent, and worth cherry-picking. The two-author maintenance profile and absence of eval files temper confidence; install the one plugin, skip the bulk.

Compared to neighbors: **marketingskills** (sibling business-function pack) is better-authored on rigor (43 eval files vs. none here) but has *no* dev bridge — pm-skills' `pm-ai-shipping` makes it marginally more relevant to a software team. Versus **harness** (revfactory), which *generates* a tailored team, pm-skills is a fixed curated marketplace; versus **agency-agents**, its chained commands are real composition rather than hand-activated personas. For pure code work, the dedicated review/audit tools elsewhere in the catalog beat a PM marketplace's one shipping plugin.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [pm-skills](https://github.com/phuryn/pm-skills) | plugin | Marketplace of 9 PM plugins — 68 skills + 42 chained commands (discovery → strategy → execution → launch); the `pm-ai-shipping` plugin audits AI-built code vs. documented intent | Want AI help with product-management work, plus a Verify/Review plugin that catches intent-vs-implementation bugs generic linters miss | marketingskills (sibling business-function pack, domain-specific); harness/agency-agents (skill/persona collections) |
