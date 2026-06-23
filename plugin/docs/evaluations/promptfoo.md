# Evaluation: Promptfoo

**Repo:** [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo)
**Stars:** 22,392 | **Last updated:** 2026-06-20 (pushed) | **License:** MIT | **Language:** TypeScript (npm/brew/pip)
**Dev loop stage:** Observability / Verify — LLM eval, red-teaming, CI/CD gating
**Layer:** Tooling (CLI + library + web viewer)

---

## What it does

Promptfoo is **a CLI and library for evaluating and red-teaming LLM apps** — "stop the trial-and-error approach, start shipping secure, reliable AI apps." Core capabilities: **automated evaluations** of prompts/models with declarative configs; **side-by-side model comparison** (OpenAI, Anthropic, Azure, Bedrock, Ollama, and more); **red teaming / vulnerability scanning** for AI security with a dashboard; **CI/CD integration** for automated checks; **PR code scanning** for LLM-related security/compliance issues; and result sharing. Install via `npm i -g promptfoo`, `brew install promptfoo`, `pip install promptfoo`, or `npx promptfoo@latest`. As of the README, **Promptfoo is now part of OpenAI** (remains open source, MIT) and is **used by OpenAI and Anthropic**.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No eval suite authored, no red-team scan executed.

```bash
gh api repos/promptfoo/promptfoo --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 22392, MIT, pushed 2026-06-20
gh api repos/promptfoo/promptfoo/readme --jq '.content' | base64 -d | head -75               # evals, red team, CI/CD, code scanning
```

## What worked

- **Category leader, genuinely.** 22K stars, MIT, used by OpenAI and Anthropic, now part of OpenAI — this is the de-facto open standard for LLM evals + red-teaming, not a hopeful newcomer. Its absence from the catalog was a gap.
- **Declarative, CI-native.** Configs + CLI + CI/CD integration make LLM evaluation a regression gate, not a manual spot-check — the same shift unit tests brought to code.
- **Two jobs, well-fused.** Eval (which prompt/model is better) *and* red-team/vuln-scan (is this app safe) in one tool, plus PR code-scanning for LLM security issues.
- **Provider-agnostic.** Side-by-side across OpenAI/Anthropic/Azure/Bedrock/Ollama lets you make model choices on evidence.
- **Local-first option.** Runs from the CLI against your own keys; no mandatory SaaS.

## What didn't work or surprised us

- **Scope is "LLM apps," not the coding dev loop directly.** It evaluates *the AI features you build*, not primarily *your code agent* — most relevant when you're shipping LLM-powered software, somewhat tangential to pure code authoring.
- **OpenAI ownership.** Now part of OpenAI; still MIT and open, but governance/roadmap independence is a watch-item for some.
- **Real setup for real value.** Meaningful evals need authored test cases/assertions and (for red-team) configured targets — it rewards investment, not a one-liner.
- **Cost of running evals.** Comparing models across many cases is inference spend; the value (catching regressions/vulns) usually justifies it, but it isn't free.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Automated evals catch prompt/model regressions before they ship; assertions encode expected behavior. |
| Speed | + / neutral | CI gating replaces manual eyeballing; authoring/ running large eval suites takes time + tokens. |
| Maintainability | + | Declarative configs are versioned, reviewable regression tests for AI behavior. |
| Safety | + | Red-teaming, vulnerability scanning, and PR code-scanning surface AI security/compliance issues pre-merge. |
| Cost Efficiency | neutral | Free/MIT; running evals/red-teams across providers consumes inference budget. |

## Verdict

**CONDITIONAL** — Promptfoo is the **standard open-source LLM eval + red-teaming tool** (MIT, 22K stars, used by OpenAI and Anthropic), and a clear catalog gap now filled. Adopt it whenever you ship LLM-powered features — prompts, RAG, agents — and want regression-tested, CI-gated quality plus security/red-team scanning instead of trial-and-error. It's CONDITIONAL (not unconditional ADOPT for *this* catalog) only because its primary object is *the AI app you build*, not the coding agent itself; for teams whose product includes LLM features it's close to essential. Author real test cases to get real value, and budget for eval inference.

Compared to neighbors: **langfuse** is observability/evals/prompt-management as a platform (tracing-first); **evalview** is agent regression testing via MCP. Promptfoo's distinguishing pitch is **declarative, CI-native LLM evals fused with red-teaming/vulnerability scanning — the category standard.**

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [promptfoo](https://github.com/promptfoo/promptfoo) | tool | LLM eval + red-teaming CLI/library (MIT, now part of OpenAI; used by OpenAI & Anthropic) — declarative configs to compare prompts/models side-by-side, run automated evals in CI/CD, and red-team/vulnerability-scan + PR code-scan AI apps | Prompt/model changes are trial-and-error with no regression signal, and LLM apps ship with untested security holes | langfuse, evalview |
