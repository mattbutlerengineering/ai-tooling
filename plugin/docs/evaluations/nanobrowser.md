# Evaluation: Nanobrowser

**Repo:** [nanobrowser/nanobrowser](https://github.com/nanobrowser/nanobrowser)
**Stars:** 13,329 | **Last updated:** 2025-11-24 (pushed) | **License:** Apache-2.0 | **Language:** TypeScript (Chrome extension)
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Verify — AI web automation in the browser
**Layer:** Tooling (Chrome extension)

---

## What it does

Nanobrowser is **an open-source AI web-automation tool that runs in your browser** — a free alternative to OpenAI Operator, installed as a **Chrome extension**. It uses a **multi-agent system** (specialized agents collaborate on complex web workflows) driven through an **interactive side panel** with real-time status. Key positioning: **100% free** (BYO API keys, pay only your own usage), **privacy-focused** (everything runs in your local browser; credentials stay local, never sent to a cloud service), **flexible LLM options** (OpenAI, Anthropic, Gemini, Ollama, Groq, Cerebras, Llama, and custom OpenAI-compatible — different models per agent), and **fully open source**.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No extension installed, no web task automated.

```bash
gh api repos/nanobrowser/nanobrowser --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 13329, Apache-2.0, pushed 2025-11-24
gh api repos/nanobrowser/nanobrowser/readme --jq '.content' | base64 -d | head -30               # Operator alternative, multi-agent, local browser, BYO-LLM
```

## What worked

- **Free, local Operator alternative.** Premium web-automation (à la OpenAI Operator) without the $200/mo and without sending credentials to a cloud — runs in *your* browser with *your* keys. That privacy + cost stance is the core appeal.
- **Multi-agent + per-agent models.** Specialized agents collaborating, each on a model you choose, is more flexible than a single monolithic web agent.
- **Browser-extension delivery.** Lives where you already are (Chrome), with an interactive side panel and real-time status — low friction for ad-hoc web tasks and verification.
- **Broad BYO-LLM support + Apache-2.0.** OpenAI/Anthropic/Gemini/Ollama/Groq/etc. and a permissive license.
- **Strong traction.** 13.3K stars.

## What didn't work or surprised us

- **Push cadence is the main caveat.** Last push **2025-11** (~7 months before this writing) — not archived, but not keeping pace with the fast-moving browser-agent field; verify current behavior/models before relying on it.
- **In-browser agent ≠ headless/CI automation.** It drives your interactive Chrome session; great for hands-on tasks, but not the same as scripted, headless, CI-friendly automation (agent-browser/playwright).
- **Trust surface.** An extension that drives your logged-in browser with your credentials is powerful and sensitive — local, but high-trust by nature.
- **Crowded browser-agent space.** Overlaps browser-use, agent-browser, page-agent, playwright; the wedge is "free local Operator alternative as a multi-agent Chrome extension."

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + / neutral | Multi-agent web automation can complete real authenticated tasks; reliability is model/site-dependent. |
| Speed | + | Automates repetitive web workflows directly in the browser via a side panel. |
| Maintainability | neutral | Extension is easy to install; project's recent cadence is a watch-item. |
| Safety | − / neutral | Drives your logged-in browser with your credentials (local, but high-trust); privacy-positive vs. cloud Operators. |
| Cost Efficiency | + | Free, BYO-keys — pay only your own model usage, no subscription. |

## Verdict

**CONDITIONAL** — Nanobrowser is a popular, Apache-2.0 **free, local, multi-agent web-automation Chrome extension** — a privacy-preserving OpenAI-Operator alternative where everything runs in your browser with your own keys. Adopt it for **hands-on, interactive web automation and verification** (authenticated flows, repetitive web tasks) when you want to avoid Operator's subscription and cloud credential handling. It's CONDITIONAL because the project's last push is ~7 months old (verify current behavior), it's an interactive in-browser agent rather than headless/CI automation, and driving your logged-in browser is a high-trust capability. For scripted/CI browser testing in the dev loop, agent-browser/playwright fit better; Nanobrowser is for interactive, local, free web tasks.

Compared to neighbors: **browser-use** is an autonomous web agent (framework); **agent-browser** is a CLI for agent browser automation; **page-agent** is in-page NL control of your own web app; **playwright** automates a controlled browser. Nanobrowser's distinguishing pitch is **a free, local, multi-agent Chrome extension that replaces paid web Operators.**

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [nanobrowser](https://github.com/nanobrowser/nanobrowser) | tool | Open-source AI web-automation Chrome extension (Apache-2.0) — a free OpenAI-Operator alternative with a multi-agent system, runs in your local browser (credentials stay local), BYO-LLM (OpenAI/Anthropic/Gemini/Ollama/Groq…), interactive side panel | Want autonomous in-browser task automation without a $200/mo Operator subscription or sending credentials to the cloud | browser-use, agent-browser, page-agent, playwright |
