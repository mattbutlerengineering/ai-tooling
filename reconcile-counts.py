#!/usr/bin/env python3
"""
reconcile-counts.py — derive the catalog tool-count from CATALOG.md and write it
everywhere it is quoted, and rebuild COMPARISON.md's per-stage summary from its own
body rows. The deterministic, error-prone half of adding a catalog entry.

Where audit-evals.py detector G *checks* that COMPARISON == CATALOG, this script
*fixes* them: insert your CATALOG row and your COMPARISON body row, then run this to
propagate every count. Idempotent — a no-op when everything already agrees.

  python3 reconcile-counts.py            # apply fixes, print what changed
  python3 reconcile-counts.py --check    # report drift, change nothing, exit 1 if any

Updates the catalog tool-count in README.md, CLAUDE.md, STACK.md, plugin/CLAUDE.md,
and COMPARISON.md (header + summary rows + Total), plus the eval-file count quoted
in README.md/STACK.md (derived from evaluations/*.md, excluding TEMPLATE.md). Does
NOT touch plugin/docs/ (run ./sync-plugin-docs.sh for the latter).
"""
import glob
import importlib.util
import os
import re
import sys
from pathlib import Path

import catalog_lib
from catalog_lib import comparison_body_counts, comparison_verdict_breakdown

ROOT = os.path.dirname(os.path.abspath(__file__))

# The composition below is derived from each eval's own headline verdict, and that
# parsing already exists in audit-evals.py. Load it rather than re-implement it
# (watchlist.py's rule): a second `## Verdict` regex here would drift from detector
# D's the first time the vocabulary changed.
_spec = importlib.util.spec_from_file_location("audit_evals", os.path.join(ROOT, "audit-evals.py"))
if _spec is None or _spec.loader is None:  # a sibling in this repo — absent means a broken checkout
    raise ImportError("cannot load audit-evals.py from " + ROOT)
ae = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(ae)

def read(p):  return Path(ROOT, p).read_text(encoding="utf-8")
def write(p, s): Path(ROOT, p).write_text(s, encoding="utf-8")

def catalog_count(root=None):
    # `root` is injectable for tests (#199); the CLI always counts this repo's tree.
    text = Path(root or ROOT, "CATALOG.md").read_text(encoding="utf-8")
    return catalog_lib.catalog_count(text)

def eval_count(root=None):
    # Derived eval-file count: every evaluations/*.md except the TEMPLATE.
    # `root` is injectable for tests, mirroring catalog_count().
    files = glob.glob(os.path.join(root or ROOT, "evaluations", "*.md"))
    return sum(1 for f in files if os.path.basename(f) != "TEMPLATE.md")

def eval_composition(root=None):
    """(verdicts, leads, other) across the same files eval_count() counts.

    `evaluations/` holds three kinds of file and the front page used to call all of
    them the first kind (#435):

      verdicts  a real `## Verdict` headline — ADOPT / KEEP / CONDITIONAL / SKIP / DEFER.
      leads     headlines `discovery-log`, the word #324 introduced across 324 files
                precisely so a lead stops "announcing a verdict it is not entitled to".
                Counting these as verdicts re-announces it in aggregate.
      other     no headline verdict at all: bulk-triage stubs with no `## Verdict`
                section, plus comparison documents whose Verdict names a winner among
                several tools (`cluster-memory`, `mem0-vs-claude-mem`) — legitimate,
                and not an evaluation of one tool. Detector AD's rule.

    The three partition the total, so README's line always adds up to eval_count()."""
    ctx = ae.DetectorContext(root or ROOT)
    verdicts = leads = other = 0
    for e in ctx.evals:
        if e.verdict == "discovery-log":
            leads += 1
        elif e.verdict:
            verdicts += 1
        else:
            other += 1
    return verdicts, leads, other


# count strings that quote the catalog total, by file
TOTAL_PATTERNS = [
    (r"(inventory of )\d+( tools)", r"\g<1>{C}\g<2>"),
    (r"\b\d+( catalog entries)", r"{C}\g<1>"),
    (r"\b\d+( tools(?:\*\*)? are cataloged)", r"{C}\g<1>"),
    (r"(distilled from )\d+( catalog entries)", r"\g<1>{C}\g<2>"),
]

def fix_total_strings(text, C):
    for pat, repl in TOTAL_PATTERNS:
        text = re.sub(pat, repl.replace("{C}", str(C)), text)
    return text

# count strings that quote the eval-file total (README.md / STACK.md). The
# "evidence-based" variant runs first so its number isn't left behind by the
# bare-"evaluations" pattern. Anchored on the word "evaluations" so unrelated
# numbers (issue refs, dates) are never touched.
EVAL_PATTERNS = [
    # plugin/CLAUDE.md phrases the same count as "N evaluation and comparison files".
    # It has always been in FILES_TOTAL, but neither pattern below matched that
    # wording, so the number drifted 87 behind while the catalog count on the line
    # above it stayed correct — the most misleading kind of stale number.
    # `evidence-based` is optional because #435 struck it from that line: the phrase
    # asserted every file carries evidence when 258 of them are leads. The number must
    # stay reconciled either way, so the adjective may come and go without the count
    # silently stopping.
    (r"\b\d+( (?:evidence-based )?evaluation and comparison files)", r"{E}\g<1>"),
    (r"\b\d+( evidence-based evaluations)", r"{E}\g<1>"),
    (r"\b\d+( evaluations)", r"{E}\g<1>"),
    (r"\b\d+( evaluation files)", r"{E}\g<1>"),
]

# The composition, which is what stops the total carrying a claim the files do not
# support (#435). Each is anchored on its own trailing phrase, so the three numbers can
# never be swapped by a regex that matched the wrong one — and because they partition
# the total, a drifted copy is arithmetic a reader can catch, not just a stale digit.
# Ordered to match eval_composition()'s (verdicts, leads, other) tuple.
COMPOSITION_PATTERNS = [
    r"\b\d+( carrying a verdict)",
    r"\b\d+( still at `discovery-log`)",
    r"\b\d+( stubs and comparison documents)",
]

def fix_eval_strings(text, E, composition=None):
    for pat, repl in EVAL_PATTERNS:
        text = re.sub(pat, repl.replace("{E}", str(E)), text)
    if composition:
        for pat, value in zip(COMPOSITION_PATTERNS, composition, strict=True):
            text = re.sub(pat, f"{value}\\g<1>", text)
    return text

def _pct(num, den):
    """Integer percent num/den (0% when den is 0), for the Validated % column."""
    return f"{round(100 * num / den)}%" if den else "0%"

# The existing Summary stage rows: first cell a plain name (no | or *), second cell
# a bare int. Header ('Tools' 2nd cell), separator, and the bold Total row don't match.
_SUMMARY_STAGE_ROW = re.compile(r"^\|\s*([A-Za-z][^|*]+?)\s*\|\s*\d+\s*\|")

def _summary_stages(text):
    """Ordered stage names in the existing '## Summary' table (header/Total excluded).
    fix_comparison rebuilds these rows' values in place — it never invents a stage row
    or drops one, so sections absent from the summary (e.g. Legend) stay absent."""
    stages, in_summary = [], False
    for line in text.splitlines():
        hm = re.match(r"^##\s+(.*)", line)
        if hm:
            in_summary = hm.group(1).strip().lower() == "summary"
            continue
        if in_summary:
            m = _SUMMARY_STAGE_ROW.match(line)
            if m:
                stages.append(m.group(1).strip())
    return stages

def _build_summary_table(stages, body, breakdown, C):
    """The regenerated Summary table lines: honest funnel columns
    'Stage | Tools | Validated | Recommended | Validated %'. Tools is the body-row
    count; Validated counts real verdicts (discovery-log excluded); Recommended is
    ADOPT+KEEP; Validated % = Validated/Tools. Total keeps Tools=C so detector G's
    CATALOG==COMPARISON check still compares the catalogued total."""
    rows = ["| Stage | Tools | Validated | Recommended | Validated % |",
            "|-------|-------|-----------|-------------|-------------|"]
    tv = tr = 0
    for s in stages:
        tools = body.get(s, 0)
        val, rec = breakdown.get(s, (0, 0))
        tv += val; tr += rec
        rows.append(f"| {s} | {tools} | {val} | {rec} | {_pct(val, tools)} |")
    rows.append(f"| **Total** | **{C}** | **{tv}** | **{tr}** | **{_pct(tv, C)}** |")
    return rows

def fix_comparison(text, C):
    body = comparison_body_counts(text)
    breakdown = comparison_verdict_breakdown(text)
    # header "All N tools from CATALOG.md"
    text = re.sub(r"(All )\d+( tools from CATALOG\.md)", rf"\g<1>{C}\g<2>", text)
    stages = _summary_stages(text)
    table = _build_summary_table(stages, body, breakdown, C)
    # Replace the whole '## Summary' table (header→Total) with the regenerated one,
    # emitted where the first table row was; non-table lines in the section pass through.
    out, in_summary, written = [], False, False
    for line in text.splitlines():
        hm = re.match(r"^##\s+(.*)", line)
        if hm:
            in_summary = hm.group(1).strip().lower() == "summary"
            written = False
            out.append(line)
            continue
        if in_summary and line.lstrip().startswith("|"):
            if not written:
                out.extend(table)
                written = True
            continue  # drop original table rows
        out.append(line)
    result = "\n".join(out)
    if text.endswith("\n"):
        result += "\n"
    return result

FILES_TOTAL = ["README.md", "CLAUDE.md", "STACK.md", "plugin/CLAUDE.md"]

def main():
    check = "--check" in sys.argv[1:]
    C = catalog_count()
    E = eval_count()
    comp = eval_composition()
    changed = []
    for f in FILES_TOTAL:
        if not os.path.exists(os.path.join(ROOT, f)):
            continue
        s = read(f); s2 = fix_eval_strings(fix_total_strings(s, C), E, comp)
        if s2 != s:
            changed.append(f)
            if not check: write(f, s2)
    s = read("COMPARISON.md"); s2 = fix_comparison(fix_total_strings(s, C), C)
    if s2 != s:
        changed.append("COMPARISON.md")
        if not check: write("COMPARISON.md", s2)
    if changed:
        verb = "would update" if check else "updated"
        print(f"reconcile: catalog count = {C}, eval count = {E} "
              f"({comp[0]} verdicts / {comp[1]} leads / {comp[2]} other); "
              f"{verb} {len(changed)} file(s): {', '.join(changed)}")
        sys.exit(1 if check else 0)
    print(f"reconcile: OK — catalog count = {C}, eval count = {E} "
          f"({comp[0]} verdicts / {comp[1]} leads / {comp[2]} other), "
          "all count strings already consistent")
    sys.exit(0)

if __name__ == "__main__":
    main()
