# Evaluation: fastapi-mcp

**Repo:** [tadata-org/fastapi_mcp](https://github.com/tadata-org/fastapi_mcp)
**Stars:** 11,920 | **Last updated:** 2025-11-24 (pushed; created 2025-03-08) | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Outer-loop Ship/Infrastructure — it is a build-time library for *producing* an MCP server from an existing FastAPI app, not a tool you run inside the dev loop. Its output (the MCP endpoint) is then consumed by agents during Plan/Implement.
**Layer:** Tooling — a Python package (`pip install fastapi-mcp` / `uv add`) that mounts an MCP server onto a FastAPI application. It generates infrastructure; it is not itself a workflow step or agent.

---

## What it does

FastAPI-MCP turns the endpoints of an existing **FastAPI** application into **MCP tools**, so an AI agent can call your API as native tools. The headline pitch is minimal config: `mcp = FastApiMCP(app); mcp.mount()` and the auto-generated MCP server is live at `/mcp` on the same app. The selling point over a generic "OpenAPI → MCP" converter is that it is **FastAPI-native**: it reuses your existing FastAPI `Depends()` for **authentication/authorization**, preserves your request/response **Pydantic schemas** and endpoint **documentation** (the same info Swagger shows), and talks to your app over **ASGI** directly — no HTTP round-trip from the MCP layer back into your own API.

Deployment is flexible: mount the MCP server onto the same app, or run it as a separate service (`04_separate_server_example.py`). The `examples/` directory walks the surface — basic usage, full schema descriptions, custom exposed-endpoint filtering, separate-server deployment, tool re-registration, and a custom MCP router. Documentation is substantial (`docs/` with getting-started, auth, ASGI, transport, deploy, customization, tool-naming, FAQ, best-practices), and there is a managed hosted option at tadata.com. Requires Python 3.10+ and uv.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No `uv add fastapi-mcp`, no FastAPI app instrumented, no MCP server mounted, no agent connected to a generated `/mcp` endpoint. Every claim is from the repository (GitHub metadata, README, recursive file tree, `examples/` and `docs/` listings), not from observed behavior. The "zero/minimal configuration," "preserves schemas," and "auth built in" claims are README framing, unverified here. No latency, schema-fidelity, or auth-correctness numbers were measured.

```bash
gh api repos/tadata-org/fastapi_mcp --jq '{desc,stars:.stargazers_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'
gh api repos/tadata-org/fastapi_mcp/readme --jq '.content' | base64 -d   # README
gh api "repos/tadata-org/fastapi_mcp/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api repos/tadata-org/fastapi_mcp/releases --jq 'length'   # 10 tagged releases (PyPI)
gh api repos/tadata-org/fastapi_mcp/commits  --jq 'length'   # 30 (page-1 cap)
```

## What worked

- **Right primitive for the FastAPI crowd.** If your service is already FastAPI, exposing it to agents is two lines. The mount-on-same-app default removes the usual MCP-server scaffolding entirely.
- **Auth via existing `Depends()` is the standout.** Reusing FastAPI dependency injection for authn/authz means MCP tools inherit the API's existing security posture rather than bolting on a new, separately-secured surface — a meaningfully better default than naive OpenAPI→MCP converters.
- **ASGI transport, not HTTP-to-self.** Calling the app through its ASGI interface avoids the MCP layer making real HTTP calls back into the same process — less overhead, fewer moving parts, and no second network hop to secure.
- **Schema and doc preservation.** Carrying Pydantic request/response models and endpoint docs into the tool definitions gives agents typed, documented tools instead of opaque endpoints — better tool-use correctness.
- **Mature, well-documented, packaged.** 11.9K stars, ~950 forks, 10 tagged PyPI releases (versioned/pinnable), CI + codecov + pre-commit + dependabot, a full `docs/` site, bilingual README, and six runnable examples. This is a maintained library.

## What didn't work or surprised us

- **Single-framework scope by design.** It is FastAPI-only. That is the whole premise, but it means the tool has zero reach for the many services not built on FastAPI — narrower than a generic OpenAPI→MCP path or a from-scratch builder.
- **Auto-exposing your whole API to an agent is a footgun.** "Point it at your app and it works" means every mounted endpoint becomes an agent-callable tool unless you filter (`03_custom_exposed_endpoints_example.py`). Destructive or privileged endpoints handed to an LLM is a real risk; the safe path (explicit allow-listing + auth) requires deliberate config, not the zero-config default.
- **Maintenance cadence is slower than its peers here.** Last push 2025-11-24 (~7 months before this review) versus very actively-pushed neighbors. Healthy and released, but not moving weekly.
- **It builds infrastructure; it does not improve your dev loop directly.** Unlike most catalog entries, this doesn't make *your* coding better — it makes *your API* consumable by agents. Its value lands only if exposing your service to agents is a goal.
- **Commercial framing.** A hosted product (tadata.com) sits behind it; the OSS library is the on-ramp. Fine, but worth noting the sustaining incentive.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Preserving Pydantic schemas + endpoint docs gives agents typed, documented tools, reducing malformed calls vs. opaque endpoints. |
| Speed | + | Two-line mount eliminates hand-writing an MCP server for a FastAPI service; ASGI transport avoids an extra network hop. |
| Maintainability | + / neutral | MCP tools track the FastAPI routes automatically (one source of truth), but adds a dependency and a new agent-facing surface to maintain. |
| Safety | − | Auto-exposing endpoints hands your whole API to an LLM unless filtered; `Depends()` auth reuse is a strong mitigation but must be configured, not assumed. |
| Cost Efficiency | neutral | Build-time tool; no direct token effect. Typed schemas may slightly reduce retry waste on malformed tool calls. |

## Verdict

**CONDITIONAL — adopt if you have a FastAPI service you want agents to call; otherwise skip.** Within its niche it is excellent: the FastAPI-native approach (reusing `Depends()` auth, preserving Pydantic schemas, ASGI transport) is genuinely better than a dumb OpenAPI→MCP converter, and the two-line mount is the lowest-friction way to make an existing FastAPI app agent-callable. The conditions are scope and safety: it only helps FastAPI users, and the zero-config default exposes every endpoint — you must allow-list and rely on auth before pointing an agent at it. The slower push cadence is a minor watch-item, not a blocker.

Compared to its catalog peer **fastmcp** (PrefectHQ): fastmcp is the general-purpose, framework-agnostic way to build MCP servers *from scratch* in Python — more flexible, more work. fastapi_mcp is the opposite trade: zero flexibility on framework, near-zero work *if* you are already on FastAPI, and it brings auth/schema reuse that a from-scratch builder makes you wire yourself. They are complements, not competitors — choose fastapi_mcp when the API already exists in FastAPI, fastmcp when you are building an MCP server independent of any web framework.

## Catalog entry

Target category: **MCP Servers**

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [fastapi_mcp](https://github.com/tadata-org/fastapi_mcp) | framework | Expose existing FastAPI endpoints as MCP tools in two lines — reuses `Depends()` auth, preserves Pydantic schemas, ASGI transport | Want agents to call an existing FastAPI service without hand-writing an MCP server | fastmcp (general-purpose MCP builder); typescript-mcp-server-generator |
