# Evaluation: Understand-Anything

**Repo:** [Egonex-AI/Understand-Anything](https://github.com/Egonex-AI/Understand-Anything)
**Stars:** 77,525 | **Last updated:** 2026-07-30 (pushed) | **License:** MIT
**Last verified:** 2026-10-19
**Last triaged:** 2026-10-19  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

Turns code into interactive knowledge graphs explorable with questions — an unusually large (★77.5K) entrant in the code-understanding space. It ships as a Claude Code plugin (`/understand`, `/understand-chat`, `/understand-diff`, `/understand-domain`, `/understand-onboard`, `/understand-dashboard`) plus a React dashboard. Per its own README it is a hybrid: deterministic Node scripts (`scan-project.mjs`, `extract-import-map.mjs`, `extract-structure.mjs`, built on tree-sitter) enumerate files and extract structure, and LLM agents then write the node summaries, layers, tours and answers on top.

## How we tested it

**Evidence:** RUN

**Hands-on** — cloned `Egonex-AI/Understand-Anything` at `f2d0164` (2026-10-12), ran `pnpm install --frozen-lockfile` (22s, rc=0; its `prepare` step built `@understand-anything/core` with `tsc`), ran its own suite with `pnpm test`, then drove the three deterministic extraction scripts directly against a purpose-built fixture repo and scored them against ground truth.

```
pnpm install --frozen-lockfile
pnpm test
 Test Files  38 passed | 1 skipped (39)
      Tests  786 passed | 12 skipped (798)
   Duration  194.32s
python3 gen.py fx                      # fixture: 20 code files, 80 symbols, 52 import edges
node scan-project.mjs fx scan.json     # filesScanned=22 filteredByIgnore=0 complexity=small   (0.30s)
node extract-import-map.mjs imp_in.json imp_out.json
                                       # filesScanned=22 filesWithImports=20 totalEdges=52     (0.40s)
node extract-structure.mjs st_in.json st_out.json
                                       # filesAnalyzed=22 filesSkipped=0 structure succeeded 22/22 (0.43s)
python3 score.py
treatment (UA scripts): symbols tp=72 fp=0  fn=8  of 80 | import edges tp=52 fp=0 fn=0 of 52
baseline (regex):       symbols tp=80 fp=48 fn=0  of 80 | import edges tp=52 fp=0 fn=0 of 52
```

Everything above ran offline with no model credentials and no network beyond the package registry.

## Test design

- **Task/corpus:** a generated fixture repo (`git init`-ed, seed 7): 12 Python modules (`pkg/m0..m11.py`, each with 3 top-level functions, 1 class with 2 methods, and 3 cross-module imports in `from pkg.mN import …` / `import pkg.mN as …` form) and 8 TypeScript modules (`src/t0..t7.ts`, each with 2 exported functions, 1 interface, 1 class, and 2 relative imports incl. `import type`). Ground truth is recorded by the generator: 80 symbols and 52 import edges. Decoys target text-matching: a commented-out `def`/`function`, a triple-quoted string containing a fake `def` and `class`, and a template literal containing a fake `export function`.
- **Baseline:** what an agent does without the tool — line-anchored regexes for `def|function|class|interface` declarations and for the import forms above (0.001s).
- **Metric:** true/false positives and misses against ground truth, for symbols and for resolved import edges; wall-clock per script.
- **Reproduce:** clone the repo, `pnpm install --frozen-lockfile`, generate a fixture with known contents, then run the three scripts under `understand-anything-plugin/skills/understand/` in order (`scan-project` → `extract-import-map` → `extract-structure`) and diff their JSON against the generator's ground truth.

### Test design — skills (required when Type is skill or plugin)

- **Triggering:** not measured. The `/understand*` skills are model-invoked and scoring their `description` fields needs a model; none is available in this environment.
- **Output A/B:** the with/without comparison above covers only the deterministic extraction layer. The LLM layer (summaries, layer assignment, guided tours, `/understand-chat` answers) has no with-skill-vs-baseline result here.

## What worked

- **Import resolution was exact on the fixture.** 52 of 52 import edges recovered with 0 false edges, resolving Python `from pkg.mN import x` and `import pkg.mN as y` and TypeScript `./tN` (including `import type`) to project file paths — the same score as the regex baseline, but via tree-sitter rather than pattern luck.
- **No decoy hits.** Tree-sitter parsing ignored the commented-out declarations and the fake `def`/`class`/`function` inside a string and a template literal: 0 false-positive symbols, against 48 for the regex baseline (24 from the triple-quoted-string decoys, 24 from class methods reported as top-level declarations; the line-anchored regex happened to skip the inline comment and template-literal decoys, so those did not discriminate).
- **Method grouping.** Python methods came back nested under their class (`C0` → `method_a`, `method_b`), with start/end lines and parameters, rather than flattened.
- **Fast and cheap.** The whole scan → imports → structure pass over 22 files took about 1.1s of wall-clock and spends no model tokens; the README's incremental-update claim is backed by dedicated `prepare-incremental` / `finalize-incremental` scripts with their own tests.
- **The repo's own suite is green.** 786 passed, 12 skipped, 0 failed, in 194s on a fresh install.

## What didn't work or surprised us

- **TypeScript interfaces were missing from the structure output.** All 8 `export interface I<n>` declarations (8 of the 80 ground-truth symbols, 10%) were absent from `functions`, `classes` and `exports`, giving 72/80 symbol recall. That is the only miss; the regex baseline found them. Interfaces may be represented elsewhere in the graph build, so this is a gap in the extraction script's output rather than proof the finished graph omits them.
- **The headline feature was not exercised.** The graph itself, the dashboard, guided tours, semantic search and Q&A depend on LLM agents inside Claude Code (the README says the first `/understand` run "can consume a significant number of tokens on large projects"). No model credentials exist here, so the quality of those outputs is unmeasured, and the fixture says nothing about it.
- **Small fixture.** 22 files in two languages, with synthetic names; results say nothing about monorepos, dynamic imports, path aliases or the other languages the plugin lists.
- **Install footprint.** `pnpm install` reported a skipped build script for the Kotlin grammar and a misplaced `pnpm.onlyBuiltDependencies` field warning; neither affected the Python/TypeScript run.
- **Overlap.** `codegraph` (a STACK ADOPT pick) and `graphify` serve the same "structural awareness" job; this tool's differentiators are the dashboard and conversational layer, which are exactly the parts left untested.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Deterministic layer: 52/52 import edges, 0 false symbols, 72/80 symbols (TS interfaces missed); LLM layer unmeasured |
| Speed | + | Extraction passes took 0.3–0.4s each on 22 files; the model-driven part is the slow one and was not timed |
| Maintainability | neutral | A read-only analysis tool; writes a graph to `.ua/` in the target project |
| Safety | neutral | Runs locally; the LLM step sends file contents to whatever model the host harness uses (README suggests Ollama for privacy) — not tested |
| Cost Efficiency | - | README warns the initial full analysis can consume significant tokens on large projects; no token count measured |
| Verifiability | + | Structure and import edges come from a deterministic parser with JSON output a human can diff against the code; LLM summaries on top are not checkable at that rate |

## Verdict

**discovery-log — tentative read** — hands-on RUN of the deterministic layer only: 52/52 import edges, 0 decoy hits, 72/80 symbols (TS interfaces missed), 786 of its own tests passing, but the graph/dashboard/Q&A that make it a product need a model that was unavailable, so no verdict is earned yet.

## Triage note

Run on 2026-10-19 by the unattended eval-runner lane. A human with a Claude Code session could finish the read by running `/understand` on a repo with a known architecture and judging the graph and `/understand-chat` answers against `codegraph` on the same repo.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [Understand-Anything](https://github.com/Egonex-AI/Understand-Anything) | tool | Turns code into interactive knowledge graphs explorable with questions | Hard to grasp unfamiliar codebases; need to ask questions about structure and relationships | codegraph, graphify, code-context-engine |  |
