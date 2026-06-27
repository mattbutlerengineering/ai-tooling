# ADR-0002: Keep markdown-as-source for catalog facts; reject full single-source generation

- **Status:** Accepted
- **Date:** 2026-06-26
- **Issue:** #112
- **Spike:** [spikes/catalog-source-of-truth.md](../../spikes/catalog-source-of-truth.md)
- **Supersedes / relates to:** continues the #45 shared-parser seam; complements [ADR-0001 (verdict vocabulary)](../decisions/0001-verdict-vocabulary.md)

## Context

The same per-tool facts are denormalized across 7+ markdown files (count, verdict, evidence
level, type/stage), and a large fraction of the automation Python exists only to keep the
copies in sync: `reconcile-counts.py`, detectors **D**/**G**/**J**, and most of
`backfill-evidence.py` / `tier-stack.py`. The spike asked whether to replace that with a
**single generated source** (per-tool YAML frontmatter or a `tools.yaml`) from which the
CATALOG/COMPARISON/STACK rows, counts, and `plugin/docs` mirror are generated — which would
make D/G/J + `reconcile-counts` unnecessary by construction.

The full comparison and a proof-of-concept sketch are in the spike. The decisive findings:

1. **The markdown is the product, not an intermediate.** Prose evals (judgement, caveats,
   "how we tested", honesty disclaimers) are hand-written, greppable, PR-reviewable, and
   shipped *directly* as `plugin/docs`. There is no build step between writing and shipping.
   Single-source would insert a permanent generate phase between contributor and product and
   make the readable table a build artifact that must not be hand-edited.
2. **"One source" is really "two sources" here.** Hundreds of CATALOG rows are
   `discovery-log` / `SOURCE-ONLY` leads with **no eval file** and therefore no frontmatter to
   generate from. A migration would still need a second store for evalless rows, so it does
   not actually collapse to a single source.
3. **The toil is bounded and largely already mechanized.** The count is auto-propagated
   (`reconcile-counts`, a non-event); the Evidence column is *derived*, not hand-kept
   (`backfill-evidence`). The remaining validators (D/G/J) run offline in `make check`, are
   characterization-tested (`test_automation.py`), and cost one `make fix` per new tool.

## Decision

**Reject the full single-source migration. Re-affirm markdown-as-source-with-validators as the
architecture for catalog facts.** The denormalization is accepted deliberately; the validators
are its bounded, already-paid price, and they are cheaper than the contributor-friction and
build-step cost of generation.

We keep the two genuinely-mechanical projections we already do — the **count** (via
`reconcile-counts`) and the **Evidence column** (via `backfill-evidence`) — because they
derive a value from a single owner rather than asking a human to maintain copies.

## Consequences

- The drift-detector suite (D/G/J) and `reconcile-counts` are **endorsed**, not technical
  debt. They stay gated in `make check` / CI.
- Contributors keep editing the readable markdown directly; no YAML/build step is introduced.
- If validator toil ever grows past its current bounded cost, the **incremental** escape hatch
  (not adopted now) is to generate *only* the COMPARISON row from per-eval frontmatter for
  tools that have an eval — narrowing D/G — without touching the prose or the evalless rows.
  This is a reversible, additive step, not the wholesale migration rejected here.

## Downstream slices: unblocked vs. retired

Because markdown stays the source, every slice the issue gated is **deepened (unblocked)**, not
retired — they make the shared-parser seam stronger rather than being obviated by generation:

- **Unblocked** — centralize COMPARISON-row parsing in `catalog_lib` (3 duplicated parsers).
- **Unblocked** — centralize CATALOG-row parsing in `catalog_lib` (4 parse sites + the private
  `_BODY_ROW` reach-across).
- **Unblocked** — unify the 3 name-normalization strategies (`_norm` / `_drift_key` /
  `_OVL_STRIP` + inline triple-key copies).
- **Unblocked** — detector protocol + `DetectorContext` injection (13 detectors; 7/13 untested
  via global `ROOT`).
- **Unblocked** — row-shape schema validation (`validate_row()`) falling out of the
  centralized parsers.

**Retired:** none. (All of the above would have been retired only under a single-source
migration, which is rejected.)
