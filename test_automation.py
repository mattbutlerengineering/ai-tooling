#!/usr/bin/env python3
"""
test_automation.py — characterization tests for the count/sync automation:
reconcile-counts.py, audit-evals.py detector G (audit_comparison), and
sync-plugin-docs.sh.

These pin the CURRENT correct behavior so the planned shared-parser refactor
(issue #45) has a regression net. They never touch the real CATALOG.md /
COMPARISON.md / plugin/ — every test runs against fixtures in a temp dir, either
through a DetectorContext built from the fixture directory (#199) or by copying
the script into a fixture tree.

Run:
  python3 -m unittest test_automation -v      # or: python3 test_automation.py
Exits non-zero on any failure (gates CI / pre-commit).
"""
import os, datetime, importlib.util, json, re, shutil, subprocess, tempfile, unittest
import urllib.error

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
backfill_lv = _load("backfill_lastverified", "backfill-lastverified.py")
tier = _load("tier_stack", "tier-stack.py")
nexteval = _load("next_evals", "next-evals.py")
watchlist = _load("watchlist", "watchlist.py")
triage = _load("triage", "triage.py")


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

| Stage | Tools | Validated | Recommended | Validated % |
|-------|-------|-----------|-------------|-------------|
| Plan | 2 | 2 | 1 | 100% |
| Ship | 1 | 1 | 1 | 100% |
| **Total** | **3** | **3** | **2** | **100%** |
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
        # Validated/Recommended come from the body verdicts (Plan: ADOPT+SKIP -> 2
        # validated, 1 recommended), not the Tools count — so a corrupted stage row
        # is rebuilt to the real funnel figures.
        broken = COMPARISON_OK.replace("| Plan | 2 | 2 | 1 | 100% |", "| Plan | 9 | 9 | 9 | 42% |") \
                              .replace("All 3 tools", "All 99 tools")
        fixed = reconcile.fix_comparison(broken, 3)
        self.assertIn("| Stage | Tools | Validated | Recommended | Validated % |", fixed)
        self.assertIn("| Plan | 2 | 2 | 1 | 100% |", fixed)
        self.assertIn("All 3 tools from CATALOG.md", fixed)

    def test_fix_comparison_fixes_total_row(self):
        # Regression test for the historical bug: the bolded **Total** row was
        # not rewritten because section and Total shared one regex. The Total now
        # carries Tools/Validated/Recommended (Tools stays the catalog count C).
        broken = COMPARISON_OK.replace("| **Total** | **3** | **3** | **2** | **100%** |",
                                       "| **Total** | **99** | **99** | **99** | **1%** |")
        fixed = reconcile.fix_comparison(broken, 3)
        self.assertIn("| **Total** | **3** | **3** | **2** | **100%** |", fixed)
        self.assertNotIn("**99**", fixed)

    def test_fix_comparison_excludes_discovery_log_from_validated(self):
        # discovery-log is a catalogued lead, not a verdict (ADR 0001): it counts
        # toward Tools but never toward Validated/Recommended.
        comp = (
            "All 2 tools from CATALOG.md at a glance.\n\n"
            "## Plan\n\n"
            "| Tool | Type | Auto | Free | Evaluated |\n"
            "|------|------|------|------|-----------|\n"
            "| a | tool | | ✓ | ADOPT |\n"
            "| b | tool | | ✓ | discovery-log |\n\n"
            "## Summary\n\n"
            "| Stage | Tools | Validated | Recommended | Validated % |\n"
            "|-------|-------|-----------|-------------|-------------|\n"
            "| Plan | 0 | 0 | 0 | 0% |\n"
            "| **Total** | **0** | **0** | **0** | **0%** |\n"
        )
        fixed = reconcile.fix_comparison(comp, 2)
        # 2 body rows, but only ADOPT is validated (discovery-log excluded); 50%.
        self.assertIn("| Plan | 2 | 1 | 1 | 50% |", fixed)
        self.assertIn("| **Total** | **2** | **1** | **1** | **50%** |", fixed)

    def test_fix_eval_strings_both_variants(self):
        self.assertEqual(reconcile.fix_eval_strings("distilled from 471 evaluations.", 487),
                         "distilled from 487 evaluations.")
        self.assertEqual(reconcile.fix_eval_strings("471 evidence-based evaluations here", 487),
                         "487 evidence-based evaluations here")

    def test_fix_eval_strings_ignores_unrelated_numbers(self):
        # The regex is anchored on "evaluations"; issue refs / bare counts are left alone.
        s = "see issue 471 and 12 tools cataloged"
        self.assertEqual(reconcile.fix_eval_strings(s, 487), s)

    def test_fix_eval_strings_plugin_phrasing(self):
        # plugin/CLAUDE.md says "evaluation and comparison files", not "evaluations".
        # It was in FILES_TOTAL all along, so it *looked* maintained while drifting 87
        # behind the real count (#302). The specific phrase must win over the loose ones.
        self.assertEqual(
            reconcile.fix_eval_strings(
                "- `evaluations/` — 469 evidence-based evaluation and comparison files", 556),
            "- `evaluations/` — 556 evidence-based evaluation and comparison files")


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


# ----------------------------------------------------------------- catalog_lib: comparison_verdict_rows (#193)
class TestComparisonVerdictRows(unittest.TestCase):
    """Pins catalog_lib.comparison_verdict_rows() — the one COMPARISON.md
    verdict-row parser detectors D, J, and M route through (#193). Locates the
    verdict via each table's 'Evaluated' header column, not a fixed offset."""

    def _pairs(self, text):
        return [(r.tool, r.verdict) for r in catalog_lib.comparison_verdict_rows(text)]

    def test_extracts_tool_and_verdict_per_body_row(self):
        self.assertEqual(self._pairs(COMPARISON_OK),
                         [("a", "ADOPT"), ("b", "SKIP"), ("c", "KEEP")])

    def test_summary_header_and_separator_rows_not_emitted(self):
        # COMPARISON_OK's Summary table also has an 'Evaluated' column, but its
        # cells are counts, not verdict tokens — no row may leak from it.
        pairs = self._pairs(COMPARISON_OK)
        self.assertNotIn(("Plan", "2"), pairs)
        self.assertEqual(len(pairs), 3)

    def test_survives_column_appended_after_verdict(self):
        # backfill-evidence appends an Evidence column; parsing must not care.
        comp = ("## Plan\n| Tool | Type | Auto | Free | Evaluated | Evidence |\n"
                "|---|---|---|---|---|---|\n"
                "| foo | tool | | ✓ | ADOPT | RUN |\n")
        self.assertEqual(self._pairs(comp), [("foo", "ADOPT")])

    def test_survives_column_inserted_before_verdict(self):
        # The failure mode of the retired fixed-offset regexes: a column inserted
        # before 'Evaluated' silently un-matched every row.
        comp = ("## Plan\n| Tool | Type | Auto | Free | Pricing | Evaluated |\n"
                "|---|---|---|---|---|---|\n"
                "| foo | tool | | ✓ | free | ADOPT |\n")
        self.assertEqual(self._pairs(comp), [("foo", "ADOPT")])

    def test_all_verdict_tokens_recognized(self):
        rows = "".join(f"| t{i} | tool | | ✓ | {v} |\n"
                       for i, v in enumerate(catalog_lib.VERDICTS))
        comp = ("## Plan\n| Tool | Type | Auto | Free | Evaluated |\n"
                "|---|---|---|---|---|\n" + rows)
        self.assertEqual([v for _, v in self._pairs(comp)], list(catalog_lib.VERDICTS))

    def test_non_verdict_cell_not_emitted(self):
        comp = ("## Plan\n| Tool | Type | Auto | Free | Evaluated |\n"
                "|---|---|---|---|---|\n"
                "| foo | tool | | ✓ | pending |\n")
        self.assertEqual(self._pairs(comp), [])

    def test_table_without_evaluated_column_contributes_nothing(self):
        comp = ("## Notes\n| Stage | Count |\n|---|---|\n| Plan | ADOPT |\n")
        self.assertEqual(self._pairs(comp), [])

    def test_body_cell_named_evaluated_is_not_a_header(self):
        # Header detection is structural (a row followed by a |---| separator),
        # so a body cell that happens to read "Evaluated" cannot re-anchor vcol.
        comp = ("## Plan\n| Tool | Type | Auto | Free | Evaluated |\n"
                "|---|---|---|---|---|\n"
                "| Evaluated | tool | | ✓ | ADOPT |\n")
        self.assertEqual(self._pairs(comp), [("Evaluated", "ADOPT")])

    def test_adjacent_table_without_evaluated_does_not_inherit_vcol(self):
        # A new table's header re-anchors or clears vcol even with no blank line
        # between tables — rows can't be keyed against the previous table's column.
        comp = ("| Tool | Type | Auto | Free | Evaluated |\n"
                "|---|---|---|---|---|\n"
                "| foo | tool | | ✓ | ADOPT |\n"
                "| Stage | Count | Note | Extra | Misc |\n"
                "|---|---|---|---|---|\n"
                "| Plan | 2 | x | y | KEEP |\n")
        self.assertEqual(self._pairs(comp), [("foo", "ADOPT")])

    def test_row_exposes_cells_as_named_field(self):
        row = catalog_lib.comparison_verdict_rows(COMPARISON_OK)[0]
        self.assertEqual(row.cells[0], "a")
        self.assertIn("ADOPT", row.cells)

    def test_verdict_vocabulary_lives_in_catalog_lib(self):
        self.assertEqual(catalog_lib.VERDICTS,
                         ("ADOPT", "CONDITIONAL", "SKIP", "DEFER", "KEEP", "discovery-log"))
        # audit-evals must reference catalog_lib's tuple, not define its own copy.
        # (Identity is asserted against the catalog_lib instance audit imported —
        # _load() gives this test file a separate instance by construction.)
        self.assertIs(audit.VERDICTS, audit.catalog_lib.VERDICTS)


# ----------------------------------------------------------------- catalog_lib: parse_catalog_rows (#196)
class TestParseCatalogRows(unittest.TestCase):
    """Pins catalog_lib.parse_catalog_rows() and is_body_row() — the one CATALOG
    link-row parser the Evaluation class and detectors F, M, N route through, and
    the public body-row predicate backfill-evidence consumes (#196). Named fields
    replace positional cell indexing behind ad-hoc length guards."""

    def test_linked_row_named_fields(self):
        rows = catalog_lib.parse_catalog_rows(CATALOG_OK)
        self.assertEqual([r.name for r in rows], ["a", "b", "c"])
        r = rows[0]
        self.assertEqual(r.url, "https://github.com/x/a")
        self.assertEqual(r.type, "tool")
        self.assertEqual(r.one_liner, "one")
        self.assertEqual(r.overlaps, "none")

    def test_unlinked_row_name_is_raw_cell_url_none(self):
        r = catalog_lib.parse_catalog_rows(
            "| OMEGA | MCP server | mem | pain | peers |\n")[0]
        self.assertEqual(r.name, "OMEGA")
        self.assertIsNone(r.url)
        self.assertEqual(r.type, "MCP server")

    def test_header_and_separator_rows_not_emitted(self):
        self.assertEqual(len(catalog_lib.parse_catalog_rows(CATALOG_OK)), 3)

    def test_non_vocab_type_row_not_emitted(self):
        rows = catalog_lib.parse_catalog_rows("| [x](https://u) | CLI | one | two | none |\n")
        self.assertEqual(rows, [])

    def test_missing_trailing_cells_resolve_to_none(self):
        r = catalog_lib.parse_catalog_rows("| [x](https://u) | tool |\n")[0]
        self.assertIsNone(r.one_liner)
        self.assertIsNone(r.overlaps)

    def test_comparison_style_row_parses_by_name(self):
        # backfill-evidence rewrites COMPARISON body rows via the same predicate.
        r = catalog_lib.parse_catalog_rows("| a | tool | | ✓ | ADOPT |\n")[0]
        self.assertEqual(r.name, "a")
        self.assertEqual(r.cells[-1], "ADOPT")

    def test_is_body_row_predicate(self):
        self.assertTrue(catalog_lib.is_body_row("| [a](https://u) | tool | one | two | none |"))
        self.assertTrue(catalog_lib.is_body_row("| OMEGA | MCP server | m | p | o |"))
        self.assertFalse(catalog_lib.is_body_row("| Name | Type | One-liner | Problem | Overlaps with |"))
        self.assertFalse(catalog_lib.is_body_row("|------|------|"))
        self.assertFalse(catalog_lib.is_body_row("prose, not a table row"))

    def test_no_catalog_lib_privates_referenced_outside(self):
        # The acceptance criterion of #196: no script reaches into catalog_lib's
        # underscore-private names (the retired ae.catalog_lib._BODY_ROW pattern).
        for fn in ("audit-evals.py", "backfill-evidence.py", "tier-stack.py",
                   "reconcile-counts.py"):
            src = open(os.path.join(ROOT, fn), encoding="utf-8").read()
            self.assertNotRegex(src, r"catalog_lib\._", msg=fn)


# ----------------------------------------------------------------- catalog_lib: name keying (#197)
class TestNameKeying(unittest.TestCase):
    """Pins catalog_lib.name_key()/alias_keys() — the ONE definition of "same
    tool" (#197). Detectors D, J, and M key COMPARISON rows through name_key;
    the alias-lookup sides (backfill-evidence, tier-stack, STACK membership)
    use alias_keys. The retired trio (_norm / _drift_key / _OVL_STRIP) keyed
    the same rows three different ways."""

    def test_case_and_punctuation_collapse(self):
        for s in ("claude-mem", "Claude Mem", "claude_mem", " CLAUDE.MEM "):
            self.assertEqual(catalog_lib.name_key(s), "claudemem", s)

    def test_identity_key_keeps_parenthetical_content(self):
        # The parenthetical can be the only discriminator between rows —
        # dropping it in the identity key would collide distinct tools.
        self.assertNotEqual(catalog_lib.name_key("awesome-claude-skills (Composio)"),
                            catalog_lib.name_key("awesome-claude-skills (travisvn)"))

    def test_distinct_names_stay_distinct(self):
        self.assertNotEqual(catalog_lib.name_key("codegraph"),
                            catalog_lib.name_key("code-review-graph"))

    def test_strip_parenthetical_is_the_one_regex(self):
        self.assertEqual(catalog_lib.strip_parenthetical("GSD (Get Shit Done)"), "GSD")
        self.assertEqual(catalog_lib.strip_parenthetical("plain"), "plain")

    def test_identity_keys_exclude_basename(self):
        # A slash-name must never register or match via its basename — that's
        # how 'vercel-labs/agent-skills' would shadow the real 'agent-skills'.
        self.assertEqual(catalog_lib.identity_keys("vercel-labs/agent-skills"),
                         ["vercellabsagentskills"])
        self.assertEqual(catalog_lib.identity_keys("GSD (Get Shit Done)"),
                         ["gsdgetshitdone", "gsd"])

    def test_alias_keys_order_and_dedup(self):
        # most specific first: full name, parenthetical-stripped, slash-basename,
        # then url basename.
        self.assertEqual(catalog_lib.alias_keys("owner/repo"), ["ownerrepo", "repo"])
        self.assertEqual(
            catalog_lib.alias_keys("GSD (Get Shit Done)", "https://github.com/obra/superpowers/"),
            ["gsdgetshitdone", "gsd", "superpowers"])
        self.assertEqual(catalog_lib.alias_keys("tool", "https://github.com/x/tool"), ["tool"])

    def test_detectors_d_j_m_share_one_comparison_map(self):
        # The #197 symptom: three verdict-parse sites, three normalizers. D, J,
        # and M now consume the same ctx.comparison_verdict_map, which registers a
        # row under all its alias keys (full AND stripped)...
        with tempfile.TemporaryDirectory() as d:
            comp = ("## Plan\n| Tool | Type | Auto | Free | Evaluated |\n"
                    "|---|---|---|---|---|\n"
                    "| GSD (Get Shit Done) | tool | | ✓ | ADOPT |\n"
                    "| awesome-claude-skills (Composio) | reference | | ✓ | KEEP |\n"
                    "| awesome-claude-skills (travisvn) | reference | | ✓ | SKIP |\n")
            _write(d, "COMPARISON.md", comp)
            m = audit.DetectorContext(d).comparison_verdict_map
            self.assertEqual(m.get("gsdgetshitdone"), "ADOPT")
            self.assertEqual(m.get("gsd"), "ADOPT")  # stripped alias registered too
            # ...while parenthetical-only discriminators keep distinct full keys.
            self.assertEqual(m.get("awesomeclaudeskillscomposio"), "KEEP")
            self.assertEqual(m.get("awesomeclaudeskillstravisvn"), "SKIP")

    def test_detector_d_matches_parenthetical_row_to_plain_eval_name(self):
        # Under the retired _norm, 'GSD (Get Shit Done)' never matched an eval
        # named gsd — D silently skipped the row. name_key closes that.
        with tempfile.TemporaryDirectory() as d:
            comp = ("## Plan\n| Tool | Type | Auto | Free | Evaluated |\n"
                    "|---|---|---|---|---|\n"
                    "| GSD (Get Shit Done) | tool | | ✓ | ADOPT |\n")
            _write(d, "COMPARISON.md", comp)
            _write(d, "evaluations/gsd.md", "## Verdict\n\n**SKIP**\n")
            flagged = audit.audit_verdicts(audit.DetectorContext(d))
            self.assertTrue(any(f[0] == "gsd" for f in flagged), flagged)


# ----------------------------------------------------------------- catalog_lib: row-shape validation (#198)
class TestRowValidation(unittest.TestCase):
    """Pins catalog_lib.validate_catalog_rows()/validate_comparison_rows() and
    detector O — a malformed row is a reported finding, not a silent skip that
    quietly corrupts the counts the suite gates on (#198)."""

    def test_wellformed_catalog_has_no_findings(self):
        self.assertEqual(catalog_lib.validate_catalog_rows(CATALOG_OK), [])

    def test_catalog_row_with_wrong_cell_count_flagged(self):
        bad = CATALOG_OK + "| [d](https://github.com/x/d) | tool | one | two |\n"
        probs = catalog_lib.validate_catalog_rows(bad)
        self.assertEqual(len(probs), 1)
        self.assertIn("4 cells", probs[0][1])

    def test_catalog_row_with_unknown_type_flagged(self):
        bad = CATALOG_OK + "| [d](https://github.com/x/d) | CLI | one | two | none |\n"
        probs = catalog_lib.validate_catalog_rows(bad)
        self.assertEqual(len(probs), 1)
        self.assertIn("CLI", probs[0][1])

    def test_indented_catalog_row_flagged(self):
        # Markdown renders a ≤3-space-indented row as a table row, but the
        # ^|-anchored parsers and counters skip it — the exact silent-skip #198 kills.
        bad = CATALOG_OK + "  | [d](https://github.com/x/d) | tool | one | two | none |\n"
        probs = catalog_lib.validate_catalog_rows(bad)
        self.assertEqual(len(probs), 1)
        self.assertIn("indented", probs[0][1])

    def test_catalog_row_with_empty_name_cell_flagged(self):
        # A whitespace-only Name cell still matches _BODY_ROW and is counted —
        # a nameless entry corrupting the counts G gates on.
        bad = CATALOG_OK + "| | tool | one | two | none |\n"
        probs = catalog_lib.validate_catalog_rows(bad)
        self.assertEqual(len(probs), 1)
        self.assertIn("Name", probs[0][1])

    def test_catalog_row_without_trailing_pipe_is_wellformed(self):
        # Markdown parses `| a | b | c | d | e` identically to the piped form —
        # the cells are all present, so it is NOT a malformed row.
        ok = CATALOG_OK + "| [d](https://github.com/x/d) | tool | one | two | none\n"
        self.assertEqual(catalog_lib.validate_catalog_rows(ok), [])

    def test_header_and_separator_not_flagged(self):
        # CATALOG_OK already carries a header + separator; a fresh table mid-file
        # must not produce findings either.
        ok = CATALOG_OK + "\n## Ship\n\n| Name | Type | One-liner | Problem | Overlaps with |\n|---|---|---|---|---|\n"
        self.assertEqual(catalog_lib.validate_catalog_rows(ok), [])

    def test_wellformed_comparison_has_no_findings(self):
        self.assertEqual(catalog_lib.validate_comparison_rows(COMPARISON_OK), [])

    def test_comparison_row_with_wrong_cell_count_flagged(self):
        bad = COMPARISON_OK.replace("| a | tool | | ✓ | ADOPT |",
                                    "| a | tool | | ✓ | ADOPT | extra |")
        probs = catalog_lib.validate_comparison_rows(bad)
        self.assertEqual(len(probs), 1)
        self.assertIn("6 cells", probs[0][1])

    def test_comparison_row_with_bad_verdict_flagged(self):
        bad = COMPARISON_OK.replace("| a | tool | | ✓ | ADOPT |",
                                    "| a | tool | | ✓ | pending |")
        probs = catalog_lib.validate_comparison_rows(bad)
        self.assertEqual(len(probs), 1)
        self.assertIn("pending", probs[0][1])

    def test_summary_table_not_validated_as_tool_rows(self):
        # Summary rows carry counts, not verdicts, and the Summary header also
        # says 'Evaluated' — the section-based exclusion keeps them finding-free.
        self.assertEqual(catalog_lib.validate_comparison_rows(COMPARISON_OK), [])

    def test_comparison_row_with_empty_tool_cell_flagged(self):
        bad = COMPARISON_OK.replace("| a | tool | | ✓ | ADOPT |",
                                    "| | tool | | ✓ | ADOPT |")
        probs = catalog_lib.validate_comparison_rows(bad)
        self.assertEqual(len(probs), 1)
        self.assertIn("Tool cell", probs[0][1])

    def test_comparison_table_with_nontool_header_still_validated(self):
        # comparison_verdict_rows anchors on ANY header carrying 'Evaluated';
        # the validator must use the same anchor, or a renamed first column
        # would let the parser consume rows the validator never sees.
        text = ("## Plan\n\n| Name | Type | Auto | Free | Evaluated |\n"
                "|---|---|---|---|---|\n"
                "| a | tool | | ✓ | pending |\n")
        probs = catalog_lib.validate_comparison_rows(text)
        self.assertEqual(len(probs), 1)
        self.assertIn("pending", probs[0][1])

    def test_detector_o_reports_findings_and_gates(self):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "CATALOG.md", CATALOG_OK + "| [d](https://github.com/x/d) | tool | one |\n")
            _write(d, "COMPARISON.md", COMPARISON_OK)
            probs = audit.audit_row_shapes(audit.DetectorContext(d))
            self.assertEqual(len(probs), 1)
            self.assertIn("CATALOG.md", probs[0])

    def test_detector_o_clean_tree_passes(self):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "CATALOG.md", CATALOG_OK)
            _write(d, "COMPARISON.md", COMPARISON_OK)
            self.assertEqual(audit.audit_row_shapes(audit.DetectorContext(d)), [])


# ----------------------------------------------------------------- evidence lookup seam (#201)
class TestEvidenceLookup(unittest.TestCase):
    """catalog_lib.evidence_lookup + DetectorContext.evidence_alias_map — the ONE
    triple-key evidence lookup tier-stack and backfill-evidence route through."""

    def test_fanout_most_specific_key_first(self):
        amap = {"gsdgetshitdone": "MEASURED", "gsd": "REVIEW"}
        self.assertEqual(catalog_lib.evidence_lookup(amap, "GSD (Get Shit Done)"), "MEASURED")

    def test_url_basename_fallback(self):
        # GSD has no eval under its own name; the install-source repo does.
        amap = {"superpowers": "RUN"}
        self.assertEqual(
            catalog_lib.evidence_lookup(amap, "GSD", "https://github.com/obra/superpowers"), "RUN")

    def test_no_match_defaults_to_source_only(self):
        self.assertEqual(catalog_lib.evidence_lookup({}, "ghost"), "SOURCE-ONLY")

    def test_alias_map_declared_beats_derived_and_derived_fallback(self):
        with tempfile.TemporaryDirectory() as d:
            # declared field wins over what the How-section prose would derive
            _write(d, "evaluations/decl.md",
                   "**Evidence:** MEASURED\n\n## How we tested it\n\nWe did not run it.\n")
            # no declared field -> derived (honest disclaimer -> REVIEW)
            _write(d, "evaluations/derv.md",
                   "## How we tested it\n\nSource-grounded review — not run hands-on.\n")
            amap = audit.DetectorContext(d).evidence_alias_map
            self.assertEqual(amap["decl"], "MEASURED")
            self.assertEqual(amap["derv"], "REVIEW")


# ----------------------------------------------------------------- detector context (#199)
class TestDetectorContext(unittest.TestCase):
    """Pins the DetectorContext protocol: every detector's inputs come through
    the context (visible in its signature), and no test monkeypatches the
    module-global ROOT anymore."""

    def test_every_detector_takes_ctx_first(self):
        import inspect
        for name in dir(audit):
            if not name.startswith("audit_"):
                continue
            params = list(inspect.signature(getattr(audit, name)).parameters)
            self.assertTrue(params and params[0] == "ctx",
                            f"{name} must take ctx as its first parameter, has {params}")

    def test_context_caches_loads(self):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "CATALOG.md", CATALOG_OK)
            ctx = audit.DetectorContext(d)
            first = ctx.catalog
            _write(d, "CATALOG.md", "changed")
            self.assertIs(ctx.catalog, first)  # cached — one read per run

    def test_no_root_monkeypatch_left_in_tests(self):
        src = open(os.path.join(ROOT, "test_automation.py"), encoding="utf-8").read()
        for needle in ("audit.ROOT" + " = ", "reconcile.ROOT" + " = "):  # split: don't match this line
            self.assertNotIn(needle, src)


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

    def test_catalog_count_from_fixture_root(self):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "CATALOG.md", CATALOG_OK)
            self.assertEqual(reconcile.catalog_count(d), 3)

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

    def test_eval_count_excludes_template(self):
        with tempfile.TemporaryDirectory() as d:
            for i in range(3):
                _write(d, f"evaluations/e{i}.md", "# eval\n")
            _write(d, "evaluations/TEMPLATE.md", "# template\n")  # not counted
            self.assertEqual(reconcile.eval_count(d), 3)

    def test_eval_count_derived_and_substituted(self):
        with tempfile.TemporaryDirectory() as d:
            self._fixture_repo(
                d, readme="distilled from 999 evaluations, 999 evidence-based evaluations.\n")
            for i in range(4):                                   # K = 4 real evals
                _write(d, f"evaluations/e{i}.md", "# eval\n")
            _write(d, "evaluations/TEMPLATE.md", "# template\n")  # excluded from the count
            # --check flags the stale 999 before applying
            self.assertEqual(self._run(d, "--check").returncode, 1)
            # apply rewrites 999 -> 4 (TEMPLATE.md excluded)
            self.assertEqual(self._run(d).returncode, 0)
            readme = open(os.path.join(d, "README.md"), encoding="utf-8").read()
            self.assertIn("distilled from 4 evaluations, 4 evidence-based evaluations.", readme)
            self.assertNotIn("999", readme)
            # idempotent: --check now clean
            self.assertEqual(self._run(d, "--check").returncode, 0)

    def test_plugin_claudemd_eval_count_is_reconciled(self):
        # The regression for #302: plugin/CLAUDE.md is in FILES_TOTAL but its wording
        # matched no EVAL_PATTERN, so the eval count on line 18 sat frozen while the
        # catalog count on line 17 was rewritten by the same run. End-to-end so the
        # file-list membership and the pattern are pinned together, not just the regex.
        with tempfile.TemporaryDirectory() as d:
            self._fixture_repo(d)
            _write(d, "plugin/CLAUDE.md",
                   "An inventory of 3 tools.\n"
                   "- `evaluations/` — 999 evidence-based evaluation and comparison files\n")
            for i in range(4):                                   # K = 4 real evals
                _write(d, f"evaluations/e{i}.md", "# eval\n")
            _write(d, "evaluations/TEMPLATE.md", "# template\n")  # excluded from the count
            self.assertEqual(self._run(d, "--check").returncode, 1)
            self.assertEqual(self._run(d).returncode, 0)
            plugin = open(os.path.join(d, "plugin", "CLAUDE.md"), encoding="utf-8").read()
            self.assertIn("4 evidence-based evaluation and comparison files", plugin)
            self.assertEqual(self._run(d, "--check").returncode, 0)


# ----------------------------------------------------------------- plugin/hooks/validate-counts.sh
@unittest.skipUnless(shutil.which("bash") and shutil.which("git"),
                     "validate-counts.sh needs bash and git")
class TestValidateCountsHook(unittest.TestCase):
    """The one test here that reads the REAL tree (read-only): the hook resolves its
    own root with `git rev-parse --show-toplevel`, so it cannot be pointed at a
    fixture. It counted evaluations/*.md including TEMPLATE.md while reconcile's
    eval_count() excluded it, so it reported a phantom off-by-one on every run —
    the worst state for a hook whose whole job is to be believed (#302)."""

    def test_hook_is_silent_on_a_clean_tree(self):
        r = subprocess.run(["bash", os.path.join(ROOT, "plugin", "hooks", "validate-counts.sh")],
                           cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(r.stdout, "", msg="hook reported drift on a reconciled tree")
        self.assertEqual(r.returncode, 0, msg=r.stderr)


# ----------------------------------------------------------------- plugin/CLAUDE.md drift
class TestPluginFrontDoorSignals(unittest.TestCase):
    """plugin/CLAUDE.md is HAND-maintained — unlike plugin/docs/, which
    sync-plugin-docs.sh mirrors and gates — so it drifts from root CLAUDE.md in
    silence. Its eval count sat 87 behind (#302) and its quality-signal list stayed
    at five for the entire life of ADR-0004's sixth signal, so anyone installing the
    marketplace package was told the framework has five and never met Verifiability
    (#313). Reads the real tree on purpose: the drift is *between two real files*,
    so a fixture would pin nothing. Derives the expected signals from root CLAUDE.md
    rather than hardcoding them, so a seventh signal needs no test edit."""

    # Anchored on a number word: root CLAUDE.md:7 also says "the quality signals they
    # move", which a bare \w+ would match first.
    _COUNT = re.compile(r"\b(four|five|six|seven|eight|nine)\s+quality signals\b", re.I)

    def _text(self, rel):
        with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
            return f.read()

    def _count_word(self, text, rel):
        m = self._COUNT.search(text)
        self.assertIsNotNone(m, msg=f"{rel} has no 'N quality signals' phrase")
        return m.group(1).lower()

    def test_signal_count_matches_root(self):
        root = self._count_word(self._text("CLAUDE.md"), "CLAUDE.md")
        plugin = self._count_word(self._text("plugin/CLAUDE.md"), "plugin/CLAUDE.md")
        self.assertEqual(plugin, root,
                         msg="plugin/CLAUDE.md quotes a different signal count than root")

    def test_plugin_names_every_root_signal(self):
        # Root lists them after a colon, up to the parenthetical gloss on the last one.
        m = re.search(r"quality signals:\s*(.+?)\s*\(", self._text("CLAUDE.md"))
        self.assertIsNotNone(m, msg="root CLAUDE.md no longer lists its signals after a colon")
        # ", and X" splits on the comma first, so the optional "and " is consumed there too.
        names = [s for s in re.split(r",\s*(?:and\s+)?|\s+and\s+", m.group(1)) if s]
        self.assertGreaterEqual(len(names), 5, msg=f"parsed too few signals: {names}")
        plugin = self._text("plugin/CLAUDE.md")
        for n in names:
            self.assertIn(n, plugin, msg=f"plugin/CLAUDE.md omits the {n} signal")


# ----------------------------------------------------------------- detector G (audit_comparison)
class TestDetectorG(unittest.TestCase):
    def _run_audit(self, catalog, comparison):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "CATALOG.md", catalog)
            _write(d, "COMPARISON.md", comparison)
            return audit.audit_comparison(audit.DetectorContext(d))

    def test_consistent_fixture_has_no_problems(self):
        self.assertEqual(self._run_audit(CATALOG_OK, COMPARISON_OK), [])

    def test_section_tools_mismatch(self):
        # Summary Tools cell disagrees with the body-row count for the stage.
        bad = COMPARISON_OK.replace("| Plan | 2 | 2 | 1 | 100% |", "| Plan | 5 | 2 | 1 | 100% |")
        problems = self._run_audit(CATALOG_OK, bad)
        self.assertTrue(any("section 'Plan'" in p and "Tools" in p for p in problems), msg=str(problems))

    def test_section_validated_mismatch(self):
        # Summary Validated cell disagrees with the real-verdict rows (Plan has 2:
        # ADOPT+SKIP). discovery-log would be excluded — here a plain corruption.
        bad = COMPARISON_OK.replace("| Plan | 2 | 2 | 1 | 100% |", "| Plan | 2 | 9 | 1 | 100% |")
        problems = self._run_audit(CATALOG_OK, bad)
        self.assertTrue(any("section 'Plan'" in p and "Validated" in p for p in problems), msg=str(problems))

    def test_total_vs_body_mismatch(self):
        # Total Tools says 9 but body sums to 3. CATALOG also 9 rows so the catalog
        # check passes and the body-total mismatch is isolated.
        catalog9 = CATALOG_OK + "".join(
            f"| [d{i}](https://github.com/x/d{i}) | tool | o | t | none |\n" for i in range(6))
        bad = COMPARISON_OK.replace("| **Total** | **3** | **3** | **2** | **100%** |",
                                    "| **Total** | **9** | **3** | **2** | **100%** |")
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
    shutil.copy(os.path.join(ROOT, "catalog_lib.py"), os.path.join(d, "catalog_lib.py"))  # verify block imports it
    _write(d, "CATALOG.md", CATALOG_OK)
    _write(d, "WORKFLOW.md", "# Workflow\n")
    _write(d, "STACK.md", "# Stack\n")
    _write(d, "STACK-LEDGER.md", "# Stack Ledger\n")
    _write(d, "NEXT-EVALS.md", "# Next evals\n")
    _write(d, "WATCHLIST.md", "# Watchlist\n")
    _write(d, "PLAYBOOK.md", "# Playbook\n")
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

    def test_entry_count_comes_from_catalog_lib(self):
        # #195: the script's entry count must be catalog_lib.catalog_count, not a
        # divergent grep. A malformed row with no space after the pipe is exactly
        # where the two disagreed: grep "^|" counted it, catalog_count does not.
        with tempfile.TemporaryDirectory() as d:
            self._fixture_tree(d)
            _write(d, "CATALOG.md", CATALOG_OK + "|x | tool | one | two | none |\n")
            r = self._run(d)
            self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)
            want = catalog_lib.catalog_count(open(os.path.join(d, "CATALOG.md"), encoding="utf-8").read())
            self.assertIn(f"CATALOG.md ({want} entries)", r.stdout,
                          msg=f"count not derived from catalog_lib (want {want}): " + r.stdout)

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
        "CATALOG.md", "WORKFLOW.md", "STACK.md", "STACK-LEDGER.md", "NEXT-EVALS.md",
        "WATCHLIST.md", "PLAYBOOK.md", "evaluations/", "discovery/", "methodologies/",
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
        # the hook resolves its JSON helper next to itself (#202) — ship it along
        shutil.copy(os.path.join(ROOT, ".claude/hooks/hook-field.py"), os.path.join(d, "hook-field.py"))
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
            "NEXT-EVALS.md": "NEXT-EVALS.md", "WATCHLIST.md": "WATCHLIST.md",
            "PLAYBOOK.md": "PLAYBOOK.md",
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


# ----------------------------------------------------------------- hook trigger seam (#202)
_GATE_DRIVER = """
import { $ } from "bun"
const [worktree, pluginPath] = Bun.argv.slice(2)
const plugin = (await import(pluginPath)).default
const hooks = await plugin({ worktree, $ })
async function gate(command) {
  const output = { args: { command } }
  await hooks["tool.execute.before"]({ tool: "bash" }, output)
  return output.args.command
}
let failed = 0
const blocked = await gate("git commit -m x")
if (!blocked.includes("BLOCKED")) { console.log("FAIL commit not blocked"); failed = 1 }
const passed = await gate("git status")
if (passed !== "git status") { console.log("FAIL non-commit rewritten"); failed = 1 }
process.exit(failed)
"""


class TestHookTriggerSeam(unittest.TestCase):
    """Pins the hook trigger layer (#202): the commit predicate is one literal
    kept in lockstep across the bash and TS gate adapters (a cross-language
    share isn't practical, so this pin IS the single definition), and both bash
    hooks extract hook-JSON fields via the one shared helper instead of each
    embedding an inline-Python one-liner."""

    # The one commit predicate. Both adapters match it as a plain substring
    # (bash `case *"lit"*`, TS regex test), so they agree iff (a) each pins this
    # literal and (b) the literal has no regex metacharacters — both asserted below.
    PREDICATE = "git commit"
    GATE = ".claude/hooks/audit-gate.sh"
    HELPER = ".claude/hooks/hook-field.py"

    def _source(self, rel):
        with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
            return f.read()

    # ---- predicate pins
    def test_bash_gate_pins_the_commit_predicate(self):
        # Pin the case ARM (trailing `)`) — a bare substring check could be
        # satisfied by a comment while the actual predicate drifted.
        src = self._source(self.GATE)
        self.assertIn('case "$cmd" in', src,
                      msg="audit-gate.sh no longer dispatches on the extracted command")
        self.assertIn(f'*"{self.PREDICATE}"*)', src,
                      msg="audit-gate.sh commit predicate drifted from the pin")

    def test_opencode_gate_pins_the_commit_predicate(self):
        import re
        m = re.search(r"COMMIT_RE = /(.+?)/(\w*)", self._source(".opencode/plugins/commit-gate.ts"))
        self.assertIsNotNone(m, msg="commit-gate.ts no longer defines COMMIT_RE")
        self.assertEqual(m.group(1), self.PREDICATE,
                         msg="commit-gate.ts commit predicate drifted from the pin")
        self.assertEqual(m.group(2), "",
                         msg="regex flags (e.g. /i) would diverge from bash's case-sensitive match")

    def test_predicate_is_metacharacter_free(self):
        # With no metacharacters the TS regex test degenerates to the same
        # substring match as bash's `case *"lit"*` glob — identical semantics.
        import re
        self.assertFalse(re.search(r"[\\.^$*+?()\[\]{}|]", self.PREDICATE))

    # ---- shared JSON extraction
    def test_bash_hooks_share_the_json_helper(self):
        for rel in (self.GATE, ".claude/hooks/auto-sync.sh"):
            src = self._source(rel)
            self.assertIn("hook-field.py", src,
                          msg=f"{rel} does not use the shared JSON helper")
            self.assertNotIn("json.load(sys.stdin)", src,
                             msg=f"{rel} still embeds an inline JSON one-liner")

    def _extract(self, field, payload):
        return subprocess.run(["python3", os.path.join(ROOT, self.HELPER), field],
                              input=payload, capture_output=True, text=True)

    def test_helper_extracts_the_requested_field(self):
        r = self._extract("command", '{"tool_input": {"command": "git commit -m x"}}')
        self.assertEqual(r.returncode, 0, msg=r.stderr)
        self.assertEqual(r.stdout.strip(), "git commit -m x")

    def test_helper_missing_field_prints_empty(self):
        r = self._extract("file_path", '{"tool_input": {"command": "git status"}}')
        self.assertEqual(r.returncode, 0, msg=r.stderr)
        self.assertEqual(r.stdout.strip(), "")

    def test_helper_fails_open_on_garbage_payload(self):
        r = self._extract("command", "not json at all")
        self.assertEqual(r.returncode, 0, msg="helper must fail open, not crash")
        self.assertEqual(r.stdout.strip(), "")

    # ---- gate behavior (the predicate + helper working end-to-end)
    def _run_gate(self, d, payload):
        gate = os.path.join(d, "audit-gate.sh")
        shutil.copy(os.path.join(ROOT, self.GATE), gate)
        shutil.copy(os.path.join(ROOT, self.HELPER), os.path.join(d, "hook-field.py"))
        env = {**os.environ, "CLAUDE_PROJECT_DIR": d}
        return subprocess.run(["bash", gate], input=payload, env=env,
                              capture_output=True, text=True)

    _FAILING_AUDIT = "import sys; sys.stderr.write('detector X: fail\\n'); sys.exit(1)\n"

    def test_gate_blocks_commit_when_audit_fails(self):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "audit-evals.py", self._FAILING_AUDIT)
            r = self._run_gate(d, '{"tool_input": {"command": "git commit -m x"}}')
            self.assertEqual(r.returncode, 2, msg=r.stdout + r.stderr)
            self.assertIn("BLOCKED", r.stderr)

    def test_gate_passes_non_commit_despite_failing_audit(self):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "audit-evals.py", self._FAILING_AUDIT)
            r = self._run_gate(d, '{"tool_input": {"command": "git status"}}')
            self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)

    def test_gate_passes_commit_when_audit_clean(self):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "audit-evals.py", "import sys; sys.exit(0)\n")
            r = self._run_gate(d, '{"tool_input": {"command": "git commit -m x"}}')
            self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)

    def test_gate_fails_open_on_garbage_payload(self):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "audit-evals.py", self._FAILING_AUDIT)
            r = self._run_gate(d, "not json at all")
            self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)

    @unittest.skipUnless(shutil.which("bun"), "bun not installed; opencode gate covered by the predicate pin only")
    def test_opencode_gate_blocks_commit_and_passes_noncommit(self):
        # Executes the REAL commit-gate plugin under bun against a fixture whose
        # audit always fails — the behavioral counterpart to the predicate pin.
        with tempfile.TemporaryDirectory() as d:
            _write(d, "audit-evals.py", self._FAILING_AUDIT)
            driver = _write(d, "driver.ts", _GATE_DRIVER)
            r = subprocess.run(
                ["bun", "run", driver, d, os.path.join(ROOT, ".opencode/plugins/commit-gate.ts")],
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
            return audit.audit_evidence_field(audit.DetectorContext(d))

    def test_audit_counts_and_lists_missing(self):
        counts, missing, strong = self._run_audit({
            "a.md": "**Evidence:** MEASURED\n\n## Verdict\n\n**ADOPT**\n",
            "b.md": "**Evidence:** REVIEW\n",
            "c.md": "no field here\n",
            "TEMPLATE.md": "**Evidence:** {MEASURED | RUN | REVIEW | SOURCE-ONLY}\n",  # skipped by ctx.evals
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
            return audit.audit_stack_drift(audit.DetectorContext(d))

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
            return audit.audit_verdict_evidence(audit.DetectorContext(d))

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
            return audit.audit_verdicts(audit.DetectorContext(d))

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


# ----------------------------------------------------------------- detector B (fabrication, #200)
class TestDetectorB(unittest.TestCase):
    """audit_fabrication over fixtures (#200): the Evidence-classifier core is
    pinned by --selftest; these pin the wrapper — which evals get flagged."""

    def _run(self, files):
        with tempfile.TemporaryDirectory() as d:
            for name, text in files.items():
                _write(d, os.path.join("evaluations", name), text)
            return audit.audit_fabrication(audit.DetectorContext(d))

    def test_honest_review_and_verified_run_pass(self):
        self.assertEqual(self._run({
            "honest.md": "## How we tested it\n\nWe did not run it; source review only.\n",
            "verified.md": "## How we tested it\n\nRan it **live** via pip install; exercised the CLI.\n",
        }), [])

    def test_bare_run_claim_flagged_by_name(self):
        flagged = self._run({
            "fabber.md": "## How we tested it\n\nWe ran it on our repo and it generated the report.\n",
            "honest.md": "## How we tested it\n\nWe did not run it; source review only.\n",
        })
        self.assertEqual(flagged, ["fabber"])

    def test_eval_without_how_section_skipped(self):
        # No 'How we tested' section = nothing to classify, not a fabrication.
        self.assertEqual(self._run({"bare.md": "## Verdict\n\n**SKIP**\n"}), [])


# ----------------------------------------------------------------- detector E (skill evidence, #200)
class TestDetectorE(unittest.TestCase):
    SKILL_ROW = "| [{n}](https://github.com/a/{n}) | skill | x | y | z |\n"
    TOOL_ROW = "| [{n}](https://github.com/a/{n}) | tool | x | y | z |\n"

    def _eval(self, row, verdict, how):
        return f"{row}\n## How we tested it\n\n{how}\n\n## Verdict\n\n**{verdict}**\n"

    def _run(self, files):
        with tempfile.TemporaryDirectory() as d:
            for name, text in files.items():
                _write(d, os.path.join("evaluations", name), text)
            return audit.audit_skill_evidence(audit.DetectorContext(d))

    def test_measured_adopt_skill_vs_review_backlog(self):
        measured, backlog = self._run({
            "meas.md": self._eval(self.SKILL_ROW.format(n="meas"), "ADOPT",
                                  "**Hands-on, measured** with-skill vs baseline A/B."),
            "revw.md": self._eval(self.SKILL_ROW.format(n="revw"), "ADOPT",
                                  "Source-grounded review — not run hands-on."),
        })
        self.assertEqual(measured, ["meas"])
        self.assertEqual(backlog, ["revw"])

    def test_non_skills_and_non_adopt_skills_ignored(self):
        measured, backlog = self._run({
            "tool.md": self._eval(self.TOOL_ROW.format(n="tool"), "ADOPT",
                                  "Source-grounded review — not run hands-on."),
            "skip.md": self._eval(self.SKILL_ROW.format(n="skip"), "SKIP",
                                  "Source-grounded review — not run hands-on."),
        })
        self.assertEqual((measured, backlog), ([], []))


# ----------------------------------------------------------------- detector letter registry
class TestDetectorLetters(unittest.TestCase):
    """Detector letters are the vocabulary CLAUDE.md, the Makefile header, TEMPLATE.md,
    routines.md and the triage-lead skill all use to refer to a detector ("detector Q
    gates this", "offline detectors B/D/G/J/K/O"). Two detectors shared the letter Q for
    months, which made "detector Q" ambiguous and left one of them effectively unnamed
    in the docs (#317). Nothing misbehaved at runtime, which is exactly why it survived
    — so pin it mechanically instead of relying on review to notice the next one."""

    HEADER = re.compile(r"^# -+ ([A-Z])\. (.+)$", re.M)     # section banners in the code
    REGISTRY = re.compile(r"^  ([A-Z])\. [A-Z]", re.M)      # the module docstring's list

    def _source(self):
        with open(os.path.join(ROOT, "audit-evals.py"), encoding="utf-8") as f:
            return f.read()

    def test_every_letter_is_unique(self):
        letters = [m.group(1) for m in self.HEADER.finditer(self._source())]
        dupes = sorted({l for l in letters if letters.count(l) > 1})
        self.assertEqual(dupes, [], msg=f"detector letter(s) used twice: {dupes}")
        self.assertGreater(len(letters), 15, "header regex stopped matching — fix the test")

    def test_registry_and_sections_agree(self):
        # The docstring registry is where a reader looks up what a letter means. It had
        # silently drifted: P, Q and S existed as detectors with no registry entry at all.
        src = self._source()
        sections = {m.group(1) for m in self.HEADER.finditer(src)}
        # The registry lives in the module docstring, above the first section banner.
        registry = {m.group(1) for m in self.REGISTRY.finditer(src[:src.index("\n# ---")])}
        self.assertEqual(sections - registry, set(),
                         msg="detector(s) with a code section but no docstring registry entry")
        self.assertEqual(registry - sections, set(),
                         msg="docstring registry entr(ies) naming a detector that has no code section")


# ----------------------------------------------------------------- detector S (skill test-design, #221)
class TestDetectorS(unittest.TestCase):
    """Detector S (--skill-design, report-only): a skill/plugin-Type eval that records a
    Triggering test OR a with-skill-vs-baseline A/B is compliant; one recording neither
    is flagged. Conservative (any triggering/A/B vocab passes); never affects exit code."""
    SKILL_ROW = "| [{n}](https://github.com/a/{n}) | skill | x | y | z |\n"
    TOOL_ROW = "| [{n}](https://github.com/a/{n}) | tool | x | y | z |\n"

    def _eval(self, row, body):
        return f"{row}\n## Test design\n\n{body}\n"

    def _run(self, files):
        with tempfile.TemporaryDirectory() as d:
            for name, text in files.items():
                _write(d, os.path.join("evaluations", name), text)
            return audit.audit_skill_design(audit.DetectorContext(d))

    def test_triggering_line_compliant_bare_flagged(self):
        compliant, missing = self._run({
            "trig.md": self._eval(self.SKILL_ROW.format(n="trig"),
                                  "Triggering: 5/5 should-fire prompts fired."),
            "bare.md": self._eval(self.SKILL_ROW.format(n="bare"),
                                  "A source-grounded read of the repository."),
        })
        self.assertEqual(compliant, ["trig"])
        self.assertEqual(missing, ["bare"])

    def test_ab_line_is_compliant(self):
        compliant, missing = self._run({
            "ab.md": self._eval(self.SKILL_ROW.format(n="ab"),
                                "Ran a with-skill vs baseline A/B on four prompts."),
        })
        self.assertEqual((compliant, missing), (["ab"], []))

    def test_non_skill_type_ignored(self):
        compliant, missing = self._run({
            "tool.md": self._eval(self.TOOL_ROW.format(n="tool"),
                                  "A source-grounded read of the repository."),
        })
        self.assertEqual((compliant, missing), ([], []))


# ----------------------------------------------------------------- detector F (dangling overlaps, #200)
class TestDetectorF(unittest.TestCase):
    HEADER = "| Name | Type | One-liner | Problem | Overlaps with |\n|---|---|---|---|---|\n"

    def _row(self, name, overlaps):
        return f"| [{name}](https://github.com/a/{name}) | tool | one | two | {overlaps} |\n"

    def _run(self, catalog):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "CATALOG.md", catalog)
            return audit.audit_overlaps(audit.DetectorContext(d))

    def test_all_overlaps_resolve_no_findings(self):
        cat = self.HEADER + self._row("a", "b") + self._row("b", "a (fork)") + self._row("c", "none")
        self.assertEqual(self._run(cat), [])  # peer, parenthetical-qualified peer, and skip-vocab

    def test_uncatalogued_token_counted_across_rows_and_lowercased(self):
        cat = self.HEADER + self._row("a", "Ghost-Tool") + self._row("b", "ghost-tool, a")
        self.assertEqual(self._run(cat), [("ghost-tool", 2)])  # display-normalized, deduped

    def test_external_peer_marker_and_prose_fragments_not_flagged(self):
        cat = self.HEADER + self._row("a", "aider-style (ext.)") \
                          + self._row("b", "same repo; a much longer prose fragment here")
        self.assertEqual(self._run(cat), [])

    def test_unlinked_row_name_matches_but_contributes_no_overlaps(self):
        # An unlinked entry ("| OMEGA | ...") resolves peers' tokens, but its own
        # Overlaps cell is never scanned for gaps.
        cat = (self.HEADER + "| OMEGA | tool | one | two | ghost-tool |\n"
               + self._row("a", "OMEGA"))
        self.assertEqual(self._run(cat), [])


# ----------------------------------------------------------------- detector M (clusters without a pick, #200)
class TestDetectorM(unittest.TestCase):
    CAT_HEADER = "| Name | Type | One-liner | Problem | Overlaps with |\n|---|---|---|---|---|\n"
    COMP_HEADER = "## Plan\n| Tool | Type | Auto | Free | Evaluated |\n|---|---|---|---|---|\n"

    def _row(self, name, overlaps):
        return f"| [{name}](https://github.com/a/{name}) | tool | one | two | {overlaps} |\n"

    def _verdict(self, name, verdict):
        return f"| {name} | tool | | ✓ | {verdict} |\n"

    def _run(self, catalog, comparison):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "CATALOG.md", catalog)
            _write(d, "COMPARISON.md", comparison)
            return audit.audit_clusters(audit.DetectorContext(d))

    def test_all_conditional_cluster_flagged(self):
        cat = self.CAT_HEADER + self._row("a", "b") + self._row("b", "a")
        comp = self.COMP_HEADER + self._verdict("a", "CONDITIONAL") + self._verdict("b", "SKIP")
        self.assertEqual(self._run(cat, comp), [["a", "b"]])

    def test_cluster_with_adopt_pick_passes(self):
        cat = self.CAT_HEADER + self._row("a", "b") + self._row("b", "a")
        comp = self.COMP_HEADER + self._verdict("a", "CONDITIONAL") + self._verdict("b", "ADOPT")
        self.assertEqual(self._run(cat, comp), [])

    def test_cluster_without_conditional_not_awaiting_a_pick(self):
        # All-SKIP clusters are settled, not awaiting: nothing to flag.
        cat = self.CAT_HEADER + self._row("a", "b") + self._row("b", "a")
        comp = self.COMP_HEADER + self._verdict("a", "SKIP") + self._verdict("b", "SKIP")
        self.assertEqual(self._run(cat, comp), [])

    def test_discovery_log_cluster_also_awaiting_a_pick(self):
        # discovery-log members count as awaiting, same as CONDITIONAL (ADR 0001/#69).
        cat = self.CAT_HEADER + self._row("a", "b") + self._row("b", "a")
        comp = self.COMP_HEADER + self._verdict("a", "discovery-log") + self._verdict("b", "SKIP")
        self.assertEqual(self._run(cat, comp), [["a", "b"]])

    def test_singleton_never_flagged(self):
        cat = self.CAT_HEADER + self._row("a", "none")
        comp = self.COMP_HEADER + self._verdict("a", "CONDITIONAL")
        self.assertEqual(self._run(cat, comp), [])


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
        self.assertIn("| Stage | Tools | Validated | Recommended | Validated % |", cmp6)
        # body counts unchanged -> detector G / reconcile see the same rows
        self.assertEqual(reconcile.comparison_body_counts(cmp6), {"Plan": 2, "Ship": 1})
        self.assertEqual(backfill.rebuild_comparison(cmp6, {}), cmp6)  # idempotent
        with tempfile.TemporaryDirectory() as d:
            _write(d, "CATALOG.md", CATALOG_OK)
            _write(d, "COMPARISON.md", cmp6)
            # G still clean with the new column
            self.assertEqual(audit.audit_comparison(audit.DetectorContext(d)), [])


# ----------------------------------------------------------------- last-verified backfill (#65)
class TestLastVerifiedBackfill(unittest.TestCase):
    """Pins backfill-lastverified.py: the field lands in the header block, an existing
    hand-set date is never overwritten, and --check catches a missing field. Fixture-only."""
    DATE = "2026-06-22"

    def test_inserts_before_dev_loop_stage(self):
        # Primary anchor (TEMPLATE order): the line lands directly above **Dev loop stage:**,
        # i.e. after the Repo/Stars header block, as a consecutive metadata line.
        t = ("# Evaluation: X\n\n**Repo:** [a/x](https://github.com/a/x)\n"
             "**Stars:** 10 | **License:** MIT\n"
             "**Dev loop stage:** Plan\n**Layer:** Tooling\n")
        out = backfill_lv.backfill_text(t, self.DATE)
        self.assertIn("**Stars:** 10 | **License:** MIT\n"
                      f"**Last verified:** {self.DATE}  {backfill_lv.COMMENT}\n"
                      "**Dev loop stage:** Plan\n", out)
        self.assertEqual(backfill_lv.backfill_text(out, "2099-01-01"), out)  # idempotent

    def test_falls_back_to_evidence_line_when_no_dev_stage(self):
        # Cluster/landscape evals have no **Dev loop stage:**; the line follows **Evidence:**.
        t = "# Landscape\n\n**Evidence:** SOURCE-ONLY\n\nbody text\n"
        out = backfill_lv.backfill_text(t, self.DATE)
        self.assertIn(f"**Evidence:** SOURCE-ONLY\n**Last verified:** {self.DATE}  "
                      f"{backfill_lv.COMMENT}\n", out)

    def test_never_overwrites_hand_set_date(self):
        t = ("# Evaluation: Y\n\n**Last verified:** 2026-06-26\n"
             "**Dev loop stage:** Reflect\n")
        self.assertEqual(backfill_lv.backfill_text(t, self.DATE), t)

    def _run_check(self, d):
        return subprocess.run(["python3", "backfill-lastverified.py", "--check"],
                              cwd=d, capture_output=True, text=True)

    def test_check_flags_missing_and_passes_after_apply(self):
        # End-to-end: a temp eval with no field -> --check exits 1; add the field -> exit 0.
        with tempfile.TemporaryDirectory() as d:
            shutil.copy(os.path.join(ROOT, "backfill-lastverified.py"), d)
            _write(d, "evaluations/missing.md",
                   "# Evaluation: Z\n\n**Dev loop stage:** Plan\n**Layer:** Tooling\n")
            _write(d, "evaluations/TEMPLATE.md", "# Template\n\n**Last verified:** {date}\n")
            r = self._run_check(d)
            self.assertEqual(r.returncode, 1, msg=r.stdout + r.stderr)
            self.assertIn("missing.md", r.stdout)
            # add the field -> now clean
            _write(d, "evaluations/missing.md",
                   "# Evaluation: Z\n\n**Last verified:** 2026-06-22\n**Dev loop stage:** Plan\n")
            self.assertEqual(self._run_check(d).returncode, 0)


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
            return audit.audit_staleness(audit.DetectorContext(d), today=self.TODAY)

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


# ----------------------------------------------------------------- detector R (metadata staleness)
class TestDetectorR(unittest.TestCase):
    """Pins the repo-metadata.json age report (#260). The cache rots in ONE direction —
    a repo archived after our last fetch keeps `archived: false` and never reaches the
    P1 successor-check band — so the report exists to make that ageing visible. Age
    comes only from the `fetched_at` stamp refresh-metadata.py writes; an unstamped
    record is UNDATED, never assigned a floor, because a floor would assert a fetch
    that never happened (the `**Last triaged:**` rule, not the `**Last verified:**` one)."""

    TODAY = datetime.date(2026, 6, 22)

    def _ago(self, days):
        return (self.TODAY - datetime.timedelta(days=days)).isoformat()

    def _run(self, records, write=True):
        with tempfile.TemporaryDirectory() as d:
            if write:
                _write(d, "repo-metadata.json", json.dumps(records))
            return audit.audit_metadata_staleness(audit.DetectorContext(d), today=self.TODAY)

    def test_ages_records_by_fetched_at(self):
        total, undated, stale, oldest = self._run({
            "a/old":   {"archived": False, "fetched_at": self._ago(200)},
            "a/older": {"archived": False, "fetched_at": self._ago(300)},
            "a/fresh": {"archived": False, "fetched_at": self._ago(10)},
        })
        self.assertEqual((total, undated), (3, 0))
        self.assertEqual([s[0] for s in stale], ["a/older", "a/old"])  # oldest first
        self.assertEqual(oldest[0], "a/older")
        self.assertEqual(oldest[2], 300)

    def test_threshold_boundary_not_stale(self):
        # exactly at the threshold is NOT past it — same boundary rule as detector L
        _, _, stale, _ = self._run({"a/x": {"fetched_at": self._ago(audit.METADATA_STALE_DAYS)}})
        self.assertEqual(stale, [])

    def test_unstamped_records_are_undated_never_backfilled(self):
        # The pre-#260 record shape. pushed_at is the REPO's push date, not our fetch
        # date, so it must not be mistaken for one — a busy repo would look freshly
        # checked no matter how old the snapshot is.
        total, undated, stale, oldest = self._run({
            "a/x": {"archived": False, "license_spdx": "MIT", "pushed_at": self._ago(1)},
        })
        self.assertEqual((total, undated, stale, oldest), (1, 1, [], None))

    def test_unparseable_stamp_counts_as_undated(self):
        _, undated, _, oldest = self._run({"a/x": {"fetched_at": "not-a-date"}})
        self.assertEqual((undated, oldest), (1, None))

    def test_missing_cache_is_not_fatal(self):
        # A fresh clone has no cache; `make check` must still run. Same tolerance
        # triage.py's load_metadata() has.
        self.assertEqual(self._run({}, write=False), (0, 0, [], None))

    def test_malformed_cache_is_not_fatal(self):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "repo-metadata.json", "[]")   # a list, not the slug->record map
            self.assertEqual(
                audit.audit_metadata_staleness(audit.DetectorContext(d)), (0, 0, [], None))

    def test_report_never_affects_exit_code(self):
        # The whole point of report-only: a maximally stale cache still exits 0.
        with tempfile.TemporaryDirectory() as d:
            shutil.copy(os.path.join(ROOT, "audit-evals.py"), os.path.join(d, "audit-evals.py"))
            shutil.copy(os.path.join(ROOT, "catalog_lib.py"), os.path.join(d, "catalog_lib.py"))
            _write(d, "repo-metadata.json",
                   json.dumps({"a/x": {"fetched_at": "2001-01-01"}}))
            r = subprocess.run(["python3", "audit-evals.py", "--metadata-staleness"],
                               cwd=d, capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)
            self.assertIn("R. metadata staleness", r.stdout)

    def test_refresh_metadata_stamps_records(self):
        # The producer side: without this stamp the detector has nothing to age.
        refresh = _load("refresh_metadata", "refresh-metadata.py")
        rec = refresh.stamp({"license_spdx": "MIT", "archived": False}, today=self.TODAY)
        self.assertEqual(rec["fetched_at"], self.TODAY.isoformat())
        self.assertEqual(rec["license_spdx"], "MIT")  # original fields preserved
        # Immutable: the caller's dict is not mutated.
        original = {"license_spdx": "MIT"}
        refresh.stamp(original, today=self.TODAY)
        self.assertNotIn("fetched_at", original)


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
            return audit.audit_savings_claims(audit.DetectorContext(d))

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

    def test_no_reach_through_to_backfill(self):
        # #201: tier-stack imports the eval model directly; the two-hop
        # tier -> backfill -> audit-evals chain (and borrowed privates) is gone.
        self.assertFalse(hasattr(tier, "bf"))

    def test_tiering_split_derived_from_evidence(self):
        # amap is injected through stack_tiers' interface (#199) — no patching
        # another module's private function.
        amap = {"foo": "MEASURED", "bar": "REVIEW"}  # baz has no eval -> SOURCE-ONLY
        t1, t2 = tier.stack_tiers(self.STACK, amap)
        self.assertEqual(t1, [("foo", "MEASURED")])           # MEASURED/RUN -> Tier 1
        self.assertEqual(t2, [("bar", "REVIEW"), ("baz", "SOURCE-ONLY")])  # rest -> Tier 2

    def test_apply_replaces_between_markers_and_is_idempotent(self):
        amap = {"foo": "RUN", "bar": "REVIEW"}
        out = tier.apply(self.STACK, amap)
        self.assertIn("**Tier 1 — measured (1)", out)
        self.assertIn("foo (RUN)", out)
        self.assertIn("baz (SOURCE-ONLY)", out)
        self.assertEqual(tier.apply(out, amap), out)  # idempotent

    def test_missing_markers_exits_2(self):
        with self.assertRaises(SystemExit) as cm:
            tier.apply("# Stack with no markers\n")
        self.assertEqual(cm.exception.code, 2)


# ----------------------------------------------------------------- detector A: install resolver (#301)
class TestLinkRotUnknowns(unittest.TestCase):
    """Pins detector C's could-not-check state (#319). It used to fold every non-404
    into 'ok', so GitHub's 429 on the ~600-request unauthenticated burst turned the
    whole sweep into a silent no-op that still printed "OK — all 612 links resolve".
    A clean bill of health and a total blackout must never render identically.
    Network-free: urlopen is monkeypatched."""

    CATALOG = (
        "## Plan\n"
        "| Name | Type | One-liner | Problem | Overlaps with |\n"
        "|------|------|-----------|---------|---------------|\n"
        "| [a](https://github.com/x/a) | tool | one | two | none |\n"
        "| [b](https://github.com/x/b) | tool | one | two | none |\n"
    )

    def setUp(self):
        self._real = audit.urllib.request.urlopen

    def tearDown(self):
        audit.urllib.request.urlopen = self._real  # never leak the fake into later tests

    def _fake(self, behavior):
        def fake_urlopen(req, timeout=None):
            raise behavior(req.full_url)
        audit.urllib.request.urlopen = fake_urlopen

    def _run(self):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "CATALOG.md", self.CATALOG)
            return audit.audit_links(audit.DetectorContext(d))

    def test_rate_limit_is_unknown_not_ok(self):
        # The exact #319 failure: 429 on every request.
        self._fake(lambda url: urllib.error.HTTPError(url, 429, "Too Many Requests", {}, None))
        problems, unknowns, total = self._run()
        self.assertEqual(problems, [])
        self.assertEqual(total, 2)
        self.assertEqual(len(unknowns), 2, "a rate-limited link must not count as verified")
        self.assertEqual({r for _, r in unknowns}, {"HTTP 429"})

    def test_404_is_still_dead(self):
        # Only a 404 genuinely means "gone" — that verdict must survive the change.
        self._fake(lambda url: urllib.error.HTTPError(url, 404, "Not Found", {}, None))
        problems, unknowns, _ = self._run()
        self.assertEqual([r for _, r in problems], ["dead", "dead"])
        self.assertEqual(unknowns, [])

    def test_server_error_and_timeout_are_unknown(self):
        for behavior, expected in (
            (lambda url: urllib.error.HTTPError(url, 503, "Service Unavailable", {}, None), "HTTP 503"),
            (lambda url: TimeoutError("timed out"), "TimeoutError"),
        ):
            self._fake(behavior)
            problems, unknowns, _ = self._run()
            self.assertEqual(problems, [], msg=f"{expected} must not be reported as a finding")
            self.assertEqual({r for _, r in unknowns}, {expected})

    def test_reporting_says_inconclusive_not_ok(self):
        # End-to-end through main(): the output a maintainer actually reads must not
        # claim success when nothing could be checked.
        with tempfile.TemporaryDirectory() as d:
            shutil.copy(os.path.join(ROOT, "audit-evals.py"), os.path.join(d, "audit-evals.py"))
            shutil.copy(os.path.join(ROOT, "catalog_lib.py"), os.path.join(d, "catalog_lib.py"))
            _write(d, "CATALOG.md", self.CATALOG)
            # Force the 429 path from inside the child process.
            _write(d, "sitecustomize.py",
                   "import urllib.request, urllib.error\n"
                   "def _boom(req, timeout=None):\n"
                   "    raise urllib.error.HTTPError(req.full_url, 429, 'Too Many Requests', {}, None)\n"
                   "urllib.request.urlopen = _boom\n")
            r = subprocess.run(["python3", "audit-evals.py", "--links"],
                               cwd=d, capture_output=True, text=True,
                               env={**os.environ, "PYTHONPATH": d})
            self.assertIn("INCONCLUSIVE", r.stdout, msg=r.stdout + r.stderr)
            self.assertIn("0/2 checked", r.stdout)
            self.assertNotIn("OK — all", r.stdout,
                             msg="a fully rate-limited sweep must never print an all-clear")


class TestInstallResolver(unittest.TestCase):
    """Pins audit_installs' output shape across the serial -> concurrent rewrite (#301).
    The risk of that change is a silent detection change hiding inside a perf change, so
    these assert the two properties the rewrite had to preserve: lookups are DEDUPED (each
    unique target resolved once) but findings are reported PER OCCURRENCE (a broken package
    cited in N files yields N findings). Network-free — the checker is monkeypatched."""

    PKG = "aitoolingfixturepkg"

    def setUp(self):
        self._real_pypi = audit.pypi_exists

    def tearDown(self):
        audit.pypi_exists = self._real_pypi  # never leak the fake into later tests

    def _ctx(self, d, *rels):
        """A fixture repo where each named file cites the same pypi package exactly once."""
        for rel in rels:
            _write(d, rel, f"# {rel}\n\nRun `pip install {self.PKG}` to get it.\n")
        return audit.DetectorContext(d)

    def test_missing_binary_is_not_broken(self):
        # A checker that cannot run at all ("npm isn't installed") must resolve to
        # "cannot verify", never BROKEN — detector A gates CI, so a false BROKEN is worse
        # than an unchecked target. Before #301 this raised FileNotFoundError and took
        # down the whole run with a traceback.
        self.assertTrue(audit._run_ok(["definitely-not-a-real-binary-ai-tooling"]))

    def test_reports_every_occurrence(self):
        # Lookups dedupe; FINDINGS do not. One broken package cited in two files is two
        # findings, one per mention. The concurrent rewrite resolves unique targets, so
        # this is the property most at risk of silently collapsing to a single finding.
        audit.pypi_exists = lambda pkg: False
        with tempfile.TemporaryDirectory() as d:
            broken = audit.audit_installs(self._ctx(d, "STACK.md", "CATALOG.md"))
        self.assertEqual(broken, [("STACK.md", "pypi", self.PKG),
                                  ("CATALOG.md", "pypi", self.PKG)])

    def test_resolves_each_unique_target_once(self):
        # The whole point of the `seen` dedupe: two mentions, one network round trip.
        calls = []
        audit.pypi_exists = lambda pkg: calls.append(pkg) or False
        with tempfile.TemporaryDirectory() as d:
            audit.audit_installs(self._ctx(d, "STACK.md", "CATALOG.md"))
        self.assertEqual(calls, [self.PKG])

    def test_ok_target_is_not_reported(self):
        audit.pypi_exists = lambda pkg: True
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(audit.audit_installs(self._ctx(d, "STACK.md", "CATALOG.md")), [])


# ----------------------------------------------------------------- make check entrypoint (#114)
class TestIntegrityMakefile(unittest.TestCase):
    """Pins the `make check` entrypoint: every gate CI enforces must live in the
    check target, and integrity.yml must delegate to `make check` — so the local
    and CI gate sets provably can't drift (#114)."""

    # The full gate set CI's integrity.yml enforces, in --check/verify mode.
    GATES = (
        "audit-evals.py --offline",
        "audit-evals.py --selftest",
        "python3 -m unittest -q test_automation",
        "reconcile-counts.py --check",
        "backfill-evidence.py --check",
        "backfill-lastverified.py --check",
        "tier-stack.py --check",
        "triage.py --check",
        "watchlist.py --check",
        "sync-plugin-docs.sh --check",
        "audit-evals.py --installs",
    )

    # Report-only trailers. Deliberately NOT in GATES — they are not gates, and adding
    # them there would assert the wrong thing. They must appear in BOTH targets and stay
    # `-`-prefixed: L ages with the calendar and R's only fix (refresh-metadata.py) needs
    # the network the offline-gate invariant forbids CI from depending on. Dropping the
    # `-` would fail `make check` for a reason no code change caused.
    TRAILERS = (
        "audit-evals.py --staleness",
        "audit-evals.py --metadata-staleness",
    )

    def _target_body(self, target="check"):
        """The recipe lines of `target:`. Prefix-safe — `check-offline:` does not start
        with `check:`, so the two targets never capture each other's bodies."""
        with open(os.path.join(ROOT, "Makefile"), encoding="utf-8") as f:
            lines = f.read().splitlines()
        body, capturing = [], False
        for l in lines:
            if l.startswith(f"{target}:"):
                capturing = True
                continue
            if capturing:
                if l.startswith("\t"):
                    body.append(l.strip())
                else:
                    break  # recipe ends at the first non-tab line
        return body

    def test_check_target_runs_every_gate(self):
        body = "\n".join(self._target_body())
        self.assertTrue(body, "Makefile has no `check:` target body")
        for gate in self.GATES:
            self.assertIn(gate, body, msg=f"`make check` is missing gate: {gate}")

    def test_check_offline_omits_installs(self):
        # `check-offline` is the fast local loop (#301): every gate `check` runs EXCEPT the
        # network install resolver. Pins both halves — dropping a gate from it would make
        # the local loop quietly weaker than CI, and adding --installs back would defeat it.
        body = self._target_body("check-offline")
        self.assertTrue(body, "Makefile has no `check-offline:` target body")
        joined = "\n".join(body)
        self.assertNotIn("audit-evals.py --installs", joined,
                         "`check-offline` must not run the network install resolver")
        for gate in self.GATES:
            if gate == "audit-evals.py --installs":
                continue
            self.assertIn(gate, joined, msg=f"`make check-offline` is missing gate: {gate}")

    def test_report_only_trailers_run_in_both_targets(self):
        for target in ("check", "check-offline"):
            body = self._target_body(target)
            self.assertTrue(body, f"Makefile has no `{target}:` target body")
            for trailer in self.TRAILERS:
                line = next((l for l in body if trailer in l), None)
                self.assertIsNotNone(line, msg=f"`make {target}` is missing trailer: {trailer}")
                self.assertTrue(line.startswith("-"),
                                msg=f"`make {target}` trailer must stay `-`-prefixed "
                                    f"(report-only, never gating): {line}")

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

    def test_staleness_report_runs_in_check_non_failing(self):
        # The staleness sweep (#65) runs inside `make check` as a report — a `-`-prefixed
        # line so a stale eval can't fail the gate (only field presence, gated by
        # backfill-lastverified --check, is enforced). Pins that wiring.
        body = self._target_body()
        stale = [l for l in body if "audit-evals.py --staleness" in l]
        self.assertEqual(len(stale), 1, "`make check` must run the staleness report exactly once")
        self.assertTrue(stale[0].startswith("-"),
                        "the staleness line must be `-`-prefixed (report-only, non-failing)")

    def test_backfill_lastverified_apply_in_fix(self):
        # apply-mode backfill must run in `fix` so the field is populated before check gates it.
        with open(os.path.join(ROOT, "Makefile"), encoding="utf-8") as f:
            mk = f.read()
        self.assertRegex(mk, r"fix:[\s\S]*python3 backfill-lastverified\.py(?!\s+--check)",
                         "`make fix` must run backfill-lastverified.py in apply mode")


# ----------------------------------------------------------------- detector P: WORKFLOW↔STACK drift (report-only)
class TestWorkflowDrift(unittest.TestCase):
    """Pins detector P (audit_workflow_drift): every STACK *pick* (github owner/repo
    slug from an install-command table row) must appear somewhere in WORKFLOW.md.
    One-directional, case-insensitive, table-scoped (excluded-tool prose isn't a pick),
    report-only. Fixture-based — never the real files (plan 003)."""

    def _ctx(self, d, stack, workflow):
        _write(d, "STACK.md", stack)
        _write(d, "WORKFLOW.md", workflow)
        return audit.DetectorContext(d)

    def test_reports_pick_absent_from_workflow(self):
        # STACK has 2 picks (table rows), WORKFLOW mentions only 1 -> 1 missing.
        stack = ("## Plan\n| Tool | What | Install | Signal |\n|---|---|---|---|\n"
                 "| [a](https://github.com/own/a) | x | `pip install a` | Correctness |\n"
                 "| [b](https://github.com/own/b) | y | `pip install b` | Speed |\n")
        workflow = "### Plan\n| [a](https://github.com/own/a) — x |\n"
        with tempfile.TemporaryDirectory() as d:
            miss = audit.audit_workflow_drift(self._ctx(d, stack, workflow))
            self.assertEqual(miss, [("own/b", 5)])  # slug + first STACK line

    def test_all_picks_present_is_empty(self):
        stack = ("| Tool | What | Install | Signal |\n|---|---|---|---|\n"
                 "| [a](https://github.com/own/a) | x | `pip install a` | Correctness |\n")
        workflow = "the manual mentions [a](https://github.com/own/a) here\n"
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(audit.audit_workflow_drift(self._ctx(d, stack, workflow)), [])

    def test_excluded_prose_slug_is_not_a_pick(self):
        # A github slug named only in STACK prose (an *excluded* tool) is not a pick
        # and must not be flagged, even though it's absent from WORKFLOW.
        stack = ("| Tool | What | Install | Signal |\n|---|---|---|---|\n"
                 "| [a](https://github.com/own/a) | x | `pip install a` | Correctness |\n\n"
                 "- **excluded batch** — [b](https://github.com/own/b) didn't meet the bar.\n")
        workflow = "[a](https://github.com/own/a)\n"
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(audit.audit_workflow_drift(self._ctx(d, stack, workflow)), [])

    def test_slug_match_is_case_insensitive(self):
        # GitHub slugs are case-insensitive: STACK links Own/Repo, WORKFLOW own/repo.
        stack = ("| Tool | What | Install | Signal |\n|---|---|---|---|\n"
                 "| [a](https://github.com/Own/Repo) | x | `pip install a` | Correctness |\n")
        workflow = "[a](https://github.com/own/repo)\n"
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(audit.audit_workflow_drift(self._ctx(d, stack, workflow)), [])


# ----------------------------------------------------------------- next-evals (#plan-005)
class TestNextEvals(unittest.TestCase):
    """Pins next-evals.py's ranking and --check gate. Fixture-based — never the
    real CATALOG.md/COMPARISON.md. Only discovery-log rows are candidates; overlap
    pressure and stage gap drive the order."""

    def _ctx(self, d, catalog, comparison):
        _write(d, "CATALOG.md", catalog)
        _write(d, "COMPARISON.md", comparison)
        return audit.DetectorContext(d)

    def test_overlap_pressure_lifts_cited_tool(self):
        # `popular` is cited by three peers; `lonely` by none. Same stage, same
        # (empty) validation, so only overlap pressure separates them.
        catalog = (
            "## Plan\n"
            "| Name | Type | One-liner | Problem | Overlaps with |\n"
            "|------|------|-----------|---------|---------------|\n"
            "| [popular](https://github.com/x/popular) | tool | one | two | none |\n"
            "| [lonely](https://github.com/x/lonely) | tool | one | two | none |\n"
            "| [c1](https://github.com/x/c1) | tool | one | two | popular |\n"
            "| [c2](https://github.com/x/c2) | tool | one | two | popular |\n"
            "| [c3](https://github.com/x/c3) | tool | one | two | popular |\n"
        )
        comparison = (
            "# Tool Comparison\n\n## Plan\n\n"
            "| Tool | Type | Auto | Free | Evaluated | Evidence |\n"
            "|------|------|------|------|-----------|----------|\n"
            "| popular | tool | | ✓ | discovery-log | SOURCE-ONLY |\n"
            "| lonely | tool | | ✓ | discovery-log | SOURCE-ONLY |\n"
            "| c1 | tool | | ✓ | discovery-log | SOURCE-ONLY |\n"
            "| c2 | tool | | ✓ | discovery-log | SOURCE-ONLY |\n"
            "| c3 | tool | | ✓ | discovery-log | SOURCE-ONLY |\n"
        )
        with tempfile.TemporaryDirectory() as d:
            ranked = nexteval.rank(self._ctx(d, catalog, comparison))
            tools = [row[1] for row in ranked]
            self.assertEqual(tools[0], "popular", f"cited tool should rank first: {tools}")
            pop = next(r for r in ranked if r[1] == "popular")
            lon = next(r for r in ranked if r[1] == "lonely")
            self.assertEqual(pop[3], 3)   # overlap_pressure
            self.assertEqual(lon[3], 0)
            self.assertGreater(pop[0], lon[0])   # score

    def test_only_discovery_log_rows_are_candidates(self):
        # Evaluated verdicts (ADOPT/KEEP/SKIP/CONDITIONAL/DEFER) are already
        # evaluated and must never appear in the queue.
        catalog = (
            "## Plan\n"
            "| Name | Type | One-liner | Problem | Overlaps with |\n"
            "|------|------|-----------|---------|---------------|\n"
            "| [lead](https://github.com/x/lead) | tool | one | two | none |\n"
            "| [picked](https://github.com/x/picked) | tool | one | two | none |\n"
            "| [kept](https://github.com/x/kept) | tool | one | two | none |\n"
            "| [dropped](https://github.com/x/dropped) | tool | one | two | none |\n"
            "| [maybe](https://github.com/x/maybe) | tool | one | two | none |\n"
        )
        comparison = (
            "# Tool Comparison\n\n## Plan\n\n"
            "| Tool | Type | Auto | Free | Evaluated | Evidence |\n"
            "|------|------|------|------|-----------|----------|\n"
            "| lead | tool | | ✓ | discovery-log | SOURCE-ONLY |\n"
            "| picked | tool | | ✓ | ADOPT | MEASURED |\n"
            "| kept | tool | | ✓ | KEEP | MEASURED |\n"
            "| dropped | tool | | ✓ | SKIP | REVIEW |\n"
            "| maybe | tool | | ✓ | CONDITIONAL | RUN |\n"
        )
        with tempfile.TemporaryDirectory() as d:
            tools = [row[1] for row in nexteval.rank(self._ctx(d, catalog, comparison))]
            self.assertEqual(tools, ["lead"], f"only discovery-log rows queue: {tools}")
            for evaluated in ("picked", "kept", "dropped", "maybe"):
                self.assertNotIn(evaluated, tools)


# ----------------------------------------------------------------- triage bands (#plan-008)
class TestTriage(unittest.TestCase):
    """Pins triage.py's band assignment and --check gate. Fixture-based — never the
    real files. Bands must partition the leads exactly once; the structural bands
    (mechanical-skip, successor-check) rest on repo-metadata.json facts and outrank
    the score-based ones, EXCEPT where an eval already reads ADOPT/KEEP."""

    CATALOG = (
        "## Plan\n"
        "| Name | Type | One-liner | Problem | Overlaps with |\n"
        "|------|------|-----------|---------|---------------|\n"
        "| [plainlead](https://github.com/x/plainlead) | tool | one | two | none |\n"
        "| [badskill](https://github.com/x/badskill) | skill | one | two | none |\n"
        "| [runtool](https://github.com/x/runtool) | tool | one | two | none |\n"
        "| [oldtool](https://github.com/x/oldtool) | tool | one | two | none |\n"
        "| [rival](https://github.com/x/rival) | tool | one | two | incumbent |\n"
    )
    COMPARISON = (
        "# Tool Comparison\n\n## Plan\n\n"
        "| Tool | Type | Auto | Free | Evaluated | Evidence |\n"
        "|------|------|------|------|-----------|----------|\n"
        "| plainlead | tool | | ✓ | discovery-log | SOURCE-ONLY |\n"
        "| badskill | skill | | ✓ | discovery-log | SOURCE-ONLY |\n"
        "| runtool | tool | | ✓ | discovery-log | SOURCE-ONLY |\n"
        "| oldtool | tool | | ✓ | discovery-log | SOURCE-ONLY |\n"
        "| rival | tool | | ✓ | discovery-log | SOURCE-ONLY |\n"
    )
    STACK = "| [incumbent](https://github.com/x/incumbent) | tool | install |\n"
    # badskill: vendored + no license -> mechanical-skip. runtool: AGPL but EXECUTED,
    # never vendored -> not disposed. oldtool: archived -> successor-check.
    META = {
        "x/plainlead": {"license_spdx": "MIT", "archived": False},
        "x/badskill": {"license_spdx": "NONE", "archived": False},
        "x/runtool": {"license_spdx": "AGPL-3.0", "archived": False},
        "x/oldtool": {"license_spdx": "MIT", "archived": True},
        "x/rival": {"license_spdx": "MIT", "archived": False},
    }

    def _fixture_tree(self, d, measure_head=0):
        for fn in ("triage.py", "next-evals.py", "audit-evals.py", "catalog_lib.py"):
            shutil.copy(os.path.join(ROOT, fn), os.path.join(d, fn))
        _write(d, "CATALOG.md", self.CATALOG)
        _write(d, "COMPARISON.md", self.COMPARISON)
        _write(d, "STACK.md", self.STACK)
        _write(d, "repo-metadata.json", json.dumps(self.META))
        if measure_head is not None:  # shrink the head so the other bands are observable
            p = os.path.join(d, "triage.py")
            with open(p, encoding="utf-8") as f:
                src = f.read()
            with open(p, "w", encoding="utf-8") as f:
                f.write(src.replace("MEASURE_HEAD = 25", f"MEASURE_HEAD = {measure_head}", 1))

    def _bands(self, d):
        triage = _load("triage_fixture", os.path.join(d, "triage.py"))
        ctx = audit.DetectorContext(d)
        ordered, ranked = triage.assign(ctx)
        return {b: [r[1] for r in rows] for b, rows in ordered.items()}, ranked

    def test_structural_bands_and_vendored_scope(self):
        with tempfile.TemporaryDirectory() as d:
            self._fixture_tree(d)
            bands, ranked = self._bands(d)
            self.assertEqual(bands["P4 mechanical-skip"], ["badskill"])
            self.assertEqual(bands["P1 successor-check"], ["oldtool"])
            # AGPL on a tool you RUN is not a disposal reason — only vendored types.
            self.assertNotIn("runtool", bands["P4 mechanical-skip"])
            self.assertIn("rival", bands["P2 challenger"])
            self.assertIn("runtool", bands["P3 backlog"])
            # Every lead lands in exactly one band.
            allocated = [t for rows in bands.values() for t in rows]
            self.assertEqual(sorted(allocated), sorted(r[1] for r in ranked))
            self.assertEqual(len(allocated), len(set(allocated)))

    def test_positive_read_shields_lead_from_bulk_lane(self):
        # badskill would be mechanically SKIPped, but its eval already reads ADOPT.
        # An unattended lane may not overrule a positive human read.
        with tempfile.TemporaryDirectory() as d:
            self._fixture_tree(d)
            os.makedirs(os.path.join(d, "evaluations"), exist_ok=True)
            _write(d, "evaluations/badskill.md",
                   "# Evaluation: badskill\n\n## Verdict\n\n**ADOPT** — worth it.\n")
            bands, _ = self._bands(d)
            self.assertEqual(bands["P4 mechanical-skip"], [])
            self.assertIn("badskill", bands["P3 backlog"])

    def test_headline_verdict_not_verdict_set_shields(self):
        # "Held at CONDITIONAL rather than ADOPT" must NOT count as a positive read
        # (verdict_set contains ADOPT; the headline verdict does not).
        with tempfile.TemporaryDirectory() as d:
            self._fixture_tree(d)
            os.makedirs(os.path.join(d, "evaluations"), exist_ok=True)
            _write(d, "evaluations/badskill.md",
                   "# Evaluation: badskill\n\n## Verdict\n\n"
                   "**CONDITIONAL** — held at CONDITIONAL rather than ADOPT.\n")
            bands, _ = self._bands(d)
            self.assertEqual(bands["P4 mechanical-skip"], ["badskill"])

    def _run(self, d, *args):
        return subprocess.run(["python3", "triage.py", *args],
                              cwd=d, capture_output=True, text=True)

    def test_check_catches_drift(self):
        with tempfile.TemporaryDirectory() as d:
            self._fixture_tree(d)
            self.assertEqual(self._run(d).returncode, 0)              # generate
            self.assertEqual(self._run(d, "--check").returncode, 0)   # fresh
            p = os.path.join(d, "NEXT-EVALS.md")
            with open(p, encoding="utf-8") as f:
                text = f.read()
            with open(p, "w", encoding="utf-8") as f:
                f.write(text.replace("badskill", "ghostskill", 1))
            self.assertEqual(self._run(d, "--check").returncode, 1)   # drift caught
            self.assertEqual(self._run(d).returncode, 0)              # regenerate repairs
            self.assertEqual(self._run(d, "--check").returncode, 0)

    def test_missing_metadata_cache_is_not_fatal(self):
        # A fresh clone has no repo-metadata.json; the structural bands go empty
        # rather than the gate exploding.
        with tempfile.TemporaryDirectory() as d:
            self._fixture_tree(d)
            os.remove(os.path.join(d, "repo-metadata.json"))
            bands, _ = self._bands(d)
            self.assertEqual(bands["P4 mechanical-skip"], [])
            self.assertEqual(bands["P1 successor-check"], [])

    def test_render_computes_score_stats(self):
        # NEXT-EVALS.md's own header says "derived (not hand-maintained)", yet the
        # score-distribution sentence was typed into render() and drifted (#303).
        # Hand-built ranked rows with known statistics: 2 distinct scores, largest
        # tie 2, 2 leads at zero pressure. If any of these were hardcoded again, the
        # assertions below would read back the constant instead of the fixture.
        ranked = [
            (2.0, "a", "Plan", 3, 1.0),
            (1.0, "b", "Plan", 0, 1.0),
            (1.0, "c", "Plan", 0, 1.0),
        ]
        ordered = {name: [] for name, _, _ in triage.BANDS}
        out = triage.render(ordered, ranked)
        self.assertIn("only 2 distinct values across these 3 leads", out)
        self.assertIn("2 have zero overlap pressure", out)
        self.assertIn("largest tie: 2", out)

    def test_render_survives_an_empty_queue(self):
        # max() over no scores would raise; an exhausted queue must still render.
        out = triage.render({name: [] for name, _, _ in triage.BANDS}, [])
        self.assertIn("only 0 distinct values across these 0 leads", out)
        self.assertIn("largest tie: 0", out)


class TestBulkTriageDetector(unittest.TestCase):
    """Pins detector Q: a bulk-triaged eval may only SKIP or stay at discovery-log.
    This is what makes eliminate-only mechanical rather than a promise."""

    def _ctx(self, d, evals):
        os.makedirs(os.path.join(d, "evaluations"), exist_ok=True)
        for name, text in evals.items():
            _write(d, f"evaluations/{name}.md", text)
        _write(d, "CATALOG.md", "")
        _write(d, "COMPARISON.md", "")
        return audit.DetectorContext(d)

    def _eval(self, verdict, marked=True):
        marker = f"\n{audit.BULK_MARKER}\n" if marked else "\n"
        return f"# Evaluation: t\n{marker}\n## Verdict\n\n**{verdict}** — because.\n"

    def test_bulk_skip_passes(self):
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, {"t": self._eval("SKIP")})
            self.assertEqual(audit.audit_bulk_triage(ctx), [])

    def test_bulk_adopt_is_overreach(self):
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, {"t": self._eval("ADOPT")})
            self.assertEqual(audit.audit_bulk_triage(ctx), [("t", "ADOPT")])

    def test_bulk_conditional_is_overreach(self):
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, {"t": self._eval("CONDITIONAL")})
            self.assertEqual(audit.audit_bulk_triage(ctx), [("t", "CONDITIONAL")])

    def test_unmarked_adopt_is_untouched(self):
        # The gate constrains the bulk lane only; a human ADOPT is none of its business.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, {"t": self._eval("ADOPT", marked=False)})
            self.assertEqual(audit.audit_bulk_triage(ctx), [])

    def test_bulk_skip_whose_prose_names_adopt_passes(self):
        # verdict_set would contain ADOPT here; the headline verdict is SKIP.
        with tempfile.TemporaryDirectory() as d:
            text = (f"# Evaluation: t\n{audit.BULK_MARKER}\n\n## Verdict\n\n"
                    "**SKIP** — not an ADOPT candidate: no license.\n")
            ctx = self._ctx(d, {"t": text})
            self.assertEqual(audit.audit_bulk_triage(ctx), [])

    def test_bulk_leave_headlining_discovery_log_passes(self):
        # The lane's OTHER outcome. Before #324 a left lead borrowed a CONDITIONAL
        # headline, so it could only be expressed as the absence of a verdict and the
        # marker had to be omitted — which left the leave path unpoliced (#327). A lead
        # now headlines its own status, so the leave outcome can sign its work.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, {"t": self._eval("discovery-log — tentative read")})
            self.assertEqual(audit.audit_bulk_triage(ctx), [])

    def test_bulk_leave_that_raises_the_verdict_is_overreach(self):
        # The signed leave path is now gated: stamping the marker and promoting in the
        # same pass is exactly what eliminate-only forbids.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, {"t": self._eval("KEEP")})
            self.assertEqual(audit.audit_bulk_triage(ctx), [("t", "KEEP")])


# ----------------------------------------------------------------- detector T (lead headlines, #324)
class TestDetectorT(unittest.TestCase):
    """Detector T (--lead-headlines, report-only): a `discovery-log` COMPARISON row says
    the tool was never exercised, so its eval is notes. 324 of them headlined
    **CONDITIONAL** anyway — a word ADR-0005 grants only to a tool we ran or one carrying
    a real adopt-if gate. #324 relabelled them; this pins that they stay relabelled."""

    COMPARISON = ("| Tool | Evaluated | Evidence |\n|---|---|---|\n"
                  "| lead | discovery-log | REVIEW |\n"
                  "| real | CONDITIONAL | MEASURED |\n")

    def _run(self, name, verdict, evidence, row="lead"):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "CATALOG.md", "")
            _write(d, "COMPARISON.md", self.COMPARISON)
            _write(d, f"evaluations/{name}.md",
                   f"# Evaluation: {row}\n\n**Evidence:** {evidence}\n\n"
                   f"## Verdict\n\n**{verdict}** — because.\n")
            return audit.audit_lead_headlines(audit.DetectorContext(d))

    def test_conditional_headline_on_a_lead_is_overreach(self):
        self.assertEqual(self._run("lead", "CONDITIONAL", "REVIEW"),
                         [("lead", "CONDITIONAL", "REVIEW")])

    def test_relabelled_lead_is_clean(self):
        self.assertEqual(self._run("lead", "discovery-log — tentative read", "REVIEW"), [])

    def test_skip_headline_on_a_lead_is_clean(self):
        # SKIP is a disposal the eliminate-only lane may write; it claims nothing.
        self.assertEqual(self._run("lead", "SKIP", "SOURCE-ONLY"), [])

    def test_adopt_headline_on_a_lead_is_overreach(self):
        # The #259 category: a positive read the row hasn't caught up to.
        self.assertEqual(self._run("lead", "ADOPT", "SOURCE-ONLY"),
                         [("lead", "ADOPT", "SOURCE-ONLY")])

    def test_run_backed_conditional_is_not_a_headline_defect(self):
        # It earned the word; the stale half is the row, which is a human's verdict call.
        self.assertEqual(self._run("lead", "CONDITIONAL", "MEASURED"), [])

    def test_non_lead_row_is_none_of_its_business(self):
        self.assertEqual(self._run("real", "CONDITIONAL", "MEASURED", row="real"), [])


class TestAuditEvalsCLI(unittest.TestCase):
    """Pins audit-evals.py's flag selection at the CLI level (#300). main() had zero
    coverage — the other suites call the audit_* detectors directly and never invoke the
    script — which let two fail-open bugs live: `--offline --verdicts` ran 1 detector
    where `--offline` alone ran 7, and an unknown flag was silently dropped so `--ofline`
    ran the full default set including the network resolver, exit 0.

    Selection is now a UNION: a flag can only ADD work, and an unrecognized argument
    exits 2. Every test here is OFFLINE — none may invoke `--installs` or the no-args
    default, which hit the network and would make the suite flaky."""

    OFFLINE_HEADERS = 7  # B, D, G, O, Q, J, K — the set `--offline` selects

    def _fixture_tree(self, d):
        for fn in ("audit-evals.py", "catalog_lib.py"):
            shutil.copy(os.path.join(ROOT, fn), os.path.join(d, fn))
        os.makedirs(os.path.join(d, "evaluations"), exist_ok=True)
        _write(d, "CATALOG.md",
               "## Plan\n\n| Name | Type | One-liner | Problem | Overlaps with |\n"
               "|------|------|-----------|---------|---------------|\n")
        _write(d, "COMPARISON.md",
               "# Tool Comparison\n\n## Plan\n\n"
               "| Tool | Type | Auto | Free | Evaluated | Evidence |\n"
               "|------|------|------|------|-----------|----------|\n")
        for name in ("STACK", "WORKFLOW", "STACK-LEDGER"):
            _write(d, f"{name}.md", f"# {name}\n")

    def _run(self, d, *args):
        return subprocess.run(["python3", "audit-evals.py", *args],
                              cwd=d, capture_output=True, text=True)

    def _headers(self, res):
        """The `== X. name ==` banner lines — one per detector that actually ran."""
        return sorted(l for l in res.stdout.splitlines() if l.startswith("== "))

    def test_offline_runs_all_seven_gates(self):
        with tempfile.TemporaryDirectory() as d:
            self._fixture_tree(d)
            res = self._run(d, "--offline")
            self.assertEqual(res.returncode, 0, res.stderr)
            heads = self._headers(res)
            self.assertEqual(len(heads), self.OFFLINE_HEADERS, heads)
            for letter in ("B.", "D.", "G.", "O.", "Q.", "J.", "K."):
                self.assertTrue(any(letter in h for h in heads),
                                msg=f"detector {letter} missing from --offline: {heads}")

    def test_offline_composes_with_explicit_flag(self):
        # THE regression test for bug 1: adding a flag must not remove gates.
        with tempfile.TemporaryDirectory() as d:
            self._fixture_tree(d)
            alone = self._headers(self._run(d, "--offline"))
            plus = self._headers(self._run(d, "--offline", "--verdicts"))
            self.assertEqual(alone, plus)  # set equality, not just the count

    def test_single_flag_runs_only_that_detector(self):
        # The fix must not turn every flag into "run everything".
        with tempfile.TemporaryDirectory() as d:
            self._fixture_tree(d)
            heads = self._headers(self._run(d, "--verdicts"))
            self.assertEqual(len(heads), 1, heads)
            self.assertIn("D.", heads[0])

    def test_unknown_flag_exits_2(self):
        # THE regression test for bug 2.
        with tempfile.TemporaryDirectory() as d:
            self._fixture_tree(d)
            res = self._run(d, "--ofline")
            self.assertEqual(res.returncode, 2)
            self.assertIn("unknown argument", res.stderr)

    def test_unknown_flag_does_not_run_detectors(self):
        # Exiting 2 *after* running the network resolver would still be a bug.
        with tempfile.TemporaryDirectory() as d:
            self._fixture_tree(d)
            self.assertEqual(self._headers(self._run(d, "--ofline")), [])

    def test_selftest_still_works(self):
        # --selftest short-circuits above the unknown-flag check; it must not be rejected.
        with tempfile.TemporaryDirectory() as d:
            self._fixture_tree(d)
            res = self._run(d, "--selftest")
            self.assertEqual(res.returncode, 0, res.stderr)
            self.assertIn("selftest", res.stdout)

    def test_report_flag_does_not_affect_exit_code(self):
        # Opt-in reports stay non-gating.
        with tempfile.TemporaryDirectory() as d:
            self._fixture_tree(d)
            res = self._run(d, "--staleness")
            self.assertEqual(res.returncode, 0, res.stderr)

    def test_offline_gates_match_the_makefile_contract(self):
        # OFFLINE_GATES is the single definition of "what --offline means"; a new gating
        # detector must land there. Pins it against the count the Makefile line relies on.
        self.assertEqual(len(audit.OFFLINE_GATES), self.OFFLINE_HEADERS)
        self.assertNotIn("--installs", audit.OFFLINE_GATES)
        self.assertIn("--installs", audit.DEFAULT_GATES)
        for flag in audit.REPORT_FLAGS:
            self.assertNotIn(flag, audit.DEFAULT_GATES,
                             msg=f"{flag} is an opt-in report and must not run by default")


class TestWatchlist(unittest.TestCase):
    """Pins watchlist.py's section derivation and --check gate. Fixture-based —
    never the real files. Section 1 pulls each DEFER row's re-evaluate trigger
    from its eval's Verdict prose; section 2 grep-parses STACK's flag phrases
    (both grammatical forms). Mirrors TestNextEvals."""

    def test_deferred_extracts_trigger_and_counts_missing(self):
        # Two DEFER rows: one has an eval whose Verdict records a trigger; the
        # other has no eval, so its trigger is unrecoverable and counts as missing.
        comparison = (
            "# Tool Comparison\n\n## Plan\n\n"
            "| Tool | Type | Auto | Free | Evaluated | Evidence |\n"
            "|------|------|------|------|-----------|----------|\n"
            "| blocked | tool | | ✓ | DEFER | REVIEW |\n"
            "| orphan | tool | | ✓ | DEFER | SOURCE-ONLY |\n"
        )
        with tempfile.TemporaryDirectory() as d:
            _write(d, "COMPARISON.md", comparison)
            _write(d, "evaluations/blocked.md",
                   "# Evaluation: blocked\n\n## Verdict\n\n"
                   "**DEFER** — promising but blocked; re-evaluate after "
                   "the API stabilizes.\n")
            rows, missing = watchlist.deferred(audit.DetectorContext(d))
            by_tool = {tool: trig for tool, _stage, trig in rows}
            self.assertEqual(by_tool["blocked"], "the API stabilizes")
            self.assertEqual(by_tool["orphan"], watchlist._NO_TRIGGER)
            self.assertEqual(missing, 1)
            # stage travels with the row so section 1 can show it
            self.assertEqual({stage for _t, stage, _tr in rows}, {"Plan"})

    def test_stack_flagged_reads_both_phrase_forms(self):
        # "flagged … — [A](u) and [B](u)": tools FOLLOW the phrase, with URLs.
        # "NAME is a candidate pending …": the subject PRECEDES it, no URL.
        stack = (
            "# Stack\n\n"
            "Two fill genuine gaps and are flagged for a hands-on eval before "
            "promotion — [alpha](https://github.com/x/alpha) and "
            "[beta](https://github.com/x/beta).\n\n"
            "worktrunk is a candidate pending a hands-on eval — see #188.\n"
        )
        with tempfile.TemporaryDirectory() as d:
            _write(d, "STACK.md", stack)
            _write(d, "STACK-LEDGER.md", "# Stack Ledger\n")
            found, _lines = watchlist.stack_flagged(audit.DetectorContext(d))
            self.assertEqual({f[0] for f in found}, {"alpha", "beta", "worktrunk"})
            alpha = next(f for f in found if f[0] == "alpha")
            self.assertEqual(alpha[1], "https://github.com/x/alpha")
            worktrunk = next(f for f in found if f[0] == "worktrunk")
            self.assertIsNone(worktrunk[1])  # preceding-subject form carries no link

    def _fixture_tree(self, d):
        for fn in ("watchlist.py", "audit-evals.py", "catalog_lib.py"):
            shutil.copy(os.path.join(ROOT, fn), os.path.join(d, fn))

    def _run(self, d, *args):
        return subprocess.run(["python3", "watchlist.py", *args],
                              cwd=d, capture_output=True, text=True)

    def test_check_catches_drift(self):
        with tempfile.TemporaryDirectory() as d:
            self._fixture_tree(d)
            _write(d, "CATALOG.md",
                   "## Plan\n\n| Name | Type | One-liner | Problem | Overlaps with |\n"
                   "|------|------|-----------|---------|---------------|\n")
            _write(d, "COMPARISON.md",
                   "# Tool Comparison\n\n## Plan\n\n"
                   "| Tool | Type | Auto | Free | Evaluated | Evidence |\n"
                   "|------|------|------|------|-----------|----------|\n"
                   "| blocked | tool | | ✓ | DEFER | REVIEW |\n")
            _write(d, "STACK.md", "# Stack\n")
            _write(d, "STACK-LEDGER.md", "# Stack Ledger\n")
            self.assertEqual(self._run(d).returncode, 0)             # generate
            self.assertEqual(self._run(d, "--check").returncode, 0)  # fresh
            p = os.path.join(d, "WATCHLIST.md")
            with open(p, encoding="utf-8") as f:
                text = f.read()
            with open(p, "w", encoding="utf-8") as f:
                f.write(text.replace("what to revisit", "corrupted", 1))
            self.assertEqual(self._run(d, "--check").returncode, 1)  # drift caught
            self.assertEqual(self._run(d).returncode, 0)             # regenerate repairs
            self.assertEqual(self._run(d, "--check").returncode, 0)

    # ---------------------------------------------------------- the staleness time bomb
    # Section 3 is derived from datetime.date.today(), not from file content, so a
    # calendar date changes the page with nothing committed — 184 evals cross a threshold
    # on 2026-10-21 alone, which used to fail `watchlist.py --check` and therefore
    # `make check` and CI, on every open PR and inside every unattended routine run.
    # The section is wrapped in STALE_START/STALE_END and excluded from the comparison.
    # These three pin both halves: the gate ignores it, and `make fix` still refreshes it.

    def _stale_fixture(self, d):
        """A fixture tree whose section 3 is non-empty: one eval dated far in the past.
        Its Type resolves through the catalog row; an unresolved Type would still be
        stale via DEFAULT_STALENESS_DAYS, so the test does not depend on that lookup."""
        self._fixture_tree(d)
        _write(d, "CATALOG.md",
               "## Plan\n\n| Name | Type | One-liner | Problem | Overlaps with |\n"
               "|------|------|-----------|---------|---------------|\n"
               "| [oldtool](https://github.com/a/oldtool) | tool | x | y | — |\n")
        _write(d, "COMPARISON.md",
               "# Tool Comparison\n\n## Plan\n\n"
               "| Tool | Type | Auto | Free | Evaluated | Evidence |\n"
               "|------|------|------|------|-----------|----------|\n"
               "| blocked | tool | | ✓ | DEFER | REVIEW |\n")
        _write(d, "STACK.md", "# Stack\n")
        _write(d, "STACK-LEDGER.md", "# Stack Ledger\n")
        _write(d, "evaluations/oldtool.md",
               "# Evaluation: oldtool\n\n**Last verified:** 2020-01-01\n"
               "**Dev loop stage:** Plan\n")

    def _read(self, d):
        with open(os.path.join(d, "WATCHLIST.md"), encoding="utf-8") as f:
            return f.read()

    def test_check_ignores_stale_section_drift(self):
        # THE regression test: a changed stale set must not fail the gate.
        with tempfile.TemporaryDirectory() as d:
            self._stale_fixture(d)
            self.assertEqual(self._run(d).returncode, 0)
            text = self._read(d)
            self.assertIn("| oldtool |", text)  # section 3 really is non-empty
            i = text.find(watchlist.STALE_START)
            j = text.find(watchlist.STALE_END)
            self.assertNotEqual(i, -1)
            self.assertNotEqual(j, -1)
            # Rewrite the block as tomorrow's sweep would — different rows, different count.
            mangled = (text[:i] + watchlist.STALE_START
                       + "\n## 3. Stale / undated evals (184 stale)\n\nwholly different\n"
                       + text[j:])
            _write(d, "WATCHLIST.md", mangled)
            self.assertEqual(self._run(d, "--check").returncode, 0)

    def test_check_still_catches_drift_outside_stale_section(self):
        # The elision must not disarm the gate wholesale.
        with tempfile.TemporaryDirectory() as d:
            self._stale_fixture(d)
            self.assertEqual(self._run(d).returncode, 0)
            _write(d, "WATCHLIST.md",
                   self._read(d).replace("what to revisit", "corrupted", 1))
            self.assertEqual(self._run(d, "--check").returncode, 1)

    def test_apply_refreshes_stale_section(self):
        # `make fix` still rebuilds the section the gate ignores, so the report stays live.
        with tempfile.TemporaryDirectory() as d:
            self._stale_fixture(d)
            self.assertEqual(self._run(d).returncode, 0)
            pristine = self._read(d)
            i, j = pristine.find(watchlist.STALE_START), pristine.find(watchlist.STALE_END)
            _write(d, "WATCHLIST.md",
                   pristine[:i] + watchlist.STALE_START + "\nBOGUS\n" + pristine[j:])
            self.assertNotIn("| oldtool |", self._read(d))
            self.assertEqual(self._run(d).returncode, 0)
            self.assertEqual(self._read(d), pristine)  # fully restored
            self.assertEqual(self._run(d, "--check").returncode, 0)

    def test_missing_markers_gate_the_whole_page(self):
        # A page written before the markers existed must stay fully gated — a missing
        # marker is not a licence to skip the comparison.
        with tempfile.TemporaryDirectory() as d:
            self._stale_fixture(d)
            self.assertEqual(self._run(d).returncode, 0)
            stripped = (self._read(d)
                        .replace(watchlist.STALE_START, "")
                        .replace(watchlist.STALE_END, ""))
            _write(d, "WATCHLIST.md", stripped)
            self.assertEqual(self._run(d, "--check").returncode, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)


class TestCatalogMirror(unittest.TestCase):
    """Pins detector U: an eval's embedded `## Catalog entry` row and `**Repo:**` header
    must agree with CATALOG.md's row for the same tool (#345, #336). The block is a
    mirror with no generator and no test, which is exactly how 62% of it drifted."""

    HDR = ("| Name | Type | One-liner | Problem it solves | Overlaps with |\n"
           "|------|------|-----------|-------------------|---------------|\n")

    def _row(self, name, url, type_="tool", one="does a thing", prob="a pain", ovl="x"):
        return f"| [{name}]({url}) | {type_} | {one} | {prob} | {ovl} |\n"

    def _ctx(self, d, catalog_rows, evals):
        os.makedirs(os.path.join(d, "evaluations"), exist_ok=True)
        _write(d, "CATALOG.md", "## Plan\n\n" + self.HDR + "".join(catalog_rows))
        _write(d, "COMPARISON.md", "")
        for name, text in evals.items():
            _write(d, f"evaluations/{name}.md", text)
        return audit.DetectorContext(d)

    def _eval(self, title, repo_url, row):
        return (f"# Evaluation: {title}\n\n**Repo:** [slug]({repo_url})\n\n"
                f"## Catalog entry\n\n{self.HDR}{row}")

    def test_matching_row_is_clean(self):
        url = "https://github.com/o/t"
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [self._row("t", url)],
                            {"t": self._eval("t", url, self._row("t", url))})
            self.assertEqual(audit.audit_catalog_mirror(ctx), [])

    def test_renamed_repo_is_a_LINK_finding(self):
        # The #336 failure: CATALOG gets repointed on a rename, the eval never does.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [self._row("t", "https://github.com/new/t")],
                            {"t": self._eval("t", "https://github.com/old/t",
                                             self._row("t", "https://github.com/old/t"))})
            kinds = [f.kind for f in audit.audit_catalog_mirror(ctx)]
            self.assertEqual(kinds, ["LINK", "LINK"])  # embedded row + **Repo:** header

    def test_case_only_link_diff_is_CASE_not_LINK(self):
        # GitHub slugs are case-insensitive and redirect: this cannot make an eval
        # assert the wrong repo's facts, so it must not dilute the LINK bucket.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [self._row("t", "https://github.com/Owner/T")],
                            {"t": self._eval("t", "https://github.com/owner/t",
                                             self._row("t", "https://github.com/owner/t"))})
            self.assertEqual({f.kind for f in audit.audit_catalog_mirror(ctx)}, {"CASE"})

    def test_one_liner_drift_is_a_TEXT_finding(self):
        url = "https://github.com/o/t"
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [self._row("t", url, one="catalog wording")],
                            {"t": self._eval("t", url, self._row("t", url, one="eval wording"))})
            f, = audit.audit_catalog_mirror(ctx)
            self.assertEqual(f.kind, "TEXT")
            self.assertTrue(f.detail.startswith("one_liner:"))

    def test_overlaps_drift_is_reported(self):
        # Not cosmetic: triage.py bands leads from the overlaps cell, so which copy
        # is authoritative decides which band a lead lands in (#344).
        url = "https://github.com/o/t"
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [self._row("t", url, ovl="incumbent")],
                            {"t": self._eval("t", url, self._row("t", url, ovl="something else"))})
            f, = audit.audit_catalog_mirror(ctx)
            self.assertEqual((f.kind, f.detail.split(":")[0]), ("TEXT", "overlaps"))

    def test_embedded_row_with_no_catalog_row_is_ORPHAN(self):
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [], {"t": self._eval("t", "https://github.com/o/t",
                                                    self._row("t", "https://github.com/o/t"))})
            self.assertEqual([f.kind for f in audit.audit_catalog_mirror(ctx)], ["ORPHAN"])

    def test_eval_with_no_embedded_row_is_not_a_finding(self):
        # 110 evals carry no `## Catalog entry` block; nothing is mirrored, so nothing drifts.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [self._row("t", "https://github.com/o/t")],
                            {"t": "# Evaluation: t\n\n**Repo:** [s](https://github.com/o/t)\n"})
            self.assertEqual(audit.audit_catalog_mirror(ctx), [])

    def test_site_headed_eval_reports_no_header_finding(self):
        # A commercial platform heads with **Site:**, not **Repo:** — absence is not drift.
        url = "https://github.com/o/t"
        with tempfile.TemporaryDirectory() as d:
            text = (f"# Evaluation: t\n\n**Site:** [x](https://example.com)\n\n"
                    f"## Catalog entry\n\n{self.HDR}{self._row('t', url)}")
            ctx = self._ctx(d, [self._row("t", url)], {"t": text})
            self.assertEqual(audit.audit_catalog_mirror(ctx), [])

    def test_pack_eval_checks_every_embedded_row(self):
        # A pack eval embeds its siblings' rows too; each mirrors a catalog row.
        a, b = "https://github.com/o/a", "https://github.com/o/b"
        with tempfile.TemporaryDirectory() as d:
            text = (f"# Evaluation: pack\n\n**Repo:** [s]({a})\n\n## Catalog entry\n\n"
                    f"{self.HDR}{self._row('a', a)}{self._row('b', b, one='eval wording')}")
            ctx = self._ctx(d, [self._row("a", a), self._row("b", b, one="catalog wording")],
                            {"pack": text})
            f, = audit.audit_catalog_mirror(ctx)
            self.assertEqual((f.tool, f.kind), ("b", "TEXT"))

    def test_parenthetical_name_resolves_to_its_catalog_row(self):
        # 'GSD (gsd-core)' must find the catalog row via identity_keys, not report ORPHAN.
        url = "https://github.com/o/gsd"
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [self._row("GSD (gsd-core)", url)],
                            {"gsd": self._eval("GSD", url, self._row("GSD (gsd-core)", url))})
            self.assertEqual(audit.audit_catalog_mirror(ctx), [])

    def test_flag_is_report_only_and_exits_zero(self):
        # Report-only, per #345: a bulk fix in either direction destroys real work in
        # the other, so this prints a number to shrink and never fails a build.
        with tempfile.TemporaryDirectory() as d:
            for fn in ("audit-evals.py", "catalog_lib.py"):
                shutil.copy(os.path.join(ROOT, fn), os.path.join(d, fn))
            self._ctx(d, [self._row("t", "https://github.com/new/t")],
                      {"t": self._eval("t", "https://github.com/old/t",
                                       self._row("t", "https://github.com/old/t"))})
            r = subprocess.run(["python3", "audit-evals.py", "--catalog-mirror"],
                               cwd=d, capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("== U. catalog-entry mirror drift", r.stdout)
            self.assertIn("2 LINK", r.stdout)

    def test_flag_is_not_in_the_default_or_offline_gate_set(self):
        self.assertNotIn("--catalog-mirror", audit.DEFAULT_GATES)
        self.assertNotIn("--catalog-mirror", audit.OFFLINE_GATES)
        self.assertIn("--catalog-mirror", audit.REPORT_FLAGS)
