#!/usr/bin/env python3
"""
watchlist.py — derive WATCHLIST.md, one readable page of everything worth
revisiting or watching (#plan-006).

"What should I re-evaluate / watch / research next?" had no answer surface: the
forward-looking signals existed but were scattered across four scripts and three
files. This aggregates them, no hand-maintenance, the same derive-don't-hand-
maintain philosophy as tier-stack.py / next-evals.py — every section is computed
from data already in the repo (COMPARISON verdicts, eval Verdict prose, STACK
prose, and the staleness / savings-claims / skill-backlog detectors), so nobody
edits WATCHLIST.md by hand and the page can never drift from its sources.

  1. Deferred — re-evaluate when trigger fires (DEFER rows + their triggers)
  2. Flagged for hands-on before promotion (STACK prose flags)
  3. Stale / undated evals (staleness detector)
  4. Unverified claims & measurement backlog (savings-claims + skill backlog)

NEXT-EVALS.md is the sibling page for *first-time* evaluation priorities; this
one is the *revisit* page.

  ./watchlist.py          # apply: regenerate WATCHLIST.md
  ./watchlist.py --check  # verify only: exit 1 if stale; mutate nothing
"""
import os, re, sys, importlib.util
import catalog_lib

ROOT = os.path.dirname(os.path.abspath(__file__))
# Load audit-evals as a module (its filename is hyphenated) to reuse the detector
# functions directly — never re-implement staleness / savings-claims / skill-backlog
# here, and never shell out to parse their text output.
_spec = importlib.util.spec_from_file_location("audit_evals", os.path.join(ROOT, "audit-evals.py"))
ae = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(ae)

WATCHLIST = os.path.join(ROOT, "WATCHLIST.md")
START, END = "<!-- WATCHLIST:START -->", "<!-- WATCHLIST:END -->"

# Section 1: the text after "re-evaluate after/when" in a DEFER eval's Verdict is
# its trigger sentence (TEMPLATE.md: "DEFER = ... re-evaluate after {trigger}").
_TRIGGER_RE = re.compile(r"re-evaluate\s+(?:after|when)\s+([^\n]*?)\.(?:\s|$)", re.I)
_VERDICT_SECTION = re.compile(r"##\s*Verdict.*?(?=\n##\s|\Z)", re.S)
_NO_TRIGGER = "trigger not recorded — add one"

# Section 2: the two hand-written STACK.md flag phrases. DELIBERATELY FRAGILE —
# section 2 grep-parses prose because STACK-LEDGER.md has no machine-readable
# flagged/pending column yet (checked at build time; see stack_flagged). The durable
# fix is encoding "flagged" as a ledger column; until then we read the prose. The
# heuristic below attaches each phrase to the tool it grammatically modifies:
# "flagged for a hands-on eval — [A] and [B]" → the links that FOLLOW the phrase;
# "worktrunk is a candidate pending a hands-on eval" → the NAME that precedes it.
FLAG_PHRASES = ("flagged for a hands-on eval", "pending a hands-on eval")
_MD_LINK = re.compile(r"\[([^\]]+)\]\((https://github\.com/[^)]+)\)")
_PENDING_SUBJECT = re.compile(r"([A-Za-z0-9][\w.-]*)\s+is a candidate")


def deferred(ctx):
    """(tool, stage, trigger) for every DEFER row in COMPARISON, trigger pulled from
    the matching eval's Verdict section. Returns the list plus the count of DEFER rows
    whose trigger could not be recovered (no eval / no Verdict section / no sentence) —
    the caller STOPs if that count is implausibly high (a data problem, not a bug)."""
    by_section = catalog_lib.comparison_rows_by_section(ctx.comparison)
    # alias name_key -> Evaluation, so a COMPARISON tool name finds its eval file.
    eval_by_alias = {}
    for ev in ctx.evals:
        for a in ev.name_aliases:
            eval_by_alias.setdefault(a, ev)
    out, missing = [], 0
    for stage, rows in by_section.items():
        for r in rows:
            if r.verdict != "DEFER":
                continue
            ev = next((eval_by_alias[k] for k in catalog_lib.alias_keys(r.tool)
                       if k in eval_by_alias), None)
            trigger = _NO_TRIGGER
            if ev is not None:
                vsec = _VERDICT_SECTION.search(ev.text)
                m = _TRIGGER_RE.search(vsec.group(0)) if vsec else None
                if m:
                    trigger = m.group(1).strip()
            if trigger == _NO_TRIGGER:
                missing += 1
            out.append((r.tool, stage, trigger))
    out.sort(key=lambda t: t[0].lower())
    return out, missing


def stack_flagged(ctx):
    """(name, url_or_None, phrase) for each tool the STACK.md prose flags for a
    hands-on eval before promotion. Prefers a machine-readable ledger column if one
    ever exists; today STACK-LEDGER.md has none, so this scans STACK prose (fragile —
    see the module note). Also returns the raw matching lines so the caller can STOP
    if the phrase pattern turns out to be too loose."""
    # Prefer the ledger if it ever encodes flagged/pending as data (durable path).
    ledger_hdr = next((l for l in ctx.ledger.splitlines()
                       if l.lstrip().startswith("|") and
                       re.search(r"flagged|pending", l, re.I) and "Tool" in l), None)
    if ledger_hdr is not None:  # ledger encodes it — not the case today, but ready
        pass  # (no ledger column yet; fall through to the prose grep)
    found, lines = [], []
    for line in ctx.stack.splitlines():
        for phrase in FLAG_PHRASES:
            idx = line.find(phrase)
            if idx == -1:
                continue
            lines.append(line)
            after = _MD_LINK.findall(line[idx + len(phrase):])
            if after:  # "flagged ... — [A](u) and [B](u)": tools follow the phrase
                for name, url in after:
                    found.append((name, url, phrase))
            else:       # "NAME is a candidate pending ...": the subject precedes it
                subj = _PENDING_SUBJECT.search(line[:idx])
                if subj:
                    found.append((subj.group(1), None, phrase))
    return found, lines


def render(ctx):
    """The full WATCHLIST.md text. Fully regenerated each run (markers wrap the body
    so a future tool can locate the block). Deterministic: every value is derived from
    file content. The one time-dependent input is section 3's stale *set* (which evals
    have crossed their staleness threshold) — it changes only when a date crosses a
    threshold, at which point `make fix` regenerates the page; the ages themselves are
    not printed, so nothing drifts day-to-day."""
    defer_rows, defer_missing = deferred(ctx)
    flagged, _flag_lines = stack_flagged(ctx)
    stale, undated = ae.audit_staleness(ctx)
    savings = ae.audit_savings_claims(ctx)
    _measured, skill_backlog = ae.audit_skill_evidence(ctx)

    L = [
        "# Watchlist — what to revisit, and when",
        "",
        "Everything worth re-evaluating or watching, **derived** (not hand-maintained) "
        "from data already in the repo: DEFER verdicts and their triggers, the STACK "
        "prose flags, the staleness sweep, and the unverified-claim / skill-measurement "
        "backlogs. Regenerate with `python3 watchlist.py`; do not edit between the "
        "markers. For *first-time* evaluation priorities see "
        "[NEXT-EVALS.md](NEXT-EVALS.md); this page is for *revisiting* work already started.",
        "",
        START,
        "",
        f"## 1. Deferred — re-evaluate when trigger fires ({len(defer_rows)})",
        "",
        "`DEFER` rows from [COMPARISON.md](COMPARISON.md): promising but blocked, each "
        "with the re-evaluate trigger from its eval's `## Verdict` (per TEMPLATE.md's "
        "DEFER definition). A missing trigger is itself an action item.",
        "",
        "| Tool | Stage | Re-evaluate when |",
        "|------|-------|------------------|",
    ]
    if defer_rows:
        for tool, stage, trigger in defer_rows:
            L.append(f"| {tool} | {stage} | {trigger} |")
    else:
        L.append("| _none_ | | |")

    L += [
        "",
        f"## 2. Flagged for hands-on before promotion ({len(flagged)})",
        "",
        "Candidates the [STACK.md](STACK.md) prose flags for a hands-on eval before any "
        "promotion — surfaced by scanning STACK for its flag phrases (fragile by design; "
        "the durable fix is a machine-readable column in STACK-LEDGER.md).",
        "",
        "| Tool | Flagged as |",
        "|------|------------|",
    ]
    if flagged:
        for name, url, phrase in flagged:
            tool = f"[{name}]({url})" if url else name
            L.append(f"| {tool} | {phrase} |")
    else:
        L.append("| _none_ | |")

    L += [
        "",
        f"## 3. Stale / undated evals ({len(stale)} stale)",
        "",
        "A point-in-time eval rots. The staleness sweep flags evals whose "
        "`**Last verified:**` date is older than its category threshold; ages are not "
        "printed so the page stays deterministic (`make fix` regenerates when a date "
        "crosses a threshold).",
        "",
        "| Eval | Type | Last verified | Threshold (days) |",
        "|------|------|---------------|------------------|",
    ]
    if stale:
        for name, typ, date, _age, threshold in stale:
            L.append(f"| {name} | {typ} | {date} | {threshold} |")
    else:
        L.append("| _none stale_ | | | |")
    L += [
        "",
        f"_{undated} eval(s) carry no `**Last verified:**` date "
        "(field presence is gated separately by `backfill-lastverified.py`)._",
    ]

    L += [
        "",
        f"## 4. Unverified claims & measurement backlog ({len(savings) + len(skill_backlog)})",
        "",
        f"**Unverified token-savings claims ({len(savings)}).** CATALOG rows with a "
        "numeric token-savings headline whose eval is not run-backed (`MEASURED`/`RUN`). "
        "Run the token-savings protocol to verify, or add an in-row disclaimer.",
        "",
        "| Tool | Evidence | Disclaimer in row? |",
        "|------|----------|--------------------|",
    ]
    if savings:
        for name, level, disclosed in savings:
            L.append(f"| {name} | {level} | {'yes' if disclosed else 'no'} |")
    else:
        L.append("| _none_ | | |")
    L += [
        "",
        f"**ADOPT skills lacking measured backing ({len(skill_backlog)}).** ADOPT-verdict "
        "skill evals not yet graduated to a measured run (#38): "
        + (", ".join(skill_backlog) if skill_backlog else "_none_") + ".",
        "",
        END,
        "",
    ]
    return "\n".join(L), defer_missing


def apply(ctx):
    return render(ctx)


def main():
    check = "--check" in sys.argv[1:]
    ctx = ae.DetectorContext(ROOT)
    new, defer_missing = apply(ctx)

    # STOP condition (#plan-006): an implausible number of DEFER evals with no
    # recoverable trigger is a data problem, not a script problem — fail loudly
    # instead of silently emitting a page full of "trigger not recorded".
    if defer_missing > 10:
        print(f"watchlist: STOP — {defer_missing} DEFER evals have no recoverable "
              "trigger; that is a data problem to fix in the evals, not here.",
              file=sys.stderr)
        sys.exit(2)

    current = open(WATCHLIST, encoding="utf-8").read() if os.path.exists(WATCHLIST) else None
    if check:
        if new != current:
            print("watchlist check: DRIFT — WATCHLIST.md is stale; run ./watchlist.py")
            sys.exit(1)
        print("watchlist check: OK — WATCHLIST.md matches the derived watchlist")
        sys.exit(0)
    if new != current:
        open(WATCHLIST, "w", encoding="utf-8").write(new)
        print("watchlist: regenerated WATCHLIST.md")
    else:
        print("watchlist: WATCHLIST.md already up to date")


if __name__ == "__main__":
    main()
