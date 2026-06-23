# Evaluation: gemini-cli

**Repo:** [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli)
**Stars:** 105,414 | **Last updated:** 2026-06-19 (pushed; created 2025-04-17) | **License:** Apache-2.0
**Dev loop stage:** Implement (an interactive terminal coding agent — query/edit codebases, run shell, fetch web; spills into Verify via `/review`, async PR-review skills, and CI automation, and into Plan via its `/full-context` and introspection commands)
**Layer:** Tooling (a Node.js CLI that wraps Google's Gemini models as an agentic loop with built-in tools, MCP support, and an extension/skill system) — a direct peer of Claude Code, not infrastructure or process

---

## What it does

Gemini CLI is Google's official open-source terminal coding agent — the most direct path from a terminal prompt to the Gemini 3 model family, with a 1M-token context window, Google Search grounding, file/shell/web-fetch tools, and MCP support for custom integrations. It is to Gemini what Claude Code is to Claude and qwen-code is to Qwen: a model-vendor's first-party agentic CLI. The headline pitch is a generous free tier (60 req/min, 1,000 req/day on a personal Google account) plus paid API-key / Vertex / Code Assist paths, all behind the same `npx @google/gemini-cli` entry point.

The repo is a serious monorepo, not a thin wrapper. The `packages/` tree splits into `cli` (the TUI), `core` (the agent loop and tool engine), `a2a-server` (agent-to-agent protocol server), `sdk`, `vscode-ide-companion` (IDE integration), `devtools`, and `test-utils`. It dogfoods its own extensibility: `.gemini/` ships custom slash commands (`.toml`) and a real `skills/` directory (agent-tui, async-pr-review with policy + shell scripts, behavioral-evals) — the same skill/subagent mechanism it exposes to users. Release cadence is industrial: weekly stable + weekly preview + nightly channels, latest tag `v0.47.0` (2026-06-18), shipping via npm, Homebrew, MacPorts, and conda.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No `npm install -g @google/gemini-cli`, no `npx`, no agent session, no model call. Every claim comes from GitHub metadata, the README, the recursive file tree, the `packages/` listing, and release/commit counts — not from observed coding output. The "1M context," "free tier limits," and model-quality claims are Google's README framing and product copy, not anything I measured against a task.

```bash
gh api repos/google-gemini/gemini-cli --jq '{desc,stars:.stargazers_count,forks:.forks_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'
gh api repos/google-gemini/gemini-cli/readme --jq '.content' | base64 -d | head -120
gh api "repos/google-gemini/gemini-cli/git/trees/HEAD?recursive=1" --jq '.tree[].path' | head -40
gh api repos/google-gemini/gemini-cli/contents/packages --jq '.[].name'   # a2a-server cli core devtools sdk test-utils vscode-ide-companion
gh api repos/google-gemini/gemini-cli/releases/latest --jq '{tag:.tag_name,date:.published_at[0:10]}'  # v0.47.0 / 2026-06-18
gh api repos/google-gemini/gemini-cli --jq '.open_issues_count'   # 1355
```

## What worked

- **First-party, well-funded, and maintained.** 105K stars, 14.1K forks, Apache-2.0, a Google-owned monorepo with weekly+nightly release trains and dedicated SDK/IDE/A2A packages. This is the lowest-bus-factor entry in the Implement category's "alternative coding CLI" cluster — qwen-code, DeepSeek-Reasonix, and oh-my-pi do not have this backing.
- **Genuinely generous free tier.** 1,000 req/day on a personal Google account is the strongest no-credit-card on-ramp of any first-party agent CLI, which matters for evaluation, low-budget projects, and avoiding metered API spend on routine work.
- **Real extensibility, dogfooded.** MCP support plus a native skills/subagents/custom-slash-command system that the repo itself uses (`.gemini/skills/async-pr-review`, `behavioral-evals`). It is not a closed black box; you can shape it the way you shape Claude Code.
- **1M-token context window.** For whole-repo reasoning, large-PDF/codebase ingestion, and long sessions, the context ceiling is materially higher than most peers and is the clearest reason to reach for it over Claude Code on a specific task.
- **Multimodal Implement.** "Generate apps from PDFs, images, or sketches" and Google Search grounding give it a Plan/Implement capability surface that text-only CLIs lack.

## What didn't work or surprised us

- **It is a full alternative harness, not an add-on to your existing one.** Adopting gemini-cli means running a *second* coding agent alongside Claude Code, with its own config, skills, and muscle memory. The catalog's center of gravity is Claude Code; gemini-cli is a fork-in-the-road, not a layer — the same CONDITIONAL caveat that applies to qwen-code and opencode.
- **Model lock-in to Gemini.** Unlike claude-code-router (route any model through one harness) or goose (model-agnostic platform), gemini-cli is Gemini-only. Its value rises and falls with how good Gemini 3 is for *your* code, which this inspection did not test.
- **Free-tier data and rate realities.** The generous free tier runs through consumer Google auth; rate limits (60/min) throttle heavy agentic loops, and free-tier usage typically carries data-use terms distinct from paid API/Vertex. Teams with code-confidentiality requirements must use the paid/Vertex path, eroding the free-tier advantage.
- **1,355 open issues.** Fast-moving, high-volume project; the nightly/preview cadence implies regressions are expected and pushed to users to surface. Pin to `@latest` (stable), not nightly, for real work.
- **Quality is unmeasured here.** Stars and Google's backing say nothing about whether Gemini produces better diffs than Claude on *your* repo. The neighbors (qwen-code, opencode) are CONDITIONAL precisely because "is it better than Claude Code for this task?" is the only question that matters, and it is answered per-task, not per-repo-star.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral / + | A capable first-party agent with 1M context and search grounding can be strong on whole-repo and research-heavy tasks; but correctness vs. Claude Code is model-dependent and untested here. |
| Speed | + | `npx` zero-install start, weekly releases, and a free tier remove friction; large context means fewer chunking round-trips on big codebases. Offset by 60 req/min throttling under heavy agentic loops. |
| Maintainability | neutral | Acts on your code like any agent; no inherent effect on your codebase's maintainability. Running two competing harnesses adds config-maintenance overhead for you. |
| Safety | − / neutral | Built-in shell + file-write tools carry the usual agent blast-radius risk; free-tier consumer auth carries data-use terms unsuitable for confidential code (use Vertex/paid). 1,355 open issues signal churn. |
| Cost Efficiency | + | Best-in-class free tier (1,000 req/day) for a first-party agent; can offload routine work off metered Claude/API budgets. Paid/Vertex tiers are standard token pricing. |

## Verdict

**CONDITIONAL — adopt as a second, Gemini-native CLI for big-context and free-tier work; not a replacement for your primary harness.** gemini-cli is the most credible, best-resourced "alternative coding agent CLI" in this catalog: Google-owned, Apache-2.0, weekly-released, genuinely extensible, with a 1M-token window and the strongest free tier of any first-party agent. But adopting it means running a parallel harness locked to Gemini, with its own config and skills, and its real coding quality versus Claude Code is per-task and untested in this inspection. Reach for it specifically when you want whole-repo/large-context reasoning, search-grounded answers, multimodal input, or zero-cost routine runs — and keep your primary harness for everything else.

Compared to neighbors: it lands in the same CONDITIONAL bucket as **qwen-code** (Qwen-native) and **opencode** (open alternative to Claude Code), but is better backed and better maintained than either, and far higher-resourced than **DeepSeek-Reasonix** or **oh-my-pi**. Unlike **claude-code-router** (route any model through Claude Code's harness) and **goose** (model-agnostic platform), gemini-cli is single-vendor — pick router/goose if model flexibility is the goal, pick gemini-cli if Gemini 3 + 1M context + free tier is the goal.

## Catalog entry

**Target category:** Implement

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [gemini-cli](https://github.com/google-gemini/gemini-cli) | platform | Google's official open-source terminal coding agent — Gemini 3, 1M-token context, search grounding, MCP + skills, generous free tier | Want a first-party, well-maintained coding-agent CLI with large context and a no-credit-card free tier as an alternative or complement to Claude Code | qwen-code, opencode, goose (alternative coding-agent CLIs); claude-code-router (model-flexible alternative) |
