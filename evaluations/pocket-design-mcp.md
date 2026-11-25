# Evaluation: pocket-design-mcp

**Repo:** [jasonmello/pocket-design-mcp](https://github.com/jasonmello/pocket-design-mcp)
**Stars:** 24 | **Last updated:** 2026-11-21 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-11-25
**Last triaged:** 2026-11-25  <!-- triaged: bulk -->
**Dev loop stage:** Implement (design-reference grounding for UI work)
**Layer:** Tooling

---

## What it does

A free MCP server (Apache-2.0) serving icons, fonts, images, components, design
tokens, easings, contrast checks, SVG tools, and patterns to coding agents.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP
that turns on redundancy with a catalogued incumbent, not on the tool's behaviour —
a question the overlap answers directly. It would not support an ADOPT, and this
eval offers none.

## Triage note

Newly discovered and catalogued today via the daily discovery pass. No STACK pick
is cited in "Overlaps with" (pressure 0) — it names `Awwards-mcp` (design
inspiration, not asset/token serving), `Figma-Context-MCP` (reads a specific Figma
file rather than serving a generic asset library), and `figma-maxxing` (also
Figma-specific), none of which is a direct duplicate of a generic icon/token/SVG
MCP server. Left at `discovery-log` for a real hands-on eval rather than a
first-day guess.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [pocket-design-mcp](https://github.com/jasonmello/pocket-design-mcp) | MCP server | Free MCP server (Apache-2.0) serving icons, fonts, design tokens, SVG tools, and contrast checks to coding agents | Coding agents building UI have no single wired-in source for icons, design tokens, or contrast/accessibility checks | Awwards-mcp, Figma-Context-MCP, figma-maxxing |
