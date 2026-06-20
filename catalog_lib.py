"""
catalog_lib.py — the single source of truth for how CATALOG.md and COMPARISON.md
are parsed for counting.

`reconcile-counts.py` *writes* the counts that `audit-evals.py` detector G
*checks* — two halves of one contract. They used to re-implement this parsing
independently, so a change to one could silently diverge from the other. Both now
import from here, so they provably agree by construction.

All functions are pure (text in, value out) — callers read the files.
"""
import re

# What counts as a catalog/comparison entry row: the Type column vocabulary.
ROW_TYPE = r"(?:MCP server|tool|skill|plugin|framework|harness|platform|reference)"
_BODY_ROW = re.compile(rf"^\|\s*[^|]+\|\s*{ROW_TYPE}\s*\|")


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
