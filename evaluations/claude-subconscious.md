# Evaluation: claude-subconscious

**Repo:** [letta-ai/claude-subconscious](https://github.com/letta-ai/claude-subconscious)
**Stars:** 2,796 | **Last updated:** 2026-06-18 | **License:** MIT
**Dev loop stage:** Reflect
**Layer:** Infrastructure

---

## What it does

A background agent (built on the Letta Code SDK) that watches Claude Code sessions, reads your codebase, builds memory, and "whispers" guidance back before each prompt. Unlike file-based memory tools (claude-mem, CLAUDE.md rules), this is a second agent running underneath — it has tool access (Read, Grep, Glob, WebSearch) and processes the full transcript after each response. Memory is stored in a Letta server (cloud or self-hosted), not in local files.

The mechanism: four hooks fire at session lifecycle points. `SessionStart` notifies the Letta agent and syncs memory blocks. `UserPromptSubmit` syncs updated memory. `PreToolUse` injects mid-workflow updates. `Stop` sends the full transcript asynchronously (120s timeout). The Letta agent then reads relevant files, updates its memory, and on the next prompt, its guidance appears as `<letta_message>` XML blocks in stdout — injected into context without writing to CLAUDE.md.

Supports two modes: `whisper` (default, messages only) and `full` (memory blocks + diffs). One agent can serve multiple Claude Code sessions in parallel via Letta Conversations, with shared memory across all of them. Multi-project support via per-directory `LETTA_AGENT_ID` overrides.

## How we tested it

**Evidence:** REVIEW

Architecture review and README analysis. Not installed locally (requires Letta API key and cloud account). Examined hooks.json, package.json (v2.1.1, depends on `@letta-ai/letta-code-sdk` and `tsx`), and repo structure.

```bash
gh api repos/letta-ai/claude-subconscious --jq '.stargazers_count, .updated_at, .license.spdx_id'
gh api 'repos/letta-ai/claude-subconscious/contents/hooks/hooks.json' --jq '.content' | base64 -d
gh api 'repos/letta-ai/claude-subconscious/contents/package.json' --jq '.content' | base64 -d
```

## What worked

- **Background agent model is genuinely novel** — this isn't just a memory store, it's a second agent with tool access that explores your codebase and builds context while you work. No other catalog entry does this.
- **Minimal integration surface** — four hooks, one SDK dependency. Doesn't touch CLAUDE.md, doesn't modify agent behavior directly. Clean separation of concerns.
- **Multi-session shared memory** — one Letta agent serves all your Claude Code sessions with unified memory. No per-session fragmentation.
- **Progressive guidance** — memory blocks on first prompt, diffs on subsequent ones. Avoids dumping full context every time.
- **Well-engineered README** — clear architecture diagrams, mode documentation, debugging instructions, multi-project setup guide.

## What didn't work or surprised us

- **Requires Letta Cloud account or self-hosted server** — not local-first. The free tier may be sufficient for individual use, but this is a vendor dependency that claude-mem doesn't have.
- **Explicitly marked "not intended for production"** — the README banner says to use Letta Code instead, positioning this as a demo app. This undermines confidence for serious adoption.
- **No local fallback** — if Letta API is down or key expires, memory is completely unavailable. claude-mem stores everything locally.
- **Cold start problem** — README admits "it takes a few sessions before it has enough signal." During that ramp-up, it's just adding hook latency with no benefit.
- **Token cost opacity** — the background agent consumes LLM tokens on the Letta side to process transcripts. There's no visibility into what this costs or how to control it.
- **Async transcript delivery with 120s timeout** — large sessions may not fully sync if the Letta agent takes too long to process.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + (potential) | Background agent can surface forgotten context and patterns, reducing repeated mistakes |
| Speed | neutral | Hook latency on every prompt; benefit only materializes after several sessions |
| Maintainability | neutral | Doesn't write to codebase files; memory is external |
| Safety | neutral | No security scanning or safety features |
| Cost Efficiency | - | Adds token consumption on Letta side for every session transcript; no cost controls |

## Verdict

**CONDITIONAL**

Use when you want a persistent, cross-session memory agent that actively explores your codebase — and you're comfortable with a Letta Cloud dependency. The background agent model is genuinely differentiated from file-based memory (claude-mem) and key-value stores (server-memory), but the "not for production" banner and cloud dependency limit the audience. If Letta Code (the full product) ships a stable equivalent, re-evaluate. For teams already using Letta, this is a natural extension. For everyone else, claude-mem (ADOPT) covers the memory need with local-first simplicity.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-subconscious](https://github.com/letta-ai/claude-subconscious) | plugin | Give Claude Code a subconscious — persistent state across sessions | Want transparent persistent state without explicit memory commands | claude-mem, OMEGA |
