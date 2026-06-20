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
and COMPARISON.md (header + summary rows + Total). Does NOT touch eval-file counts
or plugin/docs/ (run ./sync-plugin-docs.sh for the latter).
"""
import os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
ROW_TYPE = r"(?:MCP server|tool|skill|plugin|framework|harness|platform|reference)"

def read(p):  return open(os.path.join(ROOT, p), encoding="utf-8").read()
def write(p, s): open(os.path.join(ROOT, p), "w", encoding="utf-8").write(s)

def catalog_count():
    return sum(1 for l in read("CATALOG.md").splitlines()
               if l.startswith("| ") and not l.startswith("| Name") and not l.startswith("|---"))

def comparison_body_counts(text):
    """body rows per '## Section' (parenthetical-stripped), like detector G."""
    body, sec, in_summary = {}, None, False
    for l in text.splitlines():
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
        if sec and re.match(rf"^\|\s*[^|]+\|\s*{ROW_TYPE}\s*\|", l):
            body[sec] += 1
    return body

# count strings that quote the catalog total, by file
TOTAL_PATTERNS = [
    (r"(inventory of )\d+( tools)", r"\g<1>{C}\g<2>"),
    (r"\b\d+( catalog entries)", r"{C}\g<1>"),
    (r"\b\d+( tools are cataloged)", r"{C}\g<1>"),
    (r"(distilled from )\d+( catalog entries)", r"\g<1>{C}\g<2>"),
]

def fix_total_strings(text, C):
    for pat, repl in TOTAL_PATTERNS:
        text = re.sub(pat, repl.replace("{C}", str(C)), text)
    return text

def fix_comparison(text, C):
    body = comparison_body_counts(text)
    # header "All N tools from CATALOG.md"
    text = re.sub(r"(All )\d+( tools from CATALOG\.md)", rf"\g<1>{C}\g<2>", text)
    # per-stage summary rows "| Section | n | n | ... |" (bare ints; name has no | or *)
    def fix_sec(m):
        name = m.group(1).strip()
        if name in body:
            b = body[name]
            return f"| {m.group(1)} | {b} | {b} |{m.group(2)}"
        return m.group(0)
    text = re.sub(r"^\|\s*([A-Za-z][^|*]+?)\s*\|\s*\d+\s*\|\s*\d+\s*\|(.*)$", fix_sec, text, flags=re.M)
    # Total row "| **Total** | **n** | **n** | ... |" (bolded numbers)
    text = re.sub(r"(\|\s*\*\*Total\*\*\s*\|\s*\*\*)\d+(\*\*\s*\|\s*\*\*)\d+(\*\*\s*\|)",
                  rf"\g<1>{C}\g<2>{C}\g<3>", text)
    return text

FILES_TOTAL = ["README.md", "CLAUDE.md", "STACK.md", "plugin/CLAUDE.md"]

def main():
    check = "--check" in sys.argv[1:]
    C = catalog_count()
    changed = []
    for f in FILES_TOTAL:
        if not os.path.exists(os.path.join(ROOT, f)):
            continue
        s = read(f); s2 = fix_total_strings(s, C)
        if s2 != s:
            changed.append(f)
            if not check: write(f, s2)
    s = read("COMPARISON.md"); s2 = fix_comparison(fix_total_strings(s, C), C)
    if s2 != s:
        changed.append("COMPARISON.md")
        if not check: write("COMPARISON.md", s2)
    if changed:
        verb = "would update" if check else "updated"
        print(f"reconcile: catalog count = {C}; {verb} {len(changed)} file(s): {', '.join(changed)}")
        sys.exit(1 if check else 0)
    print(f"reconcile: OK — catalog count = {C}, all count strings already consistent")
    sys.exit(0)

if __name__ == "__main__":
    main()
