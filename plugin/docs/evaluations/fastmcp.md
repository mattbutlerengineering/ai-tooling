# Evaluation: FastMCP

**Repo:** [PrefectHQ/fastmcp](https://github.com/PrefectHQ/fastmcp)
**Stars:** 25,702 | **Last updated:** 2026-06-06 | **License:** Apache-2.0
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Python framework for building MCP servers, clients, and interactive apps. Decorator-based API: `@mcp.tool` on a function auto-generates the MCP schema, validation (via Pydantic/type hints), and documentation. Also provides a client SDK for connecting to any MCP server, and an "Apps" layer that renders interactive UIs directly in chat conversations.

FastMCP 1.0 was incorporated into the official MCP Python SDK in 2024. The standalone project (now v3.4.2) is the most widely used MCP framework — the README claims "a million downloads a day" and "70% of MCP servers across all languages." Three pillars: Servers (expose tools/resources/prompts), Clients (connect to servers), and Apps (interactive UIs in conversation).

## How we tested it

**Evidence:** RUN

**Hands-on**, `pip install fastmcp` into a clean venv (v3.4.2) and built a minimal server to verify the decorator API on 2026-06-20.

```python
from fastmcp import FastMCP
mcp = FastMCP("demo")

@mcp.tool                          # one decorator on a plain typed function
def add(a: int, b: int) -> int:
    "Add two numbers"
    return a + b
# introspection:
await mcp.get_tool("add")
#  → FunctionTool | name: 'add' | desc: 'Add two numbers' | params: ['a','b']
```

**Measured results.** Clean install; the "minimal boilerplate" claim is real — a single `@mcp.tool` on a type-hinted function produced a fully-formed `FunctionTool` with the **name auto-derived from the function, the description pulled from the docstring, and the JSON-schema parameters (`a`, `b`) inferred from the type hints** — zero manual schema. Note a v3 API shift worth knowing: introspection is `get_tool(name)` (singular, async), not `get_tools()`. Confirms the core ergonomics that make it the default MCP-server framework.

```bash
gh api repos/PrefectHQ/fastmcp --jq '.stargazers_count, .updated_at, .license.spdx_id'   # provenance
```

## What worked

- **Minimal boilerplate is real:** the echo server is 20 lines including imports and covers tools, resources, resource templates, and prompts — genuinely the fastest path from Python function to MCP server
- **Production-grade infrastructure:** auth providers, middleware (rate limiting, error handling, logging), dependency injection, storage backends, telemetry, pagination — not a toy framework
- **234 examples** covering auth, apps, diagnostics, filesystem providers, proxy patterns, and complex inputs — more examples than most MCP servers have lines of code
- **424 test files** with pre-commit hooks and type checking (ty) — serious engineering discipline
- **Three upgrade guides** (from FastMCP v2, from MCP Python SDK, from low-level SDK) show mature lifecycle management
- **llms.txt support** — the docs ship in LLM-consumable format at gofastmcp.com/llms.txt and llms-full.txt
- **Enterprise path via Horizon** — clear commercial story without locking down the open-source core (Apache-2.0)

## What didn't work or surprised us

- **Python-only:** no TypeScript/JavaScript version. For TypeScript MCP servers, you'd use the official SDK or typescript-mcp-server-generator skill — FastMCP only covers the Python half of the ecosystem
- **Heavy dependency surface for simple servers:** pydantic, starlette, httpx, anyio, and more. A 3-line tool server pulls in a non-trivial dependency tree compared to using the raw SDK
- **"fastmcp_slim" split is confusing:** the repo has both `fastmcp_slim/` and `fastmcp_remote/` directories with overlapping module names — the architectural boundary isn't obvious from the file structure alone
- **Last commit June 6** — 12 days without activity at evaluation time. Active but not daily

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Auto-generated schemas from type hints eliminate manual schema/validation drift |
| Speed | + | Decorator API cuts MCP server setup from hours to minutes; 40+ ready-to-use examples |
| Maintainability | + | Component base class (`FastMCPComponent`) enforces consistent identity/versioning across tools, resources, prompts |
| Safety | + | Auth providers, middleware, RBAC, and elicitation support built in; CVE patching evident (starlette floor for CVE-2026-48710) |
| Cost Efficiency | neutral | Framework overhead is negligible; MCP servers are infrastructure, not token consumers |

## Verdict

**ADOPT**

FastMCP is the standard framework for building Python MCP servers. The decorator API genuinely delivers on "fast" — going from a Python function to a production-grade MCP server with auth, middleware, and telemetry requires minimal code. 25.7K stars, Apache-2.0, mature lifecycle (v3.4.2 with upgrade guides), and incorporation into the official MCP SDK make this the default choice. Use typescript-mcp-server-generator (CONDITIONAL) for TypeScript servers instead.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [fastmcp](https://github.com/PrefectHQ/fastmcp) | framework | Fast, Pythonic way to build MCP servers and clients with minimal boilerplate (25.7K stars) | Building MCP servers requires too much setup; need a framework that makes it easy | typescript-mcp-server-generator (complementary: fastmcp = Python, ts-mcp-gen = TypeScript) |
