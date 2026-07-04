# Evaluation: mcp-use

**Repo:** [mcp-use/mcp-use](https://github.com/mcp-use/mcp-use)
**Stars:** 10,123 | **Last updated:** 2026-06-19 (pushed; created 2025-03-28) | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Implement (build MCP servers/apps) + a thin slice of Verify (the Inspector for testing/debugging servers). It is infrastructure you build *with*, not a tool that intervenes in your project's dev loop — relevant only when the thing you ship *is* an MCP server or MCP app.
**Layer:** Tooling/Infrastructure — an SDK + scaffolder (`create-mcp-use-app`) + web Inspector + CLI, plus a managed cloud (Manufact) for deploy/observability. Maintained by manufact.com, the commercial host behind it.

---

## What it does

mcp-use bills itself as "the fullstack MCP framework to build MCP Apps for ChatGPT / Claude & MCP Servers for AI Agents." In practice it is several things bundled in one monorepo (Python + TypeScript): (1) a **server SDK** — `MCPServer` with a decorator/`server.tool({...})` API, Zod/Pydantic-typed args, and an `MCP Apps` extension that pairs a tool with an auto-discovered React widget (`resources/<name>/widget.tsx`) that renders inside Claude/ChatGPT; (2) an **Inspector** — a web previewer/debugger auto-mounted at `/inspector`, also available online and as `npx @mcp-use/inspector --url ...`; (3) a **client + agent** — `MCPClient` and `MCPAgent` (LangChain-backed), so the same library can also *consume* MCP servers and drive an LLM over them; (4) a **deploy path** — `npx @mcp-use/cli deploy` to Manufact MCP Cloud (the commercial backing).

The headline differentiator versus plain server frameworks is **MCP Apps / widgets**: write a tool once, return a `widget({props, message})`, and get an interactive UI that works across MCP clients. The repo also ships ~13 one-click deployable template apps (chart builder, slide deck, maps explorer, etc.). So it spans both halves of MCP — building servers *and* building an agent/client that uses them — which is why it overlaps fastmcp (server side) and fast-agent (client/agent side) simultaneously.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** Nothing was `pip install`ed or `npx`ed; no server was started, no Inspector opened, no `deploy` invoked. The MCP Apps "write once, run everywhere" claim and the widget cross-client rendering were **not** verified against a live Claude/ChatGPT client — they are README claims. All findings come from repo metadata, README, and the file tree.

```bash
gh api repos/mcp-use/mcp-use --jq '{desc,stars:.stargazers_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'
gh api repos/mcp-use/mcp-use/readme --jq '.content' | base64 -d            # quickstarts, MCP Apps, templates, packages
gh api "repos/mcp-use/mcp-use/git/trees/HEAD?recursive=1" --jq '.tree[].path'  # monorepo: libraries/python, libraries/typescript, inspector, cli
gh api repos/mcp-use/mcp-use/commits --jq 'length'    # 30 (page-1 cap — active)
gh api repos/mcp-use/mcp-use/releases --jq 'length'   # 30 (page-1 cap — frequent releases, published to PyPI + npm)
```

## What worked

- **Genuinely fullstack and low-boilerplate.** One `server.tool({name, schema}, handler)` call with typed args (Zod in TS, Pydantic + `Annotated`/`ToolAnnotations` in Python) is about as terse as fastmcp, and the auto-mounted Inspector means you get a test harness for free on `listen()`.
- **MCP Apps / widgets are a real capability gap that fastmcp doesn't cover.** Returning a React component as tool output, auto-discovered from `resources/`, with `useWidget()` and theme support, is a meaningfully different surface than "return text" — and the ~13 ready templates lower the cost of trying it.
- **Dual server *and* client/agent in one library.** `MCPClient` + `MCPAgent` (LangChain-backed) means you can build a server and an agent that consumes it without pulling a second framework — examples cover OAuth (dynamic + preregistered), multi-server, sandboxing, structured output, middleware, multimodal.
- **Distribution and traction are real.** Published to both PyPI (`mcp_use`) and npm (`mcp-use`), frequent releases, CI (conformance, e2e, typecheck), SECURITY.md, a published skill on skills.sh, and ~10K stars on a 14-month-old repo.

## What didn't work or surprised us

- **Strong commercial gravity toward Manufact MCP Cloud.** Deploy, observability, metrics, logs, and branch-deployments route to the vendor's hosted platform. The SDK is MIT and self-hostable, but the README's "Preview → Deploy" funnel is built around the paid host — the usual open-core lock-in risk applies to the managed pieces.
- **Scope sprawl.** Server SDK + Apps + Inspector + CLI + client + agent + cloud is a lot of surface for one dependency. If you only need to *build a server*, fastmcp is narrower; if you only need to *build an agent over MCP*, fast-agent is narrower. mcp-use is "all of it," which is power or bloat depending on need.
- **MCP Apps is young and client-dependent.** "Write once, run everywhere" assumes the target client (Claude/ChatGPT) supports the widget protocol; portability is a moving target and was not verified here.
- **Not a dev-loop tool for most projects.** Unless your deliverable is an MCP server/app, this never touches your inner loop — it is infrastructure for a specific kind of product, not a workflow improver.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Typed schemas (Zod/Pydantic) + conformance CI reduce protocol-shape bugs in servers you build, but it doesn't make *your* application logic more correct. |
| Speed | + | Scaffolder + decorator API + auto-Inspector + one-click templates compress the build-a-server/app loop; hot-reload CLI helps iteration. |
| Maintainability | + / − | Clean typed SDK and a single dependency for both server and client is maintainable; offset by large surface area and coupling to a vendor cloud for the deploy/observability path. |
| Safety | neutral / − | The SDK itself is a build tool. Risk is in what you build (a server exposes tools to LLM clients) and in routing prod deploys + logs through a third-party host — evaluate Manufact's data handling before shipping sensitive servers. |
| Cost Efficiency | neutral | OSS SDK is free; managed cloud is the monetization. No token-cost effect on your agents beyond whatever server you build. |

## Verdict

**CONDITIONAL — adopt if you are building MCP servers or (especially) MCP Apps/widgets; otherwise it's infrastructure you don't need.** mcp-use is a legitimate, actively maintained, fullstack MCP framework whose standout is the MCP Apps widget layer that pure server frameworks lack. The caveats are scope sprawl and a deliberate funnel toward the maintainer's commercial cloud for deploy/observability — fine if you self-host the MIT SDK, a lock-in vector if you lean on Manufact.

Compared to neighbors: **fastmcp** is the narrower, more battle-tested *server-only* builder — pick it if all you need is a Pythonic MCP server with no UI/widgets. **fast-agent** is the narrower *client/agent* framework — pick it if you only need to build and evaluate an agent over MCP. mcp-use's claim to the slot is that it does both *plus* interactive widgets in one package; that breadth is its advantage over either neighbor and its main risk. Use mcp-use when "interactive MCP app across Claude/ChatGPT" is the goal; use fastmcp/fast-agent when you want one focused half.

## Catalog entry

**Target category: MCP Servers**

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [mcp-use](https://github.com/mcp-use/mcp-use) | framework | Fullstack MCP framework (Py + TS): build MCP servers, interactive MCP Apps/widgets, and agents/clients, with an auto-mounted Inspector and one-click cloud deploy | Building MCP servers/apps and agents that consume them requires stitching multiple libraries; unifies server + client + widget UI + debugger in one SDK | fastmcp (server-only builder), fast-agent (client/agent framework), typescript-mcp-server-generator |
