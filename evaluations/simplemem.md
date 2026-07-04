# Evaluation: SimpleMem

**Repo:** [aiming-lab/SimpleMem](https://github.com/aiming-lab/SimpleMem)
**Stars:** 3,521 | **Last updated:** 2026-05-21 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Reflect
**Layer:** Infrastructure

---

## What it does

SimpleMem is an efficient lifelong memory system for LLM agents, originating as an academic project (arXiv 2601.02553, plus EvolveMem and Omni-SimpleMem papers from the same lab). Its core thesis is *semantically lossless compression*: instead of passively accumulating raw conversation history or running expensive filtering loops, it distills interactions into compact, self-contained memory units (resolved coreferences, absolute timestamps), synthesizes related context within a session to remove redundancy at build time, and uses intent-aware retrieval planning to assemble a precise context at query time. The repo bundles three pillars under one `simplemem` PyPI package: **SimpleMem** (text, the efficiency core), **Omni-SimpleMem** (multimodal — text/image/audio/video), and **EvolveMem** (a closed-loop AutoResearch process that self-evolves the retrieval configuration). Storage is LanceDB (vectors) + SQLite, embeddings default to Qwen3-Embedding, and an OpenAI-compatible LLM is required for compression, synthesis, and answer generation.

For agent integration there are three channels, with very different maturity:
- **Python API** (`from simplemem import SimpleMem`) — the full, first-class surface (text + multimodal + `optimize()`).
- **MCP server** — a standalone multi-tenant **text-only** service, cloud-hosted at `mcp.simplemem.cloud` or self-hosted via Docker. Targets Claude Desktop, Cursor, LM Studio, Cherry Studio, "any MCP client." Multimodal and `optimize()` over MCP are on the roadmap, not shipped.
- **Claude Skill** (`SKILL/simplemem-skill`) — a self-contained skill that shells out to a Python CLI (`cli_persistent_memory.py add/query/retrieve`). It is **manual**: the model invokes `add`/`query` explicitly. There are **no hooks** — no `SessionStart`/`Stop`/auto-capture. The `cross/` package adds session-lifecycle + automatic context injection + observation extraction, but that lives behind the Python/REST API, not the shipped Claude Skill.

## How we tested it

**Evidence:** REVIEW

Architecture review via the GitHub API — read the main README, `MCP/README.md`, `cross/README.md` (the Claude-Mem comparison), `SKILL/README.md`, and `SKILL/simplemem-skill/SKILL.md`, plus the recursive file tree, release list, and repo metadata. **Did not install or run hands-on.** Rationale matches the prior memory-category evals (memsearch, agentmemory): the user already runs claude-mem (ADOPT) + OMEGA, and SimpleMem requires standing up an OpenAI-compatible API key plus either a Docker MCP service or a Python-CLI skill — installing a competing memory layer risks conflicting with the live setup. Compared against `evaluations/memsearch.md` (CONDITIONAL), `evaluations/agentmemory.md` (CONDITIONAL), and claude-mem (ADOPT, the user's choice).

```bash
gh search repos SimpleMem --limit 20 --json fullName,description,stargazersCount,url   # disambiguate the name
gh api repos/aiming-lab/SimpleMem --jq '{description,stars:.stargazers_count,license:.license.spdx_id,pushed_at,created_at,open_issues}'
gh api repos/aiming-lab/SimpleMem/readme --jq '.content' | base64 -d
gh api "repos/aiming-lab/SimpleMem/git/trees/main?recursive=1" --jq '.tree[].path'
gh api repos/aiming-lab/SimpleMem/contents/cross/README.md --jq '.content' | base64 -d
gh api repos/aiming-lab/SimpleMem/contents/SKILL/simplemem-skill/SKILL.md --jq '.content' | base64 -d
gh api repos/aiming-lab/SimpleMem/releases --jq '.[].tag_name'   # v0.3.0 latest; 13 contributors
```

Repo identity confirmed: the catalog name "SimpleMem" disambiguates against many unrelated repos (Cnblogs themes, .NET membership libs, a C# memory manipulator). The only AI-agent memory tool is `aiming-lab/SimpleMem` (3.5K stars, MIT, PyPI `simplemem`, arXiv-backed).

## What worked

- **Strong, published benchmark story.** Three arXiv papers and reproducible benchmark runners (`test_locomo10.py`, EvolveMem/OmniSimpleMem runners against LoCoMo / MemBench / Mem-Gallery). Headline claims: SimpleMem +26.4% avg F1 on LoCoMo with ~30x fewer inference tokens; Omni-SimpleMem F1=0.613 on LoCoMo; EvolveMem +25.7% relative. This is rigorous compared to most catalog memory tools and on par with agentmemory's benchmark discipline.
- **Token-efficiency is the genuine differentiator.** The "semantically lossless compression" pipeline (structured compression + online synthesis + intent-aware retrieval) is a real, papers-backed mechanism aimed squarely at Cost Efficiency — the ~30x token-consumption reduction is the thing this tool is actually about, and it is distinct from claude-mem/memsearch/agentmemory's "capture everything + hybrid search" approach.
- **Multimodal memory (Omni-SimpleMem)** — image/audio/video memory with entropy-driven selective ingestion and cross-modal KG reasoning. No other catalog memory entry (claude-mem, memsearch, agentmemory, OMEGA) does multimodal. Unique axis.
- **Self-evolving retrieval (EvolveMem)** — an LLM-driven Evaluate→Diagnose→Propose→Guard loop that tunes retrieval config offline, with automatic rollback on regression. Novel; nothing else in the category self-tunes retrieval.
- **Clean composition discipline.** `cross/` extends the base "byte-identical" via composition rather than modification, and includes 3-tier secret redaction + provenance tracking (each memory links to source evidence).
- **MIT license, PyPI distribution, Docker compose, multilingual docs, 13 contributors.** Reasonable engineering surface for a lab project.

## What didn't work or surprised us

- **The Claude-Code integration is the weakest channel, by the project's own roadmap.** The MCP server is **text-only**, **multi-tenant**, and oriented at Claude *Desktop*/Cursor, not Claude Code hooks. The Claude Skill is **manual CLI shell-outs with no auto-capture hooks** — the model must remember to call `add`/`query`. claude-mem (ADOPT), memsearch, and agentmemory all auto-capture via hooks; SimpleMem's shipped Claude surface does not. The good stuff (auto context injection, observation extraction in `cross/`) is gated behind the Python/REST API.
- **No zero-key local path.** An OpenAI-compatible LLM API key is **required** before any memory construction or retrieval — initialization fails without it. claude-mem, memsearch (ONNX bge-m3 local), and agentmemory (SQLite + local MiniLM) all run with **no cloud key**. This is a real Safety/Cost regression for a local-first user: every memory op (compress, synthesize, answer) is a paid LLM call.
- **The "+64% vs Claude-Mem" claim is self-reported and apples-to-oranges.** `cross/README.md` shows SimpleMem 48 vs Claude-Mem 29.3 on "LoCoMo Score" (and the badge confusingly labels it "64% *faster*" while the table measures a quality score). It is the authors' own harness against their own corpus — the same caveat applied to agentmemory's self-comparisons. Not independent verification, and not a reason to displace the ADOPTED tool.
- **Cloud MCP funnel.** The headline integration is a hosted service (`mcp.simplemem.cloud`) with token auth — sending memory off-box unless you self-host the Docker variant. Comparable to memsearch's Zilliz Cloud steering.
- **Young and pre-1.0.** Created Jan 2026, latest release v0.3.0, 15 open issues. Far less battle-tested than claude-mem; the multi-pillar package (text + omni + evolve, recently merged into one import) is still settling.
- **Heavier conceptual + dependency footprint** for a Claude Code user: LanceDB + SQLite + Qwen embeddings + an LLM key + (for the good features) a Docker service or Python env — to solve a problem the ADOPTED tool already solves with a plugin install.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Papers-backed +26.4% F1 on LoCoMo via compression + intent-aware retrieval; but benchmarks are self-reported and the Claude Skill recall path is manual, not auto-captured |
| Speed | + | ~30x token reduction and parallel build/retrieval modes; intent-aware planning keeps context compact |
| Maintainability | neutral | LanceDB + SQLite with clean composition in `cross/`, but pre-1.0 multi-pillar package and a manual-CLI Claude Skill add operational overhead |
| Safety | - | No local-only path — every memory op needs an OpenAI-compatible LLM key; default integration is a cloud MCP service (off-box memory) unless self-hosted |
| Cost Efficiency | neutral | Per-token efficiency is excellent (the whole point), but every capture/recall is a paid LLM call vs free local-embedding peers — net wash for a solo user |

## Verdict

**CONDITIONAL**

SimpleMem is a credible, papers-backed memory system whose real, unique value is *token-efficient compression* and *multimodal + self-evolving retrieval* — axes no other catalog memory entry covers. Use it when those specifically matter: you need image/audio/video memory, you want a benchmarked compression-first memory layer for a Python agent, or you're building a multi-tenant memory service (the MCP server is genuinely built for that). For this user's case — Claude Code, local-first, already on claude-mem (ADOPT) — it does **not** displace claude-mem: SimpleMem's shipped Claude surface is the weakest of its three channels (text-only MCP aimed at Claude Desktop, or a manual no-hooks CLI skill), it mandates a paid LLM API key with no local fallback (a regression vs claude-mem/memsearch/agentmemory's free local embeddings), and its "+64% vs Claude-Mem" headline is a self-reported, mislabeled benchmark. Like memsearch and agentmemory (both CONDITIONAL), it wins on a specific axis (here: compression efficiency + multimodality) but loses to claude-mem on Claude Code ecosystem fit, auto-capture, and zero-key local operation. It is **not** a thinner duplicate of those CONDITIONALs — it attacks a different problem (compression/token-cost, plus multimodal) rather than competing on hybrid-search recall — which earns the CONDITIONAL over a SKIP. KEEP the catalog entry; do not adopt over claude-mem.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [SimpleMem](https://github.com/aiming-lab/SimpleMem) | tool | Token-efficient lifelong memory for LLM agents via semantically lossless compression; text + multimodal, with self-evolving retrieval | Agent memory is redundant and token-hungry; need compact, benchmarked recall (incl. image/audio/video) across sessions | claude-mem, memsearch, agentmemory, mem0, OMEGA |
