# Evaluation: ag-ui

**Repo:** [ag-ui-protocol/ag-ui](https://github.com/ag-ui-protocol/ag-ui)
**Stars:** ~14,300 | **Last updated:** 2026-06-20 | **License:** MIT
**Dev loop stage:** Reference (protocol / Implement when integrating)
**Layer:** Infrastructure

---

## What it does

AG-UI ("Agent-User Interaction Protocol") is an open, lightweight, event-based protocol that standardizes how AI agents connect to user-facing applications — the UI-layer counterpart to MCP (agent↔tools) and A2A (agent↔agent).

Mechanically, AG-UI defines a standard stream of events that an agent backend emits and a frontend consumes, so agents can surface real-time state, streaming output, tool activity, and user context to a UI without bespoke per-framework wiring. You scaffold an app with `npx create-ag-ui-app`, and the project provides framework integrations plus an interactive "Dojo" for exploring the protocol. It's stewarded in the CopilotKit ecosystem and designed for simplicity and flexibility so any agent framework or frontend can implement it.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README and the protocol's stated purpose (event-based standard for agent↔frontend interaction), the `create-ag-ui-app` scaffold, and the framework-integration/Dojo resources. Placed it in Reference as a protocol standard (peer to MCP/A2A) rather than a runnable tool. Not implemented in a live app, so condition-gated.

```bash
gh api repos/ag-ui-protocol/ag-ui --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/ag-ui-protocol/ag-ui/readme --jq '.content' | base64 -d
```

## What worked

- **Fills a real gap in the protocol stack.** MCP standardized tools and A2A standardized agent-to-agent; AG-UI standardizes agent-to-UI, which has been bespoke per framework. A shared event protocol is genuinely useful.
- **Low-friction start + ecosystem.** `create-ag-ui-app`, a Dojo, and existing framework integrations make adoption concrete, not just spec reading.
- **Permissive and vendor-neutral-ish.** MIT, framework-agnostic by design — implementable by any agent/frontend.

## What didn't work or surprised us

- **Standards need adoption to matter.** Value scales with how many frameworks/frontends speak it; it's promising but newer than MCP.
- **Not for the Claude Code dev loop directly.** This is for builders shipping agent-powered *user-facing apps* — relevant as reference/architecture knowledge, not a tool you run while coding.
- **CopilotKit gravity.** Stewardship sits largely in one ecosystem; watch for truly multi-vendor governance.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | A protocol; correctness depends on implementations |
| Speed | + | Event streaming standardizes real-time UI updates from agents |
| Maintainability | + | One protocol replaces bespoke per-framework agent↔UI glue |
| Safety | neutral | Transport/interaction standard; not a safety mechanism |
| Cost Efficiency | neutral | Open protocol; no direct cost effect |

## Verdict

**CONDITIONAL**

Reach for AG-UI when you're building user-facing applications that embed agents and want a standard, event-based way to stream agent state to the frontend instead of bespoke wiring. As reference knowledge it rounds out the agent-protocol picture (MCP for tools, A2A for agents, AG-UI for UIs). Adoption breadth is the variable to watch; for in-IDE coding workflows it's architectural context, not a daily tool.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ag-ui](https://github.com/ag-ui-protocol/ag-ui) | reference | Agent-User Interaction Protocol (MIT, ★14K, by CopilotKit) — open, lightweight, event-based protocol standardizing how agents stream state and interact with front-end apps in real time; `npx create-ag-ui-app`, framework integrations, a Dojo | Wiring agents into UIs is bespoke per framework; want a standard event protocol for agent↔frontend interaction (the UI peer to MCP/A2A) | 12-factor-agents, MCP (ext.), A2A (ext.) |
