# Evaluation: briefing

**Repo:** [JacobHayes/briefing](https://github.com/JacobHayes/briefing)
**Stars:** 0 | **Last updated:** recent (exact push date not captured from the repo page; checked 2026-09-04) | **License:** MIT
**Last verified:** 2026-09-04
**Last triaged:** 2026-09-04  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

CLI + MCP server for coding agents (Claude Code, Codex, Pi, or any MCP-speaking agent). When an agent has something too long or too layered for a chat reply, it opens a paced browser view instead — one idea per screen, inline comments, context panels, and decisions with recommendations — then returns the human's feedback to the agent.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. Source-grounded only, from the repo's own README description. Not enough for a positive verdict, and none is offered.

## Triage note

Left at `discovery-log`. Zero overlap pressure (P3 backlog) — no existing entry's "Overlaps with" cell cites it. Conceptually closest to `humanlayer` (human-in-the-loop approval) and `mcp-ui` (rendering interactive surfaces from an MCP server), but distinct in mechanism (a dedicated paced browser review UI rather than an approval SDK or generic UI renderer). Brand new (★0); leaving for a real eval to judge whether the review-surface angle is differentiated enough to matter.

_Triaged 2026-09-04 by the P3 backlog band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [briefing](https://github.com/JacobHayes/briefing) | MCP server | Opens a paced browser view (MIT) for anything too long or layered for a chat reply — one idea per screen, inline comments, context panels, decisions with recommendations — then returns the human's feedback to the agent | Long or multi-part agent output/decisions get skimmed or lost in a chat reply; want a real review surface a human can annotate before replying | humanlayer, mcp-ui, DesktopCommanderMCP |
