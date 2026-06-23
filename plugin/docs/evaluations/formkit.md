# Evaluation: FormKit

**Repo:** [formkit/formkit](https://github.com/formkit/formkit)
**Stars:** 4,729 | **Last updated:** 2026-06-10 (v2.1.0) | **License:** MIT
**Dev loop stage:** Implement (a UI library you build apps with; ships an optional agent skill)
**Layer:** Infrastructure (application dependency)

---

## What it does

Catalog one-liner: "The form framework for coding agents." In reality, FormKit is the long-established Vue (and now React) **form-building library** — created by Justin Schroeder in 2021, "trusted by NBC, Nike, Bosch, Anthem Blue Cross" — that has repositioned its v2.x marketing around coding agents. The product is a UI component library: every `<FormKit>` component owns a "node" in a framework-agnostic node tree; nodes self-structure data (`group` → object, `list` → array), co-locate validation (`validation="required|email"`), compile JSON schemas, theme via Tailwind, and i18n in 30+ languages. The monorepo is the same `@formkit/core` / `@formkit/validation` / `@formkit/vue` / `@formkit/react` packages it has always shipped, plus a paid "FormKit Pro" tier of premium inputs.

The "for coding agents" claim rests on two real but narrow things: (1) the compact single-component API and self-structuring node tree are genuinely easier for an LLM to reason about than hand-wired form state, so generated form code is less error-prone; and (2) the CLI ships an actual **Agent Skill** — `npx formkit skill` copies a `SKILL.md` (+ `references/docs-index.md`) into the agent's skills dir and wires project instructions into `CLAUDE.md`/`AGENTS.md`, supporting 11 agents (Claude Code, Codex, Cursor, Cline, Gemini, Qwen, Amp, pi, Copilot, Crush, OpenCode). The skill teaches the agent FormKit's mental model (declarative over event listeners), runtime-specific doc routes (`*.react.md` vs `*.vue.md`), core-vs-Pro input distinctions, and theming workflow.

## How we tested it

**Evidence:** REVIEW

Architecture and surface-area review via the GitHub API — repo metadata, README, root `CLAUDE.md`, package list, the `packages/cli/src/skill.ts` installer, and the shipped skill asset `packages/cli/assets/skills/formkit/SKILL.md`. I did **not** install FormKit into a Vue/React project or run `npx formkit skill` against a live agent. This is the same lens applied to the aisuite (SKIP) and fast-agent (CONDITIONAL) calibration evals: decide catalog placement by whether the tool has dev-loop surface area, not by re-confirming it works as a form library (it demonstrably does, with 4.7K stars and enterprise users). No metrics below are measured.

```bash
gh api repos/formkit/formkit --jq '{stars,license,description,pushed_at,topics}'
gh api repos/formkit/formkit/readme --jq '.content' | base64 -d
gh api repos/formkit/formkit/contents/CLAUDE.md --jq '.content' | base64 -d
gh api repos/formkit/formkit/contents/packages --jq '.[].name'
gh api repos/formkit/formkit/contents/packages/cli/src/skill.ts --jq '.content' | base64 -d
gh api repos/formkit/formkit/contents/packages/cli/assets/skills/formkit/SKILL.md --jq '.content' | base64 -d
```

Reviewed: the 18-package monorepo (core/validation/rules/inputs/vue/react/nuxt/themes/zod/etc.), the `setupSkill()` installer flow and its `SUPPORTED_AGENTS` list, the `AUTO_ENABLE_FILES` mapping (`claude-code → CLAUDE.md`, `codex → AGENTS.md`), and the SKILL.md frontmatter/body.

## What worked

- **The agent integration is real, not vaporware.** `npx formkit skill` ships a properly-formed `SKILL.md` (correct frontmatter: `name` + a "Use when..." `description`) plus a docs-index reference, and auto-wires `CLAUDE.md`/`AGENTS.md` — this is a legitimate, well-built Agent Skill, broader than most libraries bother with (11 agents).
- **The library genuinely is agent-friendly by design.** The single-component API and self-structuring node tree mean less boilerplate for an LLM to get wrong; the skill steers agents toward declarative patterns and away from event-listener spaghetti, which is sound guidance.
- **Mature, maintained, well-licensed.** MIT, 4.7K stars, v2.1.0 shipped 2026-06-10, framework-agnostic core, real enterprise adoption. As a form library it is a credible choice.
- **Honest skill content.** The SKILL.md correctly flags FormKit Pro as a paid tier and notes Pro keys are client-side project keys, not server secrets — no dark-pattern upsell hidden from the agent.

## What didn't work or surprised us

- **It is a UI library you BUILD apps with — not a tool that improves the dev loop.** Like aisuite, FormKit is an application dependency. It writes no code for you, reviews no PRs, manages no context, runs no tests. Its value materializes only inside apps that happen to use FormKit forms.
- **The agent skill is library documentation, not a dev-loop capability.** The skill helps an agent use *this one library correctly* — it is conditionally useful only when your app uses FormKit. It does not generalize across the dev loop the way a review, memory, or harness tool does. Every well-documented library could (and increasingly does) ship such a skill.
- **"The form framework for coding agents" is repositioning, not a category shift.** The product, packages, and architecture are the pre-existing FormKit form library; the agent framing is marketing layered on top. The catalog's instinct that the one-liner "may be aspirational marketing" is correct — the skill is real, but the thing it serves is still a form UI library.
- **Pro tier gates premium inputs** (autocomplete, datepicker, repeater, etc.) behind `@formkit/pro` + a paid key — a normal commercial-OSS split, but worth noting the MIT core is native HTML inputs only.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Improves correctness of *form code in apps that use FormKit*, not of your dev workflow generally; out of scope like aisuite |
| Speed | neutral | Speeds up building FormKit forms specifically; no effect on the dev loop itself |
| Maintainability | neutral | Affects the maintainability of apps you build with it, not your agent setup |
| Safety | neutral | Skill correctly classifies Pro keys as client-side; no dev-loop safety surface |
| Cost Efficiency | neutral | No effect on agent token/run cost in the dev loop |

## Verdict

**SKIP**

FormKit is an excellent, mature form library and its `npx formkit skill` integration is a genuinely well-built Agent Skill — broader than most libraries ship. But within this catalog's framework (tools that move quality signals in the *dev loop*), it is the aisuite case: a library you *build applications with*, not a tool that enhances your development workflow. The agent skill is library-specific documentation that only pays off when the app you are building uses FormKit; it does not improve how a coding agent plans, implements, verifies, reviews, ships, or reflects in general. Adopt FormKit when you are building Vue/React forms and want agent-aware form scaffolding — but it does not belong in a dev-loop tooling stack. (Contrast fast-agent, which earned CONDITIONAL because it ships a runnable coding agent; FormKit ships a form library plus a skill that documents it.)

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [FormKit](https://github.com/formkit/formkit) | framework | Vue/React form library with self-structuring node tree, co-located validation, and an installable agent skill (`npx formkit skill`) | Building complex forms (validation, schema, theming) with less boilerplate, with optional agent-aware scaffolding | — (application library; no dev-loop overlap) |
