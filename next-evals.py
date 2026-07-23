#!/usr/bin/env python3
"""
next-evals.py — score the `discovery-log` leads (#plan-005). The scoring module
behind the promotion queue; `triage.py` bands and renders NEXT-EVALS.md from it.

Hundreds of catalogued tools sit at `discovery-log` — leads nothing selects for
evaluation. This ranks those leads, no hand-maintenance, the same derive-don't-
hand-maintain philosophy as tier-stack.py:

  score = 2*overlap_pressure + stage_gap_weight + evidence_bonus
    overlap_pressure  # of OTHER catalog rows citing this tool in "Overlaps with"
    stage_gap_weight  10*(1 - Validated/Tools) for the row's COMPARISON stage (0..10)
    evidence_bonus    +2 if the row's Evidence is REVIEW (some homework) else 0

The hungriest stages (fewest Validated per catalogued Tool) and the most-cited
tools float up. The weights are a starting heuristic — tune the constants below.

The score picks a HEAD, not a total order: 176 leads score zero overlap pressure
and the 461 collapse into ~83 distinct values, so triage.py uses it to rank within
a band rather than to sort the whole queue. This file has no CLI — run triage.py.
"""
import os, importlib.util
import catalog_lib

ROOT = os.path.dirname(os.path.abspath(__file__))
# Load audit-evals as a module (its filename is hyphenated) to reuse the shared
# overlap-pressure computation — never re-parse the "Overlaps with" cell here.
_spec = importlib.util.spec_from_file_location("audit_evals", os.path.join(ROOT, "audit-evals.py"))
ae = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(ae)

# Formula weights — a starting heuristic (#plan-005); expect tuning after the first
# few queue-driven evals. Named and in one place so a tweak is a one-line change.
OVERLAP_WEIGHT = 2   # points per catalog peer that cites the tool
STAGE_GAP_MAX = 10   # ceiling of 10*(1 - Validated/Tools): hungriest stage highest
EVIDENCE_BONUS = 2   # REVIEW eval (some homework) over an unread SOURCE-ONLY lead


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
