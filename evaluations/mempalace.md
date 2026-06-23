# Evaluation: MemPalace

**Repo:** [MemPalace/mempalace](https://github.com/MemPalace/mempalace)
**Stars:** ~56,000 (very high for a ~2-month repo; ~7.3K forks, reported as-is) | **Last updated:** 2026-06-19 (pushed; created 2026-04-05) | **License:** MIT | **Package:** PyPI `mempalace`
**Dev loop stage:** Memory & Context (local-first memory layer)
**Layer:** Infrastructure (local store + pluggable backend)

---

## What it does

MemPalace is a **local-first AI memory** system whose distinguishing choice is **verbatim storage** — it stores conversation history as exact text and retrieves it with semantic search, and explicitly **does not summarize, extract, or paraphrase.** It claims **96.6% R@5 (raw) on LongMemEval with zero API calls**, a pluggable backend, and runs fully local. It targets Claude Code session retention (it ships guidance/hooks for auto-saving sessions before the 30-day expiry).

Notably, the README carries a prominent **security caution**: MemPalace's only official sources are its GitHub repo, the `mempalace` PyPI package, and `mempalaceofficial.com`; other lookalike domains are flagged as impostors that "may distribute malware." That's both a supply-chain warning to heed and a signal the project is popular enough to be impersonated.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No package installed, no memory stored or retrieved, benchmark not reproduced. The R@5 figure and star/fork counts are reported verbatim and unverified. Per its own warning, only the official GitHub/PyPI sources should ever be used.

```bash
gh api repos/MemPalace/mempalace --jq '{stars,forks,license:.license.spdx_id,pushed:.pushed_at}'   # ~56K, MIT
gh api repos/MemPalace/mempalace/readme --jq '.content' | base64 -d | head -25   # verbatim storage, local-first, LongMemEval claim, impostor warning
```

## What worked

- **Verbatim, lossless storage is a real differentiator.** Most memory layers summarize/extract (and can drop or distort facts); storing exact text and retrieving by semantics avoids paraphrase-induced loss — a meaningfully different trade-off.
- **Local-first, zero-API.** No external calls for storage/retrieval is strong for privacy and cost, and removes a network dependency from the memory hot path.
- **Benchmark-forward.** Citing LongMemEval R@5 (raw) is more falsifiable than vague "smart memory" claims (still vendor-reported).
- **Pluggable backend + MIT,** with explicit Claude Code retention guidance.

## What didn't work or surprised us

- **Anomalous popularity.** ~56K stars on a repo created two months ago is extraordinary; forks scale with it (~7.3K), which is more reassuring than the hermes-agent pattern, but treat the numbers as hype signals, not a quality guarantee.
- **Impostor/malware ecosystem.** The need for a prominent "only these sources are official" warning means lookalike sites exist — install **only** from the official GitHub/PyPI, and verify before running.
- **Verbatim storage has costs.** Storing everything raw grows unbounded and shifts the burden to retrieval quality; it's a different scaling profile than summarizing memories.
- **Crowded niche.** Competes with supermemory, mem0, cognee, claude-mem; differentiation is verbatim + local + zero-API, not a new category.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Verbatim storage avoids paraphrase/extraction loss; high claimed recall keeps the right context retrievable. |
| Speed | + | Local, zero-API retrieval avoids network round-trips. |
| Maintainability | neutral | Pluggable backend; verbatim store grows unbounded and needs retention/hooks management. |
| Safety | + / − | Local-first keeps data on-box (good); the impostor-site/malware risk means install hygiene matters. |
| Cost Efficiency | + | Zero API calls for memory ops; storage is cheap-ish but unbounded. |

## Verdict

**CONDITIONAL** — MemPalace is a local-first, MIT, **verbatim** memory layer (no summarize/extract) with a strong claimed LongMemEval recall and zero API calls — a genuinely different, privacy-friendly trade-off from the summarizing memory tools, and well-suited to Claude Code session retention. Adopt it if you want lossless, on-box memory and value the benchmark posture, but: install **only** from the official GitHub/PyPI (the project warns of malware-bearing impostor sites), treat the ~56K-star count as hype rather than proof, and plan for unbounded verbatim growth. Pilot recall on your own data before relying on it.

Compared to neighbors: **supermemory** is a benchmark-leading full context stack; **mem0** a relationship-aware layer; **cognee** a knowledge-graph memory; **claude-mem** a turnkey CC plugin. MemPalace's distinguishing pitch is **verbatim, local-first, zero-API memory** with a recall benchmark.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [MemPalace](https://github.com/MemPalace/mempalace) | tool | Local-first AI memory (MIT) — verbatim storage (no summarize/extract/paraphrase) + semantic retrieval, pluggable backend, zero API calls, claims 96.6% R@5 on LongMemEval; ⚠️ install only from official GitHub/PyPI (impostor sites flagged) | Summarizing memory layers lose/distort facts and call external APIs; want lossless, on-box, zero-API recall | supermemory, mem0, cognee, claude-mem |
