# Evaluation: Semble

**Repo:** [MinishLab/semble](https://github.com/MinishLab/semble)
**Stars:** 5,307 | **Last updated:** 2026-06-19 (pushed) | **License:** MIT | **Language:** Python (PyPI: `semble`)
**Last verified:** 2026-07-08  <!-- source-grounded re-check; not a hands-on re-verification -->
**Dev loop stage:** Code Understanding (semantic code search) — Implement
**Layer:** Tooling (MCP server / CLI / sub-agent)

---

## What it does

Semble is **a code search library built for agents** that "returns the exact code snippets they need instantly, using ~98% fewer tokens than grep+read." Claims: indexing + searching a full codebase end-to-end in **under a second**, with **~200× faster indexing and ~10× faster queries than a code-specialized transformer at 99% of its retrieval quality**, and **everything runs on CPU with no API keys, GPU, or external services.** Agents query in natural language (e.g. "How is authentication handled?") and get back only the relevant snippets. Install via `uv tool install semble` → `semble install`, which detects installed agents (Claude Code, Codex, OpenCode) and offers three integrations: **MCP server**, **instructions** (AGENTS.md/CLAUDE.md CLI guidance), or a dedicated **`semble-search` sub-agent**. From MinishLab (known for static-embedding/model2vec work).

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No index built, no queries issued, the 98%/200× claims not reproduced.

```bash
gh api repos/MinishLab/semble --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 5307, MIT, pushed 2026-06-19
gh api repos/MinishLab/semble/readme --jq '.content' | base64 -d | sed -n '229,285p'        # 98% fewer tokens, CPU-only, MCP/CLI/sub-agent install
```

## What worked

- **CPU-only, no API key, sub-second — the differentiators that matter.** The recurring friction with semantic code search is embedding infra (GPU/API keys/services); Semble removing all of it while staying fast and accurate is the strongest pitch in this crowded niche, and plausibly grounded given MinishLab's static-embedding pedigree.
- **Specific, falsifiable benchmarks.** ~98% token reduction, ~200× faster indexing, ~10× faster queries at 99% retrieval quality are concrete and testable (still vendor-reported).
- **Three clean integration shapes.** MCP, AGENTS.md instructions, or a dedicated sub-agent — `semble install` auto-detects agents and wires the chosen one.
- **Agent-native by design.** Natural-language query → exact snippets, built specifically so agents skip grep+read.
- **MIT, light footprint.** Single `uv` tool, no external dependencies.

## What didn't work or surprised us

- **Most crowded niche in the catalog.** Competes with cocoindex-code, serena, claude-context, gortex, SocratiCode, code-context-engine, sem. The wedge is *fast + accurate + zero-infra on CPU*, not a new capability.
- **Self-reported numbers.** The 98%/200×/99% figures are MinishLab's; real savings/quality depend on your repo and queries.
- **Search, not edit.** It's retrieval; unlike serena it doesn't do symbol-level refactoring — pair accordingly.
- **Index freshness.** As with any index, staleness on fast-moving repos is the standing risk (re-index cadence not evaluated here).

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Accurate semantic retrieval surfaces the right code; agent reads fewer wrong files. |
| Speed | + | Sub-second whole-repo index; ~10× faster queries — minimal latency added. |
| Maintainability | + / neutral | Self-installing integrations; another index in the stack to keep fresh. |
| Safety | + | CPU-only, no API key/external service — code never leaves the machine. |
| Cost Efficiency | + | Core pitch: ~98% fewer tokens than grep+read, and zero embedding-API cost. |

## Verdict

**CONDITIONAL** — Semble is a strong entry in the (very crowded) agent code-search field, and its differentiators are the ones that actually remove adoption friction: **CPU-only, no API key/GPU/external service, sub-second whole-repo indexing**, with claimed ~98% token savings and near-transformer retrieval quality — credible given MinishLab's static-embedding background. Adopt it when you want fast, local, zero-infra semantic code search the agent uses via MCP/sub-agent, and you'd rather not run an embedding service (cloud or GPU). Against serena (LSP edits) it's retrieval-only; against cocoindex-code (also zero-config, AST) the contest is benchmarks and embedding approach — measure both on your repo. Verify the headline numbers and watch index freshness.

Compared to neighbors: **cocoindex-code** is zero-config AST search with optional local embeddings; **serena** does LSP symbol-level find/refactor; **claude-context** uses Milvus + embeddings; **gortex**/**SocratiCode** are indexed code-intelligence engines. Semble's distinguishing pitch is **CPU-only, no-API-key, sub-second semantic code search at ~98% fewer tokens than grep+read.**

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [semble](https://github.com/MinishLab/semble) | tool | Fast, accurate code search for agents (MIT) — returns exact snippets using ~98% fewer tokens than grep+read; CPU-only, no API key/GPU/external service, sub-second whole-repo index (~200× faster indexing, ~10× faster queries than a code transformer at 99% quality); MCP / CLI / sub-agent | Agents grep and read whole files to find code, burning tokens; want instant, local, natural-language code retrieval | cocoindex-code, serena, claude-context, gortex, SocratiCode |
