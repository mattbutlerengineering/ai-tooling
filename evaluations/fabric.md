# Evaluation: Fabric

**Repo:** [danielmiessler/Fabric](https://github.com/danielmiessler/Fabric)
**Stars:** 42,466 | **Last updated:** 2026-06-09 | **License:** MIT
**Dev loop stage:** Cross-cutting (general AI tasks; a thin slice touches Implement/Review/Ship)
**Layer:** Tooling (standalone CLI), not a coding-agent extension

---

## What it does

Catalog framing: Fabric is "an open-source framework for augmenting humans using AI," a modular system that organizes a crowdsourced set of reusable AI prompts ("patterns") run from a CLI, REST API, or other tools.

Mechanically, Fabric is a single Go binary (`fabric`) plus a library of 255 Markdown "patterns" under `data/patterns/` — each pattern is a `system.md` prompt for one real-world task (e.g. `summarize`, `extract_wisdom`, `analyze_claims`, `write_essay`, `create_visualization`). You pipe input into the CLI and select a pattern: `pbpaste | fabric --pattern summarize`. Fabric handles the model backends itself (Anthropic, OpenAI, Ollama, Azure, Gemini, Bedrock, GitHub Models, and many more via vendor plugins), so it is its own end-to-end harness, not something layered onto an existing coding agent. It also exposes a REST API server with Swagger docs and ships helper apps (web UI, browser extension). The mission framing is explicitly broad — "human flourishing via AI augmentation" — and the pattern library reflects that: writing, research, security analysis, learning, wellness, and visualization patterns dominate; software-development patterns are a small minority.

## How we tested it

Repo and source inspection via the GitHub API — README, release notes, and the `data/patterns/` listing. Did not install the binary, configure a model backend, or run a pattern. Fabric is a standalone general-purpose AI CLI with its own provider config and model keys; it is not a Claude Code plugin/skill/MCP server, so there is nothing to install *into* the dev loop to evaluate, and a hands-on run would only exercise it as a separate AI app. Findings rest on metadata, the README, and the actual pattern inventory.

```bash
gh api repos/danielmiessler/fabric --jq '{full_name,description,stargazers_count,language,license:.license.spdx_id,pushed_at}'
gh api repos/danielmiessler/fabric/readme --jq '.content' | base64 -d   # README
gh api repos/danielmiessler/fabric/contents/data/patterns --jq '[.[].name] | length'   # 255 patterns
gh api repos/danielmiessler/fabric/contents/data/patterns --jq '[.[].name] | map(select(test("code|review|commit|git|bug|debug|test|software|develop|refactor|security|api|technical")))[]'
```

Pattern inventory: 255 total. Software-dev-relevant patterns are a thin slice — roughly a dozen, including `coding_master`, `create_coding_feature`, `create_coding_project`, `create_git_diff_commit`, `summarize_git_changes`, `summarize_git_diff`, `review_code`, `explain_code`, `generate_code_rules`, `create_security_update`. The overwhelming majority of the library is non-coding (summarization, extraction, writing, analysis, research, learning, wellness).

## What worked

- **Large, curated, reusable prompt library.** 255 task-scoped patterns under MIT license, usable independently of the binary ("just use the patterns") — a credible source to mine individual prompts from, e.g. `review_code` or `create_git_diff_commit`.
- **Very high maturity and velocity.** 42K+ stars, active releases through 2026 (current Anthropic SDK, Opus 4.7 with 1M context, OpenAI Codex backend), broad multi-provider support, REST API with Swagger, i18n across 10 languages.
- **Provider-agnostic harness.** Swap model backends via vendor plugins; not locked to one provider.
- **A handful of genuine dev-loop patterns exist** — `create_git_diff_commit`, `summarize_git_diff`, `review_code`, `explain_code` map onto Implement/Review/Ship if extracted as prompts.

## What didn't work or surprised us

- **It is a general-purpose AI-task framework, not a coding dev-loop tool.** The mission is "augmenting humans" broadly; coding patterns are ~12 of 255. The center of gravity is summarize/extract/analyze/write, not write-code/review-PR/ship.
- **No Claude Code integration whatsoever.** No plugin, skill, MCP server, or hook. It is a separate CLI with its own model config and keys, living entirely outside the agent's dev loop — same posture that put aisuite at SKIP.
- **It is itself a harness/agent, so it overlaps the agent, not extends it.** Running `fabric --pattern review_code` is a parallel AI invocation outside the session, not something that improves work done inside Claude Code.
- **The valuable dev slice is just prompts.** The dev-loop value is a few extractable Markdown prompts, not the framework — and the catalog already has skills/plugins that do commit-message, code-review, and explain-code natively inside the loop.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | A general AI CLI run alongside the agent; doesn't change correctness of work produced in the dev loop. |
| Speed | neutral | Separate CLI invocation; no acceleration of the in-session dev loop. |
| Maintainability | neutral | No integration with dev-workflow tooling; patterns are static prompts. |
| Safety | neutral | Runs its own model calls outside the agent; no guardrails added to the dev loop. |
| Cost Efficiency | neutral | Provider-swapping helps Fabric's own runs, not agent-session token spend. |

## Verdict

**SKIP** (with a narrow CONDITIONAL note)

Fabric is an excellent, very popular, well-maintained general-purpose AI-augmentation framework — but it is a standalone CLI/harness for arbitrary AI tasks, not a tool that lives in or improves a coding dev loop. Its 255-pattern library is overwhelmingly non-coding, it has zero Claude Code integration, and where it does touch development it is itself a parallel agent rather than an enhancement to the one you already run. In this catalog's framework (tools that move quality signals inside the dev loop) it has no integration surface — the same reasoning that put aisuite and other general-agent frameworks at SKIP.

The narrow CONDITIONAL angle: a few MIT-licensed patterns (`create_git_diff_commit`, `review_code`, `explain_code`, `summarize_git_diff`) are worth mining as prompt sources for an existing skill/command — but that is harvesting prompts, not adopting the framework. Re-evaluate only if Fabric ships a first-class Claude Code skill/MCP server that brings its patterns into the session.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Fabric](https://github.com/danielmiessler/Fabric) | framework | Open-source CLI + library of 255 crowdsourced AI "patterns" (prompts) for general real-world tasks | Useful AI prompts are scattered and hard to reuse across tools; Fabric organizes them by task behind one CLI/API | aisuite |
