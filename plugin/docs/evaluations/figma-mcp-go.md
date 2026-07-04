# Evaluation: figma-mcp-go

**Repo:** [vkhanhqui/figma-mcp-go](https://github.com/vkhanhqui/figma-mcp-go)
**Stars:** 1,158 | **Last updated:** 2026-04-30 (last push; latest release v0.1.3, 2026-04-12) | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Implement (design-to-code grounding; also Plan when generating designs from text)
**Layer:** Tooling (agent-facing bridge into a live Figma file — not infrastructure, no hosted service)

---

## What it does

A Go MCP server that gives an AI agent full **read and write** access to a live Figma file — and crucially **does not use the Figma REST API at all**. Instead of polling Figma's metered REST endpoints, it ships a **Figma plugin** that you import into Figma Desktop (`Plugins → Development → Import plugin from manifest`). The MCP server (started via `npx -y @vkhanhqui/figma-mcp-go`) and the running plugin connect over a local bridge (the server listens on `127.0.0.1:1994` by default; configurable via `--ip`/`--port`). The agent calls MCP tools, the server relays the request to the plugin, the plugin manipulates the document through Figma's in-app plugin API, and results flow back.

The mechanism matters because it sidesteps the entire reason Figma's official MCP is painful for hobbyists: the REST API tool-call quotas (the README cites 6 tool calls/month on Starter/View/Collab, 200/day on Pro/Org Dev seats, 600/day Enterprise). Because the plugin runs inside the user's own Figma session, there is no API token, no per-call quota, and no rate limit — the operations are the same ones a human could do by hand in the plugin sandbox.

The surface is large: **73 tools** spanning create (frames, rectangles, ellipses, text, images, components, sections), modify (fills, strokes, opacity, corner radius, auto-layout, transforms, z-order, reparenting, batch rename, find/replace), delete, prototype reactions, styles (paint/text/effect/grid), variables and modes (incl. light/dark, `bind_variable_to_node`), pages, components/navigation (swap, detach, group), a rich read set (`get_document`, `get_design_context` with detail levels, `search_nodes`, `scan_text_nodes`), and export (`get_screenshot`, `save_screenshots`, `export_frames_to_pdf`, `export_tokens` as JSON/CSS). It also ships **MCP prompts** ("design strategies") such as `read_design_strategy`, `design_strategy`, and `text_replacement_strategy` to steer the agent toward sound multi-step editing patterns.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed or run.** I examined the GitHub repo metadata, the full README, the recursive file tree, the release/tag history, and recent commit messages. I did **not** install the npm package, import the Figma plugin, connect an agent, or invoke any of the 73 tools. No designs were read or generated, so there are no measured latencies, success rates, or output-fidelity numbers below — only what the repo and code structure attest. The 73-tool count, the "no API/no rate limit" architecture, the REST-quota table, and the default `127.0.0.1:1994` bind are taken from the README and confirmed against the file tree (e.g. `internal/bridge.go`, `internal/leader.go`/`follower.go`/`election.go`, the `plugin/` Svelte UI, and the per-domain `internal/tools_*.go` handlers).

```bash
gh api repos/vkhanhqui/figma-mcp-go
gh api repos/vkhanhqui/figma-mcp-go/readme --jq '.content' | base64 -d
gh api "repos/vkhanhqui/figma-mcp-go/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api repos/vkhanhqui/figma-mcp-go/releases --jq '.[] | {tag:.tag_name,published:.published_at}'
gh api repos/vkhanhqui/figma-mcp-go/commits --jq '.[0:8][] | .commit.message'
# Catalog differentiation:
grep -inE "figma" /Users/mbutler/github/ai-tooling/CATALOG.md
```

## What worked

- **The core premise is a real, well-targeted pain point.** Figma's official MCP meters tool calls, and on the free/Starter tier the quota (6/month per the README) is unusable for AI experimentation. A plugin-bridge architecture that never touches the REST API genuinely removes that wall for free-plan users — the headline claim is structurally credible, not marketing fluff.
- **Write access is the differentiator, not just read.** Most "Figma for agents" tools (Figma-Context-MCP, design-extract) are read-only design-to-code extractors. figma-mcp-go is read **and** write across 73 tools, enabling text-to-design generation and programmatic editing (variables, styles, prototypes, batch rename) — a categorically larger surface than its catalog overlaps.
- **The codebase looks legitimately engineered, not a thin wrapper.** Go server split by domain (`tools_read_*`, `tools_write_*`), a leader/follower election layer (`election.go`, `leader.go`, `follower.go`) for multiple plugin connections, schema definitions, and a Svelte plugin UI. There are accompanying `_test.go` and `.test.ts` files on both sides and CI workflows (`ci.yml`, `release.yml`) — basic engineering hygiene is present.
- **Low-friction install and broad client support.** One-line `claude mcp add` / `codex mcp add` / `.mcp.json` setup via `npx`, no build step, published to npm and the MCP Registry. Works with any MCP-compatible client (Claude, Cursor, Copilot, Codex).
- **Bundled MCP prompts encode multi-step editing strategy**, which is exactly where naive agents thrash on large design trees (e.g. chunked `text_replacement_strategy`).

## What didn't work or surprised us

- **Early-stage maturity.** Highest release is **v0.1.3**, all releases compressed into late March–April 2026, and the last push (2026-04-30) predates this evaluation by ~7 weeks with 27 open issues. This is a young, single-maintainer project (the author states he built it because he couldn't afford higher Figma limits). API stability and long-term maintenance are unproven.
- **Requires Figma Desktop with the plugin manually imported and running.** This is not a headless/CI-friendly path: a human must import `manifest.json` from the release `plugin.zip` and keep the plugin open in an active Figma session. The bridge depends on that live session — it cannot operate against a closed file or a pure REST handle.
- **Operations inherit the Figma plugin sandbox, not the REST API's guarantees.** The plugin runs with the user's own in-app permissions on whatever file is open; a `delete_nodes` or `find_replace_text` mistake edits the real document. There is no server-side auth boundary — anything that can reach `127.0.0.1:1994` can drive the plugin (mitigated by localhost-only default bind, but still a write-capable local surface).
- **"No rate limits" is true of the API quota, not of Figma's plugin runtime.** Large trees, font loading, and async plugin calls still have practical performance limits (a recent commit migrated synchronous calls to async-safe methods — evidence the plugin runtime imposes its own constraints). Throughput on big files is unverified here.
- **Unverified in practice.** Output fidelity for text-to-design and design-to-code (the two headline demos) is shown only in the author's videos; not reproduced. The 73-tool surface is broad enough that quality likely varies tool-to-tool.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + (when it fits) | Read tools give the agent ground-truth design context (`get_design_context`, `scan_text_nodes`, `export_tokens`) so generated code/edits reflect the actual file, not a guess; write tools let the agent apply changes directly. Tool-level fidelity unverified. |
| Speed | + / mixed | Removes the REST quota wall entirely, so iteration isn't throttled; but requires a manual Figma Desktop + plugin setup and a live session, and large-tree plugin performance is unproven. |
| Maintainability | neutral | Helps maintain design systems (variables, styles, batch rename, token export) inside Figma; offers nothing for the consuming codebase's maintainability directly. |
| Safety | - (caution) | Write access to a live document with no server-side auth boundary; a wrong destructive call edits the real file. Localhost default bind limits blast radius; young v0.1.x project raises reliability risk. |
| Cost Efficiency | + (strong for free tier) | Eliminates Figma's metered tool-call cost for AI workflows — the entire reason the tool exists. Free, MIT, self-hosted, no API token. |

## Verdict

**CONDITIONAL**

figma-mcp-go solves a real, specific problem — Figma's official MCP meters tool calls into uselessness on free/Starter plans — by bypassing the REST API with a local plugin bridge, and it goes further than the read-only design-to-code extractors by offering **full read/write across 73 tools** (text-to-design, variables, styles, prototypes, token export). For an individual or small team on a free/cheap Figma plan who wants an agent to actively *build and edit* designs (not just read them), it is the most capable option among its catalog peers. **Adopt it when (a) your project does meaningful Figma work, (b) you're rate-limited or unwilling to pay for the official MCP quota, and (c) you can run Figma Desktop with the plugin imported and a live session open.**

It is not ADOPT-everywhere: it's niche to Figma-using teams, demands a manual desktop+plugin setup that rules out headless/CI use, carries write access to live documents with no server-side auth boundary, and is an early-stage (v0.1.3, single-maintainer, ~7 weeks since last push, 27 open issues) project whose tool fidelity is unverified here. Not SKIP because the architecture is sound, the codebase is genuinely engineered, and it uniquely covers the write/generate half of the design-to-code loop that **Figma-Context-MCP** (read-only layout extraction for design→code) and **plumb-mcp** (local, rate-limit-free, but framed around read + a verification loop) do not. Among the three, choose **Figma-Context-MCP** for pure design→code reading, **plumb-mcp** for local reading with verification, and **figma-mcp-go** when you need an agent to write/generate inside Figma on a free plan.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [figma-mcp-go](https://github.com/vkhanhqui/figma-mcp-go) | MCP server | Plugin-bridge Figma MCP with full read/write (73 tools) — no REST API, no rate limits; text-to-design and design-to-code (1.1K stars) | Official Figma MCP meters tool calls into uselessness on free/Starter plans; read-only Figma MCPs can't create or edit designs | Figma-Context-MCP and plumb-mcp are read-focused design→code; figma-mcp-go adds full write/generate via a live Figma-plugin bridge |
