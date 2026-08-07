#!/usr/bin/env python3
"""Every relative markdown link in the tracked tree must resolve to a real file.

    python3 check-links.py            # report-only
    python3 check-links.py --check    # gate: exit 1 on any dead link

Detector C checks the links this repo does *not* control — ~450 unauthenticated
HEAD requests at `github.com/owner/repo`, most of which come back rate-limited, which
is why its own rule is that "absence of findings is only a pass when the checked count
equals the total". The links between two files already in this tree are the opposite
kind of question: free, offline, deterministic, and answerable on every run. Nothing
asked it until #437, and 26 were dead — five of them left behind by a dedupe that
deleted an eval and kept its citations (`19435b9`), sixteen shipped inside the
installable plugin by a sync that copies files verbatim into a tree their targets are
not in.

Gating from day one rather than after a report-only tenure, for the reason detector J
gave when it gained its reverse direction: a dead relative link is bookkeeping, not
judgement. There is nothing here for a human to weigh.

Deliberately **out of scope**: `#anchor` fragments. Whether a heading exists is a
fuzzier question with a different failure mode (slugification rules vary by renderer),
and mixing it in would put a judgement call inside a gate. This answers exactly one
question — does the file exist.
"""
import collections
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

LinkFinding = collections.namedtuple("LinkFinding", "path line text target")

_FENCE = re.compile(r"^\s*(?:```|~~~)")
_SPAN = re.compile(r"`[^`\n]*`")
_LINK = re.compile(r"\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
_SKIP_SCHEME = ("http://", "https://", "mailto:", "#", "//")


def strip_code(text):
    """`text` with fenced blocks blanked and inline spans blanked, line count preserved.

    A link inside code is **sample text, not a link**, and this is not a nicety: a naive
    scan flags `evaluations/server-github.md`, which shows illustrative shell output
    containing `[GitHub](.../servers-archived/...)`, and `evaluations/docmd.md`, which
    quotes llms.txt's own `- [title](url)` format. Both files are healthy. Flagging a
    healthy row costs more than missing a sick one (detector V's rule), so the stripping
    runs first and the line numbers survive it so a finding still points somewhere.
    """
    out, in_fence = [], False
    for line in text.split("\n"):
        if _FENCE.match(line):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else _SPAN.sub(lambda m: " " * len(m.group(0)), line))
    return "\n".join(out)


def markdown_files(root):
    """Every tracked `*.md` path, relative to `root`.

    Asked of git, because the **tracked tree is what ships**: an untracked scratch
    worktree under `.claude/` is not this repo's link surface, and hand-maintaining an
    exclusion list of such directories would drift the first time a new one appeared.
    The walk is a fallback for a non-git tree — which in practice means a test fixture.
    """
    r = subprocess.run(["git", "-C", root, "ls-files", "*.md"],
                       capture_output=True, text=True, check=False)
    if r.returncode == 0:
        return sorted(p for p in r.stdout.split("\n") if p)
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        found += [os.path.relpath(os.path.join(dirpath, f), root)
                  for f in filenames if f.endswith(".md")]
    return sorted(found)


def broken_links(root=None):
    """LinkFindings for every relative link in the tracked tree that resolves nowhere."""
    root = root or ROOT
    findings = []
    for rel in markdown_files(root):
        path = os.path.join(root, rel)
        if not os.path.isfile(path):
            continue  # tracked but deleted in the working tree — git status' problem, not ours
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        raw = text.split("\n")
        for lineno, line in enumerate(strip_code(text).split("\n"), 1):
            for m in _LINK.finditer(line):
                # The display text comes off the ORIGINAL line: stripping blanks out
                # inline spans, and a link whose label is code (`` [`ecc.md`](…) ``)
                # would otherwise be reported with an empty label.
                text_shown = raw[lineno - 1][m.start(1):m.end(1)]
                target = m.group(2)
                if target.startswith(_SKIP_SCHEME):
                    continue
                # `[{name}]({url})` in TEMPLATE.md is a placeholder for the author to
                # fill, not a link that ever pointed anywhere.
                if "{" in target or "}" in target:
                    continue
                bare = target.split("#")[0]
                if not bare:
                    continue  # a pure `#anchor` — out of scope, see the module docstring
                if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(path), bare))):
                    findings.append(LinkFinding(rel, lineno, text_shown, target))
    return findings


def main():
    check = "--check" in sys.argv
    findings = broken_links()
    total = len(findings)
    label = "gate" if check else "report-only"
    print(f"== internal links ({label}) — {total} dead ==")
    for f in findings:
        print(f"  DEAD {f.path}:{f.line}  [{f.text[:40]}]({f.target})")
    if not total:
        print("  OK — every relative markdown link resolves to a file in the tree")
        return 0
    print(f"  {total} dead relative link(s) — fix the link, or the file it should point at")
    return 1 if check else 0


if __name__ == "__main__":
    sys.exit(main())
