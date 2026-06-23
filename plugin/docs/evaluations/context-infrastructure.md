# Evaluation: context-infrastructure

**Repo:** [grapeot/context-infrastructure](https://github.com/grapeot/context-infrastructure)
**Stars:** 609 | **Last updated:** 2026-06-16 | **License:** MIT (stated in README; GitHub API returns no detected license file)
**Dev loop stage:** Reflect
**Layer:** Infrastructure

---

## What it does

A reference implementation of a "context infrastructure" for AI coding agents — persistent memory, personal rules, reusable skills, and scheduled (cron-driven) observations — extracted from a system its single author ran for roughly a year. The README is explicit that this is **not an installable tool but a blueprint**: clone it, open the directory in Claude Code / OpenCode / Cursor, and you can feel the "with context vs without context" difference, but making the AI truly *yours* requires accumulating your own behavioral data over time — "no shortcuts."

The mechanism, as documented in `AGENTS.md` (the root router the agent reads every session) and `periodic_jobs/ai_heartbeat/docs/PRD.md` (the memory design doc):

- **Three-layer memory.** **L3** = global hard constraints — every file under `rules/` (`SOUL.md` identity, `USER.md` your profile, `COMMUNICATION.md` style, `WORKSPACE.md` routing index, plus 43 decision `axioms/` and 25+ `skills/`), passively loaded each session. **L1/L2** = a dynamic observation log at `contexts/memory/OBSERVATIONS.md`, which the agent *pulls* from on demand rather than having pushed into context.
- **Pull-not-push / progressive disclosure.** The PRD's core thesis: the global memory pool grows unbounded as plain-text append, but any given task only needs a sparse slice, so the agent retrieves relevant L1/L2 observations by tag/keyword instead of loading everything.
- **Agentic heartbeat (the auto-accumulation engine).** `periodic_jobs/ai_heartbeat/src/v0/observer.py` (daily) and `reflector.py` (weekly) are meant to run under cron. The observer does NOT pre-assemble a prompt; it runs `find -mtime -1`, hands the agent the changed-file list, and lets an OpenCode-Builder session autonomously read/filter/summarize into tagged observations (`🔴 High` methodology, `🟡 Medium` project state, `🟢 Low` task log) appended to `OBSERVATIONS.md`. The weekly reflector is "garbage collection": drop stale 🟢, merge same-topic 🟡, promote shared lessons to 🔴.
- **Memory is Markdown, git-versionable.** No database for the memory pool itself.
- **Optional Tier-2 semantic search.** `tools/semantic_search/` is a separate forward-index search: `embedding.py` calls an OpenAI-compatible embeddings endpoint (defaults to a *local* LM Studio server at `localhost:1234`, model `text-embedding-qwen3-embedding-8b`), and `index.py` stores embeddings as `embeddings.npy` + `chunks.pkl` + `manifest.json` on disk with `fcntl` file locking and mmap — i.e. a flat numpy/pickle index, no vector DB.

## How we tested it

**Evidence:** REVIEW

**Architecture review via the GitHub API — did NOT install or run hands-on.** This matches every prior Memory & Context eval (claude-mem ADOPT; agentic-stack, memsearch, agentmemory, SimpleMem all CONDITIONAL): the user already runs claude-mem + OMEGA as the live memory stack, and this repo's whole premise is that it only delivers value once you spend months accumulating your *own* data — there is nothing to "try" in a single session that would produce honest evidence. The repo was UNLINKED in the catalog, so step one was verifying identity.

```bash
gh search repos context-infrastructure --limit 20 --json fullName,description,stargazersCount,url
gh api repos/grapeot/context-infrastructure --jq '{stars:.stargazers_count,license:.license.spdx_id,description,pushed_at,created_at,forks:.forks_count}'
gh api repos/grapeot/context-infrastructure/readme --jq '.content' | base64 -d
gh api repos/grapeot/context-infrastructure/contents/AGENTS.md --jq '.content' | base64 -d
gh api repos/grapeot/context-infrastructure/contents/periodic_jobs/ai_heartbeat/docs/PRD.md --jq '.content' | base64 -d
gh api repos/grapeot/context-infrastructure/contents/tools/semantic_search/search/embedding.py --jq '.content' | base64 -d
gh api repos/grapeot/context-infrastructure/contents/tools/semantic_search/search/index.py --jq '.content' | base64 -d
gh api repos/grapeot/context-infrastructure/contents/.env.example --jq '.content' | base64 -d
gh api repos/grapeot/context-infrastructure/contributors --jq 'length'   # → 1
gh api repos/grapeot/context-infrastructure/releases --jq 'length'       # → 0
```

**Repo identity confirmed.** `gh search repos context-infrastructure` returns several "context"-named projects (skaldlabs/skald, context-space, ultracontext, RetainDB, etc.). Only `grapeot/context-infrastructure` matches the catalog's Memory & Context framing — its description is verbatim "A context and memory system for AI coding agents. Persistent memory, personal rules, skills, and scheduled observations" (609 stars, 152 forks, README declares MIT). This is the correct repo; the catalog entry should link to it. Note: the API reports `license: null` and no `LICENSE` file is detected — only the README footer says "MIT."

## What worked

- **The conceptual model is genuinely strong and well-articulated.** The pull-not-push / progressive-disclosure thesis (sparse, high-density context retrieved on demand instead of stuffing everything into the window) and the L3/L1/L2 split are a clean, defensible memory architecture, documented in a real PRD rather than marketing copy.
- **Memory is plain-text Markdown, git-versionable, no DB lock-in** — the same human-readable, "your memory is your asset" philosophy that earned claude-mem/memsearch/agentic-stack praise. `OBSERVATIONS.md` is append-only text.
- **The agentic heartbeat is a clever auto-accumulation design.** The script provides only file paths + a goal; the agent decides what to read, spawns sub-agents (librarian/explore), filters noise (e.g. checks blog metadata dates to skip pure reformat churn), and the weekly reflector actively does GC/promotion. This is a more autonomous capture loop than a fixed summarizer.
- **Local-first semantic search with no vector DB.** The optional Tier-2 index defaults to a *local* LM Studio embeddings server and stores a flat numpy + pickle index with file locking — no cloud account required for the search path, lighter than memsearch's Milvus.
- **Multi-harness aware.** `AGENTS.md` is the OpenCode/Cursor-style router, and the skill-ecosystem install protocol explicitly says "start from your workspace AGENTS.md or CLAUDE.md" — so it is harness-portable in principle.

## What didn't work or surprised us

- **It is explicitly a reference implementation, not a tool — by the author's own framing.** The README leads with "这不是开箱即用的工具" (this is not an out-of-the-box tool) and warns there are "no shortcuts": value only materializes after you spend months collecting your own behavioral data. That makes it categorically different from the ADOPT/CONDITIONAL tools, which deliver value the moment they're installed.
- **It is OpenCode-centric, not Claude Code-native.** The heartbeat engine talks to a local **OpenCode Server** (`OPENCODE_API_URL`, `opencode_client.py`), `AGENTS.md` documents OpenCode `subagent_type` routing and `multi_tool_use.parallel`, and the memory PRD names "OpenCode-Builder" as the memory producer. The Claude Code path is "open the folder" — there are no Claude Code plugin/hooks/MCP integration, unlike claude-mem, memsearch, or agentic-stack's adapter.
- **Single author, zero releases, much of the content is non-transferable.** 1 contributor, 0 releases (the 152 forks are template clones, not collaboration). The README's own three-layer caveat says the 43 axioms and the skills' specific content are "可参考，不能复制" (reference only, not copyable) — they encode one person's year, not reusable infrastructure.
- **Heavy, sprawling external-dependency surface.** `.env.example` wants Gmail app passwords, an OpenCode server URL, Google Analytics 4, Kit/ConvertKit, Typefully session tokens, Gemini/OpenAI keys — because the periodic jobs include newsletter publishing, social posting, and analytics. That is the author's personal automation suite, not memory infrastructure, and most of it is irrelevant noise for a coding-agent memory use case.
- **The docs and seed content are largely in Chinese.** The README, PRD, AGENTS.md prose, and axioms are predominantly Chinese — a real adoption-friction for an English-first workflow, and a sign of how personal/single-author the repo is.
- **No published retrieval benchmarks** — recall quality is unverifiable from sources, same gap as memsearch/agentic-stack.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + (in theory) | L1/L2 observations surface past decisions/fixes into future sessions; but recall is keyword/tag-based, no benchmark, and the value depends on long-term self-accumulated data |
| Speed | neutral | Heartbeat clustering runs off-session via cron; local numpy/embedding search is fast — but it is not wired into Claude Code, so no per-turn effect for this user |
| Maintainability | + | Markdown source-of-truth, git-versionable, no DB lock-in; offset by sprawling .env deps and personal, non-transferable content |
| Safety | neutral | Local-first memory + local embedding default; but pulls in many third-party credentials (Gmail/GA4/Kit/Typefully/Gemini) for non-memory jobs, widening the secret surface |
| Cost Efficiency | + | No vector DB, local embeddings, plain-text store; the periodic agentic jobs do incur LLM calls but run off the interactive path |

## Verdict

**SKIP**

`grapeot/context-infrastructure` is a thoughtful, well-documented **blueprint** for an agent context/memory system — its pull-not-push / progressive-disclosure thesis and L3/L1/L2 Markdown memory model are sound and worth reading for ideas. But it is, by the author's own explicit statement, a **reference implementation, not an installable tool**: it ships one person's year of non-transferable axioms/skills, is **OpenCode-centric with no Claude Code plugin/hook/MCP integration**, has a single contributor and zero releases, and drags in a large, personal external-credential surface (Gmail, GA4, Kit, Typefully, Gemini) for newsletter/social/analytics jobs that have nothing to do with memory. For this user — Claude Code-first, already running claude-mem (ADOPT) + OMEGA — there is no installable artifact to adopt and the value only appears after months of bespoke data collection. Unlike memsearch and agentic-stack (CONDITIONAL — credible *tools* that win on a specific axis), this is a thin/ambiguous fit as a tool, which per the calibration leans SKIP. The catalog entry should be **linked to the verified repo and reclassified** as a *reference* blueprint rather than an installable tool. Mine it for the progressive-disclosure idea; do not install it.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [context-infrastructure](https://github.com/grapeot/context-infrastructure) | reference | Reference blueprint of a year-old agent context/memory system: 3-layer Markdown memory (rules + observations), personal axioms/skills, cron heartbeat observer/reflector | Shows what a mature pull-not-push, progressive-disclosure agent memory architecture looks like end-to-end — as a blueprint to learn from, not a tool to install | claude-mem, memsearch, agentic-stack, agentmemory, OMEGA, mem0 |
