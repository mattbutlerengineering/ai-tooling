# Implementation Plans

**Run 1** — improve skill, 2026-07-03 (audit at commit `4cc412e`). Focus: (1) evaluate skills/tools more rigorously, (2) consolidate recommendations into one answer surface, (3) make the repo function as an operating manual for AI-assisted development. Plans 001–011.

**Run 2** — improve skill, 2026-08-03 (audit at commit `a388dd2`). Focus: the automation layer itself. Run 1 built the derived-page apparatus (`triage.py`, `watchlist.py`, `tier-stack.py`, the detector engine); run 2 audits it as production code. Plans 012–015 — all four are correctness/reliability fixes in the gate path, none touches the catalog data. Selected as the default top-4 by leverage; the remaining findings are in "Findings considered and rejected".

Execute in the order below unless dependencies say otherwise. Each executor: read the plan fully before starting, honor its STOP conditions, and update your row when done.

## Execution order & status

| Plan | Title | Priority | Effort | Depends on | Status |
|------|-------|----------|--------|------------|--------|
| [001](001-fix-stale-counts.md) | Fix stale prose counts; derive eval count in reconcile | P1 | S | — | DONE ([#215](https://github.com/mattbutlerengineering/ai-tooling/issues/215)) |
| [002](002-honest-funnel-metric.md) | COMPARISON Summary reports real Validated %, not 100% | P1 | M | 001 | DONE ([#220](https://github.com/mattbutlerengineering/ai-tooling/issues/220)) |
| [003](003-workflow-stack-drift.md) | Reconcile WORKFLOW↔STACK + report-only drift detector | P1 | M | — | DONE ([#216](https://github.com/mattbutlerengineering/ai-tooling/issues/216)) |
| [004](004-discovery-intake-consolidation.md) | Consolidate scan intake on `scan`-labeled issues; index discovery/ | P2 | S | — | DONE ([#217](https://github.com/mattbutlerengineering/ai-tooling/issues/217)) |
| [005](005-next-evals-queue.md) | Generate NEXT-EVALS.md — ranked discovery-log promotion queue | P1 | M | 002 | DONE ([#223](https://github.com/mattbutlerengineering/ai-tooling/issues/223)) |
| [006](006-watchlist.md) | Generate WATCHLIST.md — deferred/stale/flagged/unverified in one page | P2 | M | 005 | DONE 2026-07-04 ([#224](https://github.com/mattbutlerengineering/ai-tooling/issues/224)) |
| [007](007-playbook-front-door.md) | PLAYBOOK.md — single front door: install / work / watch | P1 | M | 005, 006 | DONE 2026-07-04 ([#225](https://github.com/mattbutlerengineering/ai-tooling/issues/225)) |
| [008](008-staleness-activation.md) | Backfill Last-verified dates; gate field presence; surface the sweep | P2 | M | — | DONE ([#218](https://github.com/mattbutlerengineering/ai-tooling/issues/218)) |
| [009](009-measurement-protocols.md) | Per-signal measurement protocols + Test-design template block | P1 | M | — | DONE ([#219](https://github.com/mattbutlerengineering/ai-tooling/issues/219)) |
| [010](010-skill-eval-enforcement.md) | Skill-eval protocol: required section + `--skill-design` detector | P2 | S | 009 | DONE 2026-07-03 ([#221](https://github.com/mattbutlerengineering/ai-tooling/issues/221)) |
| [011](011-overlap-bakeoffs.md) | Bake-off protocol + Memory & Context pilot head-to-head | P2 | M | 009 | BLOCKED 2026-07-03 (pilot needs attended run — Steps 1-2 done) ([#222](https://github.com/mattbutlerengineering/ai-tooling/issues/222)) |
| [012](012-watchlist-staleness-timebomb.md) | Stop `make check` failing on a calendar date with zero commits | P1 | S | — | DONE 2026-08-03 ([#299](https://github.com/mattbutlerengineering/ai-tooling/issues/299)) |
| [013](013-audit-flag-parsing.md) | Make `audit-evals.py` flags compose; reject typos instead of silently changing the gate set | P1 | M | — | DONE 2026-08-03 ([#300](https://github.com/mattbutlerengineering/ai-tooling/issues/300)) |
| [014](014-parallel-install-resolver.md) | Resolve installs in parallel; add `make check-offline` | P2 | S | — | TODO |
| [015](015-derived-surface-numbers.md) | Stop hand-written numbers going stale inside derived surfaces | P2 | M | — | TODO |

Status values: TODO | IN PROGRESS | DONE | BLOCKED (with one-line reason) | REJECTED (with one-line rationale)

## Dependency notes

- **002 after 001**: both touch reconcile-counts.py/test_automation.py; 001 is smaller — land it first to avoid conflicts.
- **005 after 002**: the queue's stage-gap weight reads the Validated column 002 creates (005 has a documented inline fallback if run early).
- **006 after 005**: shares generator conventions (markers, `--check`, Makefile wiring); mirror rather than reinvent.
- **007 after 005+006**: the front door links NEXT-EVALS.md and WATCHLIST.md (has a reduced-scope fallback if run early).
- **010/011 after 009**: both apply the measurement protocols 009 defines; 009+010 edit TEMPLATE.md — land sequentially, never in parallel.
- **Independent lanes** (can run in parallel with anything): 003, 004, 008.
- Two tracks by theme: *consolidation* (001→002→005→006→007, plus 003/004) answers "one document, what to install/work/watch"; *rigor* (009→010→011, plus 008) answers "evaluate skills/tools better".

### Run 2 (012–015)

- **No hard dependencies.** All four touch different regions of different files and can run in any order, or in parallel.
- **Recommended order is 012 → 013 → 014 → 015**, by urgency rather than dependency: 012 has a dated deadline (see below), 013 fixes a gate that fails open, 014 and 015 are quality-of-life.
- **012 is time-critical.** `make check` will start failing on **2026-10-21** with zero commits — 184 evals cross their staleness thresholds in one day and `watchlist.py --check` byte-compares the page they render into. Land it before then or CI goes red on every PR and every unattended routine run.
- **Soft overlap 013 ↔ 014**: both edit `audit-evals.py`, but in different regions (`main()`'s flag block vs `audit_installs`/the network helpers). Landing them in either order is fine; landing them simultaneously in two worktrees will conflict only if one strays outside its declared scope.
- **Soft overlap 013 ↔ 014 ↔ 015 in `test_automation.py`**: each adds a *new* test class or method to a different area. Sequential landing avoids a trivial merge conflict at the bottom of the file.
- **012 and 015 both regenerate a derived page** (`WATCHLIST.md`, `NEXT-EVALS.md`). Run `make fix` after each so the tree stays green.

## Findings considered and rejected

- **Add a star/priority column to the CATALOG schema** — rejected for now; the promotion queue (005) ranks well on offline signals (overlap pressure + stage gap), and a schema change ripples through catalog_lib/add-catalog-entry/reconcile for marginal gain. Revisit only if the queue's ordering proves inadequate.
- **Split the MEASURED badge into rigor tiers (MEASURED-AB vs MEASURED-smoke)** — deferred; Evidence tokens are load-bearing across detectors B/K, backfill-evidence, tier-stack, COMPARISON. The Test-design block (009) records the same distinction as data without a token migration. Revisit after ~10 evals use the block.
- **Make the new detectors (workflow-drift, skill-design) gating immediately** — rejected; repo precedent is report-only first (`--overlaps` lifecycle), gate once quiet.
- **Numeric scoring for Maintainability/Safety signals** — rejected; they're judgment-heavy, and fake precision is the failure mode this repo exists to fight. Named-criteria rubrics instead (009).
- **Rewrite mem0-vs-claude-mem.md** — rejected; it's an honest SOURCE-ONLY record. The pilot bake-off (011) supersedes it by link.
- **Two-directional WORKFLOW↔STACK check** — rejected; WORKFLOW legitimately lists non-STACK options. The invariant is one-directional (every STACK pick appears in WORKFLOW).

### Run 2 (2026-08-03, audit at `a388dd2`)

Checked and found **not** to be problems — do not re-audit these:

- **`STACK.md`'s "~25 tools worth installing"** — verified accurate. STACK's install tables name 26 unique GitHub slugs, and `STACK-LEDGER.md` records 22 `In STACK? = yes` plus 4 `conditional`. The same phrase in `README.md:30` is likewise fine. (An earlier pass in this audit miscounted install-command *rows*, 36, as distinct tools.)
- **ReDoS in the detector regexes** — traced through `HONEST`, `NEGATION`, `PLACEHOLDER`, `_TRIGGER_RE` and the `EVAL_PATTERNS`/`TOTAL_PATTERNS` sets. No nested quantifier over an overlapping alternation; inputs are repo-local markdown, not user-supplied. Nothing to fix.
- **No `.env`, credential, or secret material** anywhere in the tree. No prompt-injection content found in any catalogued file's text.

Considered and deliberately **not** planned:

- **Migrate to single-source generation** (a data file that all markdown is generated from, replacing the markdown-as-source + validators design) — rejected as settled. ADR-0002 records markdown-as-source as a deliberate decision; the validator apparatus is the chosen consequence, not an accident. Re-litigating it is out of bounds for an audit.
- **`functools.cached_property` → precomputed context** in `DetectorContext` — rejected on measurement. The full offline detector set runs in ~1.2s; property re-derivation is not a meaningful share of `make check`'s 33.6s. The real cost is detector A's network round trips (plan 014).
- **SHA-pin the GitHub Actions in `integrity.yml`** (`actions/checkout@v4` → a commit SHA) — rejected for this repo. Both actions are first-party Anthropic-independent GitHub-published actions, the workflow has `permissions: contents: read`, and the repo holds no deployment credentials. The tag-mutation threat model doesn't justify the pin-maintenance burden here. Revisit if the workflow ever gains write permissions or a third-party action.
- **A shared `--check`/apply driver for the five generators** (`triage.py`, `watchlist.py`, `tier-stack.py`, `backfill-evidence.py`, `reconcile-counts.py`) — rejected as thin. Measured: 149 lines of `main()` across all five, mostly low similarity beyond the `"--check" in sys.argv` line. The genuinely shared logic already lives in `catalog_lib`. A driver would abstract ~30 lines and add an indirection to every generator.
- **Horizontally split `audit-evals.py`** (one module per detector) — rejected. The 18 `audit_*(ctx)` functions share one `DetectorContext` and several share derived maps (`comparison_verdict_map` feeds D, J and M). The file is long but cohesive by design, and the `#199` context seam already gives tests the decoupling a split would buy.
- **Rename `audit-evals.py` → `audit_evals.py`** so it can be imported normally instead of via `importlib.util.spec_from_file_location` — rejected as MED risk for cosmetic gain. The hyphenated name is referenced from `.claude/hooks/`, the opencode plugins, `Makefile`, `.github/workflows/integrity.yml`, `watchlist.py`, `next-evals.py`, `triage.py` and `test_automation.py`; a missed call site fails at runtime, not at import.
- **Refresh the 184 evals that go stale on 2026-10-21** — not a plan, because it is not an engineering task: each needs a genuine hands-on re-check, and back-dating or bulk-stamping them would assert verifications that never happened (`CLAUDE.md` forbids exactly this). Plan 012 removes the false CI failure; the real re-verification backlog stays visible in `WATCHLIST.md` and in `make check`'s staleness trailer.
