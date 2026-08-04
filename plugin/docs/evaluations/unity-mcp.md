# Evaluation: unity-mcp

**Repo:** [CoplayDev/unity-mcp](https://github.com/CoplayDev/unity-mcp)
**Stars:** 12,282 | **Last updated:** 2026-07-06 (pushed) | **License:** MIT
**Dev loop stage:** MCP Servers (game engine)
**Layer:** Tooling
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

Bridges an AI assistant to the Unity Editor — manage assets and scenes, edit scripts, automate
editor tasks.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04) plus
the CATALOG one-liner and "Overlaps with" cell (`blender-mcp`, `chrome-devtools-mcp`,
`DesktopCommanderMCP`). Enough to place it; not enough for a positive verdict, and none is offered.

## Triage note

Left at `discovery-log`, and deliberately kept out of this pass's media-generation sweep.

`fal-ai-mcp-server` and `hyperframes` were SKIPped here because their output *is* the artifact —
images, video — and nothing in the dev loop consumes it. unity-mcp is on the other side of that line:
Unity is an environment in which software is written, and driving its editor to manage scenes, assets
and scripts is Implement-stage work with C# underneath it. Game development is software development.

The condition on its value is the usual vendor-integration shape — everything to a Unity team, nothing
to anyone else — which is why it is neither ADOPT-everywhere nor SKIP.

★12.3K and MIT with recent activity. The interesting unexamined question is whether the editor bridge
gives the agent enough *feedback* to verify its own changes, or whether it can only act blindly — the
same gap `plumb-mcp` closes for Figma, and the difference between a useful loop and an expensive one.

No eval file existed before this pass; this stub is the placeholder, not an evaluation.
_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [unity-mcp](https://github.com/CoplayDev/unity-mcp) | MCP server | Bridges AI assistants to the Unity Editor — manage assets, scenes, scripts, automate tasks (MIT, ★11K) | Want an agent to drive the Unity Editor instead of manual asset/scene/script work | blender-mcp, chrome-devtools-mcp, DesktopCommanderMCP |
