# Evaluation: align-dev

**Repo:** [xknight254-hub/align-dev](https://github.com/xknight254-hub/align-dev)
**Stars:** 372 | **Last updated:** 2026-06-05 | **License:** MIT
**Dev loop stage:** Plan (one-time scaffolding of a repo's agent-facing standards; touches Reflect when you revise conventions)
**Layer:** Process (it produces the team's convention contract; it is not infrastructure the agent runs against)

---

## What it does

Catalog one-liner: "Generate shared coding standards and SKILL.md so agents across teams write consistently." AlignDev is a **Next.js 16 web app** — a 7-step visual wizard — that turns a set of menu selections about your frontend stack into two downloadable artifacts: a full Markdown coding-standards document and a `SKILL.md` you drop in your repo root for Claude Code, Cursor, Copilot, and other agents to load. The premise: when several AI agents work the same codebase, each interprets "good code" differently and the directory structure, naming, state management, and UI style drift apart; a single machine-readable standards file gives every agent the same contract.

The mechanism is a **configurator, not an analyzer**. You walk seven steps (core stack / UI / state / toolchain / directories / naming / design tokens). The selections accumulate in a client-side store (`lib/wizard-store.ts`) typed by a fixed enum vocabulary (`types/wizard.ts`: `Framework = nextjs | react-spa | vue | nuxt | svelte`, `GlobalState = zustand | redux-toolkit | jotai | …`, `FileNaming = kebab-case | camelCase`, `MaxFileLines = 200 | 300 | 500`, etc.). Two renderers — `lib/document-generator.ts` and `lib/skill-generator.ts` — template those choices into the standards Markdown and the SKILL.md. It never reads your repository; nothing about your existing code informs the output. Supporting touches: an `app/api/versions` route fetches latest major versions for ~30 npm packages (with `FALLBACK_VERSIONS` on failure) so pinned versions are current; `lib/wcag-utils.ts` computes AA/AAA contrast for the chosen design-token palette; 49 preset UI styles each ship Design Tokens. Scope is explicitly **frontend** — every enum is a frontend framework, UI lib, or styling/token concern. There is no backend, language-agnostic, or general-purpose standards path.

## How we tested it

Method: inspected the repository, the English README, the GitHub API maturity signals, the repo file tree, and the source that defines the mechanism (`types/wizard.ts` option vocabulary, the `lib/*-generator.ts` renderers, the `lib/wizard-store.ts` state store, the `app/` Next.js routes). This established that it is a hosted/self-hosted web wizard that templates standards from menu choices rather than a CLI or a codebase analyzer. **Did not run the wizard or generate artifacts** — this is a source + README + maturity review, not hands-on usage. No metrics were invented; the only quantitative claims below (star/contributor counts, dates) come directly from the API.

```bash
gh api repos/razr001/align-dev --jq '{stars:.stargazers_count,license:.license.spdx_id,description:.description,created_at,pushed_at,forks:.forks_count,language:.language}'
# 372 stars, license null (MIT per LICENSE/README badge), TypeScript, created 2026-06-03, pushed 2026-06-05, 21 forks
gh api repos/razr001/align-dev/readme --jq '.content' | base64 -d          # 7-step wizard, 49 UI styles, two output artifacts
gh api repos/razr001/align-dev/contributors --jq 'length'                  # 1 contributor
gh api repos/razr001/align-dev/releases --jq '.[].tag_name'                # none
gh api repos/razr001/align-dev/contents --jq '.[].name'                    # Next.js app: app/ lib/ components/ types/ (no CLI, no bin)
gh api repos/razr001/align-dev/contents/lib --jq '.[].name'               # document-generator.ts, skill-generator.ts, wizard-store.ts, ...
gh api repos/razr001/align-dev/contents/types/wizard.ts | base64 -d        # fixed frontend-only option enums
grep -niE "reporails|align-dev|capa|agnix" CATALOG.md                      # overlap check
```

## What worked

- **Correct framing of a real pain.** Multiple agents on one repo do drift on naming, structure, and state choices, and a single root-level standards/SKILL.md is the right shape of fix. The tool names the problem accurately.
- **Low-friction first draft for greenfield frontend work.** For someone starting a new Next.js/React/Vue/Nuxt/SvelteKit project who hasn't written conventions yet, a 3-minute wizard that emits a structured SKILL.md is a faster blank-page starting point than staring at an empty file.
- **Thoughtful frontend-specific touches.** Live npm version sync (so pinned versions aren't stale), WCAG AA/AAA contrast checks on the chosen palette, and exporting Design Tokens as CSS variables/JS object are genuinely useful for a frontend standards doc and go beyond a plain template.
- **Output targets the open SKILL.md / rules pattern**, so the artifact is portable across Claude Code, Cursor, and Copilot rather than locked to one agent.

## What didn't work or surprised us

- **It is a configurator, not an analyzer.** It never reads your codebase. The output reflects the menu options you clicked, not your actual conventions — so for any *existing* repo it cannot "extract" standards; you still have to know and select them. That removes most of the leverage versus just asking an agent to write a CLAUDE.md by reading your repo.
- **Fixed, frontend-only vocabulary.** The option enums are a closed list of frontend frameworks, UI libraries, and styling choices. No backend, no language-agnostic path, no custom rules outside the wizard's menus. A team with conventions the wizard doesn't model has to hand-edit the output anyway.
- **Hand-writing (or agent-writing) a CLAUDE.md is a strong, free baseline.** Claude Code reads `CLAUDE.md` natively; an agent pointed at your repo can draft a tailored standards file grounded in your *real* code in one prompt. A menu-driven generator that emits generic standards from presets is rarely better than that for an established codebase, and offers no ongoing sync.
- **Maturity is thin and decisive here.** 372 stars but **1 contributor, no releases/tags, created 2026-06-03 and last pushed 2026-06-05** — essentially a two-day-old single-author project with no maintenance track record. For a tool whose entire value is a one-time artifact you then own and edit, there is little reason to depend on the project long-term.
- **No `LICENSE` field via the API** (MIT is asserted via README badge / LICENSE file) — minor metadata quirk.
- **Web-app delivery, not a CLI.** It does not fit a scriptable/CI or headless workflow; it's a point-and-click wizard, so it can't be re-run programmatically as conventions evolve.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral / + (situational) | A shared SKILL.md can reduce cross-agent drift, but the doc only encodes generic preset choices, not repo-grounded rules; it writes no code and validates nothing |
| Speed | + (greenfield only) | A 3-minute wizard beats a blank page for a new frontend project; for an existing repo, an agent reading the code drafts a tailored file at least as fast |
| Maintainability | neutral / + | A single agreed standards contract helps consistency, but the artifact is a one-time export with no re-sync; conventions drift away from the generated doc over time |
| Safety | neutral | No security surface; runs client-side, no credentials. WCAG contrast checks are an accessibility nicety, not a safety lever |
| Cost Efficiency | neutral | Free and self-hostable; spends no agent tokens. No measurable cost effect on the dev loop |

## Verdict

**SKIP**

AlignDev correctly identifies a real problem — multiple agents drifting on conventions — and the SKILL.md-at-repo-root shape of its fix is sound. But it solves the easy half of the problem (deciding *what* a standards file should say) with a closed, frontend-only menu, while doing nothing about the hard half (grounding standards in your *actual* codebase). It never reads your repo, so for any established project it can't extract or validate your conventions; you must already know them and pick them from a fixed list. That makes its output rarely better than an agent drafting a `CLAUDE.md` from your real code in a single prompt — which Claude Code reads natively, for free, with no new dependency.

The maturity profile makes the call easy: a 372-star, single-contributor, two-day-old web app with no releases is not something to standardize a team's convention pipeline on. **Re-evaluate only if** it (a) gains the ability to analyze an existing repo and propose standards from real code (which would make it genuinely additive rather than a fancy form), and (b) shows a sustained maintenance track record with multiple contributors. Until then it is a one-time greenfield convenience, best left as a catalog reference rather than a stack slot.

Versus neighbors: **reporails/cli** *validates* whether existing agent instructions are well-formed and non-conflicting (diagnostics); **agnix** lints agent configs against hundreds of rules with an LSP/CI path. align-dev sits upstream of both as a *generator* — the catalog's "align-dev = generate, reporails = validate" framing is accurate — but unlike those CLI/CI-native tools it is a manual web wizard with no headless mode and a far thinner maintenance base, so it is the weakest of the three as a tool you'd actually wire into a workflow. **capa** generates and manages the full primitive set (skills/rules/sub-agents/MCP/hooks) from a version-controlled `capabilities.yaml`; align-dev only emits a one-shot standards doc + SKILL.md from a UI.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [align-dev](https://github.com/xknight254-hub/align-dev) | tool | Web wizard that generates a frontend coding-standards doc and SKILL.md from menu selections so agents across teams write consistently | Multiple agents across a team generate inconsistent frontend code; need a shared standards/SKILL.md contract | reporails/cli (complementary: align-dev = generate, reporails = validate), agnix, capa |
