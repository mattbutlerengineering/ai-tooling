#!/usr/bin/env python3
"""
triage.py — band the 461 `discovery-log` leads and regenerate NEXT-EVALS.md.

`next-evals.py` scores leads; this decides what may be *done* with each one. The
score alone cannot order the queue: 176 leads have zero overlap pressure and the
whole set collapses into ~83 distinct scores (largest tie: 45 tools), so below
roughly rank 100 a ranked table is alphabetical order wearing a costume. Bands are
honest about the resolution the signal actually has.

Every band states the disposition an unattended agent may reach. The rule that
makes bulk triage safe is ELIMINATE-ONLY: an agent may SKIP a lead or leave it at
discovery-log; it may never emit ADOPT/KEEP/CONDITIONAL. A false SKIP is cheap and
reversible; a false ADOPT poisons STACK. Enforced mechanically by detector Q
(audit-evals.py), not by trust.

Two facts about a repo come from `repo-metadata.json` (refresh-metadata.py), since
they live nowhere in this repo's own files:

  mechanical-skip  a VENDORED artifact (skill/plugin — prompt text copied into a
                   repo) under a license that forbids it. Scoped to vendored types
                   on purpose: AGPL on a CLI you merely *run* imposes nothing, and
                   a naive copyleft rule SKIPs anthropics/claude-code (no license,
                   Type reference) and firecrawl while letting a CC-BY-SA skill
                   through, where ShareAlike genuinely reaches the copied text.
  successor-check  archived. NOT a SKIP: Roo-Code, void and gpt-engineer are
                   archived because they MOVED. Find the successor or SKIP with a
                   reason — never dispose on a metadata bit alone.

  ./triage.py          # apply: regenerate NEXT-EVALS.md
  ./triage.py --check  # verify only: exit 1 if stale; mutate nothing
"""
import os, re, sys, json, importlib.util

import catalog_lib

ROOT = os.path.dirname(os.path.abspath(__file__))


def _load(mod, filename):
    spec = importlib.util.spec_from_file_location(mod, os.path.join(ROOT, filename))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


ae = _load("audit_evals", "audit-evals.py")
nexteval = _load("next_evals", "next-evals.py")   # rank() + the scoring weights

NEXT = os.path.join(ROOT, "NEXT-EVALS.md")
CACHE = os.path.join(ROOT, "repo-metadata.json")
START, END = "<!-- NEXT-EVALS:START -->", "<!-- NEXT-EVALS:END -->"

MEASURE_HEAD = 25   # leads shown in the human/eval-runner band (the old TOP_N)
BAND_SAMPLE = 12    # rows listed per bulk band; the band's full size is always printed

# Types whose artifact is COPIED INTO a repo, so its license binds our source.
# A tool/harness/platform/framework is executed, not vendored — license recorded,
# never disposing. See the module docstring for why this asymmetry is the point.
VENDORED_TYPES = frozenset({"skill", "plugin"})

# Licenses that disqualify a vendored artifact: none declared, or copyleft/ShareAlike
# that would reach text we copy in. NOASSERTION is EXCLUDED on purpose — it means
# GitHub could not parse the LICENSE file, not that one is absent; auto-SKIPping those
# would kill ~48 leads on a reason nobody read.
DISQUALIFYING_LICENSE = re.compile(r"^(NONE|A?GPL|CC-BY-SA|EUPL)", re.I)

LAST_TRIAGED = re.compile(r"^\*\*Last triaged:\*\*\s*(\d{4}-\d{2}-\d{2})", re.M)

BANDS = (
    ("P0 measure", "score-ranked head",
     "human or `eval-runner` only — the one band that may reach ADOPT"),
    ("P1 successor-check", "`archived == true`",
     "repoint the link to a successor, or SKIP \"archived, no successor\""),
    ("P2 challenger", "overlaps a tool already in STACK",
     "SKIP \"redundant with `<incumbent>`\", or leave at discovery-log"),
    ("P3 backlog", "everything else",
     "leave; stamp `**Last triaged:**` only"),
    ("P4 mechanical-skip", "vendored Type under a disqualifying license",
     "SKIP — zero judgement"),
)


def load_metadata():
    """slug -> repo facts. Absent cache is not fatal: the metadata-derived bands
    simply come back empty and every lead falls through to the score-based ones,
    which keeps `triage.py --check` runnable on a fresh clone before the first
    networked refresh."""
    if not os.path.exists(CACHE):
        return {}
    with open(CACHE, encoding="utf-8") as f:
        return json.load(f)


def catalog_facts(catalog_text):
    """name_key(tool) -> (Type, slug, overlaps cell) for every catalogued row."""
    facts = {}
    for row in catalog_lib.parse_catalog_rows(catalog_text):
        repos = catalog_lib.github_repos(row.url) if row.url else []
        slug = repos[0].lower() if repos else None
        facts[catalog_lib.name_key(row.name)] = (row.type, slug, row.overlaps or "")
    return facts


def stack_keys(stack_text):
    """Alias keys of every STACK pick — reuses detector J's parser so the queue and
    the drift gate can never disagree about what is 'in STACK'."""
    return ae._stack_member_keys(stack_text)


def overlaps_stack(overlaps_cell, skeys):
    """True when a lead cites a STACK pick in its 'Overlaps with' cell — i.e. it is
    a challenger to an incumbent we already install, and therefore decidable fast."""
    for tok in overlaps_cell.split(","):
        key = catalog_lib.name_key(catalog_lib.strip_parenthetical(tok))
        if key and key in skeys:
            return True
    return False


def last_triaged_map(ctx):
    """alias name_key -> the eval's **Last triaged:** date, for leads already looked
    at. Recently-triaged leads sort last within their band so each pass surfaces
    genuinely un-examined ones and the queue converges instead of re-shuffling."""
    seen = {}
    for ev in ctx.evals:
        m = LAST_TRIAGED.search(ev.text)
        if not m:
            continue
        for a in ev.name_aliases:
            seen.setdefault(a, m.group(1))
    return seen


def positive_reads(ctx):
    """alias name_key -> tentative verdict, for leads whose eval already reads ADOPT
    or KEEP.

    A discovery-log eval still carries a `## Verdict` line: per COMPARISON.md's legend
    it is "the eval's tentative read — notes, not a recommendation". Promoting such a
    lead to SKIP is the point of bulk triage. But where that read is POSITIVE, a bulk
    SKIP would have an unattended pass overrule a human who looked and liked it —
    vercel-labs/agent-skills reads ADOPT *with its missing license in view*. Eliminate-
    only cuts both ways: the lane may not contradict a positive read either. These
    leads fall through to the score-based bands, where a human decides.

    Keys on `ev.verdict` (the headline token) and never `verdict_set`, which collects
    every verdict WORD in the section: trailofbits/skills reads "Held at CONDITIONAL
    rather than ADOPT", so its set contains ADOPT while its verdict does not."""
    reads = {}
    for ev in ctx.evals:
        if ev.verdict in catalog_lib.RECOMMENDED_VERDICTS:
            for a in ev.name_aliases:
                reads.setdefault(a, ev.verdict)
    return reads


def band_of(tool, facts, meta, reads):
    """The metadata-derived band for a lead, or None when the score-based bands
    (measure / challenger / backlog) decide it. Structural facts win: a lead that is
    archived or license-disqualified is banded on that fact regardless of its score —
    unless its eval already reads ADOPT/KEEP, which no bulk lane may overrule."""
    if any(a in reads for a in catalog_lib.alias_keys(tool)):
        return None
    typ, slug, _ = facts.get(catalog_lib.name_key(tool), (None, None, ""))
    m = meta.get(slug) if slug else None
    if not m:
        return None
    lic = m.get("license_spdx") or ""
    if typ in VENDORED_TYPES and DISQUALIFYING_LICENSE.match(lic):
        return "P4 mechanical-skip"
    if m.get("archived"):
        return "P1 successor-check"
    return None


def assign(ctx):
    """tool -> band for every discovery-log lead, plus the ranked rows.

    Precedence: the structural bands (P4 mechanical-skip, P1 successor-check) claim a
    lead first, because they rest on facts rather than a heuristic score. The score
    head (P0 measure) is taken from what remains — so a top-ranked lead is never
    demoted into P2 challenger, where an agent could SKIP it as 'redundant'.
    """
    ranked = nexteval.rank(ctx)
    facts = catalog_facts(ctx.catalog)
    meta = load_metadata()
    skeys = stack_keys(ctx.stack)
    triaged = last_triaged_map(ctx)
    reads = positive_reads(ctx)

    bands = {}
    for row in ranked:
        b = band_of(row[1], facts, meta, reads)
        if b:
            bands[row[1]] = b

    head = [r for r in ranked if r[1] not in bands][:MEASURE_HEAD]
    for r in head:
        bands[r[1]] = "P0 measure"

    for row in ranked:
        tool = row[1]
        if tool in bands:
            continue
        _, _, overlaps = facts.get(catalog_lib.name_key(tool), (None, None, ""))
        bands[tool] = "P2 challenger" if overlaps_stack(overlaps, skeys) else "P3 backlog"

    # Within a band, an already-triaged lead sinks: fresh leads first.
    def sort_key(row):
        stamped = any(a in triaged for a in catalog_lib.alias_keys(row[1]))
        return (1 if stamped else 0, -row[0], -row[3], row[1])

    ordered = {name: sorted((r for r in ranked if bands[r[1]] == name), key=sort_key)
               for name, _, _ in BANDS}
    return ordered, ranked


def render(ordered, ranked):
    """NEXT-EVALS.md in full. Bands replace the old flat top-25 table; every band
    prints its true size, and any band listing only a sample says so — the repo's
    no-silent-caps rule."""
    total = len(ranked)
    lines = [
        "# Next evals — a banded promotion queue",
        "",
        f"The {total} `discovery-log` leads, **derived** (not hand-maintained) from data "
        "already in the repo plus `repo-metadata.json`. Regenerate with `python3 triage.py`; "
        "do not edit between the markers.",
        "",
        "Leads are grouped into **bands**, not a single ranked list. Within a band the order "
        "is `2*overlap_pressure + stage_gap_weight + evidence_bonus` (see `next-evals.py`), "
        "but that score only has ~83 distinct values across these leads — enough to pick a "
        "head, not to rank a tail. Leads already stamped `**Last triaged:**` sink within "
        "their band so each pass surfaces un-examined ones.",
        "",
        "**Eliminate-only.** Outside `P0 measure`, an unattended agent may SKIP a lead or "
        "leave it at `discovery-log`; it may never write ADOPT/KEEP/CONDITIONAL. A false SKIP "
        "is cheap and reversible; a false ADOPT poisons STACK. Detector Q gates this.",
        "",
        "| Band | Definition | Leads | An agent may conclude |",
        "|------|------------|-------|-----------------------|",
    ]
    for name, definition, disposition in BANDS:
        lines.append(f"| **{name}** | {definition} | {len(ordered[name])} | {disposition} |")
    lines += ["", START, ""]

    for name, _, disposition in BANDS:
        rows = ordered[name]
        lines.append(f"## {name} — {len(rows)} leads")
        lines.append("")
        lines.append(f"_{disposition}._")
        lines.append("")
        if not rows:
            lines += ["_(none)_", ""]
            continue
        shown = rows if name == "P0 measure" else rows[:BAND_SAMPLE]
        if len(shown) < len(rows):
            lines.append(f"_Listing {len(shown)} of {len(rows)} — rerun `python3 triage.py` "
                         "and read the source for the tail (no silent cap)._")
            lines.append("")
        lines.append("| Tool | Stage | Score | Why (pressure/gap) | Command |")
        lines.append("|------|-------|-------|--------------------|---------|")
        cmd = "/evaluate-tool" if name == "P0 measure" else "/triage-lead"
        for score, tool, stage, op, gap in shown:
            lines.append(f"| {tool} | {stage} | {score:.1f} | pressure {op}, gap {gap:.1f} "
                         f"| `{cmd} {tool}` |")
        lines.append("")

    lines += [END, ""]
    return "\n".join(lines)


def apply(ctx):
    return render(*assign(ctx))


def main():
    check = "--check" in sys.argv[1:]
    ctx = ae.DetectorContext(ROOT)
    new = apply(ctx)
    current = open(NEXT, encoding="utf-8").read() if os.path.exists(NEXT) else None
    if check:
        if new != current:
            print("triage check: DRIFT — NEXT-EVALS.md is stale; run ./triage.py")
            sys.exit(1)
        print("triage check: OK — NEXT-EVALS.md matches the derived bands")
        sys.exit(0)
    if new != current:
        open(NEXT, "w", encoding="utf-8").write(new)
        print("triage: regenerated NEXT-EVALS.md")
    else:
        print("triage: NEXT-EVALS.md already up to date")


if __name__ == "__main__":
    main()
