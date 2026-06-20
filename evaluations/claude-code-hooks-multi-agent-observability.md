# Evaluation: claude-code-hooks-multi-agent-observability

**Repo:** [disler/claude-code-hooks-multi-agent-observability](https://github.com/disler/claude-code-hooks-multi-agent-observability)
**Stars:** ~1,470 | **Last updated:** 2026-02-08 | **License:** none specified
**Dev loop stage:** Reflect (observability for Claude Code)
**Layer:** Infrastructure

---

## What it does

A real-time observability system for Claude Code agents, built on Claude Code's **hook events**. It captures, stores, and visualizes hook events so you can monitor multiple concurrent agents — tracing every tool call, task handoff, and agent lifecycle event across a parallel swarm.

The architecture (per the README) is a clean reference pipeline: **Claude agents → hook scripts → HTTP POST → Bun server → SQLite → WebSocket → Vue client**. Hook scripts fire on Claude Code lifecycle/tool/subagent events and POST them to a Bun server that persists to SQLite and pushes live updates over WebSocket to a Vue dashboard, with session tracking, event filtering, and live updates. It's positioned for multi-agent orchestration — watching teams of specialized agents working in parallel.

## How we tested it

Architecture review against the README and the documented pipeline (hooks → Bun+SQLite → WebSocket → Vue). Confirmed the hook-event-capture model and the multi-agent/swarm tracing focus. Note: **no license is specified** and the last push is ~2026-02 — it reads as a reference/demo system (from a well-known Claude Code educator) more than a maintained product. Not run live, so condition-gated.

```bash
gh api repos/disler/claude-code-hooks-multi-agent-observability --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/disler/claude-code-hooks-multi-agent-observability/readme --jq '.content' | base64 -d
```

## What worked

- **Hooks as the capture mechanism.** Using Claude Code's native hook events to trace tool calls, handoffs, and lifecycle is the right, low-coupling approach — no agent modification needed.
- **Multi-agent swarm focus.** Live tracing across parallel agents (sessions, filtering, real-time) addresses a real gap as multi-agent orchestration grows.
- **Clean, copyable architecture.** The hooks→Bun→SQLite→WebSocket→Vue pipeline is a clear reference you can learn from or adapt.

## What didn't work or surprised us

- **No license + demo cadence.** Absence of a license is a real adoption blocker, and the ~2026-02 last push + educational origin suggest a reference implementation, not a supported product.
- **Self-hosted stack to run.** It's a multi-service system (Bun server, SQLite, Vue client) you stand up yourself — more than a drop-in.
- **Overlaps claude-devtools/claude-hud.** Those inspect single-session logs; this one's edge is live, multi-agent swarm tracing via hooks.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Live tracing of tool calls/handoffs helps diagnose multi-agent behavior |
| Speed | + | Real-time visibility shortens debugging of parallel runs |
| Maintainability | neutral | A reference system you self-host; not a maintained product |
| Safety | + | Visibility into swarm tool use/handoffs aids oversight |
| Cost Efficiency | + | Free/OSS, local stack; no per-event service cost |

## Verdict

**CONDITIONAL**

Useful when you run multi-agent Claude Code swarms and want live tracing of tool calls, handoffs, and lifecycle via native hooks — and as a clean reference architecture for building your own. Treat it as a reference/demo: clarify the missing license before relying on it, and expect to self-host the stack. For single-session post-hoc inspection, claude-devtools is lighter; this one's value is the live, multi-agent view.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-code-hooks-multi-agent-observability](https://github.com/disler/claude-code-hooks-multi-agent-observability) | tool | Real-time multi-agent observability for Claude Code (no explicit license, ★1.5K) — hook scripts POST lifecycle/tool/subagent events to a Bun+SQLite server, visualized live in a Vue client; trace every tool call, task handoff, and agent lifecycle across a parallel swarm | Parallel multi-agent Claude Code runs are opaque; want live tracing of tool calls, handoffs, and agent lifecycle across the swarm | claude-devtools, claude-hud, langfuse, harbor |
