# Evaluation: Memory & Context cluster — claude-mem vs OMEGA

**Cluster:** Memory & Context (persistent cross-session recall)
**Contenders:** [claude-mem](https://github.com/thedotmack/claude-mem) (ADOPT, STACK pick) vs OMEGA (KEEP, retained incumbent)
**Last verified:** 2026-06-22
**Dev loop stage:** Reflect (cross-session continuity) — a memory layer spanning the whole loop rather than one stage
**Layer:** Infrastructure (a persistent store fronted by hooks/MCP tools)

---

## What it does

Both tools solve the same core problem: AI coding agents are stateless and forget everything between sessions, so each new session re-derives context, re-litigates decisions, and contradicts past conclusions. A memory layer persists decisions, lessons, and project context across session boundaries and surfaces the relevant slice back into the prompt when a new task starts.

Choosing within this cluster decides the STACK's single always-on memory substrate. The two finalists take opposite approaches:

- **claude-mem** — a native Claude Code plugin (marketplace install, zero external services) that captures session activity passively via SessionStart/PostToolUse hooks, compresses observations with the Claude Agent SDK, stores them in SQLite + Chroma, and exposes semantic search, timeline views, knowledge-graph management, and ~18 bundled skills (`make-plan`, `do`, `learn-codebase`, `pathfinder`, `weekly-digests`, etc.).
- **OMEGA** — a proprietary MCP server with a lifecycle *protocol* (`omega_welcome` → `omega_query` → `omega_store` → `omega_checkpoint`) plus coordination primitives (`[MEMORY]`/`[HANDOFF]`/`[COORD]` blocks). It is the operator's mandated, always-on incumbent — but has no public repository to inspect.

## How we tested it

**Source-grounded comparison — not a fresh hands-on A/B.** We did not run claude-mem and OMEGA side by side on the same project, did not measure recall quality, latency, or token deltas, and did not benchmark retrieval. This entry synthesizes the existing individual evaluations and the catalog verdicts along a shared dimension (transparency, capture model, friction, and verifiability), then names the STACK pick.

**Evidence:** REVIEW

Sources read and cross-referenced:

```
evaluations/mem0-vs-claude-mem.md   # claude-mem strengths/weaknesses, head-to-head table, "Keep claude-mem as primary"
evaluations/memory-systems.md       # "Recommended: claude-mem"; OMEGA "Reassess / should be downgraded"
evaluations/OMEGA.md                # "KEEP — retained incumbent, not an independently verified recommendation"
CATALOG.md (Memory & Context rows)  # OMEGA, claude-mem, agentmemory, beads overlap cluster
STACK.md (## Memory)                # claude-mem is the installed pick
```

No standalone `evaluations/claude-mem.md` exists; claude-mem's grounded findings come from `mem0-vs-claude-mem.md` and `memory-systems.md`, which both rate it the recommended memory system.

## What worked

- **claude-mem's zero-friction install and passive capture.** `mem0-vs-claude-mem.md` calls out "zero-friction install … observation-based auto-capture … you don't have to remember to save memories — the hooks do it." For a first-time adopter, friction kills adoption, and claude-mem has the least of it (a one-line marketplace install, no Docker, no API keys, no MCP config).
- **claude-mem is open and inspectable.** `memory-systems.md` flags it as the most popular by far (82.5K stars), most mature (v13), with a Chroma vector DB and tree-sitter AST exploration. Unlike OMEGA, a reader of this catalog can actually adopt, fork, and audit it.
- **OMEGA's lifecycle protocol and coordination surface.** `OMEGA.md` credits the welcome → query → store → checkpoint loop as "an opinionated discipline that makes the memory actually get used, rather than a passive KV store the agent forgets to write to," plus `[HANDOFF]`/`[COORD]` blocks for multi-agent handoffs. As the operator's mandated system it has "the strongest possible adoption signal in this catalog."

## What didn't work or surprised us

- **OMEGA has no public repo — unverifiable and unauditable.** `OMEGA.md` is blunt: "There is nothing to inspect: no source, no license terms beyond 'freemium,' no security posture, no release cadence. Every capability claim … is taken on trust." It is "the only one in the cluster you cannot read, audit, or independently verify." `memory-systems.md` reaches the same conclusion from the other side, calling for OMEGA to be "downgraded in the workflow recommendation."
- **claude-mem is Claude Code-only and resource-heavy.** `memory-systems.md` notes it "doesn't work with Cursor, Codex, Gemini," requires a Bun + uv + Node.js dependency chain, and Chroma adds ~600MB RAM. The 18 bundled skills add context overhead if you only want memory.
- **OMEGA carries lock-in and per-session overhead.** `OMEGA.md`: "Memory accreted in a proprietary store with no documented export is a switching cost that compounds," and the mandated welcome/protocol/store/checkpoint calls "spend tokens and turns every session," valuable when memory pays off but "pure overhead on short or stateless tasks."
- **Neither has been benchmarked here.** claude-mem has "no published benchmarks for retrieval quality" (`mem0-vs-claude-mem.md`); OMEGA's recall quality "is not independently benchmarked here" (`OMEGA.md`). The mem0/agentmemory neighbors are the only catalog entries with published recall numbers.

## Quality signals affected

| Signal | claude-mem | OMEGA | Comparison |
|--------|------------|-------|------------|
| Correctness | + | + / unverified | Both reduce re-litigation by recalling prior decisions; claude-mem's recall is at least inspectable, OMEGA's is taken on trust. |
| Speed | + / − | + / − | Both save re-deriving context; claude-mem's hooks add per-tool latency, OMEGA's protocol adds per-session token/turn overhead. |
| Maintainability | + | + / − | claude-mem is open and forkable; OMEGA's store is opaque and proprietary, so knowledge can't be version-controlled like docs-in-repo. |
| Safety | neutral | neutral / − | claude-mem runs locally with no external services; OMEGA is always-on ingestion with no published security model. |
| Cost Efficiency | + | neutral | claude-mem is free with no external deps; OMEGA is freemium plus per-session protocol overhead. |

## Verdict

**Winner: claude-mem (ADOPT).** It is the STACK's memory pick because it combines the lowest-friction adoption path (one-line native plugin install, zero external services), passive observation-based capture (no "remember to save" discipline required), and — decisively for a documentation catalog meant to be reproducible — an open, inspectable, forkable implementation. `mem0-vs-claude-mem.md` and `memory-systems.md` both independently land on "Recommended: claude-mem," and the latter explicitly argues OMEGA "should be downgraded" given it can't be verified.

**When the runner-up wins:** OMEGA stays as the **KEEP** fallback for anyone already invested in it — the operator runs it as the mandated, always-on coordination layer, and ripping out an accreted proprietary memory store is a real switching cost, so incumbency carries it. OMEGA also leads on the *coordination* surface (`[HANDOFF]`/`[COORD]` blocks, query-before-subagent) that claude-mem doesn't emphasize. But for a fresh adopter outside that setup, OMEGA isn't even installable — it has no public repo — so claude-mem is the actionable pick, with mem0/agentmemory as the conditional alternatives when cross-tool or benchmark-validated memory is required. Do not run two memory systems simultaneously.

## Catalog entry

n/a — this compares existing catalog entries (claude-mem, OMEGA) rather than introducing a new row.
