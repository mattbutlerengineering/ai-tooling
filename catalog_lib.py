"""
catalog_lib.py — the single source of truth for how CATALOG.md and COMPARISON.md
are parsed: entry counting, and (#193) the verdict vocabulary and verdict-row
parsing that detectors D, J, and M consume.

`reconcile-counts.py` *writes* the counts that `audit-evals.py` detector G
*checks* — two halves of one contract. They used to re-implement this parsing
independently, so a change to one could silently diverge from the other. Both now
import from here, so they provably agree by construction. The same argument
centralizes the COMPARISON verdict-row parse (ADR-0002's shared-parser seam):
three detectors used to carry byte-identical fixed-offset regexes.
`sync-plugin-docs.sh`'s apply-mode verify block counts through here too
(via python3 -c, #195).

All functions are pure (text in, value out) — callers read the files.
"""
import collections
import re

# The verdict vocabulary (ADR 0001, docs/decisions/0001-verdict-vocabulary.md).
# Defined once here; COMPARISON-row consumers reference this tuple. (The eval-file
# ## Verdict parser in audit-evals deliberately keeps its own narrower inline set —
# an eval can't carry discovery-log, which is a COMPARISON-only status.)
VERDICTS = ("ADOPT", "CONDITIONAL", "SKIP", "DEFER", "KEEP", "discovery-log")
_VERDICT_SET = frozenset(VERDICTS)

# cells carries the full row for the row-shape validation slice (#198) — the
# validate_row() work ADR-0002 lists as falling out of this centralized parser.
ComparisonRow = collections.namedtuple("ComparisonRow", "tool verdict cells")

# A markdown table separator row: |---|---| (alignment colons allowed).
_SEPARATOR_ROW = re.compile(r"^\s*\|[\s:|-]+\|\s*$")

# What counts as a catalog/comparison entry row: the Type column vocabulary.
ROW_TYPE = r"(?:MCP server|tool|skill|plugin|framework|harness|platform|reference)"
_BODY_ROW = re.compile(rf"^\|\s*[^|]+\|\s*{ROW_TYPE}\s*\|")

# A github.com/owner/repo slug: owner/repo, an optional .git suffix dropped, bounded
# by a closing paren, whitespace, quote, '#', '/', or end-of-string. Shared by the
# link-rot and archived-repo detectors so the extraction can't drift between them.
_GITHUB_SLUG = re.compile(r"github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+?)(?:\.git)?(?=[)\s\"'#/]|$)")


def github_repos(text):
    """Sorted, de-duplicated owner/repo slugs of every github.com link in `text`."""
    return sorted(set(_GITHUB_SLUG.findall(text)))


def _row_cells(line):
    """Cell contents of a markdown table row, outer pipes dropped."""
    parts = [p.strip() for p in line.split("|")]
    if parts and parts[0] == "":
        parts = parts[1:]
    if parts and parts[-1] == "":
        parts = parts[:-1]
    return parts


def comparison_verdict_rows(text):
    """Every COMPARISON.md body row carrying a verdict, as ComparisonRow records
    (tool = first cell, verdict, cells = the full row). Detectors D, J, and M all
    route through here (#193).

    The verdict cell is located via the enclosing table's header row (the
    'Evaluated' column) — never a fixed column offset — so inserting or appending
    a column (as backfill-evidence did with Evidence) cannot silently un-match
    rows. A table without an 'Evaluated' header contributes no rows; a cell that
    isn't a verdict token (Summary counts, separators) is never emitted."""
    rows, vcol = [], None
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if not line.lstrip().startswith("|"):
            vcol = None  # table ended (blank line, heading, prose)
            continue
        cells = _row_cells(line)
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        if _SEPARATOR_ROW.match(nxt):
            # A header row is structural — the row above a |---| separator — so a
            # body cell reading "Evaluated" can't re-anchor, and every new table
            # re-anchors or clears vcol even with no blank line between tables.
            vcol = cells.index("Evaluated") if "Evaluated" in cells else None
            continue
        if vcol is None or vcol >= len(cells):
            continue
        if cells[vcol] in _VERDICT_SET:
            rows.append(ComparisonRow(cells[0], cells[vcol], cells))
    return rows


def catalog_count(catalog_text):
    """Number of entry rows in CATALOG.md — table rows minus header/separator."""
    return sum(1 for l in catalog_text.splitlines()
               if l.startswith("| ") and not l.startswith("| Name") and not l.startswith("|---"))


def comparison_body_counts(comparison_text):
    """Body rows per '## Section' of COMPARISON.md (parenthetical stripped),
    excluding the '## Summary' section. This is the count detector G compares
    against the summary table and that reconcile rebuilds the summary from."""
    body, sec, in_summary = {}, None, False
    for l in comparison_text.splitlines():
        hm = re.match(r"^##\s+(.*)", l)
        if hm:
            t = hm.group(1).strip()
            if t.lower() == "summary":
                in_summary, sec = True, None
            else:
                in_summary = False
                sec = re.sub(r"\s*\(.*?\)", "", t).strip()
                body.setdefault(sec, 0)
            continue
        if in_summary:
            continue
        if sec and _BODY_ROW.match(l):
            body[sec] += 1
    return body
