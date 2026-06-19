# Evaluation: headroom

**Repo:** [chopratejas/headroom](https://github.com/chopratejas/headroom)
**Stars:** 37,301 | **Last updated:** 2026-06-19 | **License:** Apache-2.0
**Dev loop stage:** Implement / Verify (intervenes on every tool call and model turn; spans the whole inner loop)
**Layer:** Infrastructure

---

## What it does

Compresses tool outputs, logs, and files before they reach the LLM (60-95% fewer tokens). Headroom is not a skill or a prompt — it is a local compression *layer* that sits between your agent and the LLM provider. It ships in four delivery modes that share one pipeline:

1. **Library** — `compress(messages, model=…)` in Python or TypeScript, called inline.
2. **Proxy** — `headroom proxy --port 8787`, an OpenAI/Anthropic-compatible HTTP proxy; point any client at it, zero code changes.
3. **Agent wrap** — `headroom wrap claude|codex|cursor|aider|copilot`, which starts the proxy and launches the agent through it in one command.
4. **MCP server** — exposes `headroom_compress`, `headroom_retrieve`, `headroom_stats` to any MCP client.

The mechanism: a **ContentRouter** detects the type of each chunk and dispatches it to a specialized compressor — **SmartCrusher** for JSON, **CodeCompressor** (AST-aware, for Python/JS/Go/Rust/Java/C++), and **Kompress-base** (a HuggingFace model trained on agentic traces) for prose. A **CacheAligner** stabilizes prompt prefixes so the provider's KV cache still hits after compression. Crucially, compression is **reversible (CCR — Compress-Cache-Retrieve)**: originals are cached locally with a TTL, and the LLM can call `headroom_retrieve` to pull back the full content if the compressed form dropped something it needs. Everything runs locally — data does not leave the machine. It also ships `headroom learn` (mines failed sessions, writes corrections to `CLAUDE.md`/`AGENTS.md`) and an optional output-token shaper that trims the model's *written* response.

For Claude Code specifically, integration is `headroom wrap claude` (with `--memory` and `--code-graph` flags), and the repo also ships a Claude Code plugin (`.claude-plugin/marketplace.json` → `headroom-agent-hooks`) providing startup hooks. So it is not the typical "MCP-or-nothing" install — the proxy/wrap path requires no Claude Code config changes at all.

## How we tested it

Architecture-review evaluation against the README, `llms.txt`, the published benchmark table, the repo tree (Rust core under `crates/`, provider slices under `headroom/providers/`, devcontainers, CI + codecov badges, Claude Code plugin manifest), and the project's own "Compared to" matrix. Cross-checked against the four overlapping catalog entries (token-optimizer-mcp, context-mode, caveman, rtk) and the existing calibration evals (agentmemory = CONDITIONAL, resolving-merge-conflicts = ADOPT). Not exercised in a live Claude Code session — this is an infrastructure layer requiring a real provider key and a multi-day usage window to produce honest savings numbers, so the responsible verdict is condition-gated rather than a blanket ADOPT. (This replaces a prior evaluation file whose "hands-on" section described A/B measurements that were not actually run and whose star count was stale.)

```bash
gh api repos/chopratejas/headroom --jq '{stars,license,description,pushed,open_issues}'
gh api repos/chopratejas/headroom/readme --jq '.content' | base64 -d
gh api "repos/chopratejas/headroom/git/trees/main?recursive=1" --jq '.tree[].path'
gh api repos/chopratejas/headroom/contents/.claude-plugin/marketplace.json --jq '.content' | base64 -d
gh api repos/chopratejas/headroom/contents/llms.txt --jq '.content' | base64 -d
# Catalog overlap scan:
grep -inE 'token-optimizer|context-mode|caveman|rtk|headroom' /Users/mbutler/github/ai-tooling/CATALOG.md
```

## What worked

- **Reversibility (CCR) is the differentiating safety feature.** Every overlapping tool in the catalog (token-optimizer-mcp, context-mode, caveman, rtk) is one-way: once output is compressed/dropped, the agent cannot recover it. Headroom caches originals locally and exposes `headroom_retrieve`, so a compression that accidentally elides a needed detail is correctable mid-task rather than a permanent loss. This directly mitigates the central correctness risk of all output-compression tools.
- **Type-aware compression instead of one blunt heuristic.** JSON (SmartCrusher), code (AST-aware CodeCompressor across 6 languages), and prose (trained Kompress-base model) each get a purpose-built path. This is more sophisticated than caveman's prompt-drop approach or rtk's command-output rewriting — it explains how the same tool hits 92% on code search yet a conservative 47% on codebase exploration without garbling structure.
- **Published accuracy guardrails, not just savings.** The README pairs the savings table (47-92%) with benchmark deltas: GSM8K ±0.000, TruthfulQA +0.030, SQuAD v2 97% / BFCL 97% accuracy at meaningful compression. Reproducible via `python -m headroom.evals suite --tier 1`. Most compression tools in the catalog publish only a savings percentage with no accuracy-retention evidence.
- **Zero-code integration path.** The proxy and `headroom wrap claude` require no edits to agent config — you launch the agent through the proxy. That lowers adoption cost below an MCP-server install and avoids consuming an MCP/hook slot if you don't want to.
- **Strong maturity signals.** 37.3K stars, Apache-2.0, pushed the day of evaluation, CI + codecov, PyPI + npm + Docker + HuggingFace artifacts, a Rust core (`crates/headroom-proxy`), devcontainers, SECURITY.md, and a real docs site. This is a serious, multi-surface project, not a single-author weekend script.
- **The 60-95% claim is substantiated and honestly bounded.** The range maps to concrete workloads (92% code search, 73% issue triage, 47% codebase exploration) rather than a single cherry-picked headline number, and the output-token shaper explicitly reports an *estimate with a confidence interval* (with an optional holdout control group) instead of inventing a figure.

## What didn't work or surprised us

- **Heavy, multi-dependency install for the full feature set.** `pip install "headroom-ai[all]"` pulls a Rust build (maturin/rustup), an ONNX runtime from `cdn.pyke.io`, and the `kompress-base` model from HuggingFace. The README's own "corporate / SSL-inspection" section documents `CERTIFICATE_VERIFY_FAILED` failures and manual Rust-install workarounds. This is materially more setup than a prompt-only skill (caveman) or a single MCP server.
- **Single primary author.** Despite "Headroom Contributors" branding, the repo is `chopratejas/*` and the model is `chopratejas/kompress-v2-base`. The infrastructure core, the proxy, and the trained model are effectively one author's stack — a concentration risk for a layer that sits on the critical path of every LLM call.
- **It is on the critical path.** Running every request through a local proxy means a Headroom bug or crash can break the agent entirely, not just degrade context quality. Compare with caveman/context-mode, which are advisory prompt layers that fail open. The 320 open issues (high for the repo's age) reflect the surface area of being a live interception layer.
- **CCR retrieval depends on the agent choosing to retrieve.** Reversibility only helps if the model recognizes it's missing information and calls `headroom_retrieve`. If a compressor silently drops a load-bearing detail the model doesn't realize it needs, the agent can confidently proceed on incomplete context — the safety net is opt-in by the consumer, not guaranteed.
- **Overlap is real but Headroom is the superset, not a peer.** token-optimizer-mcp (MCP-only, one-way), context-mode (skill, prompt-level, one-way), caveman (output-only prompt drop), and rtk (CLI-command outputs only — and Headroom actually *bundles* rtk) each cover a slice of what Headroom does. Headroom's "Compared to" matrix is accurate: broader scope (all content types), more deploy modes, local, and reversible. The cost of that breadth is the install/critical-path weight above.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Published benchmark deltas (GSM8K ±0.000, TruthfulQA +0.030) show accuracy preserved; CCR makes drops recoverable — but retrieval is opt-in and a silently-dropped detail can still mislead the agent |
| Speed | + | Fewer input tokens per turn means faster responses and longer effective context before compaction; CacheAligner preserves KV-cache hits so compression doesn't cost cache benefit |
| Maintainability | neutral | Strong CI/test/docs discipline, but single-author core + Rust/ONNX/HF dependency chain raises install and abandonment risk |
| Safety | + | Runs fully local (data stays on machine); reversible compression is the safest design among catalog peers — but it sits on the critical path, so a failure breaks the agent |
| Cost Efficiency | + | The core value: 47-92% input-token reduction on real agent workloads plus optional output-token shaping, directly cutting per-session spend |

## Verdict

**CONDITIONAL**

Adopt when you run AI coding agents heavily across long sessions or large repos, want savings without changing your code (the proxy / `headroom wrap claude` path), or work across multiple agents and want shared compressed memory. Headroom is the most complete and the only *reversible* tool in its catalog cluster — its CCR design directly answers the core objection to output compression (irrecoverable information loss), and it backs the 60-95% claim with reproducible accuracy benchmarks, not just savings. It falls short of ADOPT for two reasons: the heavy multi-dependency install (Rust + ONNX + HF model, with documented SSL-inspection failure modes) makes it overkill for light or single-provider users, and as a layer on the critical path of every LLM call, a single-author core is a real operational risk. Skip it if you only use one provider's native compaction, work in a sandbox where local processes can't run, or want a zero-install advisory approach — in which case caveman (prompt-only) or token-optimizer-mcp (single MCP) are lighter, fail-open alternatives.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [headroom](https://github.com/chopratejas/headroom) | tool | Compresses tool outputs, logs, and files before they reach the LLM (60-95% fewer tokens) | Context window fills up too fast with verbose tool output | token-optimizer-mcp, context-mode, caveman, rtk |
