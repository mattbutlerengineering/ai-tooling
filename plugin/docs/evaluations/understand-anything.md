# Evaluation: Understand-Anything

**Repo:** [Egonex-AI/Understand-Anything](https://github.com/Egonex-AI/Understand-Anything)
**Stars:** 77,525 | **Last updated:** 2026-07-30 | **License:** MIT
**Last verified:** 2026-10-19
**Last triaged:** 2026-10-19  <!-- triaged: bulk -->
**Dev loop stage:** Plan (codebase understanding / onboarding before and during implementation)
**Layer:** Tooling

---

## What it does

Catalog one-liner: "Turns code into interactive knowledge graphs explorable by humans/agents."

Understand-Anything is a **Claude Code plugin** (also installable on Codex, Cursor, Copilot, Gemini CLI, OpenCode and ~13 other platforms via `install.sh`) that runs a multi-agent batch pipeline over a codebase and emits a knowledge graph plus an interactive web dashboard for a human to explore. The mechanism: `/understand` orchestrates 5 specialized sub-agents — `project-scanner` (discover files, detect languages/frameworks), `file-analyzer` (extract functions/classes/imports into nodes and edges), `architecture-analyzer` (assign layers: API/Service/Data/UI/Utility), `tour-builder` (generate guided learning tours ordered by dependency), and `graph-reviewer` (validate referential integrity). `/understand-domain` adds a 6th (`domain-analyzer`) and `/understand-knowledge` a 7th (`article-analyzer` for Karpathy-pattern LLM wikis). The result is written to `.understand-anything/knowledge-graph.json`.

The engine is a Tree-sitter + LLM hybrid: Tree-sitter deterministically parses source into a CST and extracts structural facts (imports, exports, definitions, call sites, inheritance) — pre-resolved into an `importMap` and used for fingerprint-based change detection — while the LLM produces the semantic layer (plain-English summaries, tags, layer assignments, business-domain mapping, guided tours, language-concept callouts). File analyzers run up to 5 concurrent, 20-30 files per batch.

Consumption is primarily **human-facing**: `/understand-dashboard` opens an interactive web UI (pan/zoom/search/click, color-coded by layer, persona-adaptive detail). Secondary agent-/dev-facing commands exist: `/understand-chat` (ask questions about the codebase), `/understand-diff` (impact analysis of current changes), `/understand-explain <path>` (deep-dive a file/function), `/understand-onboard` (generate an onboarding guide). The graph is plain JSON intended to be committed so teammates skip the pipeline. Updates are **incremental by default** (only changed files re-analyzed via fingerprints), and an optional `/understand --auto-update` installs a post-commit hook to patch the graph on every commit.

## How we tested it

**Evidence:** MEASURED

**Hands-on, measured.** Cloned `Egonex-AI/Understand-Anything` at `f2d0164` (2026-10-12), ran `pnpm install --frozen-lockfile` (17s, builds `@understand-anything/core`), and ran the plugin's own test suite plus its deterministic structural layer (the Tree-sitter `TreeSitterPlugin` and `GraphBuilder` exported by `core`) against a disclosed five-file fixture with hand-written ground truth. The LLM half of the pipeline (`/understand`'s multi-agent summaries, layers and tours) needs a model session and was out of reach in this sandbox, so what is measured is the structural graph the LLM stage sits on, versus a grep baseline.

```
git clone --depth 1 https://github.com/Egonex-AI/Understand-Anything && cd Understand-Anything
pnpm install --frozen-lockfile                       # Done in 16.6s
npx vitest run                                       # Test Files 38 passed | 1 skipped; Tests 786 passed | 12 skipped (170s)
node run.mjs                                         # fixture A/B, below
tree-sitter: 8/8 found, 0 spurious | 2/2 found, 0 spurious | 4/4 found, 0 spurious | 4/4 found, 1 spurious
grep       : 8/8 found, 2 spurious | 2/2 found, 0 spurious | 4/4 found, 0 spurious | 4/4 found, 2 spurious
  (columns: symbols | classes | imports | project-internal call targets)
tree-sitter calls spurious= ["sum"]     grep symbols spurious= ["commentedOut","insideString"]
grep calls spurious= ["round","sum"]    analysis wall-clock ms (5 files): 15.8
node graph.mjs                                       # GraphBuilder + validateGraph
{"nodes":12,"edges":10,"nodesByType":{"file":5,"function":5,"class":2},"edgesByType":{"contains":7,"imports":3},"valid":true,"issues":7}
```

## Test design

- **Task/corpus:** a five-file fixture (`billing.ts`, `util.ts`, `types.ts`, `report.py`, `billing_py.py`; 9 project symbols, 2 classes, 4 imports, 4 internal call edges) with planted traps for text matching: a commented-out `function commentedOut`, a string literal containing `function insideString() {}`, an arrow-function `const`, class methods, a Python `# def commented_out` comment and a `"def inside_string"` string. Ground truth is written by hand before running.
- **Baseline:** a regex grep a developer would write for the same job (`function X`, `const X = (`, `def X`, `class X`, `import ... from`), with the call-site grep handed the true internal symbol list, which flatters grep.
- **Metric:** per category, ground-truth items found and spurious items reported, counted by exact name; wall-clock of the analysis loop.
- **Reproduce:** the scripts are described by the commands above; the fixture contents are the planted traps listed here.

### Test design — skills (required when Type is skill or plugin)

- **Triggering:** the nine skills (`understand`, `understand-chat`, `understand-dashboard`, `understand-diff`, `understand-domain`, `understand-explain`, `understand-figma`, `understand-knowledge`, `understand-onboard`) are slash-command driven; no should/shouldn't-fire prompt set was run, because firing needs a live model session.
- **Output A/B:** the with-tool versus baseline comparison above applies to the deterministic extraction layer only; summaries, layers and tours that the skills produce were not generated, so their quality is unmeasured.

## What worked

- **Extraction beat grep on traps.** Tree-sitter reported 0 spurious symbols where the grep baseline reported 2 (`commentedOut` from a comment, `insideString` from a string literal); both found all 8 symbols, 2 classes and 4 imports.
- **Python needs no extra setup once the right constructor is used.** Passing `builtinLanguageConfigs` (42) and `builtinExtractors` (13) to `TreeSitterPlugin` gave 15 languages including Python, with call edges attributed to a caller (`render -> total_py`, `run -> render`).
- **Fast and deterministic.** 15.8 ms for five files, no network, no key; the graph validated (`valid: true`) with file, function and class nodes plus `contains` and `imports` edges.
- **Healthy engineering signal.** The repo's own suite passed 786 tests (38 files) from a clean install.

## What didn't work or surprised us

- **Default `new TreeSitterPlugin()` registers only `typescript` and `javascript`.** A Python file came back `{"status":"unsupported"}` and an empty analysis until the builtin configs were passed in; a script that follows the bare constructor silently sees nothing for other languages.
- **The headline feature is unmeasured.** Summaries, architectural layers, guided tours and the chat/diff skills all depend on a model session; this run says nothing about whether those are accurate or what they cost in tokens (the README itself warns the first `/understand` "can consume a significant number of tokens").
- **Call-edge precision is name-based.** `sum` was reported as a project call because the fixture's `Ledger.sum` shares a name with the Python builtin; the caller-scoped edge is right, the project-internal filter in the harness is what collided, but real repos with common names will see the same ambiguity.
- **Graph validation auto-corrected 7 nodes** that lacked a `summary` (defaulted to the node name) because no LLM stage supplied one; the graph is only useful as intended after that stage runs.
- **Two eval files exist for this tool.** `evaluations/Understand-Anything.md` is an older stub reading `SOURCE-ONLY`; it differs only by filename case and was left untouched here (detector AD territory, a human merge).

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Structural layer matched hand-written ground truth on symbols, classes and imports with 0 spurious, versus 2 spurious for grep; the LLM layer is unmeasured |
| Speed | neutral | 15.8 ms for the five-file structural pass; the LLM pipeline's wall-clock was not run |
| Maintainability | neutral | Produces a graph artifact for humans; does not change the code it analyzes |
| Safety | neutral | Dashboard is served read-only from local disk per its README; the multi-agent stage sends code to a model, not exercised here |
| Cost Efficiency | neutral | The deterministic stage costs no tokens; the README warns the full `/understand` pass is token-heavy and no figure was measured |
| Verifiability | + | Structural nodes and edges carry line ranges and validate against a schema, so a human can spot-check them; LLM summaries have no such check in this run |

## Verdict

**discovery-log — tentative read** — the deterministic Tree-sitter graph layer is sound (786 repo tests pass; 0 spurious symbols versus grep's 2 on a disclosed fixture), but the LLM-generated graph, tours and onboarding output that make up the product were not exercised, so this is not yet a read on the tool itself.

Left at `discovery-log` on `MEASURED` evidence for the structural layer only. A promotion read needs a model session: run `/understand` on a real repository, compare against `codegraph` on the same questions, and record token cost. The overlap analysis against `codegraph` (additive, different consumer) from the earlier review stands.

## Triage note

Left at `discovery-log`, not SKIPped. It cites
[`codegraph`](https://github.com/colbymchenry/codegraph) (STACK, `ADOPT`/`MEASURED`), but this
evaluation already worked that comparison and concluded **"additive, different shape, not a
replacement … You could run both"**: codegraph is a live MCP surface the agent queries mid-loop,
Understand-Anything is a batch pipeline producing a human-facing visual graph, tours, and
onboarding guides. Different consumer, different moment. The eval also states outright that
"this is not a SKIP-for-thinness case" at 63.9K stars and v2.7.3.

Re-evaluating it toward ADOPT needs the thing this lane cannot do — the eval names the trigger
(a live MCP query interface, or reproducible cost/quality benchmarks). P0 work.

Re-examined 2026-09-16 (5-oldest-untriaged pass): reasoning still holds, not newly dominated
by a STACK incumbent.

_Triaged 2026-08-04 by the P2 challenger band ([#265](https://github.com/mattbutlerengineering/ai-tooling/issues/265)); re-stamped 2026-09-16, 2026-10-19 (structural layer measured; LLM layer still open)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Understand-Anything](https://github.com/Egonex-AI/Understand-Anything) | tool | Turns code into interactive knowledge graphs explorable by humans/agents | Onboarding to and comprehending a large unfamiliar codebase is slow when reading code blind | codegraph, graphify, code-context-engine |
