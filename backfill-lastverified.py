#!/usr/bin/env python3
"""
backfill-lastverified.py — populate the **Last verified:** header field (#65) across
every evaluation so the staleness sweep (audit-evals.py --staleness) can see them.

The staleness sweep keys on **Last verified:**, but 455 of 487 evals never had one, so
it was structurally inert. This backfills a DATED FLOOR from each eval's git history —
the last substantive edit — which is an honest lower bound: the eval was last *true* no
later than when it was last touched. The inserted line carries an explicit comment
saying so, distinguishing a backfilled floor from a real hands-on re-check:

  **Last verified:** <git-date>  <!-- backfilled from last git edit; not a hands-on re-check -->

The floor date is DERIVED from `git log -1 --format=%as -- evaluations/<file>.md`, so the
backfill is reproducible, not hand-guessed. An author who has genuinely re-verified an
eval should replace the whole line by hand (date + drop the comment); this script never
overwrites a line that already exists — the same never-downgrade rule backfill-evidence.py
follows. The insert lands in the header metadata block, matching TEMPLATE.md's placement
(after the Repo/Stars lines, before **Dev loop stage:**).

  ./backfill-lastverified.py          # apply: insert the field into every eval missing it
  ./backfill-lastverified.py --check  # verify only: exit 1 listing evals missing the field
"""
import os, re, sys, glob, datetime, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
EVAL_GLOB = os.path.join(ROOT, "evaluations", "*.md")

LAST_VERIFIED = re.compile(r"^\*\*Last verified:\*\*", re.M)
DEV_STAGE = re.compile(r"^\*\*Dev loop stage:\*\*.*$", re.M)  # primary anchor (TEMPLATE order)
EVIDENCE_LINE = re.compile(r"^\*\*Evidence:\*\*.*$", re.M)    # fallback: cluster/landscape evals
H1 = re.compile(r"^#\s+.+$", re.M)                            # last resort
COMMENT = "<!-- backfilled from last git edit; not a hands-on re-check -->"


def git_floor_date(rel_path):
    """Last-commit date (YYYY-MM-DD) for an eval, the honest floor for **Last verified:**.
    Falls back to today for an untracked/new file (git returns nothing)."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%as", "--", rel_path],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        out = ""
    return out or datetime.date.today().isoformat()


def backfill_text(text, date):
    """Return eval text with a **Last verified:** line inserted, or unchanged if it already
    declares one (never overwrites a hand-set value). Idempotent. `date` is the floor to use.

    The line lands in the header block: immediately before **Dev loop stage:** to mirror
    TEMPLATE.md; for cluster/landscape evals that lack that line, right after **Evidence:**;
    else right after the H1 title."""
    if LAST_VERIFIED.search(text):
        return text  # already declared (by hand or a prior run) — never overwrite
    line = f"**Last verified:** {date}  {COMMENT}"
    m = DEV_STAGE.search(text)
    if m:  # insert as its own line just above Dev loop stage (consecutive, like TEMPLATE)
        return text[:m.start()] + line + "\n" + text[m.start():]
    m = EVIDENCE_LINE.search(text) or H1.search(text)
    if m:  # append directly after the anchor line, staying in the metadata block
        return text[:m.end()] + "\n" + line + text[m.end():]
    return line + "\n\n" + text  # no anchor at all — prepend


def main():
    check = "--check" in sys.argv[1:]
    changed = []

    for path in sorted(glob.glob(EVAL_GLOB)):
        if os.path.basename(path) == "TEMPLATE.md":
            continue
        text = open(path, encoding="utf-8").read()
        if LAST_VERIFIED.search(text):
            continue  # already has the field — skip (and skip the git call)
        rel = os.path.relpath(path, ROOT)
        new = backfill_text(text, git_floor_date(rel))
        if new != text:
            changed.append(rel)
            if not check:
                open(path, "w", encoding="utf-8").write(new)

    if check:
        if changed:
            print(f"last-verified check: MISSING — {len(changed)} eval(s) lack a "
                  f"**Last verified:** field; run ./backfill-lastverified.py")
            for c in changed[:20]:
                print(f"  {c}")
            if len(changed) > 20:
                print(f"  ... and {len(changed) - 20} more")
            sys.exit(1)
        print("last-verified check: OK — every eval declares a **Last verified:** date")
        sys.exit(0)
    print(f"backfilled {len(changed)} file(s) with a **Last verified:** floor date")


if __name__ == "__main__":
    main()
