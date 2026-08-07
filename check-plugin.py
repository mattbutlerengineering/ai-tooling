#!/usr/bin/env python3
"""The published plugin package must be structurally valid and internally consistent.

    python3 check-plugin.py            # report-only
    python3 check-plugin.py --check    # gate: exit 1 on any finding

Detector A gates every install command in `STACK.md`, `CATALOG.md` and `evaluations/`
because "a broken command means the tool was likely never run", and #416 sharpened that
to the page: STACK is the page whose whole purpose is to be executed. `README.md`'s
Install block is the only page here whose purpose is to be executed *by a stranger, on
this repo's own product*, and nothing checked it — neither of its two commands existed,
and `claude plugin validate ./plugin` failed outright on a missing manifest (#439).

`claude plugin validate` is the **upstream authority** and this is not equivalent to it.
It cannot be: CI has no `claude` binary, and the offline-gate invariant forbids depending
on one. This mirrors offline the parts that are checkable from the tree, and adds the
cross-file agreements upstream has no way to know about — the plugin name against the
marketplace entry, every declared version against every other, and the skills list in
`plugin/CLAUDE.md` against `plugin/skills/` on disk. That last one is a fact restated in
a hand-authored file with no generator, which is the shape that put its eval count 87
behind (#302); `plugin/CLAUDE.md`'s own rule is to gate the shared facts, not the file.

Run `claude plugin validate ./plugin` by hand before publishing. This gate is what keeps
the tree from drifting between those runs.
"""
import collections
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

Finding = collections.namedtuple("Finding", "kind detail")

_FRONTMATTER = re.compile(r"\A---\n(.*?)\n---", re.DOTALL)
# `plugin/CLAUDE.md` lists each skill as "- `/name` — description".
_LISTED_SKILL = re.compile(r"^-\s*`/([a-z0-9][a-z0-9-]*)`", re.MULTILINE)


def _load_json(path):
    """(data, error). A manifest that does not parse is a finding, never a traceback."""
    if not os.path.exists(path):
        return None, "missing"
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh), None
    except (OSError, json.JSONDecodeError) as e:
        return None, str(e)


def skill_dirs(root):
    d = os.path.join(root, "plugin", "skills")
    if not os.path.isdir(d):
        return []
    return sorted(n for n in os.listdir(d) if os.path.isdir(os.path.join(d, n)))


def frontmatter_field(text, field):
    m = _FRONTMATTER.search(text)
    if not m:
        return None
    hit = re.search(rf"^{field}:\s*(.+)$", m.group(1), re.MULTILINE)
    return hit.group(1).strip() if hit else None


def audit_plugin(root=None):
    """Findings for the published plugin package. Offline; reads only the tree."""
    root = root or ROOT
    findings = []

    market, err = _load_json(os.path.join(root, ".claude-plugin", "marketplace.json"))
    if err:
        findings.append(Finding("MANIFEST", f".claude-plugin/marketplace.json: {err}"))
    manifest, err = _load_json(os.path.join(root, "plugin", ".claude-plugin", "plugin.json"))
    if err:
        # The exact failure `claude plugin validate ./plugin` reported in #439.
        findings.append(Finding("MANIFEST", f"plugin/.claude-plugin/plugin.json: {err}"))

    entry = None
    if market:
        entries = market.get("plugins") or []
        entry = entries[0] if entries else None
        if entry is None:
            findings.append(Finding("MANIFEST", "marketplace.json declares no plugins"))
        else:
            # `source` is resolved from the REPO ROOT, not from `.claude-plugin/` —
            # `./plugin` means `<repo>/plugin`, which is how the upstream validator reads it.
            src = os.path.normpath(os.path.join(root, entry.get("source", "")))
            if not os.path.isdir(src):
                findings.append(Finding("SOURCE", f"marketplace source {entry.get('source')!r} is not a directory"))

    if manifest and entry and manifest.get("name") != entry.get("name"):
        findings.append(Finding(
            "NAME", f"plugin.json name {manifest.get('name')!r} != marketplace entry {entry.get('name')!r}"))

    # Every declared version must agree. `plugin/package.json` used to hold a second copy
    # for an npm registry this package is not published to; if one comes back, it is a
    # third place for the number to drift, so it is checked rather than assumed absent.
    versions = {}
    if manifest and "version" in manifest:
        versions["plugin/.claude-plugin/plugin.json"] = manifest["version"]
    if entry and "version" in entry:
        versions[".claude-plugin/marketplace.json"] = entry["version"]
    pkg, err = _load_json(os.path.join(root, "plugin", "package.json"))
    if pkg and "version" in pkg:
        versions["plugin/package.json"] = pkg["version"]
    if len(set(versions.values())) > 1:
        findings.append(Finding("VERSION", "declared versions disagree: "
                                + ", ".join(f"{k}={v}" for k, v in sorted(versions.items()))))

    on_disk = skill_dirs(root)
    for name in on_disk:
        path = os.path.join(root, "plugin", "skills", name, "SKILL.md")
        if not os.path.exists(path):
            findings.append(Finding("SKILL", f"{name}/ has no SKILL.md"))
            continue
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        declared = frontmatter_field(text, "name")
        if not declared:
            findings.append(Finding("SKILL", f"{name}/SKILL.md declares no `name:` frontmatter"))
        elif declared != name:
            findings.append(Finding("SKILL", f"{name}/SKILL.md declares name {declared!r}"))
        if not frontmatter_field(text, "description"):
            findings.append(Finding("SKILL", f"{name}/SKILL.md declares no `description:` frontmatter"))

    front = os.path.join(root, "plugin", "CLAUDE.md")
    if os.path.exists(front):
        with open(front, encoding="utf-8") as fh:
            listed = sorted(set(_LISTED_SKILL.findall(fh.read())))
        for name in sorted(set(listed) - set(on_disk)):
            findings.append(Finding("FRONT-DOOR", f"plugin/CLAUDE.md lists /{name}, which is not in plugin/skills/"))
        for name in sorted(set(on_disk) - set(listed)):
            findings.append(Finding("FRONT-DOOR", f"plugin/skills/{name}/ is not listed in plugin/CLAUDE.md"))

    return findings


def main():
    check = "--check" in sys.argv
    findings = audit_plugin()
    label = "gate" if check else "report-only"
    print(f"== plugin package ({label}) — {len(findings)} finding(s) ==")
    for f in findings:
        print(f"  {f.kind} {f.detail}")
    if not findings:
        print("  OK — manifests parse and agree; skills and the front door match the tree")
        return 0
    print("  run `claude plugin validate ./plugin` for the upstream check too")
    return 1 if check else 0


if __name__ == "__main__":
    sys.exit(main())
