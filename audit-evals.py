#!/usr/bin/env python3
"""
audit-evals.py — integrity checks for the ai-tooling catalog.

Two detectors, both proven to catch real problems (see git history, 2026-06-20):

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

Usage:
  python3 audit-evals.py              # A + B + D (D/B offline; A hits registries)
  python3 audit-evals.py --offline    # B + D only (no network)
  python3 audit-evals.py --installs   # install resolver only
  python3 audit-evals.py --fabrication # fabrication classifier only
  python3 audit-evals.py --verdicts   # verdict-sync only (offline)
  python3 audit-evals.py --links      # link-rot sweep only (slow, ~450 requests)
  python3 audit-evals.py --skills     # skill-evidence backlog report (offline)
  python3 audit-evals.py --selftest   # unit-test the evidence classifier (offline)

Exit code is non-zero if any BROKEN install or FABRICATION candidate is found,
so it can gate CI or a pre-commit hook.
"""
import os, re, sys, json, glob, subprocess, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.abspath(__file__))
TIMEOUT = 15

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
    for p in sorted(glob.glob(os.path.join(ROOT, "evaluations/*.md"))):
        if os.path.basename(p) == "TEMPLATE.md": continue
        sec = how_section(open(p, encoding="utf-8").read())
        if not sec: continue
        if Evidence(sec).is_fabrication_candidate:
            flagged.append(os.path.basename(p)[:-3])
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

# ---------------------------------------------------------------- D. verdict sync
VERDICTS = ("ADOPT", "CONDITIONAL", "SKIP", "DEFER", "KEEP")
_norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())

def audit_verdicts():
    """Flag evals whose ## Verdict disagrees with their COMPARISON.md row.
    Tolerates: KEEP (installed/validated status) vs ADOPT, and dual verdicts
    ("ADOPT for X — CONDITIONAL otherwise") where COMPARISON matches either."""
    comp = {}
    for line in open(os.path.join(ROOT, "COMPARISON.md"), encoding="utf-8"):
        m = re.match(r"\|\s*(.+?)\s*\|[^|]*\|[^|]*\|[^|]*\|\s*(ADOPT|CONDITIONAL|SKIP|DEFER|KEEP)\s*\|", line)
        if m:
            comp[_norm(m.group(1))] = m.group(2)
    compatible = {frozenset(("KEEP", "ADOPT"))}  # installed-tool status ~ adopt
    flagged = []
    for p in sorted(glob.glob(os.path.join(ROOT, "evaluations/*.md"))):
        if os.path.basename(p) == "TEMPLATE.md": continue
        t = open(p, encoding="utf-8").read()
        vm = re.search(r"##\s*Verdict\s*\n+\s*\*\*(ADOPT|CONDITIONAL|SKIP|DEFER|KEEP)", t)
        if not vm: continue
        ev = vm.group(1)
        # dual verdicts: collect every verdict word in the Verdict section
        vsec = re.search(r"##\s*Verdict.*?(?=\n##\s|\Z)", t, re.S)
        ev_set = {w for w in VERDICTS if re.search(rf"\b{w}\b", vsec.group(0))} if vsec else {ev}
        cands = {_norm(os.path.basename(p)[:-3])}
        h = re.search(r"^#\s*Evaluation:\s*(.+)$", t, re.M)
        if h: cands.add(_norm(h.group(1)))
        ce = re.search(r"\|\s*\[([^\]]+)\]\(https://github", t)
        if ce: cands.add(_norm(ce.group(1)))
        cv = next((comp[c] for c in cands if c in comp), None)
        if cv is None:
            continue  # name didn't map — not a verdict-sync problem
        if cv in ev_set:
            continue  # matches (incl. dual verdict)
        if any(frozenset((cv, x)) in compatible for x in ev_set):
            continue  # KEEP vs ADOPT etc.
        flagged.append((os.path.basename(p)[:-3], ev, cv))
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

# ---------------------------------------------------------------- evidence seam
class Evidence:
    """Evidentiary status of an eval's 'How we tested' section.

    The HONEST / VERIFIED / RUN_CLAIM / MEASURED regexes are consumed only here,
    so the precedence between them is decided in ONE place instead of being
    recombined differently inside each detector. The interface is the test
    surface — see selftest()."""
    def __init__(self, how):
        self.honest    = bool(HONEST.search(how))
        self.verified  = bool(VERIFIED.search(how))
        self.run_claim = bool(RUN_CLAIM.search(how))
        self.measured  = bool(MEASURED.search(how))
        self._strong   = bool(STRONG_MEASURED.search(how))

    @property
    def is_fabrication_candidate(self):
        # claims a specific run, with no honesty disclaimer and no genuine-run marker
        return self.run_claim and not (self.honest or self.verified)

    @property
    def is_measured(self):
        # measured evidence present, and either no honest-not-run disclaimer OR a
        # strong measurement marker that overrides a weak disclaimer word
        return self.measured and (self._strong or not self.honest)

def audit_skill_evidence():
    measured, backlog = [], []
    for p in sorted(glob.glob(os.path.join(ROOT, "evaluations/*.md"))):
        if os.path.basename(p) == "TEMPLATE.md": continue
        t = open(p, encoding="utf-8").read()
        if not re.search(r"\|\s*\[[^\]]+\]\([^)]+\)\s*\|\s*skill\s*\|", t):
            continue  # not a skill-type entry
        vm = re.search(r"##\s*Verdict\s*\n+\s*\*\*(ADOPT|CONDITIONAL|SKIP|DEFER|KEEP)", t)
        if not vm or vm.group(1) != "ADOPT":
            continue  # only ADOPT skills carry the "needs measured backing" bar
        name = os.path.basename(p)[:-3]
        # genuinely measured = has measurement evidence AND is not a disclosed not-run
        # review (which may merely quote the author's "with-skill" numbers).
        (measured if Evidence(how_section(t)).is_measured else backlog).append(name)
    return measured, backlog

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
    if fails:
        print("== selftest ==")
        print("\n".join(fails))
        return 1
    print(f"== selftest ==\n  OK — {len(cases)} evidence-classification cases pass")
    return 0

# ---------------------------------------------------------------- main
def main():
    args = sys.argv[1:]
    if "--selftest" in args:
        sys.exit(selftest())
    sel = [a for a in args if a in ("--installs", "--fabrication", "--links", "--verdicts", "--skills", "--offline")]
    explicit = [a for a in sel if a != "--offline"]
    do_inst = (not explicit) or "--installs" in sel
    do_fab  = (not explicit) or "--fabrication" in sel or "--offline" in sel
    do_verd = (not explicit) or "--verdicts" in sel  # offline, fast
    do_links = "--links" in sel   # opt-in: ~450 network requests, slow
    do_skills = "--skills" in sel  # opt-in report (does not affect exit code)
    if "--offline" in sel: do_inst = False
    if explicit:
        do_inst = "--installs" in sel
        do_fab  = "--fabrication" in sel
        do_verd = "--verdicts" in sel

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
    if do_links:
        print("== C. link rot (CATALOG.md repo links) ==")
        problems, total = audit_links()
        if problems:
            rc = 1
            for slug, res in problems:
                print(f"  {'DEAD' if res=='dead' else 'MOVED'} {slug}" + (f" -> {res[6:]}" if res.startswith('moved:') else ""))
        else:
            print(f"  OK — all {total} catalog repo links resolve to their canonical names")
    if do_skills:
        measured, backlog = audit_skill_evidence()
        tot = len(measured) + len(backlog)
        print(f"== E. skill evidence (report-only) — {len(measured)}/{tot} ADOPT skills have measured backing ==")
        for n in measured:
            print(f"  MEASURED {n}")
        for n in backlog:
            print(f"  backlog  {n}  (ADOPT skill, review-based — would benefit from a measured A/B; see TEMPLATE.md)")
    sys.exit(rc)

if __name__ == "__main__":
    main()
