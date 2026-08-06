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
import datetime
import importlib.util
import json
import os
import re
import shutil
import subprocess
import tempfile
import types
import unittest
import urllib.error
from pathlib import Path
from typing import ClassVar

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
checkstars = _load("check_stars", "check-stars.py")
verifyinstalls = _load("verify_installs", "verify-installs.py")


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
            src = Path(ROOT, fn).read_text(encoding="utf-8")
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


# ----------------------------------------------------------------- Ships inside column (#343)
class TestShipsInsideColumn(unittest.TestCase):
    """Pins the 6th CATALOG column. Width is derived from each table's OWN header
    rather than from a constant: bumping CATALOG_COLUMNS to 6 would make every
    5-column `## Catalog entry` mirror in evaluations/ a finding, and accepting
    5-or-6 would let a row that LOST a middle cell parse as a valid short row —
    silently shifting Overlaps into Problem, the exact corruption detector O
    exists to catch (#198)."""

    SIX = ("| Name | Type | One-liner | Problem | Overlaps with | Ships inside |\n"
           "|---|---|---|---|---|---|\n")

    def test_ships_inside_is_parsed(self):
        r = catalog_lib.parse_catalog_rows(
            self.SIX + "| [a](https://github.com/o/a) | skill | one | two | none | o/pack |\n")[0]
        self.assertEqual(r.ships_inside, "o/pack")

    def test_absent_column_reads_as_empty_not_none(self):
        # The 5-column form is still the shape of ~520 eval mirrors; a row with no
        # cell declares no container, which is "" — never None, or every consumer
        # would need a guard.
        r = catalog_lib.parse_catalog_rows(CATALOG_OK)[0]
        self.assertEqual(r.ships_inside, "")

    def test_ships_inside_is_the_last_field(self):
        # Appended, never inserted. Detector U compares type/one_liner/overlaps
        # positionally at 1/2/4; inserting anywhere earlier would make every
        # 5-column mirror a false TEXT finding.
        self.assertEqual(catalog_lib.CatalogRow._fields[-1], "ships_inside")
        self.assertEqual(catalog_lib.CatalogRow._fields[:5],
                         ("name", "url", "type", "one_liner", "overlaps"))

    def test_six_column_table_validates_clean(self):
        text = self.SIX + "| [a](https://github.com/o/a) | skill | one | two | none | o/pack |\n"
        self.assertEqual(catalog_lib.validate_catalog_rows(text), [])

    def test_six_column_table_still_flags_a_short_row(self):
        # The point of header-derived width: under a 6-column header, a 5-cell row
        # is a hole, not a legacy row.
        text = self.SIX + "| [a](https://github.com/o/a) | skill | one | two | none |\n"
        probs = catalog_lib.validate_catalog_rows(text)
        self.assertEqual(len(probs), 1)
        self.assertIn("expected 6", probs[0][1])

    def test_five_and_six_column_tables_coexist_in_one_file(self):
        # Width resets at each header, so a file may carry both — and each table is
        # judged against its own.
        text = (CATALOG_OK + "\n## Ship\n\n" + self.SIX
                + "| [d](https://github.com/o/d) | skill | one | two | none | o/pack |\n")
        self.assertEqual(catalog_lib.validate_catalog_rows(text), [])

    def test_width_resets_between_tables_not_carried_over(self):
        # A 6-column table followed by a 5-column one must not inherit 6.
        text = (self.SIX + "| [d](https://github.com/o/d) | skill | one | two | none | o/pack |\n"
                + "\n## Plan\n\n" + CATALOG_OK.split("## Plan\n\n", 1)[1])
        self.assertEqual(catalog_lib.validate_catalog_rows(text), [])

    def test_live_catalog_is_six_columns_and_clean(self):
        text = Path(ROOT, "CATALOG.md").read_text(encoding="utf-8")
        self.assertEqual(catalog_lib.validate_catalog_rows(text), [])
        rows = catalog_lib.parse_catalog_rows(text)
        self.assertTrue(any(r.ships_inside for r in rows),
                        "the column exists but nothing declares a container")


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
        src = Path(ROOT, "test_automation.py").read_text(encoding="utf-8")
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
                              cwd=d, capture_output=True, text=True, check=False)

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
            readme = Path(d, "README.md").read_text(encoding="utf-8")
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
            plugin = Path(d, "plugin", "CLAUDE.md").read_text(encoding="utf-8")
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
                           cwd=ROOT, capture_output=True, text=True, check=False)
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
    _COUNT = re.compile(r"\b(four|five|six|seven|eight|nine)\s+quality signals\b", re.IGNORECASE)

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
        return subprocess.run(["bash", "sync-plugin-docs.sh", *args], cwd=d, capture_output=True, text=True, check=False)

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
            before = Path(cat).read_text(encoding="utf-8")
            r = self._run(d, "--check")
            self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)
            self.assertEqual(Path(cat).read_text(encoding="utf-8"), before, "check mutated plugin/docs")

    def test_entry_count_comes_from_catalog_lib(self):
        # #195: the script's entry count must be catalog_lib.catalog_count, not a
        # divergent grep. A malformed row with no space after the pipe is exactly
        # where the two disagreed: grep "^|" counted it, catalog_count does not.
        with tempfile.TemporaryDirectory() as d:
            self._fixture_tree(d)
            _write(d, "CATALOG.md", CATALOG_OK + "|x | tool | one | two | none |\n")
            r = self._run(d)
            self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)
            want = catalog_lib.catalog_count(Path(d, "CATALOG.md").read_text(encoding="utf-8"))
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
    WATCHED: ClassVar[set] = {
        "CATALOG.md", "WORKFLOW.md", "STACK.md", "STACK-LEDGER.md", "NEXT-EVALS.md",
        "WATCHLIST.md", "PLAYBOOK.md", "evaluations/", "discovery/", "methodologies/",
    }

    def test_list_watched_emits_the_syncable_set(self):
        r = subprocess.run(["bash", os.path.join(ROOT, "sync-plugin-docs.sh"), "--list-watched"],
                           capture_output=True, text=True, check=False)
        self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)
        self.assertEqual(set(r.stdout.split()), self.WATCHED)

    def test_every_listed_entry_is_actually_synced(self):
        # The list must describe real sync behavior: after an apply, each listed
        # file/dir has a counterpart under plugin/docs/.
        with tempfile.TemporaryDirectory() as d:
            _sync_fixture_tree(d)
            fixture_by_dir = {"evaluations": "foo.md", "discovery": "bar.md", "methodologies": "baz.md"}
            r = subprocess.run(["bash", "sync-plugin-docs.sh"], cwd=d, capture_output=True, text=True, check=False)
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
        payload = '{"tool_input": {"file_path": "%s"}}'.replace("%s", file_path)
        env = {**os.environ, "CLAUDE_PROJECT_DIR": d}
        return subprocess.run(["bash", hook], input=payload, env=env,
                              capture_output=True, text=True, check=False)

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
                capture_output=True, text=True, cwd=d, check=False)
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
                              input=payload, capture_output=True, text=True, check=False)

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
                              capture_output=True, text=True, check=False)

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
                capture_output=True, text=True, cwd=d, check=False)
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

    HEADER = re.compile(r"^# -+ ([A-Z])\. (.+)$", re.MULTILINE)     # section banners in the code
    REGISTRY = re.compile(r"^  ([A-Z])\. [A-Z]", re.MULTILINE)      # the module docstring's list

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

    def _run(self, catalog, home=None):
        """The counted gap bucket only — every pre-#398 assertion is about that."""
        return self._full(catalog, home)[0]

    def _full(self, catalog, home=None, skills=()):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "CATALOG.md", catalog)
            for s in skills:  # skills this repo ships, the in-tree record (#403)
                os.makedirs(os.path.join(d, "skills", s), exist_ok=True)
            # home defaults to an empty dir, NOT to the real one: a unit test must not
            # read the developer's own lockfile, or its result changes per machine.
            return audit.audit_overlaps(audit.DetectorContext(d), home or d)

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

    # --- the install join (#398) ---------------------------------------------
    # CATALOG.md's legend sanctions naming an "installed skill" as a peer, and nothing
    # checked it — the unchecked install assertion ADR-0006 removed from KEEP, one file
    # over. Detector Y already reads the records; F never asked them.

    def _home(self, d, lock=None, skills=()):
        os.makedirs(os.path.join(d, ".agents"), exist_ok=True)
        os.makedirs(os.path.join(d, ".claude", "skills"), exist_ok=True)
        if lock is not None:
            with open(os.path.join(d, ".agents", ".skill-lock.json"), "w",
                      encoding="utf-8") as fh:
                json.dump({"skills": lock}, fh)
        for s in skills:
            os.makedirs(os.path.join(d, ".claude", "skills", s), exist_ok=True)
        return d

    def test_installed_token_moves_out_of_the_counted_bucket(self):
        with tempfile.TemporaryDirectory() as h:
            self._home(h, lock={"ghost-tool": {"source": "vendor/pack"}})
            gaps, _, peers, records = self._full(self.HEADER + self._row("a", "ghost-tool"), h)
            self.assertEqual(gaps, [])
            self.assertEqual(peers, [("ghost-tool", ("installed", "vendor/pack"))])
            self.assertEqual(records, 1)

    def test_a_skills_directory_entry_also_demonstrates_the_case(self):
        # `claude install-skill` leaves no lockfile entry; the directory is the record.
        with tempfile.TemporaryDirectory() as h:
            self._home(h, skills=["ghost-tool"])
            gaps, _, peers, _ = self._full(self.HEADER + self._row("a", "ghost-tool"), h)
            self.assertEqual(gaps, [])
            self.assertEqual(peers, [("ghost-tool", ("installed", "on disk"))])

    def test_no_records_leaves_every_token_counted(self):
        # A machine with no records is a machine we know nothing about. It must behave
        # exactly as before the join — never as though nothing is installed.
        with tempfile.TemporaryDirectory() as h:
            gaps, _, peers, records = self._full(self.HEADER + self._row("a", "ghost-tool"), h)
            self.assertEqual(gaps, [("ghost-tool", 1)])
            self.assertEqual((peers, records), ([], 0))

    def test_a_catalogued_token_is_never_reported_even_when_installed(self):
        # Resolution order: the catalog answers first. An installed skill that IS
        # catalogued is not a dangling token at all.
        with tempfile.TemporaryDirectory() as h:
            self._home(h, lock={"b": {"source": "vendor/pack"}})
            gaps, _, peers, _ = self._full(
                self.HEADER + self._row("a", "b") + self._row("b", "a"), h)
            self.assertEqual((gaps, peers), ([], []))

    def test_installed_peer_is_deduped_not_counted_per_reference(self):
        # The counted bucket tallies refs because more refs mean a likelier gap. The
        # peer bucket answers a yes/no question, so a second citer adds nothing.
        with tempfile.TemporaryDirectory() as h:
            self._home(h, lock={"ghost-tool": {"source": "vendor/pack"}})
            cat = self.HEADER + self._row("a", "ghost-tool") + self._row("b", "ghost-tool")
            peers = self._full(cat, h)[2]
            self.assertEqual(peers, [("ghost-tool", ("installed", "vendor/pack"))])

    def test_record_count_is_reported_even_with_no_peers(self):
        # 0 peers across 3 records is a real answer; 0 peers across 0 records is not.
        with tempfile.TemporaryDirectory() as h:
            self._home(h, lock={"x": {"source": "v/p"}}, skills=["y", "z"])
            _, _, peers, records = self._full(self.HEADER + self._row("a", "ghost-tool"), h)
            self.assertEqual(peers, [])
            self.assertEqual(records, 3)

    # --- `(ext.)` is verified, not obeyed (#403) ------------------------------
    # A marker is only true on the day it is written. F found `aider`, the catalog
    # gained it, and the rows that raised the flag kept calling it external — an
    # assertion F was contractually silent about because it skipped the token.

    def test_marked_external_token_that_is_catalogued_is_a_counted_finding(self):
        cat = (self.HEADER + self._row("a", "b (ext.)") + self._row("b", "a"))
        gaps, stale, peers, _ = self._full(cat)
        self.assertEqual(stale, [("b", "b", "a")])  # token, catalogued as, citing row
        self.assertEqual((gaps, peers), ([], []))

    def test_a_genuinely_external_marker_stays_silent(self):
        # The 16 healthy markers (e2b, modal, semgrep, …) must keep passing untouched:
        # flagging a healthy row costs more than missing a sick one (detector V's rule).
        self.assertEqual(self._full(self.HEADER + self._row("a", "e2b (ext.)"))[1], [])

    def test_stale_ext_keys_on_identity_never_on_a_basename(self):
        # #374's trap: an alias-keyed run "resolves" `MCP (ext.)` to **mdn/mcp** by
        # slash-basename. Between two rows that each name a tool, a basename is not a
        # synonym — the marker is left alone rather than flagged against a stranger.
        cat = self.HEADER + self._row("a", "MCP (ext.)") + self._row("mdn/mcp", "a")
        self.assertEqual(self._full(cat)[1], [])

    def test_stale_ext_reports_each_citing_row_separately(self):
        # The remedy is per-row (repoint this cell), so two rows asserting the same
        # stale marker are two edits, not one deduped line.
        cat = (self.HEADER + self._row("a", "c (ext.)")
               + self._row("b", "c (ext.)") + self._row("c", "a"))
        self.assertEqual(self._full(cat)[1], [("c", "c", "a"), ("c", "c", "b")])

    # --- the two disclosures F can already read (#403) ------------------------

    def test_container_disclosed_in_the_parenthetical_is_a_peer_not_a_gap(self):
        # `systematic-debugging (superpowers)`: the row already says where the peer
        # lives, and the container is catalogued — the `Ships inside` idea (#343) done
        # informally, in the one column that has no such column.
        cat = self.HEADER + self._row("a", "ghost-skill (b)") + self._row("b", "a")
        gaps, _, peers, _ = self._full(cat)
        self.assertEqual(gaps, [])
        self.assertEqual(peers, [("ghost-skill", ("contained", "b"))])

    def test_an_undisclosed_container_stays_a_counted_candidate(self):
        # The disclosure is what settles it. Drop the parenthetical and the same token
        # is a lead again — so the bucket can never be reached by wishing.
        self.assertEqual(self._run(self.HEADER + self._row("a", "ghost-skill")
                                   + self._row("b", "a")), [("ghost-skill", 1)])

    def test_a_skill_this_repo_ships_is_a_peer_not_a_gap(self):
        # `skills/evaluate-tool/` is a real conceptual peer of a skill-evaluation tool
        # and can never be a catalog row. In-tree, versioned, offline — a stronger
        # record than the lockfile, and the only one readable in CI.
        gaps, _, peers, _ = self._full(self.HEADER + self._row("a", "evaluate-tool"),
                                       skills=["evaluate-tool"])
        self.assertEqual(gaps, [])
        self.assertEqual(peers, [("evaluate-tool", ("repo", "skills/evaluate-tool/"))])

    def test_the_catalogs_own_declaration_outranks_an_install_record(self):
        # Strongest record first (ADR-0006's split): a declaration is a fact about the
        # artifact and reproduces everywhere, an install record is a fact about one
        # laptop. Same token, both available — the declaration is what gets reported.
        with tempfile.TemporaryDirectory() as h:
            self._home(h, lock={"ghost-skill": {"source": "vendor/pack"}})
            cat = self.HEADER + self._row("a", "ghost-skill (b)") + self._row("b", "a")
            self.assertEqual(self._full(cat, h)[2], [("ghost-skill", ("contained", "b"))])


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
                              cwd=d, capture_output=True, text=True, check=False)

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
                               cwd=d, capture_output=True, text=True, check=False)
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
                               env={**os.environ, "PYTHONPATH": d}, check=False)
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
        # The two non-stdlib gates (#388). Written as the Makefile variables spell them,
        # so pointing RUFF/MYPY at a venv doesn't look like a dropped gate.
        "$(RUFF) check",
        "$(MYPY)",
        "audit-evals.py --offline",
        "audit-evals.py --selftest",
        "python3 -m unittest -q test_automation",
        "reconcile-counts.py --check",
        "backfill-evidence.py --check",
        "backfill-lastverified.py --check",
        "check-stars.py --check",
        "verify-installs.py --check",
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

    def test_lint_gates_are_pinned_and_run_first(self):
        # ruff and mypy are the only non-stdlib gates (#388), so two things must hold or
        # the build breaks for a reason no code change caused: the versions are pinned to
        # an exact release, and CI installs them. They run first in both check targets
        # because a syntax error should surface before twelve data gates parse the tree
        # with it.
        reqs = Path(ROOT, "requirements-dev.txt").read_text(encoding="utf-8")
        pins = [l.strip() for l in reqs.splitlines()
                if l.strip() and not l.strip().startswith("#")]
        self.assertTrue(pins, "requirements-dev.txt declares no pins")
        for pin in pins:
            self.assertIn("==", pin, msg=f"dev dependency is not pinned exactly: {pin}")
        self.assertTrue(any(p.startswith("ruff==") for p in pins))
        self.assertTrue(any(p.startswith("mypy==") for p in pins))

        for target in ("check", "check-offline"):
            body = self._target_body(target)
            self.assertEqual(body[:2], ["$(RUFF) check", "$(MYPY)"],
                             msg=f"`make {target}` must run the lint gates first")

        ci = Path(ROOT, ".github/workflows/integrity.yml").read_text(encoding="utf-8")
        self.assertIn("requirements-dev.txt", ci,
                      "CI must install the dev pins or `make check` cannot run the lint gates")

    def test_fix_applies_ruff_before_the_data_fixers(self):
        # `ruff check --fix` reorders imports and rewrites expressions; the data fixers
        # then regenerate derived pages from whatever the scripts now produce. Running it
        # after them would leave the tree needing a second `make fix` to settle.
        body = self._target_body("fix")
        self.assertTrue(body, "Makefile has no `fix:` target body")
        self.assertEqual(body[0], "$(RUFF) check --fix")

    def test_the_local_only_fixers_stay_out_of_fix(self):
        # `make fix` is the canonical repair and runs in CI's shadow via `check`. Two
        # apply-mode commands must never be wired into it, for the same reason from
        # different directions: `verify-installs.py --record` reads ONE laptop's install
        # records (ADR-0006), and `refresh-metadata.py` needs the network the offline-gate
        # invariant forbids CI from depending on. Their gates are shape/staleness checks
        # precisely because the apply side cannot run there.
        body = "\n".join(self._target_body("fix"))
        for local_only in ("verify-installs.py --record", "refresh-metadata.py"):
            self.assertNotIn(local_only, body,
                             msg=f"`make fix` must not run the local-only {local_only}")

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
    META: ClassVar[dict] = {
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

    # ---- #374: the shield is an identity test, so it may not use alias_keys ----
    # alias_keys adds the slash-basename so an entry installed under another name
    # resolves (GSD <- obra/superpowers). Between two rows that BOTH name a tool,
    # that basename is not a synonym but a different tool: 'vercel-labs/agent-skills'
    # keys to 'agentskills', which is addyosmani/agent-skills — an unrelated ADOPT
    # and a STACK pick. Two real leads were shielded by that stranger's verdict.
    def _collision_tree(self, d):
        """badskill (ADOPT) + vendor/badskill (a distinct lead sharing its basename)."""
        self._fixture_tree(d)
        _write(d, "CATALOG.md", self.CATALOG +
               "| [vendor/badskill](https://github.com/vendor/badskill) "
               "| skill | one | two | none |\n")
        _write(d, "COMPARISON.md", self.COMPARISON +
               "| vendor/badskill | skill | | ✓ | discovery-log | SOURCE-ONLY |\n")
        meta = dict(self.META)
        meta["vendor/badskill"] = {"license_spdx": "NONE", "archived": False}
        _write(d, "repo-metadata.json", json.dumps(meta))
        os.makedirs(os.path.join(d, "evaluations"), exist_ok=True)
        _write(d, "evaluations/badskill.md",
               "# Evaluation: badskill\n\n## Verdict\n\n**ADOPT** — worth it.\n")

    def test_basename_collision_does_not_shield_a_different_tool(self):
        # vendor/badskill has no eval of its own; badskill's ADOPT must not reach it.
        with tempfile.TemporaryDirectory() as d:
            self._collision_tree(d)
            bands, _ = self._bands(d)
            self.assertEqual(bands["P4 mechanical-skip"], ["vendor/badskill"])
            self.assertIn("badskill", bands["P3 backlog"])   # its own ADOPT still shields

    def test_slash_named_lead_is_shielded_by_its_own_positive_read(self):
        # The other direction: the fix must not cost a lead its OWN shield.
        with tempfile.TemporaryDirectory() as d:
            self._collision_tree(d)
            _write(d, "evaluations/vendor-badskill.md",
                   "# Evaluation: vendor/badskill\n\n## Verdict\n\n**KEEP** — installed.\n")
            bands, _ = self._bands(d)
            self.assertEqual(bands["P4 mechanical-skip"], [])

    def test_parenthetical_alias_still_shields(self):
        # identity_keys keeps the parenthetical-stripped form — only the basename
        # fallback is dropped. A row named 'x (y)' evaluated as 'x' stays shielded.
        with tempfile.TemporaryDirectory() as d:
            self._fixture_tree(d)
            _write(d, "CATALOG.md", self.CATALOG.replace(
                "| [badskill](https://github.com/x/badskill) | skill",
                "| [badskill (Vendor)](https://github.com/x/badskill) | skill"))
            _write(d, "COMPARISON.md", self.COMPARISON.replace(
                "| badskill | skill", "| badskill (Vendor) | skill"))
            os.makedirs(os.path.join(d, "evaluations"), exist_ok=True)
            _write(d, "evaluations/badskill.md",
                   "# Evaluation: badskill\n\n## Verdict\n\n**ADOPT** — worth it.\n")
            bands, _ = self._bands(d)
            self.assertEqual(bands["P4 mechanical-skip"], [])

    def test_triaged_sink_is_also_an_identity_test(self):
        # Same mismatch in assign()'s sort_key: last_triaged_map registers under
        # ev.name_aliases (no basenames), so a basename lookup would sink a lead
        # because a DIFFERENT tool sharing its basename was triaged. No such
        # collision exists in the corpus today — this fixture manufactures one.
        # 'vendor/badskill' has never been triaged and outranks 'zpeer' by name,
        # so it must lead; a basename lookup would sink it on badskill's stamp.
        with tempfile.TemporaryDirectory() as d:
            self._fixture_tree(d)
            _write(d, "CATALOG.md",
                   "## Plan\n"
                   "| Name | Type | One-liner | Problem | Overlaps with |\n"
                   "|------|------|-----------|---------|---------------|\n"
                   "| [badskill](https://github.com/x/badskill) | skill | one | two | none |\n"
                   "| [vendor/badskill](https://github.com/vendor/badskill) "
                   "| tool | one | two | none |\n"
                   "| [zpeer](https://github.com/x/zpeer) | tool | one | two | none |\n")
            _write(d, "COMPARISON.md",
                   "# Tool Comparison\n\n## Plan\n\n"
                   "| Tool | Type | Auto | Free | Evaluated | Evidence |\n"
                   "|------|------|------|------|-----------|----------|\n"
                   "| badskill | skill | | ✓ | ADOPT | REVIEW |\n"
                   "| vendor/badskill | tool | | ✓ | discovery-log | SOURCE-ONLY |\n"
                   "| zpeer | tool | | ✓ | discovery-log | SOURCE-ONLY |\n")
            _write(d, "repo-metadata.json", json.dumps({
                "vendor/badskill": {"license_spdx": "MIT", "archived": False},
                "x/zpeer": {"license_spdx": "MIT", "archived": False}}))
            os.makedirs(os.path.join(d, "evaluations"), exist_ok=True)
            _write(d, "evaluations/badskill.md",
                   "# Evaluation: badskill\n**Last triaged:** 2026-08-05  "
                   "<!-- triaged: human -->\n\n## Verdict\n\n**ADOPT** — worth it.\n")
            bands, _ = self._bands(d)
            self.assertEqual(bands["P3 backlog"], ["vendor/badskill", "zpeer"])

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

    # ---- #343: P5 ships-inside ----
    def _contained_tree(self, d, type_="skill", meta=None):
        """badskill declares a container, so it is not an independent lead."""
        self._fixture_tree(d)
        _write(d, "CATALOG.md",
               "## Plan\n"
               "| Name | Type | One-liner | Problem | Overlaps with | Ships inside |\n"
               "|------|------|-----------|---------|---------------|--------------|\n"
               "| [badskill](https://github.com/x/pack) | " + type_ +
               " | one | two | none | x/pack |\n"
               "| [plainlead](https://github.com/x/plainlead) | tool | one | two | none | |\n")
        _write(d, "COMPARISON.md",
               "# Tool Comparison\n\n## Plan\n\n"
               "| Tool | Type | Auto | Free | Evaluated | Evidence |\n"
               "|------|------|------|------|-----------|----------|\n"
               "| badskill | " + type_ + " | | ✓ | discovery-log | SOURCE-ONLY |\n"
               "| plainlead | tool | | ✓ | discovery-log | SOURCE-ONLY |\n")
        _write(d, "repo-metadata.json", json.dumps(meta or {
            "x/pack": {"license_spdx": "MIT", "archived": False},
            "x/plainlead": {"license_spdx": "MIT", "archived": False}}))

    def test_declared_container_bands_the_lead_as_ships_inside(self):
        with tempfile.TemporaryDirectory() as d:
            self._contained_tree(d)
            bands, _ = self._bands(d)
            self.assertEqual(bands["P5 ships-inside"], ["badskill"])
            self.assertEqual(bands["P3 backlog"], ["plainlead"])

    def test_containment_outranks_the_mechanical_bands(self):
        # A contained row's own license and archival state answer a question about
        # the WRONG artifact — those facts belong to the container. Banding it P4
        # would SKIP it for a reason that is not about it.
        with tempfile.TemporaryDirectory() as d:
            self._contained_tree(d, meta={
                "x/pack": {"license_spdx": "NONE", "archived": True},
                "x/plainlead": {"license_spdx": "MIT", "archived": False}})
            bands, _ = self._bands(d)
            self.assertEqual(bands["P5 ships-inside"], ["badskill"])
            self.assertEqual(bands["P4 mechanical-skip"], [])
            self.assertEqual(bands["P1 successor-check"], [])

    def test_an_empty_ships_inside_cell_bands_nothing(self):
        # The column is on every row; only a filled cell means containment.
        with tempfile.TemporaryDirectory() as d:
            self._contained_tree(d)
            bands, _ = self._bands(d)
            self.assertNotIn("plainlead", bands["P5 ships-inside"])

    def test_positive_read_still_shields_a_contained_row(self):
        # Eliminate-only is unchanged: P5's disposition is a SKIP, so a lead whose
        # eval already reads ADOPT must not reach it either.
        with tempfile.TemporaryDirectory() as d:
            self._contained_tree(d)
            os.makedirs(os.path.join(d, "evaluations"), exist_ok=True)
            _write(d, "evaluations/badskill.md",
                   "# Evaluation: badskill\n\n## Verdict\n\n**ADOPT** — worth it.\n")
            bands, _ = self._bands(d)
            self.assertEqual(bands["P5 ships-inside"], [])
            self.assertIn("badskill", bands["P3 backlog"])

    def test_five_column_catalog_produces_no_p5(self):
        # The column is additive: a catalog without it must band exactly as before.
        with tempfile.TemporaryDirectory() as d:
            self._fixture_tree(d)
            bands, _ = self._bands(d)
            self.assertEqual(bands["P5 ships-inside"], [])

    def _run(self, d, *args):
        return subprocess.run(["python3", "triage.py", *args],
                              cwd=d, capture_output=True, text=True, check=False)

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

    def test_unattributed_stamp_is_flagged(self):
        # #327: a `**Last triaged:**` with no marker is unpoliceable, not innocent —
        # Q cannot tell a lane that left a lead from one that raised it.
        with tempfile.TemporaryDirectory() as d:
            text = "# Evaluation: t\n**Last triaged:** 2026-08-04\n\n## Verdict\n\n**SKIP** — x.\n"
            ctx = self._ctx(d, {"t": text})
            self.assertEqual(audit.audit_bulk_triage(ctx), [("t", audit.UNATTRIBUTED)])

    def test_human_marked_stamp_is_exempt(self):
        # A human pass may reach any verdict — that is the whole difference between lanes.
        with tempfile.TemporaryDirectory() as d:
            text = (f"# Evaluation: t\n**Last triaged:** 2026-08-04  {audit.HUMAN_MARKER}\n\n"
                    "## Verdict\n\n**ADOPT** — measured.\n")
            ctx = self._ctx(d, {"t": text})
            self.assertEqual(audit.audit_bulk_triage(ctx), [])

    def test_bulk_marked_stamp_is_policed_not_merely_attributed(self):
        with tempfile.TemporaryDirectory() as d:
            text = (f"# Evaluation: t\n**Last triaged:** 2026-08-04  {audit.BULK_MARKER}\n\n"
                    "## Verdict\n\n**ADOPT** — nope.\n")
            ctx = self._ctx(d, {"t": text})
            self.assertEqual(audit.audit_bulk_triage(ctx), [("t", "ADOPT")])

    def test_eval_with_no_stamp_at_all_is_untouched(self):
        # Q's business is triage lanes; an eval nobody triaged is none of its business.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, {"t": "# Evaluation: t\n\n## Verdict\n\n**ADOPT** — fine.\n"})
            self.assertEqual(audit.audit_bulk_triage(ctx), [])


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
                              cwd=d, capture_output=True, text=True, check=False)

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
                              cwd=d, capture_output=True, text=True, check=False)

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

    # --- unlinked catalog rows are still catalogued (#401) --------------------
    # An entry with no repo to link (`| server-github | MCP server | DEPRECATED, archived
    # — superseded by github-mcp-server |`) is a catalogued tool. Excluding it from
    # IDENTITY resolution made its own eval's mirror a false ORPHAN. Detector F already
    # draws this line: unlinked entries name-match only.

    def test_unlinked_catalog_row_resolves_its_mirror(self):
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, ["| t | tool | does a thing | a pain | x |\n"],
                            {"t": self._eval("t", "https://github.com/o/t",
                                             self._row("t", "https://github.com/o/t"))})
            self.assertEqual([f.kind for f in audit.audit_catalog_mirror(ctx)], [])

    def test_unlinked_catalog_row_is_never_a_link_finding(self):
        # There is no URL on the catalog side to compare against, so a mirror that
        # carries one is not a disagreement — reporting LINK here would demand the eval
        # drop a working link to match an absence.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, ["| t | tool | does a thing | a pain | x |\n"],
                            {"t": self._eval("t", "https://github.com/o/other",
                                             self._row("t", "https://github.com/o/other"))})
            self.assertEqual([f.kind for f in audit.audit_catalog_mirror(ctx)], [])

    def test_unlinked_catalog_row_still_reports_text_drift(self):
        # Indexing the row is not the same as excusing it. Once it resolves, its cells
        # are compared like any other row's — the finding becomes TRUE, not absent.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, ["| t | tool | catalog wording | a pain | x |\n"],
                            {"t": self._eval("t", "https://github.com/o/t",
                                             self._row("t", "https://github.com/o/t"))})
            finds = audit.audit_catalog_mirror(ctx)
            self.assertEqual([f.kind for f in finds], ["TEXT"])
            self.assertIn("one_liner", finds[0].detail)

    def test_a_genuinely_uncatalogued_tool_is_still_ORPHAN(self):
        # The fix must not swallow the real class: nothing named `t` exists here.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, ["| other | tool | does a thing | a pain | x |\n"],
                            {"t": self._eval("t", "https://github.com/o/t",
                                             self._row("t", "https://github.com/o/t"))})
            self.assertEqual([f.kind for f in audit.audit_catalog_mirror(ctx)], ["ORPHAN"])

    def test_live_tree_has_no_orphan_or_case_findings(self):
        # The #401 backlog, pinned at zero. TEXT is deliberately NOT pinned — #345's
        # sequencing note is that it stays a human's per-row call.
        finds = audit.audit_catalog_mirror(audit.DetectorContext(ROOT))
        self.assertEqual([f"{f.kind} {f.eval_name}" for f in finds
                          if f.kind in ("ORPHAN", "CASE", "LINK", "AMBIG")], [])

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
                               cwd=d, capture_output=True, text=True, check=False)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("== U. catalog-entry mirror drift", r.stdout)
            self.assertIn("2 LINK", r.stdout)

    def test_flag_is_not_in_the_default_or_offline_gate_set(self):
        self.assertNotIn("--catalog-mirror", audit.DEFAULT_GATES)
        self.assertNotIn("--catalog-mirror", audit.OFFLINE_GATES)
        self.assertIn("--catalog-mirror", audit.REPORT_FLAGS)

    def test_hyphen_collision_resolves_by_exact_name(self):
        # name_key collapses non-alphanumerics, so 'agent-skills' and 'agentskills' key
        # identically. A single collapsed-key map handed one eval the OTHER tool's row
        # and reported a LINK against it — a detector reporting a defect that isn't.
        a = "https://github.com/addyosmani/agent-skills"
        b = "https://github.com/agentskills/agentskills"
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [self._row("agent-skills", a), self._row("agentskills", b)],
                            {"agentskills": self._eval("agentskills", b,
                                                       self._row("agentskills", b))})
            self.assertEqual(audit.audit_catalog_mirror(ctx), [])

    def test_collapsed_key_reaching_two_rows_is_AMBIG_not_a_guess(self):
        # No exact match, and the fallback key reaches two distinct tools: resolve to
        # nothing and say so, rather than to whichever row happened to come first.
        a = "https://github.com/one/agent-skills"
        b = "https://github.com/two/agent_skills"
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [self._row("agent-skills", a), self._row("agent_skills", b)],
                            {"e": self._eval("e", a, self._row("agentskills", a))})
            f, = audit.audit_catalog_mirror(ctx)
            self.assertEqual(f.kind, "AMBIG")
            self.assertIn("agentskills", f.detail)

    def test_header_documenting_a_rename_is_not_drift(self):
        # `[old](…) — **now redirects to** [new](…)` is richer than the catalog's single
        # link, not stale. Accept the header when the catalog URL appears anywhere on it.
        old, new = "https://github.com/o/old", "https://github.com/o/new"
        with tempfile.TemporaryDirectory() as d:
            text = (f"# Evaluation: t\n\n**Repo:** [old]({old}) — **now redirects to** "
                    f"[new]({new})\n\n## Catalog entry\n\n{self.HDR}{self._row('t', new)}")
            ctx = self._ctx(d, [self._row("t", new)], {"t": text})
            self.assertEqual(audit.audit_catalog_mirror(ctx), [])

    def test_header_naming_only_the_old_repo_is_still_drift(self):
        old, new = "https://github.com/o/old", "https://github.com/o/new"
        with tempfile.TemporaryDirectory() as d:
            text = (f"# Evaluation: t\n\n**Repo:** [old]({old})\n\n"
                    f"## Catalog entry\n\n{self.HDR}{self._row('t', new)}")
            ctx = self._ctx(d, [self._row("t", new)], {"t": text})
            # only the header is stale here — the embedded row already matches
            self.assertEqual([f.kind for f in audit.audit_catalog_mirror(ctx)], ["LINK"])


class TestMaintenanceSignal(unittest.TestCase):
    """Pins detector V and the refresher's discontinuation regex (#351). `archived` only
    catches maintainers who flipped the flag; daytona announced death in its README, kept
    `archived: false`, and sat in P3 backlog for two months."""

    HDR = ("| Name | Type | One-liner | Problem it solves | Overlaps with |\n"
           "|------|------|-----------|-------------------|---------------|\n")

    def _ctx(self, d, records, rows=("daytona", "https://github.com/daytonaio/daytona"),
             verdict="ADOPT", one_liner="x"):
        os.makedirs(os.path.join(d, "evaluations"), exist_ok=True)
        name, url = rows
        _write(d, "CATALOG.md", "## Implement\n\n" + self.HDR +
               f"| [{name}]({url}) | tool | {one_liner} | y | z |\n")
        _write(d, "COMPARISON.md",
               "# Tool Comparison\n\n## Implement\n\n"
               "| Tool | Type | Auto | Free | Evaluated | Evidence |\n"
               "|------|------|------|------|-----------|----------|\n"
               f"| {name} | tool | y | y | {verdict} | REVIEW |\n")
        _write(d, "repo-metadata.json", json.dumps(records))
        return audit.DetectorContext(d)

    def test_discontinued_readme_is_reported_with_its_verdict(self):
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, {"daytonaio/daytona": {
                "archived": False, "license_spdx": "404",
                "discontinued": "no longer maintained", "license_lost": True}})
            finds, collected, acked = audit.audit_maintenance(ctx)
            self.assertEqual((collected, acked), (1, []))
            self.assertEqual([f.kind for f in finds], ["DISCONTINUED", "LICENSE-LOST"])
            self.assertEqual(finds[0].verdict, "ADOPT")
            self.assertEqual(finds[0].tool, "daytona")

    def test_archived_false_is_not_a_free_pass(self):
        # The whole point: this record would never reach the P1 successor-check band.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, {"daytonaio/daytona": {
                "archived": False, "license_spdx": "MIT", "discontinued": "is discontinued"}})
            finds, _, _ = audit.audit_maintenance(ctx)
            self.assertEqual(len(finds), 1)

    def test_healthy_record_is_clean(self):
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, {"daytonaio/daytona": {
                "archived": False, "license_spdx": "MIT",
                "discontinued": None, "license_lost": False}})
            self.assertEqual(audit.audit_maintenance(ctx), ([], 1, []))

    def test_uncollected_signal_reports_zero_records_not_zero_findings(self):
        # Absence of the field means "not collected", never "nothing is dead" — the
        # count is what distinguishes them, so it must not read as a clean bill.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, {"daytonaio/daytona": {"archived": False, "license_spdx": "MIT"}})
            self.assertEqual(audit.audit_maintenance(ctx), ([], 0, []))

    def test_missing_cache_is_not_an_exception(self):
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "evaluations"), exist_ok=True)
            _write(d, "CATALOG.md", ""); _write(d, "COMPARISON.md", "")
            self.assertEqual(audit.audit_maintenance(audit.DetectorContext(d)), ([], 0, []))

    def test_strongest_verdict_sorts_first(self):
        # A dead tool we RECOMMEND outranks a dead lead nobody was going to reach.
        with tempfile.TemporaryDirectory() as d:
            _write(d, "CATALOG.md", "## Implement\n\n" + self.HDR +
                   "| [a](https://github.com/o/a) | tool | x | y | z |\n"
                   "| [b](https://github.com/o/b) | tool | x | y | z |\n")
            _write(d, "COMPARISON.md",
                   "# T\n\n## Implement\n\n| Tool | Type | Auto | Free | Evaluated | Evidence |\n"
                   "|---|---|---|---|---|---|\n"
                   "| a | tool | y | y | discovery-log | REVIEW |\n"
                   "| b | tool | y | y | ADOPT | RUN |\n")
            _write(d, "repo-metadata.json", json.dumps({
                "o/a": {"discontinued": "is discontinued"},
                "o/b": {"discontinued": "no longer maintained"}}))
            os.makedirs(os.path.join(d, "evaluations"), exist_ok=True)
            finds, _, _ = audit.audit_maintenance(audit.DetectorContext(d))
            self.assertEqual([f.tool for f in finds], ["b", "a"])

    def test_flag_is_report_only_and_opt_in(self):
        self.assertIn("--maintenance", audit.REPORT_FLAGS)
        self.assertNotIn("--maintenance", audit.DEFAULT_GATES)
        self.assertNotIn("--maintenance", audit.OFFLINE_GATES)

    # --- the acknowledgment escape hatch (#360) -------------------------------
    # V's second false-positive class is not mechanically separable: giskard-oss says
    # "no longer actively maintained" of Giskard **v2** while the repo ships v3. No regex
    # resolves a phrase's subject, so a human's judgement has to be recordable — but
    # narrowly, or the hatch becomes a mute button.

    def test_acked_finding_is_returned_apart_and_not_counted_as_a_finding(self):
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, {"daytonaio/daytona": {
                "discontinued": "no longer actively maintained",
                "discontinued_ack": {"phrase": "no longer actively maintained",
                                     "why": "said of v2; repo ships v3"}}})
            finds, collected, acked = audit.audit_maintenance(ctx)
            self.assertEqual(finds, [])
            self.assertEqual(collected, 1)          # still collected, just not a finding
            self.assertEqual([f.kind for f in acked], ["DISCONTINUED"])
            self.assertIn("no longer actively maintained", acked[0].detail)

    def test_ack_pins_the_phrase_so_a_new_banner_reports_again(self):
        # The whole point of pinning: a stale ack must not shield a repo that later
        # gains a genuine repo-level banner.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, {"daytonaio/daytona": {
                "discontinued": "this repository is deprecated",
                "discontinued_ack": {"phrase": "no longer actively maintained"}}})
            finds, _, acked = audit.audit_maintenance(ctx)
            self.assertEqual([f.kind for f in finds], ["DISCONTINUED"])
            self.assertEqual(acked, [])

    def test_ack_does_not_silence_a_lost_license(self):
        # The ack is scoped to the README phrase it names; license_lost is a different
        # signal and must survive it.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, {"daytonaio/daytona": {
                "discontinued": "no longer maintained", "license_spdx": "404",
                "license_lost": True,
                "discontinued_ack": {"phrase": "no longer maintained"}}})
            finds, _, acked = audit.audit_maintenance(ctx)
            self.assertEqual([f.kind for f in finds], ["LICENSE-LOST"])
            self.assertEqual([f.kind for f in acked], ["DISCONTINUED"])

    def test_malformed_ack_does_not_silence(self):
        # A bare string or a missing phrase is not a grant. Fail toward reporting.
        for ack in ("no longer maintained", {}, {"why": "trust me"}, None, []):
            with tempfile.TemporaryDirectory() as d:
                ctx = self._ctx(d, {"daytonaio/daytona": {
                    "discontinued": "no longer maintained", "discontinued_ack": ack}})
                finds, _, acked = audit.audit_maintenance(ctx)
                self.assertEqual([f.kind for f in finds], ["DISCONTINUED"], ack)
                self.assertEqual(acked, [], ack)

    # --- the CATALOG disclosure sub-signal (#395) -----------------------------
    # The verdict lives in COMPARISON.md and the eval; the catalog row is what a reader
    # scans. All three live findings advertised dead projects in the present tense.

    def test_undisclosed_row_is_reported_as_such(self):
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, {"daytonaio/daytona": {"discontinued": "no longer maintained"}},
                            one_liner="Secure sandbox infrastructure (AGPL-3.0, 72K stars)")
            finds, _, _ = audit.audit_maintenance(ctx)
            self.assertFalse(finds[0].disclosed)

    def test_disclosing_row_is_not_a_gap(self):
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, {"daytonaio/daytona": {"discontinued": "no longer maintained"}},
                            one_liner="⚠️ discontinued (June 2026) — secure sandbox infra")
            finds, _, _ = audit.audit_maintenance(ctx)
            self.assertTrue(finds[0].disclosed)

    def test_the_existing_archived_note_convention_counts_as_disclosure(self):
        # 23 rows already carry a `⚠️ archived` note; the sub-signal must recognize the
        # convention that is there rather than demand one exact new word.
        for note in ("⚠️ archived (2024) — browser agents",
                     "one of the original CLIs (⚠️ repo no longer maintained)",
                     "an editor (⚠️ main repo archived)",
                     "sunset by its vendor", "deprecated in favour of X",
                     "development has moved to a private codebase"):
            with tempfile.TemporaryDirectory() as d:
                ctx = self._ctx(d, {"daytonaio/daytona": {"discontinued": "no longer maintained"}},
                                one_liner=note)
                finds, _, _ = audit.audit_maintenance(ctx)
                self.assertTrue(finds[0].disclosed, note)

    def test_disclosure_is_read_from_the_whole_row_not_just_the_one_liner(self):
        # A row may disclose in its problem statement instead; flagging it would push a
        # human to re-add a note that is already there.
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "evaluations"), exist_ok=True)
            _write(d, "CATALOG.md", "## Implement\n\n" + self.HDR +
                   "| [daytona](https://github.com/daytonaio/daytona) | tool | sandboxes "
                   "| historical reference; the repo is discontinued | e2b |\n")
            _write(d, "COMPARISON.md",
                   "# T\n\n## Implement\n\n| Tool | Type | Auto | Free | Evaluated | Evidence |\n"
                   "|---|---|---|---|---|---|\n| daytona | tool | y | y | SKIP | REVIEW |\n")
            _write(d, "repo-metadata.json",
                   json.dumps({"daytonaio/daytona": {"discontinued": "no longer maintained"}}))
            finds, _, _ = audit.audit_maintenance(audit.DetectorContext(d))
            self.assertTrue(finds[0].disclosed)

    def test_a_record_with_no_catalog_row_is_not_a_disclosure_gap(self):
        # There is no row to fix, so counting it would put a number on the board that
        # nothing in this repo can move.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, {"o/uncatalogued": {"discontinued": "no longer maintained"}})
            finds, _, _ = audit.audit_maintenance(ctx)
            self.assertEqual(finds[0].tool, "o/uncatalogued")
            self.assertTrue(finds[0].disclosed)

    def test_an_acked_false_positive_is_never_pushed_toward_disclosure(self):
        # V's rule: a match is a candidate, not a disposition. An acked finding is not a
        # finding, so it cannot contribute to the undisclosed count either.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, {"daytonaio/daytona": {
                "discontinued": "no longer maintained",
                "discontinued_ack": {"phrase": "no longer maintained", "why": "said of v2"}}})
            finds, _, acked = audit.audit_maintenance(ctx)
            self.assertEqual(finds, [])
            self.assertEqual(len(acked), 1)

    def test_lost_license_carries_no_disclosure_claim(self):
        # Scoped to DISCONTINUED: a row already prints its license, so there is nothing
        # for a reader to be misled about in the same way.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, {"daytonaio/daytona": {
                "license_spdx": "404", "license_lost": True}})
            finds, _, _ = audit.audit_maintenance(ctx)
            self.assertEqual([f.kind for f in finds], ["LICENSE-LOST"])
            self.assertTrue(finds[0].disclosed)

    def test_live_findings_all_disclose(self):
        # The #395 backlog, pinned at zero: a discontinued row must say so where a
        # reader sees it, not only in the eval one file away.
        finds, collected, _ = audit.audit_maintenance(audit.DetectorContext(ROOT))
        if collected:                       # only meaningful once --maintenance has run
            undisclosed = [f.tool for f in finds if not f.disclosed]
            self.assertEqual(undisclosed, [])

    def test_real_giskard_record_is_acked_in_the_committed_cache(self):
        # Pins the disposition itself: the live record must carry an ack whose phrase
        # matches its own banner, or the sweep regrows a finding a human already judged.
        with open(os.path.join(ROOT, "repo-metadata.json"), encoding="utf-8") as fh:
            rec = json.load(fh).get("giskard-ai/giskard-oss", {})
        if rec.get("discontinued"):     # only meaningful once --maintenance has run
            self.assertEqual(rec["discontinued_ack"]["phrase"], rec["discontinued"])
            self.assertIn("why", rec["discontinued_ack"])


class TestInstallRecords(unittest.TestCase):
    """Pins detector Y (#366). KEEP is DEFINED as the validated-INSTALLED status and
    nothing checked the installed half — so three STACK members turned out to be name
    collisions with an artifact from a different source."""

    HDR = ("| Name | Type | One-liner | Problem it solves | Overlaps with |\n"
           "|------|------|-----------|-------------------|---------------|\n")

    def _home(self, d, lock=None, plugins=None, skill_dirs=(), cache=()):
        os.makedirs(os.path.join(d, ".agents"), exist_ok=True)
        os.makedirs(os.path.join(d, ".claude", "plugins"), exist_ok=True)
        os.makedirs(os.path.join(d, ".claude", "skills"), exist_ok=True)
        for market, plugin, version in cache:   # cache/<marketplace>/<plugin>/<version>
            os.makedirs(os.path.join(d, ".claude", "plugins", "cache",
                                     market, plugin, version), exist_ok=True)
        if lock is not None:
            with open(os.path.join(d, ".agents", ".skill-lock.json"), "w") as fh:
                json.dump({"version": 3, "skills": lock}, fh)
        if plugins is not None:
            with open(os.path.join(d, ".claude", "plugins", "installed_plugins.json"), "w") as fh:
                json.dump({"version": 2, "plugins": plugins}, fh)
        for s in skill_dirs:
            os.makedirs(os.path.join(d, ".claude", "skills", s), exist_ok=True)
        return d

    def _ctx(self, d, rows, verdicts, typ="skill"):
        os.makedirs(os.path.join(d, "evaluations"), exist_ok=True)
        _write(d, "CATALOG.md", "## Implement\n\n" + self.HDR + "".join(
            f"| [{n}]({u}) | {typ} | x | y | z |\n" for n, u in rows))
        _write(d, "COMPARISON.md",
               "# T\n\n## Implement\n\n"
               "| Tool | Type | Auto | Free | Evaluated | Evidence |\n"
               "|---|---|---|---|---|---|\n" + "".join(
                   f"| {n} | {typ} | y | y | {v} | REVIEW |\n" for n, v in verdicts))
        return audit.DetectorContext(d)

    @staticmethod
    def _lock(**pairs):
        return {n: {"source": s, "sourceType": "github"} for n, s in pairs.items()}

    def test_same_name_from_another_source_is_a_collision(self):
        # code-review: ADOPT-as-anthropics/claude-plugins-official, but what is symlinked
        # in is mattpocock/skills' own code-review — a different tool, same name.
        with tempfile.TemporaryDirectory() as d, tempfile.TemporaryDirectory() as h:
            ctx = self._ctx(d, [("code-review", "https://github.com/anthropics/official")],
                            [("code-review", "KEEP")])
            self._home(h, lock=self._lock(**{"code-review": "mattpocock/skills"}))
            finds, _, _ = audit.audit_installed(ctx, home=h)
            # mattpocock/skills is also UNCATALOGUED in this fixture; that is correct and
            # separate, so scope the assertion to the collision under test.
            hits = [f for f in finds if f.kind != "UNCATALOGUED"]
            self.assertEqual([(f.kind, f.tool) for f in hits], [("COLLISION", "code-review")])
            self.assertIn("mattpocock/skills", hits[0].detail)

    def test_matching_slug_is_clean(self):
        with tempfile.TemporaryDirectory() as d, tempfile.TemporaryDirectory() as h:
            ctx = self._ctx(d, [("thing", "https://github.com/o/pack")], [("thing", "ADOPT")])
            self._home(h, lock=self._lock(thing="o/pack"))
            self.assertEqual(audit.audit_installed(ctx, home=h)[0], [])

    # ---- #366: the slug is asked FIRST; a name shadow is not a missing install ----
    def test_installed_slug_under_a_shadowed_name_is_not_a_collision(self):
        # caveman (ADOPT, JuliusBrussee/caveman) ships caveman-commit/-compress/-help/
        # -review, all installed. The bare name 'caveman' in the lockfile belongs to
        # mattpocock/skills. Asking the name first reported the row as an unbacked
        # ADOPT, which it is not.
        with tempfile.TemporaryDirectory() as d, tempfile.TemporaryDirectory() as h:
            ctx = self._ctx(d, [("caveman", "https://github.com/JuliusBrussee/caveman")],
                            [("caveman", "ADOPT")])
            self._home(h, lock=self._lock(**{"caveman": "mattpocock/skills",
                                             "caveman-review": "JuliusBrussee/caveman"}))
            finds, shadowed, _ = audit.audit_installed(ctx, home=h)
            self.assertEqual([f.tool for f in finds if f.kind != "UNCATALOGUED"], [])
            self.assertEqual([(f.kind, f.tool) for f in shadowed],
                             [("SHADOWED", "caveman")])
            self.assertIn("mattpocock/skills", shadowed[0].detail)

    def test_shadow_is_only_reported_when_a_name_really_resolves_elsewhere(self):
        # Installed under its own name: nothing to report in either bucket.
        with tempfile.TemporaryDirectory() as d, tempfile.TemporaryDirectory() as h:
            ctx = self._ctx(d, [("thing", "https://github.com/o/pack")], [("thing", "ADOPT")])
            self._home(h, lock=self._lock(thing="o/pack"))
            finds, shadowed, _ = audit.audit_installed(ctx, home=h)
            self.assertEqual(finds, [])
            self.assertEqual(shadowed, [])

    def test_slug_absent_and_name_taken_is_still_a_collision(self):
        # The fix must not weaken the real finding: code-review's row slug is NOT
        # installed, and the name belongs to someone else. That stays a COLLISION.
        with tempfile.TemporaryDirectory() as d, tempfile.TemporaryDirectory() as h:
            ctx = self._ctx(d, [("code-review", "https://github.com/anthropics/official")],
                            [("code-review", "KEEP")])
            self._home(h, lock=self._lock(**{"code-review": "mattpocock/skills"}))
            finds, shadowed, _ = audit.audit_installed(ctx, home=h)
            self.assertEqual([f.kind for f in finds if f.kind != "UNCATALOGUED"],
                             ["COLLISION"])
            self.assertEqual(shadowed, [])

    def test_shadowed_rows_are_not_counted_as_findings(self):
        # The headline is a number to shrink; a row a human cannot fix (someone else
        # named their skill the same) must not inflate it. V's `acked` rule.
        with tempfile.TemporaryDirectory() as d, tempfile.TemporaryDirectory() as h:
            ctx = self._ctx(d, [("caveman", "https://github.com/o/caveman")],
                            [("caveman", "ADOPT")])
            self._home(h, lock=self._lock(**{"caveman": "someone/else",
                                             "caveman-x": "o/caveman"}))
            finds, shadowed, _ = audit.audit_installed(ctx, home=h)
            self.assertNotIn("caveman", [f.tool for f in finds])
            self.assertEqual(len(shadowed), 1)

    def test_a_directory_answers_for_a_slug_with_no_lock_entry(self):
        # claude install-skill and npm globals leave no lockfile entry. The directory
        # fallback is what keeps NO-RECORD from being mostly noise.
        with tempfile.TemporaryDirectory() as d, tempfile.TemporaryDirectory() as h:
            ctx = self._ctx(d, [("thing", "https://github.com/o/pack")], [("thing", "ADOPT")])
            self._home(h, lock={}, skill_dirs=("thing",))
            self.assertEqual(audit.audit_installed(ctx, home=h)[0], [])

    def test_nothing_answering_at_all_is_no_record(self):
        with tempfile.TemporaryDirectory() as d, tempfile.TemporaryDirectory() as h:
            ctx = self._ctx(d, [("thing", "https://github.com/o/pack")], [("thing", "ADOPT")])
            self._home(h, lock=self._lock(other="x/y"))
            finds, _, _ = audit.audit_installed(ctx, home=h)
            self.assertEqual([(f.kind, f.tool) for f in finds][:1], [("NO-RECORD", "thing")])

    def test_installed_source_with_no_catalog_row_is_uncatalogued(self):
        # Found from the install side: a scan only ever looks at what EXISTS, never at
        # what is already running here.
        with tempfile.TemporaryDirectory() as d, tempfile.TemporaryDirectory() as h:
            ctx = self._ctx(d, [("thing", "https://github.com/o/pack")], [("thing", "ADOPT")])
            self._home(h, lock=self._lock(thing="o/pack", extra="who/dis"))
            finds, _, _ = audit.audit_installed(ctx, home=h)
            self.assertEqual([(f.kind, f.tool) for f in finds], [("UNCATALOGUED", "who/dis")])

    def test_only_installable_types_are_judged(self):
        # A CLI or MCP server is installed by npm, brew or a settings entry — none of
        # which leaves a mark in these records, so flagging it would be pure noise.
        with tempfile.TemporaryDirectory() as d, tempfile.TemporaryDirectory() as h:
            ctx = self._ctx(d, [("ripgrep", "https://github.com/bs/ripgrep")],
                            [("ripgrep", "ADOPT")], typ="tool")
            self._home(h, lock=self._lock(other="x/y"))
            finds, _, _ = audit.audit_installed(ctx, home=h)
            self.assertEqual([f.tool for f in finds if f.kind != "UNCATALOGUED"], [])

    # ---- #366: a fetched version in the plugin cache is not "nothing answers" ----
    def test_unknown_cache_version_is_still_no_record(self):
        # #332's trap: a directory under the cache means the MARKETPLACE was added.
        # `unknown` is listing metadata for code that was never pulled.
        with tempfile.TemporaryDirectory() as d, tempfile.TemporaryDirectory() as h:
            ctx = self._ctx(d, [("feature-dev", "https://github.com/anthropics/official")],
                            [("feature-dev", "KEEP")], typ="plugin")
            self._home(h, lock={}, skill_dirs=("unrelated",),
                       cache=[("official", "feature-dev", "unknown")])
            finds, _, _ = audit.audit_installed(ctx, home=h)
            self.assertEqual([(f.kind, f.tool) for f in finds],
                             [("NO-RECORD", "feature-dev")])

    def test_an_unknown_only_cache_is_not_knowledge_about_this_machine(self):
        # A machine whose ONLY evidence is `unknown` cache dirs has told us the
        # marketplace was added and nothing else — 0 records, so no findings at all,
        # rather than a sweep that flags every row against metadata it cannot read.
        with tempfile.TemporaryDirectory() as d, tempfile.TemporaryDirectory() as h:
            ctx = self._ctx(d, [("feature-dev", "https://github.com/anthropics/official")],
                            [("feature-dev", "KEEP")], typ="plugin")
            self._home(h, cache=[("official", "feature-dev", "unknown")])
            self.assertEqual(audit.audit_installed(ctx, home=h), ([], [], 0))

    def test_real_cache_version_is_cache_only_not_no_record(self):
        # A version string means this machine pulled the code. Still a finding — a
        # fetch is not an activation — but "nothing answers to this row" is false.
        with tempfile.TemporaryDirectory() as d, tempfile.TemporaryDirectory() as h:
            ctx = self._ctx(d, [("claude-reflect", "https://github.com/b/claude-reflect")],
                            [("claude-reflect", "KEEP")], typ="plugin")
            self._home(h, lock={}, cache=[("reflect-marketplace", "claude-reflect", "3.1.0")])
            finds, _, _ = audit.audit_installed(ctx, home=h)
            self.assertEqual([(f.kind, f.tool) for f in finds],
                             [("CACHE-ONLY", "claude-reflect")])
            self.assertIn("3.1.0", finds[0].detail)

    def test_every_fetched_version_is_reported_never_a_latest(self):
        # These are opaque strings — semver AND commit shas — so a lexicographic max
        # reads 13.11.0 as older than 13.4.0. Report the set; invent no order.
        with tempfile.TemporaryDirectory() as d, tempfile.TemporaryDirectory() as h:
            ctx = self._ctx(d, [("claude-mem", "https://github.com/t/claude-mem")],
                            [("claude-mem", "ADOPT")], typ="plugin")
            self._home(h, lock={}, cache=[("t", "claude-mem", "13.11.0"),
                                          ("t", "claude-mem", "13.4.0"),
                                          ("t", "claude-mem", "unknown")])
            finds, _, _ = audit.audit_installed(ctx, home=h)
            self.assertEqual(finds[0].kind, "CACHE-ONLY")
            self.assertIn("13.11.0", finds[0].detail)
            self.assertIn("13.4.0", finds[0].detail)
            self.assertNotIn("unknown", finds[0].detail)

    def test_an_install_record_still_outranks_the_cache(self):
        # A real install must not be downgraded to CACHE-ONLY by its own cache entry.
        with tempfile.TemporaryDirectory() as d, tempfile.TemporaryDirectory() as h:
            ctx = self._ctx(d, [("thing", "https://github.com/o/pack")],
                            [("thing", "ADOPT")], typ="plugin")
            self._home(h, lock=self._lock(thing="o/pack"),
                       cache=[("m", "thing", "1.0.0")])
            finds, _, _ = audit.audit_installed(ctx, home=h)
            self.assertEqual(finds, [])

    def test_no_records_reports_zero_records_not_zero_findings(self):
        # V's rule: absence of a record is "nothing known about this machine", never
        # "nothing is installed".
        with tempfile.TemporaryDirectory() as d, tempfile.TemporaryDirectory() as h:
            ctx = self._ctx(d, [("thing", "https://github.com/o/pack")], [("thing", "ADOPT")])
            self.assertEqual(audit.audit_installed(ctx, home=h), ([], [], 0))

    def test_malformed_records_do_not_raise(self):
        with tempfile.TemporaryDirectory() as d, tempfile.TemporaryDirectory() as h:
            ctx = self._ctx(d, [("thing", "https://github.com/o/pack")], [("thing", "ADOPT")])
            os.makedirs(os.path.join(h, ".agents"))
            with open(os.path.join(h, ".agents", ".skill-lock.json"), "w") as fh:
                fh.write("{not json")
            self.assertEqual(audit.audit_installed(ctx, home=h), ([], [], 0))

    def test_flag_is_local_only_and_never_a_gate(self):
        # CI has no lockfile. A build that fails for a reason no code change caused is
        # worse than the drift it would catch.
        self.assertIn("--installed", audit.REPORT_FLAGS)
        self.assertNotIn("--installed", audit.DEFAULT_GATES)
        self.assertNotIn("--installed", audit.OFFLINE_GATES)

    def test_installed_flag_does_not_trigger_the_installs_resolver(self):
        # The two flags differ by two characters and the wiring reused one variable, so
        # `--installed` silently ran detector A's ~50 network requests.
        with open(os.path.join(ROOT, "audit-evals.py"), encoding="utf-8") as fh:
            src = fh.read()
        self.assertIn('do_inst = "--installs" in want', src)
        self.assertIn('do_instrec = "--installed" in want', src)


class TestCollapsedIdentity(unittest.TestCase):
    """Pins detector X (#343). A row naming a COMPONENT of an artifact catalogued as a
    WHOLE is not an independent lead — mattpocock/skills produced three separate P3 leads
    for skills that all ship in one pack the catalog already ADOPTs."""

    HDR = ("| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |\n"
           "|------|------|-----------|-------------------|---------------|--------------|\n")

    def _ctx(self, d, catalog_rows, verdicts):
        """catalog_rows is (name, url) or (name, url, ships_inside)."""
        os.makedirs(os.path.join(d, "evaluations"), exist_ok=True)
        _write(d, "CATALOG.md", "## Implement\n\n" + self.HDR + "".join(
            f"| [{r[0]}]({r[1]}) | skill | x | y | z | {r[2] if len(r) > 2 else ''} |\n"
            for r in catalog_rows))
        _write(d, "COMPARISON.md",
               "# T\n\n## Implement\n\n"
               "| Tool | Type | Auto | Free | Evaluated | Evidence |\n"
               "|---|---|---|---|---|---|\n" + "".join(
                   f"| {n} | skill | y | y | {v} | REVIEW |\n" for n, v in verdicts))
        return audit.DetectorContext(d)

    PACK = "https://github.com/o/pack"

    def test_lead_sharing_a_link_with_an_adopt_row_is_settled(self):
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [("pack", self.PACK), ("skill-a", self.PACK)],
                            [("pack", "ADOPT"), ("skill-a", "discovery-log")])
            finds, _ = audit.audit_identity(ctx)
            self.assertEqual([(f.kind, f.tool, f.verdict) for f in finds],
                             [("SETTLED", "skill-a", "ADOPT")])

    def test_two_undecided_facets_are_collapsed_not_settled(self):
        # jira + confluence: one repo, neither disposed. A redundancy verdict between
        # them would be meaningless — that is the same thing, not a competitor.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [("jira", self.PACK), ("confluence", self.PACK)],
                            [("jira", "discovery-log"), ("confluence", "discovery-log")])
            finds, _ = audit.audit_identity(ctx)
            self.assertEqual([f.kind for f in finds], ["COLLAPSED", "COLLAPSED"])
            self.assertEqual(finds[0].peers, ("jira",))

    def test_distinct_subpaths_are_faceted_and_never_counted(self):
        # THE precision rule. claude-plugins-official is 8 rows over 8 subpaths — a
        # monorepo of independently-installable plugins, not one artifact counted 8 times.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [("a", self.PACK + "/tree/main/plugins/a"),
                                ("b", self.PACK + "/tree/main/plugins/b")],
                            [("a", "discovery-log"), ("b", "discovery-log")])
            finds, context = audit.audit_identity(ctx)
            self.assertEqual(finds, [])
            self.assertEqual([f.kind for f in context], ["FACETED"])

    def test_collapsed_group_with_no_leads_is_context_not_a_finding(self):
        # The identity is still collapsed, but no queue slot is wasted. Reported so the
        # group is not silently invisible; not counted, because there is nothing to do.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [("a", self.PACK), ("b", self.PACK)],
                            [("a", "ADOPT"), ("b", "ADOPT")])
            finds, context = audit.audit_identity(ctx)
            self.assertEqual(finds, [])
            self.assertEqual([f.kind for f in context], ["NO-LEADS"])

    def test_a_lone_row_is_never_a_group(self):
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [("a", self.PACK)], [("a", "discovery-log")])
            self.assertEqual(audit.audit_identity(ctx), ([], []))

    def test_flag_is_report_only_and_opt_in(self):
        # #343 chose the `Ships inside` column, and triage.py's P5 band excludes declared
        # facets from the queue as a consequence. The detector itself stays report-only:
        # it reports what is NOT yet declared, and merging rows is still not its call.
        self.assertIn("--identity", audit.REPORT_FLAGS)
        self.assertNotIn("--identity", audit.DEFAULT_GATES)
        self.assertNotIn("--identity", audit.OFFLINE_GATES)

    # ---- DECLARED: the column is how a finding stops being one (#343)
    def test_a_group_that_names_its_container_is_declared_not_counted(self):
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [("pack", self.PACK), ("skill-a", self.PACK, "o/pack")],
                            [("pack", "ADOPT"), ("skill-a", "discovery-log")])
            finds, context = audit.audit_identity(ctx)
            self.assertEqual(finds, [], "a declared container is not a finding")
            self.assertEqual([f.kind for f in context], ["DECLARED"])

    def test_the_container_row_s_own_empty_cell_is_not_a_hole(self):
        # The pack row does not ship inside itself. A group qualifies when every member
        # either names its container or IS the container the others name.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [("pack", self.PACK), ("a", self.PACK, "o/pack"),
                                ("b", self.PACK, "o/pack")],
                            [("pack", "ADOPT"), ("a", "discovery-log"), ("b", "discovery-log")])
            finds, context = audit.audit_identity(ctx)
            self.assertEqual(finds, [])
            self.assertEqual([f.kind for f in context], ["DECLARED"])

    def test_a_partly_declared_group_is_still_a_finding(self):
        # Declaring one row does not settle the other. The undeclared lead stays counted,
        # or the column would let a group half-disappear.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [("a", self.PACK, "o/pack"), ("b", self.PACK)],
                            [("a", "discovery-log"), ("b", "discovery-log")])
            finds, context = audit.audit_identity(ctx)
            self.assertEqual([(f.kind, f.tool) for f in finds], [("COLLAPSED", "b")])
            self.assertEqual(context, [])

    def test_declared_is_checked_before_the_link_shape_split(self):
        # A monorepo whose rows link distinct subpaths AND declare their container is
        # reported by the stronger fact: the catalog says so, rather than the detector
        # inferring it from the link shape.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [("a", self.PACK + "/tree/main/a", "o/pack"),
                                ("b", self.PACK + "/tree/main/b", "o/pack")],
                            [("a", "discovery-log"), ("b", "discovery-log")])
            _, context = audit.audit_identity(ctx)
            self.assertEqual([f.kind for f in context], ["DECLARED"])

    def test_live_run_has_no_undeclared_collapsed_identity(self):
        # Guards the real tree. mattpocock/skills is the case #343 was filed over and
        # claude-plugins-official is the false positive the link-shape split must avoid;
        # both now carry the column, so the finding count is the number the column was
        # added to drive to zero. A NEW collapsed group would break this, which is the point.
        finds, context = audit.audit_identity(audit.DetectorContext(ROOT))
        self.assertEqual(finds, [], f"undeclared collapsed identity: {finds}")
        declared = {f.slug for f in context if f.kind == "DECLARED"}
        self.assertIn("mattpocock/skills", declared)
        self.assertIn("anthropics/claude-plugins-official", declared)


class TestScopeMismatch(unittest.TestCase):
    """Pins detector W (#353). next-evals.py's score has no scope term — every term
    measures how much attention a lead attracts — so a row WORKFLOW.md's one-line
    exclusion already disposes of can rank into P0, the one band an unattended pass may
    not write to. pydantic-ai sits there at pressure 12 while agent-kit, same class, was
    disposed in P3."""

    def test_concession_vocab_matches_the_codified_exclusion(self):
        # The two dominant corpus strings ARE WORKFLOW.md's exclusion, quoted verbatim by
        # the #348 SKIP pass. If they stop matching, the detector has gone blind.
        for s in ("for building AI products",
                  "not for your own dev workflow",
                  "it builds LLM apps, not coding agents",
                  "not a drop-in coding harness",
                  "tangential to authoring code"):
            self.assertTrue(audit.SCOPE_CONCESSION.search(s), s)

    def test_clearance_vocab_recognizes_the_bridge_arguments(self):
        # Real strings from evals that quote the exclusion IN ORDER TO distinguish
        # themselves from it. Each would otherwise be a false positive.
        for s in ("fast-agent clears the bar that aisuite and LangGraph did not",
                  "it is not a library for building AI products, but a harness you run",
                  "catalog-relevant as the obs/eval layer",
                  "with one genuine bridge into Implement"):
            self.assertTrue(audit.SCOPE_CLEARED.search(s), s)

    def test_type_gate_is_the_types_the_exclusion_is_about(self):
        # "Visual/programmatic agent BUILDERS". A harness or tool is something you run —
        # the gate is what drops mirrord ("not a coding agent", said of a k8s tool) and
        # 12-factor-agents (a reference). Both survive the phrase match alone.
        self.assertEqual(audit.SCOPE_TYPES, frozenset({"framework", "platform"}))

    def test_quote_is_line_scoped(self):
        # A sentence-scoped window ran past the newline and spliced a header into a prose
        # line, which reads as a garbled claim rather than as the eval's own words.
        text = "**Dev loop stage:** X — for building AI products\n**Layer:** Infrastructure"
        m = audit.SCOPE_CONCESSION.search(text)
        self.assertNotIn("Layer", audit._scope_quote(text, m))

    def test_flag_is_report_only_and_opt_in(self):
        # The immediate item is a HUMAN read of a P0 lead. Moving that authority to an
        # unattended lane is precisely what #353 declined to do.
        self.assertIn("--scope", audit.REPORT_FLAGS)
        self.assertNotIn("--scope", audit.DEFAULT_GATES)
        self.assertNotIn("--scope", audit.OFFLINE_GATES)

    def test_lazy_triage_import_does_not_recurse(self):
        # triage.py loads audit-evals.py at import time; a module-level import back would
        # recurse forever. This is the regression net for that.
        mod = audit._load_sibling("triage_probe", "triage.py")
        self.assertTrue(hasattr(mod, "assign"))

    def test_live_run_separates_findings_from_cleared(self):
        # End-to-end against the real tree: the detector must not report a lead that
        # argues it clears the bar as a finding.
        finds, cleared = audit.audit_scope(audit.DetectorContext(ROOT))
        self.assertEqual({f.tool for f in finds} & {c.tool for c in cleared}, set())
        for f in finds + cleared:
            self.assertIn(f.typ, audit.SCOPE_TYPES)
            self.assertTrue(f.phrase.strip(), f.tool)


class TestAckCarryForward(unittest.TestCase):
    """`discontinued_ack` is the one field in repo-metadata.json that a human writes and
    the refresher does not own. If a refresh drops it, V's acknowledged false positive
    silently regrows and the judgement call has to be made again (#360)."""

    def _mod(self):
        spec = importlib.util.spec_from_file_location(
            "refresh_metadata", os.path.join(ROOT, "refresh-metadata.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def _run(self, mod, stdout=None, boom=None):
        """Stub `gh` so this stays offline: either a canned payload or a failure.

        Swaps the module's `subprocess` REFERENCE for a shim rather than assigning
        `mod.subprocess.run` — the latter mutates the real stdlib module and breaks
        every other test in this file."""
        def fake(cmd, **kw):
            if boom:
                raise boom
            return types.SimpleNamespace(stdout=stdout)
        mod.subprocess = types.SimpleNamespace(
            run=fake, CalledProcessError=subprocess.CalledProcessError)
        return mod

    PAYLOAD = ('{"license_spdx":"MIT","archived":false,"stars":1,'
               '"pushed_at":"2026-08-05","resolved_name":"o/r"}')
    ACK: ClassVar[dict] = {"phrase": "no longer actively maintained", "why": "said of v2"}

    def test_plain_refresh_preserves_the_ack(self):
        # The common case: a routine refresh with no --maintenance flag must not erase it.
        mod = self._run(self._mod(), stdout=self.PAYLOAD)
        rec = mod.fetch("o/r", today=datetime.date(2026, 8, 5), previous={"discontinued_ack": self.ACK})
        self.assertEqual(rec["discontinued_ack"], self.ACK)
        self.assertEqual(rec["license_spdx"], "MIT")

    def test_unreachable_repo_still_preserves_the_ack(self):
        # A transient `gh` failure must not cost a human decision.
        mod = self._run(self._mod(), boom=FileNotFoundError("gh"))
        rec = mod.fetch("o/r", today=datetime.date(2026, 8, 5), previous={"discontinued_ack": self.ACK})
        self.assertEqual(rec["discontinued_ack"], self.ACK)
        self.assertEqual(rec["license_spdx"], mod.UNREACHABLE)

    def test_no_previous_ack_adds_no_field(self):
        mod = self._run(self._mod(), stdout=self.PAYLOAD)
        self.assertNotIn("discontinued_ack", mod.fetch("o/r", today=datetime.date(2026, 8, 5)))


class TestDiscontinuationRegex(unittest.TestCase):
    """The README banner is the HIGH-PRECISION signal, deliberately not a pushed_at
    threshold: dormancy is not discontinuation. plandex was SKIPped at 13 months because
    a coding agent rots when model APIs turn over; ralph was left at ~6 because an
    autonomous loop is a pattern over whatever harness you point it at."""

    def _rx(self):
        spec = importlib.util.spec_from_file_location(
            "refresh_metadata", os.path.join(ROOT, "refresh-metadata.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod.DISCONTINUED

    def test_matches_real_banners(self):
        rx = self._rx()
        for text in (
            "This repository is no longer maintained. As of June 2026, Daytona's core "
            "development has moved to a private codebase.",
            "> **This project is discontinued.**",
            "This repo is deprecated - use the successor instead.",
            "The repository is now read-only.",
            "This repository will receive no further updates, fixes, or releases.",
            "NOTE: this package is not actively maintained.",
        ):
            self.assertIsNotNone(rx.search(text), text)

    def test_does_not_match_healthy_readmes(self):
        rx = self._rx()
        for text in (
            "Actively maintained and used in production by hundreds of teams.",
            "A fast, well-maintained toolkit for building agents.",
            "Maintained by the core team. Contributions welcome.",
            "Supports read-only mode for safe inspection.",
            # Both real, both live tools, both flagged by a bare `is read-only` on the
            # detector's first collection run. A false positive costs trust in every
            # other finding; a miss costs one stale row.
            "This command is read-only and will not perform any changes.",
            "The closing `final-review` is read-only. It returns `REVIEW: GREEN`.",
        ):
            self.assertIsNone(rx.search(text), text)

    def test_matches_a_repo_that_really_is_read_only(self):
        rx = self._rx()
        self.assertIsNotNone(rx.search("This repository is read-only for all users."))


# ----------------------------------------------------- Z. unread license declaration (#372)
class TestLicenseDeclared(unittest.TestCase):
    """Pins detector Z, the refresher's license-declaration parsers, and triage.py's
    effective_license (#372).

    `license_spdx: NONE` is what GitHub returns when there is no root LICENSE file — its
    licensee detector reads nothing else. It was recorded, and read by P4 mechanical-skip,
    as though it meant the repo grants nothing, and for 9 of 28 records it did not:
    `andrej-karpathy-skills` and `web-access` were SKIPped "text carrying no license grant
    cannot be copied in" against a README reading `## License` / `MIT`."""

    HDR = ("| Name | Type | One-liner | Problem it solves | Overlaps with |\n"
           "|------|------|-----------|-------------------|---------------|\n")

    def _refresh(self):
        return _load("refresh_metadata", "refresh-metadata.py")

    # --- the parsers -----------------------------------------------------------
    def test_readme_license_reads_the_whole_file_not_the_head(self):
        # A discontinuation banner is at the TOP or it is not a banner; a license section
        # is at the BOTTOM. vercel-labs/agent-skills' is at line 226, well past README_HEAD.
        m = self._refresh()
        text = "# Tool\n\n" + ("filler paragraph.\n" * 400) + "\n## License\n\nMIT\n"
        self.assertGreater(len(text), m.README_HEAD)
        found = m.readme_license(text)
        self.assertEqual(found[0], "MIT")
        self.assertIn("License", found[1])

    def test_readme_license_quotes_what_it_matched(self):
        # Detector V's rule: a human judges the wording, not the regex.
        m = self._refresh()
        spdx, phrase = m.readme_license("## License\n\nThis repository is licensed under "
                                        "the Apache License 2.0.\n")
        self.assertEqual(spdx, "Apache-2.0")
        self.assertIn("Apache License 2.0", phrase)

    def test_no_heading_or_no_name_is_no_declaration(self):
        m = self._refresh()
        self.assertIsNone(m.readme_license("# Tool\n\nA thing that does things.\n"))
        self.assertIsNone(m.readme_license("## License\n\nSee the LICENSE file.\n"))

    def test_family_precedence_never_reads_agpl_as_gpl(self):
        # The whole point of the field is to stop a wrong license disposing a lead.
        m = self._refresh()
        for token, family in (("AGPL-3.0", "AGPL"), ("LGPL 2.1", "LGPL"), ("GPLv3", "GPL"),
                              ("Apache License 2.0", "Apache-2.0"), ("BSD-3-Clause",
                              "BSD-3-Clause"), ("CC-BY-SA 4.0", "CC-BY-SA"),
                              ("CC BY-NC-SA", "CC-BY-NC-SA"), ("MIT", "MIT"),
                              ("ISC", "ISC"), ("Unlicense", "Unlicense")):
            self.assertEqual(m.normalize_spdx(token), family, token)

    def test_version_is_never_invented(self):
        # "GPL" in prose that never said 3.0 must not become GPL-3.0: this field exists
        # to stop a fabricated license fact, so it may not introduce one.
        m = self._refresh()
        self.assertEqual(m.normalize_spdx("GPL"), "GPL")

    def test_declared_license_records_a_readme_manifest_conflict(self):
        # builderio/agent-native: MIT in the README, ISC in package.json. The standing
        # "the LICENSE file governs" tiebreak (#26) has nothing to govern with here.
        m = self._refresh()
        m.manifest_license = lambda slug: ("ISC", 'package.json: "ISC"', "package.json")
        rec = m.declared_license("o/r", readme="## License\n\nMIT\n")
        self.assertEqual((rec["spdx"], rec["conflict"]), ("MIT", "ISC"))
        self.assertIn("ISC", rec["phrase"])

    def test_declared_license_is_none_when_nothing_declares_one(self):
        m = self._refresh()
        m.manifest_license = lambda slug: None
        self.assertIsNone(m.declared_license("o/r", readme="# Tool\n\nNo terms here.\n"))

    # --- triage: the band this unblocks ----------------------------------------
    def test_effective_license_prefers_a_declaration_over_a_bare_none(self):
        self.assertEqual(triage.effective_license(
            {"license_spdx": "NONE", "license_declared": {"spdx": "MIT"}}), "MIT")
        self.assertEqual(triage.effective_license({"license_spdx": "NONE"}), "NONE")
        self.assertEqual(triage.effective_license({"license_spdx": "MIT"}), "MIT")
        self.assertEqual(triage.effective_license({}), "")

    def test_a_declared_copyleft_still_disqualifies(self):
        # It resolves in BOTH directions — the field records what the repo says, and a
        # README declaring AGPL disqualifies a vendored artifact on exactly the reasoning
        # a parsed AGPL does. Anything else would make the field an escape hatch.
        lic = triage.effective_license(
            {"license_spdx": "NONE", "license_declared": {"spdx": "AGPL"}})
        self.assertTrue(triage.DISQUALIFYING_LICENSE.match(lic))

    def test_vendored_lead_with_a_declared_mit_leaves_the_mechanical_band(self):
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "evaluations"), exist_ok=True)
            _write(d, "CATALOG.md", "## Plan\n\n" + self.HDR +
                   "| [skl](https://github.com/o/skl) | skill | one | two | none |\n")
            _write(d, "COMPARISON.md",
                   "# Tool Comparison\n\n## Plan\n\n"
                   "| Tool | Type | Auto | Free | Evaluated | Evidence |\n"
                   "|------|------|------|------|-----------|----------|\n"
                   "| skl | skill | | ✓ | discovery-log | SOURCE-ONLY |\n")
            _write(d, "STACK.md", "# STACK\n")
            ctx = audit.DetectorContext(d)
            facts = triage.catalog_facts(ctx.catalog)
            bare = {"o/skl": {"license_spdx": "NONE", "archived": False}}
            self.assertEqual(triage.band_of("skl", facts, bare, {}), "P4 mechanical-skip")
            declared = {"o/skl": dict(bare["o/skl"],
                                      license_declared={"spdx": "MIT", "where": "readme"})}
            self.assertIsNone(triage.band_of("skl", facts, declared, {}))
            copyleft = {"o/skl": dict(bare["o/skl"],
                                      license_declared={"spdx": "AGPL", "where": "readme"})}
            self.assertEqual(triage.band_of("skl", facts, copyleft, {}),
                             "P4 mechanical-skip")

    # --- detector Z ------------------------------------------------------------
    def _ctx(self, d, records, verdict="SKIP", verdict_text=None):
        os.makedirs(os.path.join(d, "evaluations"), exist_ok=True)
        _write(d, "CATALOG.md", "## Plan\n\n" + self.HDR +
               "| [skl](https://github.com/o/skl) | skill | one | two | none |\n")
        _write(d, "COMPARISON.md",
               "# Tool Comparison\n\n## Plan\n\n"
               "| Tool | Type | Auto | Free | Evaluated | Evidence |\n"
               "|------|------|------|------|-----------|----------|\n"
               f"| skl | skill | | ✓ | {verdict} | REVIEW |\n")
        if verdict_text:
            _write(d, "evaluations/skl.md",
                   f"# Evaluation: skl\n\n## Verdict\n\n{verdict_text}\n")
        _write(d, "repo-metadata.json", json.dumps(records))
        return audit.DetectorContext(d)

    DECLARED: ClassVar[dict] = {"o/skl": {"license_spdx": "NONE", "archived": False,
                          "license_declared": {"spdx": "MIT", "where": "readme",
                                               "phrase": "## License MIT"}}}

    def test_a_skip_grounded_on_the_license_is_the_strongest_kind(self):
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, self.DECLARED, verdict_text=(
                "**SKIP** — no declared license. A skill/plugin is *vendored* — its text "
                "is copied into the consuming repo — and text carrying no license grant "
                "cannot be copied in."))
            finds, records, withdrawn = audit.audit_license_declared(ctx)
            self.assertEqual((records, withdrawn), (1, []))
            self.assertEqual([(f.kind, f.spdx) for f in finds], [("GROUNDED", "MIT")])
            self.assertIn("## License MIT", finds[0].phrase)

    def test_a_skip_on_other_grounds_is_only_recorded(self):
        # The record is still wrong and the next bulk pass reads it — but no human's
        # disposition rests on it, which is a different order of problem.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, self.DECLARED, verdict_text=(
                "**SKIP** — dormant for 13 months and redundant with the incumbent."))
            finds, _, _ = audit.audit_license_declared(ctx)
            self.assertEqual([f.kind for f in finds], ["RECORDED"])

    def test_a_passing_mention_of_a_license_is_not_a_ground(self):
        # Deliberately narrow: if every verdict that says the word "license" counted,
        # every clean row would be a finding and the count would stop meaning anything.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, self.DECLARED, verdict_text=(
                "**SKIP** — capable, permissively licensed, and wholly redundant."))
            finds, _, _ = audit.audit_license_declared(ctx)
            self.assertEqual([f.kind for f in finds], ["RECORDED"])

    def test_conflict_is_reported_apart(self):
        with tempfile.TemporaryDirectory() as d:
            recs = {"o/skl": {"license_spdx": "NONE", "license_declared": {
                "spdx": "MIT", "where": "readme", "phrase": "x", "conflict": "ISC"}}}
            ctx = self._ctx(d, recs, verdict="discovery-log")
            finds, _, _ = audit.audit_license_declared(ctx)
            self.assertEqual([(f.kind, f.conflict) for f in finds], [("CONFLICT", "ISC")])

    def test_grounded_outranks_conflict(self):
        # A false disposition outranks a bookkeeping disagreement — and the conflict is
        # still carried on the finding rather than lost to the sort.
        with tempfile.TemporaryDirectory() as d:
            recs = {"o/skl": {"license_spdx": "NONE", "license_declared": {
                "spdx": "MIT", "where": "readme", "phrase": "x", "conflict": "ISC"}}}
            ctx = self._ctx(d, recs, verdict_text="**SKIP** (license) — no LICENSE file.")
            finds, _, _ = audit.audit_license_declared(ctx)
            self.assertEqual([(f.kind, f.conflict) for f in finds], [("GROUNDED", "ISC")])

    def test_uncollected_field_reports_zero_records_not_zero_findings(self):
        # V's rule: absence of the field means "not collected", never "every NONE is a
        # real absence". The count is what distinguishes them.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, {"o/skl": {"license_spdx": "NONE", "archived": False}})
            self.assertEqual(audit.audit_license_declared(ctx), ([], 0, []))

    def test_missing_cache_is_not_an_exception(self):
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "evaluations"), exist_ok=True)
            _write(d, "CATALOG.md", ""); _write(d, "COMPARISON.md", "")
            self.assertEqual(
                audit.audit_license_declared(audit.DetectorContext(d)), ([], 0, []))

    def test_flag_is_report_only_and_opt_in(self):
        self.assertIn("--license-declared", audit.REPORT_FLAGS)
        self.assertNotIn("--license-declared", audit.DEFAULT_GATES)
        self.assertNotIn("--license-declared", audit.OFFLINE_GATES)

    # --- the withdrawal bucket -------------------------------------------------
    # A verdict that has already withdrawn its license ground still QUOTES the claim it
    # withdrew, because quoting it is the honest way to record a correction. Without a
    # bucket, an eval is punished for documenting its own repair and the count can never
    # reach zero. Same shape as W's "argues it clears the bar" and V's ack.

    def test_a_withdrawn_ground_is_printed_but_not_counted(self):
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, self.DECLARED, verdict_text=(
                "**SKIP — off-scope.** ~~A second ground: no license.~~ Withdrawn: the "
                "README declares MIT. The scope ground below decides the row on its own."))
            finds, records, withdrawn = audit.audit_license_declared(ctx)
            self.assertEqual(finds, [])
            self.assertEqual(records, 1)                    # still collected
            self.assertEqual([f.kind for f in withdrawn], ["GROUNDED"])

    def test_withdrawal_recognizes_the_explicit_sentence_form(self):
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, self.DECLARED, verdict_text=(
                "**SKIP** — dormant. The license ground stated here is withdrawn; the "
                "repo has no LICENSE file but its README declares MIT."))
            finds, _, withdrawn = audit.audit_license_declared(ctx)
            self.assertEqual((finds, len(withdrawn)), ([], 1))

    def test_a_live_ground_is_not_withdrawn_by_the_word_license_alone(self):
        # The hatch must not open on any verdict that merely discusses licensing, or it
        # becomes a mute button for the findings it exists to let a human clear.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, self.DECLARED, verdict_text=(
                "**SKIP** — no declared license. The license question is central here "
                "and the licensing terms matter for a vendored skill."))
            finds, _, withdrawn = audit.audit_license_declared(ctx)
            self.assertEqual([f.kind for f in finds], ["GROUNDED"])
            self.assertEqual(withdrawn, [])

    def test_withdrawal_applies_only_to_a_grounded_finding(self):
        # RECORDED and CONFLICT are facts about the METADATA, not about a verdict, so a
        # retraction in someone's prose must not suppress them.
        with tempfile.TemporaryDirectory() as d:
            recs = {"o/skl": {"license_spdx": "NONE", "license_declared": {
                "spdx": "MIT", "where": "readme", "phrase": "x", "conflict": "ISC"}}}
            ctx = self._ctx(d, recs, verdict="discovery-log",
                            verdict_text="~~no license~~ withdrawn — README declares MIT.")
            finds, _, withdrawn = audit.audit_license_declared(ctx)
            self.assertEqual([f.kind for f in finds], ["CONFLICT"])
            self.assertEqual(withdrawn, [])


class TestStarConvention(unittest.TestCase):
    """Pins check-stars.py, the presence gate for **Stars:** (#377).

    The convention (#256/#261) is that every eval DECLARES a value and that what it
    declares depends on what the file is about. So the gate has exactly two jobs, and
    these tests pin both directions of each: a missing line fails, and every legitimate
    declaration — a count, a per-contender list, a reasoned `n/a` — passes.

    The second direction is the load-bearing one. #256's data fix regressed because
    nothing enforced the field; a gate that over-enforced would regress the other way,
    by pressuring authors of repo-less evals to invent a star count. Never assert that
    the value is numeric here."""

    def _write(self, d, name, header):
        path = os.path.join(d, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# Evaluation: {name[:-3]}\n\n"
                    "**Repo:** [o/r](https://github.com/o/r)\n"
                    f"{header}"
                    "**Last verified:** 2026-08-05\n\n## What it does\n\nx\n")
        return path

    # ---- the value parser: what counts as the declaration
    def test_value_stops_at_the_pipe_and_ignores_the_provenance_comment(self):
        # TEMPLATE's header packs Stars/Last-updated/License onto one line, and the
        # figure carries a repo-metadata.json stamp. Neither is part of the value.
        t = "**Stars:** 48,535  <!-- repo-metadata.json, fetched 2026-08-04 --> | **License:** MIT\n"
        self.assertEqual(checkstars.star_value(t), "48,535")

    def test_no_line_at_all_reads_as_undeclared(self):
        self.assertIsNone(checkstars.star_value("# Evaluation: x\n\n**Repo:** none\n"))

    # ---- direction 1: a missing line is a finding
    def test_missing_field_is_flagged(self):
        with tempfile.TemporaryDirectory() as d:
            self._write(d, "forgot.md", "")
            missing, bare = checkstars.audit([os.path.join(d, "forgot.md")])
            self.assertEqual(missing, ["forgot.md"])
            self.assertEqual(bare, [])

    # ---- direction 2: every legitimate shape passes, incl. the non-numeric ones
    def test_each_legitimate_declaration_passes(self):
        with tempfile.TemporaryDirectory() as d:
            shapes = {
                "one-tool.md": "**Stars:** 48,535 | **License:** Apache-2.0\n",
                "contenders.md": "**Stars:** codegraph 64,594 · serena 27,562\n",
                "reasoned-na.md": "**Stars:** n/a — methodology, no repo\n",
                "parenthetical-na.md": "**Stars:** N/A (academic paper) | **License:** arXiv\n",
                "mixed-na.md": "**Stars:** claude-mem 89,595 · OMEGA n/a — no public repo\n",
            }
            for name, header in shapes.items():
                self._write(d, name, header)
            missing, bare = checkstars.audit(
                [os.path.join(d, n) for n in shapes])
            self.assertEqual(missing, [], "a legitimate declaration was flagged as missing")
            self.assertEqual(bare, [], "a reasoned n/a was mistaken for a bare one")

    # ---- the printed-not-counted bucket
    def test_bare_na_is_reported_but_never_a_failure(self):
        # `n/a` with no reason is half a declaration. It is worth seeing and is not a
        # build breaker — the same printed-not-counted shape as detector V's `acked`.
        with tempfile.TemporaryDirectory() as d:
            for name, header in (("bare.md", "**Stars:** n/a | **License:** proprietary\n"),
                                 ("dangling.md", "**Stars:** n/a —\n")):
                self._write(d, name, header)
            missing, bare = checkstars.audit(
                [os.path.join(d, "bare.md"), os.path.join(d, "dangling.md")])
            self.assertEqual(missing, [])
            self.assertEqual(bare, ["bare.md", "dangling.md"])

    # ---- exit codes: the Makefile picks gate vs report-only, the script supports both
    def test_exit_codes_differ_by_mode(self):
        with tempfile.TemporaryDirectory() as d:
            self._write(d, "forgot.md", "")
            self._write(d, "ok.md", "**Stars:** 12\n")
            saved = checkstars.EVAL_GLOB
            checkstars.EVAL_GLOB = os.path.join(d, "*.md")
            try:
                self.assertEqual(checkstars.main(["--check"]), 1, "gate mode must fail")
                self.assertEqual(checkstars.main([]), 0, "report mode must never fail")
            finally:
                checkstars.EVAL_GLOB = saved

    def test_clean_tree_passes_in_gate_mode(self):
        with tempfile.TemporaryDirectory() as d:
            self._write(d, "ok.md", "**Stars:** n/a — protocol doc, no repo\n")
            saved = checkstars.EVAL_GLOB
            checkstars.EVAL_GLOB = os.path.join(d, "*.md")
            try:
                self.assertEqual(checkstars.main(["--check"]), 0)
            finally:
                checkstars.EVAL_GLOB = saved


class TestInstallEvidenceColumn(unittest.TestCase):
    """Pins verify-installs.py, the `Install evidence` column in STACK-LEDGER.md (ADR-0006,
    #382).

    The column exists because `KEEP` used to assert installation and nothing checked it.
    So the two things worth pinning are (a) that the classifier asks the row's own SLUG
    before its NAME — identity-by-name is the bug the column was built to end, and the
    first draft committed it inside the fix — and (b) that `--check` gates SHAPE and only
    shape, because CI has no lockfile and a build must never fail because a laptop
    changed.

    Fixtures only. Nothing here reads the real ledger or the real machine."""

    LEDGER = (
        "# Stack Exclusion Ledger\n\nprose\n\n## ADOPT / KEEP tools\n\n"
        "| Tool | Verdict | Stage | In STACK? | Exclusion reason (required when `no`) |\n"
        "|------|---------|-------|-----------|----------------------------------------|\n"
        "| codegraph | ADOPT | Plan | yes | |\n"
        "| documentation-writer | ADOPT | Reflect | no | Overlaps the pick |\n"
        "\n## Batch exclusions\n\n"
        "| Batch | Date | Tools | STACK decision | Rationale | Flagged |\n"
        "|-------|------|-------|----------------|-----------|---------|\n"
        "| 2026-06-19 discovery (#37) | 2026-06-19 | 19 | all excluded | prose | x |\n")

    def _records(self, **kw):
        base = {"slugs": set(), "lock_by_key": {}, "plugin_names": set(),
                "fetched_keys": {}, "disk_keys": set()}
        base.update(kw)
        return verifyinstalls.Records(**base)

    # ---- the classifier: slug first, then the collision guard, then the name records
    def test_own_slug_settles_the_row_even_when_the_name_belongs_to_another_repo(self):
        # #366's `caveman`: the row's four skills ARE installed, while the bare name in
        # the lockfile belongs to mattpocock/skills. Asking the name first reported a
        # healthy ADOPT as unbacked.
        rec = self._records(slugs={"juliusbrussee/caveman"},
                            lock_by_key={"caveman": "mattpocock/skills"})
        self.assertEqual(
            verifyinstalls.classify("juliusbrussee/caveman", "caveman", "2026-08-05", rec),
            "lockfile 2026-08-05")

    def test_a_name_owned_by_another_repo_is_a_collision_not_an_install(self):
        # `code-review` is ADOPT-as-claude-plugins-official; the code-review on this
        # machine is mattpocock/skills' own. Every name-keyed record below therefore
        # belongs to that other tool — recording it here is the bug itself.
        rec = self._records(lock_by_key={"codereview": "mattpocock/skills"},
                            disk_keys={"codereview"}, plugin_names={"codereview"})
        self.assertEqual(
            verifyinstalls.classify("anthropics/claude-plugins-official", "codereview",
                                    "2026-08-05", rec),
            "collision 2026-08-05")

    def test_a_fetched_cache_version_is_its_own_answer_not_no_record(self):
        # #332's discriminator: a real version means the code was pulled, `unknown` means
        # only the marketplace was added. A fetch is still not an activation, so this is
        # neither `none` nor `lockfile`.
        rec = self._records(fetched_keys={"claudereflect": "3.1.0"})
        self.assertEqual(
            verifyinstalls.classify("nixlim/claude-reflect", "claudereflect", "2026-08-05", rec),
            "cache 3.1.0 2026-08-05")

    def test_multiple_fetched_versions_stay_one_whitespace_free_token(self):
        # read_install_records joins with ", ", which would break the value regex — and a
        # lexicographic max would read 13.11.0 as older than 13.4.0, so picking one is
        # not the fix. Both are kept, slash-joined.
        rec = self._records(fetched_keys={"claudemem": "13.11.0, 13.4.0"})
        value = verifyinstalls.classify("t/claude-mem", "claudemem", "2026-08-05", rec)
        self.assertEqual(value, "cache 13.11.0/13.4.0 2026-08-05")
        self.assertRegex(value, verifyinstalls.VALUE)

    def test_plugins_json_outranks_a_bare_directory(self):
        rec = self._records(plugin_names={"x"}, disk_keys={"x"})
        self.assertTrue(
            verifyinstalls.classify("o/x", "x", "2026-08-05", rec).startswith("plugins-json"))

    def test_nothing_answering_reads_as_none(self):
        self.assertEqual(verifyinstalls.classify("o/x", "x", "2026-08-05", self._records()),
                         "none 2026-08-05")

    # ---- 0 records is 'no data', never 'nothing is installed'
    def test_a_machine_with_no_records_yields_nothing_rather_than_a_clean_sweep(self):
        with tempfile.TemporaryDirectory() as home:
            self.assertIsNone(verifyinstalls.read_records(home))
            self.assertEqual(verifyinstalls.machine_evidence("2026-08-05", home), ({}, {}))

    # ---- resolution: exact name first, ambiguous key resolves to nothing
    def test_lookup_prefers_the_exact_name_over_a_colliding_key(self):
        # `agent-skills` (a skill) and `agentskills` (the SKILL.md spec) share a name_key.
        # A single map would hand one row the other's install fact.
        ev = ({"agent-skills": "lockfile 2026-08-05", "agentskills": "n/a"}, {})
        self.assertEqual(verifyinstalls._lookup(ev, "agent-skills"), "lockfile 2026-08-05")
        self.assertEqual(verifyinstalls._lookup(ev, "agentskills"), "n/a")

    def test_an_ambiguous_key_resolves_to_nothing_rather_than_a_coin_flip(self):
        # Detector U's rule. `by_key` is built without keys two rows claim, so a ledger
        # name that only matches by key gets no answer at all.
        self.assertIsNone(verifyinstalls._lookup(({}, {}), "agentskills"))

    # ---- the rewriter
    def test_record_widens_the_header_and_fills_every_row(self):
        out = verifyinstalls.rewrite(
            self.LEDGER, ({"codegraph": "n/a",
                           "documentation-writer": "lockfile 2026-08-05"}, {}))
        self.assertIn("| Exclusion reason (required when `no`) | Install evidence |", out)
        self.assertIn("| codegraph | ADOPT | Plan | yes | | n/a |", out)
        self.assertIn("| documentation-writer | ADOPT | Reflect | no | Overlaps the pick "
                      "| lockfile 2026-08-05 |", out)
        self.assertEqual(verifyinstalls.audit(out), [])

    def test_the_batch_exclusion_table_is_left_alone(self):
        # A different table with a different shape: it records group decisions, not
        # per-tool install facts.
        out = verifyinstalls.rewrite(self.LEDGER, ({"codegraph": "n/a"}, {}))
        self.assertIn("| 2026-06-19 discovery (#37) | 2026-06-19 | 19 | all excluded "
                      "| prose | x |", out)

    def test_rewriting_is_idempotent(self):
        ev = ({"codegraph": "n/a", "documentation-writer": "none 2026-08-05"}, {})
        once = verifyinstalls.rewrite(self.LEDGER, ev)
        self.assertEqual(verifyinstalls.rewrite(once, ev), once)

    def test_a_row_the_machine_cannot_see_keeps_its_dated_record(self):
        # A refresh that cannot see a tool must not erase an earlier run's record of it.
        once = verifyinstalls.rewrite(
            self.LEDGER, ({"documentation-writer": "lockfile 2026-07-01"}, {}))
        again = verifyinstalls.rewrite(once, ({"codegraph": "n/a"}, {}))
        self.assertIn("| lockfile 2026-07-01 |", again)

    # ---- --check gates shape, and only shape
    def test_check_flags_a_missing_column_and_a_missing_value(self):
        problems = dict(verifyinstalls.audit(self.LEDGER))
        self.assertIn("(table header)", problems)
        self.assertIn("codegraph", problems)
        self.assertIn("documentation-writer", problems)

    def test_check_rejects_a_value_outside_the_vocabulary(self):
        bad = verifyinstalls.rewrite(self.LEDGER, ({"codegraph": "n/a",
                                                    "documentation-writer": "n/a"}, {}))
        bad = bad.replace("| codegraph | ADOPT | Plan | yes | | n/a |",
                          "| codegraph | ADOPT | Plan | yes | | yes |")
        self.assertEqual([n for n, _ in verifyinstalls.audit(bad)], ["codegraph"])

    def test_check_never_asserts_a_value_is_still_true(self):
        # The whole CI contract: a stale-but-well-formed value passes. A build must not
        # fail because a laptop changed, and CI has no lockfile to consult anyway.
        old = verifyinstalls.rewrite(self.LEDGER, ({"codegraph": "lockfile 1999-01-01",
                                                    "documentation-writer": "none 1999-01-01"}, {}))
        self.assertEqual(verifyinstalls.audit(old), [])

    # ---- detector J must keep matching the widened row
    def test_detector_j_still_parses_a_six_column_ledger(self):
        # _LEDGER_ROW is anchored to end-of-line; before #382 widened it, a sixth column
        # dropped every row on the floor.
        widened = verifyinstalls.rewrite(self.LEDGER, ({"codegraph": "n/a",
                                                        "documentation-writer": "none 2026-08-05"}, {}))
        for text, why in ((self.LEDGER, "five-column"), (widened, "six-column")):
            names = [m[0] for m in audit._LEDGER_ROW.findall(text)]
            self.assertEqual(names, ["codegraph", "documentation-writer"], why)
