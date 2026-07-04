# Evaluation: OpenOSINT

**Repo:** [OpenOSINT/OpenOSINT](https://github.com/OpenOSINT/OpenOSINT)
**Stars:** 711 | **Last updated:** 2026-06-19 (pushed; created 2026-05-06) | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Discover (outer loop — reconnaissance/intelligence gathering); not a software-build tool
**Layer:** Tooling (a Python agent + CLI + MCP server that wraps external OSINT binaries and APIs)

---

## What it does

The catalog one-liner would read: "AI-powered OSINT agent with REPL, CLI, and MCP server — 18 reconnaissance tools (email, username, IP, domain, breach, Shodan, VirusTotal, …) for authorized security research." It is published to PyPI (`pip install openosint`) and to the MCP Registry under `io.github.OpenOSINT/openosint`.

The actual mechanism: OpenOSINT is an LLM agent loop over a fixed set of 18 reconnaissance tools. The model (Anthropic Claude by default, or local Ollama, or any OpenAI-compatible endpoint) is given the tool schemas; it decides which tool to call, your code executes the *real* underlying binary or API (e.g. `holehe`, `sherlock`, `sublist3r`, `phoneinfoga`, plus HTTP calls to Shodan/VirusTotal/Censys/AbuseIPDB/HaveIBeenPwned/IP2Location/GitHub/DNS/Bright Data SERP+Unlocker), and the genuine subprocess/API output is fed back to the model. The README's framing — "hallucination in tool results is structurally impossible" — is correct in the narrow sense that tool *outputs* are real binary results; the model's *synthesis/report* of those results is still model-generated and can mislead. Tools run async via `asyncio.gather()` with subprocess timeouts; investigations auto-export Markdown + PDF reports and persist session history to `~/.openosint/history/`. The MCP server exposes all 18 tools natively to Claude Code / Claude Desktop / any MCP client, so the same recon surface is available inside an agent session with no extra wiring.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No `pip install openosint`, no REPL, no MCP server started, no tool executed against any target. Every claim below comes from the repository (GitHub metadata, README, full file tree, commit/release counts), not from observed runtime behaviour. The performance/behaviour descriptions ("structurally impossible to hallucinate", async parallelism) are the author's README claims, paraphrased and qualified — not measurements I made.

```bash
gh api repos/OpenOSINT/OpenOSINT --jq '{desc,stars:.stargazers_count,forks:.forks_count,pushed:.pushed_at,created:.created_at,license:.license.spdx_id}'
gh api repos/OpenOSINT/OpenOSINT/readme --jq '.content' | base64 -d
gh api "repos/OpenOSINT/OpenOSINT/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api repos/OpenOSINT/OpenOSINT/commits --jq 'length'        # 30 (default page)
gh api repos/OpenOSINT/OpenOSINT/releases --jq 'length'       # 26
gh api repos/OpenOSINT/OpenOSINT/contributors --jq '[.[].login]'  # 2 (SonoTommy, teamvelociraptor)
```

## What worked

- **Real tools, not hallucinated answers.** The architecture genuinely runs external binaries/APIs and feeds back actual output. For a domain (OSINT) where the failure mode is fabricated "findings", grounding the tool layer in real subprocess results is the right design and a real Correctness win over a model answering recon questions from memory.
- **Three interfaces, one tool surface.** REPL, direct CLI (`openosint email target@example.com`), Web UI, and an MCP server — the MCP server is the relevant slice for this catalog, exposing all 18 tools to Claude Code/Desktop with no extra config.
- **Backend-agnostic and offline-capable.** Anthropic Claude, local Ollama, or any OpenAI-compatible endpoint (LiteLLM, vLLM, LM Studio). You can run the LLM layer fully offline, which matters for sensitive investigations.
- **Active and shipping.** 26 releases since 2026-05-06, pushed the day of evaluation, published to both PyPI and the MCP Registry, with a CHANGELOG, Dockerfile, issue templates, and CONTRIBUTING — more release discipline than most single-purpose MCP servers in the catalog.
- **Explicit legal framing.** A dedicated `DISCLAIMER.md`, "authorized security research only" banner, and an acceptable-use page — appropriate for a tool with this reach.

## What didn't work or surprised us

- **High network/system reach — the dominant Safety concern.** This is the opposite of a sandboxed MCP server. It spawns external subprocesses (`holehe`, `sherlock`, `sublist3r`, `phoneinfoga` — none vendored, all must be in `PATH`) and makes outbound calls to a dozen third-party intelligence APIs, several of which (Shodan, Censys, VirusTotal, Bright Data) actively probe or scrape targets. Wired into an agent loop, an LLM autonomously deciding to run reconnaissance against attacker-supplied identifiers is a meaningful abuse/blast-radius surface.
- **"Hallucination impossible" is overstated.** True for tool *outputs*; the agent's compiled report — pivots, attributions, conclusions — is still model-generated and can confidently misattribute. The marketing line risks lulling users into over-trusting the narrative layer.
- **Out of scope for the dev loop.** This is a reconnaissance/intelligence tool, not a software-build tool. It only touches the catalog because it ships an MCP server; it does not move code Correctness, build Speed, or Maintainability. Its relevance to an *AI-tooling-for-development* catalog is marginal.
- **Heavy commercial overlay.** The repo carries a paid Prompt Pack, Open Collective donate buttons, a sponsored API (IP2Location) wired into a tool, `COMMERCIAL-LICENSE.md`/`COMMERCIAL.md`, and a `cloud/` directory with checkout/webhook/Polar billing routes. The OSS core is MIT, but the project is structured as a commercial funnel.
- **Two-author project, very young.** Created 2026-05-06; two contributors. The 26 releases reflect rapid iteration, not maturity — surface area is large and the team is small.
- **Legal/compliance burden lands on the user.** Breach-data lookups, phone intelligence, and live dorking carry jurisdiction-specific legal constraints the disclaimer pushes entirely onto the operator.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + / neutral | Tool outputs are real binary/API results (no fabrication at the tool layer); but the model's synthesis/report on top is still hallucination-prone, and it does not touch code correctness. |
| Speed | neutral | Async parallel tool execution speeds *investigations*, but this is recon, not the software build/verify loop the catalog optimizes. |
| Maintainability | neutral | No bearing on codebase maintainability; it produces investigation reports, not maintainable code. |
| Safety | - | Spawns uncontrolled external subprocesses and calls a dozen target-probing intelligence APIs; an LLM autonomously driving recon against arbitrary inputs is a real abuse/blast-radius surface. |
| Cost Efficiency | neutral | Several backing APIs (Shodan/VirusTotal/Censys/Bright Data) are metered; LLM agent loop spends tokens per investigation. Offline Ollama backend can zero out LLM cost. |

## Verdict

**SKIP** (for this catalog's purpose) — OpenOSINT is a competent, actively maintained AI OSINT agent, but it is a security-research/reconnaissance tool, not an AI-for-software-development tool. It only qualifies for the MCP Servers category on a technicality (it ships an MCP server), and it does not move any of the dev-loop quality signals the catalog exists to track. Its network/system reach also makes it a poor default to wire into a coding agent.

Compared to neighbors: the catalog's MCP servers cluster around development needs — **github-mcp-server** (repo operations), **exa-mcp-server**/**firecrawl-mcp** (web search/scrape *for research during development*), **playwright** (UI testing). OpenOSINT's closest functional neighbors (exa/firecrawl) fetch web content to *inform development*; OpenOSINT instead runs offensive reconnaissance against people and infrastructure. That is a different domain. If a security-tooling sub-catalog ever existed it would be a CONDITIONAL there (adopt for authorized red-team/SOC work, behind human approval gating); inside an AI-development catalog it is out of scope — SKIP.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [OpenOSINT](https://github.com/OpenOSINT/OpenOSINT) | MCP server | AI OSINT agent (REPL/CLI/MCP) wrapping 18 real recon tools — email, username, IP, breach, Shodan, VirusTotal — for authorized security research only | Security researchers want an agent that runs real reconnaissance tools and compiles findings instead of hallucinating them | exa-mcp-server, firecrawl-mcp (complementary: those fetch web content for dev research, OpenOSINT runs offensive recon — different domain) |
