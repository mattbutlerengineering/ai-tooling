# Evaluation: autoresearch

**Repo:** [karpathy/autoresearch](https://github.com/karpathy/autoresearch)
**Stars:** 87,570 | **Last updated:** 2026-06-19 | **License:** MIT
**Dev loop stage:** Reflect / Discover (outer loop — automated experimentation)
**Layer:** Tooling

---

## What it does

An autonomous research framework that gives an AI coding agent a real ML training setup (single-GPU GPT training on [nanochat](https://github.com/karpathy/nanochat)) and lets it experiment overnight. The agent modifies `train.py`, trains for a fixed 5-minute budget, checks if val_bpb improved, keeps or discards the change, and loops. The human wakes up to a `results.tsv` log of ~100 experiments and (hopefully) a better model.

The mechanism is remarkably simple: 3 core files (`prepare.py` read-only constants/eval, `train.py` agent-editable model code, `program.md` agent instructions). `program.md` is a ~200-line "skill" that defines the experiment loop, output format, logging protocol, simplicity criterion, and a critical `NEVER STOP` directive. The agent is autonomous — no human approval needed between experiments.

## How we tested it

Architecture review of the repo structure, `program.md` agent instructions, and `train.py` training code. Did not run hands-on (requires NVIDIA GPU). Assessed the methodology, instruction quality, and applicability to the ai-tooling catalog's scope.

```bash
gh api repos/karpathy/autoresearch --jq '.description, .stargazers_count'
gh api repos/karpathy/autoresearch/contents/program.md --jq '.content' | base64 -d
```

## What worked

- **program.md is an exemplary agent skill**: Clear constraints (fixed time budget, single file to edit, single metric), explicit output format, structured logging to TSV, and the `NEVER STOP` directive that enables true overnight autonomy. This is one of the best-written agent instruction documents in the catalog.
- **Simplicity criterion is novel**: "A 0.001 val_bpb improvement that adds 20 lines of hacky code? Probably not worth it. A 0.001 val_bpb improvement from deleting code? Definitely keep." This is a principled approach to autonomous code quality that most harnesses lack.
- **Fixed time budget is a design insight**: By fixing training time at 5 minutes regardless of what the agent changes, experiments are directly comparable. This eliminates the most common failure mode in autonomous research (unbounded runs).
- **Git-based experiment tracking**: Each experiment gets a commit, discarded experiments get `git reset`, kept experiments advance the branch. Simple, reviewable, no external experiment tracking needed.

## What didn't work or surprised us

- **Domain-locked to ML training**: The framework is specifically for neural network hyperparameter/architecture search on a single GPU. It cannot be repurposed for general software research, web scraping, or information synthesis (which last30days covers).
- **87K stars for a niche tool**: The star count reflects Karpathy's personal following more than broad applicability. Most developers don't have H100s or need autonomous LLM training optimization.
- **No cross-agent support**: The `program.md` instructions mention Claude/Codex but the repo itself has no plugin infrastructure, no MCP server, no CLI. It's a repo you clone and point your agent at.
- **No safety guardrails beyond the instruction**: The `NEVER STOP` directive means the agent runs indefinitely. If it enters a crash loop, it burns tokens on repeated failures until manually stopped. No circuit breaker, no max-experiment count.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Fixed-budget + single-metric design makes experiments directly comparable; git-based tracking preserves reproducibility |
| Speed | + | ~12 experiments/hour, ~100 overnight — orders of magnitude faster than manual ML research |
| Maintainability | neutral | Single-file constraint keeps code reviewable, but no architectural guidance beyond the simplicity criterion |
| Safety | - | No circuit breaker, no token budget cap, no max-experiment guard — indefinite autonomous operation with no kill switch |
| Cost Efficiency | neutral | 5-minute GPU runs are cheap, but indefinite agent sessions can burn significant LLM tokens on the reasoning between experiments |

## Verdict

**CONDITIONAL**

Use when you have a single-GPU ML training setup and want autonomous overnight experimentation. The `program.md` is a masterclass in agent instruction design — study it even if you never train a model. Not applicable to general software development research (last30days covers that), and the 87K stars overstate its breadth of applicability. The methodology (fixed budget, single metric, git-based tracking, simplicity criterion) is transferable to other domains even if the specific implementation is ML-only.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [autoresearch](https://github.com/karpathy/autoresearch) | tool | AI agents running automated ML research experiments overnight — 87K stars | Research is tedious; want AI to run experiments autonomously with keep/discard tracking | last30days-skill (different domain: autoresearch = ML experiments, last30days = web/social research) |
