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

Usage:
  python3 audit-evals.py              # both detectors, network checks on
  python3 audit-evals.py --offline    # classifier only (no registry/network calls)
  python3 audit-evals.py --installs   # install resolver only
  python3 audit-evals.py --fabrication # classifier only

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
        if HONEST.search(sec) or VERIFIED.search(sec):
            continue  # honest review or genuine hands-on
        if RUN_CLAIM.search(sec):
            flagged.append(os.path.basename(p)[:-3])
    return flagged

# ---------------------------------------------------------------- main
def main():
    args = sys.argv[1:]
    do_inst = not args or "--installs" in args
    do_fab  = not args or "--fabrication" in args or "--offline" in args
    if "--offline" in args: do_inst = False
    if "--installs" in args: do_fab = False
    if "--fabrication" in args: do_inst = False

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
    sys.exit(rc)

if __name__ == "__main__":
    main()
