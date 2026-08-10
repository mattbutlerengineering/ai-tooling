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

# The verdict vocabulary (ADR-0005, docs/adr/0005-verdict-vocabulary.md).
# Defined once here; both the COMPARISON-row consumers and the eval-file ## Verdict
# parser in audit-evals build from this tuple. discovery-log used to be treated as a
# COMPARISON-only status, which left 324 lead evals headlining **CONDITIONAL** — a
# word ADR-0005 reserves for tools we actually exercised (#324). A lead's eval now
# headlines `discovery-log` and reads as the tentative note it is.
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
# row for #198. The positional fields assume CATALOG's column shape — on a
# COMPARISON-shaped row only name/type/cells are meaningful (validate_catalog_rows /
# validate_comparison_rows, #198, enforce shape).
#
# ships_inside (#343) is the LAST field and empty on almost every row: the artifact you
# actually install to get this one, when that is not this row's own repo. It is appended
# rather than inserted precisely so that name/type/one_liner/overlaps keep their indices —
# the ~520 embedded `## Catalog entry` mirrors stay 5-column, and detector U, which
# compares type/one_liner/overlaps positionally, cannot see the difference. Same reasoning
# that let COMPARISON.md gain its Evidence column without perturbing detector G.
CatalogRow = collections.namedtuple(
    "CatalogRow", "name url type one_liner overlaps cells ships_inside")

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


# An HTML comment. Stripped before matching a CLAIM, never before matching PROVENANCE
# about one — detector AC's rule (#417), generalised in #451 after detector Q read
# TEMPLATE.md's own guidance comment ("OPTIONAL next line: **Last triaged:** …") as a
# triage stamp, so every eval created the documented way failed a gating detector.
#
# The distinction is load-bearing rather than stylistic, because some provenance markers
# ARE comments: `<!-- triaged: bulk -->` and `<!-- backfilled from last git edit -->` say
# something about a claim and must stay readable in the raw text. A blanket strip would
# delete them along with the noise, which is why this is a helper the caller applies to
# the claim side only, and never a flag on the reader.
_HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)


def strip_html_comments(text):
    """`text` with every HTML comment removed."""
    return _HTML_COMMENT.sub("", text)


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
        cell = lambda i, cells=cells: cells[i] if len(cells) > i else None
        rows.append(CatalogRow(name, url, cell(1), cell(2), cell(4), cells,
                               cell(SHIPS_INSIDE_COL) or ""))
    return rows


# CATALOG.md's column shape: Name | Type | One-liner | Problem | Overlaps | Ships inside.
# CATALOG_COLUMNS is the FALLBACK width, used only for text whose table declares no
# header — the real width comes from each table's own header row (see below), which is
# how validate_comparison_rows has always worked and why COMPARISON could gain a column
# without a constant to bump. The ~520 embedded `## Catalog entry` mirrors declare the
# 5-column header and are validated against it; CATALOG.md declares 6 (#343).
CATALOG_COLUMNS = 5
SHIPS_INSIDE_COL = 5          # index of the Ships inside cell when a table carries one
SHIPS_INSIDE_HEADER = "Ships inside"


def catalog_body_rows(text):
    """(line_no, line, cells, table_width) for every CATALOG body row — a pipe-line that
    is neither a separator nor the header above one. `table_width` is the enclosing
    table's own header width, or None outside any table (#343).

    The population detector O walks, shared by its validator and its coverage line so
    the two cannot disagree about what was examined (#481)."""
    lines = text.splitlines()
    width = None
    for i, line in enumerate(lines):
        if not line.lstrip().startswith("|"):
            width = None  # table ended (blank line, heading, prose)
            continue
        if _SEPARATOR_ROW.match(line):
            continue
        cells = _row_cells(line)
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        if _SEPARATOR_ROW.match(nxt):
            width = len(cells)  # header row (structural: the row above a |---| separator)
            continue
        yield i + 1, line, cells, width


def comparison_body_rows(text):
    """(line_no, cells, hdr_cols, vcol) for every COMPARISON row inside a table the
    verdict parser consumes — one carrying an `Evaluated` column, outside `## Summary`.

    Narrower than `catalog_body_rows` on purpose: a row in a foreign table is out of
    scope rather than unchecked, so counting every body row here would overstate what
    detector O examined — which is the direction that makes a coverage number worse
    than none (#481)."""
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
        yield i + 1, cells, hdr_cols, vcol


def validate_catalog_rows(text):
    """(line_no, problem) findings for CATALOG table lines that would otherwise
    be silently skipped or mis-parsed (#198): a pipe-line that isn't a header,
    separator, or recognized entry row; entry rows whose cell count doesn't match
    their own table's header (a missing cell silently shifts every field after
    it); an indented row (markdown renders it, the ^|-anchored parsers and
    counters skip it); and an empty Name cell (counted, but nameless). A clean
    tree returns [].

    Width comes from the ENCLOSING TABLE'S HEADER, not from a constant (#343).
    Adding the Ships inside column could otherwise only be done two ways, and
    both are worse: bump the constant and every 5-column eval mirror becomes a
    finding, or accept 5-or-6 and a row that LOST a middle cell parses as a valid
    short row — silently shifting Overlaps into Problem, which is the exact
    corruption #198 built this check to catch."""
    # The row-walking loop lives in `catalog_body_rows` so detector O's coverage line
    # counts the population this validator actually walks rather than re-deriving it
    # (#481). Two extractors for one fact is #443, and a coverage number that overstates
    # what a gate examined is the defect the number exists to remove.
    problems = []
    for i, line, cells, width in catalog_body_rows(text):
        expected = width or CATALOG_COLUMNS
        if line != line.lstrip():
            problems.append((i, "indented table row (markdown renders it, but the parsers and counters skip it)"))
        elif not _BODY_ROW.match(line):
            got = repr(cells[1]) if len(cells) > 1 else "missing"
            problems.append((i, f"not a recognized entry row (Type cell {got} not in the Type vocabulary)"))
        elif len(cells) != expected:
            problems.append((i, f"expected {expected} cells, found {len(cells)} cells"))
        elif not cells[0]:
            problems.append((i, "empty Name cell (row is counted, but nameless)"))
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
    # Row-walking lives in `comparison_body_rows` — see the note on the catalog half.
    problems = []
    for i, cells, hdr_cols, vcol in comparison_body_rows(text):
        if len(cells) != hdr_cols:
            problems.append((i, f"expected {hdr_cols} cells, found {len(cells)} cells"))
        elif cells[vcol] not in _VERDICT_SET:
            problems.append((i, f"Evaluated cell {cells[vcol]!r} is not a verdict token"))
        elif not cells[0]:
            problems.append((i, "empty Tool cell (row carries a verdict, but no name)"))
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


# --- resolving a link to the catalog row it names (#463, #465) -----------------
#
# A catalog row is identified by its LINK, and several rows can sit behind one
# `owner/repo`: 30 rows share 7 slugs today, because a pack's members each get a row
# (`mattpocock/skills` holds 6, `anthropics/claude-plugins-official` 8). Every consumer
# that starts from a link — detector J's STACK picks, detector V's metadata records,
# detector Z's license records, detector AE's WORKFLOW lines — has to answer the same
# question, and each of them used to answer it by taking whichever row `parse_catalog_rows`
# yielded first.
#
# That is a coin flip, and #463 showed it is not a theoretical one: reordering CATALOG.md
# turned a green `make check` into 5 gating failures naming KEEP tools for a SKIP. The
# rule is the one #401/#374/#457 keep arriving at — **an ambiguous lookup resolves to
# NOTHING, never to a candidate** — so this returns `(row, None)` when it is sure and
# `(None, candidates)` when it is not, and the caller decides whether ambiguity is a
# finding (J gates it) or a silence (AE skips it, since flagging a healthy row costs
# more than missing a sick one).
CatalogLinks = collections.namedtuple("CatalogLinks", "by_link by_slug")


def norm_link(url):
    """A github URL flattened for comparison: no trailing slash, case-folded. GitHub
    itself redirects on case, which is why detector U holds CASE out of LINK."""
    return (url or "").strip().rstrip("/").lower()


def link_index(catalog_text):
    """CatalogLinks over every github-linked CATALOG.md row: exact URL → row, and
    `owner/repo` → every row behind it (in catalog order, deduped by name)."""
    by_link, by_slug = {}, collections.defaultdict(list)
    for r in parse_catalog_rows(catalog_text):
        url = (r.url or "").strip()
        if not url.lower().startswith("https://github.com/"):
            continue
        by_link.setdefault(norm_link(url), r)
        for s in github_repos(url):
            if not any(x.name == r.name for x in by_slug[s.lower()]):
                by_slug[s.lower()].append(r)
    return CatalogLinks(by_link, dict(by_slug))


def rows_for_slug(index, slug):
    """Every catalog row behind `owner/repo`. A metadata record or an archival flag is
    a fact about the REPO, so it is about all of them — asking one row on their behalf
    is how detector V reported one row's disclosure as nine rows' (#465)."""
    return index.by_slug.get((slug or "").lower(), [])


def _links_repo_root(url):
    """True when the URL is `github.com/owner/repo` with no subpath."""
    if not url or "github.com/" not in url.lower():
        return False
    return len(norm_link(url).split("github.com/")[-1].split("/")) == 2


def container_row(index, slug):
    """The row that links the repo ROOT, or None. Among rows sharing a slug this is the
    one naming the whole artifact — detector X's `Ships inside` container test — so it
    is the honest subject of a repo-level fact. Never "the first row"."""
    return next((r for r in rows_for_slug(index, slug) if _links_repo_root(r.url)), None)


def resolve_link(index, text, url, slug=None):
    """(row, None) when one catalog row is identifiable, else (None, candidates).

    Precedence — narrowest evidence first:
      1. a unique row behind the slug (the 99% case: nothing to disambiguate);
      2. the link TEXT matching exactly one candidate's Name — a WORKFLOW line or a
         STACK pick links a pack member at the pack root and names it in the text,
         which is the only thing that tells `code-review` from `feature-dev`;
      3. the exact URL, when it names a candidate — a row linking its own subpath.
    Anything else is ambiguous and resolves to nothing.

    Name-before-link is deliberate and was wrong in the first draft: link-first sent
    `code-review`, `feature-dev`, `pr-review-toolkit` and `resolving-merge-conflicts`
    to the CONTAINER row, whose verdict is a different tool's."""
    if slug is None:
        slug = next(iter(github_repos(url or "")), "")
    candidates = rows_for_slug(index, slug)
    if len(candidates) <= 1:
        return (candidates[0] if candidates else None), None
    exact = [c for c in candidates if c.name.lower() == (text or "").strip().lower()]
    if len(exact) == 1:
        return exact[0], None
    row = index.by_link.get(norm_link(url))
    return (row, None) if row in candidates else (None, candidates)


# --- which tools does STACK.md recommend (#469) --------------------------------
#
# One fact with five implementations, three of them the literal regex below written out
# again: detector J's ledger check and its gating SKIP check (byte-identical copies, one
# file apart), `tier-stack.py`'s `_LINK`, detector P's own `|`-line rule, and detector
# AG's first-cell rule. #443 states the rule this broke — *"Two extractors for one fact,
# in two languages, coupled by nothing"* — and here the consumers are load-bearing:
# `triage.py`'s P2 band, which is a band an unattended pass may SKIP from.
#
# A pick is a markdown link to a github repo at the START of a table cell. That anchor is
# what distinguishes a recommendation from a mention: STACK.md:117 reads
# `… [GSD](…) planning + [graphify](…) knowledge-graph views | … graphify is not in STACK`,
# and only the cell-initial link is the row's subject. Detector P's looser rule counted
# `graphify` and would have demanded WORKFLOW.md document a tool STACK disclaims.
StackPick = collections.namedtuple("StackPick", "text url slug")

_STACK_PICK = re.compile(r"\|\s*\[([^\]]+)\]\((https://github\.com/[^)]+)\)")


def stack_picks(stack_text):
    """Every StackPick in STACK.md, in appearance order, duplicates included.

    One link can yield several picks only if `github_repos` reads several slugs from one
    URL; callers that want tools rather than slugs dedupe by `text` (tier-stack) or by
    `slug` (detectors J and P). Order is preserved because `tier-stack.py` renders the
    Evidence tiers in STACK appearance order."""
    return [StackPick(text, url, slug.lower())
            for text, url in _STACK_PICK.findall(stack_text)
            for slug in github_repos(url)]


def distinct_stack_picks(stack_text):
    """The picks STACK.md recommends — first occurrence per display text, in order.

    The ONE definition of *how many tools the page recommends* (#502), shared by
    `tier-stack.py`'s Evidence tiers block and `reconcile-counts.py`'s prose count so
    the sentence at the top of the page and the generated block twelve lines below it
    are the same population by construction and cannot drift (#443/#469).

    The key is the **display text**, not the slug, because the question is how many
    things a reader installs: `anthropics/claude-plugins-official` ships five separately
    installed picks, so the 35 rows here are 30 tools and only 24 slugs. Deduping by slug
    answers a different question — the one detectors J and P ask, where a verdict is a
    fact about a repo — and answering it here is what let `~25` stand for two months
    (#502). Two genuinely distinct tools sharing a display name would collapse into one;
    none do today, and a test pins it.
    """
    seen, out = set(), []
    for pick in stack_picks(stack_text):
        if pick.text not in seen:
            seen.add(pick.text)
            out.append(pick)
    return out
