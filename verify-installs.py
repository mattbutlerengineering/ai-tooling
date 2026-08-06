#!/usr/bin/env python3
"""
verify-installs.py — write and check the `Install evidence` column in STACK-LEDGER.md
(ADR-0006, #382).

WHY THE COLUMN EXISTS. `KEEP` used to mean "also-ran **already installed**", so a verdict
carried an unchecked assertion about one laptop — and `STACK.md`, detector J and the ledger
all read verdict data as though it had been checked. Detector Y (#366) was the first thing
to look and found all four `plugin`-Type KEEPs unbacked. ADR-0006 splits the two apart:
verdicts answer *do we recommend it*, this column answers *is it here, how was that
checked, and when*.

THE VOCABULARY, and why `n/a` is the load-bearing value:

    lockfile <date>          the row's own slug is in ~/.agents/.skill-lock.json
    plugins-json <date>      recorded in ~/.claude/plugins/installed_plugins.json
    skills-dir <date>        a directory answering to it exists under ~/.claude/skills/
    cache <version> <date>   the plugin cache holds a FETCHED version — a fetch is not an
                             activation, and nothing on disk records which happened
    collision <date>         this row's slug is absent AND its name on this machine
                             resolves to a different repo
    none <date>              checked on that date; nothing answered to it
    n/a                      this Type leaves no install record at all

A bare installed yes/no column would have been worse than nothing. An `MCP server` row is
not *not installed* — it is **unobservable by these records**, and `n/a` says so instead of
implying a clean check. That is the same rule as the detectors' "0 records, never 0
findings".

JOINED ON SLUG, NEVER ON NAME. Name-matching is the bug this came from (#332, #343, #366):
`code-review` is `anthropics/claude-plugins-official` in the catalog while the `code-review`
on this machine is `mattpocock/skills`' own — a different tool with a different design. The
row's own slug is asked first (detector Y's ordering), and `collision` exists so that case
cannot flatten into `skills-dir` — recording a name-match as this row's install is the exact
error the column was built to end.

TWO MODES, and the split is the offline-gate invariant:

  ./verify-installs.py --record   rewrite the column from THIS machine's records. Local
                                  only, because that is what the records are.
  ./verify-installs.py --check    validate SHAPE only — every ADOPT/KEEP row carries a
                                  well-formed value. Offline, no machine access, in
                                  `make check`.

CI gates that the fact is *declared and well formed*, never that it is *true*. A build must
not fail because a laptop changed, and #366 said so before any of this existed.
"""
import collections
import datetime
import importlib.util
import json
import os
import re
import sys
from pathlib import Path

import catalog_lib

ROOT = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(ROOT, "STACK-LEDGER.md")

# The install-record reader and the Type/verdict scoping live with detector Y; reusing them
# is what keeps the column and the detector from disagreeing about what "installed" means.
_spec = importlib.util.spec_from_file_location("audit_evals", os.path.join(ROOT, "audit-evals.py"))
if _spec is None or _spec.loader is None:  # a sibling in this repo — absent means a broken checkout
    raise ImportError("cannot load audit-evals.py; is the checkout complete?")
ae = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(ae)

HEADER = "Install evidence"
# Shape only. `--check` must never assert a value is true, so this is the whole contract.
VALUE = re.compile(
    r"^(?:n/a"
    r"|(?:lockfile|plugins-json|skills-dir|collision|none) \d{4}-\d{2}-\d{2}"
    r"|cache \S+ \d{4}-\d{2}-\d{2})$")

# The ADOPT/KEEP table's rows. The batch-exclusion table below it has a different shape and
# is deliberately out of scope — it records group decisions, not per-tool install facts.
_ROW = re.compile(r"^\|\s*([^|]+?)\s*\|\s*(ADOPT|KEEP)\s*\|([^|]*)\|([^|]*)\|([^|]*)\|(.*)$")
_HEADER_ROW = re.compile(r"^\|\s*Tool\s*\|\s*Verdict\s*\|")
_SEPARATOR = re.compile(r"^\|[\s:-]+\|[\s:|-]*$")


Records = collections.namedtuple(
    "Records", "slugs lock_by_key plugin_names fetched_keys disk_keys")


def read_records(home=None):
    """This machine's install records, or None when it keeps none at all.

    None is the point: a machine we know nothing about must read as 'no data', never as
    'nothing is installed' — the detectors' "0 records, never 0 findings" rule."""
    by_name, slugs, on_disk, fetched = ae.read_install_records(home)
    if not (len(by_name) + len(on_disk) + len(fetched)):
        return None
    return Records(
        slugs=slugs,
        lock_by_key={catalog_lib.name_key(n): s for n, s in by_name.items()},
        plugin_names=_plugin_record_names(home),
        fetched_keys={catalog_lib.name_key(n): v for n, v in fetched.items()},
        disk_keys={catalog_lib.name_key(n) for n in on_disk})


def classify(slug, key, today, rec):
    """The one decision: which value a row's `slug` and name-`key` earn from `rec`.

    THE ORDER IS THE PRECISION STORY (detector Y, #366). The row's OWN slug is asked first
    and settles the row whatever else shares its name. Only when the slug is absent does
    the name get consulted — and then the first thing asked is whether another repo owns
    it, because if so every name-keyed record below belongs to that other tool. Dropping
    that one branch is what made the first draft record `code-review` and `skill-creator`
    as installed on the strength of a directory belonging to something else: the exact
    identity-by-name error this column exists to end, committed inside the fix for it."""
    installed_from = rec.lock_by_key.get(key)
    if slug in rec.slugs:
        return f"lockfile {today}"
    if installed_from and installed_from != slug:
        return f"collision {today}"
    if key in rec.plugin_names:
        return f"plugins-json {today}"
    if key in rec.fetched_keys:
        # Every fetched version, never a "latest" — these are opaque strings (semver AND
        # commit shas) and a lexicographic max reads 13.11.0 as older than 13.4.0.
        # Slash-joined so the cell value stays one whitespace-free token.
        return f"cache {rec.fetched_keys[key].replace(', ', '/')} {today}"
    if key in rec.disk_keys:
        return f"skills-dir {today}"
    return f"none {today}"


def machine_evidence(today, home=None):
    """(exact-name map, unambiguous identity-key map) of install values for every
    catalogued ADOPT/KEEP row, from this machine's records.

    TWO MAPS, EXACT NAME FIRST, because `name_key` is not an identity here: `agent-skills`
    (addyosmani, a skill) and `agentskills` (the SKILL.md spec, a reference) both key to
    `agentskills`, and a single map would hand one row the other's install fact. Detector
    U's rule — an ambiguous fallback resolves to nothing rather than to a coin flip — so a
    key claimed by two rows is dropped from the fallback map entirely and only the exact
    name can reach those rows.

    Returns ({}, {}) when the machine holds no records at all."""
    rec = read_records(home)
    if rec is None:
        return {}, {}

    ctx = ae.DetectorContext(ROOT)
    verd = ctx.comparison_verdict_map

    exact, by_key, owner, ambiguous = {}, {}, {}, set()
    for r in catalog_lib.parse_catalog_rows(ctx.catalog):
        if not r.url:
            continue
        ids = catalog_lib.identity_keys(r.name)
        if next((verd[k] for k in ids if k in verd), None) not in ae.SETTLED_VERDICTS:
            continue
        if (r.type or "").strip() not in ae.INSTALLABLE_TYPES:
            value = "n/a"             # unobservable by these records — not "absent"
        else:
            slug = (next(iter(catalog_lib.github_repos(r.url)), "") or "").lower()
            value = classify(slug, ids[0], today, rec)
        exact[r.name] = value
        for k in ids:
            # Ambiguity is about IDENTITY, not about the values agreeing. Two rows keying
            # alike is a collision even when today's answers happen to match.
            if owner.setdefault(k, r.name) != r.name:
                ambiguous.add(k)
            by_key.setdefault(k, value)
    return exact, {k: v for k, v in by_key.items() if k not in ambiguous}


def _plugin_record_names(home):
    """Names from installed_plugins.json alone.

    Detector Y merges this file with the ~/.claude/skills/ listing into one `on_disk` set,
    because for its purposes either one answers "something is here". The column has to tell
    them apart — a recorded plugin is a stronger fact than a bare directory — so this reads
    the one file again rather than changing Y's return shape out from under its callers."""
    p = os.path.join(home, ae.PLUGIN_RECORD.replace("~/", "")) if home \
        else os.path.expanduser(ae.PLUGIN_RECORD)
    try:
        with open(p, encoding="utf-8") as fh:
            return {catalog_lib.name_key(k.split("@")[0])
                    for k in (json.load(fh).get("plugins") or {})}
    except (OSError, ValueError, AttributeError):
        return set()


def rewrite(text, evidence):
    """Ledger text with the column rewritten from `evidence` (the pair machine_evidence
    returns).

    A row the machine has no entry for keeps whatever it already declared — a refresh that
    cannot see a tool must not erase an earlier run's dated record of it. The header and
    separator are widened in the same pass rather than by a literal string replace, so a
    reformatted separator can't leave six-cell rows under a five-cell header."""
    out, seen_header, pending_separator = [], False, False
    for raw in text.splitlines(keepends=True):
        line = raw.rstrip("\n")
        if not seen_header and _HEADER_ROW.match(line):
            seen_header = True
            pending_separator = not line.rstrip().endswith(f"{HEADER} |")
            out.append(raw if not pending_separator else f"{line.rstrip()} {HEADER} |\n")
            continue
        if pending_separator:
            # Only the separator immediately under the widened header — the batch-exclusion
            # table further down has its own, and widening that one would corrupt it.
            pending_separator = False
            if _SEPARATOR.match(line):
                out.append(f"{line.rstrip()}--------------------|\n")
                continue
        m = _ROW.match(line)
        if not m:
            out.append(raw)
            continue
        name, verdict, stage, in_stack, reason, tail = m.groups()
        value = _lookup(evidence, name) or _existing_value(tail) or "n/a"
        out.append(f"| {name} | {verdict} |{stage}|{in_stack}|{reason}| {value} |\n")
    return "".join(out)


def _lookup(evidence, name):
    """Exact catalog name first, then the unambiguous identity keys — the order that keeps
    `agent-skills` and `agentskills` apart."""
    exact, by_key = evidence
    if name in exact:
        return exact[name]
    return next((by_key[k] for k in catalog_lib.identity_keys(name) if k in by_key), None)


def _existing_value(tail):
    return next((c for c in (c.strip() for c in tail.split("|")) if VALUE.match(c)), None)


def audit(text):
    """[(what, problem)] for a header or ADOPT/KEEP row whose column is missing or
    malformed. Shape only — this never asserts that a recorded value is still true."""
    problems, seen_header = [], False
    for line in text.splitlines():
        if not seen_header and _HEADER_ROW.match(line):
            seen_header = True
            if not line.rstrip().endswith(f"{HEADER} |"):
                problems.append(("(table header)", f"no `{HEADER}` column"))
            continue
        m = _ROW.match(line)
        if not m:
            continue
        name, _v, _s, _i, _r, tail = m.groups()
        if _existing_value(tail) is None:
            cells = [c.strip() for c in tail.split("|") if c.strip()]
            problems.append((name.strip(), f"no valid `{HEADER}` value"
                                           + (f" (found {cells[0]!r})" if cells else "")))
    return problems


def main(argv):
    text = Path(LEDGER).read_text(encoding="utf-8")

    if "--check" in argv:
        problems = audit(text)
        if problems:
            print(f"install-evidence check: {len(problems)} ADOPT/KEEP row(s) with no "
                  f"well-formed `{HEADER}` value")
            for name, why in problems:
                print(f"  {name}: {why}")
            print("  run `./verify-installs.py --record` on the machine these records "
                  "describe (ADR-0006)")
            return 1
        print(f"install-evidence check: OK — every ADOPT/KEEP row declares `{HEADER}`")
        return 0

    if "--record" not in argv:
        print("usage: verify-installs.py --record | --check")
        print("  --record  rewrite STACK-LEDGER.md's `Install evidence` column from THIS")
        print("            machine's install records (local only — ADR-0006)")
        print("  --check   validate the column's shape; offline, safe in CI")
        return 2

    today = datetime.date.today().isoformat()
    evidence = machine_evidence(today)
    exact = evidence[0]
    if not exact:
        # 0 records, never 0 findings: a machine with no install records is one we know
        # nothing about, and overwriting the column from it would assert a check that
        # never happened.
        print("install-evidence: 0 install records on this machine — nothing rewritten")
        return 0
    new = rewrite(text, evidence)
    if new == text:
        print("install-evidence: already current")
        return 0
    Path(LEDGER).write_text(new, encoding="utf-8")
    counts = {}
    for v in exact.values():
        counts[v.split()[0]] = counts.get(v.split()[0], 0) + 1
    print(f"install-evidence: recorded {len(exact)} row(s) — "
          + ", ".join(f"{k} {n}" for k, n in sorted(counts.items())))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
