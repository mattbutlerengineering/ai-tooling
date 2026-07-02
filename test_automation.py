#!/usr/bin/env python3
"""
test_automation.py — characterization tests for the count/sync automation:
reconcile-counts.py, audit-evals.py detector G (audit_comparison), and
sync-plugin-docs.sh.

These pin the CURRENT correct behavior so the planned shared-parser refactor
(issue #45) has a regression net. They never touch the real CATALOG.md /
COMPARISON.md / plugin/ — every test runs against fixtures in a temp dir, either
by monkeypatching a module's ROOT or by copying the script into a fixture tree.

Run:
  python3 -m unittest test_automation -v      # or: python3 test_automation.py
Exits non-zero on any failure (gates CI / pre-commit).
"""
import os, datetime, importlib.util, shutil, subprocess, tempfile, unittest

ROOT = os.path.dirname(os.path.abspath(__file__))


def _load(mod_name, filename):
    """Import a repo script by path (filenames are hyphenated, not importable)."""
    spec = importlib.util.spec_from_file_location(mod_name, os.path.join(ROOT, filename))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


catalog_lib = _load("catalog_lib", "catalog_lib.py")
reconcile = _load("reconcile_counts", "reconcile-counts.py")
audit = _load("audit_evals", "audit-evals.py")
backfill = _load("backfill_evidence", "backfill-evidence.py")
tier = _load("tier_stack", "tier-stack.py")


# ----------------------------------------------------------------- fixtures
# A small but structurally faithful pair. Body: Plan=2 (a tool, b skill),
# Ship=1 (c tool) -> 3 rows. Summary mirrors that; Total 3; CATALOG has 3 rows.
CATALOG_OK = """# Catalog

## Plan

| Name | Type | One-liner | Problem | Overlaps with |
|------|------|-----------|---------|---------------|
| [a](https://github.com/x/a) | tool | one | two | none |
| [b](https://github.com/x/b) | skill | one | two | none |
| [c](https://github.com/x/c) | tool | one | two | none |
"""

COMPARISON_OK = """# Tool Comparison

All 3 tools from CATALOG.md at a glance.

## Plan

| Tool | Type | Auto | Free | Evaluated |
|------|------|------|------|-----------|
| a | tool | | ✓ | ADOPT |
| b | skill | | ✓ | SKIP |

## Ship

| Tool | Type | Auto | Free | Evaluated |
|------|------|------|------|-----------|
| c | tool | | ✓ | KEEP |

## Summary

| Stage | Tools | Evaluated | Adoption rate |
|-------|-------|-----------|---------------|
| Plan | 2 | 2 | 100% |
| Ship | 1 | 1 | 100% |
| **Total** | **3** | **3** | **100%** |
"""


def _write(d, name, text):
    p = os.path.join(d, name)
    os.makedirs(os.path.dirname(p), exist_ok=True) if os.path.dirname(name) else None
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)
    return p


# ----------------------------------------------------------------- reconcile: pure fns
class TestReconcilePureFns(unittest.TestCase):
    def test_fix_total_strings_each_pattern(self):
        cases = {
            "An inventory of 99 tools here.": "An inventory of 3 tools here.",
            "There are 99 catalog entries.": "There are 3 catalog entries.",
            "Now 99 tools are cataloged.": "Now 3 tools are cataloged.",
            "distilled from 99 catalog entries": "distilled from 3 catalog entries",
        }
        for src, want in cases.items():
            self.assertEqual(reconcile.fix_total_strings(src, 3), want, msg=src)

    def test_fix_total_strings_noop_when_correct(self):
        s = "An inventory of 3 tools."
        self.assertEqual(reconcile.fix_total_strings(s, 3), s)

    def test_comparison_body_counts(self):
        self.assertEqual(reconcile.comparison_body_counts(COMPARISON_OK), {"Plan": 2, "Ship": 1})

    def test_fix_comparison_rebuilds_summary_and_header(self):
        broken = COMPARISON_OK.replace("| Plan | 2 | 2 |", "| Plan | 9 | 9 |") \
                              .replace("All 3 tools", "All 99 tools")
        fixed = reconcile.fix_comparison(broken, 3)
        self.assertIn("| Plan | 2 | 2 | 100% |", fixed)
        self.assertIn("All 3 tools from CATALOG.md", fixed)

    def test_fix_comparison_fixes_total_row(self):
        # Regression test for the historical bug: the bolded **Total** row was
        # not rewritten because section and Total shared one regex.
        broken = COMPARISON_OK.replace("| **Total** | **3** | **3** |",
                                       "| **Total** | **99** | **99** |")
        fixed = reconcile.fix_comparison(broken, 3)
        self.assertIn("| **Total** | **3** | **3** | **100%** |", fixed)
        self.assertNotIn("**99**", fixed)


# ----------------------------------------------------------------- catalog_lib: github_repos
class TestCatalogLibGithubRepos(unittest.TestCase):
    """Pins catalog_lib.github_repos() — the shared github.com/owner/repo slug
    extractor that audit-evals' link-rot and archived detectors route through
    (#113). Returns sorted, de-duplicated slugs."""

    def test_extracts_from_markdown_link(self):
        self.assertEqual(catalog_lib.github_repos("| [a](https://github.com/x/a) |"), ["x/a"])

    def test_strips_dot_git_suffix(self):
        self.assertEqual(catalog_lib.github_repos("see https://github.com/foo/bar.git for more"), ["foo/bar"])

    def test_stops_at_delimiters(self):
        # closing paren, whitespace, quote, hash, slash, and end-of-string all bound the slug
        for text in ('(https://github.com/foo/bar)', 'https://github.com/foo/bar ',
                     '"https://github.com/foo/bar"', 'https://github.com/foo/bar#readme',
                     'https://github.com/foo/bar/tree/main', 'https://github.com/foo/bar'):
            self.assertEqual(catalog_lib.github_repos(text), ["foo/bar"], msg=text)

    def test_dedupes_and_sorts(self):
        text = "https://github.com/z/z https://github.com/a/a https://github.com/z/z"
        self.assertEqual(catalog_lib.github_repos(text), ["a/a", "z/z"])

    def test_no_match_returns_empty(self):
        self.assertEqual(catalog_lib.github_repos("no links here"), [])

    def test_matches_legacy_inline_regex(self):
        # Equivalence to the regex the two detectors used before extraction.
        # This copy is the frozen baseline (the extraction's oracle), NOT a second
        # source of truth — if _GITHUB_SLUG legitimately changes, update it here too.
        import re
        legacy = lambda t: sorted(set(re.findall(
            r"github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+?)(?:\.git)?(?=[)\s\"'#/]|$)", t)))
        with open(os.path.join(ROOT, "CATALOG.md"), encoding="utf-8") as f:
            sample = f.read()
        self.assertEqual(catalog_lib.github_repos(sample), legacy(sample))


# ----------------------------------------------------------------- reconcile: catalog_count + main (subprocess)
class TestReconcileMain(unittest.TestCase):
    def _fixture_repo(self, d, catalog=CATALOG_OK, readme="An inventory of 3 tools.\n\nThere are 3 catalog entries.\n"):
        shutil.copy(os.path.join(ROOT, "reconcile-counts.py"), os.path.join(d, "reconcile-counts.py"))
        shutil.copy(os.path.join(ROOT, "catalog_lib.py"), os.path.join(d, "catalog_lib.py"))  # reconcile imports it
        _write(d, "CATALOG.md", catalog)
        _write(d, "COMPARISON.md", COMPARISON_OK)
        _write(d, "README.md", readme)
        _write(d, "CLAUDE.md", "An inventory of 3 tools.\n")
        _write(d, "STACK.md", "distilled from 3 catalog entries\n")
        _write(d, "plugin/CLAUDE.md", "An inventory of 3 tools.\n")

    def _run(self, d, *args):
        return subprocess.run(["python3", "reconcile-counts.py", *args],
                              cwd=d, capture_output=True, text=True)

    def test_catalog_count_via_monkeypatched_root(self):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "CATALOG.md", CATALOG_OK)
            orig = reconcile.ROOT
            try:
                reconcile.ROOT = d
                self.assertEqual(reconcile.catalog_count(), 3)
            finally:
                reconcile.ROOT = orig

    def test_check_clean_exits_zero(self):
        with tempfile.TemporaryDirectory() as d:
            self._fixture_repo(d)
            r = self._run(d, "--check")
            self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)

    def test_check_drift_exits_nonzero(self):
        with tempfile.TemporaryDirectory() as d:
            self._fixture_repo(d, readme="An inventory of 99 tools.\n")
            r = self._run(d, "--check")
            self.assertEqual(r.returncode, 1, msg=r.stdout + r.stderr)

    def test_apply_is_idempotent(self):
        with tempfile.TemporaryDirectory() as d:
            self._fixture_repo(d, readme="An inventory of 99 tools.\n")
            first = self._run(d)                 # applies the fix
            self.assertEqual(first.returncode, 0, msg=first.stdout + first.stderr)
            second = self._run(d, "--check")     # nothing left to change
            self.assertEqual(second.returncode, 0, msg=second.stdout + second.stderr)


# ----------------------------------------------------------------- detector G (audit_comparison)
class TestDetectorG(unittest.TestCase):
    def _run_audit(self, catalog, comparison):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "CATALOG.md", catalog)
            _write(d, "COMPARISON.md", comparison)
            orig = audit.ROOT
            try:
                audit.ROOT = d
                return audit.audit_comparison()
            finally:
                audit.ROOT = orig

    def test_consistent_fixture_has_no_problems(self):
        self.assertEqual(self._run_audit(CATALOG_OK, COMPARISON_OK), [])

    def test_section_sum_mismatch(self):
        bad = COMPARISON_OK.replace("| Plan | 2 | 2 |", "| Plan | 5 | 5 |")
        problems = self._run_audit(CATALOG_OK, bad)
        self.assertTrue(any("section 'Plan'" in p for p in problems), msg=str(problems))

    def test_total_vs_body_mismatch(self):
        # Total says 9 but body sums to 3. CATALOG also 9 rows so the catalog
        # check passes and the body-total mismatch is isolated.
        catalog9 = CATALOG_OK + "".join(
            f"| [d{i}](https://github.com/x/d{i}) | tool | o | t | none |\n" for i in range(6))
        bad = COMPARISON_OK.replace("| **Total** | **3** | **3** |", "| **Total** | **9** | **9** |")
        problems = self._run_audit(catalog9, bad)
        self.assertTrue(any("body rows sum to 3" in p for p in problems), msg=str(problems))

    def test_comparison_vs_catalog_mismatch(self):
        catalog2 = "\n".join(CATALOG_OK.splitlines()[:-1]) + "\n"  # drop last row -> 2 entries
        problems = self._run_audit(catalog2, COMPARISON_OK)
        self.assertTrue(any("!= CATALOG.md 2 entries" in p for p in problems), msg=str(problems))


# ----------------------------------------------------------------- sync-plugin-docs.sh
def _sync_fixture_tree(d):
    """A minimal repo tree with every synced doc/dir, for exercising sync-plugin-docs.sh."""
    shutil.copy(os.path.join(ROOT, "sync-plugin-docs.sh"), os.path.join(d, "sync-plugin-docs.sh"))
    _write(d, "CATALOG.md", CATALOG_OK)
    _write(d, "WORKFLOW.md", "# Workflow\n")
    _write(d, "STACK.md", "# Stack\n")
    _write(d, "STACK-LEDGER.md", "# Stack Ledger\n")
    _write(d, "evaluations/foo.md", "# eval foo\n")
    _write(d, "discovery/bar.md", "# discovery bar\n")
    _write(d, "methodologies/baz.md", "# methodology baz\n")
    _write(d, "plugin/skills/myskill/SKILL.md",
           "See ${CLAUDE_PLUGIN_ROOT}/docs/CATALOG.md for the catalog.\n")


class TestSyncPluginDocs(unittest.TestCase):
    def _fixture_tree(self, d):
        _sync_fixture_tree(d)

    def _run(self, d, *args):
        return subprocess.run(["bash", "sync-plugin-docs.sh", *args], cwd=d, capture_output=True, text=True)

    def test_happy_path_roundtrips_and_passes_guard(self):
        with tempfile.TemporaryDirectory() as d:
            self._fixture_tree(d)
            r = self._run(d)
            self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)
            # docs mirrored
            self.assertTrue(os.path.exists(os.path.join(d, "plugin/docs/CATALOG.md")))
            self.assertTrue(os.path.exists(os.path.join(d, "plugin/docs/evaluations/foo.md")))
            self.assertTrue(os.path.exists(os.path.join(d, "plugin/docs/discovery/bar.md")))
            self.assertTrue(os.path.exists(os.path.join(d, "plugin/docs/methodologies/baz.md")))

    def test_strips_plugin_root_prefix_in_root_skills(self):
        # The sed strips the whole "${CLAUDE_PLUGIN_ROOT}/docs/" prefix, so a
        # "${CLAUDE_PLUGIN_ROOT}/docs/CATALOG.md" reference becomes "CATALOG.md".
        with tempfile.TemporaryDirectory() as d:
            self._fixture_tree(d)
            self._run(d)
            with open(os.path.join(d, "skills/myskill/SKILL.md"), encoding="utf-8") as f:
                out = f.read()
            self.assertNotIn("${CLAUDE_PLUGIN_ROOT}", out)
            self.assertIn("See CATALOG.md for the catalog.", out)

    def test_stale_plugin_docs_reconciled_by_delete(self):
        # rsync --delete should remove a plugin/docs eval with no root counterpart,
        # leaving counts equal so the script's verification guard passes (exit 0).
        with tempfile.TemporaryDirectory() as d:
            self._fixture_tree(d)
            _write(d, "plugin/docs/evaluations/stale.md", "# orphan\n")
            r = self._run(d)
            self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)
            self.assertFalse(os.path.exists(os.path.join(d, "plugin/docs/evaluations/stale.md")))

    def test_check_passes_when_in_sync_and_mutates_nothing(self):
        # After an apply, --check must exit 0 and leave plugin/docs/ byte-for-byte unchanged.
        with tempfile.TemporaryDirectory() as d:
            self._fixture_tree(d)
            self.assertEqual(self._run(d).returncode, 0)
            cat = os.path.join(d, "plugin/docs/CATALOG.md")
            before = open(cat, encoding="utf-8").read()
            r = self._run(d, "--check")
            self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)
            self.assertEqual(open(cat, encoding="utf-8").read(), before, "check mutated plugin/docs")

    def test_check_fails_on_drift(self):
        # A stale plugin/docs copy (root doc changed but not re-synced) must fail --check.
        with tempfile.TemporaryDirectory() as d:
            self._fixture_tree(d)
            self.assertEqual(self._run(d).returncode, 0)
            _write(d, "CATALOG.md", CATALOG_OK + "\n| [new](https://github.com/a/new) | tool | x | y | z |\n")
            r = self._run(d, "--check")
            self.assertEqual(r.returncode, 1, msg="drift not detected: " + r.stdout + r.stderr)


# ----------------------------------------------------------------- watch-list seam (#194)
# Driver for exercising the real opencode plugin under bun: fires edit events at a
# fixture worktree and exits non-zero if a watched entry fails to sync (or an
# unwatched one triggers). argv: <worktree> <plugin-path>
_OPENCODE_DRIVER = """
import { $ } from "bun"
import { existsSync } from "node:fs"
import { join } from "node:path"
const [worktree, pluginPath] = Bun.argv.slice(2)
const plugin = (await import(pluginPath)).default
const hooks = await plugin({ worktree, $ })
async function fire(fp) {
  const output = { metadata: {} }
  await hooks["tool.execute.after"]({ tool: "edit", args: { file_path: fp } }, output)
  return output.metadata
}
let failed = 0
for (const rel of ["STACK-LEDGER.md", "discovery/bar.md", "methodologies/baz.md", "CATALOG.md"]) {
  await fire(join(worktree, rel))
  if (!existsSync(join(worktree, "plugin/docs", rel))) { console.log("FAIL no sync: " + rel); failed = 1 }
}
const meta = await fire(join(worktree, "README.md"))
if (meta.opencodeAutoSynced) { console.log("FAIL unwatched path triggered"); failed = 1 }
process.exit(failed)
"""


class TestWatchListSeam(unittest.TestCase):
    """Pins the watch-list seam (#194): sync-plugin-docs.sh --list-watched is the
    one definition of the syncable set, and both harness auto-sync adapters derive
    their trigger predicate from it instead of hand-copying it. This fixes
    adapter-trigger drift; a brand-new root doc still needs a WATCHED_* entry
    (ADR-0001's allowlist is deliberate)."""

    # The syncable set. Adding a doc to sync-plugin-docs.sh's WATCHED_* arrays
    # must update this pin — the same alerting contract as TestIntegrityMakefile.GATES.
    WATCHED = {
        "CATALOG.md", "WORKFLOW.md", "STACK.md", "STACK-LEDGER.md",
        "evaluations/", "discovery/", "methodologies/",
    }

    def test_list_watched_emits_the_syncable_set(self):
        r = subprocess.run(["bash", os.path.join(ROOT, "sync-plugin-docs.sh"), "--list-watched"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)
        self.assertEqual(set(r.stdout.split()), self.WATCHED)

    def test_every_listed_entry_is_actually_synced(self):
        # The list must describe real sync behavior: after an apply, each listed
        # file/dir has a counterpart under plugin/docs/.
        with tempfile.TemporaryDirectory() as d:
            _sync_fixture_tree(d)
            fixture_by_dir = {"evaluations": "foo.md", "discovery": "bar.md", "methodologies": "baz.md"}
            r = subprocess.run(["bash", "sync-plugin-docs.sh"], cwd=d, capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)
            for entry in self.WATCHED:
                if entry.endswith("/"):
                    tail = os.path.join(entry.rstrip("/"), fixture_by_dir[entry.rstrip("/")])
                else:
                    tail = entry
                self.assertTrue(os.path.exists(os.path.join(d, "plugin/docs", tail)),
                                msg=f"listed entry not synced: {entry}")

    def _run_claude_hook(self, d, file_path):
        hook = os.path.join(d, "auto-sync.sh")
        shutil.copy(os.path.join(ROOT, ".claude/hooks/auto-sync.sh"), hook)
        payload = '{"tool_input": {"file_path": "%s"}}' % file_path
        env = {**os.environ, "CLAUDE_PROJECT_DIR": d}
        return subprocess.run(["bash", hook], input=payload, env=env,
                              capture_output=True, text=True)

    def test_claude_hook_triggers_on_every_watched_entry(self):
        # An edit to ANY watched entry — including STACK-LEDGER.md, discovery/,
        # methodologies/, the three the hand-copied predicate silently omitted —
        # must re-run the sync (observable as plugin/docs/ being populated).
        edits = {
            "CATALOG.md": "CATALOG.md", "WORKFLOW.md": "WORKFLOW.md",
            "STACK.md": "STACK.md", "STACK-LEDGER.md": "STACK-LEDGER.md",
            "evaluations/": "evaluations/foo.md", "discovery/": "discovery/bar.md",
            "methodologies/": "methodologies/baz.md",
        }
        self.assertEqual(set(edits), self.WATCHED)  # one edit per watched entry
        for entry, rel in edits.items():
            with tempfile.TemporaryDirectory() as d:
                _sync_fixture_tree(d)
                r = self._run_claude_hook(d, os.path.join(d, rel))
                self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)
                self.assertTrue(os.path.exists(os.path.join(d, "plugin/docs", rel)),
                                msg=f"hook did not sync after editing {entry}")

    def test_claude_hook_ignores_unwatched_and_derived_paths(self):
        # Unwatched files and edits inside the derived plugin/docs/ copy must not
        # re-sync (observable as plugin/docs/ never being created).
        for rel in ("README.md", "plugin/docs/CATALOG.md"):
            with tempfile.TemporaryDirectory() as d:
                _sync_fixture_tree(d)
                r = self._run_claude_hook(d, os.path.join(d, rel))
                self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)
                self.assertFalse(os.path.exists(os.path.join(d, "plugin/docs/WORKFLOW.md")),
                                 msg=f"hook synced on a non-trigger path: {rel}")

    def test_both_adapters_derive_from_list_watched(self):
        # Lockstep pin (CLAUDE.md invariant): each harness adapter consumes
        # --list-watched rather than restating the watch set. The opencode plugin
        # can't be executed from here, so pin its source: it must call
        # --list-watched and must not hardcode any watched basename.
        adapters = (".claude/hooks/auto-sync.sh", ".opencode/plugins/auto-sync.ts")
        for rel in adapters:
            with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
                src = f.read()
            self.assertIn("--list-watched", src,
                          msg=f"{rel} does not derive its trigger set from --list-watched")
        with open(os.path.join(ROOT, ".opencode/plugins/auto-sync.ts"), encoding="utf-8") as f:
            ts = f.read()
        for name in sorted(self.WATCHED):
            self.assertNotIn(f'"{name.rstrip("/")}"', ts,
                             msg=f"opencode adapter hardcodes watched entry {name}")

    def test_claude_hook_fails_open_when_sync_script_missing(self):
        # The seam's new failure mode: --list-watched unavailable (script missing
        # or broken). Contract: exit 0, never break the session, no sync attempted.
        with tempfile.TemporaryDirectory() as d:
            r = self._run_claude_hook(d, os.path.join(d, "CATALOG.md"))
            self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)
            self.assertFalse(os.path.exists(os.path.join(d, "plugin/docs")))

    @unittest.skipUnless(shutil.which("bun"), "bun not installed; opencode adapter covered by source pin only")
    def test_opencode_plugin_triggers_on_every_previously_missed_entry(self):
        # Executes the REAL opencode plugin under bun against a fixture worktree —
        # the behavioral counterpart to the textual derive-pin above.
        with tempfile.TemporaryDirectory() as d:
            _sync_fixture_tree(d)
            driver = _write(d, "driver.ts", _OPENCODE_DRIVER)
            r = subprocess.run(
                ["bun", "run", driver, d, os.path.join(ROOT, ".opencode/plugins/auto-sync.ts")],
                capture_output=True, text=True, cwd=d)
            self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)


# ----------------------------------------------------------------- detector I (evidence field, #62)
class TestEvidenceField(unittest.TestCase):
    def test_evidence_level_parses_each_value(self):
        for lvl in ("MEASURED", "RUN", "REVIEW", "SOURCE-ONLY"):
            ev = audit.Evaluation("x", f"## How we tested it\n\n**Evidence:** {lvl}\n\nbody\n")
            self.assertEqual(ev.evidence_level, lvl)

    def test_evidence_level_absent_is_none(self):
        ev = audit.Evaluation("x", "## How we tested it\n\nran it but never declared a field\n")
        self.assertIsNone(ev.evidence_level)

    def test_evidence_level_ignores_prose_mentions(self):
        # The word "Evidence" in prose must not be parsed as the declared field.
        ev = audit.Evaluation("x", "We have strong evidence it works; Evidence: maybe.\n")
        self.assertIsNone(ev.evidence_level)

    def _run_audit(self, files):
        with tempfile.TemporaryDirectory() as d:
            for name, text in files.items():
                _write(d, os.path.join("evaluations", name), text)
            orig = audit.ROOT
            try:
                audit.ROOT = d
                return audit.audit_evidence_field()
            finally:
                audit.ROOT = orig

    def test_audit_counts_and_lists_missing(self):
        counts, missing, strong = self._run_audit({
            "a.md": "**Evidence:** MEASURED\n\n## Verdict\n\n**ADOPT**\n",
            "b.md": "**Evidence:** REVIEW\n",
            "c.md": "no field here\n",
            "TEMPLATE.md": "**Evidence:** {MEASURED | RUN | REVIEW | SOURCE-ONLY}\n",  # skipped by load_evals
        })
        self.assertEqual(counts["MEASURED"], 1)
        self.assertEqual(counts["REVIEW"], 1)
        self.assertEqual(missing, ["c"])  # TEMPLATE.md excluded, c has no field
        # only the ADOPT-verdict eval counts toward the strong (ADOPT/KEEP) tally
        self.assertEqual(strong["MEASURED"], 1)
        self.assertEqual(strong["REVIEW"], 0)


# ----------------------------------------------------------------- detector J (stack drift, #70)
class TestDetectorJ(unittest.TestCase):
    STACK = "## Plan\n| [foo](https://github.com/x/foo) | desc | `cmd` | sig |\n"
    COMP = ("## Plan\n| Tool | Type | Auto | Free | Evaluated | Evidence |\n"
            "|---|---|---|---|---|---|\n"
            "| foo | tool | | ✓ | ADOPT | RUN |\n"
            "| bar | tool | | ✓ | ADOPT | REVIEW |\n")
    LEDGER_OK = "| foo | ADOPT | Plan | yes | |\n| bar | ADOPT | Plan | no | overlaps foo |\n"

    def _run(self, stack, ledger, comp):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "STACK.md", stack)
            _write(d, "STACK-LEDGER.md", ledger)
            _write(d, "COMPARISON.md", comp)
            orig = audit.ROOT
            try:
                audit.ROOT = d
                return audit.audit_stack_drift()
            finally:
                audit.ROOT = orig

    def test_consistent_passes(self):
        self.assertEqual(self._run(self.STACK, self.LEDGER_OK, self.COMP), [])

    def test_adopt_missing_from_ledger_flagged(self):
        probs = self._run(self.STACK, "| foo | ADOPT | Plan | yes | |\n", self.COMP)
        self.assertTrue(any("bar" in p and "neither in STACK nor" in p for p in probs), probs)

    def test_excluded_row_without_reason_flagged(self):
        probs = self._run(self.STACK, "| foo | ADOPT | Plan | yes | |\n| bar | ADOPT | Plan | no | |\n", self.COMP)
        self.assertTrue(any("excluded (no) but records no reason" in p for p in probs), probs)

    def test_in_stack_row_absent_from_stack_flagged(self):
        probs = self._run("## Plan\n", self.LEDGER_OK, self.COMP)
        self.assertTrue(any("marked 'yes' but not found in STACK.md" in p for p in probs), probs)

    def test_verdict_mismatch_flagged(self):
        comp2 = self.COMP.replace("| bar | tool | | ✓ | ADOPT |", "| bar | tool | | ✓ | SKIP |")
        probs = self._run(self.STACK, self.LEDGER_OK, comp2)
        self.assertTrue(any("verdict ADOPT != COMPARISON SKIP" in p for p in probs), probs)

    def test_install_source_alias_matches(self):
        # A tool in STACK under a different link text but its repo basename (GSD <- superpowers)
        stack = "## Implement\n| [GSD](https://github.com/obra/superpowers) | desc | `cmd` | sig |\n"
        ledger = "| superpowers | ADOPT | Implement | yes | |\n"
        comp = ("## Implement\n| Tool | Type | Auto | Free | Evaluated |\n|---|---|---|---|---|\n"
                "| superpowers | skill | | ✓ | ADOPT |\n")
        self.assertEqual(self._run(stack, ledger, comp), [])  # matched via repo basename


# ----------------------------------------------------------------- detector K (verdict evidence, #71)
class TestDetectorK(unittest.TestCase):
    def _run(self, files):
        with tempfile.TemporaryDirectory() as d:
            for name, text in files.items():
                _write(d, os.path.join("evaluations", name), text)
            orig = audit.ROOT
            try:
                audit.ROOT = d
                return audit.audit_verdict_evidence()
            finally:
                audit.ROOT = orig

    def test_measured_adopt_passes(self):
        self.assertEqual(self._run({"a.md": "**Evidence:** MEASURED\n\n## Verdict\n\n**ADOPT**\n"}), [])

    def test_review_with_disclaimer_passes(self):
        t = "## How we tested it\n\nSource-grounded review — not run hands-on.\n\n**Evidence:** REVIEW\n\n## Verdict\n\n**ADOPT**\n"
        self.assertEqual(self._run({"b.md": t}), [])

    def test_source_only_adopt_without_disclaimer_fails(self):
        flagged = self._run({"c.md": "**Evidence:** SOURCE-ONLY\n\n## Verdict\n\n**ADOPT**\n"})
        self.assertEqual(flagged, [("c", "ADOPT", "SOURCE-ONLY")])

    def test_review_without_disclaimer_fails(self):
        # A hand-set REVIEW with no actual not-run disclaimer is exactly what the gate catches.
        flagged = self._run({"d.md": "**Evidence:** REVIEW\n\n## Verdict\n\n**ADOPT**\n"})
        self.assertEqual(flagged, [("d", "ADOPT", "REVIEW")])

    def test_keep_treated_like_adopt(self):
        flagged = self._run({"k.md": "**Evidence:** SOURCE-ONLY\n\n## Verdict\n\n**KEEP**\n"})
        self.assertEqual(flagged, [("k", "KEEP", "SOURCE-ONLY")])

    def test_skip_and_conditional_ignored(self):
        self.assertEqual(self._run({
            "e.md": "**Evidence:** SOURCE-ONLY\n\n## Verdict\n\n**SKIP**\n",
            "f.md": "**Evidence:** SOURCE-ONLY\n\n## Verdict\n\n**CONDITIONAL**\n",
        }), [])


# ----------------------------------------------------------------- detector D (verdict sync) + discovery-log (#69)
class TestDetectorD(unittest.TestCase):
    def _run(self, comparison, evals):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "COMPARISON.md", comparison)
            for name, text in evals.items():
                _write(d, os.path.join("evaluations", name), text)
            orig = audit.ROOT
            try:
                audit.ROOT = d
                return audit.audit_verdicts()
            finally:
                audit.ROOT = orig

    HEADER = "## Plan\n| Tool | Type | Auto | Free | Evaluated | Evidence |\n|---|---|---|---|---|---|\n"

    def test_discovery_log_row_not_synced(self):
        # A discovery-log COMPARISON row is a lead, not a verdict: an eval still reading
        # CONDITIONAL must NOT be flagged as a mismatch.
        comp = self.HEADER + "| foo | tool | | ✓ | discovery-log | REVIEW |\n"
        evals = {"foo.md": "**Evidence:** REVIEW\n\n## Verdict\n\n**CONDITIONAL**\n"}
        self.assertEqual(self._run(comp, evals), [])

    def test_real_mismatch_still_flagged(self):
        comp = self.HEADER + "| bar | tool | | ✓ | ADOPT | MEASURED |\n"
        evals = {"bar.md": "**Evidence:** MEASURED\n\n## Verdict\n\n**SKIP**\n"}
        flagged = self._run(comp, evals)
        self.assertTrue(any(f[0] == "bar" for f in flagged), flagged)


# ----------------------------------------------------------------- backfill-evidence (#67)
class TestEvidenceBackfill(unittest.TestCase):
    def test_derive_levels(self):
        self.assertEqual(audit.Evidence("**Hands-on, measured** A/B, token deltas").level, "MEASURED")
        self.assertEqual(audit.Evidence("Source-grounded review — not run hands-on.").level, "REVIEW")
        self.assertEqual(audit.Evidence("We ran it on our repo and exercised the CLI.").level, "RUN")
        self.assertEqual(audit.Evidence("").level, "SOURCE-ONLY")

    def test_field_inserted_as_own_paragraph_and_idempotent(self):
        t = "# Evaluation: X\n\n## How we tested it\n\nWe did not run it; source review.\n"
        out = backfill.backfill_eval_text(t)
        self.assertIn("## How we tested it\n\n**Evidence:** REVIEW\n\n", out)
        self.assertEqual(backfill.backfill_eval_text(out), out)  # never double-inserts

    def test_field_never_overwrites_existing(self):
        t = "## How we tested it\n\n**Evidence:** MEASURED\n\nran it live with metrics.\n"
        self.assertEqual(backfill.backfill_eval_text(t), t)

    def test_comparison_column_keeps_detector_g_clean_and_idempotent(self):
        # The real transform appends an Evidence column; empty alias map -> SOURCE-ONLY cells.
        cmp6 = backfill.rebuild_comparison(COMPARISON_OK, {})
        self.assertIn("| Evaluated | Evidence |", cmp6)
        self.assertIn("| ADOPT | SOURCE-ONLY |", cmp6)
        # Summary table untouched (no Evidence column bleeds into per-stage aggregates)
        self.assertIn("| Stage | Tools | Evaluated | Adoption rate |", cmp6)
        # body counts unchanged -> detector G / reconcile see the same rows
        self.assertEqual(reconcile.comparison_body_counts(cmp6), {"Plan": 2, "Ship": 1})
        self.assertEqual(backfill.rebuild_comparison(cmp6, {}), cmp6)  # idempotent
        with tempfile.TemporaryDirectory() as d:
            _write(d, "CATALOG.md", CATALOG_OK)
            _write(d, "COMPARISON.md", cmp6)
            orig = audit.ROOT
            try:
                audit.ROOT = d
                self.assertEqual(audit.audit_comparison(), [])  # G still clean with the new column
            finally:
                audit.ROOT = orig


# ----------------------------------------------------------------- detector L (staleness, #65)
class TestDetectorL(unittest.TestCase):
    TODAY = datetime.date(2026, 6, 22)

    def _eval(self, typ, date=None):
        head = f"**Last verified:** {date}\n\n" if date else ""
        return head + f"| [x](https://github.com/a/x) | {typ} | one | two | none |\n"

    def _run(self, files):
        with tempfile.TemporaryDirectory() as d:
            for name, text in files.items():
                _write(d, os.path.join("evaluations", name), text)
            orig = audit.ROOT
            try:
                audit.ROOT = d
                return audit.audit_staleness(today=self.TODAY)
            finally:
                audit.ROOT = orig

    def _ago(self, days):
        return (self.TODAY - datetime.timedelta(days=days)).isoformat()

    def test_category_aware_thresholds(self):
        stale, undated = self._run({
            "harness_stale.md": self._eval("harness", self._ago(130)),    # 130 > 120 -> stale
            "harness_fresh.md": self._eval("harness", self._ago(100)),    # 100 < 120 -> ok
            "ref_old_but_ok.md": self._eval("reference", self._ago(130)), # 130 < 365 -> ok
            "tool_stale.md": self._eval("tool", self._ago(200)),          # 200 > 180 -> stale
            "undated.md": self._eval("tool"),                             # no date -> undated
        })
        self.assertEqual({s[0] for s in stale}, {"harness_stale", "tool_stale"})
        self.assertEqual(undated, 1)

    def test_unknown_type_uses_default_threshold(self):
        # weirdtype not in STALENESS_DAYS -> DEFAULT_STALENESS_DAYS (180); 200 > 180 -> stale
        stale, undated = self._run({"x.md": self._eval("weirdtype", self._ago(200))})
        self.assertEqual(len(stale), 1)
        self.assertEqual(undated, 0)

    def test_threshold_boundary_not_stale(self):
        # exactly at the threshold (age == threshold) is NOT past it
        stale, _ = self._run({"t.md": self._eval("tool", self._ago(180))})  # 180 == 180
        self.assertEqual(stale, [])


# ----------------------------------------------------------------- detector N (savings claims)
class TestSavingsClaims(unittest.TestCase):
    HEADER = "| Name | Type | One-liner | Problem | Overlaps |\n|---|---|---|---|---|\n"

    def _has(self, one_liner):
        return audit._has_savings_claim(one_liner)

    def test_recognises_savings_headlines(self):
        for s in ("Compresses tool output (60-95% fewer tokens)",
                  "Context window optimization — 96% reduction across 15 platforms",
                  "95%+ context reduction for tool outputs",
                  "returns exact snippets using ~98% fewer tokens than grep",
                  "257 languages — 50x token reduction",
                  "claims ~6× lower token consumption than comparable agents"):
            self.assertTrue(self._has(s), s)

    def test_ignores_non_savings_numbers(self):
        for s in ("Static-binary engine indexing 158 languages into a graph",
                  "94% of languages supported by the parser",   # % but no token/context
                  "2M-token effective context, self-hostable",  # token figure, no reduction verb
                  "battle-tested at 10B+ tokens/day throughput"):
            self.assertFalse(self._has(s), s)

    def _run(self, catalog, evals):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "CATALOG.md", catalog)
            for name, text in evals.items():
                _write(d, os.path.join("evaluations", name), text)
            orig = audit.ROOT
            try:
                audit.ROOT = d
                return audit.audit_savings_claims()
            finally:
                audit.ROOT = orig

    def _row(self, name, one_liner):
        return f"| [{name}](https://github.com/a/{name}) | tool | {one_liner} | p | none |\n"

    def test_unverified_claim_flagged(self):
        cat = self.HEADER + self._row("foo", "Compresses output, 94% token savings")
        evals = {"foo.md": "**Evidence:** SOURCE-ONLY\n\n## Verdict\n\n**CONDITIONAL**\n"}
        self.assertEqual(self._run(cat, evals), [("foo", "SOURCE-ONLY", False)])

    def test_measured_claim_suppressed(self):
        cat = self.HEADER + self._row("foo", "Compresses output, 94% token savings")
        evals = {"foo.md": "**Evidence:** MEASURED\n\n## Verdict\n\n**ADOPT**\n"}
        self.assertEqual(self._run(cat, evals), [])

    def test_no_eval_surfaces_as_no_eval(self):
        cat = self.HEADER + self._row("bar", "Cuts 65% of tokens by dropping filler")
        self.assertEqual(self._run(cat, {}), [("bar", "(no eval)", False)])

    def test_self_reported_disclaimer_bucketed(self):
        cat = self.HEADER + self._row("baz", "Persistent memory; 71.5× fewer tokens; self-reported")
        flagged = self._run(cat, {})
        self.assertEqual(flagged, [("baz", "(no eval)", True)])

    def test_non_savings_row_not_flagged(self):
        cat = self.HEADER + self._row("qux", "Parses session logs into daily token & cost reports")
        self.assertEqual(self._run(cat, {}), [])


# ----------------------------------------------------------------- tier-stack (#72)
class TestTierStack(unittest.TestCase):
    STACK = ("# Stack\n\n<!-- TIERS:START -->\n<!-- TIERS:END -->\n\n## Plan\n"
             "| [foo](https://github.com/x/foo) | d | `c` | s |\n"
             "| [bar](https://github.com/x/bar) | d | `c` | s |\n"
             "| [baz](https://github.com/x/baz) | d | `c` | s |\n")

    def _with_amap(self, amap, fn):
        orig = tier.bf._build_alias_map
        try:
            tier.bf._build_alias_map = lambda: amap
            return fn()
        finally:
            tier.bf._build_alias_map = orig

    def test_tiering_split_derived_from_evidence(self):
        amap = {"foo": "MEASURED", "bar": "REVIEW"}  # baz has no eval -> SOURCE-ONLY
        t1, t2 = self._with_amap(amap, lambda: tier.stack_tiers(self.STACK))
        self.assertEqual(t1, [("foo", "MEASURED")])           # MEASURED/RUN -> Tier 1
        self.assertEqual(t2, [("bar", "REVIEW"), ("baz", "SOURCE-ONLY")])  # rest -> Tier 2

    def test_apply_replaces_between_markers_and_is_idempotent(self):
        amap = {"foo": "RUN", "bar": "REVIEW"}
        out = self._with_amap(amap, lambda: tier.apply(self.STACK))
        self.assertIn("**Tier 1 — measured (1)", out)
        self.assertIn("foo (RUN)", out)
        self.assertIn("baz (SOURCE-ONLY)", out)
        self.assertEqual(self._with_amap(amap, lambda: tier.apply(out)), out)  # idempotent

    def test_missing_markers_exits_2(self):
        with self.assertRaises(SystemExit) as cm:
            tier.apply("# Stack with no markers\n")
        self.assertEqual(cm.exception.code, 2)


# ----------------------------------------------------------------- make check entrypoint (#114)
class TestIntegrityMakefile(unittest.TestCase):
    """Pins the `make check` entrypoint: every gate CI enforces must live in the
    check target, and integrity.yml must delegate to `make check` — so the local
    and CI gate sets provably can't drift (#114)."""

    # The full gate set CI's integrity.yml enforces, in --check/verify mode.
    GATES = (
        "audit-evals.py --offline",
        "audit-evals.py --selftest",
        "reconcile-counts.py --check",
        "backfill-evidence.py --check",
        "tier-stack.py --check",
        "sync-plugin-docs.sh --check",
        "audit-evals.py --installs",
    )

    def _check_target_body(self):
        with open(os.path.join(ROOT, "Makefile"), encoding="utf-8") as f:
            lines = f.read().splitlines()
        body, capturing = [], False
        for l in lines:
            if l.startswith("check:"):
                capturing = True
                continue
            if capturing:
                if l.startswith("\t"):
                    body.append(l.strip())
                else:
                    break  # recipe ends at the first non-tab line
        return body

    def test_check_target_runs_every_gate(self):
        body = "\n".join(self._check_target_body())
        self.assertTrue(body, "Makefile has no `check:` target body")
        for gate in self.GATES:
            self.assertIn(gate, body, msg=f"`make check` is missing gate: {gate}")

    def test_ci_delegates_to_make_check(self):
        with open(os.path.join(ROOT, ".github/workflows/integrity.yml"), encoding="utf-8") as f:
            yml = f.read()
        self.assertIn("make check", yml,
                      "integrity.yml must call `make check` so CI and the Makefile can't drift")

    def test_fix_then_check(self):
        # `fix` must end by re-running check, so a clean `make fix` means a green tree.
        with open(os.path.join(ROOT, "Makefile"), encoding="utf-8") as f:
            mk = f.read()
        self.assertRegex(mk, r"fix:[\s\S]*\$\(MAKE\)\s+check",
                         "`make fix` must re-run `make check` after applying fixers")


if __name__ == "__main__":
    unittest.main(verbosity=2)
