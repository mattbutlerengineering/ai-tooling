#!/usr/bin/env python3
"""
audit-evals.py — integrity checks for the ai-tooling catalog.

Twelve detectors (A-L), each proven to catch real problems (see git history,
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
     renames (moved). ~450 network requests, so it is off by default.

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

Usage:
  python3 audit-evals.py              # A + B + D + G (D/B/G offline; A hits registries)
  python3 audit-evals.py --offline    # B + D + G only (no network)
  python3 audit-evals.py --installs   # install resolver only
  python3 audit-evals.py --fabrication # fabrication classifier only
  python3 audit-evals.py --verdicts   # verdict-sync only (offline)
  python3 audit-evals.py --comparison # COMPARISON.md vs CATALOG.md consistency (offline)
  python3 audit-evals.py --drift      # STACK.md vs verdicts + exclusion ledger (offline)
  python3 audit-evals.py --verdict-evidence  # ADOPT/KEEP must be run-backed or disclaimered (offline)
  python3 audit-evals.py --links      # link-rot sweep only (slow, ~450 requests)
  python3 audit-evals.py --archived   # archived-repo report (slow, ~450 gh-api calls)
  python3 audit-evals.py --skills     # skill-evidence backlog report (offline)
  python3 audit-evals.py --overlaps   # dangling overlap-reference report (offline)
  python3 audit-evals.py --evidence   # declared Evidence-field distribution (offline)
  python3 audit-evals.py --staleness  # flag evals past their last-verified threshold (offline)
  python3 audit-evals.py --selftest   # unit-test the evidence classifier (offline)

Exit code is non-zero if any gating detector finds a problem — a BROKEN install
(A), a FABRICATION candidate (B), a VERDICT mismatch (D), COMPARISON drift (G),
STACK-derivation drift (J), a WEAK-backed ADOPT/KEEP verdict (K), or link rot (C,
when --links is run) — so it can gate CI or a pre-commit hook. E (skill evidence),
F (dangling overlaps), and I (evidence field) are report-only and never affect the
exit code; --selftest exits non-zero on a failing assertion, so it can gate alone.
"""
import os, re, sys, json, glob, subprocess, datetime, urllib.request, urllib.error
import catalog_lib

ROOT = os.path.dirname(os.path.abspath(__file__))
TIMEOUT = 15

# Staleness thresholds in days, by eval Type (#65). Fast-moving categories rot sooner
# than stable references — configured in ONE place. Tune here, not per detector call.
STALENESS_DAYS = {
    "harness": 120, "MCP server": 120, "framework": 120, "platform": 120,  # fast-moving
    "tool": 180, "skill": 180, "plugin": 180,                              # moderate
    "reference": 365,                                                       # stable
}
DEFAULT_STALENESS_DAYS = 180

# ---------------------------------------------------------------- helpers
def http_ok(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ai-tooling-audit"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.status == 200
    except Exception:
        return False

def npm_exists(pkg):
    return subprocess.run(["npm", "view", pkg, "version"],
                          capture_output=True, text=True).returncode == 0

def gh_repo_exists(slug):
    return subprocess.run(["gh", "api", f"repos/{slug}", "--jq", ".full_name"],
                          capture_output=True, text=True).returncode == 0

def pypi_exists(pkg):   return http_ok(f"https://pypi.org/pypi/{pkg}/json")
def crates_exists(pkg): return http_ok(f"https://crates.io/api/v1/crates/{pkg}")

# ---------------------------------------------------------------- A. installs
PKG_CLEAN = lambda s: re.sub(r"[<>=].*|\[.*?\]|['\"]|@latest$", "", s).strip()

# A package token that is really a placeholder / prose fragment, not installable.
PLACEHOLDER = re.compile(r"^\.+$|\.\.\.|[<>{}|&]|^-|,$|"
                         r"^(install|installer|command|version|CLI|skills|name|pkg|package|foo|bar)$", re.I)
# If a backtick command is discussed as the WRONG/non-existent option ("not `npx x`",
# "listed as `npx x` (doesn't exist)", "earlier draft showed `x`, which does not exist"),
# it's a correction note, not an install to resolve. Markers can sit on either side.
NEGATION = re.compile(r"\b(not|non-?existent|does ?n.?t exist|do(es)? not exist|no such|wrong|"
                      r"instead of|isn.?t|rather than|earlier draft|was wrong|404|nonexistent)\b", re.I)

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

def audit_installs():
    files = ["STACK.md", "CATALOG.md"] + sorted(glob.glob("evaluations/*.md", root_dir=ROOT))
    seen, broken = {}, []
    checkers = {"pypi": pypi_exists, "crates": crates_exists, "npm": npm_exists, "gh": gh_repo_exists}
    for rel in files:
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p): continue
        for kind, pkg in extract_installs(open(p, encoding="utf-8").read()):
            key = (kind, pkg)
            if key in seen:
                ok = seen[key]
            else:
                ok = checkers[kind](pkg); seen[key] = ok
            if not ok:
                broken.append((rel, kind, pkg))
    return broken

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
                    r"could not install|attempted to apply", re.I)
# Specific run claims a fabricator invents (used only when no honest/verified marker is present).
RUN_CLAIM = re.compile(r"\b(ran it|we ran|i ran|ran the|ran against|added the .* server|"
                       r"used it (on|to|across)|deployed |generated |executed |"
                       r"launched |wrapped the|let it index|pointed it|fed it)\b", re.I)
# Markers of a genuine, trustable hands-on run.
VERIFIED = re.compile(r"\*\*hands-on\*\*|verified hands-on|verified (live|:)|re-verified|re-ran|"
                      r"ran it \*\*live\*\*|ran it (live|for real)|ran the .*\blive\b|live from inside|"
                      r"installed (it|the real|via|globally|as a skill|as a claude)|"
                      r"installed \(|pip[- ]?install.*\bran\b|exercised the|one real script execution|"
                      r"ran `|loaded all tool schemas", re.I)

def how_section(text):
    m = re.search(r"#+\s*How we tested.*?(?=\n#+\s|\Z)", text, re.S | re.I)
    return m.group(0) if m else ""

def audit_fabrication():
    flagged = []
    for ev in load_evals():
        if not ev.how:
            continue
        if ev.evidence.is_fabrication_candidate:
            flagged.append(ev.name)
    return flagged

# ---------------------------------------------------------------- C. link rot
def check_repo(slug):
    """Return 'ok', 'dead', or 'moved:<new>' for a github owner/repo slug."""
    url = f"https://github.com/{slug}"
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "ai-tooling-audit"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            final = r.geturl().replace("https://github.com/", "").rstrip("/")
            if final.lower() != slug.lower():
                return f"moved:{final}"
            return "ok"
    except urllib.error.HTTPError as e:
        return "dead" if e.code == 404 else "ok"
    except Exception:
        return "ok"  # network hiccup — don't false-flag

def audit_links():
    import concurrent.futures
    text = open(os.path.join(ROOT, "CATALOG.md"), encoding="utf-8").read()
    slugs = sorted(set(re.findall(r"github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+?)(?:\.git)?(?=[)\s\"'#/]|$)", text)))
    problems = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=24) as ex:
        for slug, res in zip(slugs, ex.map(check_repo, slugs)):
            if res != "ok":
                problems.append((slug, res))
    return problems, len(slugs)

# ---------------------------------------------------------------- L. staleness sweep
def audit_staleness(today=None):
    """Detector L (#65, REPORT-ONLY): flag evals whose **Last verified:** date is older
    than its category threshold (STALENESS_DAYS, keyed by Type) — fast-moving harnesses/
    MCP servers rot sooner than stable references. `today` is injectable for tests.
    Returns (stale, undated) where stale is a list of (name, type, date, age_days,
    threshold) and undated is the count of evals carrying no last-verified date."""
    today = today or datetime.date.today()
    stale, undated = [], 0
    for ev in load_evals():
        d = ev.last_verified
        if d is None:
            undated += 1
            continue
        threshold = STALENESS_DAYS.get(ev.type, DEFAULT_STALENESS_DAYS)
        age = (today - d).days
        if age > threshold:
            stale.append((ev.name, ev.type, d.isoformat(), age, threshold))
    return stale, undated

# ---------------------------------------------------------------- H. archived repos
# A catalogued repo that GitHub has flagged `archived` is no longer maintained — the
# entry shouldn't read as a live recommendation without saying so. Link rot (C) can't
# catch this: an archived repo's link still resolves. This is how 4 archived entries
# (incl. gpt-engineer ★55K and a same-named superseded chrome-devtools fork's cousin)
# were found. Opt-in (uses authenticated `gh api`, so not rate-limited), report-only:
# keep notable/historical tools but expect the entry to carry a ⚠️ archived note.
def check_archived(slug):
    r = subprocess.run(["gh", "api", f"repos/{slug}", "--jq", "[.archived, .pushed_at[0:7]]"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return None
    try:
        arch, pushed = json.loads(r.stdout)
        return (bool(arch), pushed)
    except Exception:
        return None

def audit_archived():
    import concurrent.futures
    text = open(os.path.join(ROOT, "CATALOG.md"), encoding="utf-8").read()
    slugs = sorted(set(re.findall(r"github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+?)(?:\.git)?(?=[)\s\"'#/]|$)", text)))
    archived = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as ex:
        for slug, res in zip(slugs, ex.map(check_archived, slugs)):
            if res and res[0]:
                # already disclosed in the entry? (a ⚠️ near the link)
                flagged = bool(re.search(re.escape(slug) + r".{0,400}?(?:archived|⚠️)", text, re.S | re.I))
                archived.append((slug, res[1], flagged))
    return archived, len(slugs)

# ---------------------------------------------------------------- D. verdict sync
# discovery-log (ADR 0001 / #69): a COMPARISON status for catalogued tools that were
# never exercised (Evidence REVIEW/SOURCE-ONLY) — leads, not verdicts. They are
# excluded from verdict-sync (D) and verdict-evidence (K): an eval's tentative
# CONDITIONAL read is the lead's notes, not a promoted verdict to enforce.
VERDICTS = ("ADOPT", "CONDITIONAL", "SKIP", "DEFER", "KEEP", "discovery-log")
_norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())

def audit_verdicts():
    """Flag evals whose ## Verdict disagrees with their COMPARISON.md row.
    Tolerates: KEEP (installed/validated status) vs ADOPT, and dual verdicts
    ("ADOPT for X — CONDITIONAL otherwise") where COMPARISON matches either."""
    comp = {}
    for line in open(os.path.join(ROOT, "COMPARISON.md"), encoding="utf-8"):
        m = re.match(r"\|\s*(.+?)\s*\|[^|]*\|[^|]*\|[^|]*\|\s*(ADOPT|CONDITIONAL|SKIP|DEFER|KEEP|discovery-log)\s*\|", line)
        if m:
            comp[_norm(m.group(1))] = m.group(2)
    compatible = {frozenset(("KEEP", "ADOPT"))}  # installed-tool status ~ adopt
    flagged = []
    for ev in load_evals():
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
    r"^\|\s*([^|]+?)\s*\|\s*(ADOPT|KEEP)\s*\|[^|]*\|\s*(yes|conditional|no)\s*\|\s*([^|]*?)\s*\|\s*$", re.M)

def _drift_key(name):
    """Normalize a tool name for cross-file matching: drop a parenthetical, then
    strip to alphanumerics. 'GSD (Get Shit Done)' and 'gsd' collapse to the same key."""
    return _norm(re.sub(r"\s*\(.*?\)", "", name))

def _comparison_verdict_map():
    comp = {}
    for line in open(os.path.join(ROOT, "COMPARISON.md"), encoding="utf-8"):
        m = re.match(r"\|\s*(.+?)\s*\|[^|]*\|[^|]*\|[^|]*\|\s*(ADOPT|CONDITIONAL|SKIP|DEFER|KEEP|discovery-log)\s*\|", line)
        if m:
            comp[_drift_key(m.group(1))] = m.group(2)
    return comp

def _stack_member_keys():
    """Tools recommended in STACK.md, keyed by BOTH link text and repo basename —
    so an entry installed under another name (GSD ← obra/superpowers) still matches."""
    txt = open(os.path.join(ROOT, "STACK.md"), encoding="utf-8").read()
    keys = set()
    for text, url in re.findall(r"\|\s*\[([^\]]+)\]\((https://github\.com/[^)]+)\)", txt):
        keys.add(_drift_key(text))
        keys.add(_norm(url.rstrip("/").split("/")[-1]))
    return keys

def audit_stack_drift():
    """Detector J: cross-check STACK.md against COMPARISON.md verdicts + the ledger.
    Flags: an ADOPT/KEEP tool absent from both STACK and the ledger; a ledger row whose
    verdict disagrees with COMPARISON; an excluded row with no reason; a ledger row
    marked in-STACK that isn't actually in STACK.md."""
    problems = []
    comp = _comparison_verdict_map()
    stack = _stack_member_keys()
    ledger_text = open(os.path.join(ROOT, "STACK-LEDGER.md"), encoding="utf-8").read()
    ledger_keys = {}
    for name, verdict, in_stack, reason in _LEDGER_ROW.findall(ledger_text):
        k = _drift_key(name)
        ledger_keys[k] = True
        if in_stack == "no" and not reason.strip():
            problems.append(f"ledger '{name}' is excluded (no) but records no reason")
        cv = comp.get(k)
        if cv and cv != verdict and frozenset((cv, verdict)) != frozenset(("KEEP", "ADOPT")):
            problems.append(f"ledger '{name}' verdict {verdict} != COMPARISON {cv}")
        if in_stack in ("yes", "conditional") and k not in stack:
            problems.append(f"ledger '{name}' marked '{in_stack}' but not found in STACK.md")
    for k, v in comp.items():
        if v in ("ADOPT", "KEEP") and k not in ledger_keys:
            problems.append(f"{v} tool '{k}' in COMPARISON is neither in STACK nor the exclusion ledger (#64)")
    return problems

# ---------------------------------------------------------------- K. verdict evidence gate
def audit_verdict_evidence():
    """Detector K (#71): a strong verdict can't rest on a README skim. An ADOPT/KEEP
    eval must be run-backed (Evidence MEASURED or RUN) OR carry an explicit honesty
    disclaimer in its 'How we tested' section (Evidence.honest — the documented escape
    hatch). A REVIEW/SOURCE-ONLY ADOPT/KEEP with no disclaimer is flagged. Generalizes
    the skills-only report-only detector E into a catalog-wide gate. Offline, gating."""
    flagged = []
    for ev in load_evals():
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
                      r"\*\*hands-on,? measured|run_eval", re.I)
# A strong, unambiguous measurement marker — strong enough to override a *weak*
# honest-review word (e.g. "inspected"/"read"/"examined") that would otherwise
# demote a genuinely measured eval. (Real case: a measured eval that wrote
# "inspected each SKILL.md" was wrongly held in the backlog because `\binspected\b`
# lives in HONEST. Sealing precedence here makes that a decision, not an accident.)
STRONG_MEASURED = re.compile(r"measured a/b|\ba/b\b|trigger rate|assertion (passed|failed)|"
                             r"\*\*hands-on,? measured|run_eval|tiktoken|measured ~", re.I)

# ------------------------------------------------------- declared evidence field
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
        return cls(os.path.basename(path)[:-3], open(path, encoding="utf-8").read())

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
    def is_skill(self):
        return bool(re.search(r"\|\s*\[[^\]]+\]\([^)]+\)\s*\|\s*skill\s*\|", self.text))

    @property
    def type(self):
        """The Type cell from the eval's catalog row (tool/skill/MCP server/…), or None."""
        m = re.search(r"\|\s*\[[^\]]+\]\([^)]+\)\s*\|\s*([^|]+?)\s*\|", self.text)
        return m.group(1).strip() if m else None

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

    @property
    def verdict(self):
        m = re.search(r"##\s*Verdict\s*\n+\s*\*\*(ADOPT|CONDITIONAL|SKIP|DEFER|KEEP)", self.text)
        return m.group(1) if m else None

    @property
    def verdict_set(self):
        # every verdict word in the Verdict section (handles dual verdicts)
        if not self.verdict:
            return set()
        vsec = re.search(r"##\s*Verdict.*?(?=\n##\s|\Z)", self.text, re.S)
        if vsec:
            return {w for w in VERDICTS if re.search(rf"\b{w}\b", vsec.group(0))}
        return {self.verdict}

    @property
    def name_aliases(self):
        # normalized names this eval might be keyed by in COMPARISON.md
        cands = {_norm(self.name)}
        h = re.search(r"^#\s*Evaluation:\s*(.+)$", self.text, re.M)
        if h: cands.add(_norm(h.group(1)))
        ce = re.search(r"\|\s*\[([^\]]+)\]\(https://github", self.text)
        if ce: cands.add(_norm(ce.group(1)))
        return cands

def load_evals():
    """Yield every Evaluation under evaluations/, skipping the template."""
    for p in sorted(glob.glob(os.path.join(ROOT, "evaluations/*.md"))):
        if os.path.basename(p) == "TEMPLATE.md":
            continue
        yield Evaluation.from_path(p)

def audit_evidence_field():
    """REPORT-ONLY: tally the declared **Evidence:** field across evals (issue #62),
    catalog-wide and within the ADOPT/KEEP set (issue #67 — "what % of ADOPT is
    MEASURED"). Returns (counts, missing, strong) where counts/strong are level->int
    over all evals / over ADOPT+KEEP evals, and missing lists evals with no field.
    Records how hard we looked, separate from the verdict; gating weak backing is #71."""
    counts = {lvl: 0 for lvl in EVIDENCE_LEVELS}
    strong = {lvl: 0 for lvl in EVIDENCE_LEVELS}  # restricted to ADOPT/KEEP-verdict evals
    missing = []
    for ev in load_evals():
        lvl = ev.evidence_level
        if lvl:
            counts[lvl] += 1
            if ev.verdict in ("ADOPT", "KEEP"):  # primary verdict, not every word mentioned
                strong[lvl] += 1
        else:
            missing.append(ev.name)
    return counts, missing, strong

def audit_skill_evidence():
    measured, backlog = [], []
    for ev in load_evals():
        if not ev.is_skill:
            continue  # not a skill-type entry
        if ev.verdict != "ADOPT":
            continue  # only ADOPT skills carry the "needs measured backing" bar
        # genuinely measured = has measurement evidence AND is not a disclosed not-run
        # review (which may merely quote the author's "with-skill" numbers).
        (measured if ev.evidence.is_measured else backlog).append(ev.name)
    return measured, backlog

# ---------------------------------------------------------------- F. dangling overlaps (report-only)
# Each entry's "Overlaps with" cell names peer tools. A token naming a tool that
# ISN'T itself catalogued is either a deliberate external/conceptual peer (the
# format allows this — e.g. "aider-style (ext.)") or a real gap: a notable tool we
# forgot to add. This is exactly how aider, continue, and agenta were found. The
# more rows reference the same uncatalogued token, the likelier it is a real gap.
# Report-only — surfaces candidates for human review; does not affect exit code.
_OVL_STRIP = lambda s: re.sub(r"\s*\(.*?\)", "", s).strip().lower()
_OVL_SKIP = ("complementary", "different", "approach", "same repo",
             "conceptual", "none", "—", "–")

def audit_overlaps():
    text = open(os.path.join(ROOT, "CATALOG.md"), encoding="utf-8").read()
    names, rows = set(), []
    for line in text.splitlines():
        m = re.match(r"\|\s*\[([^\]]+)\]\([^)]*\)\s*\|", line)
        if m:
            names.add(m.group(1).lower())
            names.add(_OVL_STRIP(m.group(1)))  # also the parenthetical-stripped form
            rows.append(line)
        else:  # unlinked entries like "| OMEGA | MCP server |"
            m2 = re.match(rf"\|\s*([A-Za-z0-9][\w.-]+)\s*\|\s*{catalog_lib.ROW_TYPE}\s*\|", line)
            if m2:
                names.add(m2.group(1).lower())
    from collections import Counter
    miss = Counter()
    for line in rows:
        cells = line.split("|")
        if len(cells) < 6:
            continue
        for tok in cells[-2].split(","):  # the "Overlaps with" cell
            t = _OVL_STRIP(tok)
            tl = tok.lower()
            if (not t or "ext." in tl or "=" in tok or ";" in tok
                    or tok.count("(") != tok.count(")")  # mid-parenthetical fragment
                    or len(t) > 22 or len(t.split()) > 2
                    or any(x in tl for x in _OVL_SKIP)):
                continue  # external/conceptual peer or prose fragment, not a gap
            if t not in names:
                miss[t] += 1
    return miss.most_common()

# ---------------------------------------------------------------- M. clusters without a pick (report-only)
# ADR 0001 / #69: when several catalogued tools solve the same problem (an overlap
# cluster), the catalog should name ONE best-in-class ADOPT pick rather than hedge
# CONDITIONAL on all of them. This report surfaces overlap clusters (connected via
# the "Overlaps with" graph) where NO member is ADOPT/KEEP yet at least one is
# CONDITIONAL — i.e. clusters still awaiting a pick. Report-only; it makes the #69
# migration findable, it does not migrate anything.
def audit_clusters():
    text = open(os.path.join(ROOT, "CATALOG.md"), encoding="utf-8").read()
    # name -> set(overlap peers), restricted to catalogued names
    cat_names, edges = set(), {}
    for line in text.splitlines():
        m = re.match(r"\|\s*\[([^\]]+)\]\([^)]*\)\s*\|", line)
        if not m:
            continue
        nm = _OVL_STRIP(m.group(1))
        cat_names.add(nm)
        cells = line.split("|")
        peers = []
        if len(cells) >= 6:
            for tok in cells[-2].split(","):
                t = _OVL_STRIP(tok)
                if t and "ext." not in tok.lower() and len(t.split()) <= 2:
                    peers.append(t)
        edges[nm] = peers
    # verdict per name from COMPARISON
    verd = {}
    for line in open(os.path.join(ROOT, "COMPARISON.md"), encoding="utf-8"):
        m = re.match(r"\|\s*(.+?)\s*\|[^|]*\|[^|]*\|[^|]*\|\s*(ADOPT|CONDITIONAL|SKIP|DEFER|KEEP|discovery-log)\s*\|", line)
        if m:
            verd[_OVL_STRIP(m.group(1))] = m.group(2)
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
        verds = {verd.get(m) for m in members}
        has_pick = "ADOPT" in verds or "KEEP" in verds
        awaiting = "CONDITIONAL" in verds or "discovery-log" in verds
        if awaiting and not has_pick:
            flagged.append(sorted(members))
    return sorted(flagged, key=lambda c: (-len(c), c[0].lower()))

# ---------------------------------------------------------------- G. comparison consistency
# COMPARISON.md mirrors CATALOG.md: its per-stage summary must sum to its own body
# rows, and its Total must equal the CATALOG entry count. Manual count edits drift
# easily (a single tool addition touches both files), and nothing else cross-checks
# them — so a CATALOG/COMPARISON disagreement could ship silently. Gating, offline.
def _catalog_count():
    return catalog_lib.catalog_count(open(os.path.join(ROOT, "CATALOG.md"), encoding="utf-8").read())

def audit_comparison():
    text = open(os.path.join(ROOT, "COMPARISON.md"), encoding="utf-8").read()
    body = catalog_lib.comparison_body_counts(text)  # shared with reconcile-counts.py
    summary, in_summary = {}, False
    for l in text.splitlines():       # second pass: the Summary table only
        hm = re.match(r"^##\s+(.*)", l)
        if hm:
            in_summary = hm.group(1).strip().lower() == "summary"
            continue
        if in_summary:
            sm = re.match(r"\|\s*(.+?)\s*\|\s*(\d+)\s*\|", l)
            if sm and sm.group(1).strip().replace("**", "").lower() not in ("stage", "total"):
                summary[sm.group(1).strip().replace("**", "")] = int(sm.group(2))
    problems = []
    for s, cnt in summary.items():
        if body.get(s, 0) != cnt:
            problems.append(f"section '{s}': summary says {cnt}, body has {body.get(s, 0)}")
    mtot = re.search(r"\|\s*\*\*Total\*\*\s*\|\s*\*\*(\d+)\*\*", text)
    total = int(mtot.group(1)) if mtot else None
    body_total = sum(body.values())
    if total is not None and total != body_total:
        problems.append(f"Total says {total}, body rows sum to {body_total}")
    cat = _catalog_count()
    if total is not None and total != cat:
        problems.append(f"COMPARISON Total {total} != CATALOG.md {cat} entries")
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
    # declared Evidence field (issue #62)
    eviz = Evaluation("ev", "## How we tested it\n\n**Evidence:** MEASURED\n\nran it live.\n")
    expect(eviz.evidence_level == "MEASURED", f"evidence_level {eviz.evidence_level!r} != MEASURED")
    src = Evaluation("sv", "**Evidence:** SOURCE-ONLY\n")
    expect(src.evidence_level == "SOURCE-ONLY", f"hyphenated level {src.evidence_level!r} != SOURCE-ONLY")
    expect(none.evidence_level is None, "absent Evidence field not None")
    n_eval_checks = 9

    if fails:
        print("== selftest ==")
        print("\n".join(fails))
        return 1
    print(f"== selftest ==\n  OK — {len(cases)} evidence + {len(level_cases)} level + {n_eval_checks} eval-parsing cases pass")
    return 0

# ---------------------------------------------------------------- main
def main():
    args = sys.argv[1:]
    if "--selftest" in args:
        sys.exit(selftest())
    sel = [a for a in args if a in ("--installs", "--fabrication", "--links", "--archived", "--verdicts", "--comparison", "--drift", "--verdict-evidence", "--skills", "--overlaps", "--clusters", "--evidence", "--staleness", "--offline")]
    explicit = [a for a in sel if a != "--offline"]
    do_inst = (not explicit) or "--installs" in sel
    do_fab  = (not explicit) or "--fabrication" in sel or "--offline" in sel
    do_verd = (not explicit) or "--verdicts" in sel  # offline, fast
    do_comp = (not explicit) or "--comparison" in sel or "--offline" in sel  # offline gate
    do_drift = (not explicit) or "--drift" in sel or "--offline" in sel  # offline gate (#70)
    do_vev = (not explicit) or "--verdict-evidence" in sel or "--offline" in sel  # offline gate (#71)
    do_links = "--links" in sel   # opt-in: ~450 network requests, slow
    do_archived = "--archived" in sel  # opt-in: ~450 gh-api calls; report-only
    do_skills = "--skills" in sel  # opt-in report (does not affect exit code)
    do_overlaps = "--overlaps" in sel  # opt-in report (does not affect exit code)
    do_clusters = "--clusters" in sel  # opt-in report (does not affect exit code)
    do_evidence = "--evidence" in sel  # opt-in report (does not affect exit code)
    do_staleness = "--staleness" in sel  # opt-in report (does not affect exit code)
    if "--offline" in sel: do_inst = False
    if explicit:
        do_inst = "--installs" in sel
        do_fab  = "--fabrication" in sel
        do_verd = "--verdicts" in sel
        do_comp = "--comparison" in sel
        do_drift = "--drift" in sel
        do_vev = "--verdict-evidence" in sel

    rc = 0
    if do_inst:
        print("== A. install resolver ==")
        broken = audit_installs()
        if broken:
            rc = 1
            for rel, kind, pkg in broken:
                print(f"  BROKEN [{kind}] {pkg}  ({rel})")
        else:
            print("  OK — all checked install targets resolve")
    if do_fab:
        print("== B. fabrication classifier ==")
        flagged = audit_fabrication()
        if flagged:
            rc = 1
            print(f"  REVIEW ({len(flagged)}): a 'How we tested' that claims a run with no honesty disclaimer")
            for b in flagged:
                print(f"    - {b}")
        else:
            print("  OK — every 'How we tested' either discloses not-run or shows a verified run")
    if do_verd:
        print("== D. verdict sync (eval ## Verdict vs COMPARISON.md) ==")
        vflag = audit_verdicts()
        if vflag:
            rc = 1
            for name, ev, cv in vflag:
                print(f"  MISMATCH {name}: eval={ev}  COMPARISON={cv}")
        else:
            print("  OK — eval verdicts agree with COMPARISON (dual verdicts & KEEP tolerated)")
    if do_comp:
        print("== G. comparison consistency (COMPARISON.md vs CATALOG.md) ==")
        cprob = audit_comparison()
        if cprob:
            rc = 1
            for p in cprob:
                print(f"  DRIFT {p}")
        else:
            print("  OK — COMPARISON summary sums to its body rows and Total matches CATALOG.md")
    if do_drift:
        print("== J. stack-derivation drift (STACK.md vs verdicts + ledger) ==")
        dprob = audit_stack_drift()
        if dprob:
            rc = 1
            for p in dprob:
                print(f"  DRIFT {p}")
        else:
            print("  OK — every ADOPT/KEEP tool is in STACK or the ledger; STACK & ledger agree with verdicts")
    if do_vev:
        print("== K. verdict evidence (ADOPT/KEEP must be run-backed or disclaimered) ==")
        vev = audit_verdict_evidence()
        if vev:
            rc = 1
            for name, verd, lvl in vev:
                print(f"  WEAK {name}: {verd} backed only by {lvl} and no honesty disclaimer "
                      f"(graduate the eval to MEASURED/RUN, or add a not-run disclaimer)")
        else:
            print("  OK — every ADOPT/KEEP eval is run-backed (MEASURED/RUN) or carries a disclaimer")
    if do_links:
        print("== C. link rot (CATALOG.md repo links) ==")
        problems, total = audit_links()
        if problems:
            rc = 1
            for slug, res in problems:
                print(f"  {'DEAD' if res=='dead' else 'MOVED'} {slug}" + (f" -> {res[6:]}" if res.startswith('moved:') else ""))
        else:
            print(f"  OK — all {total} catalog repo links resolve to their canonical names")
    if do_archived:
        print("== H. archived repos (report-only) ==")
        arch, total = audit_archived()
        undisclosed = [(s, p) for s, p, flagged in arch if not flagged]
        for s, p, flagged in arch:
            tag = "" if flagged else "  <- NOT disclosed in the entry; add a ⚠️ archived note or repoint"
            print(f"  ARCHIVED {s} (last push {p}){tag}")
        if not arch:
            print(f"  OK — none of {total} catalog repos are archived")
        elif not undisclosed:
            print(f"  ({len(arch)} archived, all already disclosed with a ⚠️ note)")
    if do_skills:
        measured, backlog = audit_skill_evidence()
        tot = len(measured) + len(backlog)
        print(f"== E. skill evidence (report-only) — {len(measured)}/{tot} ADOPT skills have measured backing ==")
        for n in measured:
            print(f"  MEASURED {n}")
        for n in backlog:
            print(f"  backlog  {n}  (ADOPT skill, review-based — would benefit from a measured A/B; see TEMPLATE.md)")
    if do_evidence:
        counts, missing, strong = audit_evidence_field()
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
        stale, undated = audit_staleness()
        print(f"== L. staleness sweep (report-only) — {len(stale)} stale eval(s), {undated} undated ==")
        for name, typ, d, age, thr in sorted(stale, key=lambda r: -r[3]):
            print(f"  STALE {name} ({typ}) last verified {d} — {age}d old > {thr}d threshold")
        if not stale:
            print("  OK — no dated eval is past its category staleness threshold")
        if undated:
            print(f"  ({undated} evals carry no **Last verified:** date yet — add one when you re-check them)")
    if do_overlaps:
        gaps = audit_overlaps()
        strong = [(t, c) for t, c in gaps if c >= 2]
        print(f"== F. dangling overlaps (report-only) — {len(gaps)} uncatalogued peer tokens ==")
        if not gaps:
            print("  OK — every 'Overlaps with' token resolves to a catalog entry")
        for t, c in strong:
            print(f"  GAP?  {t}  ({c} refs — likely a notable tool missing from the catalog)")
        for t, c in gaps:
            if c < 2:
                print(f"  maybe {t}  ({c} ref — check: real gap or external/conceptual peer)")
    if do_clusters:
        cl = audit_clusters()
        print(f"== M. clusters without a pick (report-only, #69) — {len(cl)} overlap cluster(s) all-CONDITIONAL, no ADOPT/KEEP pick ==")
        if not cl:
            print("  OK — every overlap cluster with a CONDITIONAL member also has an ADOPT/KEEP pick")
        for members in cl:
            print(f"  PICK?  {' / '.join(members)}")
    sys.exit(rc)

if __name__ == "__main__":
    main()
