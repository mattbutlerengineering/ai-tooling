# Evaluation: PaperOrchestra

**Repo:** [Ar9av/PaperOrchestra](https://github.com/Ar9av/PaperOrchestra)
**Stars:** 587 | **Last updated:** 2026-06-13 (pushed; created 2026-04-09) | **License:** NOASSERTION (see repo `LICENSE`)
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Plan / Research (outer-loop knowledge production), with Verify-style integrity gates (citation F1, autoraters); not a code-production tool
**Layer:** Process / Tooling (a host-agent-executable skill pack: `SKILL.md` instruction docs + verbatim paper prompts + purely deterministic local helper scripts; no API keys, no LLM SDK)

---

## What it does

The catalog one-liner: "An automated AI research-paper writer based on Google's PaperOrchestra paper, packaged as skills for any coding agent." It is a faithful, host-agnostic re-implementation of the five-agent pipeline from [PaperOrchestra (arXiv:2604.05018)](https://arxiv.org/pdf/2604.05018) — Outline → Plotting → Literature Review → Section Writing → Content Refinement — that the paper reports beating single-agent and tree-search baselines on `PaperWritingBench` (the README cites the paper's own 50–68% literature-review and 14–38% overall win margins; these are *the paper's* numbers, not anything reproduced here).

The mechanism is deliberately thin-by-design: seven skills (`paper-orchestra` orchestrator + six workers) are *instruction documents* the host agent reads and follows, plus `references/` (the verbatim Appendix-F prompts, JSON schemas, rubrics, halt rules) and `scripts/` that are **purely deterministic** — JSON schema validation, Levenshtein fuzzy matching for citation verification, BibTeX formatting, dedup, LaTeX sanity checks, coverage gates. There are no embedded LLM calls and no API keys; all reasoning, web search, Semantic Scholar lookups, and LaTeX compilation are delegated to the host coding agent (Claude Code, Cursor, Antigravity, Cline, Aider, OpenCode) by instruction. Two skills go beyond authoring: `paper-writing-bench` reverse-engineers raw materials from an existing paper to build benchmark cases, and `paper-autoraters` runs the paper's own evaluators (Citation F1, 6-axis LitReview quality, side-by-side paper/litreview quality). An optional `agent-research-aggregator` pre-skill scrapes scattered agent history into the `(idea.md, experimental_log.md)` inputs the pipeline expects.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No skill was installed via `npx skills add`, no pipeline was executed, no paper was generated, and the deterministic helper scripts were not run. Every claim below comes from the repository (GitHub metadata, README, recursive file tree, the bundled `examples/agentic-security-report/`), not from observed output. The win-margin figures are the upstream paper's self-reported benchmark results, restated in the README — not measured here.

```bash
gh api repos/Ar9av/PaperOrchestra --jq '{desc,stars:.stargazers_count,forks:.forks_count,pushed:.pushed_at,created:.created_at,license:.license.spdx_id,topics:.topics}'
gh api repos/Ar9av/PaperOrchestra/readme --jq '.content' | base64 -d
gh api "repos/Ar9av/PaperOrchestra/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api repos/Ar9av/PaperOrchestra/commits --jq 'length'   # 30 (page-1 cap)
gh api repos/Ar9av/PaperOrchestra/releases --jq 'length'  # 2
```

## What worked

- **Grounded in a real, citable method.** Unlike generic "research assistant" prompt packs, this implements a specific published pipeline with its prompts, schemas, and halt rules transcribed from Appendix F. The provenance is explicit and the design decisions are traceable to the paper.
- **No-API-keys, host-delegated architecture is a clean fit for coding agents.** The skills carry instructions and deterministic glue only; the host agent supplies all LLM/search/compile capability. That makes it portable across six agents and avoids the "ships its own SDK and key handling" failure mode common to research tools.
- **Verification is first-class, not an afterthought.** Citation integrity (Semantic Scholar verify, Levenshtein > 70, cutoff filtering, dedup), coverage gates, and the bundled `paper-autoraters` mean the pipeline has built-in quality checks rather than trusting the draft. The halt rules in content-refinement explicitly guard against gaming the evaluator.
- **Real worked example.** `examples/agentic-security-report/` ships inputs, drafts, generated figures, and figure-generation scripts — a concrete artifact to inspect rather than a bare prompt list.
- **Reasonable maturity for its age:** 587★ / 80 forks, a CHANGELOG, CITATION.cff, 2 tagged releases, and architecture/fidelity docs — disciplined for a two-month-old single-author skill pack.

## What didn't work or surprised us

- **Narrow audience.** This writes *academic/technical research papers in LaTeX*. For the overwhelming majority of software work it is out of the day-to-day loop; it earns its place only when you actually need to produce paper-grade writeups.
- **Fidelity to the paper ≠ reproduced results.** The README borrows the upstream benchmark margins; nothing in the repo demonstrates those numbers on your inputs. Output quality still rests on the host model following dense instructions faithfully — there is no code that guarantees the paper's reported performance.
- **Cost can be substantial.** The skill table itself estimates ~20–30 LLM calls each for plotting and literature review; a full run is a long, multi-call session whose token cost lands on the host agent.
- **License is `NOASSERTION` via the API.** A `LICENSE` file exists but GitHub couldn't classify it — worth reading before any redistribution, especially given it re-implements a Google-authored method.
- **Crowded research-skill neighborhood.** It overlaps the catalog's other research packs; its differentiator is being a faithful single-paper implementation rather than a broad toolbox.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Citation-integrity verification (Semantic Scholar + Levenshtein, dedup, cutoff) and autoraters target the exact failure mode of automated writing — fabricated/loose citations. |
| Speed | + | Collapses a multi-day paper-drafting workflow into a structured pipeline with reusable prompts and deterministic glue, when the task is in scope. |
| Maintainability | neutral | Produces LaTeX papers, not codebase artifacts; no effect on a project's code maintainability. |
| Safety | + / neutral | Helper scripts are explicitly no-network/no-LLM; host agent does any web/Semantic Scholar access. Risk surface is the host's own tools, not the skill. |
| Cost Efficiency | − | A full run is ~50+ host LLM calls (plotting + litreview alone are ~20–30 each); expensive per paper. |

## Verdict

**CONDITIONAL** — adopt only when you actually produce research-paper-grade writeups (academic submissions, formal technical reports, security/whitepaper deliverables in LaTeX). It is the strongest of this catalog's research-writing cluster precisely because it is a *faithful implementation of one published, benchmarked method* with built-in citation verification and autoraters, rather than a loose "research assistant" persona. For everyday coding it is out of the loop, the cost per run is high, and the upstream benchmark margins are inherited, not reproduced.

Compared to neighbors: **academic-research-skills** and **scientific-agent-skills** are broader skill collections covering literature search and analysis but without a single rigorous end-to-end pipeline or autoraters; **deep-research** (harness) does multi-source fact-checked *reports*, not submission-ready LaTeX papers. PaperOrchestra wins on rigor and verification within its narrow lane; it loses on breadth and on being relevant to non-research workflows.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [PaperOrchestra](https://github.com/Ar9av/PaperOrchestra) | skill | Host-agnostic skill pack implementing Google's PaperOrchestra 5-agent pipeline (outline→plot→litreview→write→refine) with citation verification + autoraters; no API keys | Turn unstructured research materials into a submission-ready LaTeX paper with verified citations, runnable by any coding agent | academic-research-skills, scientific-agent-skills (broader/looser); deep-research (reports, not papers) |
