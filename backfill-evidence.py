#!/usr/bin/env python3
"""
backfill-evidence.py — populate the Evidence-strength field (#62/#67) across every
evaluation and mirror it as a column in COMPARISON.md, kept in sync with the evals.

The value is DERIVED from each eval's own honesty / measurement signals — the same
ones audit-evals.py detector B trusts (see Evidence.level there) — so the backfill is
reproducible and grounded in the eval's text, not hand-guessed:

  MEASURED    — a measured marker is present (ran it AND captured metrics)
  RUN         — claims/shows a hands-on run, no metrics, no not-run disclaimer
  REVIEW      — discloses it was NOT run (source-grounded review)
  SOURCE-ONLY — no 'How we tested' section, or (in COMPARISON) a catalog row with no
                eval file at all — i.e. we have no evaluation evidence, only metadata

An author who has done better than the derived value should edit the eval's
**Evidence:** line by hand; this script never downgrades a line that already exists.
The COMPARISON column is fully regenerated from the evals each run, so it cannot drift.

  ./backfill-evidence.py          # apply: insert missing fields + rebuild the column
  ./backfill-evidence.py --check  # verify only: exit 1 if anything would change; mutate nothing
"""
import os, re, sys, glob, importlib.util
import catalog_lib

ROOT = os.path.dirname(os.path.abspath(__file__))

# Import the derivation + eval model from audit-evals.py (single source of truth).
_spec = importlib.util.spec_from_file_location("audit_evals", os.path.join(ROOT, "audit-evals.py"))
ae = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(ae)

EVAL_GLOB = os.path.join(ROOT, "evaluations", "*.md")
COMPARISON = os.path.join(ROOT, "COMPARISON.md")
HOW_HEADING = re.compile(r"^##\s+How we tested it[ \t]*$", re.M)
H1 = re.compile(r"^#\s+.+$", re.M)


# ---------------------------------------------------------------- eval field backfill
def backfill_eval_text(text):
    """Return eval text with an Evidence field inserted, or unchanged if it already
    declares one. Idempotent."""
    if ae.EVIDENCE_FIELD.search(text):
        return text  # already declared (by hand or a prior run) — never overwrite
    level = ae.Evidence(ae.how_section(text)).level
    field = f"**Evidence:** {level}"
    anchor = HOW_HEADING.search(text) or H1.search(text)  # under How section, else under the title
    if anchor:
        end = anchor.end()
        rest = text[end:].lstrip("\n")  # Evidence becomes its own paragraph regardless of prior spacing
        return text[:end] + "\n\n" + field + "\n\n" + rest
    return field + "\n\n" + text


# ---------------------------------------------------------------- COMPARISON column
_SEP = re.compile(r"^\|[\s\-|]+\|\s*$")
_HEADER = re.compile(r"^\|\s*Tool\s*\|.*\|\s*Evaluated\s*(\|\s*Evidence\s*)?\|\s*$")


def rebuild_comparison(text, amap):
    """Regenerate the Evidence column in every per-stage table, idempotently. The
    Summary table is left untouched (its rows are per-stage aggregates, not tool rows).
    A header sets the expected column count; the separator immediately after it is
    regenerated to match."""
    out, in_summary, sep_cols = [], False, None
    for line in text.splitlines():
        hm = re.match(r"^##\s+(.*)", line)
        if hm:
            in_summary = hm.group(1).strip().lower() == "summary"
            sep_cols = None
            out.append(line); continue
        if in_summary:
            out.append(line); continue
        if _HEADER.match(line):
            base = re.sub(r"\s*\|\s*Evidence\s*\|\s*$", " |", line)  # normalize: drop existing col
            newh = re.sub(r"\s*\|\s*$", " | Evidence |", base)
            out.append(newh)
            sep_cols = newh.count("|") - 1
            continue
        if sep_cols is not None and _SEP.match(line):
            out.append("|" + "------|" * sep_cols)
            sep_cols = None
            continue
        row = next(iter(catalog_lib.parse_catalog_rows(line)), None)
        if row:
            tool = row.name
            # strip a trailing Evidence cell if present, then append the fresh value (idempotent)
            core = re.sub(r"\s*\|\s*(MEASURED|RUN|REVIEW|SOURCE-ONLY)\s*\|\s*$", " |", line)
            out.append(re.sub(r"\s*\|\s*$", f" | {catalog_lib.evidence_lookup(amap, tool)} |", core))
            continue
        out.append(line)
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


# ---------------------------------------------------------------- driver
def main():
    check = "--check" in sys.argv[1:]
    changed = []

    for path in sorted(glob.glob(EVAL_GLOB)):
        if os.path.basename(path) == "TEMPLATE.md":
            continue
        text = open(path, encoding="utf-8").read()
        new = backfill_eval_text(text)
        if new != text:
            changed.append(os.path.relpath(path, ROOT))
            if not check:
                open(path, "w", encoding="utf-8").write(new)

    # Built from a fresh DetectorContext AFTER the eval rewrites above, so the
    # map reflects any Evidence fields this run just inserted (#199/#201).
    amap = ae.DetectorContext(ROOT).evidence_alias_map
    ctext = open(COMPARISON, encoding="utf-8").read()
    cnew = rebuild_comparison(ctext, amap)
    if cnew != ctext:
        changed.append("COMPARISON.md")
        if not check:
            open(COMPARISON, "w", encoding="utf-8").write(cnew)

    if check:
        if changed:
            print(f"backfill check: DRIFT — {len(changed)} file(s) would change; run ./backfill-evidence.py")
            for c in changed[:20]:
                print(f"  {c}")
            if len(changed) > 20:
                print(f"  ... and {len(changed) - 20} more")
            sys.exit(1)
        print("backfill check: OK — every eval declares Evidence and the COMPARISON column is in sync")
        sys.exit(0)
    print(f"backfilled {len(changed)} file(s): "
          f"{len([c for c in changed if c != 'COMPARISON.md'])} evals + "
          f"{'COMPARISON.md' if 'COMPARISON.md' in changed else 'no COMPARISON change'}")


if __name__ == "__main__":
    main()
