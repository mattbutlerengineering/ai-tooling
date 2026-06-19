# Evaluation: Waza

**Repo:** [tw93/Waza](https://github.com/tw93/Waza)
**Stars:** 5,945 | **Last updated:** 2026-06-19 (pushed; created 2026-03-12) | **License:** MIT
**Dev loop stage:** Spans the inner loop by *habit* — Plan (`/think`), Implement/Design (`/design`), Verify (`/hunt` debugging), Review (`/check`), plus Reflect/knowledge (`/learn`, `/read`, `/health`). It is a curated skill suite, not a single-stage tool.
**Layer:** Process / Tooling (eight installed Agent Skills — `SKILL.md` + reference docs + helper scripts per skill; cross-tool via the `skills` installer and Claude Code / Codex plugin marketplaces)

---

## What it does

The catalog one-liner: "🥷 Engineering habits you already know, turned into skills Claude can run." Waza (技, *waza* — a martial-arts term for a move drilled until it becomes instinct) packages eight engineering disciplines as installable skills, each invoked as a slash command in Claude Code (or by name in Codex/Antigravity/OpenCode): `/think` (pressure-test the problem and produce a decision-complete plan), `/design` (distinctive frontend UI with screenshot-driven aesthetic iteration), `/check` (review the diff, extract project constraints, verify with evidence, handle approved release/publish follow-through), `/hunt` (systematic debugging — confirm root cause before any fix), `/write` (rewrite prose to read naturally in English and Chinese), `/learn` (six-phase produce-to-learn research workflow), `/read` (URL/PDF reading with platform-specific routing), and `/health` (audit agent/project health with a budget-aware summary pass).

The mechanism is the now-standard Agent Skills pattern: each skill is a folder with a dense `SKILL.md` the host agent reads and follows, plus `references/` (gotchas from real failures), `agents/` (sub-agent definitions, e.g. `reviewer-architecture.md` under `/check`), and helper `scripts/`. A `RESOLVER.md` and `rules/waza-routing.md` handle skill routing, and `rules/` carries cross-cutting context (anti-patterns, durable-context, English/Chinese style). It installs globally (`npx skills add tw93/Waza -a claude-code -g -y`) or per-skill, and ships both a Claude Code plugin marketplace and a Codex plugin marketplace. Waza is the middle of a deliberate trilogy by the same author — Kaku (書く, writes code), Waza (技, drills habits), Kami (紙, ships documents).

## How we tested it

**Source-grounded inspection — not installed, not run.** No skill was installed via `npx skills add` or the plugin marketplace, no slash command was invoked, and no helper script was executed. Every claim comes from the repository (GitHub metadata, README, recursive file tree, the skills/rules layout), not from observed behavior. The CI badges (tests passing) and release count are repo facts; the *quality* of each skill in use was not measured.

```bash
gh api repos/tw93/Waza --jq '{desc,stars:.stargazers_count,forks:.forks_count,pushed:.pushed_at,created:.created_at,license:.license.spdx_id,topics:.topics}'
gh api repos/tw93/Waza/readme --jq '.content' | base64 -d
gh api "repos/tw93/Waza/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api repos/tw93/Waza/commits --jq 'length'   # 30 (page-1 cap)
gh api repos/tw93/Waza/releases --jq 'length'  # 30
```

## What worked

- **Genuinely well-maintained and disciplined.** MIT, 5,945★ / 358 forks, **30 tagged releases**, CI with both `test.yml` and `release.yml`, a `packaging.allowlist`, `VERSION`, and `CLAUDE.md`/`AGENTS.md`. This is real release engineering, not a prompt dump — rare among skill collections in this catalog.
- **Curated, not bloated.** Eight skills chosen to map onto the actual engineering loop, versus the 200–271-file mega-rosters elsewhere in the catalog. Each maps to a clear "when to use" trigger, which keeps the routing surface small and legible.
- **Cross-tool and cross-lingual by design.** First-class install paths for Claude Code, Codex, Antigravity (app + CLI), and OpenCode, plus explicit English/Chinese prose support in `/write` — useful for bilingual teams, distinctive among English-only skill packs.
- **Habits that match this catalog's values.** `/think` (decision-complete planning), `/hunt` (root-cause-before-fix debugging), and `/check` (verify-with-evidence review) are exactly the disciplines the dev-loop framework prizes — close cousins of the superpowers brainstorming / systematic-debugging / verification skills.
- **Skills carry real failure-mode notes.** `references/` with "gotchas from real failures" and dedicated reviewer sub-agents under `/check` suggest the content is iterated, not theoretical.

## What didn't work or surprised us

- **Heavy overlap with skills you likely already run.** Each Waza skill has a near-direct counterpart in the superpowers suite (`/think` ≈ brainstorming, `/hunt` ≈ systematic-debugging, `/check` ≈ verification-before-completion / requesting-code-review, `/design` ≈ frontend-design). For a setup already running superpowers, Waza is largely duplicative rather than additive.
- **It's a workflow pack, not deterministic tooling.** Like all skill collections, outcomes depend on the host model following dense `SKILL.md` instructions; there is no code enforcing the disciplines. Quality varies with the driving agent.
- **Trilogy coupling / scope creep risk.** Some value assumes adopting the siblings (Kaku for code, Kami for docs); installing all three enlarges the skill/routing surface considerably.
- **Routing adds a layer.** `RESOLVER.md` + `waza-routing.md` are a small meta-system to learn; for users who prefer invoking skills directly this is extra surface, and it can compete with other installed routers.
- **Author-brand momentum.** A chunk of the star count tracks the author's following (tw93 is a popular Mac/dev-tools author); popularity is a weak proxy for per-skill quality, which still has to be judged skill-by-skill.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | `/hunt` (root-cause-before-fix) and `/check` (verify-with-evidence) institutionalize disciplines that reduce wrong-fix and unverified-done failures. |
| Speed | + / neutral | Slash-command habits remove the cost of re-prompting structure each session; offset by overlap with skills already loaded and the routing layer to learn. |
| Maintainability | + | `/think` and `/check` push decision-complete plans and constraint extraction; the *repo itself* is unusually maintainable (30 releases, CI, allowlist). |
| Safety | neutral | Skill instructions + local helper scripts; no inherent network/host reach beyond what the host agent already has. |
| Cost Efficiency | neutral | Lean eight-skill set is token-frugal vs mega-rosters; full-trilogy adoption raises the routing/skill surface. |

## Verdict

**CONDITIONAL** — adopt selectively if you are *not* already running an equivalent discipline suite. Waza is one of the highest-quality skill packs in this catalog: curated to eight loop-aligned habits, genuinely maintained (30 releases, CI, plugin marketplaces), cross-tool, and bilingual. The blocker to a blanket ADOPT is overlap — for a setup already running superpowers (brainstorming, systematic-debugging, verification, frontend-design), most of Waza is duplicative, and running two routing layers adds friction. Cherry-pick the skills that fill genuine gaps (e.g. `/write` for bilingual prose, `/health` for agent-config audits) rather than installing the full pack on top of existing coverage.

Compared to neighbors: **agency-agents** is a 271-file uncoordinated persona menu (CONDITIONAL, cherry-pick); Waza is the opposite design — a small, curated, version-released suite. Against **superpowers**, Waza is comparable in philosophy but narrower and largely overlapping; superpowers is the broader, more battle-tested base, so Waza is best treated as a *supplement* for its few distinctive skills, not a replacement.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Waza](https://github.com/tw93/Waza) | skill | Eight curated, version-released engineering-habit skills (`/think` `/design` `/check` `/hunt` `/write` `/learn` `/read` `/health`), cross-tool and bilingual | Want loop-aligned engineering disciplines (plan, debug, review, verify) as installable slash commands without writing them yourself | superpowers (brainstorming/debugging/verification/frontend-design), agency-agents (uncurated roster), gstack |
