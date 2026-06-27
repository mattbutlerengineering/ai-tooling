# Spike: single source of truth for catalog facts vs. markdown-as-source

**Issue:** #112 · **Outcome:** [ADR-0002](../docs/adr/0002-catalog-source-of-truth.md) · **Date:** 2026-06-26

The most consequential architecture choice in the automation layer: the same per-tool
facts are denormalized across 7+ markdown files, and a large fraction of the Python
exists only to keep the copies in sync. This spike weighs replacing that with a single
generated source, and records the decision as an ADR.

## The denormalization, concretely

| Fact | Copied in | Sync machinery that exists *only* for this |
|------|-----------|--------------------------------------------|
| **Catalog count** | `README.md`, `CLAUDE.md`, `plugin/CLAUDE.md`, `COMPARISON.md` (×2: header + summary total) | `reconcile-counts.py` (propagate + `--check`) |
| **Verdict** | each eval's `## Verdict`, `COMPARISON.md` row, `STACK-LEDGER.md` | detectors **D** (verdict sync), **G** (comparison consistency), **J** (stack drift) |
| **Evidence level** | each eval's `**Evidence:**`, `COMPARISON.md` column | `backfill-evidence.py` (re-derive + re-sync) |
| **Type / dev-loop stage** | `CATALOG.md` row, `COMPARISON.md` row (+ stage section) | detector **G**, the `Tool | Type` prefix parsers in 4 sites |
| **The CATALOG/COMPARISON tables themselves** | root + `plugin/docs/` mirror | `sync-plugin-docs.sh` |

The smell the issue names is real: **a large share of the Python is a drift police force**,
not feature code. If a fact lived in exactly one place, detectors D/G/J + `reconcile-counts`
+ much of `backfill`/`tier-stack` would have nothing to check.

## The two options

### A. Single-source-generated
Define each tool's structured facts **once** — per-tool YAML frontmatter in its eval, or a
central `tools.yaml` — and **generate** the CATALOG/COMPARISON/STACK rows, counts, and the
`plugin/docs` mirror from it.

- **Eliminates drift by construction.** You can't desync two copies if there's one copy.
  Detectors D/G/J and `reconcile-counts` become unnecessary; `backfill`/`tier-stack` shrink
  to pure projection.
- **Costs a build step.** The repo gains a generate phase; CI must run it and diff-check it.
- **Moves the edit surface to YAML.** Contributors edit structured records, not the readable
  table. The greppable markdown table becomes a *build artifact* you must not hand-edit.

### B. Markdown-source-with-validators (status quo)
Hand-written markdown is the source of truth; Python validators catch drift after the fact.

- **The markdown IS the product.** Prose evals are hand-written, greppable, PR-reviewable, and
  shipped *directly* as `plugin/docs`. There is no build step between "write" and "ship".
- **Drift is possible but caught.** Detectors D/G/J + `reconcile-counts` + `backfill` are the
  cost of admitting denormalization; they run offline in `make check` and gate CI.
- **The toil is bounded and already paid.** The sync scripts exist and are tested
  (`test_automation.py`); the marginal cost per new tool is one `make fix`.

## Proof-of-concept sketch (Option A, one tool, one view)

What a tool's structured record + one generated view would look like:

```yaml
# evaluations/markitdown.md frontmatter (the single source)
---
name: markitdown
type: tool
stage: Plan            # dev-loop stage → COMPARISON section
auto: false
free: true
verdict: ADOPT
evidence: MEASURED
overlaps: [pandoc, unstructured, docling]
---
```

```python
# generate_comparison_row(record) -> the COMPARISON.md line, never hand-edited
def comparison_row(r):
    cell = lambda b: "✓" if b else ""
    return f"| {r['name']} | {r['type']} | {cell(r['auto'])} | {cell(r['free'])} | {r['verdict']} | {r['evidence']} |"
# -> | markitdown | tool | | ✓ | ADOPT | MEASURED |
```

The COMPARISON row is now a pure function of the eval's frontmatter — detectors D and G
(verdict sync, comparison consistency) are replaced by "regenerate and diff". **But note the
gap that kills the *pure* version:** ~hundreds of CATALOG rows are `discovery-log` /
`SOURCE-ONLY` leads with **no eval file** — there is no frontmatter to generate them from.
A single-source migration would still need a second store (a `tools.yaml`) for evalless rows,
so "one source" becomes "two sources" (frontmatter + yaml) in practice.

## The decision driver

The trade-off is not "drift police vs. clean architecture." It is **what the source artifact
is for**:

- The evals are **prose** — judgement, caveats, "how we tested", honesty disclaimers. That
  cannot be reduced to YAML without becoming a different, lesser product.
- The CATALOG/COMPARISON tables are **semi-mechanical**, but they are also the human-readable
  artifact shipped as plugin docs and reviewed in PRs.
- The denormalization that hurts most (the **count**) is already auto-propagated and is a
  non-event. The denormalization with real teeth (**verdict/evidence**) is already *derived*,
  not hand-kept, by `backfill-evidence.py` and gated by D/G/J.

So the validators are not unbounded toil — they are the bounded, already-paid price of keeping
the readable markdown as the thing you edit and ship. A build step would trade that bounded
price for a permanent layer between contributor and product.

**Recommendation → reject the full single-source migration; re-affirm markdown-as-source with
validators.** Keep the one genuinely-mechanical projection we already do (the Evidence column
via `backfill`, the count via `reconcile`). See ADR-0002 for the recorded decision and which
downstream refactors it unblocks vs. retires.
