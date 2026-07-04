# Evaluation: How Claude Code Works

**Repo:** [Windy3f3f3f3f/how-claude-code-works](https://github.com/Windy3f3f3f3f/how-claude-code-works)
**Stars:** 2,680 | **Last updated:** 2026-05-05 (pushed; created 2026-03-31) | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Reflect / Reference (understanding the tool you build with; not part of the edit-test loop)
**Layer:** Reference (documentation — 15 chapters + online docs site, bilingual 中文/English)

---

## What it does

How Claude Code Works is a **source-grounded deep dive into Claude Code's internals** — 15 thematic chapters distilled from Claude Code's ~500K-line TypeScript source, covering the agent loop, context engineering, tool system, permission/security model, and compaction pipeline. The authors' framing: Anthropic shipped 500K lines; "where do you even start reading?" — so they read it *with* Claude Code, had it write docs explaining the source, and published the result.

The content is concrete and architecture-first (with Mermaid diagrams): a `QueryEngine` → `query` main loop → Claude API → response parser → tool-execution engine (read/edit/shell/search/MCP) → results re-injected; a context layer (system prompt, git status, CLAUDE.md, compaction); and a permission layer (rule layer, **Bash AST analysis**, user confirmation). It explicitly surfaces production-grade design decisions most "demo-level" agent frameworks skip — e.g. why Claude Code *feels* fast: (1) full-pipeline streaming, (2) **tool pre-execution** (a file the model "says" it will read is already being read, hiding ~1s tool latency inside the model's 5–30s generation window), and (3) **9-stage parallel startup** (~235ms critical path). It ships a companion build-it-yourself project, **Claude Code From Scratch** (~4000 lines TS or Python, 11 chapters).

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — read, not benchmarked.** A reference resource isn't "run"; assessment is of coverage, accuracy framing, and structure from the repo (GitHub metadata, README architecture diagram + design-decision sections, the online docs TOC). Claims about Claude Code internals are the authors' analysis of the source, not independently re-verified against the source here.

```bash
gh api repos/Windy3f3f3f3f/how-claude-code-works --jq '{stars,created_at,pushed_at,license:.license.spdx_id}'
gh api repos/Windy3f3f3f3f/how-claude-code-works/readme --jq '.content' | base64 -d   # 15-chapter TOC, architecture, design decisions
```

## What worked

- **Fills a genuine gap: the *internals*, not usage.** Most Claude Code material is how-to-use; this explains how it's *built*. For anyone building an agent or trying to reason about why Claude Code behaves as it does, that's the more valuable and scarcer resource.
- **Concrete, source-derived design insights.** Tool pre-execution, full-pipeline streaming, 9-stage parallel startup, and Bash-AST-based permission analysis are real, transferable engineering patterns — not hand-wavy "agents have a loop" content.
- **Architecture-first with diagrams.** The query-loop / context / permission breakdown gives a mental model fast; ≥1 Mermaid diagram orients before the prose.
- **Build-to-understand companion.** "Claude Code From Scratch" (TS + Python, 11 chapters) turns the reading into a runnable exercise — strong pairing for actually internalizing the design.
- **MIT, popular, free, with an online docs site.**

## What didn't work or surprised us

- **Accuracy is the authors' reverse-engineering, and a moving target.** It's analysis of a specific source snapshot; Claude Code evolves continuously, so details (exact stage counts, tool totals, timings) can drift. Treat specifics as "true at time of writing," not a spec.
- **Slightly stale + primarily Chinese.** Last pushed ~6 weeks before evaluation; the primary docs are 中文 with an English README/version — fine, but the English coverage may lag the Chinese.
- **Reference, not a tool.** It improves understanding; it doesn't move correctness/speed of *your* code directly. Value is educational/architectural.
- **Unofficial.** Not an Anthropic publication — authoritative-feeling but community-authored; cross-check against official docs for anything load-bearing.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + / neutral | Understanding the agent loop, context engineering, and permission model helps you steer Claude Code and build better agents; no direct effect on your code. |
| Speed | + | Faster mental model of *why* Claude Code behaves as it does (streaming, pre-execution, compaction) than reading 500K lines yourself. |
| Maintainability | neutral | Educational; doesn't touch your codebase. |
| Safety | + / neutral | The permission/Bash-AST/confirmation chapters are genuinely useful for reasoning about agent safety design. |
| Cost Efficiency | + | Free/MIT; the compaction/context chapters inform token-efficiency decisions. |

## Verdict

**CONDITIONAL** (reference) — an excellent, scarce resource if you want to understand Claude Code's *internals* — to build your own agent, debug odd behavior, or make informed context/permission/cost decisions. The source-derived design insights (tool pre-execution, streaming pipeline, Bash-AST permissions, compaction) are real and transferable, and the "from scratch" companion makes it actionable. Caveats are inherent to the genre: it's community reverse-engineering of an evolving codebase (treat specifics as point-in-time), it's primarily Chinese, and it's a learning artifact, not a tool. Pair specifics with official docs before relying on them.

Compared to neighbors: it sits in the Reference section alongside other learning resources (e.g. karpathy-llm-wiki). Within Claude Code material, it's the **internals/architecture** complement to *usage* guides (the deferred claude-code-ultimate-guide) — read this to understand how it works, those to learn how to drive it. Its companion **claude-code-from-scratch** is the build-it variant.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [how-claude-code-works](https://github.com/Windy3f3f3f3f/how-claude-code-works) | reference | Source-grounded deep dive into Claude Code internals — 15 chapters on the agent loop, context engineering, tool system, and permission/Bash-AST security, distilled from the ~500K-line source (+ a "from scratch" build companion) | Claude Code's source is huge; want to understand how the leading coding agent actually works to build your own or use it better | karpathy-llm-wiki, claude-plugins-official |
