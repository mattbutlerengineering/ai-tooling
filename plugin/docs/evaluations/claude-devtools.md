# Evaluation: claude-devtools

**Repo:** [matt1398/claude-devtools](https://github.com/matt1398/claude-devtools)
**Stars:** ~3,600 | **Last updated:** 2026-05-13 | **License:** MIT
**Dev loop stage:** Reflect (observability for Claude Code)
**Layer:** Tooling

---

## What it does

A visual debugging tool for Claude Code — "your Claude is coding blind; see everything it did." It reads the session transcripts/logs that Claude Code already writes to your machine and presents them in a UI so you can inspect what a session actually did.

Mechanically it parses local Claude Code logs (no external instrumentation or proxy) and surfaces: full session transcripts, individual tool calls (inputs/outputs), token usage, subagent activity, and context-window consumption. The value is post-hoc visibility — understanding why a session burned tokens, which tools or subagents ran, and where context filled up — directly from data you already have on disk.

## How we tested it

Architecture review against the README and the stated feature set (read local Claude Code logs → visual inspection of tool calls, token usage, subagents, context window). Confirmed it operates on existing on-disk transcripts with no external service or code changes. Did not run the UI against a live log directory, so condition-gated.

```bash
gh api repos/matt1398/claude-devtools --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/matt1398/claude-devtools/readme --jq '.content' | base64 -d
```

## What worked

- **Visibility from data you already have.** It reads existing Claude Code logs — zero instrumentation, no proxy, no API keys — to make opaque sessions legible. Low-friction and privacy-preserving (local).
- **The right signals.** Tool calls, token usage, subagents, and context-window consumption are exactly what you need to debug "why did this session go sideways / cost so much."
- **Purpose-built for the harness.** Unlike general LLM observability (langfuse/opik), it speaks Claude Code's session model natively.

## What didn't work or surprised us

- **Post-hoc, not live guardrails.** It explains what happened after the fact; it doesn't intervene mid-session (unlike loop/token-waste detectors).
- **Claude-Code-specific.** Tied to Claude Code's log format; not a general agent observability tool.
- **Overlaps status-line / HUD tools.** claude-hud and ccstatusline surface live session stats; claude-devtools is the deeper post-hoc transcript inspector.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Inspecting tool I/O helps diagnose wrong actions/decisions |
| Speed | + | Faster debugging of long/expensive sessions than scrolling logs |
| Maintainability | neutral | A debugging aid; doesn't change the codebase |
| Safety | + | Visibility into subagent/tool activity aids oversight |
| Cost Efficiency | + | Token-usage and context views pinpoint where spend goes |

## Verdict

**CONDITIONAL**

Adopt as a Claude Code post-hoc debugger when you want to understand token spend, tool/subagent behavior, and context-window pressure from your existing local logs — low-friction and local. It complements live status-line/HUD tools (claude-hud, ccstatusline) and general observability (langfuse/opik) rather than replacing them; reach for it when a session misbehaved and you need to see exactly what it did.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-devtools](https://github.com/matt1398/claude-devtools) | tool | Visual DevTools for Claude Code (MIT, ★3.6K) — reads local session transcripts/logs to inspect tool calls, token usage, subagents, and context-window consumption in a UI, with no external instrumentation | Claude Code runs are opaque — hard to see why a session burned tokens or which tools/subagents ran; want a local visual debugger over the logs | claude-hud, ccstatusline, langfuse, opik |
