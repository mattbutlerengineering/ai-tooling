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
  ./watchlist.py --check  # verify only: exit 1 if the page is out of date; mutate nothing

--check gates every section except 3. Section 3 (the staleness report) is derived from
today's date rather than file content, so it is excluded — see render() and
_without_stale_block. Apply mode always rewrites the whole page.
"""
import importlib.util
import os
import re
import sys
from pathlib import Path

import catalog_lib

ROOT = os.path.dirname(os.path.abspath(__file__))
# Load audit-evals as a module (its filename is hyphenated) to reuse the detector
# functions directly — never re-implement staleness / savings-claims / skill-backlog
# here, and never shell out to parse their text output.
_spec = importlib.util.spec_from_file_location("audit_evals", os.path.join(ROOT, "audit-evals.py"))
if _spec is None or _spec.loader is None:  # a sibling in this repo — absent means a broken checkout
    raise ImportError("cannot load audit-evals.py; is the checkout complete?")
ae = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(ae)

WATCHLIST = os.path.join(ROOT, "WATCHLIST.md")
START, END = "<!-- WATCHLIST:START -->", "<!-- WATCHLIST:END -->"
# Section 3 is the one part of this page derived from `datetime.date.today()` rather than
# from file content, so it is wrapped in its own markers and excluded from `--check`'s
# comparison. The staleness sweep is REPORT-ONLY (see CLAUDE.md and audit_staleness's
# docstring, and the `-`-prefixed staleness line in the Makefile); gating on it turned a
# calendar date into a red CI run with zero commits — 184 evals cross a threshold on
# 2026-10-21 alone. `make fix` still refreshes the section.
STALE_START, STALE_END = "<!-- WATCHLIST:STALE:START -->", "<!-- WATCHLIST:STALE:END -->"

# Section 1: the conditional clause in a DEFER eval's Verdict is its trigger sentence
# (TEMPLATE.md: "DEFER = ... re-evaluate after {trigger}").
#
# WIDEN THIS VOCABULARY, NEVER NARROW IT (#416). The single `re-evaluate (after|when)`
# pattern this replaces recovered 2 of 4 triggers, and the two it missed had stated
# theirs plainly in other words — letta's "becomes a clear ADOPT only if your goal
# shifts…", SkillOpt's "adopt once a turnkey path … exists". The page then printed
# `_NO_TRIGGER` beside them under prose reading "A missing trigger is itself an action
# item", manufacturing a backlog item asking a human to write down what was already
# written. That is detector V's rule — flagging a healthy row costs more than missing a
# sick one — and the remedy is the same one `HONEST` and the clearance vocab use: a
# wider vocabulary can only REMOVE a false action item, never add one.
#
# The earliest match across all patterns wins, so the eval's own sentence order decides
# rather than the order these are listed in. `;` terminates as well as `.`: these
# verdicts join independent clauses with it, and the trigger is the first — without it
# letta's cell trails "; for the dev loop it documents, defer" into a "Re-evaluate when"
# column. No currently-recovered trigger contains one, so this cannot rewrite them.
_TRIGGER_RES = (
    re.compile(r"re-?evaluate\s+(?:after|when|once|if)\s+([^\n]*?)[.;](?:\s|$)", re.IGNORECASE),
    re.compile(r"revisit\s+(?:after|when|once|if)\s+([^\n]*?)[.;](?:\s|$)", re.IGNORECASE),
    re.compile(r"\bADOPT\b[^.;\n]*?\bonly\s+(?:if|when|once)\s+([^\n]*?)[.;](?:\s|$)", re.IGNORECASE),
    re.compile(r"\badopts?\s+(?:once|if|when)\s+([^\n]*?)[.;](?:\s|$)", re.IGNORECASE),
)
_VERDICT_SECTION = re.compile(r"##\s*Verdict.*?(?=\n##\s|\Z)", re.DOTALL)
_NO_TRIGGER = "trigger not recorded — add one"
# An eval-only DEFER has no COMPARISON row to take a stage from; read its own header.
_EVAL_STAGE = re.compile(r"^\*\*Dev loop stage:\*\*\s*([^\n|]+)", re.MULTILINE)

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


def eval_trigger(ev):
    """The re-evaluate trigger stated in an eval's `## Verdict`, or None. Earliest match
    across _TRIGGER_RES wins, so the eval's own sentence order decides. A captured `|`
    would silently break the markdown table this feeds, so it is escaped here — the cell
    is a prose sentence an eval author wrote, not a controlled value."""
    if ev is None:
        return None
    vsec = _VERDICT_SECTION.search(ev.text)
    if not vsec:
        return None
    best = None
    for rx in _TRIGGER_RES:
        m = rx.search(vsec.group(0))
        if m and (best is None or m.start(1) < best.start(1)):
            best = m
    return best.group(1).strip().replace("|", r"\|") if best else None


def deferred(ctx):
    """(tool, stage, trigger, eval_or_None) for every DEFER in the repo, trigger pulled
    from the eval's Verdict section. Returns the list plus the count whose trigger could
    not be recovered (no eval / no Verdict section / no sentence) — the caller STOPs if
    that count is implausibly high (a data problem, not a bug).

    Sourced from DEFER *verdicts*, not DEFER *rows* (#416). Reading COMPARISON alone made
    this section blind to a DEFER an eval carries without a row, and the one such eval is
    the most actionable item the page exists to list: `agentmemory-vs-claude-mem-bakeoff`,
    the tree's only `**Status:** BLOCKED`, a designed three-arm pilot waiting on one
    attended run. It has no row *correctly* — a bake-off between two tools that each
    already have one is a comparison document whose rows are references, not claims
    (detector AD's rule) — so the fix is to widen the source, not to add a row. Same root
    as #412 one page over: a derived surface asked COMPARISON for something the eval
    corpus holds more of. This function already opened every eval to fetch the trigger;
    the index was in hand when it chose the row set.

    An eval-only entry takes its stage from its own `**Dev loop stage:**` header and is
    returned with its Evaluation so the caller can render it as an eval link — a reader
    must be able to see why it has no COMPARISON line to click."""
    by_section = catalog_lib.comparison_rows_by_section(ctx.comparison)
    # alias name_key -> Evaluation, so a COMPARISON tool name finds its eval file. This
    # is an ALIAS map by design (catalog_lib.identity_keys' docstring): a row named GSD
    # must reach obra/superpowers' eval, so the lookup keeps its basename fallback.
    eval_by_alias = {}
    for ev in ctx.evals:
        for a in ev.name_aliases:
            eval_by_alias.setdefault(a, ev)
    out, missing, seen = [], 0, set()
    for stage, rows in by_section.items():
        for r in rows:
            if r.verdict != "DEFER":
                continue
            ev = next((eval_by_alias[k] for k in catalog_lib.alias_keys(r.tool)
                       if k in eval_by_alias), None)
            if ev is not None:
                seen.add(ev.name)
            out.append((r.tool, stage, eval_trigger(ev) or _NO_TRIGGER, None))
    comp = ctx.comparison_verdict_map
    for ev in ctx.evals:
        if ev.verdict != "DEFER" or ev.name in seen:
            continue
        if any(a in comp for a in ev.name_aliases):
            continue  # has a row; already emitted above (under the row's own name)
        m = _EVAL_STAGE.search(ev.text)
        out.append((ev.name, m.group(1).strip() if m else "—",
                    eval_trigger(ev) or _NO_TRIGGER, ev))
    missing = sum(1 for t in out if t[2] == _NO_TRIGGER)
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
                       re.search(r"flagged|pending", l, re.IGNORECASE) and "Tool" in l), None)
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
    """The full WATCHLIST.md text. Fully regenerated each run (markers wrap the body so a
    future tool can locate the block). Every section is derived from file content and
    gated by `--check` — except section 3.

    Section 3's stale *set* comes from `datetime.date.today()`, so it changes on a calendar
    date with nothing committed (184 evals cross a threshold on 2026-10-21 alone). It is
    wrapped in STALE_START/STALE_END and excluded from the `--check` comparison by
    _without_stale_block — the staleness sweep is report-only, and gating on it would fail
    CI on every open PR and inside every unattended routine run for reasons no diff could
    explain. `make fix` still regenerates it, so the report stays current.

    Any future section derived from wall-clock time needs the same treatment; the rule is
    that `--check` gates only what is derived from file content."""
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
        "Every `DEFER` verdict in the repo: promising but blocked, each with the "
        "re-evaluate trigger from its eval's `## Verdict` (per TEMPLATE.md's DEFER "
        "definition). A missing trigger is itself an action item. Most are "
        "[COMPARISON.md](COMPARISON.md) rows; an _eval-only_ entry is a DEFER carried by "
        "an eval with no catalog row — a bake-off or comparison document, whose subjects "
        "have their own rows — so it is linked to the eval instead.",
        "",
        "| Tool | Stage | Re-evaluate when |",
        "|------|-------|------------------|",
    ]
    if defer_rows:
        for tool, stage, trigger, ev in defer_rows:
            cell = f"[{tool}](evaluations/{ev.name}.md) _(eval-only)_" if ev else tool
            L.append(f"| {cell} | {stage} | {trigger} |")
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
        STALE_START,
        f"## 3. Stale / undated evals ({len(stale)} stale)",
        "",
        "A point-in-time eval rots. The staleness sweep flags evals whose "
        "`**Last verified:**` date is older than its category threshold. This section is a "
        "**report**, refreshed by `make fix` — it is the one part of this page derived from "
        "today's date rather than from file content, so `watchlist.py --check` does not gate "
        "on it. Ages are not printed; only the crossing matters.",
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
        STALE_END,
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


def _without_stale_block(text):
    """The page with section 3 elided — the surface `--check` gates on. Everything else
    here is derived purely from file content and stays gated; section 3 is derived from
    today's date, so byte-comparing it would fail the gate on a calendar date with zero
    commits. Markers absent (a page written before they existed) means gate the whole
    text — a missing marker must not silently un-gate the page."""
    if text is None:
        return None
    i, j = text.find(STALE_START), text.find(STALE_END)
    if i == -1 or j == -1:
        return text
    return text[:i] + text[j + len(STALE_END):]


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

    current = Path(WATCHLIST).read_text(encoding="utf-8") if os.path.exists(WATCHLIST) else None
    if check:
        # Compare with section 3 elided; apply mode below still writes the full text, so
        # `make fix` keeps the staleness report fresh even though the gate ignores it.
        if _without_stale_block(new) != _without_stale_block(current):
            print("watchlist check: DRIFT — WATCHLIST.md is stale; run ./watchlist.py")
            sys.exit(1)
        print("watchlist check: OK — WATCHLIST.md matches the derived watchlist")
        sys.exit(0)
    if new != current:
        Path(WATCHLIST).write_text(new, encoding="utf-8")
        print("watchlist: regenerated WATCHLIST.md")
    else:
        print("watchlist: WATCHLIST.md already up to date")


if __name__ == "__main__":
    main()
