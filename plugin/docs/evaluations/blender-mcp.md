# Evaluation: blender-mcp

**Repo:** [ahujasid/blender-mcp](https://github.com/ahujasid/blender-mcp)
**Stars:** 22,947 | **Last updated:** 2026-06-11 (pushed; created 2025-03-07) | **License:** MIT
**Dev loop stage:** Off the software dev loop — it is a 3D-content authoring bridge (Implement/produce *assets*, not code). Relevant to this catalog mainly as a Safety case study in host-reaching MCP servers.
**Layer:** Infrastructure (a stdio MCP server that opens a TCP socket to a running Blender instance and drives it; an in-app Blender addon executes the commands)

---

## What it does

BlenderMCP connects Claude to a running Blender via MCP, enabling prompt-assisted 3D modeling, scene creation, and manipulation. Two components: a **Blender addon (`addon.py`)** that runs a **socket server inside Blender** (default `localhost:9876`), and an **MCP server (`src/blender_mcp/server.py`)** that the model talks to and which forwards commands over that socket. Beyond object/material/scene tools it offers **viewport screenshots** back to the model, asset pipelines to **Poly Haven**, **Sketchfab**, and AI generators (**Hyper3D Rodin**, **Hunyuan3D**), a **remote-host** mode (`BLENDER_HOST`/`BLENDER_PORT`), and — the load-bearing tool — **`execute_blender_code`**, which runs **arbitrary Python inside the Blender process**.

Mechanism (from `server.py`): a `FastMCP` server with `@mcp.tool()`-decorated functions; each opens/reuses a `socket.socket(AF_INET, SOCK_STREAM)` to the addon and ships a JSON command. `get_viewport_screenshot` captures the viewport and (with consent) uploads it for telemetry. `execute_blender_code` is wrapped in `@rich_telemetry_tool("execute_blender_code", capture_code=True)` — i.e. the code you run can be captured into telemetry. Telemetry is on by default, anonymous, and disabled via the addon checkbox or `DISABLE_TELEMETRY=true`.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** Blender was not launched, the addon was not loaded, no socket was opened, and no `execute_blender_code` was issued. We did **not** install or execute it — appropriate given the tool's host reach. Claims come from the repo: metadata, README, file tree, and `src/blender_mcp/server.py` (tool decorators, socket setup, telemetry wrappers). No rendering quality, latency, or success-rate was measured.

```bash
gh api repos/ahujasid/blender-mcp --jq '{desc,stars:.stargazers_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'
gh api "repos/ahujasid/blender-mcp/git/trees/HEAD?recursive=1" --jq '.tree[].path'   # addon.py, server.py, telemetry*.py
gh api repos/ahujasid/blender-mcp/readme --jq '.content' | base64 -d | grep -niE "arbitrary|security|remote|telemetry|caution"
gh api repos/ahujasid/blender-mcp/contents/src/blender_mcp/server.py --jq '.content' | base64 -d | grep -nE "@mcp.tool|socket|execute_blender_code|telemetry"
```

## What worked

- **A real, two-way creative bridge.** Not a toy: object/material/scene CRUD, viewport screenshots fed back to the model (so it can *see* the scene), and integrations with Poly Haven, Sketchfab, Hyper3D Rodin, and Hunyuan3D for sourcing or generating assets. Active (pushed 2026-06-11), MIT, 22.9K stars, with releases, a Discord, and an official site.
- **Honest about the danger.** The README has an explicit "Limitations & Security Considerations" section warning that `execute_blender_code` runs arbitrary Python, "can be powerful but potentially dangerous," and to "ALWAYS save your work before using it." Telemetry has both a UI toggle and a kill-switch env var. That candor is better than most host-reaching servers manage.
- **Clean, conventional MCP implementation.** `FastMCP` + decorated tools + a single socket client with timeout handling and reconnection. Easy to read as a reference for an MCP server that drives an external desktop application.

## What didn't work or surprised us

- **`execute_blender_code` is an arbitrary-code-execution channel by design.** Blender's Python (`bpy`) is not sandboxed — it can read/write the filesystem, spawn subprocesses, and reach the network with the privileges of the Blender process. Handing that to an LLM-driven tool is broad host reach, not a 3D-only capability. This is the headline Safety concern.
- **Socket server with no visible auth.** The addon listens on a TCP port (default 9876) and the README documents a **remote-host** mode. A listening socket that executes forwarded Python, exposed beyond `localhost`, is an obvious lateral-movement / unauthenticated-RCE surface — there is no authentication layer evident in the design.
- **Telemetry on by default, and it can capture your code.** `execute_blender_code` is wrapped with `capture_code=True`, and screenshots are uploaded with consent. It is anonymized and disablable, but "phones home with the code you ran unless you opt out" is a posture worth flagging for any sensitive scene or proprietary asset.
- **Off-target for a software dev loop.** This produces 3D assets, not code, tests, or reviews. It belongs in the catalog only as a notable host-reaching MCP server / Safety exemplar, not as a stage tool.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | n/a | Output is 3D scenes/assets, not code; no software-correctness signal applies. Viewport-screenshot feedback does let the model self-correct its modeling. |
| Speed | + | For its niche, prompt-driven scene construction and asset import beat manual Blender work; socket round-trips are local and fast. |
| Maintainability | neutral | Clean MCP implementation, but irrelevant to your codebase's maintainability — it touches Blender, not your repo. |
| Safety | − − | `execute_blender_code` = unsandboxed arbitrary Python in the Blender process; an open TCP socket with a documented remote-host mode and no visible auth; default-on telemetry that can capture executed code. Highest host-reach risk profile of any tool reviewed here. |
| Cost Efficiency | neutral / − | The MCP server is free/open; cost risk is indirect — AI asset generators (Hyper3D/Hunyuan3D) and Sketchfab are external paid/quota services invoked through it. |

## Verdict

**SKIP (for this catalog's purpose) — out of scope, and a Safety cautionary case.** blender-mcp is a competent, popular, honestly-documented bridge for AI-assisted 3D content creation — genuinely useful if 3D modeling is your domain. But it produces assets, not software, so it has no place in a software dev loop, and its core value (`execute_blender_code`) is unsandboxed arbitrary Python over an optionally-remote, unauthenticated socket with default-on code-capturing telemetry. For anyone evaluating it: run it only against a local Blender, keep the socket on `localhost`, never expose the remote-host mode on an untrusted network, set `DISABLE_TELEMETRY=true` for proprietary work, and save before every `execute_blender_code`.

Compared to neighbors: unlike the catalog's dev-loop MCP servers (which read code, run tests, or query docs), blender-mcp's reach is into a live desktop app's full Python runtime — categorically broader than, say, a docs-fetching or browser-automation server, and it warrants the same scrutiny as any tool granted arbitrary local execution.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [blender-mcp](https://github.com/ahujasid/blender-mcp) | MCP server | Drives a live Blender instance over a socket for prompt-assisted 3D modeling — includes arbitrary-Python execution and asset pipelines (Poly Haven, Sketchfab, Hyper3D) | Want AI-assisted 3D scene/asset creation in Blender from natural language | (none in catalog — 3D-content bridge; relevant as a host-reaching/arbitrary-execution Safety exemplar) |
