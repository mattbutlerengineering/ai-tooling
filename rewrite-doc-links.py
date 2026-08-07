#!/usr/bin/env python3
"""Repoint a synced doc's outside-the-bundle links at the canonical repo.

    python3 rewrite-doc-links.py <dest-docs-dir>

`sync-plugin-docs.sh` copies seven root files and three directories into `plugin/docs/`
**verbatim**, so every relative link in a synced file whose target lives outside that
set lands in a tree the target is not in. Sixteen were dead that way (#437), three of
them on `plugin/docs/PLAYBOOK.md` — the front door of the bundle a user actually
installs — including `[CLAUDE.md](CLAUDE.md)` under a heading promising that CI
enforces all of it. None is fixable at the source: the root link is correct *at root*.
It is the copy that is wrong, which makes this the sync's job, and the skills half of
the same script already does the analogous transform (it strips `${CLAUDE_PLUGIN_ROOT}/docs/`
out of every SKILL.md on the way through).

One rule carries the whole design: **the sync fixes depth, not rot.**

  target resolves inside the bundle   → leave it; the relative link still works
  target exists at repo root          → rewrite to the canonical blob URL
  target exists nowhere               → LEAVE IT ALONE

That third branch is the load-bearing one. Minting a URL for a file nobody has would
let the sync quietly launder a *dead* link into a plausible-looking one — the exact
defect class #437 opened with, where a dedupe deleted an eval and left five citations
pointing at it. A link broken at root must stay broken in the copy so `check-links.py`
keeps reporting it at the source, where the fix belongs.

Idempotent: a rewritten link is absolute, and absolute links are skipped.
"""
import os
import re
import sys

BLOB = "https://github.com/mattbutlerengineering/ai-tooling/blob/main/"
_FENCE = re.compile(r"^\s*(?:```|~~~)")
_LINK = re.compile(r"(\[[^\]]*\]\()([^)\s]+)(\))")
_SKIP_SCHEME = ("http://", "https://", "mailto:", "#", "//")


def rewrite_text(text, root_rel, dest_dir, repo_root):
    """`text` of a synced file whose root-relative source path is `root_rel`."""
    src_dir = os.path.dirname(root_rel)
    dest_path_dir = os.path.dirname(os.path.join(dest_dir, root_rel))
    out, in_fence = [], False

    def one(m):
        target = m.group(2)
        if target.startswith(_SKIP_SCHEME) or "{" in target or "}" in target:
            return m.group(0)
        bare, frag = (*target.split("#", 1), "")[:2]
        if not bare:
            return m.group(0)
        if os.path.exists(os.path.normpath(os.path.join(dest_path_dir, bare))):
            return m.group(0)                       # still inside the bundle
        at_root = os.path.normpath(os.path.join(repo_root, src_dir, bare))
        if not os.path.exists(at_root):
            return m.group(0)                       # rot, not depth — leave it for the gate
        rel = os.path.relpath(at_root, repo_root).replace(os.sep, "/")
        return f"{m.group(1)}{BLOB}{rel}{'#' + frag if frag else ''}{m.group(3)}"

    for line in text.split("\n"):
        if _FENCE.match(line):
            in_fence = not in_fence
            out.append(line)
            continue
        out.append(line if in_fence else _LINK.sub(one, line))
    return "\n".join(out)


def rewrite_tree(dest_dir, repo_root):
    """Rewrite every `.md` under `dest_dir`; returns the number of files changed."""
    changed = 0
    for dirpath, _dirnames, filenames in os.walk(dest_dir):
        for fn in sorted(filenames):
            if not fn.endswith(".md"):
                continue
            path = os.path.join(dirpath, fn)
            root_rel = os.path.relpath(path, dest_dir)
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
            fixed = rewrite_text(text, root_rel, dest_dir, repo_root)
            if fixed != text:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(fixed)
                changed += 1
    return changed


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__.strip().split("\n\n")[1].strip(), file=sys.stderr)
        sys.exit(2)
    dest = sys.argv[1]
    print(f"link rewrite: {rewrite_tree(dest, os.path.dirname(os.path.abspath(__file__)))} file(s) repointed")
