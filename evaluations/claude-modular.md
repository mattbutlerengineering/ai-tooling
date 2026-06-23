# Evaluation: claude-modular

**Repo:** [oxygen-fragment/claude-modular](https://github.com/oxygen-fragment/claude-modular)
**Stars:** 284 | **Last updated:** 2025-07-16 | **License:** MIT
**Dev loop stage:** Plan + Implement + Verify + Review + Ship (a full-loop command template)
**Layer:** Process (markdown command prompts) with a decorative Infrastructure/config veneer

---

## What it does

Catalog one-liner: "Modular Claude Code command framework — 30+ commands, token optimization, hierarchical config, MCP integration." It is a **`.claude/` directory template** you copy into a project. The substance is a small library of slash-command prompts organized into five category folders (`project/`, `development/`, `testing/`, `deployment/`, `documentation/`), plus a `templates/CLAUDE.md.template`, three example/playbook docs, and a `.claude/config/` tree (`settings.json` + `development.json`/`staging.json`/`production.json`) that purports to give "hierarchical, environment-specific configuration."

Mechanically, each command is a markdown file with a custom XML schema — `<instructions>` wrapping `<context>`, `<requirements>`, `<execution>`, `<validation>`, `<examples>`. For example `create-feature.md` walks the agent through plan → branch → implement → test → document → QA with a validation checklist. These are real, well-organized prompt scaffolds. You install by `cp -r .claude /path/to/project/` and editing `CLAUDE.md` from the template. The headline features — "50-80% token savings," "2-10x productivity," "hierarchical config inheritance," "security-first design" — are claims in the README and keys in `settings.json`, not enforced behavior.

## How we tested it

**Evidence:** REVIEW

Repo, README, file-tree, command-file, and config inspection via the GitHub API — **not a hands-on installed run, and not needed to reach the verdict.** The metadata alone (created and last-pushed within ~2.5 hours on the same day, single contributor, ~4 commits, no releases) plus reading the actual command files and config schema was decisive. There was no value in copying a stale template `.claude/` into a project just to confirm what the source already shows.

```bash
gh api repos/oxygen-fragment/claude-modular --jq '{stars,license,description,pushed_at,created_at,forks,open_issues}'
# 284 stars, MIT, 42 forks, 8 open issues, created AND pushed 2025-07-16 (~2.5h apart)
gh api "repos/oxygen-fragment/claude-modular/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api ".../git/trees/HEAD?recursive=1" --jq '[.tree[]|select(.path|test("commands/.*\\.md$"))]|length'  # 15
gh api repos/oxygen-fragment/claude-modular/contributors --jq '.[].login'   # oxygen-fragment (1)
gh api 'repos/oxygen-fragment/claude-modular/commits?per_page=1' -i | grep -i '^link:'   # ~4 commits total
gh api repos/oxygen-fragment/claude-modular/releases --jq '.[].tag_name'   # (none)
gh api .../contents/.claude/commands/project/create-feature.md --jq '.content' | base64 -d
gh api .../contents/.claude/config/settings.json --jq '.content' | base64 -d
```

## What worked

- **The command prompts are genuinely well-structured.** The XML schema (`context`/`requirements`/`execution`/`validation`/`examples`) is a clean, copy-able pattern. `create-feature.md`, `code-review.md`, etc. are readable, checklist-driven prompt scaffolds that a beginner could learn good command-authoring structure from. As a *reference for how to write a slash command*, the format has pedagogical value.
- **Sensible category taxonomy.** project / development / testing / deployment / documentation is a clean mental model for organizing a `.claude/commands/` tree, and the namespaced invocation (`/project:create-feature`, `/test:generate-tests`) matches Claude Code's directory-based command convention.
- **MIT licensed, fully self-contained, zero install risk.** It is just markdown and JSON — copying it mutates nothing in `~/.claude`, runs no hooks, and calls no shell. The blast radius is whatever you choose to paste in. This is the opposite of the invasive-install risk seen in claude-night-market / gstack.

## What didn't work or surprised us

- **It is an abandoned same-day template dump, not a framework.** Created and last pushed on 2025-07-16 within ~2.5 hours, 1 contributor, ~4 commits, no tags/releases, untouched for ~11 months. There is no maintenance, no community, no iteration — the antithesis of the catalog's "keeps improving" thesis.
- **The command count is inflated.** Catalog says "30+ commands"; the README says "20+"; the repo actually contains **15** command files. Neither headline number is accurate.
- **The "2-10x productivity" and "50-80% token savings" claims are unsubstantiated marketing.** There is no benchmark, no methodology, no data. The only cited basis is two markdown "research papers" committed to the repo by the same author (`The modular Claude Code implementation playbook.md`, `Optimizing Agentic Development Workflows...md`) — self-referential, not third-party validation. Treat the numbers as zero-evidence.
- **The "hierarchical config" / "token optimization" layer is decorative — it does nothing.** `settings.json` invents keys like `max_tokens_per_session`, `auto_clear_threshold`, `progressive_disclosure`, `token_optimization.lazy_loading`, `quality_gates.require_tests`, and an `extends`-based inheritance scheme. **Claude Code does not read any of these.** Real `.claude/settings.json` keys are `permissions`, `hooks`, `env`, `model`, etc. This JSON is aspirational fiction the agent might glance at as context at best; it enforces nothing. The "security-first design" (`secret_scanning`, `audit_logging`, `permission_validation`) is likewise just unread config keys, not active controls.
- **Placeholder, never-finished polish.** The README still ships `git clone https://github.com/your-username/claude-modular.git` and links Issues/Discussions/Wiki at `your-username/claude-modular`. Support links are broken; it was published without a final pass.
- **Heavy overlap with tools the user already runs, with far less substance.** Its command set (feature scaffolding, code-review, test generation, refactor, deploy, docs) is a strict subset of what superpowers (TDD/review/debugging/verification skills), GSD (phase planning/execution/verification), and claude-night-market provide — except those are maintained, code-backed, and in the user's stack. claude-modular adds nothing they lack.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Command prompts include validation checklists, but they are generic and unenforced; no mechanism beyond ordinary prompting, and nothing the user's existing skills don't already cover better. |
| Speed | neutral | Pre-written command scaffolds could save authoring time, but the "2-10x productivity" claim is unbenchmarked marketing with no evidence. |
| Maintainability | - | The framework itself is unmaintained (11 months stale, 1 author); adopting its decorative config would add unread JSON to a project that future readers may mistake for active settings. |
| Safety | neutral | Pure markdown/JSON, zero install footprint (a genuine plus), but the advertised "security-first" controls (`secret_scanning`, `audit_logging`) are non-functional config keys, not real protections. |
| Cost Efficiency | neutral | "50-80% token savings" is asserted with no data; the `token_optimization` config block is read by nothing. |

## Verdict

**SKIP**

Evaluated and rejected. claude-modular is a well-formatted but abandoned same-day template dump (1 contributor, ~4 commits, no releases, untouched ~11 months) whose headline claims do not survive inspection: "30+ commands" is actually 15, "2-10x productivity / 50-80% token savings" are unbenchmarked marketing sourced only to the author's own committed essays, and the advertised "hierarchical config / token optimization / security-first" layer is a `settings.json` full of keys Claude Code never reads — it enforces nothing. The only real artifact is ~15 generic XML-structured command prompts, which are a fine *teaching example* of command structure but add nothing the user's maintained stack lacks.

It is SKIP rather than CONDITIONAL because, unlike claude-night-market and gstack (both CONDITIONAL, cherry-pick) — which are actively maintained, have real code-backed hooks/methodology, and substance worth scoping a trial around — claude-modular has no maintenance, no code-backed enforcement, no validation, and is strictly redundant with superpowers + GSD, which the user already runs. There is nothing additive to cherry-pick. If you ever want the XML command-schema idea, copy the *pattern* from one file; do not adopt the repo. Re-evaluate only if it gains real maintenance and the config layer is reworked against actual Claude Code settings — neither of which has happened in ~11 months.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-modular](https://github.com/oxygen-fragment/claude-modular) | framework | Abandoned `.claude/` template: 15 XML-structured command prompts plus a decorative (unread-by-Claude-Code) config layer; "30+ commands / 2-10x" claims are inflated | Ad-hoc Claude Code setups lack systematic command organization and reuse | superpowers, claude-night-market, GSD, gstack |
