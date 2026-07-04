#!/usr/bin/env python3
"""
next-evals.py — derive NEXT-EVALS.md, a ranked promotion queue that answers "what
do we evaluate next" from data already in the repo (#plan-005).

Hundreds of catalogued tools sit at `discovery-log` — leads nothing selects for
evaluation. This ranks those leads, no hand-maintenance, the same derive-don't-
hand-maintain philosophy as tier-stack.py:

  score = 2*overlap_pressure + stage_gap_weight + evidence_bonus
    overlap_pressure  # of OTHER catalog rows citing this tool in "Overlaps with"
    stage_gap_weight  10*(1 - Validated/Tools) for the row's COMPARISON stage (0..10)
    evidence_bonus    +2 if the row's Evidence is REVIEW (some homework) else 0

The hungriest stages (fewest Validated per catalogued Tool) and the most-cited
tools float up. The weights are a starting heuristic — tune the constants below.

  ./next-evals.py          # apply: regenerate NEXT-EVALS.md
  ./next-evals.py --check  # verify only: exit 1 if stale; mutate nothing
"""
import os, sys, importlib.util
import catalog_lib

ROOT = os.path.dirname(os.path.abspath(__file__))
# Load audit-evals as a module (its filename is hyphenated) to reuse the shared
# overlap-pressure computation — never re-parse the "Overlaps with" cell here.
_spec = importlib.util.spec_from_file_location("audit_evals", os.path.join(ROOT, "audit-evals.py"))
ae = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(ae)

NEXT = os.path.join(ROOT, "NEXT-EVALS.md")
START, END = "<!-- NEXT-EVALS:START -->", "<!-- NEXT-EVALS:END -->"

# Formula weights — a starting heuristic (#plan-005); expect tuning after the first
# few queue-driven evals. Named and in one place so a tweak is a one-line change.
OVERLAP_WEIGHT = 2   # points per catalog peer that cites the tool
STAGE_GAP_MAX = 10   # ceiling of 10*(1 - Validated/Tools): hungriest stage highest
EVIDENCE_BONUS = 2   # REVIEW eval (some homework) over an unread SOURCE-ONLY lead
TOP_N = 25           # rows shown in NEXT-EVALS.md (the tail is counted, never capped silently)


def stage_gap_weight(section, breakdown, totals):
    """STAGE_GAP_MAX*(1 - Validated/Tools) for a COMPARISON stage — 0 when every
    catalogued tool in the stage is validated, near the max when almost none is.
    Returns 0.0 for a stage with no tools (nothing to be hungry about)."""
    tools = totals.get(section, 0)
    if not tools:
        return 0.0
    validated = breakdown.get(section, (0, 0))[0]
    return STAGE_GAP_MAX * (1 - validated / tools)


def rank(ctx):
    """(score, tool, stage, overlap_pressure, gap) for every discovery-log
    COMPARISON row, best first. ONLY discovery-log rows are candidates — an
    ADOPT/KEEP/SKIP/CONDITIONAL/DEFER row is already evaluated, never queued.
    Ties break on higher overlap_pressure, then tool name, so the order is stable
    (the --check gate depends on it)."""
    by_section = catalog_lib.comparison_rows_by_section(ctx.comparison)
    breakdown = catalog_lib.comparison_verdict_breakdown(ctx.comparison)
    totals = catalog_lib.comparison_body_counts(ctx.comparison)
    pressure = ae.overlap_pressure_map(ctx)   # cited name_key -> set of citing rows
    amap = ctx.evidence_alias_map
    ranked = []
    for section, rows in by_section.items():
        gap = stage_gap_weight(section, breakdown, totals)
        for r in rows:
            if r.verdict != "discovery-log":
                continue
            citing = set()
            for k in catalog_lib.alias_keys(r.tool):
                citing |= pressure.get(k, set())
            op = len(citing)
            bonus = EVIDENCE_BONUS if catalog_lib.evidence_lookup(amap, r.tool) == "REVIEW" else 0
            score = OVERLAP_WEIGHT * op + gap + bonus
            ranked.append((score, r.tool, section, op, gap))
    ranked.sort(key=lambda t: (-t[0], -t[3], t[1]))
    return ranked


def render(ranked):
    """The full NEXT-EVALS.md text from the ranked candidates. Fully regenerated
    each run (markers wrap the table so a future tool can locate the block)."""
    shown = ranked[:TOP_N]
    total = len(ranked)
    dropped = total - len(shown)
    lines = [
        "# Next evals — a ranked promotion queue",
        "",
        "The `discovery-log` leads most worth evaluating next, **derived** (not "
        "hand-maintained) from data already in the repo. Regenerate with "
        "`python3 next-evals.py`; do not edit between the markers.",
        "",
        "Score = `2*overlap_pressure + stage_gap_weight + evidence_bonus`, where "
        "`overlap_pressure` is how many other catalog rows cite the tool in "
        '"Overlaps with", `stage_gap_weight` is `10*(1 - Validated/Tools)` for the '
        "tool's [COMPARISON.md](COMPARISON.md) stage (hungriest stage highest), and "
        "`evidence_bonus` is +2 when some homework exists (Evidence `REVIEW`). The "
        "weights are a starting heuristic — see `next-evals.py`. The queue *selects*; "
        "a human or attended agent runs `/evaluate-tool` (unattended runs produce thin "
        "verdicts the fabrication gates exist to catch).",
        "",
        f"_Showing the top {len(shown)} of {total} discovery-log candidates — "
        f"{dropped} not shown (no silent cap: rerun and read the source for the tail)._",
        "",
        START,
        "",
        "| Rank | Tool | Stage | Score | Why (pressure/gap) | Eval command |",
        "|------|------|-------|-------|--------------------|--------------|",
    ]
    for i, (score, tool, stage, op, gap) in enumerate(shown, 1):
        why = f"pressure {op}, gap {gap:.1f}"
        lines.append(f"| {i} | {tool} | {stage} | {score:.1f} | {why} | `/evaluate-tool {tool}` |")
    lines += ["", END, ""]
    return "\n".join(lines)


def apply(ctx):
    return render(rank(ctx))


def main():
    check = "--check" in sys.argv[1:]
    ctx = ae.DetectorContext(ROOT)
    new = apply(ctx)
    current = open(NEXT, encoding="utf-8").read() if os.path.exists(NEXT) else None
    if check:
        if new != current:
            print("next-evals check: DRIFT — NEXT-EVALS.md is stale; run ./next-evals.py")
            sys.exit(1)
        print("next-evals check: OK — NEXT-EVALS.md matches the derived queue")
        sys.exit(0)
    if new != current:
        open(NEXT, "w", encoding="utf-8").write(new)
        print("next-evals: regenerated NEXT-EVALS.md")
    else:
        print("next-evals: NEXT-EVALS.md already up to date")


if __name__ == "__main__":
    main()
