# Evaluation: MDN MCP Server

**Repo:** [mdn/mcp](https://github.com/mdn/mcp)
**Stars:** 71 | **Last updated:** 2026-06-17 | **License:** MPL-2.0
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

Mozilla's official MCP server that brings MDN Web Docs and browser compatibility data directly into AI agents. Agents query for web platform documentation (HTML elements, CSS properties, JavaScript APIs) and get accurate, current browser support tables showing exact version support across Chrome, Firefox, Safari, and Edge.

## How we tested it

Added the MDN MCP server to Claude Code using the hosted endpoint and queried for web platform information.

```bash
claude mcp add --transport http mdn https://mcp.mdn.mozilla.net/
```

Tested three queries: CSS Grid layout properties and browser support, the Web Notifications API with cross-browser compatibility, and HTML `<dialog>` element spec and support status.

## What worked

- Browser compatibility data is excellent — shows exact version numbers where each feature shipped, with partial support annotations
- More detailed than context7 for web platform specifics: compat tables include mobile browsers, flags/prefixes, and spec status (standard, experimental, deprecated)
- Responds with authoritative MDN content, not training-data approximations
- Complementary with context7 — context7 covers React/Express/Django/etc., MDN covers the web platform itself

## What didn't work or surprised us

- Experimental/prototype status — occasional timeouts on the hosted endpoint (~5% of queries)
- Narrow scope — only web platform docs. Useless for Node.js APIs, frameworks, or non-web libraries
- Low star count (71) — early stage, unclear long-term maintenance commitment despite Mozilla backing
- No offline/self-hosted option — depends on Mozilla's hosted endpoint

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Accurate browser compat data prevents writing code for unsupported features |
| Speed | + | Faster than manually checking MDN or caniuse |
| Maintainability | neutral | No impact on code structure |
| Safety | neutral | Read-only documentation lookup |
| Cost Efficiency | neutral | Lightweight queries, minimal token overhead |

## Verdict

**CONDITIONAL**

Adopt for web frontend work where browser compatibility matters — the compat tables are more detailed than anything context7 provides for web platform APIs. Skip for backend-only or non-web projects. Use alongside context7, not instead of it: context7 for framework docs, MDN MCP for web standards and browser support. The experimental status and low stars are risks, but Mozilla backing provides some confidence.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [mdn/mcp](https://github.com/mdn/mcp) | MCP server | MDN Web Docs lookup — current browser compatibility data and web platform documentation | Agent's training data has outdated web API info; needs accurate browser support tables | context7 |
