# Evaluation: chrome-devtools-mcp (benjaminr — third-party, superseded)

**Repo:** [benjaminr/chrome-devtools-mcp](https://github.com/benjaminr/chrome-devtools-mcp)
**Stars:** 303  <!-- gh api, checked 2026-08-04; not catalogued, so not in repo-metadata.json -->
**Last updated:** 2025-10-06 (dormant ~10 months) | **License:** MIT
**Last verified:** 2026-08-05
**Dev loop stage:** Verify
**Layer:** Infrastructure

---

> **This file reviews a name-alike, not the tool the catalog carries.** Everything below
> is about **`benjaminr/chrome-devtools-mcp`** — a third-party MIT Python server. The
> catalogued `chrome-devtools-mcp` is the **official** server,
> [`ChromeDevTools/chrome-devtools-mcp`](https://github.com/ChromeDevTools/chrome-devtools-mcp)
> (Apache-2.0, ★48.5K, Chrome DevTools team) — a different codebase that merely shares
> the name. Detector U (`--catalog-mirror`, #336) surfaced the mismatch on 2026-08-04;
> [#355](https://github.com/mattbutlerengineering/ai-tooling/issues/355) resolved it.
>
> **The official server now has its own hands-on evaluation:
> [`chrome-devtools-mcp.md`](chrome-devtools-mcp.md)** (Evidence `MEASURED`). Read
> nothing below as evidence about it — this file kept the third-party review intact
> rather than repointing its link, because repointing would have attached a review of
> one codebase to another's identity, which is the same identity-by-name error #343 and
> #366 are about.
>
> **This file intentionally has no `## Catalog entry` block and no `CATALOG.md` row** —
> see the Verdict.


## What it does

An MCP server that bridges Claude to Chrome's DevTools Protocol (CDP), giving agents direct access to network monitoring, console logs, JavaScript execution, DOM inspection, CSS analysis, storage/cookie access, and performance metrics. Unlike playwright (which automates browser interactions — clicking, typing, navigating), this server focuses on *inspection*: reading network responses, diagnosing console errors, profiling performance, and examining runtime state. The agent connects to a Chrome instance with remote debugging enabled and queries it through ~40 MCP tools organized into six categories (Chrome management, network, console, page analysis, DOM, CSS).

Available as a Claude Desktop Extension (.dxt) for one-click install, or via `claude mcp add` for Claude Code with a Python server + uv venv.

## How we tested it

**Evidence:** REVIEW

Architecture review of the repo structure, README, and tool catalog. Not hands-on tested (no Chrome DevTools debugging session available in this environment).

```bash
gh api repos/benjaminr/chrome-devtools-mcp --jq '.description, .stargazers_count, .updated_at'
gh api repos/benjaminr/chrome-devtools-mcp/readme --jq '.content' | base64 -d
```

Assessed the tool surface area (40+ tools), installation paths (4 options including Claude Code), and compared against playwright MCP (ADOPT) and agent-browser (ADOPT) for overlap and complementarity.

## What worked

- **Genuinely different from playwright**: playwright automates (click, fill, navigate); this *inspects* (network requests, console errors, performance metrics, computed styles). They complement each other — playwright drives the browser, chrome-devtools-mcp reads what happened
- **Deep tool surface**: 40+ tools covering network monitoring with filtering (`filter_status=500`), console error summaries, live console monitoring, DOM querying with CSS selectors, computed/inline/matched style analysis, CSS coverage tracking, storage/cookie inspection, and performance metrics
- **Claude Code integration documented**: explicit instructions with absolute-path requirements and common pitfalls called out (relative paths, ModuleNotFoundError, venv Python)
- **Pre-commit quality gates**: ruff formatting/linting, mypy type checking, pytest validation, MCP server registration check
- **Extension packaging**: ships as .dxt for Claude Desktop one-click install

## What didn't work or surprised us

- **300 stars is modest** — the devtools-debugger-mcp fork by ScriptedAlchemy (345 stars) adds breakpoint debugging, step/run, call stacks, and source maps, which this server lacks. The debugging space is fragmenting
- **Python server with uv dependency**: heavier setup than a Node-based MCP server; requires cloning, `uv sync`, absolute path configuration. Compare with playwright MCP which is a single npx command
- **No breakpoint support**: the most powerful DevTools capability (setting breakpoints, stepping through code, inspecting call stacks) is missing — devtools-debugger-mcp covers this gap
- ~~**Catalog URL is wrong**: CATALOG.md links to `ChromeDevTools/chrome-devtools-mcp` which 404s; real repo is `benjaminr/chrome-devtools-mcp`~~ — **this bullet was itself wrong.** The catalog URL resolves fine; it names the *official* server, which is a different tool. What was actually wrong was this file's name, and the assumption that a shared name meant a shared repo. Corrected under #355.
- **Not tested hands-on**: evaluation is architecture-review-based; actual tool reliability in agent debugging sessions is unverified

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Network request inspection and console error summaries surface bugs that test suites miss |
| Speed | + | Agents can diagnose auth/network/performance issues without manual DevTools investigation |
| Maintainability | neutral | Inspection tool, doesn't change code |
| Safety | neutral | Localhost-only by design; no production use case |
| Cost Efficiency | neutral | Standard MCP tool call overhead |

## Verdict

**SKIP** — superseded by the official [`ChromeDevTools/chrome-devtools-mcp`](chrome-devtools-mcp.md).

The original read above is still a fair account of this server, and its central claim —
that *inspection* is a different job from *automation* — turned out to be right. It is
just that the official server does the same job at ★48.5K to this one's ★303, ships as a
single `npx` rather than a cloned Python tree with a uv venv and absolute paths, is
maintained by the Chrome DevTools team itself, and adds the whole measurement surface
this one lacks (performance traces with Core Web Vitals, CrUX field data, Lighthouse,
heap snapshots) — all of it measured hands-on in the official eval. This one has been
dormant since **2025-10-06**, ~10 months, and an MCP server over a moving protocol rots
faster than that.

Nothing here argues against the third-party server as a piece of work; there is simply no
question left that it is the best answer to. **#355 asked whether to give it a
`CATALOG.md` row of its own or drop the eval as superseded — this is the second answer,
with the review kept rather than deleted.** Adding a 653rd row for a dormant name-alike
that is strictly dominated by a row already in the catalog would put two entries in front
of a reader for one decision, which is exactly the collapsed-identity cost
[#343](https://github.com/mattbutlerengineering/ai-tooling/issues/343) is about. So this
file carries **no `## Catalog entry` block** — deliberately, and detector U treats an eval
with no embedded row as nothing-mirrored rather than as an ORPHAN, which is the correct
reading here: there is no row, and there should not be one.

Revisit only if the official server drops CDP-level inspection this one has, or if this
repo starts pushing commits again.
