#!/usr/bin/env python3
"""
audit-evals.py — integrity checks for the ai-tooling catalog.

Fifteen detectors (A-O), each proven to catch real problems (see git history,
2026-06-20), plus a --selftest that unit-tests the evidence classifier:

  A. INSTALL RESOLVER — every install command in STACK.md / CATALOG.md / evaluations/
     should point at an artifact that actually exists (npm / PyPI / crates.io / GitHub).
     A broken install command is strong evidence the tool was never run.

  B. FABRICATION CLASSIFIER — an eval's "How we tested it" section should either
     disclose it was NOT run (honest review) or describe a real hands-on run.
     A section that asserts a specific run (past-tense verbs, invented metrics) with
     NO honesty disclaimer is a fabrication candidate to review.

  C. LINK ROT (opt-in, --links) — every github.com/owner/repo link in CATALOG.md
     should resolve to its canonical current name. Flags 404s (dead) and silent
     renames (moved). ~450 network requests, so it is off by default. Reports
     n/total CHECKED and says INCONCLUSIVE rather than OK when any link could not
     be verified: only a 404 means "gone", and every other failure (429 rate limit,
     5xx, timeout) is "could not check". Folding those into "ok" once made the
     sweep print a clean bill of health for 612 links while GitHub 429'd all of
     them (#319).

  D. VERDICT SYNC — each eval's "## Verdict" should agree with its COMPARISON.md
     row. Tolerates dual verdicts ("ADOPT for X — CONDITIONAL otherwise") and the
     KEEP (installed/validated) status standing in for ADOPT. Offline.

  E. SKILL EVIDENCE (opt-in, --skills, REPORT-ONLY) — a skill's value is a
     behaviour change, so an ADOPT verdict on a *skill* should rest on a measured
     eval (triggering / with-skill-vs-baseline), not a README review. Lists which
     ADOPT skills are measured vs the review-based backlog. Does NOT affect the
     exit code — it's a tracked metric, not a gate (the backlog is pre-existing).

  F. DANGLING OVERLAPS (opt-in, --overlaps, REPORT-ONLY) — an "Overlaps with"
     token naming a tool that isn't itself catalogued is either a deliberate
     external peer (allowed) or a real gap (a notable tool we forgot). The more
     rows cite the same uncatalogued token, the likelier it's a gap — this is how
     aider/continue/agenta were found. Report-only; surfaces candidates.

  G. COMPARISON CONSISTENCY — COMPARISON.md's per-stage summary must sum to its
     own body rows, and its Total must equal the CATALOG.md entry count. Catches
     manual count drift between the two authoritative files (a tool addition edits
     both). Offline, gating, on by default.

  H. ARCHIVED REPOS (opt-in, --archived, REPORT-ONLY) — a catalogued repo GitHub has
     flagged `archived` is unmaintained; the entry should carry a ⚠️ archived note or
     repoint to a successor. Link rot (C) misses this (the link still resolves).
     Found 4 (incl. gpt-engineer ★55K). Uses authenticated `gh api`; report-only.

  J. STACK-DERIVATION DRIFT — STACK.md must be derivable from the verdict data
     (COMPARISON.md) plus the exclusion ledger (STACK-LEDGER.md, #64): every ADOPT/
     KEEP tool is either in STACK or has a logged exclusion reason, ledger verdicts
     match COMPARISON, and nothing marked in-STACK is missing from STACK.md. Kills the
     hand-maintained drift prior audits kept finding. Offline, gating, on by default.

  K. VERDICT EVIDENCE GATE — a strong verdict can't rest on a README skim. An ADOPT/
     KEEP eval must be run-backed (Evidence MEASURED or RUN) or carry an explicit honesty
     disclaimer (the documented escape hatch); a REVIEW/SOURCE-ONLY ADOPT/KEEP with no
     disclaimer fails. Generalizes the skills-only report-only detector E into a catalog-
     wide gate (#71). Offline, gating, on by default.

  L. STALENESS SWEEP (opt-in, --staleness, REPORT-ONLY) — a point-in-time eval rots:
     a fast-moving harness can be wrong months after it was written. Flags evals whose
     **Last verified:** date is older than its category threshold (STALENESS_DAYS, keyed
     by Type — harnesses/MCP servers age faster than references). Report-only (#65).

  I. EVIDENCE-STRENGTH FIELD (opt-in, --evidence, REPORT-ONLY) — tallies each eval's
     declared **Evidence:** field (MEASURED / RUN / REVIEW / SOURCE-ONLY): how hard we
     looked, recorded as data and separate from the verdict (what we concluded). The
     tracer-bullet slice (issue #62) only parses and reports; backfill + a COMPARISON
     column (#67) and gating on weak backing (#71) build on it. Offline.

  M. CLUSTERS WITHOUT A PICK (opt-in, --clusters, REPORT-ONLY) — ADR 0001 / #69: a
     catalog should name ONE best-in-class ADOPT pick per overlap cluster, not hedge
     CONDITIONAL on all of them. Flags overlap clusters (connected via "Overlaps with")
     where no member is ADOPT/KEEP yet at least one is CONDITIONAL — the clusters still
     awaiting a pick. Makes the #69 migration findable; migrates nothing.

  N. TOKEN-SAVINGS CLAIMS (opt-in, --savings-claims, REPORT-ONLY) — a CATALOG row
     whose one-liner makes a numeric token-savings headline (a % or N× next to token
     vocabulary) should be run-backed (Evidence MEASURED/RUN) or carry an in-row
     self-reported/unverified disclaimer. Turns the Optimize cluster's unverified
     savings claims into a number to shrink (evaluations/token-savings-protocol.md).

  O. ROW SHAPE — a malformed table row in CATALOG.md / COMPARISON.md used to be
     silently skipped by the parse sites, quietly corrupting the counts G gates on.
     validate_catalog_rows / validate_comparison_rows (catalog_lib) report any
     unrecognized, wrong-width, indented, or nameless entry row, and any per-stage
     COMPARISON row whose Evaluated cell isn't a verdict token, with file and line
     number (#198). Offline, gating, on by default.

  P. WORKFLOW-STACK DRIFT (opt-in, --workflow-drift, REPORT-ONLY) — WORKFLOW.md and
     STACK.md must not give a newcomer two different answers to "what do I use for X".
     Every STACK pick (matched by owner/repo slug, not display name) must appear
     somewhere in WORKFLOW.md; the reverse is not required, since WORKFLOW legitimately
     lists non-STACK CONDITIONAL options. Offline.

  Q. ELIMINATE-ONLY BULK TRIAGE — an eval marked "triaged: bulk" may only read SKIP or
     stay at discovery-log; it may never carry ADOPT/KEEP/CONDITIONAL. A false SKIP is
     cheap and reversible, a false ADOPT poisons STACK, and K's honesty-disclaimer
     escape hatch would otherwise let a README skim carry an ADOPT. Also fails an
     UNATTRIBUTED stamp: a `**Last triaged:**` with neither the bulk marker nor
     `<!-- triaged: human -->` is unpoliceable, not innocent — Q can only constrain a
     lane it can identify, so a bare date looks exactly like a lane that behaved (#327).
     The human marker exempts the verdict ceiling, since reaching a real verdict is what
     a human pass is for. This is what makes eliminate-only mechanical rather than a
     promise. Offline, gating, on by default.

  S. SKILL TEST-DESIGN (opt-in, --skill-design, REPORT-ONLY) — every skill/plugin-Type
     eval should record at least one skill dimension (a Triggering test or a
     with-skill-vs-baseline A/B) per TEMPLATE.md (#38). Conservative by design: an eval
     counts as compliant on any triggering/A-B vocabulary, so an honest measured eval is
     never false-flagged. A tracked metric, not a gate. Offline.
     (Was a second "Q" until #317 — Q belongs to eliminate-only, which is referenced by
     letter in CLAUDE.md, triage.py, TEMPLATE.md, routines.md and the triage-lead skill.)

  T. LEAD HEADLINE OVERREACH (opt-in, --lead-headlines, REPORT-ONLY) — a COMPARISON row
     reading `discovery-log` says the tool was never exercised, so its eval is notes,
     not a recommendation. 324 of them nonetheless opened `## Verdict` with **CONDITIONAL**,
     a word ADR-0005 grants only to a tool we ran or one carrying a real adopt-if gate.
     #324 relabelled them to `discovery-log — tentative read`; this keeps them relabelled.
     Scoped to REVIEW/SOURCE-ONLY: a run-backed CONDITIONAL has earned the word, and
     there the row is the stale half — a human's verdict call, not a headline defect.
     Report-only; the survivors are escalations awaiting a human (#259). Offline.

  R. METADATA STALENESS (opt-in, --metadata-staleness, REPORT-ONLY) — repo-metadata.json
     is a committed snapshot the triage bands rest on, and it rots in one direction:
     a repo archived after our last refresh keeps `archived: false`, so it never
     reaches the P1 successor-check band and nobody is told. Ages the cache from the
     per-record `fetched_at` stamp refresh-metadata.py writes (`pushed_at` is the
     REPO's push date, not ours). Unstamped records report undated, never backfilled.
     Offline (#260). Cannot become a gate: it would fail for a reason no code change
     caused, and its only fix needs the network CI must not depend on.

  U. CATALOG-ENTRY MIRROR DRIFT (opt-in, --catalog-mirror, REPORT-ONLY) — TEMPLATE.md
     has every eval close with a `## Catalog entry` copy of its CATALOG.md row: a fact
     restated in ~520 places with no generator and no test, so it drifted (#345). Four
     kinds, reported apart because they are not equally dangerous. LINK — the eval and
     the catalog name different repos, so a rename leaves the eval asserting a dead
     slug and the stars/license it was written against (#336; `herdr` was SKIP-eligible
     on exactly this). ORPHAN — an embedded row naming no catalogued tool. TEXT — the
     one-liner/problem/overlaps cells disagree; not cosmetic, since triage.py bands
     leads from the overlaps cell. AMBIG — two catalog rows collapse to one name_key
     ('agent-skills' vs 'agentskills'), so the mirror cannot be identified; resolution
     is exact-name-first for this reason, and an ambiguous fallback resolves to nothing
     rather than to a coin flip. CASE — the URLs differ only in capitalization, which
     GitHub redirects; kept out of LINK so that bucket stays actionable, but printed,
     not filtered. Offline: a string comparison between two files already in the tree,
     unlike C's ~450 requests. Report-only and deliberately NOT a bulk fixer — #345's
     sequencing note is that a wholesale rewrite in either direction destroys real work
     in the other, because the eval side is sometimes the better text (`azure-skills`).

  V. MAINTENANCE SIGNAL (opt-in, --maintenance, REPORT-ONLY) — triage.py's P1
     successor-check band is `archived == true`, which only catches maintainers who
     flipped GitHub's flag. daytonaio/daytona (★72K, the catalog's canonical sandbox
     answer) announced discontinuation in its README in June 2026, moved development to
     a private codebase, kept `archived: false`, and sat in P3 backlog as ordinary
     un-examined work for two months (#351). Reports the two per-record signals
     `refresh-metadata.py --maintenance` writes: `discontinued` (the README banner
     phrase, quoted so a human judges the phrase rather than trusting the regex) and
     `license_lost` (a real license that became NONE/404 since the last snapshot).
     A match is a CANDIDATE, not a disposition: the phrase's subject may be a component
     or a version rather than the repo (giskard-oss's "no longer actively maintained"
     is about Giskard **v2** while the repo ships v3), which no regex resolves. That is
     why the phrase is quoted in the output and why this detector never bands anything.
     Deliberately NOT a pushed_at threshold — dormancy is not discontinuation, and
     `plandex` vs `ralph` is why. Sorted strongest-verdict-first: a dead tool we still
     recommend outranks a dead lead nobody was going to reach. An uncollected signal
     reports 0 RECORDS, never 0 findings — absence of the field means "not collected".
     Offline (reads the committed cache).

  W. P0 SCOPE MISMATCH (opt-in, --scope, REPORT-ONLY) — next-evals.py scores a lead as
     2*overlap_pressure + stage_gap_weight + evidence_bonus. All three terms measure how
     much ATTENTION a lead attracts; none asks whether it is a tool this catalog is FOR.
     So a row can be both clearly out of scope and highly ranked — and ranking high puts
     it in P0 measure, the one band an unattended pass may not write to (#353). Overlap
     pressure is the trap: a framework accumulates pressure from the very rows SKIPped
     alongside it, so the more thoroughly a class is eliminated, the higher its survivors
     score. `pydantic-ai` sits in P0 at pressure 12 while `agent-kit`, same class, was
     disposed in P3.
     Reports leads whose OWN EVAL concedes the WORKFLOW.md exclusion — "visual/programmatic
     agent builders — for building AI products, not for your own dev workflow" — gated to
     the framework/platform Types that exclusion is about. The detector does not decide
     scope; it finds evals that already said it, which is why the conceding phrase is
     QUOTED (V's rule) and why it bands nothing.
     Two bucketing rules keep it precise. An eval that argues it CLEARS the bar is bucketed
     apart, not counted — `fast-agent` and `sandcastle` quote the exclusion in order to
     distinguish themselves from it, and `opik`/`helicone` concede tangency while asserting
     "catalog-relevant as the obs layer". That is detector B's HONEST-vocabulary shape:
     widen the clearance vocab if it false-flags, do not tighten the concession vocab.
     The Type gate drops `mirrord` (a k8s tool whose eval says "not a coding agent" about
     itself) and `12-factor-agents` (a reference). Both survived the phrase match alone.
     Report-only: the immediate item is a HUMAN read of a P0 lead, and moving that
     authority is exactly what #353 declined to do. Offline.

  X. COLLAPSED CATALOG IDENTITY (opt-in, --identity, REPORT-ONLY) — a row that names a
     COMPONENT of an artifact catalogued as a WHOLE is not an independent lead. The P3
     lane hit this five times from both directions before it was filed (#343): three
     separate leads for skills that all ship in `mattpocock/skills` (a STACK pick), and
     `jira`+`confluence`, which are one repo. Three observed effects — the queue is
     overstated (installing the pack settles all three at once), a redundancy verdict
     between the two is meaningless (that is the same thing, not a competitor), and the
     eliminate-only band cannot act, so every pass spends a note re-explaining why.
     Groups catalog rows by resolved `owner/repo` and splits them by whether the CATALOG
     links already distinguish the rows:
       SETTLED   — a discovery-log lead sharing a slug with an ADOPT/KEEP row. Strongest:
                   the decision is made; the lead is a facet of an adopted artifact.
       COLLAPSED — a lead sharing a slug with other rows, none of them settled.
       FACETED   — every row in the group links its own subpath, so the catalog already
                   distinguishes them. Printed, never counted: `claude-plugins-official`
                   (8 rows, 8 subpaths) and `modelcontextprotocol/servers` (3 and 3) are
                   monorepos of independently-installable artifacts, which is a different
                   thing from one artifact counted N times.
     That link-shape split is the whole precision story — the four collapsed groups all
     have EVERY row pointing at one identical URL, so nothing in the catalog distinguishes
     them, while the faceted ones point at distinct paths.
     It does not see two cases #343 also lists, and cannot: a row whose pack is not itself
     catalogued (`presentation-creator` inside `getsentry/skills`), and a row whose link
     is the WHOLE product while the artifact is a component inside it (`prisma`, where the
     ★46.9K measures the ORM, not the MCP server). Both need a human, not a slug compare.
     Report-only, and deliberately not a fixer: whether to merge rows, add a "ships inside"
     column, or exclude facets from the queue is the decision #343 asks for. Offline.

  Y. INSTALL-RECORD MISMATCH (opt-in, --installed, REPORT-ONLY, LOCAL-ONLY) — KEEP is
     DEFINED as the validated-INSTALLED status, STACK.md is the install list, and detector
     J gates STACK derivation against the verdict data. Every one of those rests on an
     install fact, and until now nothing looked at one (#366). It cannot be a gate: install
     status is a property of one laptop, which is exactly why it drifts unobserved.
     Reads the records a machine actually keeps — `~/.agents/.skill-lock.json` (the
     `npx skills` v3 lockfile: a `source` slug, path and hash per skill),
     `~/.claude/plugins/installed_plugins.json`, and the `~/.claude/skills/` directory —
     and joins them to ADOPT/KEEP rows of `skill`/`plugin` Type, the only Types these
     records cover.
     Joined on SLUG, never on name, because name-matching IS the bug. #332's "already
     installed/active" was a marketplace CACHE directory read as an install; three STACK
     members turned out to be name COLLISIONS, a same-named artifact from a different
     source (`code-review` is ADOPT-as-anthropics/claude-plugins-official while what is
     symlinked in is `mattpocock/skills`'s `skills/engineering/code-review`, a different
     tool with a different design). That is #343's root — identity by name rather than by
     slug — one layer out, on a filesystem where 72 skills from 16 sources are flattened
     into one directory.
       COLLISION    — the name resolves, to something from another repo. Strongest.
       NO-RECORD    — no record and no directory answers to the row at all.
       UNCATALOGUED — an installed source with no catalog row (found from the install
                      side; a scan only ever looks at what exists, never at what runs here).
     NO-RECORD is deliberately NOT called "not installed": `claude install-skill` and npm
     globals leave no entry in either record, so absence is absence OF A RECORD. The
     directory fallback is what makes it worth printing anyway. Missing record files report
     0 RECORDS, never 0 findings — V's rule, same reason. Never in `make check`: CI has no
     lockfile, and a build that fails for a reason no code change caused is worse than
     unobserved drift.

  Z. UNREAD LICENSE DECLARATION (opt-in, --license-declared, REPORT-ONLY) — GitHub's
     licensee detector reads a root LICENSE file and nothing else, so `license_spdx:
     NONE` means "no LICENSE file", not "no license". triage.py's P4 mechanical-skip
     band disposes vendored leads on that value, and 8 of 28 NONE records turned out to
     declare a license anyway — in a README `## License` section, in package.json, or in
     both (#372). Reads the `license_declared` field refresh-metadata.py writes and
     reports it against the disposition each row already carries.
       GROUNDED — the row is SKIP and its `## Verdict` rests on the license. The
                  disposition is false: `andrej-karpathy-skills` and `web-access` were
                  both SKIPped "text carrying no license grant cannot be copied in"
                  against a README reading `## License` / `MIT`. Strongest.
       CONFLICT — the README and the manifest name different licenses. The standing
                  "the LICENSE file governs" tiebreak (#26) has nothing to govern with
                  when there is no LICENSE file, so a human picks.
       RECORDED — declared elsewhere, but no verdict rests on it. The record is still
                  wrong and the next bulk pass reads it.
     The declaration is QUOTED, per V's rule: a README line naming MIT without the
     license text or a copyright holder is a thinner record than a LICENSE file, and
     whether that clears the bar is a human's call. This detector never says a tool is
     adoptable — only that the ground under a mechanical SKIP is not an absence.
     A verdict that has ALREADY withdrawn its license ground is bucketed apart and not
     counted, because an honest retraction quotes the claim it retracts and would
     otherwise flag forever — W's "argues it clears the bar" shape. Widen
     LICENSE_WITHDRAWN if it misses an honest retraction; never narrow LICENSE_GROUND
     to compensate, which would hide live findings to clear stale ones.
     Report-only: the remedy is a re-read of a human's verdict, not a build failure.
     Offline — it compares two files already in the tree.

Usage:
  python3 audit-evals.py              # A + B + D + G + J + K + O + Q (all offline but A)
  python3 audit-evals.py --offline    # B + D + G + J + K + O + Q only (no network)
  python3 audit-evals.py --installs   # install resolver only
  python3 audit-evals.py --fabrication # fabrication classifier only
  python3 audit-evals.py --verdicts   # verdict-sync only (offline)
  python3 audit-evals.py --comparison # COMPARISON.md vs CATALOG.md consistency (offline)
  python3 audit-evals.py --drift      # STACK.md vs verdicts + exclusion ledger (offline)
  python3 audit-evals.py --verdict-evidence  # ADOPT/KEEP must be run-backed or disclaimered (offline)
  python3 audit-evals.py --rows       # malformed CATALOG/COMPARISON table rows (offline)
  python3 audit-evals.py --bulk-triage  # bulk-marked evals may only SKIP (offline)
  python3 audit-evals.py --scope      # P0 leads whose eval concedes it is out of scope (offline)
  python3 audit-evals.py --identity   # catalog rows that are facets of one artifact (offline)
  python3 audit-evals.py --installed  # ADOPT/KEEP rows vs this machine's install records (local)
  python3 audit-evals.py --license-declared  # 'NONE' licenses declared outside a LICENSE file (offline)
  python3 audit-evals.py --links      # link-rot sweep only (slow, ~450 requests)
  python3 audit-evals.py --archived   # archived-repo report (slow, ~450 gh-api calls)
  python3 audit-evals.py --skills     # skill-evidence backlog report (offline)
  python3 audit-evals.py --overlaps   # dangling overlap-reference report (offline)
  python3 audit-evals.py --clusters   # overlap clusters still awaiting a pick (offline)
  python3 audit-evals.py --savings-claims  # unverified token-savings headlines (offline)
  python3 audit-evals.py --evidence   # declared Evidence-field distribution (offline)
  python3 audit-evals.py --staleness  # flag evals past their last-verified threshold (offline)
  python3 audit-evals.py --metadata-staleness  # age the repo-metadata.json cache (offline)
  python3 audit-evals.py --lead-headlines  # discovery-log leads claiming a verdict (offline)
  python3 audit-evals.py --selftest   # unit-test the evidence classifier (offline)

Exit code is non-zero if any gating detector finds a problem — a BROKEN install
(A), a FABRICATION candidate (B), a VERDICT mismatch (D), COMPARISON drift (G),
STACK-derivation drift (J), a WEAK-backed ADOPT/KEEP verdict (K), a MALFORMED
table row (O), or link rot (C, when --links is run) — so it can gate CI or a
pre-commit hook. E (skill evidence), F (dangling overlaps), and I (evidence field)
are report-only and never affect the exit code; --selftest exits non-zero on a
failing assertion, so it can gate alone.
"""
import collections
import contextlib
import datetime
import functools
import glob
import importlib.util
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

import catalog_lib

ROOT = os.path.dirname(os.path.abspath(__file__))


def _load_sibling(name, filename):
    """Load a hyphenated sibling script as a module, ON DEMAND.

    triage.py loads THIS module at its own import time, so anything here that needs
    triage.py must import it lazily or the two recurse. Called from a detector rather
    than at module scope, the nested copy never re-enters the detector, so it
    terminates at depth 2."""
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, filename))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
TIMEOUT = 15

# Staleness thresholds in days, by eval Type (#65). Fast-moving categories rot sooner
# than stable references — configured in ONE place. Tune here, not per detector call.
STALENESS_DAYS = {
    "harness": 120, "MCP server": 120, "framework": 120, "platform": 120,  # fast-moving
    "tool": 180, "skill": 180, "plugin": 180,                              # moderate
    "reference": 365,                                                       # stable
}
DEFAULT_STALENESS_DAYS = 180

# How old a repo-metadata.json record may get before detector R reports it (#260).
# The cache answers "is this repo archived / what license" for the triage bands, and
# a repo archived tomorrow keeps its stale record until someone refreshes. Archival
# and relicensing move on a scale of months, so this sits with the fast-moving eval
# categories rather than below them. A starting heuristic — tune here.
METADATA_STALE_DAYS = 120

# ---------------------------------------------------------------- helpers
def http_ok(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ai-tooling-audit"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.status == 200
    except Exception:  # noqa: BLE001 — any failure here means 'cannot verify', not 'broken'
        return False

def _run_ok(cmd):
    """True if `cmd` exits 0. A missing binary or a hung process means 'cannot verify',
    not 'broken' — detector A gates CI, so a false BROKEN is worse than an unchecked
    target. Without the timeout a single wedged `npm view` blocks the whole gate
    indefinitely; without the FileNotFoundError catch, a machine with no `npm` takes the
    run down with a traceback. A real 404 still exits non-zero and is still reported."""
    try:
        return subprocess.run(cmd, capture_output=True, text=True,
                              timeout=TIMEOUT, check=False).returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return True

def npm_exists(pkg):
    return _run_ok(["npm", "view", pkg, "version"])

def gh_repo_exists(slug):
    return _run_ok(["gh", "api", f"repos/{slug}", "--jq", ".full_name"])

def pypi_exists(pkg):   return http_ok(f"https://pypi.org/pypi/{pkg}/json")
def crates_exists(pkg): return http_ok(f"https://crates.io/api/v1/crates/{pkg}")

# ---------------------------------------------------------------- A. installs
PKG_CLEAN = lambda s: re.sub(r"[<>=].*|\[.*?\]|['\"]|@latest$", "", s).strip()

# A package token that is really a placeholder / prose fragment, not installable.
PLACEHOLDER = re.compile(r"^\.+$|\.\.\.|[<>{}|&]|^-|,$|"
                         r"^(install|installer|command|version|CLI|skills|name|pkg|package|foo|bar)$", re.IGNORECASE)
# If a backtick command is discussed as the WRONG/non-existent option ("not `npx x`",
# "listed as `npx x` (doesn't exist)", "earlier draft showed `x`, which does not exist"),
# it's a correction note, not an install to resolve. Markers can sit on either side.
NEGATION = re.compile(r"\b(not|non-?existent|does ?n.?t exist|do(es)? not exist|no such|wrong|"
                      r"instead of|isn.?t|rather than|earlier draft|was wrong|404|nonexistent)\b", re.IGNORECASE)

def extract_installs(text):
    """Yield (kind, package) from install-like commands in markdown."""
    for m in re.finditer(r"`([^`]*)`", text):
        cmd = m.group(1).strip()
        # skip commands framed as the WRONG/non-existent option (correction notes), either side
        window = text[max(0, m.start() - 70):m.end() + 60]
        if NEGATION.search(window):
            continue
        for pat, kind in [
            (r"^pip(?:x| install| ) *install +'?([A-Za-z0-9._-]+)", "pypi"),
            (r"^cargo install +([A-Za-z0-9._-]+)", "crates"),
            (r"^npm install +(?:-[gD] +)?(@?[A-Za-z0-9._/-]+)", "npm"),
            (r"^npx +(?:-y +)?(@?[A-Za-z0-9._/-]+)", "npm"),
            (r"claude install-(?:plugin|skill) +([A-Za-z0-9._-]+/[A-Za-z0-9._-]+)", "gh"),
        ]:
            mm = re.match(pat, cmd)
            if mm:
                pkg = PKG_CLEAN(mm.group(1))
                if pkg and not PLACEHOLDER.search(pkg):
                    yield kind, pkg

def audit_installs(ctx):
    """Detector A: every install command must point at a real artifact. Resolution runs
    concurrently (86 unique targets, ~22s serial) — no two lookups depend on each other,
    so this mirrors audit_links' ThreadPoolExecutor. Mentions are collected first and
    filtered afterwards, which keeps the reported order and the per-occurrence shape
    exactly as they were: lookups DEDUPE, findings do NOT, so a broken package cited in
    three evals is still three findings."""
    import concurrent.futures
    files = ["STACK.md", "CATALOG.md", *sorted(glob.glob("evaluations/*.md", root_dir=ctx.root))]
    checkers = {"pypi": pypi_exists, "crates": crates_exists, "npm": npm_exists, "gh": gh_repo_exists}
    mentions = []  # (rel, kind, pkg) in file order — this IS the reported order
    for rel in files:
        if not os.path.exists(ctx.path(rel)): continue
        for kind, pkg in extract_installs(ctx.read(rel)):
            mentions.append((rel, kind, pkg))
    targets = sorted({(kind, pkg) for _rel, kind, pkg in mentions})
    # max_workers matches audit_links. Do NOT raise it: PyPI and the npm registry
    # rate-limit, and a 429 would surface as a false BROKEN.
    with concurrent.futures.ThreadPoolExecutor(max_workers=24) as ex:
        seen = dict(zip(targets, ex.map(lambda t: checkers[t[0]](t[1]), targets), strict=True))
    return [(rel, kind, pkg) for rel, kind, pkg in mentions if not seen[(kind, pkg)]]

# ---------------------------------------------------------------- B. fabrication
# Disclaimers / review verbs that mark an eval as an HONEST not-run review.
HONEST = re.compile(r"not installed|not run|did not|do not|source-grounded|architecture review|"
                    r"readme review|readme[- ]based|repo[/ ].*review|review[ -]based|inspection — not|"
                    r"not exercised|not hands-on|review only|mechanism review|scope review|review — not|"
                    r"not connected|not deployed|not reproduced|not a hands-on|source review|"
                    r"source-and-docs|architecture[- ]level|surface[- ]area review|"
                    r"\bread (the|every|all|\d|through|\d+)|\bfetched\b|\binspected\b|\bexamined\b|"
                    r"\benumerated\b|\bcounted\b|\bdiffed\b|queried the (github|rest) api|github[- ]api|"
                    r"as (installed|checked out) on this machine|mentally|applied (to|against)|"
                    r"could not install|attempted to apply", re.IGNORECASE)
# Specific run claims a fabricator invents (used only when no honest/verified marker is present).
RUN_CLAIM = re.compile(r"\b(ran it|we ran|i ran|ran the|ran against|added the .* server|"
                       r"used it (on|to|across)|deployed |generated |executed |"
                       r"launched |wrapped the|let it index|pointed it|fed it)\b", re.IGNORECASE)
# Markers of a genuine, trustable hands-on run.
VERIFIED = re.compile(r"\*\*hands-on\*\*|verified hands-on|verified (live|:)|re-verified|re-ran|"
                      r"ran it \*\*live\*\*|ran it (live|for real)|ran the .*\blive\b|live from inside|"
                      r"installed (it|the real|via|globally|as a skill|as a claude)|"
                      r"installed \(|pip[- ]?install.*\bran\b|exercised the|one real script execution|"
                      r"ran `|loaded all tool schemas", re.IGNORECASE)

def how_section(text):
    m = re.search(r"#+\s*How we tested.*?(?=\n#+\s|\Z)", text, re.DOTALL | re.IGNORECASE)
    return m.group(0) if m else ""

def audit_fabrication(ctx):
    flagged = []
    for ev in ctx.evals:
        if not ev.how:
            continue
        if ev.evidence.is_fabrication_candidate:
            flagged.append(ev.name)
    return flagged

# ---------------------------------------------------------------- C. link rot
def check_repo(slug):
    """Return 'ok', 'dead', 'moved:<new>', or 'unknown:<reason>' for a github
    owner/repo slug.

    'unknown' exists because this used to fold every non-404 into 'ok' (#319).
    GitHub answers this detector's ~600-request unauthenticated burst with HTTP
    429, so EVERY link — including live ones like torvalds/linux — came back
    'ok' and the sweep printed a clean bill of health having verified nothing.
    "Could not check" and "checked and fine" must not be the same value: silence
    is not success."""
    url = f"https://github.com/{slug}"
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "ai-tooling-audit"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            final = r.geturl().replace("https://github.com/", "").rstrip("/")
            if final.lower() != slug.lower():
                return f"moved:{final}"
            return "ok"
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return "dead"          # the one status that genuinely means "gone"
        return f"unknown:HTTP {e.code}"   # 429 rate limit, 5xx, auth walls — not a verdict
    except Exception as e:  # noqa: BLE001 — every non-404 outcome is inconclusive by design
        return f"unknown:{type(e).__name__}"  # timeout / DNS / TLS — also not a verdict

def audit_links(ctx):
    """(problems, unknowns, total) — problems are dead/moved links, unknowns are
    links this run could not verify. Callers MUST NOT report success while
    unknowns is non-empty; an inconclusive sweep is not a passing one."""
    import concurrent.futures
    slugs = catalog_lib.github_repos(ctx.catalog)
    problems, unknowns = [], []
    with concurrent.futures.ThreadPoolExecutor(max_workers=24) as ex:
        for slug, res in zip(slugs, ex.map(check_repo, slugs), strict=True):
            if res.startswith("unknown:"):
                unknowns.append((slug, res[len("unknown:"):]))
            elif res != "ok":
                problems.append((slug, res))
    return problems, unknowns, len(slugs)

# ---------------------------------------------------------------- L. staleness sweep
def audit_staleness(ctx, today=None):
    """Detector L (#65, REPORT-ONLY): flag evals whose **Last verified:** date is older
    than its category threshold (STALENESS_DAYS, keyed by Type) — fast-moving harnesses/
    MCP servers rot sooner than stable references. `today` is injectable for tests.
    Returns (stale, undated) where stale is a list of (name, type, date, age_days,
    threshold) and undated is the count of evals carrying no last-verified date."""
    today = today or datetime.date.today()
    stale, undated = [], 0
    for ev in ctx.evals:
        d = ev.last_verified
        if d is None:
            undated += 1
            continue
        threshold = STALENESS_DAYS.get(ev.type, DEFAULT_STALENESS_DAYS)
        age = (today - d).days
        if age > threshold:
            stale.append((ev.name, ev.type, d.isoformat(), age, threshold))
    return stale, undated

# ---------------------------------------------------------------- R. metadata staleness
# repo-metadata.json is a COMMITTED SNAPSHOT of GitHub facts (license, archived, stars)
# that the triage bands rest on. It rots in silence and in one direction: a repo archived
# tomorrow keeps its `archived: false` record, so it never reaches the P1 successor-check
# band and nobody is told. Detector L covers evals rotting; nothing covered the cache.
#
# REPORT-ONLY on purpose, and this one cannot become a gate the way F/N might. Gating it
# would fail `make check` for a reason no code change caused — the cache ages on the
# calendar — and the only fix is `refresh-metadata.py`, which needs the network that the
# offline-gate invariant forbids CI from depending on.
#
# Age comes from a per-record `fetched_at` stamp that refresh-metadata.py writes. Records
# predating that stamp report as UNDATED rather than being backfilled: a floor date would
# assert a fetch that never happened, the same reason `**Last triaged:**` is never
# backfilled while `**Last verified:**` (which has an honest git-derived floor) is.
def audit_metadata_staleness(ctx, today=None):
    """Detector R (#260, REPORT-ONLY): age the repo-metadata.json cache. Returns
    (total, undated, stale, oldest) — total records; count with no `fetched_at`;
    a list of (slug, date, age) past METADATA_STALE_DAYS, oldest first; and the
    oldest (slug, date, age) overall, or None when nothing carries a stamp.
    A missing or unreadable cache is (0, 0, [], None), never an exception: a fresh
    clone has no cache and `make check` must still run (same tolerance triage.py's
    load_metadata() has)."""
    today = today or datetime.date.today()
    try:
        records = json.loads(ctx.read("repo-metadata.json"))
    except (OSError, ValueError):
        return 0, 0, [], None
    if not isinstance(records, dict):
        return 0, 0, [], None
    dated, undated = [], 0
    for slug, meta in records.items():
        stamp = meta.get("fetched_at") if isinstance(meta, dict) else None
        try:
            d = datetime.date.fromisoformat(stamp)
        except (TypeError, ValueError):
            undated += 1  # never stamped, or unparseable — both mean "age unknown"
            continue
        dated.append((slug, d, (today - d).days))
    dated.sort(key=lambda r: -r[2])
    stale = [(s, d.isoformat(), age) for s, d, age in dated if age > METADATA_STALE_DAYS]
    oldest = (dated[0][0], dated[0][1].isoformat(), dated[0][2]) if dated else None
    return len(records), undated, stale, oldest

# ---------------------------------------------------------------- H. archived repos
# A catalogued repo that GitHub has flagged `archived` is no longer maintained — the
# entry shouldn't read as a live recommendation without saying so. Link rot (C) can't
# catch this: an archived repo's link still resolves. This is how 4 archived entries
# (incl. gpt-engineer ★55K and a same-named superseded chrome-devtools fork's cousin)
# were found. Opt-in (uses authenticated `gh api`, so not rate-limited), report-only:
# keep notable/historical tools but expect the entry to carry a ⚠️ archived note.
def check_archived(slug):
    r = subprocess.run(["gh", "api", f"repos/{slug}", "--jq", "[.archived, .pushed_at[0:7]]"],
                       capture_output=True, text=True, check=False)
    if r.returncode != 0:
        return None
    try:
        arch, pushed = json.loads(r.stdout)
        return (bool(arch), pushed)
    except Exception:  # noqa: BLE001 — a malformed `gh` payload means 'unknown', not a crash
        return None

def audit_archived(ctx):
    import concurrent.futures
    text = ctx.catalog
    slugs = catalog_lib.github_repos(text)
    archived = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as ex:
        for slug, res in zip(slugs, ex.map(check_archived, slugs), strict=True):
            if res and res[0]:
                # already disclosed in the entry? (a ⚠️ near the link)
                flagged = bool(re.search(re.escape(slug) + r".{0,400}?(?:archived|⚠️)", text, re.DOTALL | re.IGNORECASE))
                archived.append((slug, res[1], flagged))
    return archived, len(slugs)

# ---------------------------------------------------------------- D. verdict sync
# discovery-log (ADR 0001 / #69): a COMPARISON status for catalogued tools that were
# never exercised (Evidence REVIEW/SOURCE-ONLY) — leads, not verdicts. They are
# excluded from verdict-sync (D) and verdict-evidence (K): an eval's tentative
# CONDITIONAL read is the lead's notes, not a promoted verdict to enforce.
VERDICTS = catalog_lib.VERDICTS  # vocabulary defined once, in catalog_lib (#193)

def audit_verdicts(ctx):
    """Flag evals whose ## Verdict disagrees with their COMPARISON.md row.
    Tolerates: KEEP (installed/validated status) vs ADOPT, and dual verdicts
    ("ADOPT for X — CONDITIONAL otherwise") where COMPARISON matches either."""
    comp = ctx.comparison_verdict_map
    compatible = {frozenset(("KEEP", "ADOPT"))}  # installed-tool status ~ adopt
    flagged = []
    for ev in ctx.evals:
        if not ev.verdict:
            continue
        ev_set = ev.verdict_set  # every verdict word — handles dual verdicts
        cv = next((comp[c] for c in ev.name_aliases if c in comp), None)
        if cv is None:
            continue  # name didn't map — not a verdict-sync problem
        if cv == "discovery-log":
            continue  # lead, not a verdict — the eval's tentative read isn't synced
        if cv in ev_set:
            continue  # matches (incl. dual verdict)
        if any(frozenset((cv, x)) in compatible for x in ev_set):
            continue  # KEEP vs ADOPT etc.
        flagged.append((ev.name, ev.verdict, cv))
    return flagged

# ---------------------------------------------------------------- J. stack-derivation drift
# STACK.md must be *derivable* from the verdict data (COMPARISON.md) plus the
# exclusion ledger (STACK-LEDGER.md, #64): every ADOPT/KEEP tool is either in STACK
# or has a logged exclusion reason, and nothing in STACK contradicts its verdict.
# This kills the hand-maintained drift prior audits kept finding (abtop/codeburn,
# serena, documentation-writer). Gating, on by default. Consumes the #64 ledger.
_LEDGER_ROW = re.compile(
    r"^\|\s*([^|]+?)\s*\|\s*(ADOPT|KEEP)\s*\|[^|]*\|\s*(yes|conditional|no)\s*\|\s*([^|]*?)\s*\|\s*$", re.MULTILINE)

def _stack_member_keys(stack_text):
    """Tools recommended in STACK.md, keyed by BOTH link text and repo basename —
    so an entry installed under another name (GSD ← obra/superpowers) still matches."""
    keys = set()
    for text, url in re.findall(r"\|\s*\[([^\]]+)\]\((https://github\.com/[^)]+)\)", stack_text):
        keys.update(catalog_lib.alias_keys(text, url))
    return keys

def audit_stack_drift(ctx):
    """Detector J: cross-check STACK.md against COMPARISON.md verdicts + the ledger.
    Flags: an ADOPT/KEEP tool absent from both STACK and the ledger; a ledger row whose
    verdict disagrees with COMPARISON; an excluded row with no reason; a ledger row
    marked in-STACK that isn't actually in STACK.md."""
    problems = []
    comp = ctx.comparison_verdict_map
    stack = _stack_member_keys(ctx.stack)
    ledger_keys = set()
    for name, verdict, in_stack, reason in _LEDGER_ROW.findall(ctx.ledger):
        ids = catalog_lib.identity_keys(name)
        ledger_keys.update(ids)
        if in_stack == "no" and not reason.strip():
            problems.append(f"ledger '{name}' is excluded (no) but records no reason")
        cv = next((comp[k] for k in ids if k in comp), None)
        if cv and cv != verdict and frozenset((cv, verdict)) != frozenset(("KEEP", "ADOPT")):
            problems.append(f"ledger '{name}' verdict {verdict} != COMPARISON {cv}")
        # STACK membership legitimately fans out to basenames (GSD ← superpowers).
        if in_stack in ("yes", "conditional") and \
                not any(k in stack for k in catalog_lib.alias_keys(name)):
            problems.append(f"ledger '{name}' marked '{in_stack}' but not found in STACK.md")
    for r in ctx.comparison_rows:
        if r.verdict in ("ADOPT", "KEEP") and \
                not any(k in ledger_keys for k in catalog_lib.identity_keys(r.tool)):
            problems.append(f"{r.verdict} tool '{r.tool}' in COMPARISON is neither in STACK nor the exclusion ledger (#64)")
    return problems

# ---------------------------------------------------------------- O. row shape (gating)
# A malformed table row used to be silently skipped: the parse sites guarded with
# ad-hoc cell-count thresholds and continued past anything unrecognized, so
# reconcile-counts and backfill-evidence simply rewrote around a bad row and the
# counts quietly excluded it. Validation now happens in one place (catalog_lib)
# and a bad row is a gating finding — it corrupts the counts the suite already
# gates on (G), so it must not pass. (#198)
def audit_row_shapes(ctx):
    problems = []
    for fname, text, validate in (("CATALOG.md", ctx.catalog, catalog_lib.validate_catalog_rows),
                                  ("COMPARISON.md", ctx.comparison, catalog_lib.validate_comparison_rows)):
        problems.extend(f"{fname}:{ln} {msg}" for ln, msg in validate(text))
    return problems

# ---------------------------------------------------------------- K. verdict evidence gate
def audit_verdict_evidence(ctx):
    """Detector K (#71): a strong verdict can't rest on a README skim. An ADOPT/KEEP
    eval must be run-backed (Evidence MEASURED or RUN) OR carry an explicit honesty
    disclaimer in its 'How we tested' section (Evidence.honest — the documented escape
    hatch). A REVIEW/SOURCE-ONLY ADOPT/KEEP with no disclaimer is flagged. Generalizes
    the skills-only report-only detector E into a catalog-wide gate. Offline, gating."""
    flagged = []
    for ev in ctx.evals:
        if ev.verdict not in ("ADOPT", "KEEP"):
            continue
        if ev.evidence_level in ("MEASURED", "RUN"):
            continue  # run-backed
        if ev.evidence.honest:
            continue  # explicit not-run disclaimer present (escape hatch)
        flagged.append((ev.name, ev.verdict, ev.evidence_level))
    return flagged

# ---------------------------------------------------------------- E. skill evidence (report-only)
# A skill's value is a behaviour change, so an ADOPT verdict on a *skill* should
# rest on a measured eval (triggering and/or with-skill-vs-baseline), not a README
# review. This is a backlog report, not a gate — it does not affect the exit code.
MEASURED = re.compile(r"tiktoken|with[- ]skill|baseline|measured a/b|\ba/b\b|trigger rate|"
                      r"assertion (passed|failed)|measured ~|token.*reduction.*measured|"
                      r"\*\*hands-on,? measured|run_eval", re.IGNORECASE)
# A strong, unambiguous measurement marker — strong enough to override a *weak*
# honest-review word (e.g. "inspected"/"read"/"examined") that would otherwise
# demote a genuinely measured eval. (Real case: a measured eval that wrote
# "inspected each SKILL.md" was wrongly held in the backlog because `\binspected\b`
# lives in HONEST. Sealing precedence here makes that a decision, not an accident.)
STRONG_MEASURED = re.compile(r"measured a/b|\ba/b\b|trigger rate|assertion (passed|failed)|"
                             r"\*\*hands-on,? measured|run_eval|tiktoken|measured ~", re.IGNORECASE)

# ---------------------------------------------------------------- I. declared evidence field
# Issue #62: the *declared* evidence-strength field — how hard we looked, recorded
# explicitly as data rather than inferred from prose. Distinct from the Evidence
# class below, which *infers* fabrication/measurement signals from the How section.
EVIDENCE_LEVELS = ("MEASURED", "RUN", "REVIEW", "SOURCE-ONLY")
EVIDENCE_FIELD = re.compile(
    r"\*\*Evidence:\*\*\s*`?(" + "|".join(EVIDENCE_LEVELS) + r")\b")

# ---------------------------------------------------------------- evidence seam
class Evidence:
    """Evidentiary status of an eval's 'How we tested' section.

    The HONEST / VERIFIED / RUN_CLAIM / MEASURED regexes are consumed only here,
    so the precedence between them is decided in ONE place instead of being
    recombined differently inside each detector. The interface is the test
    surface — see selftest()."""
    def __init__(self, how):
        self._how      = how
        self.honest    = bool(HONEST.search(how))
        self.verified  = bool(VERIFIED.search(how))
        self.run_claim = bool(RUN_CLAIM.search(how))
        self.measured  = bool(MEASURED.search(how))
        self._strong   = bool(STRONG_MEASURED.search(how))

    @property
    def level(self):
        """Derive the 4-value evidence strength (issue #67) from the same honesty /
        measurement signals detector B trusts, so the backfill is reproducible and
        grounded in the eval's own text rather than hand-guessed. Precedence: a
        not-run disclaimer (REVIEW) outranks run-ish verbs; an empty How section
        means nothing was tested here (SOURCE-ONLY)."""
        if self.is_measured:                 return "MEASURED"
        if self.honest:                      return "REVIEW"
        if self.run_claim or self.verified:  return "RUN"
        if not self._how.strip():            return "SOURCE-ONLY"
        return "REVIEW"

    @property
    def is_fabrication_candidate(self):
        # claims a specific run, with no honesty disclaimer and no genuine-run marker
        return self.run_claim and not (self.honest or self.verified)

    @property
    def is_measured(self):
        # measured evidence present, and either no honest-not-run disclaimer OR a
        # strong measurement marker that overrides a weak disclaimer word
        return self.measured and (self._strong or not self.honest)

# ---------------------------------------------------------------- eval model
class Evaluation:
    """One evaluation file, parsed once. The eval-file grammar — How section,
    Verdict, dual-verdict set, catalog row, name aliases — lives here so detectors
    consume a value instead of each re-deriving it from raw markdown. Build from a
    path with from_path(); the (name, text) constructor keeps it unit-testable
    without the tree (see selftest)."""
    def __init__(self, name, text):
        self.name = name
        self.text = text

    @classmethod
    def from_path(cls, path):
        return cls(os.path.basename(path)[:-3], Path(path).read_text(encoding="utf-8"))

    @property
    def how(self):
        return how_section(self.text)

    @property
    def evidence(self):
        return Evidence(self.how)

    @property
    def evidence_level(self):
        """The declared **Evidence:** field value (issue #62), or None if absent.
        One of EVIDENCE_LEVELS — records how hard we looked, separate from the verdict."""
        m = EVIDENCE_FIELD.search(self.text)
        return m.group(1) if m else None

    @property
    def derived_evidence(self):
        """Evidence level inferred from this eval's own signals (issue #67 backfill).
        backfill-evidence.py writes this into the declared field; afterwards the two agree."""
        return self.evidence.level

    @property
    def effective_evidence(self):
        """The declared **Evidence:** value if the eval carries one, else the
        derived level — what every evidence consumer should read (#201)."""
        return self.evidence_level or self.derived_evidence

    @property
    def catalog_rows(self):
        """The catalog-row copies embedded in this eval, via the shared parser (#196)."""
        return catalog_lib.parse_catalog_rows(self.text)

    @property
    def is_skill(self):
        return any(r.url and r.type == "skill" for r in self.catalog_rows)

    @property
    def type(self):
        """The Type cell from the eval's catalog row (tool/skill/MCP server/…), or None."""
        rows = self.catalog_rows
        return rows[0].type if rows else None

    @property
    def last_verified(self):
        """The declared **Last verified:** date (issue #65) as a date, or None if absent/bad."""
        m = re.search(r"\*\*Last verified:\*\*\s*(\d{4}-\d{2}-\d{2})", self.text)
        if not m:
            return None
        try:
            return datetime.date.fromisoformat(m.group(1))
        except ValueError:
            return None

    # The `**Repo:**` header link. Detector U compares it to the CATALOG row's link:
    # when a repo is renamed the catalog row gets repointed and this header does not,
    # so the eval keeps asserting a pre-rename slug forever (#336).
    _REPO_HEADER = re.compile(r"^\*\*Repo:\*\*.*$", re.MULTILINE)
    _MD_LINK = re.compile(r"\[[^\]]*\]\(([^)]*)\)")

    @property
    def repo_link(self):
        """The FIRST URL in this eval's `**Repo:**` header, or None (some evals head
        with `**Site:**` for a commercial platform)."""
        links = self.repo_links
        return links[0] if links else None

    @property
    def repo_links(self):
        """EVERY URL on the `**Repo:**` line. A header that documents a rename names
        both repos — `[old](…) — **now redirects to** [new](…)` — and that form is
        richer than the catalog's single link, not drift. Detector U accepts the header
        when the catalog's URL appears anywhere on the line."""
        m = self._REPO_HEADER.search(self.text)
        return self._MD_LINK.findall(m.group(0)) if m else []

    # The headline token, drawn from the ONE vocabulary in catalog_lib (#324). An eval
    # whose row is a `discovery-log` lead may headline `discovery-log` and say what it
    # is — a tentative read — instead of borrowing CONDITIONAL, a word ADR-0005 reserves
    # for tools we actually exercised. Longest-first alternation so a token that is a
    # prefix of another can never win the shorter match.
    _VERDICT_HEAD = re.compile(
        r"##\s*Verdict\s*\n+\s*\*\*(" +
        "|".join(re.escape(v) for v in sorted(catalog_lib.VERDICTS, key=len, reverse=True)) + ")")

    @property
    def verdict(self):
        m = self._VERDICT_HEAD.search(self.text)
        return m.group(1) if m else None

    @property
    def verdict_set(self):
        # every verdict word in the Verdict section (handles dual verdicts)
        if not self.verdict:
            return set()
        vsec = re.search(r"##\s*Verdict.*?(?=\n##\s|\Z)", self.text, re.DOTALL)
        if vsec:
            return {w for w in VERDICTS if re.search(rf"\b{w}\b", vsec.group(0))}
        return {self.verdict}

    @property
    def name_aliases(self):
        # normalized names this eval might be keyed by in COMPARISON.md
        cands = {catalog_lib.name_key(self.name)}
        h = re.search(r"^#\s*Evaluation:\s*(.+)$", self.text, re.MULTILINE)
        if h: cands.add(catalog_lib.name_key(h.group(1)))
        ce = next((r for r in self.catalog_rows
                   if r.url and r.url.startswith("https://github")), None)
        if ce: cands.add(catalog_lib.name_key(ce.name))
        return cands

# ---------------------------------------------------------------- detector context (#199)
class DetectorContext:
    """The detectors' input seam: everything a detector consumes, loaded once
    from one root directory. main() builds one from ROOT; tests build one from
    a fixture directory — the context replaces the ROOT monkeypatch as the test
    surface, so a detector's real inputs are visible in its signature.
    Properties are read lazily and cached — each cached input is read once per
    run, and detectors D, J, and M literally share one comparison_verdict_map
    (#197). (Detector A additionally walks raw file text via ctx.read: it scans
    every evaluations/*.md including the template ctx.evals skips.)"""
    def __init__(self, root):
        self.root = root

    def path(self, rel):
        return os.path.join(self.root, rel)

    def read(self, rel):
        return Path(self.path(rel)).read_text(encoding="utf-8")

    @functools.cached_property
    def catalog(self):
        return self.read("CATALOG.md")

    @functools.cached_property
    def comparison(self):
        return self.read("COMPARISON.md")

    @functools.cached_property
    def stack(self):
        return self.read("STACK.md")

    @functools.cached_property
    def workflow(self):
        return self.read("WORKFLOW.md")

    @functools.cached_property
    def ledger(self):
        return self.read("STACK-LEDGER.md")

    @functools.cached_property
    def evals(self):
        """Every Evaluation under evaluations/, skipping the template."""
        return [Evaluation.from_path(p)
                for p in sorted(glob.glob(os.path.join(self.root, "evaluations/*.md")))
                if os.path.basename(p) != "TEMPLATE.md"]

    @functools.cached_property
    def comparison_rows(self):
        """COMPARISON.md's verdict rows via the shared catalog_lib parser (#193)."""
        return catalog_lib.comparison_verdict_rows(self.comparison)

    @functools.cached_property
    def comparison_verdict_map(self):
        """The ONE COMPARISON name→verdict map detectors D, J, and M share (#197).
        Each row registers under catalog_lib.identity_keys — full and parenthetical-
        stripped name_key, never the slash-basename ('vercel-labs/agent-skills' must
        not shadow the real 'agent-skills' row). When a stripped alias collides
        across rows ('awesome-claude-skills (Composio)' vs '(travisvn)'), setdefault
        keeps the FIRST registration in file order for the ambiguous stripped key;
        each row's full key stays unambiguous, and consumers holding a qualified
        name always hit the full key first."""
        m = {}
        for r in self.comparison_rows:
            for k in catalog_lib.identity_keys(r.tool):
                m.setdefault(k, r.verdict)
        return m

    @functools.cached_property
    def evidence_alias_map(self):
        """alias name_key → effective Evidence level, first registration wins —
        the map catalog_lib.evidence_lookup consumes (#201). Built once here so
        detector N, backfill-evidence, and tier-stack all read the same map
        instead of each rebuilding it from the evals."""
        amap = {}
        for ev in self.evals:
            for a in ev.name_aliases:
                amap.setdefault(a, ev.effective_evidence)
        return amap

def audit_evidence_field(ctx):
    """REPORT-ONLY: tally the declared **Evidence:** field across evals (issue #62),
    catalog-wide and within the ADOPT/KEEP set (issue #67 — "what % of ADOPT is
    MEASURED"). Returns (counts, missing, strong) where counts/strong are level->int
    over all evals / over ADOPT+KEEP evals, and missing lists evals with no field.
    Records how hard we looked, separate from the verdict; gating weak backing is #71."""
    counts = dict.fromkeys(EVIDENCE_LEVELS, 0)
    strong = dict.fromkeys(EVIDENCE_LEVELS, 0)  # restricted to ADOPT/KEEP-verdict evals
    missing = []
    for ev in ctx.evals:
        lvl = ev.evidence_level
        if lvl:
            counts[lvl] += 1
            if ev.verdict in ("ADOPT", "KEEP"):  # primary verdict, not every word mentioned
                strong[lvl] += 1
        else:
            missing.append(ev.name)
    return counts, missing, strong

def audit_skill_evidence(ctx):
    measured, backlog = [], []
    for ev in ctx.evals:
        if not ev.is_skill:
            continue  # not a skill-type entry
        if ev.verdict != "ADOPT":
            continue  # only ADOPT skills carry the "needs measured backing" bar
        # genuinely measured = has measurement evidence AND is not a disclosed not-run
        # review (which may merely quote the author's "with-skill" numbers).
        (measured if ev.evidence.is_measured else backlog).append(ev.name)
    return measured, backlog

# ---------------------------------------------------------------- S. skill test-design (report-only)
# TEMPLATE.md's "Test design — skills" section requires every skill/plugin-Type eval to
# record BOTH skill dimensions (issue #38): Triggering (does the description fire on the
# right prompts?) and an Output A/B (with-skill vs baseline). This report surfaces
# skill/plugin evals that record NEITHER — the structural gap the required section
# closes. Conservative by design (same lenient-vocab spirit as detector B's HONEST
# regex): an eval counts as compliant if it names a triggering test OR an A/B anywhere,
# so an honest measured eval is never false-flagged. Widen the vocab if it does; never
# tighten it into a gate here — this mirrors --skills as a tracked metric, not a gate.
_SKILL_TRIGGER_RE = re.compile(r"trigger|run_eval|should[- ]?fire", re.IGNORECASE)
_SKILL_AB_RE = re.compile(r"\bA/B\b|with[- ]skill|without[- ]skill|baseline|skill on vs", re.IGNORECASE)

def audit_skill_design(ctx):
    """Detector S (REPORT-ONLY): skill/plugin-Type evals that record NEITHER a triggering
    test nor an A/B, per TEMPLATE.md's required skills Test-design section (#38). Returns
    (compliant, missing) as lists of eval names. Never affects the exit code."""
    compliant, missing = [], []
    for ev in ctx.evals:
        if ev.type not in ("skill", "plugin"):
            continue  # only skill/plugin-Type evals carry the two-dimension bar
        has = bool(_SKILL_TRIGGER_RE.search(ev.text) or _SKILL_AB_RE.search(ev.text))
        (compliant if has else missing).append(ev.name)
    return compliant, missing

# ---------------------------------------------------------------- F. dangling overlaps (report-only)
# Each entry's "Overlaps with" cell names peer tools. A token naming a tool that
# ISN'T itself catalogued is either a deliberate external/conceptual peer (the
# format allows this — e.g. "aider-style (ext.)") or a real gap: a notable tool we
# forgot to add. This is exactly how aider, continue, and agenta were found. The
# more rows reference the same uncatalogued token, the likelier it is a real gap.
# Report-only — surfaces candidates for human review; does not affect exit code.
# _ovl_display is presentation + heuristics (word counts, report text), NOT a
# same-tool key — matching goes through catalog_lib.name_key (#197).
_ovl_display = lambda s: catalog_lib.strip_parenthetical(s).strip().lower()
_OVL_SKIP = ("complementary", "different", "approach", "same repo",
             "conceptual", "none", "—", "–")

def audit_overlaps(ctx):
    names, rows = set(), []
    for r in catalog_lib.parse_catalog_rows(ctx.catalog):
        names.update(catalog_lib.alias_keys(r.name))
        if r.url is not None:
            rows.append(r)  # unlinked entries ("| OMEGA | ...") name-match only
    from collections import Counter
    miss = Counter()
    for r in rows:
        if r.overlaps is None:
            continue
        for tok in r.overlaps.split(","):  # the "Overlaps with" cell
            t = _ovl_display(tok)
            tl = tok.lower()
            if (not t or "ext." in tl or "=" in tok or ";" in tok
                    or tok.count("(") != tok.count(")")  # mid-parenthetical fragment
                    or len(t) > 22 or len(t.split()) > 2
                    or any(x in tl for x in _OVL_SKIP)):
                continue  # external/conceptual peer or prose fragment, not a gap
            if not any(k in names for k in catalog_lib.alias_keys(tok)):
                miss[t] += 1
    return miss.most_common()


def overlap_pressure_map(ctx):
    """name_key(cited tool) -> set of DISTINCT catalog rows (by their name_key)
    that cite it in 'Overlaps with'. Shares audit_overlaps' tokenization and skip
    filters — the only difference is it counts EVERY cited token, not just the
    uncatalogued ones detector F reports — so next-evals.py can weigh a
    discovery-log candidate by how many peers point at it (#plan-005). A caller
    unions the sets across a candidate's alias_keys; self-citations are dropped."""
    cites = {}
    for r in catalog_lib.parse_catalog_rows(ctx.catalog):
        if r.overlaps is None:
            continue
        citer = catalog_lib.name_key(r.name)
        for tok in r.overlaps.split(","):
            t, tl = _ovl_display(tok), tok.lower()
            if (not t or "ext." in tl or "=" in tok or ";" in tok
                    or tok.count("(") != tok.count(")")
                    or len(t) > 22 or len(t.split()) > 2
                    or any(x in tl for x in _OVL_SKIP)):
                continue
            key = catalog_lib.name_key(catalog_lib.strip_parenthetical(tok))
            if key and key != citer:
                cites.setdefault(key, set()).add(citer)
    return cites

# ---------------------------------------------------------------- P. WORKFLOW↔STACK drift (report-only)
# README sends readers to WORKFLOW.md as "the full operating manual" and STACK.md is
# the install list; they must not give a newcomer two different answers to "what do I
# use for X". The invariant is ONE-directional: every STACK *pick* must appear
# somewhere in WORKFLOW.md (the manual must at least mention every pick). The reverse
# is NOT required — WORKFLOW legitimately lists non-STACK CONDITIONAL options.
# Matched by github owner/repo slug, NOT display name (names vary — "GSD" links to
# obra/superpowers), reusing catalog_lib.github_repos so the extraction can't drift.
# STACK picks are scoped to the install-command *table rows*, so the prose that names
# *excluded* tools (the "excluded (#37)" batch: brooks-lint, code-on-incus) and self/
# issue links aren't mistaken for picks. Slugs are lowercased (GitHub is case-
# insensitive: STACK links NVIDIA/SkillSpector but clones NVIDIA/skillspector).
# Report-only, not a gate — prints a count so it's "a number to shrink" (plan 003).
def audit_workflow_drift(ctx):
    """Detector P: STACK picks absent from WORKFLOW.md. Returns (slug, stack_line) for
    each STACK-pick github slug that appears nowhere in WORKFLOW.md, first STACK line."""
    wf = {s.lower() for s in catalog_lib.github_repos(ctx.workflow)}
    first_line = {}
    for i, line in enumerate(ctx.stack.splitlines(), 1):
        if not line.lstrip().startswith("|"):
            continue  # picks live in the install-command tables, not the prose
        for slug in catalog_lib.github_repos(line):
            first_line.setdefault(slug.lower(), i)
    return [(slug, ln) for slug, ln in sorted(first_line.items()) if slug not in wf]

# ---------------------------------------------------------------- M. clusters without a pick (report-only)
# ADR 0001 / #69: when several catalogued tools solve the same problem (an overlap
# cluster), the catalog should name ONE best-in-class ADOPT pick rather than hedge
# CONDITIONAL on all of them. This report surfaces overlap clusters (connected via
# the "Overlaps with" graph) where NO member is ADOPT/KEEP yet at least one is
# CONDITIONAL — i.e. clusters still awaiting a pick. Report-only; it makes the #69
# migration findable, it does not migrate anything.
def audit_clusters(ctx):
    # name_key -> set(overlap peer keys), restricted to catalogued names; disp
    # keeps the human-readable member name the report prints (#197).
    rows = [r for r in catalog_lib.parse_catalog_rows(ctx.catalog) if r.url is not None]
    cat_names, edges, disp, nverd = set(), {}, {}, {}
    verd = ctx.comparison_verdict_map
    for r in rows:
        nm = catalog_lib.name_key(r.name)
        cat_names.add(nm)
        disp.setdefault(nm, _ovl_display(r.name))
        nverd[nm] = next((verd[k] for k in catalog_lib.identity_keys(r.name) if k in verd), None)
    for r in rows:  # second pass: peer tokens resolve against the full name set
        nm = catalog_lib.name_key(r.name)
        peers = []
        if r.overlaps:
            for tok in r.overlaps.split(","):
                t = _ovl_display(tok)
                if t and "ext." not in tok.lower() and len(t.split()) <= 2:
                    p = next((k for k in catalog_lib.alias_keys(tok) if k in cat_names), None)
                    if p: peers.append(p)
        edges[nm] = peers
    # union-find over overlap edges (only between catalogued names)
    parent = {n: n for n in cat_names}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    def union(a, b):
        if a in parent and b in parent:
            parent[find(a)] = find(b)
    for nm, peers in edges.items():
        for p in peers:
            union(nm, p)
    from collections import defaultdict
    clusters = defaultdict(set)
    for n in cat_names:
        clusters[find(n)].add(n)
    flagged = []
    for members in clusters.values():
        if len(members) < 2:
            continue
        verds = {nverd.get(m) for m in members}
        has_pick = "ADOPT" in verds or "KEEP" in verds
        awaiting = "CONDITIONAL" in verds or "discovery-log" in verds
        if awaiting and not has_pick:
            flagged.append(sorted(disp[m] for m in members))
    return sorted(flagged, key=lambda c: (-len(c), c[0].lower()))

# ---------------------------------------------------------------- N. token-savings claims (report-only)
# Nearly every Optimize-cluster entry advertises a self-reported "% token savings"
# headline (60-95% fewer tokens, 96% reduction, 50x token reduction, ~98% fewer
# tokens) yet almost none are hands-on MEASURED in this repo — the loudest claims in
# the catalog rest on the weakest evidence. This report flags every CATALOG row whose
# one-liner makes a numeric token-savings claim but whose eval is not run-backed
# (Evidence MEASURED/RUN), so the unverified backlog is a number to watch shrink
# (mirrors --skills; gating is a later #71-style decision). An in-row "self-reported"/
# "unverified" disclaimer is the honest path — like detector B's HONEST vocab — and is
# bucketed apart from the silent claims. Report-only; does not affect exit code.
_SAVINGS_NUM = re.compile(r"~?\d+(?:\.\d+)?(?:\s*[-–]\s*\d+(?:\.\d+)?)?\s*%\+?|~?\d+(?:\.\d+)?\s*(?:×|x\b)")
_SAVINGS_NEAR = re.compile(r"token|context|prompt|saving|reduc|fewer|less|waste|compress|consumption|lower|smaller|\bcut", re.IGNORECASE)
_SAVINGS_CTX = re.compile(r"token|context|prompt", re.IGNORECASE)
_SAVINGS_DISCLAIMER = re.compile(r"self-?reported|unverified", re.IGNORECASE)

def _has_savings_claim(one_liner):
    """A numeric token-savings headline: a percentage or N× figure sitting next to
    reduction/token vocabulary, in a one-liner that is itself about tokens/context.
    Scopes to the Optimize cluster without computing cluster membership, and avoids
    false positives like '94% of languages' or '2M-token context' (figure, no verb)."""
    if not _SAVINGS_CTX.search(one_liner):
        return False
    for m in _SAVINGS_NUM.finditer(one_liner):
        lo, hi = max(0, m.start() - 28), m.end() + 28
        if _SAVINGS_NEAR.search(one_liner[lo:hi]):
            return True
    return False

def audit_savings_claims(ctx):
    """Return (name, evidence_level, disclosed) for every CATALOG row making a numeric
    token-savings claim that is NOT run-backed. Verified rows (MEASURED/RUN) drop out;
    rows with no eval surface as '(no eval)'. Sorted by name. Report-only."""
    levels = ctx.evidence_alias_map  # normalized catalog name -> effective evidence level
    flagged = []
    for r in catalog_lib.parse_catalog_rows(ctx.catalog):
        if r.url is None or r.one_liner is None or not _has_savings_claim(r.one_liner):
            continue
        # NOT catalog_lib.evidence_lookup: N distinguishes "(no eval)" (None) from an
        # eval-derived SOURCE-ONLY, which the lookup's SOURCE-ONLY default would erase.
        lvl = next((levels[k] for k in catalog_lib.alias_keys(r.name) if k in levels), None)
        if lvl in ("MEASURED", "RUN"):
            continue  # claim is run-backed — exactly what we want
        disclosed = any(_SAVINGS_DISCLAIMER.search(c) for c in r.cells)
        flagged.append((r.name, lvl or "(no eval)", disclosed))
    return sorted(flagged, key=lambda r: r[0].lower())

# ---------------------------------------------------------------- G. comparison consistency
# COMPARISON.md mirrors CATALOG.md: its per-stage Summary must be an honest funnel.
# Tools must sum to its own body rows and equal the CATALOG entry count; Validated
# must equal the real-verdict rows (discovery-log excluded, per ADR 0001) — not the
# raw catalogued count. Manual edits drift easily (a single tool addition touches both
# files) and nothing else cross-checks them, so a disagreement could ship silently.
# Gating, offline.
def _summary_cells(line):
    """Cells of a Summary table row, outer pipes dropped and bold markers stripped."""
    return [c.strip().replace("**", "") for c in line.strip().strip("|").split("|")]

# ---------------------------------------------------------------- Q. eliminate-only bulk triage
# An unattended bulk-triage pass (triage.py's bands) may REJECT a lead but never
# promote one: it writes SKIP, or leaves the lead at discovery-log. A false SKIP is
# cheap and reversible; a false ADOPT poisons STACK, and detector K's honesty-
# disclaimer escape hatch would happily let a README skim carry an ADOPT.
#
# Policy is worthless unattended unless it is mechanical. An eval touched by the bulk
# lane carries BULK_MARKER; this gate fails if such an eval claims anything stronger
# than SKIP. Gating, offline. A human who genuinely exercises the tool drops the
# marker (and says so in "How we tested it") before writing a stronger verdict.
BULK_MARKER = "<!-- triaged: bulk -->"
# SKIP is the disposal; `discovery-log` is the leave. The latter used to be expressible
# only as the ABSENCE of a headline, because a left lead borrowed CONDITIONAL and this
# gate would have failed the build for prose the lane never wrote. Since #324 a lead
# headlines `discovery-log`, so the leave outcome is a token the gate can recognize.
BULK_ALLOWED = frozenset({"SKIP", "discovery-log"})
# A `**Last triaged:**` stamp says *some* lane examined this lead — but not which, and Q
# can only police a lane it can identify. The bulk marker is that identification; a human
# pass writes HUMAN_MARKER instead, which exempts the eval (a human may reach any verdict,
# which is the whole difference between the lanes). A stamp carrying NEITHER is the hole
# #327 names: it looks exactly like a lane that behaved, and Q never sees it. The
# /triage-lead skill has written the bulk marker on both outcomes since #323; this makes
# that protocol mechanical instead of a promise.
TRIAGE_STAMP = "**Last triaged:**"
HUMAN_MARKER = "<!-- triaged: human -->"
UNATTRIBUTED = "unattributed"  # the second finding kind audit_bulk_triage returns

def audit_bulk_triage(ctx):
    """(eval name, verdict) for every bulk-marked eval whose verdict exceeds the
    eliminate-only authority. A marked eval with no verdict is fine — it stayed at
    discovery-log, which is the other permitted outcome.

    Keys on the HEADLINE verdict, not verdict_set: the latter collects every verdict
    word in the section, so a SKIP whose prose reads "not an ADOPT" would trip a
    set-based check. The headline is what COMPARISON.md and detector D consume."""
    flagged = []
    for ev in ctx.evals:
        if BULK_MARKER not in ev.text:
            # An unattributed stamp is unpoliceable, not innocent: Q cannot tell a lane
            # that left a lead from one that raised it (#327). Reported at the stamp, so
            # the fix is attribution rather than a verdict argument.
            if TRIAGE_STAMP in ev.text and HUMAN_MARKER not in ev.text:
                flagged.append((ev.name, UNATTRIBUTED))
            continue
        if ev.verdict and ev.verdict not in BULK_ALLOWED:
            flagged.append((ev.name, ev.verdict))
    return flagged

# ---------------------------------------------------------------- T. lead headline overreach
# A COMPARISON row reading `discovery-log` says the tool was never exercised — its eval
# is notes, not a recommendation. 324 such evals nonetheless opened `## Verdict` with
# **CONDITIONAL**, a word ADR-0005 grants only to a tool we ran or one carrying a real
# `adopt-if:` gate (#324). That is not cosmetic: the /triage-lead protocol escalates any
# lead whose headline reads CONDITIONAL, so the mislabel shielded 11 of 13 leads in one
# band and nearly made the pass a no-op. #324 relabelled them; this keeps them relabelled.
#
# Scoped to REVIEW/SOURCE-ONLY evidence deliberately. A run-backed eval that headlines
# CONDITIONAL has earned the word — there the *row* is what's stale, which is a verdict
# decision for a human, not a headline this detector can call wrong.
LEAD_ALLOWED_HEADLINES = frozenset({"discovery-log", "SKIP"})  # "it's a lead" / "we rejected it"

def audit_lead_headlines(ctx):
    """(eval name, headline verdict, evidence level) for every `discovery-log` row whose
    unexercised eval headlines a verdict word it is not entitled to. Report-only: the
    survivors are escalations awaiting a human verdict (#259), not build breakers."""
    comp = ctx.comparison_verdict_map
    flagged = []
    for ev in ctx.evals:
        if not ev.verdict or ev.verdict in LEAD_ALLOWED_HEADLINES:
            continue
        cv = next((comp[c] for c in ev.name_aliases if c in comp), None)
        if cv != "discovery-log":
            continue
        level = ev.effective_evidence
        if level in ("MEASURED", "RUN"):
            continue  # earned the word; the row is the stale half — a human call
        flagged.append((ev.name, ev.verdict, level))
    return flagged


# ---------------------------------------------------------------- U. catalog-entry mirror drift (report-only)
# TEMPLATE.md has every eval close with a `## Catalog entry` section holding that tool's
# CATALOG.md row. It is a mirror — a fact restated in two places with no generator and no
# test — so it drifts, and 62% of it had (#345). This is the same class root CLAUDE.md
# calls out for plugin/CLAUDE.md: *gate the shared facts, not the file*.
#
# Two kinds, reported apart because they are not equally dangerous:
#
#   LINK  — the eval points at a different repo than the catalog does (#336). When a repo
#           is renamed the daily discovery pass repoints the CATALOG row and nothing
#           repoints the eval, so the eval asserts a dead slug (and the stars/license it
#           was written against) indefinitely. `herdr` was SKIP-eligible on stale facts
#           for exactly this reason. This is the class worth gating first.
#   TEXT  — the one-liner / problem / overlaps cells disagree. Cosmetic-looking, but the
#           overlaps cell is what `triage.py` bands leads from, so a disagreement here
#           decides which band a lead lands in (`softaworks/agent-toolkit`, #344).
#
# Report-only, and deliberately NOT a bulk fixer: #345's sequencing note is that whichever
# direction is applied wholesale destroys real work in the other, because the eval side is
# sometimes the better text (`azure-skills`). This prints the number to shrink; a human
# decides per row which side is right.
CatalogMirrorFinding = collections.namedtuple("CatalogMirrorFinding", "eval_name tool kind detail")

def audit_catalog_mirror(ctx):
    """CatalogMirrorFindings for every eval whose embedded `## Catalog entry` row (or
    `**Repo:**` header) disagrees with CATALOG.md's row for the same tool. Offline —
    a string comparison between two files already in the tree, unlike detector C's
    ~450 HTTP requests, which is what makes it cheap enough to run every time."""
    # Two maps, because one is not enough. name_key collapses non-alphanumerics, so
    # `agent-skills` (addyosmani) and `agentskills` (the spec) key identically — and a
    # single setdefault map silently handed one eval the OTHER tool's row and reported a
    # LINK against it. Exact name wins; the collapsed key is a fallback, and a fallback
    # key reaching two different rows resolves to nothing rather than to a coin flip.
    exact, fuzzy, ambiguous = {}, {}, set()
    for r in catalog_lib.parse_catalog_rows(ctx.catalog):
        if r.url is None:
            continue
        exact.setdefault(r.name, r)
        for k in catalog_lib.identity_keys(r.name):
            if k in fuzzy and fuzzy[k].name != r.name:
                ambiguous.add(k)
            fuzzy.setdefault(k, r)

    def lookup(name):
        """(row, ambiguous_key) for a name — never a guess between two distinct tools."""
        if name in exact:
            return exact[name], None
        for k in catalog_lib.identity_keys(name):
            if k in ambiguous:
                return None, k
            if k in fuzzy:
                return fuzzy[k], None
        return None, None

    findings = []
    for ev in ctx.evals:
        rows = [r for r in ev.catalog_rows if r.url is not None]
        if not rows:
            continue  # no embedded row: nothing mirrored, nothing to drift
        # A pack eval embeds several rows (8090-software-factory carries the platform's);
        # every one of them mirrors some catalog row, so check each against its own.
        for row in rows:
            crow, ambig = lookup(row.name)
            if ambig:
                findings.append(CatalogMirrorFinding(
                    ev.name, row.name, "AMBIG",
                    f"two CATALOG.md rows collapse to the key '{ambig}' — cannot tell which is mirrored"))
                continue
            if crow is None:
                findings.append(CatalogMirrorFinding(
                    ev.name, row.name, "ORPHAN",
                    "embedded row names a tool with no CATALOG.md row"))
                continue
            if row.url != crow.url:
                findings.append(CatalogMirrorFinding(
                    ev.name, row.name, _link_kind(row.url, crow.url),
                    f"eval row {row.url} != catalog {crow.url}"))
            for field in ("type", "one_liner", "overlaps"):
                mine, theirs = getattr(row, field), getattr(crow, field)
                if mine != theirs:
                    findings.append(CatalogMirrorFinding(
                        ev.name, row.name, "TEXT", f"{field}: {_clip(mine)} != {_clip(theirs)}"))
        # The header link is checked against the FIRST embedded row's catalog match: that
        # row is the eval's own subject (pack evals lead with theirs), and an eval with no
        # `**Repo:**` header is not a finding — commercial platforms head with `**Site:**`.
        heads = ev.repo_links
        crow, _ = lookup(rows[0].name)
        if heads and crow and crow.url and crow.url not in heads:
            findings.append(CatalogMirrorFinding(
                ev.name, rows[0].name, _link_kind(heads[0], crow.url),
                f"**Repo:** header {heads[0]} != catalog {crow.url}"))
    return findings


def _link_kind(a, b):
    """LINK for a genuine repo disagreement, CASE when the two URLs differ only in
    capitalization. GitHub owner/repo names are case-insensitive and redirect, so a
    case-only diff cannot make an eval assert the wrong repo's facts — the failure
    #336 is about. Reported apart rather than dropped: it is still a tidy-up, and a
    silently-filtered finding reads as "clean" when it isn't."""
    return "CASE" if a.lower() == b.lower() else "LINK"


def _clip(s, n=58):
    s = (s or "").replace("\n", " ")
    return s if len(s) <= n else s[:n - 1] + "…"


# ---------------------------------------------------------------- V. maintenance signal (report-only)
# `archived == true` is triage.py's P1 successor-check band, and it only catches
# maintainers who flipped GitHub's archive flag. daytonaio/daytona — ★72K, the catalog's
# canonical answer to "run untrusted AI-generated code" — announced discontinuation in
# its README in June 2026 and moved development to a private codebase, and sat in P3
# backlog as ordinary un-examined work for two months because `archived` stayed false
# (#351). P1 reading "0 leads" presents as "nothing archived to check"; that is true and
# also says nothing about how many catalogued projects are dead.
#
# This reports the two per-record signals `refresh-metadata.py --maintenance` writes:
# `discontinued` (the README banner phrase) and `license_lost` (a real license that
# became NONE/404 since the last snapshot — daytona went AGPL-3.0 → 404 while
# vercel-labs/skills went NONE → MIT, and detector R can see neither, because it ages
# the snapshot as a whole and both records were well inside the threshold).
#
# Report-only, and the ordering is the point: a discontinued tool with an ADOPT/KEEP
# verdict is a live recommendation to install a dead project, which is worth more than a
# dead `discovery-log` lead nobody was going to reach anyway.
MaintenanceFinding = collections.namedtuple("MaintenanceFinding", "slug kind detail verdict tool")

def audit_maintenance(ctx):
    """MaintenanceFindings for every catalogued repo whose metadata records a
    discontinuation banner or a lost license, strongest verdict first. A cache with no
    maintenance fields yields nothing and says so via the count — the signal is opt-in
    on the refresher, so its absence means "not collected", never "nothing is dead"."""
    try:
        records = json.loads(ctx.read("repo-metadata.json"))
    except (OSError, ValueError):
        return [], 0, []
    if not isinstance(records, dict):
        return [], 0, []
    # slug -> catalog row name, so a finding names the tool a human recognizes
    by_slug = {}
    for r in catalog_lib.parse_catalog_rows(ctx.catalog):
        if r.url:
            for s in catalog_lib.github_repos(r.url):
                by_slug.setdefault(s.lower(), r.name)
    verd = ctx.comparison_verdict_map
    collected = sum(1 for m in records.values()
                    if isinstance(m, dict) and ("discontinued" in m or "license_lost" in m))
    findings, acked = [], []
    for slug, meta in sorted(records.items()):
        if not isinstance(meta, dict):
            continue
        tool = by_slug.get(slug, slug)
        v = next((verd[k] for k in catalog_lib.identity_keys(tool) if k in verd), "—")
        phrase = meta.get("discontinued")
        if phrase:
            f = MaintenanceFinding(slug, "DISCONTINUED", f'README: "{phrase}"', v, tool)
            (acked if _acked(meta, phrase) else findings).append(f)
        if meta.get("license_lost"):
            findings.append(MaintenanceFinding(slug, "LICENSE-LOST",
                                               f"now {meta.get('license_spdx')}", v, tool))
    rank = {"ADOPT": 0, "KEEP": 0, "CONDITIONAL": 1, "DEFER": 2, "discovery-log": 3, "SKIP": 4}
    for bucket in (findings, acked):
        bucket.sort(key=lambda f: (rank.get(f.verdict, 3), f.slug))
    return findings, collected, acked


def _acked(meta, phrase):
    """True when a human has recorded that THIS phrase is a false positive. The ack
    pins the exact phrase it was granted against, so a README that later gains a real
    repo-level banner reports again instead of hiding behind a stale acknowledgment.

    This exists because V's version-scoped class is not mechanically separable —
    giskard-oss says "no longer actively maintained" of Giskard **v2** while the repo
    ships v3 — and a permanently-stuck false positive turns "a number to shrink" into
    noise. Acked findings are still PRINTED, just not counted (no silent caps)."""
    ack = meta.get("discontinued_ack")
    return isinstance(ack, dict) and ack.get("phrase") == phrase


def audit_comparison(ctx):
    text = ctx.comparison
    body = catalog_lib.comparison_body_counts(text)          # shared with reconcile-counts.py
    breakdown = catalog_lib.comparison_verdict_breakdown(text)  # per-stage (validated, recommended)
    # Parse the Summary table into per-stage {tools, validated} plus the Total row.
    summary, total, in_summary = {}, None, False
    for l in text.splitlines():       # second pass: the Summary table only
        hm = re.match(r"^##\s+(.*)", l)
        if hm:
            in_summary = hm.group(1).strip().lower() == "summary"
            continue
        if not in_summary or not l.lstrip().startswith("|"):
            continue
        cells = _summary_cells(l)
        name = cells[0]
        if len(cells) < 3 or not cells[1].isdigit() or not cells[2].isdigit():
            continue  # header, separator, or a malformed row
        rec = {"tools": int(cells[1]), "validated": int(cells[2])}
        if name.lower() == "total":
            total = rec
        else:
            summary[name] = rec
    problems = []
    for s, rec in summary.items():
        if body.get(s, 0) != rec["tools"]:
            problems.append(f"section '{s}': summary Tools {rec['tools']}, body has {body.get(s, 0)}")
        exp_val = breakdown.get(s, (0, 0))[0]
        if rec["validated"] != exp_val:
            problems.append(f"section '{s}': summary Validated {rec['validated']}, real-verdict rows total {exp_val}")
    body_total = sum(body.values())
    val_total = sum(v for v, _ in breakdown.values())
    cat = catalog_lib.catalog_count(ctx.catalog)
    if total is not None:
        if total["tools"] != body_total:
            problems.append(f"Total Tools says {total['tools']}, body rows sum to {body_total}")
        if total["validated"] != val_total:
            problems.append(f"Total Validated says {total['validated']}, real-verdict rows sum to {val_total}")
        if total["tools"] != cat:
            problems.append(f"COMPARISON Total {total['tools']} != CATALOG.md {cat} entries")
    return problems

# ---------------------------------------------------------------- selftest
def selftest():
    """Lock in the evidence-classification precedence. Run: audit-evals.py --selftest"""
    cases = [
        # (label, how-section text, expect_fabrication, expect_measured)
        ("disclosed not-run review",
         "We did not install this; source review only.", False, False),
        ("verified hands-on run",
         "Ran it **live** via pip install; exercised the CLI.", False, False),
        ("bare run claim, no disclaimer = fabrication candidate",
         "We ran it on our repo and it generated the report.", True, False),
        ("measured A/B with no honest word = measured",
         "**Hands-on, measured** with-skill vs baseline A/B.", False, True),
        ("STRONG measured marker overrides a weak honest word (the bug we hit)",
         "**Hands-on, measured** — inspected each SKILL.md, ran a measured A/B.", False, True),
        ("weak measured token + honest disclaimer = NOT measured",
         "We did not run it; the author reports a with-skill number.", False, False),
    ]
    fails = []
    for label, how, exp_fab, exp_meas in cases:
        ev = Evidence(how)
        if ev.is_fabrication_candidate != exp_fab:
            fails.append(f"  FAIL [fabrication] {label}: got {ev.is_fabrication_candidate}, want {exp_fab}")
        if ev.is_measured != exp_meas:
            fails.append(f"  FAIL [measured] {label}: got {ev.is_measured}, want {exp_meas}")

    # Evidence.level derivation (issue #67 backfill)
    level_cases = [
        ("**Hands-on, measured** A/B with token deltas.", "MEASURED"),
        ("Source-grounded review — not run hands-on; read the docs.", "REVIEW"),
        ("We ran it on our repo and exercised the CLI flow.", "RUN"),
        ("", "SOURCE-ONLY"),
    ]
    for how, want in level_cases:
        got = Evidence(how).level
        if got != want:
            fails.append(f"  FAIL [level] {how[:32]!r}: got {got}, want {want}")

    # Evaluation parsing — the eval-file grammar is now a unit-testable surface
    def expect(cond, msg):
        if not cond: fails.append(f"  FAIL [eval] {msg}")
    skill = Evaluation("foo",
        "# Evaluation: Foo\n\n| [foo](https://github.com/a/foo) | skill | x | y | z |\n\n## Verdict\n\n**ADOPT**\n")
    expect(skill.is_skill, "skill-type row not detected")
    expect(skill.verdict == "ADOPT", f"verdict {skill.verdict!r} != ADOPT")
    expect("foo" in skill.name_aliases, "name alias from heading missing")
    tool = Evaluation("bar",
        "| [bar](https://github.com/a/bar) | tool | x | y | z |\n\n## Verdict\n\n**SKIP**\n")
    expect(not tool.is_skill, "tool-type row misdetected as skill")
    dual = Evaluation("baz", "## Verdict\n\n**ADOPT** for X — **CONDITIONAL** otherwise\n")
    expect(dual.verdict_set == {"ADOPT", "CONDITIONAL"}, f"dual verdict_set {dual.verdict_set}")
    none = Evaluation("qux", "## Overview\n\nNo verdict here.\n")
    expect(none.verdict is None and none.verdict_set == set(), "missing verdict not handled")
    # A lead headlines its own status rather than borrowing CONDITIONAL (#324).
    lead = Evaluation("lead", "## Verdict\n\n**discovery-log — tentative read** — notes only.\n")
    expect(lead.verdict == "discovery-log", f"lead verdict {lead.verdict!r} != discovery-log")
    # declared Evidence field (issue #62)
    eviz = Evaluation("ev", "## How we tested it\n\n**Evidence:** MEASURED\n\nran it live.\n")
    expect(eviz.evidence_level == "MEASURED", f"evidence_level {eviz.evidence_level!r} != MEASURED")
    src = Evaluation("sv", "**Evidence:** SOURCE-ONLY\n")
    expect(src.evidence_level == "SOURCE-ONLY", f"hyphenated level {src.evidence_level!r} != SOURCE-ONLY")
    expect(none.evidence_level is None, "absent Evidence field not None")
    n_eval_checks = 10

    if fails:
        print("== selftest ==")
        print("\n".join(fails))
        return 1
    print(f"== selftest ==\n  OK — {len(cases)} evidence + {len(level_cases)} level + {n_eval_checks} eval-parsing cases pass")
    return 0

# ---------------------------------------------------------------- CLI flag sets
# The seven offline gates `--offline` selects — the set `make check`, the
# `.claude/hooks/audit-gate.sh` pre-commit hook and the opencode commit-gate plugin all
# run (all three invoke `--offline` bare, so they move together). This tuple is the
# source of truth for what "offline" means; CLAUDE.md's prose list documents it and
# must be updated alongside any change here.
# ---------------------------------------------------------------- W. P0 scope mismatch (report-only)
# The score has no scope term (#353). Every term measures attention, so a lead that
# WORKFLOW.md's one-line exclusion already disposes of can still rank into P0 measure —
# the band reserved for leads that might reach ADOPT, and the one an unattended pass may
# not write to. Spending a measured evaluation to reach a SKIP a codified rule already
# reached is the most expensive path to that SKIP.

# The eval's OWN concession, harvested from the corpus rather than invented. The two
# dominant strings are WORKFLOW.md's exclusion quoted verbatim by the #348 SKIP pass.
SCOPE_CONCESSION = re.compile(
    r"for building AI products"
    r"|not for your own dev workflow"
    r"|building agentic products"
    r"|building an agentic product"
    r"|for building agent products"
    r"|build(?:s|ing) LLM apps"       # pydantic-ai: "It builds LLM apps, not coding agents."
    r"|building LLM-powered"
    r"|not a coding (?:agent|harness)"
    r"|drop-in coding harness"
    r"|not authoring code"
    r"|tangential to (?:the )?(?:coding|authoring)"
    r"|adjacent to the coding dev loop", re.IGNORECASE)

# An eval that quotes the exclusion in order to DISTINGUISH itself from it. Same shape as
# detector B's HONEST vocabulary: the escape hatch is what keeps the finding count honest,
# so widen this when it false-flags rather than narrowing the concession vocab above.
SCOPE_CLEARED = re.compile(
    r"clears the bar"
    r"|catalog-relevant as"
    r"|genuine bridge into"
    r"|not (?:merely |just )?a library for building", re.IGNORECASE)

# The Types WORKFLOW.md's exclusion is about ("visual/programmatic agent builders").
# A harness or tool is something you RUN; the exclusion was never aimed at it.
SCOPE_TYPES = frozenset({"framework", "platform"})

ScopeFinding = collections.namedtuple("ScopeFinding", "tool band typ phrase")


def audit_scope(ctx):
    """(findings, cleared) — leads whose own eval concedes the WORKFLOW.md scope
    exclusion, P0 first. `cleared` holds the ones that argue they clear the bar; they
    are printed but not counted, because a detector whose headline number includes its
    own known false positives is not a number anyone shrinks."""
    # Lazy import: triage.py loads THIS module at import time, so a module-level import
    # here would recurse. Called from main(), the nested copy never re-enters.
    triage = _load_sibling("triage_bands", "triage.py")
    try:
        ordered, _ = triage.assign(ctx)
    except (OSError, ValueError, KeyError):
        return [], []

    types = {catalog_lib.name_key(r.name): (r.type or "").strip()
             for r in catalog_lib.parse_catalog_rows(ctx.catalog)}
    by_key = {}
    for ev in ctx.evals:
        for k in catalog_lib.identity_keys(ev.name):
            by_key.setdefault(k, ev)

    findings, cleared = [], []
    for band, rows in ordered.items():
        for row in rows:
            tool = row[1]
            typ = types.get(catalog_lib.name_key(tool), "")
            if typ not in SCOPE_TYPES:
                continue
            ev = next((by_key[k] for k in catalog_lib.identity_keys(tool) if k in by_key), None)
            if ev is None:
                continue
            m = SCOPE_CONCESSION.search(ev.text)
            if not m:
                continue
            f = ScopeFinding(tool, band, typ, _scope_quote(ev.text, m))
            (cleared if SCOPE_CLEARED.search(ev.text) else findings).append(f)

    # P0 first: it is the only band a bulk lane cannot reach, so a finding there is the
    # one that stays stuck until a human looks.
    for bucket in (findings, cleared):
        bucket.sort(key=lambda f: (0 if f.band.startswith("P0") else 1, f.band, f.tool))
    return findings, cleared


def _scope_quote(text, match, width=110):
    """The conceding phrase in its own line, windowed around the match. Quoted rather
    than summarized so a human judges the eval's own words — detector V's rule, for the
    same reason: a phrase match is a candidate, not a disposition.

    Line-scoped on purpose. A sentence-scoped window ran past `\n` and produced quotes
    that spliced a header into a prose line ("...dev loop **Layer:** Infrastructure"),
    which reads as a garbled claim rather than as the eval's words."""
    ls = text.rfind("\n", 0, match.start()) + 1
    le = text.find("\n", match.end())
    line = " ".join(text[ls: le if le != -1 else len(text)].split()).strip(" -*_#|")
    hit = line.lower().find(match.group(0).lower().split("\n")[0][:20])
    if len(line) <= width or hit == -1:
        return line[:width] + ("…" if len(line) > width else "")
    start = max(0, hit - (width - len(match.group(0))) // 2)
    frag = line[start:start + width]
    return ("…" if start else "") + frag + ("…" if start + width < len(line) else "")



# ---------------------------------------------------------------- X. collapsed catalog identity (report-only)
# Two rows, one artifact (#343). A row naming a COMPONENT of something catalogued as a
# WHOLE overstates the lead queue, makes a redundancy verdict between the two meaningless
# ("redundant with X" is not a thing you can say about X's own contents), and strands the
# eliminate-only band, which can neither SKIP it nor explain it in a verdict.

IdentityFinding = collections.namedtuple("IdentityFinding", "kind slug tool verdict peers")

SETTLED_VERDICTS = frozenset({"ADOPT", "KEEP"})


def audit_identity(ctx):
    """(findings, faceted) — leads that are facets of one catalogued artifact, plus the
    multi-row groups that are NOT findings, carried so neither goes unmentioned.

    The split is by LINK SHAPE, and it carries all the precision. Where every row in a
    slug group points at one identical URL, nothing in the catalog tells them apart —
    that is the #343 pattern. Where each row links its own subpath, the group is a
    monorepo of independently-installable artifacts (`claude-plugins-official`: 8 rows,
    8 subpaths), which is a different thing and must not be counted as drift."""
    rows = [r for r in catalog_lib.parse_catalog_rows(ctx.catalog) if r.url]
    groups = collections.defaultdict(list)
    for r in rows:
        slug = next(iter(catalog_lib.github_repos(r.url)), None)
        if slug:
            groups[slug.lower()].append(r)

    verd = ctx.comparison_verdict_map

    def verdict_of(name):
        return next((verd[k] for k in catalog_lib.identity_keys(name) if k in verd), "—")

    findings, context = [], []
    for slug, members in sorted(groups.items()):
        if len(members) < 2:
            continue
        by_verdict = [(r.name, verdict_of(r.name)) for r in members]
        names = tuple(n for n, _ in by_verdict)
        if len({r.url for r in members}) == len(members):
            context.append(IdentityFinding("FACETED", slug, "", "", names))
            continue
        settled = tuple((n, v) for n, v in by_verdict if v in SETTLED_VERDICTS)
        leads = [n for n, v in by_verdict if v == "discovery-log"]
        if not leads:
            # The identity is still collapsed, but no queue slot is wasted — every row
            # is already disposed. Reported so the group is not silently invisible.
            context.append(IdentityFinding("NO-LEADS", slug, "", "", names))
            continue
        for name in leads:
            findings.append(IdentityFinding(
                "SETTLED" if settled else "COLLAPSED", slug, name,
                settled[0][1] if settled else "",
                tuple(n for n, _ in settled) if settled
                else tuple(n for n in names if n != name)))

    # SETTLED first: a lead whose artifact is already ADOPT/KEEP is the one whose queue
    # slot is provably wasted, where a COLLAPSED group is merely two facets of one
    # undecided thing.
    findings.sort(key=lambda f: (0 if f.kind == "SETTLED" else 1, f.slug, f.tool))
    return findings, context



# ---------------------------------------------------------------- Y. install-record mismatch (report-only)
# KEEP is DEFINED as the validated-installed status, and nothing checked the installed
# half (#366). Joined on SLUG rather than name, because name-matching is the bug itself:
# #332's "already installed/active" was a marketplace cache directory, and three STACK
# members are name collisions with an artifact from a different source.

SKILL_LOCK = "~/.agents/.skill-lock.json"          # npx skills (vercel-labs/skills) v3
PLUGIN_RECORD = "~/.claude/plugins/installed_plugins.json"
SKILL_DIR = "~/.claude/skills"
PLUGIN_CACHE = "~/.claude/plugins/cache"           # <marketplace>/<plugin>/<version|unknown>
# #332's discriminator, generalized. A directory under the plugin cache means the
# MARKETPLACE was added, never that a plugin was installed — that is the trap #332 fell
# into. But the version subdirectory splits the trap in two: `unknown` is listing metadata
# for a plugin whose code was never fetched, while a real version string ('3.1.0', a commit
# sha) means this machine pulled that plugin at that version. #332 used exactly this to
# separate the genuinely-installed claude-md-management (`1.0.0`, matching its installPath)
# from plugin-dev (`unknown`). Evidence of a fetch is strictly more than `unknown` and
# strictly less than an installed_plugins.json entry, so it gets its own bucket rather
# than being collapsed into either.
UNFETCHED = "unknown"
# The only Types these records can cover. A CLI or an MCP server is installed by npm,
# brew or a settings entry, none of which leaves a mark here — flagging them would be
# noise indistinguishable from signal.
INSTALLABLE_TYPES = frozenset({"skill", "plugin"})

InstallFinding = collections.namedtuple("InstallFinding", "kind tool verdict detail")


def read_install_records(home=None):
    """(skill_name -> source slug, set of installed slugs, set of names on disk,
    plugin name -> fetched version).

    Every value is absent-tolerant: a machine with no lockfile is a machine we know
    nothing about, which must read as 0 records rather than as a clean bill."""
    def path(p):
        return os.path.join(home, p.replace("~/", "")) if home else os.path.expanduser(p)

    by_name, slugs, on_disk, fetched = {}, set(), set(), {}
    try:
        with open(path(SKILL_LOCK), encoding="utf-8") as fh:
            for name, meta in (json.load(fh).get("skills") or {}).items():
                src = (meta or {}).get("source")
                if src:
                    by_name[name] = src.lower()
                    slugs.add(src.lower())
    except (OSError, ValueError, AttributeError):
        pass
    try:
        with open(path(PLUGIN_RECORD), encoding="utf-8") as fh:
            for key in (json.load(fh).get("plugins") or {}):
                on_disk.add(key.split("@")[0])
    except (OSError, ValueError, AttributeError):
        pass
    with contextlib.suppress(OSError):
        on_disk |= set(os.listdir(path(SKILL_DIR)))
    cache = path(PLUGIN_CACHE)
    for market in _listdir(cache):
        for plugin in _listdir(os.path.join(cache, market)):
            vers = [v for v in _listdir(os.path.join(cache, market, plugin))
                    if v != UNFETCHED]
            if vers:                       # a real version string: the code was pulled
                # Every fetched version, not a "latest": these are opaque strings (semver
                # AND commit shas), and a lexicographic max reads 13.11.0 as older than
                # 13.4.0. Reporting the set states what is on disk and invents no order.
                fetched.setdefault(plugin, ", ".join(vers))
    return by_name, slugs, on_disk, fetched


def _listdir(p):
    try:
        return sorted(d for d in os.listdir(p) if not d.startswith("."))
    except OSError:
        return []


def audit_installed(ctx, home=None):
    """(findings, shadowed, records) — ADOPT/KEEP skill/plugin rows this machine's install
    records do not back, plus installed sources the catalog does not know.

    THE SLUG IS ASKED FIRST (#366). The row's own slug being present in the lockfile
    settles the row: it is installed, full stop. A skill of the same name sourced from
    somewhere else is then a name shadow, not a missing install — `caveman` (ADOPT,
    JuliusBrussee/caveman) ships four `caveman-*` skills that ARE installed here, while
    the bare name `caveman` in the lockfile belongs to mattpocock/skills. Testing the
    name first reported that row as a COLLISION, i.e. as an unbacked ADOPT, which it is
    not. A detector that flags a healthy row is worse than one that misses a sick one —
    detector V's rule, and the same identity-by-name root the detector exists to find.

    Shadows are returned APART and printed rather than counted: the name really does
    resolve elsewhere on this machine, which is worth knowing and is not a defect in
    the row (V's `acked`, W's `cleared`, X's `FACETED`).

    CACHE-ONLY sits between NO-RECORD and clean (#366). The plugin cache is #332's trap
    — a directory there means the marketplace was added — but the version subdirectory
    splits it: `unknown` is listing metadata, while a real version string means the code
    was pulled. Four rows sat in NO-RECORD holding a fetched version (claude-reflect
    3.1.0, superpowers 5.1.0, security-guidance 2.0.6, claude-mem 13.11.0/13.4.0), which
    'nothing on the machine answers to this row' does not describe. It is still a finding
    — a fetch is not an activation, and nothing records which of the two happened — but
    calling it NO-RECORD overstates by exactly the amount #332 warned about in the other
    direction."""
    by_name, slugs, on_disk, fetched = read_install_records(home)
    records = len(by_name) + len(on_disk) + len(fetched)
    if not records:
        return [], [], 0

    verd = ctx.comparison_verdict_map
    rows = [r for r in catalog_lib.parse_catalog_rows(ctx.catalog) if r.url]
    catalogued = {(next(iter(catalog_lib.github_repos(r.url)), "") or "").lower()
                  for r in rows}
    lock_by_key = {catalog_lib.name_key(n): s for n, s in by_name.items()}
    disk_keys = {catalog_lib.name_key(n) for n in on_disk}
    fetched_keys = {catalog_lib.name_key(n): v for n, v in fetched.items()}

    findings, shadowed = [], []
    for r in rows:
        v = next((verd[k] for k in catalog_lib.identity_keys(r.name) if k in verd), "—")
        if v not in SETTLED_VERDICTS or (r.type or "").strip() not in INSTALLABLE_TYPES:
            continue
        slug = (next(iter(catalog_lib.github_repos(r.url)), "") or "").lower()
        key = catalog_lib.name_key(r.name)
        installed_from = lock_by_key.get(key)
        shadow = installed_from and installed_from != slug
        if slug in slugs:                      # the row's own repo is installed: settled
            if shadow:
                shadowed.append(InstallFinding(
                    "SHADOWED", r.name, v,
                    f"{slug} is installed; the name '{r.name}' resolves to "
                    f"{installed_from} instead"))
        elif shadow:
            findings.append(InstallFinding(
                "COLLISION", r.name, v,
                f"row says {slug}, installed skill of that name comes from {installed_from}"))
        elif key in fetched_keys:
            findings.append(InstallFinding(
                "CACHE-ONLY", r.name, v,
                f"no install record; plugin cache holds fetched version(s) "
                f"{fetched_keys[key]} — code was pulled, activation is unrecorded"))
        elif key not in disk_keys:
            findings.append(InstallFinding(
                "NO-RECORD", r.name, v, f"no record and no directory answers to {slug}"))

    for slug in sorted(slugs - catalogued):
        n = sum(1 for s in by_name.values() if s == slug)
        findings.append(InstallFinding("UNCATALOGUED", slug, "—",
                                       f"{n} installed skill(s), no catalog row"))

    rank = {"COLLISION": 0, "NO-RECORD": 1, "CACHE-ONLY": 2, "UNCATALOGUED": 3}
    findings.sort(key=lambda f: (rank[f.kind], f.tool))
    shadowed.sort(key=lambda f: f.tool)
    return findings, shadowed, records



# ---------------------------------------------------------------- Z. unread license declaration (report-only)
# `license_spdx: NONE` is what GitHub returns when there is no root LICENSE file. It is
# recorded, and read by triage.py's P4 mechanical-skip band, as though it meant the repo
# grants nothing — and for 8 of 28 records it did not (#372). This reports the gap
# against the disposition each row already carries, strongest first: a SKIP whose stated
# ground is the license is a wrong disposition, not merely a wrong record.

# A verdict "rests on the license" when it says so. Deliberately narrow — a passing
# mention ("MIT, permissive") must not count, or every clean row becomes a finding.
LICENSE_GROUND = re.compile(
    r"no (?:declared |real |explicit )?licen[cs]e"
    r"|licen[cs]e(?: is)? (?:not declared|absent|missing)"
    r"|no LICENSE file"
    r"|carrying no licen[cs]e grant"
    r"|licen[cs]e alone"
    r"|\*\*SKIP\*\* ?\(licen[cs]e\)", re.IGNORECASE)

# A verdict that has ALREADY withdrawn its license ground still quotes the claim it
# withdrew — because quoting it is the honest way to record a correction (detector V's
# rule). Without this, an eval is punished for documenting its own repair and the count
# can never reach zero. Same shape as W's "argues it clears the bar" and V's ack: still
# printed, not counted.
#
# The recognized form is a STRUCK-THROUGH claim, `~~…licen…~~`, or an explicit
# withdrawn/retracted sentence naming the license. Widen this vocabulary if it misses an
# honest retraction — never narrow LICENSE_GROUND to compensate, which would hide live
# findings to clear stale ones.
LICENSE_WITHDRAWN = re.compile(
    r"~~[^~]{0,300}licen[a-z]*[^~]{0,300}~~"
    r"|licen[a-z]*[^.\n]{0,100}(?:is |was |been )?(?:withdrawn|retracted)"
    r"|(?:withdrawn|retracted)[^.\n]{0,100}licen[a-z]*", re.IGNORECASE)

LicenseFinding = collections.namedtuple(
    "LicenseFinding", "kind tool slug verdict spdx where phrase conflict")


def audit_license_declared(ctx):
    """(findings, records) — catalogued repos whose metadata records a license declared
    outside a LICENSE file, plus the number of records carrying the field.

    A cache with no `license_declared` anywhere yields 0 RECORDS, not 0 findings: the
    field is written by the refresher, so its absence means "not collected", never
    "every NONE is a real absence" (detector V's rule, same reason)."""
    try:
        records = json.loads(ctx.read("repo-metadata.json"))
    except (OSError, ValueError):
        return [], 0, []
    if not isinstance(records, dict):
        return [], 0, []

    by_slug = {}
    for r in catalog_lib.parse_catalog_rows(ctx.catalog):
        if r.url:
            for s in catalog_lib.github_repos(r.url):
                by_slug.setdefault(s.lower(), r.name)
    verd = ctx.comparison_verdict_map
    # alias -> the eval's Verdict section, so "is the license the stated ground?" reads
    # the argument rather than the whole file (a How-we-tested `gh api ... .license` line
    # is evidence of a check, not of a disposition).
    grounds = {}
    for ev in ctx.evals:
        sec = re.search(r"##\s*Verdict.*?(?=\n##\s|\Z)", ev.text, re.DOTALL)
        if sec:
            for a in ev.name_aliases:
                grounds.setdefault(a, sec.group(0))

    collected = sum(1 for m in records.values()
                    if isinstance(m, dict) and m.get("license_declared"))
    findings, withdrawn = [], []
    for slug, meta in sorted(records.items()):
        if not isinstance(meta, dict):
            continue
        d = meta.get("license_declared")
        if not isinstance(d, dict) or not d.get("spdx"):
            continue
        tool = by_slug.get(slug, slug)
        v = next((verd[k] for k in catalog_lib.identity_keys(tool) if k in verd), "—")
        sec = next((grounds[a] for a in catalog_lib.alias_keys(tool) if a in grounds), "")
        grounded = v == "SKIP" and LICENSE_GROUND.search(sec)
        if grounded:
            kind = "GROUNDED"
        elif d.get("conflict"):
            kind = "CONFLICT"
        else:
            kind = "RECORDED"
        f = LicenseFinding(kind, tool, slug, v, d["spdx"], d.get("where", "?"),
                           d.get("phrase", ""), d.get("conflict"))
        (withdrawn if grounded and LICENSE_WITHDRAWN.search(sec) else findings).append(f)

    rank = {"GROUNDED": 0, "CONFLICT": 1, "RECORDED": 2}
    for bucket in (findings, withdrawn):
        bucket.sort(key=lambda f: (rank[f.kind], f.tool))
    return findings, collected, withdrawn


OFFLINE_GATES = ("--fabrication", "--verdicts", "--comparison", "--drift",
                 "--verdict-evidence", "--rows", "--bulk-triage")
# With no flags at all: the offline gates plus the network install resolver.
DEFAULT_GATES = (*OFFLINE_GATES, "--installs")
# Opt-in reports. Never in the default set; never affect the exit code.
REPORT_FLAGS = ("--links", "--archived", "--skills", "--skill-design", "--overlaps",
                "--workflow-drift", "--clusters", "--savings-claims", "--evidence",
                "--staleness", "--metadata-staleness", "--lead-headlines",
                "--catalog-mirror", "--maintenance", "--scope", "--identity", "--installed",
                "--license-declared")
DETECTOR_FLAGS = DEFAULT_GATES + REPORT_FLAGS
# Every argument main() accepts. Anything else is a typo, and a typo used to be silently
# dropped from `sel` — which made the argument list read as empty and turned `--ofline`
# into "run everything, including the ~26s network resolver", exit 0. Fail loudly instead.
KNOWN_FLAGS = (*DETECTOR_FLAGS, "--offline", "--selftest")

# ---------------------------------------------------------------- main
def main():
    args = sys.argv[1:]
    if "--selftest" in args:
        sys.exit(selftest())

    unknown = [a for a in args if a not in KNOWN_FLAGS]
    if unknown:
        print(f"audit-evals: unknown argument(s): {' '.join(unknown)}", file=sys.stderr)
        print(f"  known: {' '.join(sorted(KNOWN_FLAGS))}", file=sys.stderr)
        sys.exit(2)

    # Requested detectors are a UNION, so a flag can only ever ADD work. The old matrix
    # ended in an `if explicit:` block that dropped the `or "--offline" in sel` clause,
    # so `--offline --verdicts` ran 1 detector where `--offline` alone ran 7 — adding a
    # flag silently deleted six gates and still exited 0.
    # Every surviving arg is a detector flag or `--offline`: `--selftest` returned above
    # and anything unrecognized exited 2, so no filtering is left to do here.
    sel = set(args)
    want = set()
    if "--offline" in sel:
        want |= set(OFFLINE_GATES)
    want |= (sel - {"--offline"})
    if not want:
        want = set(DEFAULT_GATES)

    do_inst = "--installs" in want
    do_fab  = "--fabrication" in want
    do_verd = "--verdicts" in want           # offline, fast
    do_comp = "--comparison" in want         # offline gate
    do_drift = "--drift" in want             # offline gate (#70)
    do_vev = "--verdict-evidence" in want    # offline gate (#71)
    do_rows = "--rows" in want               # offline gate (#198)
    do_bulk = "--bulk-triage" in want        # offline gate
    do_links = "--links" in want             # opt-in: ~450 network requests, slow
    do_archived = "--archived" in want       # opt-in: ~450 gh-api calls; report-only
    do_skills = "--skills" in want           # opt-in report (does not affect exit code)
    do_skill_design = "--skill-design" in want  # opt-in report (does not affect exit code)
    do_overlaps = "--overlaps" in want       # opt-in report (does not affect exit code)
    do_wf_drift = "--workflow-drift" in want    # opt-in report (does not affect exit code)
    do_clusters = "--clusters" in want       # opt-in report (does not affect exit code)
    do_savings = "--savings-claims" in want  # opt-in report (does not affect exit code)
    do_evidence = "--evidence" in want       # opt-in report (does not affect exit code)
    do_staleness = "--staleness" in want     # opt-in report (does not affect exit code)
    do_meta_stale = "--metadata-staleness" in want  # opt-in report (does not affect exit code)
    do_lead_head = "--lead-headlines" in want   # opt-in report (does not affect exit code)
    do_mirror = "--catalog-mirror" in want   # opt-in report (does not affect exit code)
    do_maint = "--maintenance" in want       # opt-in report (does not affect exit code)
    do_scope = "--scope" in want             # opt-in report (does not affect exit code)
    do_ident = "--identity" in want          # opt-in report (does not affect exit code)
    # NOT `do_inst` — that name belongs to detector A's `--installs`. Reusing it
    # silently rebound it, so `--installed` also ran the network install resolver.
    do_instrec = "--installed" in want       # opt-in LOCAL report (never a gate)
    do_licdecl = "--license-declared" in want  # opt-in report (does not affect exit code)

    ctx = DetectorContext(ROOT)  # the one place the module global feeds the detectors (#199)
    rc = 0
    if do_inst:
        print("== A. install resolver ==")
        broken = audit_installs(ctx)
        if broken:
            rc = 1
            for rel, kind, pkg in broken:
                print(f"  BROKEN [{kind}] {pkg}  ({rel})")
        else:
            print("  OK — all checked install targets resolve")
    if do_fab:
        print("== B. fabrication classifier ==")
        flagged = audit_fabrication(ctx)
        if flagged:
            rc = 1
            print(f"  REVIEW ({len(flagged)}): a 'How we tested' that claims a run with no honesty disclaimer")
            for b in flagged:
                print(f"    - {b}")
        else:
            print("  OK — every 'How we tested' either discloses not-run or shows a verified run")
    if do_verd:
        print("== D. verdict sync (eval ## Verdict vs COMPARISON.md) ==")
        vflag = audit_verdicts(ctx)
        if vflag:
            rc = 1
            for name, ev, cv in vflag:
                print(f"  MISMATCH {name}: eval={ev}  COMPARISON={cv}")
        else:
            print("  OK — eval verdicts agree with COMPARISON (dual verdicts & KEEP tolerated)")
    if do_comp:
        print("== G. comparison consistency (COMPARISON.md vs CATALOG.md) ==")
        cprob = audit_comparison(ctx)
        if cprob:
            rc = 1
            for p in cprob:
                print(f"  DRIFT {p}")
        else:
            print("  OK — COMPARISON summary sums to its body rows and Total matches CATALOG.md")
    if do_rows:
        print("== O. row shape (CATALOG.md / COMPARISON.md table rows) ==")
        rprob = audit_row_shapes(ctx)
        if rprob:
            rc = 1
            for p in rprob:
                print(f"  MALFORMED {p}")
        else:
            print("  OK — every table row parses as a well-formed entry row")
    if do_bulk:
        print("== Q. eliminate-only bulk triage ==")
        bprob = audit_bulk_triage(ctx)
        if bprob:
            rc = 1
            for name, verdict in bprob:
                if verdict == UNATTRIBUTED:
                    print(f"  UNATTRIBUTED {name}: carries `{TRIAGE_STAMP}` with neither "
                          f"`{BULK_MARKER}` nor `{HUMAN_MARKER}` — Q cannot police a lane "
                          f"it cannot identify (#327)")
                else:
                    print(f"  OVERREACH {name}: bulk-triaged eval claims {verdict} — "
                          f"the bulk lane may only SKIP or leave at discovery-log")
        else:
            print("  OK — every bulk-triaged eval stays within eliminate-only authority")
    if do_drift:
        print("== J. stack-derivation drift (STACK.md vs verdicts + ledger) ==")
        dprob = audit_stack_drift(ctx)
        if dprob:
            rc = 1
            for p in dprob:
                print(f"  DRIFT {p}")
        else:
            print("  OK — every ADOPT/KEEP tool is in STACK or the ledger; STACK & ledger agree with verdicts")
    if do_vev:
        print("== K. verdict evidence (ADOPT/KEEP must be run-backed or disclaimered) ==")
        vev = audit_verdict_evidence(ctx)
        if vev:
            rc = 1
            for name, verd, lvl in vev:
                print(f"  WEAK {name}: {verd} backed only by {lvl} and no honesty disclaimer "
                      f"(graduate the eval to MEASURED/RUN, or add a not-run disclaimer)")
        else:
            print("  OK — every ADOPT/KEEP eval is run-backed (MEASURED/RUN) or carries a disclaimer")
    if do_links:
        problems, unknowns, total = audit_links(ctx)
        checked = total - len(unknowns)
        print(f"== C. link rot (CATALOG.md repo links) — {checked}/{total} checked ==")
        if problems:
            rc = 1
            for slug, res in problems:
                print(f"  {'DEAD' if res=='dead' else 'MOVED'} {slug}" + (f" -> {res[6:]}" if res.startswith('moved:') else ""))
        if unknowns:
            # Never "OK" on an inconclusive run: this detector once printed a clean
            # sweep of 612 links while GitHub 429'd every single request (#319).
            reasons = collections.Counter(r for _, r in unknowns)
            summary = ", ".join(f"{n}x {r}" for r, n in reasons.most_common())
            print(f"  INCONCLUSIVE — {len(unknowns)} link(s) could not be verified ({summary}).")
            print("  Re-run later, or authenticate: an unauthenticated burst of ~600 HEAD "
                  "requests is rate-limited. Findings above are still real; absence of "
                  "findings is NOT a pass.")
        elif not problems:
            print(f"  OK — all {total} catalog repo links resolve to their canonical names")
    if do_archived:
        print("== H. archived repos (report-only) ==")
        arch, total = audit_archived(ctx)
        undisclosed = [(s, p) for s, p, flagged in arch if not flagged]
        for s, p, flagged in arch:
            tag = "" if flagged else "  <- NOT disclosed in the entry; add a ⚠️ archived note or repoint"
            print(f"  ARCHIVED {s} (last push {p}){tag}")
        if not arch:
            print(f"  OK — none of {total} catalog repos are archived")
        elif not undisclosed:
            print(f"  ({len(arch)} archived, all already disclosed with a ⚠️ note)")
    if do_skills:
        measured, backlog = audit_skill_evidence(ctx)
        tot = len(measured) + len(backlog)
        print(f"== E. skill evidence (report-only) — {len(measured)}/{tot} ADOPT skills have measured backing ==")
        for n in measured:
            print(f"  MEASURED {n}")
        for n in backlog:
            print(f"  backlog  {n}  (ADOPT skill, review-based — would benefit from a measured A/B; see TEMPLATE.md)")
    if do_skill_design:
        compliant, missing = audit_skill_design(ctx)
        tot = len(compliant) + len(missing)
        print(f"== S. skill test-design (report-only) — {len(compliant)}/{tot} skill/plugin evals record a triggering test or A/B ==")
        for n in compliant:
            print(f"  ok       {n}")
        for n in missing:
            print(f"  MISSING  {n}  (skill/plugin eval records neither a triggering test nor an A/B; see TEMPLATE.md's skills Test-design section)")
        if not missing:
            print("  OK — every skill/plugin eval records at least one skill dimension")
    if do_evidence:
        counts, missing, strong = audit_evidence_field(ctx)
        have = sum(counts.values()); tot = have + len(missing)
        strong_tot = sum(strong.values())
        print(f"== I. evidence-strength field (report-only) — {have}/{tot} evals declare Evidence ==")
        for lvl in EVIDENCE_LEVELS:
            print(f"  {lvl:<12} {counts[lvl]}")
        if missing:
            print(f"  {'(none)':<12} {len(missing)}  (eval declares no Evidence field — run ./backfill-evidence.py)")
        if strong_tot:
            backed = strong['MEASURED'] + strong['RUN']
            pct = round(100 * strong['MEASURED'] / strong_tot)
            print(f"  ADOPT/KEEP set ({strong_tot}): {strong['MEASURED']} MEASURED ({pct}%), "
                  f"{strong['RUN']} RUN, {strong['REVIEW']} REVIEW, {strong['SOURCE-ONLY']} SOURCE-ONLY "
                  f"→ {backed}/{strong_tot} run-backed (the rest are review-only — #68 graduates them, #71 gates)")
    if do_staleness:
        stale, undated = audit_staleness(ctx)
        print(f"== L. staleness sweep (report-only) — {len(stale)} stale eval(s), {undated} undated ==")
        for name, typ, d, age, thr in sorted(stale, key=lambda r: -r[3]):
            print(f"  STALE {name} ({typ}) last verified {d} — {age}d old > {thr}d threshold")
        if not stale:
            print("  OK — no dated eval is past its category staleness threshold")
        if undated:
            print(f"  ({undated} evals carry no **Last verified:** date yet — add one when you re-check them)")
    if do_meta_stale:
        total, undated, stale, oldest = audit_metadata_staleness(ctx)
        print(f"== R. metadata staleness (report-only) — {total} record(s), "
              f"{len(stale)} past {METADATA_STALE_DAYS}d, {undated} undated ==")
        if not total:
            print("  no repo-metadata.json — run `python3 refresh-metadata.py` to build it")
        elif oldest is None:
            print("  UNDATED — no record carries a fetch date, so the cache's age is unknown.")
            print("  Run `python3 refresh-metadata.py` to stamp them (not backfilled: a "
                  "floor date would assert a fetch that never happened).")
        else:
            slug, date, age = oldest
            print(f"  oldest fetch {date} ({age}d ago, {slug})")
            if stale:
                print(f"  {len(stale)} record(s) past the {METADATA_STALE_DAYS}d threshold — "
                      "an archived-since repo still reads as live to the triage bands.")
                print("  Refresh: `python3 refresh-metadata.py`")
            else:
                print("  OK — every stamped record is within the threshold")
            if undated:
                print(f"  ({undated} record(s) carry no fetch date — refresh to stamp them)")
    if do_overlaps:
        gaps = audit_overlaps(ctx)
        strong = [(t, c) for t, c in gaps if c >= 2]
        print(f"== F. dangling overlaps (report-only) — {len(gaps)} uncatalogued peer tokens ==")
        if not gaps:
            print("  OK — every 'Overlaps with' token resolves to a catalog entry")
        for t, c in strong:
            print(f"  GAP?  {t}  ({c} refs — likely a notable tool missing from the catalog)")
        for t, c in gaps:
            if c < 2:
                print(f"  maybe {t}  ({c} ref — check: real gap or external/conceptual peer)")
    if do_wf_drift:
        wfmiss = audit_workflow_drift(ctx)
        print(f"== P. WORKFLOW↔STACK drift (report-only) — {len(wfmiss)} STACK pick(s) missing from WORKFLOW.md ==")
        if not wfmiss:
            print("  OK — every STACK pick appears somewhere in WORKFLOW.md")
        for slug, ln in wfmiss:
            print(f"  MISSING {slug}  (STACK.md:{ln} — add it to the appropriate WORKFLOW stage)")
    if do_clusters:
        cl = audit_clusters(ctx)
        print(f"== M. clusters without a pick (report-only, #69) — {len(cl)} overlap cluster(s) all-CONDITIONAL, no ADOPT/KEEP pick ==")
        if not cl:
            print("  OK — every overlap cluster with a CONDITIONAL member also has an ADOPT/KEEP pick")
        for members in cl:
            print(f"  PICK?  {' / '.join(members)}")
    if do_savings:
        sav = audit_savings_claims(ctx)
        silent = [r for r in sav if not r[2]]
        print(f"== N. token-savings claims (report-only) — {len(silent)} unverified savings claim(s), "
              f"{len(sav) - len(silent)} self-reported ==")
        if not sav:
            print("  OK — every numeric token-savings headline is run-backed (MEASURED/RUN)")
        for name, lvl, disclosed in sav:
            tag = "  [self-reported — honest, but verify]" if disclosed else \
                  "  (run the token-savings protocol to graduate to MEASURED)"
            print(f"  UNVERIFIED {name}  ({lvl}){tag}")
    if do_lead_head:
        leads = audit_lead_headlines(ctx)
        print(f"== T. lead headline overreach (report-only) — {len(leads)} lead(s) "
              f"headlining a verdict they are not entitled to ==")
        if not leads:
            print("  OK — every discovery-log lead headlines discovery-log or SKIP")
        for name, verd, lvl in leads:
            print(f"  OVERREACH {name}: row=discovery-log but eval headlines {verd} at {lvl} evidence "
                  f"(relabel it a tentative read, or promote the row with a run behind it)")
    if do_mirror:
        drift = audit_catalog_mirror(ctx)
        kinds = collections.Counter(f.kind for f in drift)
        evals_hit = len({f.eval_name for f in drift})
        print(f"== U. catalog-entry mirror drift (report-only) — {len(drift)} disagreement(s) "
              f"across {evals_hit} eval(s): {kinds['LINK']} LINK, {kinds['ORPHAN']} ORPHAN, "
              f"{kinds['TEXT']} TEXT, {kinds['CASE']} CASE, {kinds['AMBIG']} AMBIG ==")
        if not drift:
            print("  OK — every embedded catalog row matches CATALOG.md")
        # LINK first: a stale slug makes an eval assert facts about the wrong repo (#336),
        # where TEXT drift is a disagreement about wording that a human resolves per row.
        order = {"LINK": 0, "ORPHAN": 1, "AMBIG": 2, "TEXT": 3, "CASE": 4}
        for f in sorted(drift, key=lambda f: (order[f.kind], f.eval_name)):
            print(f"  {f.kind:6} {f.eval_name} [{f.tool}]: {f.detail}")
    if do_maint:
        finds, collected, acked = audit_maintenance(ctx)
        print(f"== V. maintenance signal (report-only) — {len(finds)} finding(s) "
              f"across {collected} record(s) carrying the signal ==")
        if not collected:
            print("  no maintenance data — run `python3 refresh-metadata.py --maintenance` "
                  "to collect it (absence of the field is 'not collected', not 'nothing is dead')")
        elif not finds:
            print("  OK — no catalogued repo announces discontinuation or has lost its license")
        for f in finds:
            print(f"  {f.kind} [{f.verdict}] {f.tool} ({f.slug}): {f.detail}")
        for f in acked:
            print(f"  acknowledged false positive — {f.tool} ({f.slug}): {f.detail}")
    if do_scope:
        finds, cleared = audit_scope(ctx)
        p0 = sum(1 for f in finds if f.band.startswith("P0"))
        print(f"== W. P0 scope mismatch (report-only) — {len(finds)} lead(s) whose eval "
              f"concedes the scope exclusion, {p0} in P0 ==")
        if not finds:
            print("  OK — no framework/platform lead concedes it is out of scope")
        for f in finds:
            print(f"  SCOPE [{f.band}] {f.tool} ({f.typ}): \"{f.phrase}\"")
        for f in cleared:
            print(f"  argues it clears the bar — [{f.band}] {f.tool} ({f.typ}): \"{f.phrase}\"")
    if do_ident:
        finds, context = audit_identity(ctx)
        settled = sum(1 for f in finds if f.kind == "SETTLED")
        print(f"== X. collapsed catalog identity (report-only) — {len(finds)} lead(s) that "
              f"are facets of one artifact, {settled} already settled ==")
        if not finds:
            print("  OK — no lead shares a catalog link with another row")
        for f in finds:
            tail = (f"already {f.verdict} as {f.peers[0]}" if f.kind == "SETTLED"
                    else f"shares its link with {', '.join(f.peers)}")
            print(f"  {f.kind:9} {f.tool} ({f.slug}): {tail}")
        for f in context:
            why = ("each row links its own subpath" if f.kind == "FACETED"
                   else "collapsed, but every row is already disposed")
            print(f"  {f.kind.lower()} ({why}) — {f.slug}: "
                  f"{len(f.peers)} rows, {', '.join(f.peers)}")
    if do_instrec:
        finds, shadowed, records = audit_installed(ctx)
        print(f"== Y. install-record mismatch (report-only, this machine) — "
              f"{len(finds)} finding(s) across {records} install record(s) ==")
        if not records:
            print("  no install records found — absence of a record is 'nothing known "
                  "about this machine', never 'nothing is installed'")
        elif not finds:
            print("  OK — every ADOPT/KEEP skill/plugin row is backed by an install record")
        for f in finds:
            print(f"  {f.kind:12} {f.tool} [{f.verdict}]: {f.detail}")
        for f in shadowed:
            print(f"  {f.kind:12} (installed; name shadowed, not counted) "
                  f"{f.tool} [{f.verdict}]: {f.detail}")
    if do_licdecl:
        finds, records, withdrawn = audit_license_declared(ctx)
        grounded = sum(1 for f in finds if f.kind == "GROUNDED")
        print(f"== Z. unread license declaration (report-only) — {len(finds)} record(s) "
              f"whose 'NONE' license is declared elsewhere, {grounded} carrying a "
              f"license-grounded SKIP ==")
        if not records:
            print("  no license_declared data — run `python3 refresh-metadata.py` to "
                  "collect it (absence of the field is 'not collected', never 'every "
                  "NONE is a real absence')")
        elif not finds:
            print("  OK — no catalogued repo declares a license GitHub failed to read")
        for f in finds:
            extra = f" — manifest says {f.conflict}" if f.conflict else ""
            print(f"  {f.kind:8} {f.tool} ({f.slug}) [{f.verdict}]: {f.spdx} in "
                  f"{f.where}{extra} — \"{f.phrase}\"")
        for f in withdrawn:
            print(f"  ground already withdrawn — {f.tool} ({f.slug}) [{f.verdict}]: "
                  f"{f.spdx} in {f.where}")
    sys.exit(rc)

if __name__ == "__main__":
    main()
