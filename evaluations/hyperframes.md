# Evaluation: hyperframes

**Repo:** [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes)
**Stars:** 34,025 | **Last updated:** 2026-07-10 (pushed) | **License:** Apache-2.0
**Dev loop stage:** MCP Servers (media generation, out of scope)
**Layer:** Tooling
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

An HTML-to-video pipeline built for agents — write HTML animations, render them to video — shipped
with an MCP server.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04) plus
the CATALOG one-liner and "Overlaps with" cell (`fal-ai-mcp-server`, `blender-mcp`). Sufficient for a
scope-based SKIP; not sufficient for a positive verdict, and none is offered.

## Verdict

**SKIP** — off-scope, on the same ground as `fal-ai-mcp-server` in this pass: the output is a media
asset, not code or a check on code.

Rendering HTML animations into video is production work for marketing, demos and motion graphics.
No stage of the loop this catalog maps — Plan, Implement, Verify, Review, Ship, Reflect — consumes a
video file, and an always-on MCP server is a permanent tool-surface cost for a capability that never
fires while building software.

The line is worth drawing precisely because the MCP Servers blurb is broad and several neighbours look
similar but stay. `Figma-Context-MCP` reads a design that must be *implemented in code*. `unity-mcp`
drives an editor in which software is *built*. Both feed the loop. This one terminates in an artifact
the loop does not consume.

★34K and Apache-2.0, from HeyGen, so this is a scope call and not a quality one — the HTML-as-source
approach is a genuinely clever way to make video generation diffable and reviewable, and the row stays
findable for anyone whose product needs it.

Re-open if this catalog widens to cover product asset pipelines — the same boundary that governs
`fal-ai-mcp-server` and, closer to the line, `blender-mcp`.
_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [hyperframes](https://github.com/heygen-com/hyperframes) | MCP server | Write HTML, render video (Apache-2.0, ★33K, by HeyGen) — HTML-to-video pipeline built for agents, ships an MCP server | Agents lack a direct way to render HTML animations and motion graphics into video programmatically | fal-ai-mcp-server, blender-mcp |
