# Evaluation: cc-skills-golang

**Repo:** [samber/cc-skills-golang](https://github.com/samber/cc-skills-golang)
**Stars:** 2,227 | **Last updated:** 2026-06-09 (pushed; created 2026-03-21) | **License:** MIT
**Dev loop stage:** Primarily **Implement** and **Review** (idiomatic Go authoring + diff-focused review modes), with strong **Verify** coverage (testing, benchmarking, troubleshooting) and **Reflect/Ship** touches (observability, CI, security scanning). A language-knowledge layer that loads on demand into whichever stage the agent is in.
**Layer:** Process — a pack of 43 cross-referencing `SKILL.md` instruction sets (plus references, code examples, and per-skill evals); no runtime of its own.

---

## What it does

A **Go-specific** agent-skills collection from samber — author of the widely used `samber/lo`, `samber/do`, `samber/oops`, `samber/slog-*` Go libraries. Where most public skill packs lean TypeScript/Python, this one covers Go's idioms end to end: 43 atomic skills spanning code quality (`golang-error-handling`, `golang-naming`, `golang-code-style`, `golang-lint`, `golang-structs-interfaces`), architecture (`golang-design-patterns`, `golang-dependency-injection`, `golang-project-layout`, `golang-context`, `golang-concurrency`), QA/perf (`golang-testing`, `golang-benchmark`, `golang-performance`, `golang-troubleshooting`, `golang-observability`, `golang-security`, `golang-safety`), project-start scaffolding (`golang-cli`, `golang-grpc`, `golang-graphql`, `golang-database`, `golang-swagger`), and library-specific skills for the popular ecosystem (`golang-spf13-cobra`, `golang-spf13-viper`, `golang-stretchr-testify`, `golang-uber-fx`, `golang-uber-dig`, `golang-google-wire`) and samber's own libs (`golang-samber-lo/do/mo/oops/slog/hot/ro`).

The skills are explicitly designed as **cross-referencing units** — `golang-error-handling` defers slog-handler details to `golang-samber-slog` and oops specifics to `golang-samber-oops`, with a documented "install all general-purpose skills together" recommendation so the guidance stays consistent. The frontmatter is unusually rich: each skill declares a persona, **modes** (coding / review / audit, with audit fanning out parallel sub-agents per category), `allowed-tools` scoped to Go tooling (`Bash(go:*)`, `Bash(golangci-lint:*)`), version, and a "company skill supersedes community default" precedence rule. It is multi-tool by design (skills.sh CLI, Claude Code plugin marketplace, Gemini CLI extension, Cursor, Copilot, OpenCode, Codex, Antigravity, Openclaw).

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No skill was installed, no Go project was generated or reviewed under the skills, and the published eval numbers were *not* reproduced by me. Every claim below comes from the repository: GitHub metadata, README, full recursive file tree, the `EVALUATIONS.md` results table, and the full text of `skills/golang-error-handling/SKILL.md` as a representative sample. The with-skill/without-skill uplift figures cited are **the author's reported eval results**, read from `EVALUATIONS.md` — I did not regenerate them.

```bash
gh api repos/samber/cc-skills-golang --jq '{desc,stars:.stargazers_count,forks:.forks_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id,topics:.topics}'
# desc: null | stars 2227 | forks 141 | topics incl. claude-code, codex, cursor, gemini, opencode, antigravity, openclaw
gh api "repos/samber/cc-skills-golang/git/trees/HEAD?recursive=1" --jq '.tree[]|select(.path|test("^skills/[^/]+$")).path' | wc -l   # 43 skills
gh api repos/samber/cc-skills-golang/contents/skills/golang-error-handling/SKILL.md --jq '.content' | base64 -d   # persona + 3 modes + scoped allowed-tools + version 1.2.0
gh api repos/samber/cc-skills-golang/contents/EVALUATIONS.md --jq '.content' | base64 -d   # per-skill with/without-skill assertion tables
gh api repos/samber/cc-skills-golang/commits --jq 'length'    # 30 (page-1 cap)
gh api repos/samber/cc-skills-golang/releases --jq 'length'   # 7 tagged releases
```

## What worked

- **Fills a real gap with credible authorship.** Go-specific agent skills are scarce relative to TS/Python, and samber is a recognized Go library author — the library skills (`samber-*`, uber-fx, cobra, testify) encode real ecosystem knowledge, not generic advice. The README explicitly states the skills were distilled from the author's own Go commits and then "edited, tested, reviewed and reworked by a human."
- **Published eval data — rare and the right discipline.** `EVALUATIONS.md` reports per-skill with-skill vs. without-skill assertion pass rates and uplift, with version stamps. Most are meaningful gains (e.g. `golang-concurrency` 100% vs 61%, +39pp; `golang-dependency-injection` 98% vs 51%, +47pp; `golang-database` 95% vs 57%). Crucially it also **flags its own weak results** ("low delta, high without" on `golang-spf13-viper`/`-cobra` where the baseline is already ~98–100%, and "low with-skill score" on `golang-code-style` 80% and `golang-samber-mo` 88%). That honesty is a quality signal in itself.
- **Genuinely strong skill engineering.** The error-handling SKILL.md ships a persona, three operating modes (coding/review/audit), parallel sub-agent fan-out for audits, scoped `allowed-tools` limiting Bash to `go`/`golangci-lint`/`git`, and a clear precedence rule for company overrides. This is materially more disciplined than the typical single-file persona pack.
- **Cross-referencing avoids contradiction.** The "atomic, cross-referencing units" design (error-handling owns the logging rules, observability defers to it) reduces the conflicting-guidance problem that large skill packs usually suffer.
- **Maintained and CI-backed.** 7 releases, per-skill versions (error-handling at v1.2.0), and workflows for lint/validate/security-scan plus auto-updating library skills. Multi-tool install paths are documented for 8+ editors.

## What didn't work or surprised us

- **All-or-nothing for full value.** The cross-referencing design means installing a single skill gives "a partial and potentially inconsistent view"; the author recommends installing all general-purpose skills. That is 30+ skills competing for the agent's attention — a real discovery/context-budget cost on any non-trivial Go session.
- **Opinionated toward samber's stack.** Seven `golang-samber-*` skills and a heavy `do`/`fx`/`wire` DI emphasis bake the author's library preferences into the guidance. Excellent if you use those libs; noise (and possible nudging toward them) if you don't.
- **Some skills barely beat baseline.** By the project's own evals, `golang-spf13-viper` (−2pp) and `golang-spf13-cobra` (+2pp) add little over a strong baseline, and `golang-code-style` tops out at 80% even *with* the skill — useful honesty, but it means a few skills are low-value installs.
- **Evals are author-run, not independently reproduced.** The uplift table is convincing but self-reported; I did not re-run it, and assertion-pass-rate is a proxy for idiomatic correctness, not a guarantee of shipped-code quality.
- **No description and Go-only by definition.** The repo has no GitHub description, and the value is strictly scoped to Go projects — irrelevant to a non-Go codebase.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Strongest signal: idiomatic Go rules (`%w` wrapping, `errors.Is/As`, single-handling rule, no swallowed errors) with audit/review modes that grep for violations; evals show large pass-rate uplift on most skills. |
| Speed | + / − | Encodes idioms the agent would otherwise re-derive, speeding authoring and review; offset by the context cost of loading 30+ cross-referencing skills for full consistency. |
| Maintainability | + | Pushes project-layout, naming, structs/interfaces, and DI conventions that keep a Go codebase consistent and navigable. |
| Safety | + / neutral | Dedicated `golang-security` and `golang-safety` skills plus repo-level security-scan CI; `allowed-tools` are scoped to Go tooling rather than open Bash, limiting blast radius. |
| Cost Efficiency | neutral | On-demand loading keeps idle cost low, but the "install all" recommendation enlarges per-session context; a few skills add little over baseline and aren't worth the tokens. |

## Verdict

**ADOPT (for Go projects) — the strongest language-specific skill pack in this catalog.** For anyone doing AI-assisted Go development, cc-skills-golang is a clear win: credible library-author provenance, genuinely well-engineered skills (personas, coding/review/audit modes, scoped tools), a cross-referencing design that avoids self-contradiction, published-and-self-critical eval data, and active maintenance with real releases. Install the general-purpose skills as a set, skip the `golang-samber-*` and `spf13-*` skills unless you use those libraries, and treat the low-uplift ones (viper, cobra, code-style) as optional. The honesty of `EVALUATIONS.md` — flagging its own weak deltas — is exactly what the catalog rewards. Verdict is scoped: irrelevant outside Go.

Compared to neighbors: it is the clear standout among **language/domain skill packs**. **SwiftUI-Agent-Skill** is a single-domain skill; **mattpocock/skills** is the TypeScript-side complement (the two are non-overlapping by language); broad packs like **wshobson/agents**, **ECC**, and **gstack** spread across many languages and roles but none match this depth or eval rigor *for Go specifically*. Where general packs give you breadth, cc-skills-golang gives you a vetted, eval-backed Go vertical — and it publishes its scorecard, which almost none of the others do.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [cc-skills-golang](https://github.com/samber/cc-skills-golang) | skill | 43 cross-referencing, eval-backed Go agent skills (idioms, testing, perf, security, DI, popular libs) by Go library author samber; multi-editor, persona + coding/review/audit modes | Go developers lack deep, idiomatic, vetted agent skills — most public packs are TypeScript/Python focused | mattpocock/skills (complementary: TypeScript vs Go); SwiftUI-Agent-Skill (other language-specific skill); wshobson/agents, ECC, gstack (broad packs without Go depth or eval data) |
