#!/usr/bin/env python3
"""
check-stars.py — the presence gate for the **Stars:** header field (#377).

#256 fixed the data twice and the field kept going missing, because nothing stopped a
new eval from omitting it: 10 evals lacked it when #256 was filed and 20 lacked it when
#256 closed, every one of the new ones written while the issue was open. That is the
failure root `CLAUDE.md` names for `plugin/CLAUDE.md` — **gate the shared facts, not the
file**. A convention with no generator and no test drifts back.

WHAT IT CHECKS — presence, and only presence. The star convention (#256/#261, recorded in
TEMPLATE.md) says every eval *declares* a value, and what it declares depends on what the
file is about:

    one tool          -> its star count
    named contenders  -> one figure per contender, so a head-to-head doesn't pick a
                         winner in its header
    no single subject -> `n/a` WITH THE REASON

That third bucket is what makes a gate possible at all. Before the convention, a protocol
doc with no repo and a forgotten eval both presented as *no line*; a declared `n/a`
distinguishes them. So this keys on the line existing, **never on it being a number** — a
check that demanded a numeric count would fail every legitimately-`n/a` file and pressure
authors into inventing a figure, which is the exact failure the convention exists to
prevent. Staleness of a figure is not a build breaker either; only absence is.

BARE `n/a` IS PRINTED, NEVER FAILED. `n/a` with no reason is half a declaration — it says
the field is inapplicable without saying why, which is what the convention's "WITH THE
REASON" clause is about. But the reason is prose, and a check that guessed at prose would
flag healthy files; a detector that flags a healthy file is worse than one that misses a
sick one (detector V's rule). So it lands in a printed-not-counted bucket, the same shape
as V's `acked`, W's `cleared` and X's `FACETED`.

GATE OR REPORT-ONLY — the Makefile decides, not this file. #377 left that open as a
#71-style call. Both modes are built, so the choice is one word in one place:

  ./check-stars.py            # report: print coverage, always exit 0
  ./check-stars.py --check    # gate: exit 1 listing every eval missing the field

`make check` runs it with `--check`, taking #377's own recommendation — the field is at
677/677, so the gate starts green and a report-only pass would have had nothing to
observe. Reverting to report-only is dropping `--check` from the Makefile; nothing else
changes, and `TestStarConvention` pins both directions either way.
"""
import os
import re
import sys
import glob

ROOT = os.path.dirname(os.path.abspath(__file__))
EVAL_GLOB = os.path.join(ROOT, "evaluations", "*.md")

STARS_LINE = re.compile(r"^\*\*Stars:\*\*(.*)$", re.M)
HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)
# A declaration that says "inapplicable" and stops there. Trailing dashes/colons are
# stripped so `n/a —` (a reason the author meant to write and didn't) still reads as bare.
BARE_NA = re.compile(r"^n/?a[\s\-—:.]*$", re.I)


def star_value(text):
    """The declared value, or None if the eval declares no **Stars:** line at all.

    Takes the first segment before the `|` that separates Stars from Last-updated/License
    in TEMPLATE's header line, with any HTML comment (the repo-metadata.json provenance
    stamp) removed first so the stamp is never mistaken for the value."""
    m = STARS_LINE.search(text)
    if m is None:
        return None
    return HTML_COMMENT.sub("", m.group(1)).split("|")[0].strip()


def audit(paths):
    """(missing, bare) — evals with no **Stars:** line, and evals declaring a reasonless
    `n/a`. Two lists because they are not the same problem: the first is an undeclared
    fact, the second is a declared one missing its justification."""
    missing, bare = [], []
    for path in sorted(paths):
        name = os.path.basename(path)
        with open(path, encoding="utf-8") as f:
            value = star_value(f.read())
        if value is None:
            missing.append(name)
        elif BARE_NA.match(value):
            bare.append(name)
    return missing, bare


def main(argv):
    gating = "--check" in argv
    paths = glob.glob(EVAL_GLOB)
    missing, bare = audit(paths)
    total = len(paths)
    declared = total - len(missing)

    mode = "gate" if gating else "report-only"
    print(f"== star convention ({mode}) — {declared}/{total} eval(s) declare **Stars:** ==")

    for name in bare:
        # Printed, never counted: a reasonless n/a is worth seeing and is not a build
        # breaker, and the reason is prose no check should try to grade.
        print(f"  note   {name}: declares a bare `n/a` with no reason")

    if not missing:
        print("  OK — every eval declares a **Stars:** value")
        return 0

    for name in missing:
        print(f"  MISSING {name}: no **Stars:** line "
              f"(declare a count, a per-contender list, or `n/a — <reason>`)")
    print(f"  {len(missing)} eval(s) missing the field — see the star convention in "
          f"evaluations/TEMPLATE.md")
    return 1 if gating else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
