# Code Understanding Tools

Evaluation date: 2026-06-15

## Evaluation Criteria

- **Repo health** — stars, recency, activity, community
- **Scope** — what inputs it handles (code only vs. docs/images/videos)
- **Integration** — which AI coding tools it supports
- **Mechanism** — how it actually works (MCP server, skill, CLI, etc.)
- **Output quality** — what you get back and how agents consume it
- **Maintenance** — how actively maintained, release cadence

---

## Tool Comparisons

### graphify

**Repo:** [safishamsi/graphify](https://github.com/safishamsi/graphify)
**Stars:** 67,715 | **Last updated:** 2026-06-16 | **License:** MIT | **Language:** Python
**YC S26 company**

**What it actually does:** A Python CLI/skill invoked via `/graphify .` that processes an entire project — code, docs, PDFs, images, videos — into a knowledge graph. Outputs three files: `graph.html` (interactive browser visualization), `GRAPH_REPORT.md` (key concepts, surprising connections, suggested questions), and `graph.json` (the full graph for querying). Also supports `graphify export callflow-html` for Mermaid call-flow diagrams.

**Mechanism:** Runs as a Claude Code skill (invoked via `/graphify`). Processes files with AI to extract entities and relationships, builds a graph, then clusters communities. One-shot batch process — you run it, it produces output files, done.

**Strengths:**
- Broadest input scope: handles code, SQL, shell scripts, docs, papers, PDFs, images, and videos — not just source code
- Multiple output formats (HTML visualization, markdown report, raw JSON)
- Massive community (67k stars), actively maintained, YC-backed
- Works across 20+ AI coding tools (Claude Code, Codex, Cursor, Gemini CLI, Copilot, etc.)
- The `GRAPH_REPORT.md` is directly consumable by agents in subsequent sessions
- Callflow export gives Mermaid diagrams for architecture documentation

**Weaknesses:**
- Batch process, not live — graph goes stale as code changes until you re-run
- Requires Python 3.10+ and uv/pipx installation
- One-shot analysis means agents can't query incrementally during a session
- PyPI package name is `graphifyy` (double-y), which is confusing

---

### codegraph

**Repo:** [colbymchenry/codegraph](https://github.com/colbymchenry/codegraph)
**Stars:** 49,711 | **Last updated:** 2026-06-16 | **License:** MIT | **Language:** TypeScript
**1.0 released**

**What it actually does:** A CLI tool that builds a pre-indexed semantic knowledge graph of your codebase, then exposes it to AI agents via an MCP server. Agents query the graph directly through a `codegraph_explore` tool instead of scanning files with grep/read. Auto-syncs on every file change — the index is never stale.

**Mechanism:** Runs as an MCP server that agents connect to. After `codegraph init`, it watches for file changes and updates the graph automatically. Agents use a `codegraph_explore` tool to query symbol relationships, call graphs, and code structure. Zero file reads needed.

**Strengths:**
- **Live auto-sync** — graph updates on every file change, never stale
- **MCP-based** — agents query it natively as a tool, not via reading output files
- **Benchmarked savings** — 16% cheaper, 58% fewer tool calls, 47% fewer tokens across 7 real codebases
- No runtime dependency (bundles its own Node.js)
- Answers include exact methods and code structure, collapsing redundant implementations to signatures
- `codegraph install` auto-configures all supported agents in one command

**Weaknesses:**
- Code-only — doesn't handle docs, PDFs, images, or videos
- Requires per-project initialization (`codegraph init` + `.codegraph/` directory)
- Relatively newer project (created Jan 2026) — less battle-tested
- Commercial platform coming (potential future lock-in)

---

### Understand-Anything

**Repo:** [Egonex-AI/Understand-Anything](https://github.com/Egonex-AI/Understand-Anything)
**Stars:** 60,606 | **Last updated:** 2026-06-11 | **License:** MIT | **Language:** TypeScript

**What it actually does:** A Claude Code plugin that runs a multi-agent pipeline to analyze your project, builds a knowledge graph of every file, function, class, and dependency, then produces an interactive dashboard. Has two views: structural graph (code entities and relationships) and domain view (business processes as horizontal flows). Also supports knowledge base analysis for wiki-style docs. Features guided tours that walk you through the architecture in dependency order.

**Mechanism:** Claude Code plugin invoked via `/understand`. Multi-agent pipeline does the analysis, then produces an interactive HTML dashboard. Also supports `/understand-knowledge` for knowledge bases.

**Strengths:**
- Best visualization — interactive dashboard with structural and domain/business-logic views
- Guided tours auto-generate architecture walkthroughs in correct dependency order
- Knowledge base mode for wiki-style documentation (Karpathy-pattern)
- Multi-agent pipeline produces richer analysis than single-pass tools
- Strong community (60k stars)

**Weaknesses:**
- Plugin-only (Claude Code) — narrower integration surface than graphify/codegraph
- No live sync — batch process like graphify
- No evidence of token/cost savings benchmarks
- Last updated June 11, slightly less active than graphify/codegraph
- Heavier-weight process (multi-agent pipeline takes longer)

---

### repomix

**Repo:** [yamadashy/repomix](https://github.com/yamadashy/repomix)
**Stars:** 26,306 | **Last updated:** 2026-06-14 | **License:** MIT | **Language:** TypeScript

**What it actually does:** Packs an entire repository into a single file (XML, Markdown, or plain text) optimized for feeding to LLMs. Not a knowledge graph — it's a serialization tool. Includes file tree, content, and metadata in one document. Has a web interface at repomix.com.

**Mechanism:** CLI tool (`npx repomix`) that reads all files and concatenates them with structure metadata. Output is a single file you paste into an LLM chat. No MCP server, no agent integration, no graph.

**Strengths:**
- Simplest approach — just works, no setup, no dependencies
- Most mature project (created July 2024, 2 years of development)
- Useful for LLMs without file access (ChatGPT, web interfaces)
- Web version available at repomix.com
- Good for one-off analysis when you don't have agent file access

**Weaknesses:**
- Not a knowledge graph — no relationship extraction, no structure analysis
- Solves a different problem: "give an LLM my code" vs. "help an agent understand my code"
- Agents that already have file access (Claude Code, Codex) don't need this
- Output file can be enormous for large repos, potentially exceeding context windows
- No incremental updates — full re-pack every time

---

## Summary Comparison

| Feature | graphify | codegraph | Understand-Anything | repomix |
|---------|----------|-----------|---------------------|---------|
| Stars | 67,715 | 49,711 | 60,606 | 26,306 |
| Approach | Batch knowledge graph | Live MCP knowledge graph | Batch multi-agent analysis | Flat file serialization |
| Auto-sync | No | **Yes** | No | No |
| Agent integration | Skill (invoked manually) | **MCP server (always-on)** | Plugin (invoked manually) | None (copy-paste) |
| Input scope | **Code + docs + images + video** | Code only | Code + knowledge bases | Code only |
| Token savings | Not measured | **16% cheaper, 58% fewer tool calls** | Not measured | Not applicable |
| Visualization | HTML graph + report | No visualization | **Best: interactive dashboard** | No visualization |
| Runtime | Python 3.10+ | Self-contained binary | Claude Code plugin | Node.js/npx |

---

## Verdict

**Recommended: codegraph**

**Why:** For the specific use case of "help AI agents understand my codebase during development," codegraph wins on the dimension that matters most: **it's always on and always current.** The MCP server integration means agents automatically query the knowledge graph without you running a command — and the graph never goes stale because it auto-syncs on every file change. The benchmarked 16% cost savings and 58% fewer tool calls across 7 real codebases provide concrete evidence, not just claims. For a workflow where agents are running increasingly autonomously, having a live, always-current code understanding layer is more valuable than a richer-but-stale batch analysis.

**Runner-up: graphify — use when you need broader analysis**

Graphify handles inputs that codegraph can't: PDFs, images, videos, SQL schemas, documentation. If you're onboarding to a new project and need to understand the full ecosystem (not just code), graphify's `GRAPH_REPORT.md` with key concepts and suggested questions is more useful than codegraph's code-only graph. It's also the better choice for architecture documentation (callflow diagrams) and for producing artifacts that humans (not just agents) will read.

**Use both together:** codegraph for continuous agent awareness during coding sessions, graphify for periodic deep analysis when onboarding or documenting architecture. They don't conflict — codegraph runs as an MCP server, graphify runs as a one-shot skill.

**Skip: Understand-Anything** — best visualization but no live sync and no measured efficiency gains. If you're already using codegraph + graphify, Understand-Anything adds a prettier dashboard but not more capability.

**Skip: repomix** — solves a different problem (feeding code to LLMs without file access). Agents that already have file access don't need it.
