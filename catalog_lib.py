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
(via python3 -c, #195). The same-tool keying (#197) and the triple-key
evidence lookup (#201) live here as well, next to the parsers they serve.

All functions are pure (text/values in, value out) — callers read the files.
"""
import collections
import re

# The verdict vocabulary (ADR 0001, docs/decisions/0001-verdict-vocabulary.md).
# Defined once here; COMPARISON-row consumers reference this tuple. (The eval-file
# ## Verdict parser in audit-evals deliberately keeps its own narrower inline set —
# an eval can't carry discovery-log, which is a COMPARISON-only status.)
VERDICTS = ("ADOPT", "CONDITIONAL", "SKIP", "DEFER", "KEEP", "discovery-log")
_VERDICT_SET = frozenset(VERDICTS)

# The subset of VERDICTS that are *genuine* evaluation verdicts. discovery-log is
# a catalogued lead, not a verdict ("surfaced in triage but never exercised") — the
# Legend's split, in code (#plan-002). Used by the COMPARISON Summary's Validated
# funnel: Validated counts real verdicts only, discovery-log excluded.
REAL_VERDICTS = frozenset({"ADOPT", "KEEP", "CONDITIONAL", "SKIP", "DEFER"})
# ADOPT/KEEP are the "Recommended" subset (adopt-in-all-projects or validated-keep).
RECOMMENDED_VERDICTS = frozenset({"ADOPT", "KEEP"})


def is_real_verdict(token):
    """True iff `token` is a genuine evaluation verdict (ADR 0001), excluding
    discovery-log — a lead surfaced in triage, not a verdict. This is the domain
    rule that splits COMPARISON's Validated funnel from its raw catalogued count."""
    return token in REAL_VERDICTS

# cells carries the full row for the row-shape validation slice (#198) — the
# validate_row() work ADR-0002 lists as falling out of this centralized parser.
ComparisonRow = collections.namedtuple("ComparisonRow", "tool verdict cells")

# A CATALOG.md entry row (#196). name is the link text for linked rows, the raw
# first cell for unlinked ones (OMEGA, server-github); url is None when unlinked.
# one_liner/overlaps are None when the row is short; cells again carries the full
# row for #198. The positional fields assume CATALOG's 5-column shape — on a
# COMPARISON-shaped row only name/type/cells are meaningful (validate_catalog_rows /
# validate_comparison_rows, #198, enforce shape).
CatalogRow = collections.namedtuple("CatalogRow", "name url type one_liner overlaps cells")

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


# The parenthetical qualifier in a tool name: "GSD (Get Shit Done)" → "GSD".
_PARENTHETICAL = re.compile(r"\s*\(.*?\)")


def strip_parenthetical(s):
    """Drop parenthetical qualifiers: 'GSD (Get Shit Done)' → 'GSD'."""
    return _PARENTHETICAL.sub("", s)


def name_key(s):
    """THE canonical same-tool identity key (#197): lowercased, non-alphanumerics
    collapsed away — 'claude-mem', 'Claude Mem', and 'claude_mem' key identically.
    Parenthetical content is KEPT: it can be the only discriminator between rows
    ('awesome-claude-skills (Composio)' vs '(travisvn)'), so dropping it here
    would collide distinct tools. Identity maps register under identity_keys
    (full + stripped); lookups fan out — identity_keys against identity maps,
    alias_keys (which adds basenames) against alias/STACK maps. The retired
    trio (_norm / _drift_key / _OVL_STRIP) keyed the same rows three ways."""
    return re.sub(r"[^a-z0-9]", "", s.lower())


def identity_keys(name):
    """The keys a tool row REGISTERS under, and that lookups against an identity
    map (COMPARISON verdicts, the STACK ledger) may try: the full name and the
    parenthetical-stripped form. Deliberately excludes basenames — a slash-name
    ('vercel-labs/agent-skills') must never shadow or match the distinct tool
    its basename spells ('agent-skills'); basenames are an alias_keys-only
    fallback for maps that need cross-name matching (eval aliases, STACK)."""
    keys = [name_key(name)]
    stripped = name_key(strip_parenthetical(name))
    if stripped and stripped not in keys:
        keys.append(stripped)
    return keys


def alias_keys(name, url=None):
    """Every key a lookup for `name` should try, most-specific first: the full
    name, the parenthetical-stripped form ('GSD (Get Shit Done)' → 'gsd'), the
    slash-basename ('owner/repo' → 'repo'), and the repo basename of `url` — so
    an entry installed under another name (GSD ← obra/superpowers) still
    matches. Ordered and deduped so callers trying keys in sequence keep
    full-name precedence."""
    cands = [name, strip_parenthetical(name), name.split("/")[-1]]
    if url:
        cands.append(url.rstrip("/").split("/")[-1])
    keys = []
    for c in cands:
        k = name_key(c)
        if k and k not in keys:
            keys.append(k)
    return keys


def evidence_lookup(alias_map, name, url=None):
    """The ONE triple-key evidence lookup (#201): fan `name` (and `url`) out
    through alias_keys against `alias_map` (alias name_key → Evidence level,
    most-specific key wins) and default to SOURCE-ONLY — a name with no eval
    has no evaluation evidence, only metadata. tier-stack and backfill-evidence
    both route through here instead of re-implementing the fan-out; the map
    itself is built once by DetectorContext.evidence_alias_map (audit-evals)."""
    return next((alias_map[k] for k in alias_keys(name, url) if k in alias_map),
                "SOURCE-ONLY")


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


def is_body_row(line):
    """Public predicate: a CATALOG/COMPARISON-style entry row — first cell a name
    (linked or not), second cell in the Type vocabulary. Header, separator, and
    prose lines are not body rows. (#196)"""
    return bool(_BODY_ROW.match(line))


# The leading link cell of a CATALOG row: [name](url).
_LINK_CELL = re.compile(r"^\[([^\]]+)\]\(([^)]*)\)")


def parse_catalog_rows(text):
    """Every CATALOG-style entry row in `text` as CatalogRow records, fields by
    name instead of positional cell indexing (#196). The Evaluation class and
    detectors F, M, N all route through here; backfill-evidence uses the same
    predicate. Works on any text carrying such rows — CATALOG.md itself or the
    catalog-row copy inside an eval file."""
    rows = []
    for line in text.splitlines():
        if not _BODY_ROW.match(line):
            continue
        cells = _row_cells(line)
        m = _LINK_CELL.match(cells[0])
        name, url = (m.group(1), m.group(2)) if m else (cells[0], None)
        cell = lambda i: cells[i] if len(cells) > i else None
        rows.append(CatalogRow(name, url, cell(1), cell(2), cell(4), cells))
    return rows


# CATALOG.md's documented column count: Name | Type | One-liner | Problem | Overlaps.
CATALOG_COLUMNS = 5


def validate_catalog_rows(text):
    """(line_no, problem) findings for CATALOG table lines that would otherwise
    be silently skipped or mis-parsed (#198): a pipe-line that isn't a header,
    separator, or recognized entry row; entry rows whose cell count isn't
    CATALOG_COLUMNS (a missing cell silently shifts every field after it); an
    indented row (markdown renders it, the ^|-anchored parsers and counters
    skip it); and an empty Name cell (counted, but nameless). A clean tree
    returns []."""
    problems = []
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if not line.lstrip().startswith("|") or _SEPARATOR_ROW.match(line):
            continue
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        if _SEPARATOR_ROW.match(nxt):
            continue  # header row (structural: the row above a |---| separator)
        cells = _row_cells(line)
        if line != line.lstrip():
            problems.append((i + 1, "indented table row (markdown renders it, but the parsers and counters skip it)"))
        elif not _BODY_ROW.match(line):
            got = repr(cells[1]) if len(cells) > 1 else "missing"
            problems.append((i + 1, f"not a recognized entry row (Type cell {got} not in the Type vocabulary)"))
        elif len(cells) != CATALOG_COLUMNS:
            problems.append((i + 1, f"expected {CATALOG_COLUMNS} cells, found {len(cells)} cells"))
        elif not cells[0]:
            problems.append((i + 1, "empty Name cell (row is counted, but nameless)"))
    return problems


def validate_comparison_rows(text):
    """(line_no, problem) findings for COMPARISON per-stage table rows (#198):
    inside any table whose header carries an 'Evaluated' column — the same
    anchor comparison_verdict_rows uses, so a table the parser consumes is
    always validated — every body row must match the header's width, hold a
    verdict token in its Evaluated cell, and name a tool in its first cell.
    The '## Summary' section is excluded by section (its header also says
    'Evaluated' but its rows are aggregate counts, not tool rows — the same
    exclusion comparison_body_counts applies). A clean tree returns []."""
    problems = []
    lines = text.splitlines()
    hdr_cols = vcol = None
    in_summary = False
    for i, line in enumerate(lines):
        hm = re.match(r"^##\s+(.*)", line)
        if hm:
            in_summary = hm.group(1).strip().lower() == "summary"
        if not line.lstrip().startswith("|"):
            hdr_cols = vcol = None
            continue
        if _SEPARATOR_ROW.match(line):
            continue
        cells = _row_cells(line)
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        if _SEPARATOR_ROW.match(nxt):
            if not in_summary and "Evaluated" in cells:
                hdr_cols, vcol = len(cells), cells.index("Evaluated")
            else:
                hdr_cols = vcol = None  # Summary or foreign table
            continue
        if hdr_cols is None:
            continue
        if len(cells) != hdr_cols:
            problems.append((i + 1, f"expected {hdr_cols} cells, found {len(cells)} cells"))
        elif cells[vcol] not in _VERDICT_SET:
            problems.append((i + 1, f"Evaluated cell {cells[vcol]!r} is not a verdict token"))
        elif not cells[0]:
            problems.append((i + 1, "empty Tool cell (row carries a verdict, but no name)"))
    return problems


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
                sec = strip_parenthetical(t).strip()
                body.setdefault(sec, 0)
            continue
        if in_summary:
            continue
        if sec and _BODY_ROW.match(l):
            body[sec] += 1
    return body


def comparison_verdict_breakdown(comparison_text):
    """Per '## Section' of COMPARISON.md, a (validated, recommended) count pair:
    validated = body rows whose Evaluated cell is a real verdict (discovery-log
    excluded, per ADR 0001); recommended = the ADOPT+KEEP subset. Section tracking
    mirrors comparison_body_counts; the Evaluated column is anchored via each table's
    header row exactly as comparison_verdict_rows does (never a fixed offset). The
    '## Summary' section is excluded. This is the source the Summary's Validated
    funnel is rebuilt from (reconcile) and gated against (detector G)."""
    breakdown, sec, in_summary, vcol = {}, None, False, None
    lines = comparison_text.splitlines()
    for i, l in enumerate(lines):
        hm = re.match(r"^##\s+(.*)", l)
        if hm:
            t = hm.group(1).strip()
            if t.lower() == "summary":
                in_summary, sec = True, None
            else:
                in_summary = False
                sec = strip_parenthetical(t).strip()
                breakdown.setdefault(sec, [0, 0])
            vcol = None
            continue
        if not l.lstrip().startswith("|"):
            vcol = None  # table ended
            continue
        if in_summary or _SEPARATOR_ROW.match(l):
            continue
        cells = _row_cells(l)
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        if _SEPARATOR_ROW.match(nxt):
            vcol = cells.index("Evaluated") if "Evaluated" in cells else None
            continue
        if sec is None or vcol is None or vcol >= len(cells):
            continue
        v = cells[vcol]
        if is_real_verdict(v):
            breakdown[sec][0] += 1
            if v in RECOMMENDED_VERDICTS:
                breakdown[sec][1] += 1
    return {k: tuple(v) for k, v in breakdown.items()}


def comparison_rows_by_section(text):
    """{section -> [ComparisonRow]} for COMPARISON.md — every verdict-bearing body
    row grouped by its '## Section' (parenthetical stripped). Section tracking and
    Evaluated-column anchoring are identical to comparison_verdict_breakdown (never
    a fixed offset); the '## Summary' section is excluded. Lets a caller that needs
    a row's *stage* — not just its verdict — avoid re-parsing COMPARISON (next-evals
    keys candidates to their stage this way, #plan-005)."""
    out, sec, in_summary, vcol = {}, None, False, None
    lines = text.splitlines()
    for i, l in enumerate(lines):
        hm = re.match(r"^##\s+(.*)", l)
        if hm:
            t = hm.group(1).strip()
            if t.lower() == "summary":
                in_summary, sec = True, None
            else:
                in_summary = False
                sec = strip_parenthetical(t).strip()
                out.setdefault(sec, [])
            vcol = None
            continue
        if not l.lstrip().startswith("|"):
            vcol = None  # table ended
            continue
        if in_summary or _SEPARATOR_ROW.match(l):
            continue
        cells = _row_cells(l)
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        if _SEPARATOR_ROW.match(nxt):
            vcol = cells.index("Evaluated") if "Evaluated" in cells else None
            continue
        if sec is None or vcol is None or vcol >= len(cells):
            continue
        if cells[vcol] in _VERDICT_SET:
            out[sec].append(ComparisonRow(cells[0], cells[vcol], cells))
    return out
