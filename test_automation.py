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
import contextlib
import datetime
import gc
import importlib.util
import inspect
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import types
import unittest
import urllib.error
import warnings
from pathlib import Path
from typing import ClassVar
from unittest import mock

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
checklinks = _load("check_links", "check-links.py")
rewritelinks = _load("rewrite_doc_links", "rewrite-doc-links.py")
checkplugin = _load("check_plugin", "check-plugin.py")
freshness = _load("freshness", "freshness.py")


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
        # plugin/README.md says "evaluation and comparison files", not "evaluations".
        # It was in FILES_TOTAL all along, so it *looked* maintained while drifting 87
        # behind the real count (#302). The specific phrase must win over the loose ones.
        # Both wordings are pinned: #435 struck "evidence-based" from that line, and the
        # count must not quietly stop tracking because an adjective moved.
        self.assertEqual(
            reconcile.fix_eval_strings(
                "- `evaluations/` — 469 evidence-based evaluation and comparison files", 556),
            "- `evaluations/` — 556 evidence-based evaluation and comparison files")
        self.assertEqual(
            reconcile.fix_eval_strings(
                "- `evaluations/` — 469 evaluation and comparison files", 556),
            "- `evaluations/` — 556 evaluation and comparison files")

    def test_fix_eval_strings_leaves_composition_alone_without_it(self):
        # The composition is opt-in: a caller with no counts must not have the three
        # numbers zeroed or invented. Passing None leaves the prose untouched.
        s = "682 evaluation files: 293 carrying a verdict, 258 still at `discovery-log`."
        self.assertEqual(reconcile.fix_eval_strings(s, 682), s)

    def test_fix_eval_strings_rewrites_each_composition_number(self):
        # Each number is anchored on its own trailing phrase, so the three can never be
        # swapped by a regex matching the wrong one (#435).
        s = ("999 evaluation files: 1 carrying a verdict "
             "(ADOPT/KEEP/CONDITIONAL/SKIP/DEFER), 2 still at `discovery-log` — leads, "
             "not verdicts — and 3 stubs and comparison documents")
        out = reconcile.fix_eval_strings(s, 682, (293, 258, 131))
        self.assertIn("682 evaluation files", out)
        self.assertIn("293 carrying a verdict", out)
        self.assertIn("258 still at `discovery-log`", out)
        self.assertIn("131 stubs and comparison documents", out)


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
        _write(d, "plugin/README.md", "An inventory of 3 tools.\n")
        # reconcile derives the eval composition through audit-evals' verdict parser
        # rather than a second regex (#435), so the fixture repo carries that sibling too.
        shutil.copy(os.path.join(ROOT, "audit-evals.py"), os.path.join(d, "audit-evals.py"))

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
        # The regression for #302: plugin/README.md is in FILES_TOTAL but its wording
        # matched no EVAL_PATTERN, so the eval count on line 18 sat frozen while the
        # catalog count on line 17 was rewritten by the same run. End-to-end so the
        # file-list membership and the pattern are pinned together, not just the regex.
        with tempfile.TemporaryDirectory() as d:
            self._fixture_repo(d)
            _write(d, "plugin/README.md",
                   "An inventory of 3 tools.\n"
                   "- `evaluations/` — 999 evidence-based evaluation and comparison files\n")
            for i in range(4):                                   # K = 4 real evals
                _write(d, f"evaluations/e{i}.md", "# eval\n")
            _write(d, "evaluations/TEMPLATE.md", "# template\n")  # excluded from the count
            self.assertEqual(self._run(d, "--check").returncode, 1)
            self.assertEqual(self._run(d).returncode, 0)
            plugin = Path(d, "plugin", "README.md").read_text(encoding="utf-8")
            self.assertIn("4 evidence-based evaluation and comparison files", plugin)
            self.assertEqual(self._run(d, "--check").returncode, 0)

    def test_eval_composition_partitions_the_total(self):
        # README used to call every file in evaluations/ an "evidence-based evaluation
        # with a verdict" (#435). The three buckets are derived from each file's own
        # headline verdict and must add up to eval_count(), so a reader can check the
        # arithmetic rather than trust the adjective.
        with tempfile.TemporaryDirectory() as d:
            _write(d, "evaluations/a.md", "# a\n\n## Verdict\n\n**ADOPT** — good.\n")
            _write(d, "evaluations/b.md", "# b\n\n## Verdict\n\n**SKIP** — no license.\n")
            _write(d, "evaluations/c.md",
                   "# c\n\n## Verdict\n\n**discovery-log — tentative read** — a lead.\n")
            _write(d, "evaluations/d.md", "# d\n\nA stub with no Verdict section.\n")
            _write(d, "evaluations/TEMPLATE.md", "# template\n\n## Verdict\n\n**ADOPT**\n")
            comp = reconcile.eval_composition(d)
            self.assertEqual(comp, (2, 1, 1))
            self.assertEqual(sum(comp), reconcile.eval_count(d))  # partitions the total

    def test_a_lead_is_never_counted_as_a_verdict(self):
        # #324 relabelled 324 leads precisely so they stop announcing a verdict they are
        # not entitled to; counting them as verdicts re-announces it in aggregate.
        with tempfile.TemporaryDirectory() as d:
            _write(d, "evaluations/lead.md",
                   "# lead\n\n## Verdict\n\n**discovery-log — tentative read** — notes only.\n")
            self.assertEqual(reconcile.eval_composition(d), (0, 1, 0))

    def test_composition_is_written_and_gated_end_to_end(self):
        # The number and its label move together: a drifted composition fails --check
        # exactly like a drifted total, which is what #435 asked for.
        with tempfile.TemporaryDirectory() as d:
            self._fixture_repo(d, readme=(
                "An inventory of 3 tools.\n\nThere are 3 catalog entries.\n\n"
                "- 999 evaluation files: 9 carrying a verdict, 9 still at `discovery-log` "
                "and 9 stubs and comparison documents\n"))
            _write(d, "evaluations/a.md", "# a\n\n## Verdict\n\n**ADOPT** — good.\n")
            _write(d, "evaluations/b.md",
                   "# b\n\n## Verdict\n\n**discovery-log — tentative read** — a lead.\n")
            _write(d, "evaluations/c.md", "# c\n\nno verdict here.\n")
            self.assertEqual(self._run(d, "--check").returncode, 1)
            self.assertEqual(self._run(d).returncode, 0)
            readme = Path(d, "README.md").read_text(encoding="utf-8")
            self.assertIn("3 evaluation files", readme)
            self.assertIn("1 carrying a verdict", readme)
            self.assertIn("1 still at `discovery-log`", readme)
            self.assertIn("1 stubs and comparison documents", readme)
            self.assertEqual(self._run(d, "--check").returncode, 0)


# ----------------------------------------------------------------- plugin/hooks/validate-counts.sh
@unittest.skipUnless(shutil.which("bash") and shutil.which("git"),
                     "validate-counts.sh needs bash and git")
@unittest.skipUnless(shutil.which("git"), "the hook resolves its root with git rev-parse")
class TestValidateCountsHook(unittest.TestCase):
    """The PostToolUse count hook. It used to re-implement the count extraction in bash,
    grepping the prose phrasing each number sits in, so a prose rewrite silently deleted
    a check: 3 of 5 had rotted to no-ops, two within three days (#443). It delegates to
    `reconcile-counts.py --check` / `sync-plugin-docs.sh --check` now — the one-
    implementation rule CLAUDE.md already states for every other hook here.

    Both directions are pinned, and the second is the point. The only test this class
    used to have asserted the hook is SILENT on a clean tree — which is the *symptom*:
    a hook with zero live checks is maximally silent, so that test passed more easily
    the more broken the hook got."""

    HOOK: ClassVar[str] = os.path.join(ROOT, "plugin", "hooks", "validate-counts.sh")

    def _run(self, cwd):
        return subprocess.run(["bash", self.HOOK], cwd=cwd, capture_output=True,
                              text=True, check=False)

    def _fixture_repo(self, d, readme):
        """A temp git repo carrying reconcile-counts.py and what it reads. `git init` is
        required, not incidental: the hook finds its root with `git rev-parse
        --show-toplevel`, which is why a bare directory was never enough to test it."""
        subprocess.run(["git", "init", "-q"], cwd=d, check=True)
        for f in ("reconcile-counts.py", "catalog_lib.py", "audit-evals.py"):
            shutil.copy(os.path.join(ROOT, f), os.path.join(d, f))
        _write(d, "CATALOG.md", CATALOG_OK)
        _write(d, "COMPARISON.md", COMPARISON_OK)
        _write(d, "CLAUDE.md", "An inventory of 3 tools.\n")
        _write(d, "STACK.md", "distilled from 3 catalog entries\n")
        _write(d, "plugin/README.md", "An inventory of 3 tools.\n")
        _write(d, "README.md", readme)

    def test_hook_is_silent_on_a_clean_tree(self):
        r = self._run(ROOT)
        self.assertEqual(r.stdout, "", msg="hook reported drift on a reconciled tree")
        self.assertEqual(r.returncode, 0, msg=r.stderr)

    def test_hook_reports_drift(self):
        # The direction the old test could not check. Without this, every check in the
        # hook could be dead and the suite would stay green.
        with tempfile.TemporaryDirectory() as d:
            self._fixture_repo(d, readme="An inventory of 99 tools.\n\nThere are 99 catalog entries.\n")
            r = self._run(d)
            self.assertIn("drift detected", r.stdout, msg=r.stdout + r.stderr)

    def test_hook_is_silent_when_that_same_tree_is_reconciled(self):
        # Same fixture, correct numbers: the report above is drift, not noise.
        with tempfile.TemporaryDirectory() as d:
            self._fixture_repo(d, readme="An inventory of 3 tools.\n\nThere are 3 catalog entries.\n")
            self.assertEqual(self._run(d).stdout, "")

    def test_hook_is_a_silent_noop_in_a_foreign_repo(self):
        # The installed plugin fires this on every Edit/Write in someone else's project.
        with tempfile.TemporaryDirectory() as d:
            subprocess.run(["git", "init", "-q"], cwd=d, check=True)
            _write(d, "unrelated.py", "print(1)\n")
            r = self._run(d)
            self.assertEqual(r.stdout, "")
            self.assertEqual(r.returncode, 0, msg=r.stderr)

    def test_hook_does_not_re_extract_counts_from_prose(self):
        # The regression that made 3 checks dead: a `grep` for the phrasing a number sits
        # in is a second extractor for a fact reconcile-counts.py already owns, and it
        # fails SILENTLY when the prose moves. Delegation is the fix; this keeps it.
        with open(self.HOOK, encoding="utf-8") as f:
            body = "\n".join(l for l in f if not l.lstrip().startswith("#"))
        self.assertIn("reconcile-counts.py --check", body)
        for dead in ("inventory of", "evidence", "num_after", "num_before"):
            self.assertNotIn(dead, body, msg=f"hook re-extracts counts from prose: {dead!r}")


# ----------------------------------------------------------------- comments are not claims (#451)
class TestCommentsAreNotClaims(unittest.TestCase):
    """A header field is a CLAIM and is read from comment-stripped text; a marker about
    that field is PROVENANCE and is read from the raw text. Detector AC settled the rule
    for `**License:**` in #417 and nothing generalised it, so detector Q — which GATES —
    read `**Last triaged:**` out of TEMPLATE.md's own guidance comment, and every eval
    created the documented way (copy the template, fill it in) failed `make check`.

    The template test uses the REAL TEMPLATE.md, because the bug was that the template's
    text and the parser disagreed; a fixture template would pin the fixture."""

    def _ctx(self, d, **files):
        for name, text in files.items():
            _write(d, os.path.join("evaluations", name + ".md"), text)
        return audit.DetectorContext(d)

    def test_a_filled_in_template_copy_passes_the_gating_detector(self):
        # The headline regression. The remedy Q named was worse than the finding: one
        # marker exempts an eval from the verdict ceiling it never earned, the other
        # forbids an honest hands-on ADOPT.
        with open(os.path.join(ROOT, "evaluations", "TEMPLATE.md"), encoding="utf-8") as f:
            filled = re.sub(r"## Verdict\n", "## Verdict\n\n**ADOPT** — ran it hands-on.\n",
                            f.read(), count=1)
        with tempfile.TemporaryDirectory() as d:
            findings = audit.audit_bulk_triage(self._ctx(d, my_new_eval=filled))
        self.assertEqual(findings, [], msg=f"a copy of TEMPLATE.md fails detector Q: {findings}")

    def test_a_commented_stamp_is_not_a_stamp(self):
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, x="# E\n\n<!-- OPTIONAL: **Last triaged:** 2026-01-01 -->\n")
            self.assertEqual(audit.audit_bulk_triage(ctx), [])

    def test_a_real_stamp_still_needs_attribution(self):
        # The detector is not weakened: an unattributed stamp on a real line still fires.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, x="# E\n\n**Last triaged:** 2026-01-01\n")
            self.assertEqual(audit.audit_bulk_triage(ctx), [("x", audit.UNATTRIBUTED)])

    def test_the_markers_are_still_read_from_the_raw_text(self):
        # Load-bearing, and the reason this cannot be one flag on the whole detector:
        # `<!-- triaged: bulk -->` IS a comment. Stripping both sides would silently
        # retire the eliminate-only shield.
        real = "# E\n\n**Last triaged:** 2026-01-01  <!-- triaged: bulk -->\n\n## Verdict\n\n**ADOPT** — x\n"
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(audit.audit_bulk_triage(self._ctx(d, x=real)), [("x", "ADOPT")])

    def test_a_human_marker_still_exempts(self):
        human = "# E\n\n**Last triaged:** 2026-01-01  <!-- triaged: human -->\n\n## Verdict\n\n**ADOPT** — x\n"
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(audit.audit_bulk_triage(self._ctx(d, x=human)), [])

    def test_a_commented_date_never_becomes_the_staleness_anchor(self):
        # The dangerous direction is the opposite of a stale-looking demo: a comment
        # carrying a RECENT date would make a genuinely stale eval report fresh, and
        # detector L, --staleness and WATCHLIST.md all rest on this value.
        ev = audit.Evaluation("x", "# E\n\n<!-- e.g. **Last verified:** 2020-01-01 -->\n"
                                   "**Last verified:** 2026-08-01\n")
        self.assertEqual(ev.last_verified, datetime.date(2026, 8, 1))
        only = audit.Evaluation("y", "# E\n\n<!-- e.g. **Last verified:** 2020-01-01 -->\n")
        self.assertIsNone(only.last_verified, msg="a commented example date became the eval's date")

    def test_the_backfill_marker_still_survives_beside_a_real_value(self):
        # backfill-lastverified.py writes the comment AFTER the value on the same line.
        ev = audit.Evaluation("x", "**Last verified:** 2026-06-01  "
                                   "<!-- backfilled from last git edit; not a hands-on re-check -->\n")
        self.assertEqual(ev.last_verified, datetime.date(2026, 6, 1))
        self.assertIn(backfill_lv.COMMENT, ev.text)

    def test_a_commented_field_never_satisfies_a_presence_gate(self):
        commented = "# E\n\n<!--\n**Stars:** 1,234\n**Last verified:** 2026-08-01\n-->\n"
        self.assertIsNone(checkstars.star_value(commented))
        self.assertFalse(backfill_lv.declares_last_verified(commented))
        real = "# E\n\n**Stars:** 1,234\n**Last verified:** 2026-08-01\n"
        self.assertEqual(checkstars.star_value(real), "1,234")
        self.assertTrue(backfill_lv.declares_last_verified(real))

    def test_one_stripper_not_four(self):
        # #443's rule: one fact, one implementation. Three copies of this regex existed.
        for mod in ("audit-evals.py", "check-stars.py", "backfill-lastverified.py"):
            with open(os.path.join(ROOT, mod), encoding="utf-8") as f:
                body = f.read()
            self.assertNotIn('re.compile(r"<!--.*?-->"', body,
                             msg=f"{mod} re-implements the comment stripper")


# ----------------------------------------------------------------- stage drift, detector AG (#453)
class TestStageDrift(unittest.TestCase):
    """A tool's dev loop stage is written in the eval header AND in the COMPARISON section
    it sits under, and nothing compared them. The detector is deliberately generous — the
    corpus is full of legitimately multi-stage tools — so most of these pin what must NOT
    be reported."""

    HEAD = "| Tool | Type | Auto | Free | Evaluated | Evidence |\n|---|---|---|---|---|---|\n"

    def _ctx(self, d, sections, evals, stack=""):
        comp = ["# Tool Comparison", ""]
        for sec, rows in sections.items():
            comp += [f"## {sec}", "", self.HEAD.rstrip()]
            comp += [f"| {t} | tool | | ✓ | {v} | REVIEW |" for t, v in rows]
            comp.append("")
        _write(d, "COMPARISON.md", "\n".join(comp) + "\n")
        _write(d, "CATALOG.md", "# Catalog\n")
        _write(d, "STACK.md", stack or "# Stack\n")
        for name, stage in evals.items():
            body = f"# Evaluation: {name}\n\n**Dev loop stage:** {stage}\n\n" if stage else f"# Evaluation: {name}\n\n"
            body += f"## Catalog entry\n\n| Name | Type | One-liner | Problem | Overlaps |\n|---|---|---|---|---|\n| {name} | tool | x | y | z |\n"
            _write(d, os.path.join("evaluations", name + ".md"), body)
        return audit.DetectorContext(d)

    def _drift(self, **kw):
        with tempfile.TemporaryDirectory() as d:
            return audit.audit_stage_drift(self._ctx(d, **kw))

    def test_a_section_the_header_never_names_is_a_finding(self):
        drift, _stack, comparable, _un = self._drift(
            sections={"Ship": [("worktrunk", "discovery-log")]},
            evals={"worktrunk": "Implement"})
        self.assertEqual([(f.tool, f.section, f.named) for f in drift],
                         [("worktrunk", "Ship", ["Implement"])])
        self.assertEqual(comparable, 1)

    def test_the_header_is_quoted_so_a_human_reads_the_sentence(self):
        # V's rule: the detector cannot resolve which side is stale, so it never says.
        drift, _s, _c, _u = self._drift(
            sections={"Review": [("code-on-incus", "discovery-log")]},
            evals={"code-on-incus": "Cross-cutting / Safety (isolation substrate; touches Implement)"})
        self.assertIn("touches Implement", drift[0].header)

    def test_any_named_stage_matching_the_section_is_agreement(self):
        # The generosity rule, and the reason resolving-merge-conflicts is not a finding:
        # a multi-stage tool must still be filed under ONE of its stages.
        drift, _s, comparable, _u = self._drift(
            sections={"Implement": [("rmc", "ADOPT")]},
            evals={"rmc": "Ship (merge/integration; touches Implement when conflicts arise)"})
        self.assertEqual(drift, [])
        self.assertEqual(comparable, 1)

    def test_a_header_naming_no_loop_stage_is_never_a_finding(self):
        # check-stars.py's rule: an honest non-answer is not graded into a finding.
        drift, _s, comparable, unusable = self._drift(
            sections={"Implement": [("vercel-ai", "discovery-log")]},
            evals={"vercel-ai": "Mostly off-loop (an SDK for building LLM apps)"})
        self.assertEqual((drift, comparable, unusable), ([], 0, 1))

    def test_category_sections_are_not_stage_claims(self):
        # 316 rows sit under a category; comparing them would flag every healthy one.
        drift, _s, comparable, unusable = self._drift(
            sections={"MCP Servers": [("git-mcp", "discovery-log")]},
            evals={"git-mcp": "Implement"})
        self.assertEqual((drift, comparable, unusable), ([], 0, 0))

    def test_stage_names_are_word_anchored(self):
        # `Planning`/`Implementation` are prose, not a declaration of that stage.
        self.assertEqual(audit.named_stages("Planning and implementation notes"), [])
        self.assertEqual(audit.named_stages("Verify / Ship (preview environments)"),
                         ["Verify", "Ship"])

    def test_stack_is_a_third_copy_and_is_compared_stage_to_stage_only(self):
        stack = ("# Stack\n\n## Ship\n\n| Tool | What | Install | Signal |\n|---|---|---|---|\n"
                 "| [rmc](https://github.com/a/b) | x | y | z |\n"
                 "| [gh-mcp](https://github.com/c/d) | x | y | z |\n")
        _drift, stack_drift, _c, _u = self._drift(
            sections={"Implement": [("rmc", "ADOPT")], "MCP Servers": [("gh-mcp", "ADOPT")]},
            evals={"rmc": "Ship (touches Implement)", "gh-mcp": "Plan"},
            stack=stack)
        # rmc: Ship vs Implement, both stages -> finding. gh-mcp: Ship vs a CATEGORY
        # section -> a different axis, and legitimate.
        self.assertEqual([f.tool for f in stack_drift], ["rmc"])

    def test_a_row_claimed_by_two_evals_resolves_to_neither(self):
        # AD's open question; answering it here would put a stranger's header on the row.
        with tempfile.TemporaryDirectory() as d:
            self._ctx(d, sections={"Ship": [("dup", "discovery-log")]},
                      evals={"dup": "Implement"})
            _write(d, os.path.join("evaluations", "dup-two.md"),
                   "# Evaluation: dup\n\n**Dev loop stage:** Plan\n\n## Catalog entry\n\n"
                   "| Name | Type | One-liner | Problem | Overlaps |\n|---|---|---|---|---|\n"
                   "| dup | tool | x | y | z |\n")
            drift, _s, comparable, _u = audit.audit_stage_drift(audit.DetectorContext(d))
        self.assertEqual((drift, comparable), ([], 0))

    def test_the_stage_header_is_read_from_comment_stripped_text(self):
        # #451: a commented example line is provenance, never a declaration.
        ev = audit.Evaluation("x", "# E\n\n<!-- e.g. **Dev loop stage:** Plan -->\n"
                                   "**Dev loop stage:** Ship\n")
        self.assertEqual(ev.dev_loop_stage, "Ship")
        only = audit.Evaluation("y", "# E\n\n<!-- e.g. **Dev loop stage:** Plan -->\n")
        self.assertIsNone(only.dev_loop_stage)


class TestLayerDrift(unittest.TestCase):
    """`**Layer:**` was the one eval header field nothing read, and all three copies of the
    fact drifted (#475). AI is AG's twin on the other axis of the same 2-D map, so most of
    these pin what must NOT be reported."""

    CHEAD = ("| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |\n"
             "|---|---|---|---|---|---|\n")

    VHEAD = "| Tool | Type | Auto | Free | Evaluated | Evidence |\n|---|---|---|---|---|---|\n"

    def _ctx(self, d, workflow, evals, rows=()):
        cat = ["# Catalog", "", "## Skills & Plugins", "", self.CHEAD.rstrip()]
        cat += [f"| [{n}]({u}) | tool | x | y | z |  |" for n, u in rows]
        _write(d, "CATALOG.md", "\n".join(cat) + "\n")
        # eval_by_row is keyed off COMPARISON rows (detector AD's claim map), so a
        # fixture with no rows resolves nothing at all.
        comp = ["# Tool Comparison", "", "## Implement", "", self.VHEAD.rstrip()]
        comp += [f"| {n} | tool | | ✓ | discovery-log | REVIEW |" for n, _u in rows]
        _write(d, "COMPARISON.md", "\n".join(comp) + "\n")
        _write(d, "STACK.md", "# Stack\n")
        _write(d, "WORKFLOW.md", workflow)
        for name, layer in evals.items():
            body = f"# Evaluation: {name}\n\n"
            if layer:
                body += f"**Layer:** {layer}\n"
            body += (f"\n## Catalog entry\n\n| Name | Type | One-liner | Problem | Overlaps |\n"
                     f"|---|---|---|---|---|\n| {name} | tool | x | y | z |\n")
            _write(d, os.path.join("evaluations", name + ".md"), body)
        return audit.DetectorContext(d)

    def _run(self, **kw):
        with tempfile.TemporaryDirectory() as d:
            return audit.audit_layer_drift(self._ctx(d, **kw))

    @staticmethod
    def _table(*rows):
        out = ["## Plan", "", "| Layer | What | Signals |", "|---|---|---|"]
        out += [f"| {ly} | {what} | Speed |" for ly, what in rows]
        return "\n".join(out) + "\n"

    def test_a_table_layer_the_eval_header_never_names_is_a_finding(self):
        wf = self._table(("**Infrastructure**",
                          "[github-mcp-server](https://github.com/github/github-mcp-server) — x"))
        drift, _sd, _u, _nl, cover = self._run(
            workflow=wf, evals={"github-mcp-server": "Tooling"},
            rows=[("github-mcp-server", "https://github.com/github/github-mcp-server")])
        self.assertEqual([(f.tool, f.declared, f.named) for f in drift],
                         [("github-mcp-server", "Infrastructure", ["Tooling"])])
        self.assertEqual(cover.rows, 1)

    def test_any_named_layer_matching_is_agreement(self):
        # AG's generosity rule: `Process / Tooling` filed under either is healthy, and
        # flagging a healthy row costs more than missing a sick one (detector V).
        wf = self._table(("**Tooling**", "[t](https://github.com/o/t) — x"))
        drift, _sd, _u, _nl, cover = self._run(
            workflow=wf, evals={"t": "Process / Tooling (a skill that ships a CLI)"},
            rows=[("t", "https://github.com/o/t")])
        self.assertEqual((drift, cover.rows), ([], 1))

    def test_the_header_is_quoted_so_a_human_reads_it(self):
        wf = self._table(("**Process**", "[t](https://github.com/o/t) — x"))
        drift, _sd, _u, _nl, _c = self._run(
            workflow=wf, evals={"t": "Infrastructure (a running MCP server, not a habit)"},
            rows=[("t", "https://github.com/o/t")])
        self.assertIn("not a habit", drift[0].header)

    def test_the_layer_cell_carries_forward_across_continuation_rows(self):
        # Only the first row of a layer group fills the cell; the rest are blank, which is
        # why this is a line walk. Reading a blank cell as "no layer" would lose 2 of 3.
        wf = self._table(("**Tooling**", "[a](https://github.com/o/a) — x"),
                         ("", "[b](https://github.com/o/b) — x"),
                         ("", "[c](https://github.com/o/c) — x"))
        drift, _sd, _u, _nl, cover = self._run(
            workflow=wf, evals={"a": "Tooling", "b": "Process", "c": "Process"},
            rows=[("a", "https://github.com/o/a"), ("b", "https://github.com/o/b"),
                  ("c", "https://github.com/o/c")])
        self.assertEqual(cover.rows, 3)
        self.assertEqual(sorted(f.tool for f in drift), ["b", "c"])

    def test_a_new_table_does_not_inherit_the_previous_tables_layer(self):
        # The tables are separated by PROSE, not a heading — the case the header-row reset
        # exists for. With only a heading between them the reset is unreachable, so a
        # fixture that used one would pin nothing.
        wf = (self._table(("**Infrastructure**", "[a](https://github.com/o/a) — x"))
              + "\nSome prose between two tables.\n\n| Layer | What | Signals |\n|---|---|---|\n"
              + "| | [b](https://github.com/o/b) — x | Speed |\n")
        _d, _sd, _u, _nl, cover = self._run(
            workflow=wf, evals={"a": "Infrastructure", "b": "Process"},
            rows=[("a", "https://github.com/o/a"), ("b", "https://github.com/o/b")])
        # `b` sits under no layer cell at all, so it is not comparable — never compared
        # against the previous table's Infrastructure.
        self.assertEqual(cover.rows, 1)

    def test_the_adoption_ladder_is_compared_against_the_stage_tables(self):
        # SELF-DRIFT needs no join and cannot be a resolution artifact.
        wf = (self._table(("**Tooling**", "[caveman](https://github.com/o/caveman) — x"))
              + "\n## Adopting This Workflow\n\n### Start here: Process\n\n"
                "- **caveman** — reduce token waste from day one\n")
        _d, self_drift, _u, _nl, cover = self._run(
            workflow=wf, evals={"caveman": "Tooling"},
            rows=[("caveman", "https://github.com/o/caveman")])
        self.assertEqual([(f.tool, f.declared, f.named) for f in self_drift],
                         [("caveman", "Process", ["Tooling"])])
        self.assertEqual(cover.filed_twice, 1)

    def test_a_ladder_bullet_naming_two_tools_is_split(self):
        # `headroom + context-mode` and `code-review plugin + pr-review-toolkit` each name
        # two; taking the bullet whole would silently drop one of every pair.
        wf = (self._table(("**Tooling**", "[headroom](https://github.com/o/headroom) — x"),
                          ("", "[context-mode](https://github.com/o/cm) — x"))
              + "\n## Adopting This Workflow\n\n### Add when you want autonomy: Orchestration\n\n"
                "- **headroom + context-mode** — token compression\n")
        _d, self_drift, _u, _nl, cover = self._run(
            workflow=wf, evals={"headroom": "Tooling", "context-mode": "Tooling"},
            rows=[("headroom", "https://github.com/o/headroom"),
                  ("context-mode", "https://github.com/o/cm")])
        self.assertEqual(sorted(f.tool for f in self_drift), ["context-mode", "headroom"])
        self.assertEqual(cover.filed_twice, 2)

    def test_the_ladders_fourth_layer_name_is_reported_verbatim(self):
        # `Orchestration` exists in no template, no eval header and no stage table.
        # Normalising it into the closed set would erase the finding.
        wf = (self._table(("**Tooling**", "[gsd](https://github.com/o/gsd) — x"))
              + "\n## Adopting This Workflow\n\n### Add when you want autonomy: Orchestration\n\n"
                "- **gsd** — structured project orchestration\n")
        _d, self_drift, _u, _nl, _c = self._run(
            workflow=wf, evals={"gsd": "Tooling"},
            rows=[("gsd", "https://github.com/o/gsd")])
        self.assertEqual(self_drift[0].declared, "Orchestration")

    def test_a_ladder_entry_in_no_stage_table_is_not_compared(self):
        wf = ("## Adopting This Workflow\n\n### Start here: Process\n\n"
              "- **beads** — issue tracking\n")
        _d, self_drift, _u, _nl, cover = self._run(workflow=wf, evals={})
        self.assertEqual((self_drift, cover.filed_twice), ([], 0))

    def test_a_layer_outside_the_closed_set_is_undeclared(self):
        _d, _sd, undecl, _nl, cover = self._run(
            workflow="# W\n", evals={"ralph": "Harness", "ok": "Tooling"})
        self.assertEqual([(f.tool, f.header) for f in undecl], [("ralph", "Harness")])
        self.assertEqual(cover.declaring, 2)

    def test_a_missing_layer_line_is_printed_and_never_counted(self):
        # check-stars.py's rule: an honest non-answer is not graded into a finding.
        _d, _sd, undecl, no_layer, cover = self._run(
            workflow="# W\n", evals={"memory-systems": None})
        self.assertEqual(undecl, [])
        self.assertEqual([f.tool for f in no_layer], ["memory-systems"])
        self.assertEqual(cover.declaring, 0)

    def test_named_layers_is_word_anchored(self):
        self.assertEqual(audit.named_layers("Processing pipeline"), [])
        self.assertEqual(audit.named_layers("Infrastructure (MCP server)"),
                         ["Infrastructure"])
        self.assertEqual(audit.named_layers("Process / Tooling"), ["Process", "Tooling"])

    def test_the_layer_header_is_read_from_comment_stripped_text(self):
        # #451: a commented example is provenance, never a declaration.
        ev = audit.Evaluation("x", "# E\n\n<!-- **Layer:** Process -->\n"
                                   "**Layer:** Tooling\n")
        self.assertEqual(ev.layer, "Tooling")
        self.assertIsNone(audit.Evaluation("y", "# E\n\n<!-- **Layer:** Process -->\n").layer)

    def test_live_tree_reports_every_bucket_with_a_population(self):
        # #467's rule: a bare finding count reads identically whether anything was checked.
        drift, self_drift, undecl, no_layer, cover = audit.audit_layer_drift(
            audit.DetectorContext(ROOT))
        self.assertTrue(cover.rows and cover.filed_twice and cover.declaring)
        self.assertLessEqual(len(drift), cover.rows)
        self.assertLessEqual(len(self_drift), cover.filed_twice)
        self.assertLessEqual(len(undecl), cover.declaring)
        self.assertTrue(no_layer, "the printed-not-counted bucket lost its members")


class TestDetectorPopulations(unittest.TestCase):
    """#467's rule — a check reports what it examined, because `0 findings` and
    `0 examined` print identically — and #481 carried it to the seven gates while
    recording the report-only side as already done. It was not: eight detectors printed a
    finding count with no denominator, and `CLAUDE.md` said the work was finished, which
    is why nobody looked (#494).

    The pin is what makes it stay done. A claim of completeness with nothing checking it
    is the shape `plugin/README.md`'s rotted facts and `validate-counts.sh`'s three no-op
    checks both had — *gate the shared facts, not the file*."""

    # Every offline report-only flag. The network ones (`--links`, `--archived`) and the
    # local-only `--installed` are out: a unit test must not depend on the network or on
    # one laptop's lockfile (detector Y's own reason for never entering `make check`).
    OFFLINE_REPORT_FLAGS = (
        "--skills", "--skill-design", "--overlaps", "--workflow-drift", "--clusters",
        "--savings-claims", "--evidence", "--staleness", "--metadata-staleness",
        "--lead-headlines", "--catalog-mirror", "--maintenance", "--scope", "--identity",
        "--license-declared", "--containment", "--conditional-gate", "--license-header",
        "--duplicate-evals", "--workflow-skips", "--containment-evidence", "--stage-drift",
        "--repo-installs", "--layer-drift", "--link-identity", "--claim-drift",
        "--claude-verbs")

    # A denominator in any of the shapes the corpus uses: `6/8`, `0 of 693`, `across 619
    # record(s)`, `in 318 of 583`, `644 record(s)`.
    POPULATION = re.compile(r"\d+\s*/\s*\d+|\bof\s+\d+|\bacross\s+\d+|\bin\s+\d+"
                            r"|\d+\s+record\(s\)")

    def _headlines(self):
        r = subprocess.run(["python3", "audit-evals.py", *self.OFFLINE_REPORT_FLAGS],
                           cwd=ROOT, capture_output=True, text=True, check=False)
        return [ln for ln in r.stdout.splitlines() if ln.startswith("== ")]

    def test_every_offline_report_flag_prints_exactly_one_headline(self):
        """Guards the test below from passing vacuously: if a flag stopped emitting a
        headline, a per-headline assertion would simply have one fewer line to check."""
        heads = self._headlines()
        self.assertEqual(len(heads), len(self.OFFLINE_REPORT_FLAGS),
                         "one headline per flag:\n" + "\n".join(heads))

    def test_every_report_only_headline_states_the_population_it_walked(self):
        offenders = [h for h in self._headlines() if not self.POPULATION.search(h)]
        self.assertEqual(offenders, [],
                         "a report-only headline with no denominator — `0 findings` and "
                         "`0 examined` print identically (#319/#467/#481)")

    def test_the_flag_list_is_the_whole_offline_report_set(self):
        """Derived, not hand-listed: a detector added to `REPORT_FLAGS` must arrive here
        too, or the sweep above silently stops covering it — the same rot `check-plugin.py`
        pins for the front-door skills list."""
        known_excluded = {"--links", "--archived", "--installed"}
        self.assertEqual(set(audit.REPORT_FLAGS) - known_excluded,
                         set(self.OFFLINE_REPORT_FLAGS),
                         "REPORT_FLAGS changed — add the new flag here (or to the "
                         "network/local exclusion set, with a reason)")


class TestClaimDrift(unittest.TestCase):
    """AG did the stage axis, AI the layer axis; AK does the NUMBER axis — a fact written
    in several places with nothing comparing them. `caveman` is MEASURED, its eval retracts
    "~60-75%" by name, and that retracted figure still ships on the front door, the install
    list and the manual (#490)."""

    CHEAD = ("| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |\n"
             "|---|---|---|---|---|---|\n")

    def _ctx(self, d, rows, pages=None, evals=None):
        cat = ["# Catalog", "", "## Skills & Plugins", "", self.CHEAD.rstrip()]
        for n, u, one in rows:
            cat.append(f"| [{n}]({u}) | tool | {one} | y | z |  |")
        _write(d, "CATALOG.md", "\n".join(cat) + "\n")
        comp = ["## Plan", "| Tool | Type | Auto | Free | Evaluated | Evidence |",
                "|---|---|---|---|---|---|"]
        for n, _, _ in rows:
            comp.append(f"| {n} | tool | - | - | ADOPT | MEASURED |")
        _write(d, "COMPARISON.md", "\n".join(comp) + "\n")
        for f in ("STACK.md", "WORKFLOW.md", "PLAYBOOK.md", "README.md"):
            _write(d, f, (pages or {}).get(f, "# x\n"))
        for name, body in (evals or {}).items():
            _write(d, os.path.join("evaluations", name + ".md"), body)
        return audit.DetectorContext(d)

    def _run(self, **kw):
        with tempfile.TemporaryDirectory() as d:
            return audit.audit_claim_drift(self._ctx(d, **kw))

    CAVE = ("caveman", "https://github.com/JuliusBrussee/caveman", "cuts tokens")

    @staticmethod
    def _eval(name, url, body):
        return (f"# {name}\n\n**Repo:** [{name}]({url})\n\n"
                f"**Evidence:** MEASURED\n\n## Verdict\n\n**ADOPT** — x\n\n{body}\n")

    RETRACT = '- **The headline "~60-75%" is optimistic for natural register.** We measured ~49%.\n'

    # ---- REFUTED -------------------------------------------------------------
    def test_a_page_restating_a_withdrawn_figure_is_refuted(self):
        _, ref, _, _ = self._run(
            rows=[self.CAVE],
            pages={"STACK.md": "| [caveman](https://github.com/JuliusBrussee/caveman) | ~60-75% cut |\n"},
            evals={"caveman": self._eval("caveman", "https://github.com/JuliusBrussee/caveman", self.RETRACT)})
        self.assertEqual([(f.rel, f.line, f.claim) for f in ref], [("STACK.md", 1, "60-75%")])

    def test_the_top_of_a_withdrawn_range_restated_as_a_point_estimate_is_refuted(self):
        """`WORKFLOW.md:81` says "cuts ~75% of agent output tokens" — the top of the
        retracted ~60-75% band, restated as if it were the measurement."""
        _, ref, _, _ = self._run(
            rows=[self.CAVE],
            pages={"WORKFLOW.md": "| [caveman](https://github.com/JuliusBrussee/caveman) | ~75% |\n"},
            evals={"caveman": self._eval("caveman", "https://github.com/JuliusBrussee/caveman", self.RETRACT)})
        self.assertEqual([f.claim for f in ref], ["75%"])

    def test_a_range_merely_overlapping_the_withdrawn_one_is_drift_and_nothing_stronger(self):
        """`~65-75%` shares an endpoint with the retracted `~60-75%` and is a different
        claim. Containment runs ONE way — the conservative side, detector V's rule."""
        dr, ref, _, _ = self._run(
            rows=[self.CAVE],
            pages={"WORKFLOW.md": "| [caveman](https://github.com/JuliusBrussee/caveman) | ~65-75% |\n",
                   "STACK.md": "| [caveman](https://github.com/JuliusBrussee/caveman) | ~49-59% |\n"},
            evals={"caveman": self._eval("caveman", "https://github.com/JuliusBrussee/caveman", self.RETRACT)})
        self.assertEqual(ref, [], "an overlapping range is not the withdrawn figure")
        self.assertEqual(len(dr), 1, "but the two pages still disagree")

    def test_a_number_present_in_the_eval_but_not_withdrawn_is_not_refuted(self):
        """The rule that made REFUTED possible at all: `75` appears in caveman's eval ONLY
        inside the retraction, so a set-membership test over the eval TEXT reports the
        wrong lines as healthy. Keying on the retraction SENTENCE is what separates them."""
        _, ref, _, _ = self._run(
            rows=[self.CAVE],
            pages={"STACK.md": "| [caveman](https://github.com/JuliusBrussee/caveman) | ~49% |\n"},
            evals={"caveman": self._eval("caveman", "https://github.com/JuliusBrussee/caveman",
                                         self.RETRACT)})
        self.assertEqual(ref, [], "~49% is the MEASURED figure, not the withdrawn one")

    def test_one_line_is_one_finding_however_many_sentences_withdraw_it(self):
        """`caveman` retracts one figure in TWO sentences; counting the line twice made 3
        defects read as 6. The count is what a human works down."""
        _, ref, _, _ = self._run(
            rows=[self.CAVE],
            pages={"STACK.md": "| [caveman](https://github.com/JuliusBrussee/caveman) | ~60-75% |\n"},
            evals={"caveman": self._eval(
                "caveman", "https://github.com/JuliusBrussee/caveman",
                self.RETRACT + '\nThe earlier "~60-75%" was optimistic; budget ~50%.\n')})
        self.assertEqual(len(ref), 1)

    def test_a_retraction_quote_never_spans_a_heading(self):
        """`[^.]*?` crosses a markdown heading happily. The quote is the evidence a human
        judges, so it must be the sentence the author actually wrote."""
        _, ref, _, _ = self._run(
            rows=[self.CAVE],
            pages={"STACK.md": "| [caveman](https://github.com/JuliusBrussee/caveman) | ~60-75% |\n"},
            evals={"caveman": self._eval("caveman", "https://github.com/JuliusBrussee/caveman",
                                         "## What didn't work\n\n" + self.RETRACT)})
        self.assertEqual(len(ref), 1)
        self.assertNotIn("What didn't work", ref[0].detail)

    # ---- DRIFT ---------------------------------------------------------------
    def test_pages_disagreeing_about_one_tool_are_drift(self):
        dr, _, tools, lines = self._run(
            rows=[self.CAVE],
            pages={"STACK.md": "| [caveman](https://github.com/JuliusBrussee/caveman) | ~60-75% |\n",
                   "WORKFLOW.md": "| [caveman](https://github.com/JuliusBrussee/caveman) | ~49-59% |\n"})
        self.assertEqual([f.tool for f in dr], ["juliusbrussee/caveman"])
        self.assertEqual(dr[0].claim, ["49-59%", "60-75%"])
        self.assertEqual((tools, lines), (1, 2))

    def test_pages_agreeing_are_not_drift_but_are_still_walked(self):
        dr, _, tools, lines = self._run(
            rows=[self.CAVE],
            pages={"STACK.md": "| [caveman](https://github.com/JuliusBrussee/caveman) | ~49-59% |\n",
                   "WORKFLOW.md": "| [caveman](https://github.com/JuliusBrussee/caveman) | ~49-59% |\n"})
        self.assertEqual(dr, [])
        self.assertEqual((tools, lines), (1, 2), "agreement must be WALKED, not skipped")

    # ---- attribution ---------------------------------------------------------
    def test_a_line_naming_several_tools_attributes_its_number_to_none_of_them(self):
        """A row citing other tools in `Overlaps with` is not a claim about them. A first
        probe that ignored this reported 4 findings of which 3 were its own arithmetic."""
        dr, _, tools, lines = self._run(
            rows=[self.CAVE, ("headroom", "https://github.com/headroomlabs-ai/headroom", "x")],
            pages={"STACK.md": ("| [caveman](https://github.com/JuliusBrussee/caveman) | 95% | "
                                "[headroom](https://github.com/headroomlabs-ai/headroom) |\n")})
        self.assertEqual((dr, tools, lines), ([], 0, 0))

    def test_an_eval_link_and_a_repo_link_are_one_tool(self):
        """PLAYBOOK links only EVALS, by design ("every claim below is a link"), so a
        slug-only detector reads the front door as claim-free — which is how this survived."""
        dr, _, tools, lines = self._run(
            rows=[self.CAVE],
            pages={"PLAYBOOK.md": "- **[caveman](evaluations/caveman.md)** — ~60-75% fewer tokens\n",
                   "STACK.md": "| [caveman](https://github.com/JuliusBrussee/caveman) | ~49-59% |\n"},
            evals={"caveman": self._eval("caveman", "https://github.com/JuliusBrussee/caveman", "x")})
        self.assertEqual(lines, 2)
        self.assertEqual(tools, 1, "an eval link and a repo link must collapse to ONE tool")
        self.assertEqual(len(dr), 1)

    def test_a_number_with_no_link_on_its_line_is_not_attributed(self):
        """Disclosed rather than silent: STACK's Quick Start comment restates the retracted
        figure with no link, and guessing its subject from prose is the identity-by-name
        error this file rejects everywhere else."""
        dr, ref, tools, lines = self._run(
            rows=[self.CAVE],
            pages={"STACK.md": "# 2. Output token compression (~60-75% savings)\n"},
            evals={"caveman": self._eval("caveman", "https://github.com/JuliusBrussee/caveman",
                                         self.RETRACT)})
        self.assertEqual((dr, ref, tools, lines), ([], [], 0, 0))

    def test_a_longer_number_donates_no_tail_digits_to_a_following_percentage(self):
        """Without `(?<!\\d)` the pattern reads `1250%` as `250%` — a claim nobody wrote,
        attributed to a real tool. A date is the same shape and yields nothing either."""
        self.assertEqual(audit._claim_tokens("1250% faster"), [])
        self.assertEqual(audit._claim_tokens("2026-06-18"), [])
        self.assertEqual(audit._claim_tokens("★9700 and 95% saved"), ["95%"])

    def test_a_slug_several_rows_sit_behind_resolves_to_no_single_eval(self):
        """#465's shared-slug shape: a pack root is linked by several rows, each with its
        own eval. Taking the first would put a SIBLING's retraction on this claim — the
        coin flip #463/#465 forbid. Resolving to nothing costs a missed finding; resolving
        to a stranger flags a healthy line, and that is the expensive direction (V's rule)."""
        pack = "https://github.com/mattpocock/skills"
        rmc = ("resolving-merge-conflicts", pack, "a")
        cr = ("code-review", pack, "b")
        evals = {"resolving-merge-conflicts": self._eval("resolving-merge-conflicts", pack, "x"),
                 "code-review": self._eval("code-review", pack, self.RETRACT)}
        page = {"STACK.md": f"| [resolving-merge-conflicts]({pack}) | ~60-75% |\n"}
        # BOTH orders, because a first-row resolver picks whichever `CATALOG.md` lists
        # first: asserting one order lets the coin flip pass whenever it lands heads.
        for rows in ([rmc, cr], [cr, rmc]):
            _, ref, _, lines = self._run(rows=rows, pages=page, evals=evals)
            self.assertEqual(lines, 1, "the line is still WALKED")
            self.assertEqual(ref, [], "a sibling's retraction must not reach this claim")

    # ---- live tree -----------------------------------------------------------
    def test_live_tree_counts_never_exceed_their_populations(self):
        dr, ref, tools, lines = audit.audit_claim_drift(audit.DetectorContext(audit.ROOT))
        self.assertLessEqual(len(dr), tools)
        self.assertLessEqual(len(ref), lines)
        self.assertGreater(lines, 0, "0 lines walked reads exactly like 0 findings (#319)")
        self.assertGreater(tools, 0)

    def test_live_tree_ships_no_figure_its_own_eval_withdrew(self):
        """REFUTED is pinned at zero and DRIFT deliberately is not — detector U's own split
        between the buckets a mechanical fact settles and the ones a human calls per row.

        A withdrawn figure is settled by the eval that withdrew it: there is no reading on
        which a page should advertise a number its own measurement retracted, so a new one
        is a regression and belongs in a red build. DRIFT is weaker — two pages could
        legitimately state different figures for a tool measured on two axes (input vs
        output tokens), and pinning it would turn that into a build failure, which is
        detector V's expensive direction with the strongest possible lever behind it.
        """
        _, ref, _, lines = audit.audit_claim_drift(audit.DetectorContext(audit.ROOT))
        self.assertEqual([f"{f.rel}:{f.line} {f.claim} ({f.tool})" for f in ref], [],
                         "a reader-facing page restates a figure its own eval withdraws")
        self.assertGreater(lines, 0, "0 claim lines walked would pass this vacuously")


class TestLinkIdentity(unittest.TestCase):
    """Every identity fix landed here asked "given a slug, which row" (#343/#366/#374/
    #413/#457/#463/#465). AJ asks the other direction — given the NAME a link shows a
    reader, does the URL point at that tool — and `STACK.md` tells a reader to run
    `claude install-plugin obra/superpowers` to get GSD (#483)."""

    CHEAD = ("| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |\n"
             "|---|---|---|---|---|---|\n")

    def _ctx(self, d, rows, stack="", workflow="", evals=None):
        cat = ["# Catalog", "", "## Skills & Plugins", "", self.CHEAD.rstrip()]
        for n, u in rows:
            link = f"[{n}]({u})" if u else n
            cat.append(f"| {link} | tool | x | y | z |  |")
        _write(d, "CATALOG.md", "\n".join(cat) + "\n")
        _write(d, "STACK.md", stack or "# Stack\n")
        _write(d, "WORKFLOW.md", workflow or "# Workflow\n")
        for name, body in (evals or {}).items():
            _write(d, os.path.join("evaluations", name + ".md"), body)
        return audit.DetectorContext(d)

    def _run(self, **kw):
        with tempfile.TemporaryDirectory() as d:
            return audit.audit_link_identity(self._ctx(d, **kw))

    # The live shape: two catalogued tools, a link naming one and pointing at the other.
    GSD = ("GSD (Get Shit Done)", "https://github.com/open-gsd/gsd-core")
    SUP = ("superpowers", "https://github.com/obra/superpowers")

    def test_a_link_naming_one_tool_and_pointing_at_another_is_a_finding(self):
        find, walked = self._run(
            rows=[self.GSD, self.SUP],
            stack="| [GSD](https://github.com/obra/superpowers) | plan | `x` | Speed |\n")
        self.assertEqual([(f.rel, f.named, f.slug) for f in find],
                         [("STACK.md", "GSD (Get Shit Done)", "obra/superpowers")])
        self.assertEqual(find[0].rows, ["superpowers"])
        self.assertEqual(walked, 1)

    def test_a_link_naming_the_tool_it_points_at_is_not_a_finding(self):
        find, walked = self._run(
            rows=[self.GSD, self.SUP],
            stack="| [GSD](https://github.com/open-gsd/gsd-core) | plan | `x` | Speed |\n")
        self.assertEqual(find, [])
        self.assertEqual(walked, 1, "the healthy link must still be WALKED, not skipped")

    def test_a_pack_member_linked_at_the_pack_root_is_healthy(self):
        """#465's documented shape, and the whole precision story: 85 live links sit behind
        a shared slug and a FIRST-ROW resolver flags 49 of them. The healthy set is every
        row behind the slug, never the one row a single-answer resolver picks."""
        pack = "https://github.com/mattpocock/skills"
        find, walked = self._run(
            # `mattpocock/skills` deliberately FIRST, so a first-row resolver answers with
            # the container for the member link and the test fails.
            rows=[("mattpocock/skills", pack),
                  ("resolving-merge-conflicts", pack + "/tree/main/skills/git")],
            stack=f"| [resolving-merge-conflicts]({pack}) | ship | `x` | Speed |\n")
        self.assertEqual(find, [])
        self.assertEqual(walked, 1)

    def test_findings_do_not_depend_on_catalog_row_order(self):
        """The property #463 violated inside the detector that GATES. Same two rows, both
        orders, same answer."""
        stack = "| [GSD](https://github.com/obra/superpowers) | plan | `x` | Speed |\n"
        a, _ = self._run(rows=[self.GSD, self.SUP], stack=stack)
        b, _ = self._run(rows=[self.SUP, self.GSD], stack=stack)
        self.assertEqual([f.named for f in a], [f.named for f in b])
        self.assertEqual([f.rows for f in a], [f.rows for f in b])

    def test_text_that_names_no_catalogued_tool_is_not_walked(self):
        """Conservative by construction: prose text resolves to nothing, so the link is
        never compared. Flagging a healthy row costs more than missing a sick one."""
        find, walked = self._run(
            rows=[self.SUP],
            stack="| [the harness we use](https://github.com/obra/superpowers) | x |\n")
        self.assertEqual((find, walked), ([], 0))

    def test_a_url_no_catalog_row_is_behind_is_not_walked(self):
        find, walked = self._run(
            rows=[self.GSD],
            stack="| [GSD](https://github.com/some/stranger) | plan | `x` |\n")
        self.assertEqual((find, walked), ([], 0))

    def test_an_ambiguous_text_key_resolves_to_nothing_not_a_coin_flip(self):
        """Detector U's AMBIG rule. `agent-skills` and `agentskills` collapse to one
        `identity_key`; with two rows claiming it, a text matching neither by NAME resolves
        to nothing rather than to whichever row CATALOG.md happens to list first."""
        rows = [("agent-skills", "https://github.com/vercel-labs/agent-skills"),
                ("agentskills", "https://github.com/tech-leads-club/agentskills"),
                self.SUP]
        find, walked = self._run(
            rows=rows,
            stack="| [Agent Skills](https://github.com/obra/superpowers) | x |\n")
        self.assertEqual((find, walked), ([], 0))
        # ...and an EXACT name still wins over the ambiguous key, which is the reason the
        # fallback can be dropped at all (verify-installs.py's exact-name-first rule).
        find2, walked2 = self._run(
            rows=rows,
            stack="| [agentskills](https://github.com/obra/superpowers) | x |\n")
        self.assertEqual(walked2, 1)
        self.assertEqual([f.named for f in find2], ["agentskills"])

    def test_markdown_emphasis_in_the_text_is_stripped(self):
        """The corpus cites this tool as ``GSD`` as often as GSD — 4 of the 8 live
        findings are inside backticks. `identity_keys` drops backticks on its own, so the
        strip is load-bearing on the EXACT-NAME path only: this row is reachable by name
        and its key is ambiguous, so an unstripped text resolves to nothing."""
        rows = [("agentskills", "https://github.com/tech-leads-club/agentskills"),
                ("agent-skills", "https://github.com/vercel-labs/agent-skills"),
                self.SUP]
        find, walked = self._run(
            rows=rows,
            evals={"bmad-method": "# x\n\nredundant with "
                                  "[`agentskills`](https://github.com/obra/superpowers)\n"})
        self.assertEqual(walked, 1)
        self.assertEqual([(f.rel, f.text, f.named) for f in find],
                         [("evaluations/bmad-method.md", "`agentskills`", "agentskills")])

    def test_the_text_index_keys_on_identity_never_alias(self):
        """#374: `alias_keys` deliberately adds the URL basename so an entry installed
        under another name resolves — but between two rows that each NAME a tool a
        basename is not a synonym. An unrelated row at `foo/gsd` must not make the text
        `GSD` ambiguous and silently withhold the finding."""
        find, walked = self._run(
            rows=[self.GSD, self.SUP,
                  ("unrelated-row", "https://github.com/foo/gsd")],
            stack="| [GSD](https://github.com/obra/superpowers) | plan | `x` |\n")
        self.assertEqual(walked, 1)
        self.assertEqual([f.named for f in find], ["GSD (Get Shit Done)"])

    def test_findings_are_reported_in_walk_order_STACK_first(self):
        """An EXECUTED page outranks a cited one (detector V's ordering). This is the walk
        order rather than a `sort()`, so it is `files` that must keep STACK first."""
        bad = "[GSD](https://github.com/obra/superpowers)"
        find, _ = self._run(
            rows=[self.GSD, self.SUP],
            stack=f"| {bad} | plan | `x` |\n",
            workflow=f"| {bad} | tooling |\n",
            evals={"a-lead": f"# x\n\nredundant with {bad}\n"})
        self.assertEqual([f.rel for f in find],
                         ["STACK.md", "WORKFLOW.md", "evaluations/a-lead.md"])

    def test_CATALOG_is_out_of_scope(self):
        """A row's Name cell names its own row by construction, so it could never be a
        finding; eval-vs-catalog link disagreement is detector U's `LINK` bucket."""
        self.assertNotIn("CATALOG.md", audit.LINK_IDENTITY_FILES)
        find, walked = self._run(rows=[self.GSD, self.SUP])
        self.assertEqual((find, walked), ([], 0))

    def test_it_is_report_only_and_never_gates(self):
        self.assertIn("--link-identity", audit.REPORT_FLAGS)
        self.assertNotIn("--link-identity", audit.OFFLINE_GATES)
        self.assertNotIn("--link-identity", audit.DEFAULT_GATES)

    def test_live_tree_findings_never_exceed_the_population(self):
        """#467's rule: the headline's second number is what was WALKED, so a finding set
        larger than it would mean the detector is reporting outside its own population."""
        find, walked = audit.audit_link_identity(audit.DetectorContext(audit.ROOT))
        self.assertLessEqual(len(find), walked)
        self.assertGreater(walked, 0, "the live tree walks no links at all")
        for f in find:
            self.assertNotIn(f.named, f.rows, "a finding whose text row IS behind the slug")


class TestInstallExtractor(unittest.TestCase):
    """Detector A GATES, and its extractor had no tests at all — which is how it came to
    require the literal word `install` and leave 10 real commands invisible to a headline
    reading `86/86 target(s) checked` (#485). Pinned in BOTH directions: what it must now
    see, and what it must still refuse to mint a target from."""

    @staticmethod
    def _ex(cmd):
        return list(audit.extract_installs("`" + cmd + "`"))

    # --- what the literal-`install` requirement used to hide -------------------------
    def test_npm_i_and_npm_add_are_installs(self):
        for cmd in ("npm i -g promptfoo", "npm add -g promptfoo"):
            self.assertEqual(self._ex(cmd), [("npm", "promptfoo")], cmd)

    def test_every_package_on_the_line_is_checked_not_just_the_first(self):
        """`npm install a b c` installs three packages; the extractor checked `a`, so
        `strands-agents-tools` had never been verified once."""
        self.assertEqual(
            self._ex("npm i -D jest @stryker-mutator/core @stryker-mutator/jest-runner"),
            [("npm", "jest"), ("npm", "@stryker-mutator/core"),
             ("npm", "@stryker-mutator/jest-runner")])
        self.assertEqual(self._ex("pip install strands-agents strands-agents-tools"),
                         [("pypi", "strands-agents"), ("pypi", "strands-agents-tools")])

    # --- the precision rules: a false BROKEN fails the build for a HEALTHY eval -------
    def test_a_shell_operator_ends_the_package_list(self):
        """A naive whitespace split mints targets named `&&`, `npx` and `start`. All four
        corpus lines that continue past the packages must behave exactly as before."""
        self.assertEqual(self._ex("npm install -g flowise && npx flowise start"),
                         [("npm", "flowise")])
        self.assertEqual(self._ex("npm install -g squish-memory && squish install --all"),
                         [("npm", "squish-memory")])
        self.assertEqual(self._ex("npm install && npm run build"), [])
        self.assertEqual(self._ex("cargo install --git"), [])

    def test_extras_quotes_and_version_pins_are_stripped_not_lost(self):
        """The first prototype LOST these two: the package is `markitdown`, not
        `markitdown[all]`. A coverage regression in a gating detector is worse than the
        gap being fixed, so the lost-nothing direction is pinned too."""
        self.assertEqual(self._ex("pip install 'markitdown[all]'"), [("pypi", "markitdown")])
        self.assertEqual(self._ex("pipx install 'cocoindex-code[full]'"),
                         [("pypi", "cocoindex-code")])
        self.assertEqual(self._ex("npm install ccusage@latest"), [("npm", "ccusage")])

    def test_a_url_or_path_install_target_is_not_minted_as_a_registry_name(self):
        """npm genuinely accepts a git URL, a tarball or a local path where a registry
        name goes. None of those is a package to look up, and inside a GATE an
        unrecognized token becoming a target means a false BROKEN and a red build."""
        for cmd in ("npm i git+https://github.com/o/r.git",
                    "npm install file:./local-pkg",
                    "npm i https://example.com/pkg.tgz"):
            self.assertEqual(self._ex(cmd), [], cmd)

    def test_a_scoped_package_keeps_its_leading_at(self):
        """The version-pin strip must never eat an npm scope."""
        self.assertEqual(self._ex("npm i -g @qwen-code/qwen-code"),
                         [("npm", "@qwen-code/qwen-code")])

    def test_the_other_forms_are_untouched(self):
        self.assertEqual(self._ex("npx ccusage@latest daily --json"), [("npm", "ccusage")])
        self.assertEqual(self._ex("cargo install ripgrep"), [("crates", "ripgrep")])

    def test_the_marketplace_form_is_the_one_that_resolves(self):
        """`claude install-plugin` / `install-skill` are not subcommands — `claude --help`
        lists neither, and the extractor keyed on them resolved their ARGUMENT while never
        asking whether the VERB exists (#487). Keying on the fake verb also meant the REAL
        commands already in the corpus went unchecked; three targets joined the gate when
        the pattern was repointed."""
        for cmd in ("claude plugin marketplace add obra/superpowers",
                    "claude plugins marketplace add obra/superpowers",
                    "claude plugin marketplace add obra/superpowers && "
                    "claude plugin install superpowers@superpowers-dev"):
            self.assertEqual(self._ex(cmd), [("gh", "obra/superpowers")], cmd)
        self.assertEqual(self._ex("claude install-plugin obra/superpowers"), [])

    def test_a_command_framed_as_the_wrong_one_is_still_skipped(self):
        """The NEGATION window is what keeps correction notes from becoming findings."""
        self.assertEqual(
            list(audit.extract_installs("this does not exist: `npm i -g nope-nope`")), [])

    def test_no_reader_facing_page_tells_anyone_to_run_a_fake_subcommand(self):
        """`claude` accepts an unrecognized first argument AS A PROMPT (#439), so a
        fabricated subcommand does not error — it opens a session with the command as the
        user's message and sits there. `STACK.md` carried ten of them for ten months, the
        `setup-workflow` skill handed two to an agent, and detector A passed on all of
        them because it checked the repo and never the verb (#487).

        Scoped to the pages a reader or an agent EXECUTES. `CLAUDE.md`, `audit-evals.py`
        and this file all name the fake verbs on purpose — documenting a defect is not
        committing it, the same line detector B's HONEST vocabulary draws."""
        import glob as _g
        pages = ["STACK.md", "WORKFLOW.md", "CATALOG.md", "README.md", "PLAYBOOK.md",
                 *_g.glob("evaluations/*.md", root_dir=audit.ROOT),
                 *_g.glob("skills/**/*.md", root_dir=audit.ROOT, recursive=True),
                 *_g.glob("plugin/docs/**/*.md", root_dir=audit.ROOT, recursive=True),
                 *_g.glob("plugin/skills/**/*.md", root_dir=audit.ROOT, recursive=True)]
        offenders = []
        for rel in pages:
            path = os.path.join(audit.ROOT, rel)
            if not os.path.exists(path):
                continue
            with open(path, encoding="utf-8") as fh:
                for i, line in enumerate(fh, 1):
                    if "claude install-plugin" in line or "claude install-skill" in line:
                        offenders.append(f"{rel}:{i}")
        self.assertEqual(offenders, [], "a `claude` subcommand that does not exist")

    def test_the_live_tree_gains_coverage_and_loses_none(self):
        """The invariant the fix is FOR: every target the old extractor found is still
        found, and the ten alias lines are now among them."""
        ctx = audit.DetectorContext(audit.ROOT)
        import glob
        files = ["STACK.md", "CATALOG.md",
                 *sorted(glob.glob("evaluations/*.md", root_dir=ctx.root))]
        found = set()
        for rel in files:
            if os.path.exists(ctx.path(rel)):
                found |= set(audit.extract_installs(ctx.read(rel)))
        for gained in [("npm", "@qwen-code/qwen-code"), ("npm", "claurst"),
                       ("npm", "inngest"), ("pypi", "strands-agents-tools")]:
            self.assertIn(gained, found, "an alias-form install went unchecked again")
        for kept in [("pypi", "markitdown"), ("pypi", "cocoindex-code"),
                     ("gh", "obra/superpowers")]:
            self.assertIn(kept, found, "the widened extractor LOST a target")


class TestClaudeVerbs(unittest.TestCase):
    """#487 fixed the ten fabricated `claude install-plugin`/`install-skill` commands it
    found and deliberately declined to build a general gate (#488). AL is that gate: every
    backticked `claude <word>` command whose word is neither a declared subcommand, a flag,
    nor a quoted prompt."""

    def _ctx(self, d, stack="", eval_body=None, discovery_body=None):
        _write(d, "STACK.md", stack or "# Stack\n")
        _write(d, "WORKFLOW.md", "# Workflow\n")
        _write(d, "CATALOG.md", "# Catalog\n")
        _write(d, "README.md", "# README\n")
        _write(d, "PLAYBOOK.md", "# Playbook\n")
        if eval_body is not None:
            _write(d, os.path.join("evaluations", "x.md"), eval_body)
        if discovery_body is not None:
            _write(d, os.path.join("discovery", "loop1.md"), discovery_body)
        return audit.DetectorContext(d)

    def _run(self, **kw):
        with tempfile.TemporaryDirectory() as d:
            return audit.audit_claude_verbs(self._ctx(d, **kw))

    def test_a_declared_subcommand_is_not_a_finding(self):
        find, walked = self._run(stack="Run `claude plugin marketplace add obra/superpowers`.\n")
        self.assertEqual((find, walked), ([], 1))

    def test_a_sub_verb_of_a_real_subcommand_is_not_flagged(self):
        """`claude auth login` reads as the real verb `auth` — `login` is never checked on
        its own here, unlike a bare `claude login`."""
        find, walked = self._run(stack="Run `claude auth login` first.\n")
        self.assertEqual((find, walked), ([], 1))

    def test_a_flag_is_not_a_verb(self):
        """Filtered before it becomes a candidate, the same way extract_installs drops a
        PLACEHOLDER before counting a target — a flag is never a `claude <word>` command."""
        find, walked = self._run(stack="Run `claude -p --output-format stream-json`.\n")
        self.assertEqual((find, walked), ([], 0))

    def test_a_quoted_prompt_is_not_a_verb(self):
        find, walked = self._run(stack='Run `claude "fix the failing test"`.\n')
        self.assertEqual((find, walked), ([], 0))

    def test_an_unrecognized_word_is_a_finding(self):
        find, walked = self._run(eval_body="Reuses your session via `claude login`.\n")
        self.assertEqual([(f.rel, f.verb) for f in find], [("evaluations/x.md", "login")])
        self.assertEqual(walked, 1)

    def test_discovery_files_are_walked(self):
        find, walked = self._run(discovery_body="Search terms (`claude code skill`).\n")
        self.assertEqual([(f.rel, f.verb) for f in find], [("discovery/loop1.md", "code")])
        self.assertEqual(walked, 1)

    def test_a_dotfile_reference_is_not_a_command(self):
        """`.claude` is the config directory, not the CLI — a preceding `.` must block the
        match the same way a preceding word char or hyphen does."""
        find, walked = self._run(stack="Install via `cp -r .claude /path/to/project/`.\n")
        self.assertEqual((find, walked), ([], 0))

    def test_a_hyphenated_tool_name_is_not_a_command(self):
        """`claude-code` and `claude-squad` are tool names, not `claude` followed by a
        verb — a hyphen right after "claude" must block the match."""
        find, walked = self._run(
            stack="`claude-code → CLAUDE.md`; `claude-squad: stable 1.0.19 (bottled)`.\n")
        self.assertEqual((find, walked), ([], 0))

    def test_bare_claude_with_no_argument_is_not_walked(self):
        find, walked = self._run(stack="Just run `claude` to start a session.\n")
        self.assertEqual((find, walked), ([], 0))

    def test_a_command_framed_as_the_wrong_one_is_still_skipped(self):
        """NEGATION reused rather than re-invented — the issue's own instruction."""
        find, _walked = self._run(
            stack="Not `claude bogus-verb` — that command does not exist.\n")
        self.assertEqual(find, [])


class TestRepoInstallRecord(unittest.TestCase):
    """`skills-lock.json` is the one install record inside the tree, and nothing read it
    (#473). Detectors F and Y read the HOME lockfile and are local-only for that reason;
    this one is committed, so it is as readable in CI as CATALOG.md."""

    CHEAD = ("| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |\n"
             "|---|---|---|---|---|---|\n")
    VHEAD = "| Tool | Type | Auto | Free | Evaluated | Evidence |\n|---|---|---|---|---|---|\n"

    def _ctx(self, d, lock, rows, verdicts):
        if lock is not None:
            _write(d, "skills-lock.json", json.dumps(lock))
        cat = ["# Catalog", "", "## Skills & Plugins", "", self.CHEAD.rstrip()]
        cat += [f"| [{n}]({u}) | tool | x | y | z |  |" for n, u in rows]
        _write(d, "CATALOG.md", "\n".join(cat) + "\n")
        comp = ["# Tool Comparison", "", "## Skills & Plugins", "", self.VHEAD.rstrip()]
        comp += [f"| {t} | tool | | ✓ | {v} | REVIEW |" for t, v in verdicts]
        _write(d, "COMPARISON.md", "\n".join(comp) + "\n")
        _write(d, "STACK.md", "# Stack\n")
        return audit.DetectorContext(d)

    def _run(self, lock, rows, verdicts):
        with tempfile.TemporaryDirectory() as d:
            return audit.audit_repo_installs(self._ctx(d, lock, rows, verdicts))

    LOCK: ClassVar[dict] = {"skills": {"find-skills": {"source": "vercel-labs/skills"}}}

    def test_a_vendored_source_still_at_discovery_log_is_the_counted_finding(self):
        # The shape #473 measured: the repo runs it, and the queue holds a lead for it.
        f, ev, records = self._run(
            self.LOCK, [("vercel-labs/skills", "https://github.com/vercel-labs/skills")],
            [("vercel-labs/skills", "discovery-log")])
        self.assertEqual([(x.kind, x.tool, x.key) for x in f],
                         [("UNEVALUATED-INCUMBENT", "vercel-labs/skills", "find-skills")])
        self.assertEqual((ev, records), ([], 1))

    def test_a_settled_source_is_printed_and_never_counted(self):
        # V's `acked` / W's `cleared` / X's `FACETED`: this is the outcome the detector
        # exists to produce, so counting it would leave the headline unable to reach zero.
        f, ev, records = self._run(
            self.LOCK, [("vercel-labs/skills", "https://github.com/vercel-labs/skills")],
            [("vercel-labs/skills", "ADOPT")])
        self.assertEqual(f, [])
        self.assertEqual([(x.kind, x.verdict) for x in ev], [("evaluated", "ADOPT")])
        self.assertEqual(records, 1)

    def test_a_vendored_source_with_no_catalog_row_is_counted(self):
        # Found from the install side — the only side that can see it (detector Y's rule).
        f, _ev, records = self._run(self.LOCK, [], [])
        self.assertEqual([(x.kind, x.slug) for x in f],
                         [("UNCATALOGUED", "vercel-labs/skills")])
        self.assertEqual(records, 1)

    def test_resolution_is_by_slug_never_by_the_lockfile_key(self):
        # `find-skills` is a skill NAME several packs ship; the identity is the source
        # slug (#343/#366/#374). A key-keyed lookup would answer about a stranger.
        f, _ev, _r = self._run(
            self.LOCK,
            [("find-skills", "https://github.com/someone-else/find-skills"),
             ("vercel-labs/skills", "https://github.com/vercel-labs/skills")],
            [("find-skills", "SKIP"), ("vercel-labs/skills", "discovery-log")])
        self.assertEqual([(x.kind, x.tool) for x in f],
                         [("UNEVALUATED-INCUMBENT", "vercel-labs/skills")])

    def test_a_shared_slug_resolves_to_the_row_linking_the_repo_root(self):
        # #465: several rows can sit behind one slug, and the lockfile's `source` names
        # the whole artifact — so the container row is the subject, not row order.
        f, _ev, _r = self._run(
            self.LOCK,
            [("member", "https://github.com/vercel-labs/skills/tree/main/skills/a"),
             ("vercel-labs/skills", "https://github.com/vercel-labs/skills")],
            [("member", "SKIP"), ("vercel-labs/skills", "discovery-log")])
        self.assertEqual([(x.kind, x.tool) for x in f],
                         [("UNEVALUATED-INCUMBENT", "vercel-labs/skills")])

    def test_a_missing_lockfile_reports_zero_records_not_zero_findings(self):
        # Detector V's rule: vendoring nothing is a different statement from a clean
        # sweep, so the headline must be able to say which one it saw.
        self.assertEqual(self._run(None, [], []), ([], [], 0))
        self.assertEqual(self._run({"skills": {}}, [], []), ([], [], 0))

    def test_a_malformed_lockfile_is_not_a_crash(self):
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, {"skills": "not-a-dict"}, [], [])
            self.assertEqual(audit.audit_repo_installs(ctx), ([], [], 0))
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, None, [], [])
            _write(d, "skills-lock.json", "{ this is not json")
            self.assertEqual(audit.audit_repo_installs(ctx), ([], [], 0))

    def test_an_entry_with_no_source_is_not_a_record(self):
        # No slug means nothing to resolve; counting it would put a number on the board
        # that nothing here can move.
        self.assertEqual(self._run({"skills": {"x": {"skillPath": "a/SKILL.md"}}}, [], []),
                         ([], [], 0))

    @staticmethod
    def _live(*parts):
        with open(os.path.join(ROOT, *parts), encoding="utf-8") as fh:
            return fh.read()

    HOMES = (".agents/skills", ".claude/skills")

    def test_live_tree_lockfile_entries_resolve_to_a_real_skill_directory(self):
        # The invariant that makes the record trustworthy at all: a lockfile naming a
        # skill the tree does not contain would make every finding above unfalsifiable.
        lock = json.loads(self._live("skills-lock.json"))
        homes = self.HOMES
        for key in lock.get("skills", {}):
            self.assertTrue(
                any(os.path.isfile(os.path.join(ROOT, h, key, "SKILL.md")) for h in homes),
                f"skills-lock.json names `{key}` but no SKILL.md exists under {homes}")

    def test_live_tree_opencode_skill_permissions_name_a_real_skill(self):
        # `permission.skill` is `{"*": "allow", "add-catalog-entry": "ask"}` — so renaming
        # or moving the skill does not break the rule loudly, it silently downgrades a
        # deliberate confirmation gate to auto-allow under the `*` default.
        cfg = json.loads(self._live("opencode.json"))
        named = [k for k in (cfg.get("permission", {}).get("skill") or {}) if k != "*"]
        homes = self.HOMES
        for name in named:
            self.assertTrue(
                any(os.path.isfile(os.path.join(ROOT, h, name, "SKILL.md")) for h in homes),
                f"opencode.json gates skill `{name}`, which no home defines — the rule is "
                "dead and `*` decides instead")

    def test_live_tree_every_project_skill_declares_its_own_name(self):
        # Both harnesses key a skill by its frontmatter `name:`, not its folder, and
        # opencode drops any skill with no `description:` before the model ever sees it.
        for home in self.HOMES:
            base = os.path.join(ROOT, home)
            for folder in sorted(os.listdir(base)) if os.path.isdir(base) else []:
                path = os.path.join(base, folder, "SKILL.md")
                if not os.path.isfile(path):
                    continue
                text = self._live(home, folder, "SKILL.md")
                head = text.split("---")[1] if "---" in text else ""
                self.assertRegex(head, rf"(?m)^name:\s*{re.escape(folder)}\s*$",
                                 f"{home}/{folder}/SKILL.md: frontmatter `name:` must "
                                 "match the folder")
                self.assertRegex(head, r"(?m)^description:\s*\S",
                                 f"{home}/{folder}/SKILL.md: a skill with no "
                                 "`description:` is filtered out and never surfaced")

    def test_watchlist_reads_the_shared_property_not_its_own_regex(self):
        # The two sources meet in WATCHLIST's Stage column (#416); one implementation.
        with open(os.path.join(ROOT, "watchlist.py"), encoding="utf-8") as f:
            body = f.read()
        self.assertNotIn("Dev loop stage:\\*\\*", body,
                         msg="watchlist.py re-implements the stage-header regex")
        self.assertIn("dev_loop_stage", body)

    def test_the_live_tree_reports_a_number_not_an_error(self):
        drift, stack_drift, comparable, _u = audit.audit_stage_drift(
            audit.DetectorContext(ROOT))
        self.assertGreater(comparable, 100, msg="the detector stopped resolving evals")
        for f in drift + stack_drift:
            self.assertTrue(f.header, msg=f"{f.tool} reported with no header to quote")


# ----------------------------------------------------------------- routine gate contract (#449)
class TestRoutineGateContract(unittest.TestCase):
    """`docs/agents/routines.md` is what an unattended cloud agent reads before deciding
    whether to merge its own PR. It carried the repo's only standing licence to proceed
    past a red gate — "a detector-A-only failure is not a blocker" — written when the
    install resolver reported *could not check* as BROKEN.

    #448 removed the reason; this removes the licence and keeps it removed. The risk was
    never the stale sentence: the carve-out named a **detector** rather than a **cause**,
    so it also excused a genuine 404 install command — the one thing detector A exists to
    catch, in the one lane that writes install commands into CATALOG.md and evaluations/
    and is least able to notice a bad one.

    Reads the real doc, because the drift is *in* that file and a fixture would pin
    nothing (TestPluginFrontDoorSignals' rule)."""

    DOC: ClassVar[str] = os.path.join(ROOT, "docs", "agents", "routines.md")

    # The exact shape of the exception, not the word "detector": the doc must stay free
    # to explain WHY there is no exception, and does.
    _EXCUSED = re.compile(r"not a blocker|is not blocking|except(ion)? .{0,40}\bdetector\b",
                          re.IGNORECASE)

    def _text(self):
        with open(self.DOC, encoding="utf-8") as f:
            return f.read()

    def test_no_gate_failure_is_excused(self):
        for i, line in enumerate(self._text().splitlines(), 1):
            if line.lstrip().startswith(("*", ">")) or "used to" in line:
                continue   # quoting the retracted rule is how the doc explains itself
            self.assertIsNone(self._EXCUSED.search(line),
                              msg=f"routines.md:{i} excuses a red gate: {line.strip()!r}")

    def test_the_do_not_merge_list_gates_every_check(self):
        text = self._text()
        self.assertIn("**`make check` is red.**", text)
        self.assertNotIn("on anything other than", text)

    def test_it_tells_the_agent_what_an_offline_run_looks_like(self):
        # Without this the next reader sees UNCHECKED/INCONCLUSIVE, reads it as red, and
        # re-adds the carve-out. Naming the shape is what makes "no exception" workable.
        text = self._text()
        for token in ("UNCHECKED", "INCONCLUSIVE", "#448"):
            self.assertIn(token, text, msg=f"routines.md never mentions {token}")


# ------------------------------------------------- agent-facing skill contracts (#477)
class TestSkillContracts(unittest.TestCase):
    """A project skill is a procedure an agent follows instead of deriving one, so a fact
    it restates from the code is load-bearing in the way `plugin/README.md`'s facts are —
    *gate the shared facts, not the file*. Project skills were pinned for frontmatter
    shape only (`name:` matches the folder, a `description:` exists), never for what the
    body claims, and both claims below had rotted:

      `/triage-lead`        said it served P1/P2/P3 while `triage.py` routed FIVE bands to
                            it. Wrong the day it was written — #269 created the bands
                            including P4 and the command line, #271 wrote the skill two
                            issues later — and wrong again when #343/#394 added P5. Three
                            edits since (#323, #330, #358) left the list untouched.
      `/add-catalog-entry`  named `plugin/CLAUDE` as a reconcile target. That file was
                            renamed in #441/#442, and its REAPPEARANCE is a check-plugin
                            `FRONT-DOOR` finding — so the skill pointed at a write target
                            whose existence fails `make check`.

    Both derive from the code rather than hand-listing, so adding a band or a count target
    fails here instead of silently outdating the skill."""

    @staticmethod
    def _skill(name):
        with open(os.path.join(ROOT, ".claude", "skills", name, "SKILL.md"),
                  encoding="utf-8") as fh:
            return fh.read()

    def test_the_skill_names_every_band_routed_to_it(self):
        # Keyed on a ROW of the skill's band table, not on the bare token appearing
        # somewhere in the file: prose discussing P5 is not a procedure for P5, and a
        # substring pin would pass more easily the more of the table was deleted — the
        # test direction #443 caught in the counts hook.
        routed = [n for n, _, _ in triage.BANDS if n != "P0 measure"]
        rows = [ln for ln in self._skill("triage-lead").splitlines()
                if ln.startswith("| **P")]
        for band in routed:
            match = [r for r in rows if r.startswith(f"| **{band}**")]
            self.assertEqual(len(match), 1,
                             msg=f"NEXT-EVALS.md prints `/triage-lead` for {band!r}; the "
                                 "skill's band table has no row for it, so an agent "
                                 "handed a lead from it follows another band's procedure")
            # Three cells of content: why the lead is here, and what a SKIP here reads.
            self.assertGreaterEqual(len([c for c in match[0].split("|") if c.strip()]), 3,
                                    msg=f"{band!r}'s row states no disposition")

    def test_the_skill_points_at_the_test_that_pins_it(self):
        # The skill tells a reader which check keeps its table honest. A renamed class
        # would leave it citing a test that does not exist — this PR's own defect class.
        self.assertIn(type(self).__name__, self._skill("triage-lead"))

    def test_the_routing_rule_itself_is_pinned(self):
        # The test above derives `routed` from BANDS on the premise that every band but
        # P0 prints /triage-lead. If that line changes and nothing reads it, the pin goes
        # on passing while measuring the wrong set — #443's rule that a check must not
        # rest on a fact it does not verify.
        with open(os.path.join(ROOT, "triage.py"), encoding="utf-8") as fh:
            src = fh.read()
        self.assertIn('cmd = "/evaluate-tool" if name == "P0 measure" else "/triage-lead"',
                      src, msg="the band->command rule moved; re-derive `routed` from it")

    def test_a_band_whose_disposition_names_a_value_supplies_it(self):
        # P2's disposition reads `<incumbent>` and P5's `<container>`. Both were computed
        # to assign the band and then dropped, so the page named a value it never gave
        # (#457, then #477). A NEW placeholder band must make a decision here rather than
        # landing in neither — same shape as the Makefile's NO_APPLY_MODE set.
        placeholder = {n for n, _, disp in triage.BANDS if re.search(r"<\w+>", disp)}
        self.assertEqual(placeholder, {"P2 challenger", "P5 ships-inside"},
                         msg="a band's disposition gained or lost a placeholder — teach "
                             "render() to supply it, then update this set")
        ranked = [(2.0, "a", "Plan", 3, 1.0)]
        for band, incumbents, containers, expect in (
                ("P2 challenger", {"a": ["GSD"]}, {}, "challenges GSD"),
                ("P5 ships-inside", {}, {"a": "o/pack"}, "ships inside `o/pack`")):
            ordered = {n: [] for n, _, _ in triage.BANDS}
            ordered[band] = ranked
            out = triage.render(ordered, ranked, incumbents, containers)
            row = next(ln for ln in out.splitlines() if ln.startswith("| a |"))
            self.assertIn(expect, row, msg=f"{band} does not supply its own placeholder")

    def test_the_reconcile_targets_are_named_by_path(self):
        # `README/CLAUDE/STACK/plugin/CLAUDE` is a slash-joined shorthand, so a rename
        # leaves it looking plausible. Naming the real paths makes it checkable.
        reconcile = _load("reconcile_counts", os.path.join(ROOT, "reconcile-counts.py"))
        text = self._skill("add-catalog-entry")
        for path in reconcile.FILES_TOTAL:
            self.assertIn(path, text,
                          msg=f"reconcile-counts.py rewrites {path}; the skill that tells "
                              "an agent to run it does not say so")


# ----------------------------------------------------------------- freshness (#445)
class TestFreshness(unittest.TestCase):
    """freshness.py answers the SessionStart hook's two questions. The hook used to
    answer them itself and got both wrong (#445): staleness from file **mtime** against
    a flat 30 days, and "is this star catalogued?" from the bare repo **basename** as a
    substring of the whole catalog.

    The star tests are the #445 corpus, not invented cases. Each one is a starred repo
    the old hook hid, and each hid for a different reason, which is why they are pinned
    separately: a fix that only handled same-name-different-owner would leave the prose
    matches live."""

    CATALOG = (
        "| Tool | Type | One-liner | Problem | Overlaps | Ships inside |\n"
        "|---|---|---|---|---|---|\n"
        "| [agent-skills](https://github.com/addyosmani/agent-skills) | skill | "
        "one-command containerized runs, its own computer | p | conductor, Docling (ext.) | |\n"
        "| [awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) | reference | o | p | q | |\n"
        "| [codebase-design](https://github.com/mattpocock/skills/tree/main/skills/engineering/codebase-design)"
        " | skill | o | p | q | mattpocock/skills |\n"
        "\nNote: the `x` record now redirects to "
        "[ai-creator-academy](https://github.com/Anil-matcha/ai-creator-academy).\n"
    )

    def _gaps(self, *slugs):
        return freshness.uncatalogued("\n".join(slugs), self.CATALOG)

    def test_a_bare_basename_in_prose_never_hides_a_repo(self):
        # `apple/container` matched "containerized"; `cloudflare/computer` matched the
        # word "computer" in a one-liner. Neither is a github link to anything.
        self.assertEqual(self._gaps("apple/container", "cloudflare/computer"),
                         ["apple/container", "cloudflare/computer"])

    def test_a_basename_in_an_overlaps_cell_never_hides_a_repo(self):
        # Two unrelated repos both named `conductor` were hidden by a bare `conductor`
        # token. #374's rule: between two rows that each name a tool, a basename is not
        # a synonym.
        self.assertEqual(self._gaps("Netflix/conductor", "gemini-cli-extensions/conductor"),
                         ["Netflix/conductor", "gemini-cli-extensions/conductor"])

    def test_an_external_marker_never_hides_the_repo_it_excludes(self):
        # `Docling (ext.)` exists to say the tool is NOT catalogued, and it is what
        # convinced the old hook the tool WAS (detector F's STALE-EXT shape, #403).
        self.assertEqual(self._gaps("docling-project/docling"), ["docling-project/docling"])

    def test_same_name_different_owner_is_a_gap(self):
        self.assertEqual(self._gaps("appcypher/awesome-mcp-servers"),
                         ["appcypher/awesome-mcp-servers"])

    def test_a_catalogued_slug_is_not_a_gap(self):
        self.assertEqual(self._gaps("punkpeye/awesome-mcp-servers"), [])

    def test_resolution_is_case_insensitive(self):
        # GitHub slugs are case-preserving but case-insensitive; `gh` returns the
        # canonical casing and a catalog link may not match it.
        self.assertEqual(self._gaps("PunkPeye/Awesome-MCP-Servers"), [])

    def test_a_subpath_link_resolves_to_its_owner_repo(self):
        # Starring the container of a catalogued subpath is not a gap. This is the bug
        # latent in /sync-stars' own `github\.com/[^)]+` extraction (#445).
        self.assertEqual(self._gaps("mattpocock/skills"), [])

    def test_resolution_is_generous_beyond_the_name_cell(self):
        # Any github link anywhere counts, not only a row's Name cell: a repo LINKED
        # from a redirect note is one a human has already looked at, and re-offering it
        # as a new lead costs more than missing it (detector V's rule). A repo merely
        # *named* in prose is a different thing and stays a gap — that is the case the
        # old basename grep got wrong.
        self.assertEqual(self._gaps("Anil-matcha/ai-creator-academy"), [])

    def test_read_slugs_drops_anything_that_is_not_owner_repo(self):
        # A `gh` error line or a stray URL on stdin must never become a lead.
        self.assertEqual(
            freshness.read_slugs("a/b\n\n# comment\nnot-a-slug\nhttps://x/y/z\n/leading\ntrailing/\nA/B\nc/d"),
            ["a/b", "c/d"])

    def test_report_is_empty_when_there_is_nothing_to_say(self):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "evaluations/x.md", "| [x](https://github.com/a/x) | tool | o | p | q |\n")
            self.assertEqual(freshness.report("", self.CATALOG, root=d), [])

    def test_staleness_comes_from_the_repos_own_sweep(self):
        # Not mtime: the fixture files are written milliseconds ago and are still stale,
        # because the field that decides is **Last verified:** against the Type's
        # threshold. The reverse case is the one mtime got structurally wrong — a fresh
        # clone made every eval zero minutes old and the check silent.
        # 200 days: past the harness threshold (120), inside the reference one (365).
        old = (datetime.date.today() - datetime.timedelta(days=200)).isoformat()
        with tempfile.TemporaryDirectory() as d:
            _write(d, "evaluations/h.md",
                   f"**Last verified:** {old}\n\n| [h](https://github.com/a/h) | harness | o | p | q |\n")
            _write(d, "evaluations/r.md",
                   f"**Last verified:** {old}\n\n| [r](https://github.com/a/r) | reference | o | p | q |\n")
            lines = freshness.report("", self.CATALOG, root=d)
        self.assertEqual(len(lines), 1, msg=lines)
        self.assertIn("threshold 120d", lines[0])   # the harness Type's, not a flat 30
        self.assertIn("h", lines[0])                # the reference at 400d is NOT stale

    def test_the_detail_cap_is_disclosed_not_silent(self):
        old = (datetime.date.today() - datetime.timedelta(days=400)).isoformat()
        with tempfile.TemporaryDirectory() as d:
            for i in range(5):
                _write(d, f"evaluations/e{i}.md",
                       f"**Last verified:** {old}\n\n| [e{i}](https://github.com/a/e{i}) | harness | o | p | q |\n")
            lines = freshness.report("", self.CATALOG, root=d, limit=2)
        self.assertEqual(len(lines), 3)
        self.assertIn("and 3 more", lines[-1])

    def test_the_network_stays_out_of_this_script(self):
        # refresh-metadata.py is documented as the only script that calls `gh`. Keeping
        # the fetch in the caller is also what makes this file testable offline.
        with open(os.path.join(ROOT, "freshness.py"), encoding="utf-8") as f:
            body = "\n".join(l for l in f if not l.lstrip().startswith("#"))
        code = body.split('"""', 2)[-1]
        for net in ("gh api", "subprocess", "urllib", "requests"):
            self.assertNotIn(net, code, msg=f"freshness.py reaches the network: {net!r}")


class TestFreshnessHook(unittest.TestCase):
    """The SessionStart hook. Both directions are pinned, and the structural test is the
    one that matters: the defects #445 fixed were a bash re-implementation of two facts
    the repo already owns, and a re-implementation regrows the moment someone wants the
    hook to "still say something" outside the repo."""

    HOOK: ClassVar[str] = os.path.join(ROOT, "plugin", "hooks", "check-freshness.sh")
    QUIET: ClassVar[str] = '{"continue":true,"suppressOutput":true}'

    def _run(self, cwd, stars=""):
        """Runs the hook with a `gh` shim on PATH, so no test touches the network."""
        with tempfile.TemporaryDirectory() as bin_d:
            shim = os.path.join(bin_d, "gh")
            with open(shim, "w", encoding="utf-8") as f:
                f.write("#!/bin/bash\nprintf '%s' " + shlex.quote(stars) + "\n")
            os.chmod(shim, 0o755)
            env = dict(os.environ, PATH=bin_d + os.pathsep + os.environ["PATH"])
            return subprocess.run(["bash", self.HOOK], cwd=cwd, env=env,
                                  capture_output=True, text=True, check=False)

    def _fixture_repo(self, d):
        subprocess.run(["git", "init", "-q"], cwd=d, check=True)
        for f in ("freshness.py", "catalog_lib.py", "audit-evals.py"):
            shutil.copy(os.path.join(ROOT, f), os.path.join(d, f))
        _write(d, "CATALOG.md", TestFreshness.CATALOG)
        _write(d, "evaluations/x.md", "| [x](https://github.com/a/x) | tool | o | p | q |\n")

    def test_a_foreign_repo_gets_the_quiet_payload_and_nothing_else(self):
        # The installed plugin fires this at every session start in someone else's
        # project, where the advice ("run /update-catalog") names an operation on a
        # catalog they do not have.
        with tempfile.TemporaryDirectory() as d:
            subprocess.run(["git", "init", "-q"], cwd=d, check=True)
            r = self._run(d, stars="some/repo\n")
            self.assertEqual(r.stdout.strip(), self.QUIET, msg=r.stdout + r.stderr)
            self.assertEqual(r.returncode, 0, msg=r.stderr)

    def test_outside_any_git_repo_it_is_quiet(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(self._run(d).stdout.strip(), self.QUIET)

    def test_it_reports_an_uncatalogued_star(self):
        with tempfile.TemporaryDirectory() as d:
            self._fixture_repo(d)
            r = self._run(d, stars="Netflix/conductor\n")
            self.assertIn("1 starred repo(s) with no catalog row", r.stdout, msg=r.stdout + r.stderr)

    def test_it_is_quiet_when_every_star_is_catalogued(self):
        with tempfile.TemporaryDirectory() as d:
            self._fixture_repo(d)
            r = self._run(d, stars="punkpeye/awesome-mcp-servers\n")
            self.assertEqual(r.stdout.strip(), self.QUIET, msg=r.stdout + r.stderr)

    def test_output_is_never_a_control_payload_concatenated_with_text(self):
        # The old hook printed the JSON line AND 100 lines of text, so the payload did
        # not parse (`Extra data: line 3 column 1`) and the control line was simply the
        # first thing the user saw. Either shape alone is fine; both together is not.
        with tempfile.TemporaryDirectory() as d:
            self._fixture_repo(d)
            for stars in ("Netflix/conductor\n", "punkpeye/awesome-mcp-servers\n"):
                out = self._run(d, stars=stars).stdout
                if out.strip().startswith("{"):
                    json.loads(out)          # a control payload must be parseable alone
                else:
                    self.assertNotIn("{", out)

    def test_the_hook_does_not_re_answer_either_question_in_bash(self):
        # The #445 regression guard. `stat`/mtime is the staleness re-implementation and
        # `cut -d/ -f2` is the identity-by-name one; either returning is the whole bug.
        with open(self.HOOK, encoding="utf-8") as f:
            body = "\n".join(l for l in f if not l.lstrip().startswith("#"))
        self.assertIn("freshness.py", body)
        for dead in ("stat -f", "stat -c", "STALE_DAYS", "cut -d/", "grep -qi"):
            self.assertNotIn(dead, body, msg=f"hook re-answers in bash: {dead!r}")

    def test_session_start_is_async(self):
        # ~9s of paginated `gh` on startup|clear|compact, previously on the critical path.
        with open(os.path.join(ROOT, "plugin", "hooks", "hooks.json"), encoding="utf-8") as f:
            hooks = json.load(f)
        entry = hooks["hooks"]["SessionStart"][0]["hooks"][0]
        self.assertTrue(entry["async"], msg="SessionStart hook blocks the session")


# ----------------------------------------------------------------- plugin/README.md drift
class TestPluginFrontDoorSignals(unittest.TestCase):
    """plugin/README.md is HAND-maintained — unlike plugin/docs/, which
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
        plugin = self._count_word(self._text("plugin/README.md"), "plugin/README.md")
        self.assertEqual(plugin, root,
                         msg="plugin/README.md quotes a different signal count than root")

    def test_plugin_names_every_root_signal(self):
        # Root lists them after a colon, up to the parenthetical gloss on the last one.
        m = re.search(r"quality signals:\s*(.+?)\s*\(", self._text("CLAUDE.md"))
        self.assertIsNotNone(m, msg="root CLAUDE.md no longer lists its signals after a colon")
        # ", and X" splits on the comma first, so the optional "and " is consumed there too.
        names = [s for s in re.split(r",\s*(?:and\s+)?|\s+and\s+", m.group(1)) if s]
        self.assertGreaterEqual(len(names), 5, msg=f"parsed too few signals: {names}")
        plugin = self._text("plugin/README.md")
        for n in names:
            self.assertIn(n, plugin, msg=f"plugin/README.md omits the {n} signal")


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
    # The sync repoints links that leave the bundle (#437), so the fixture carries that
    # sibling too — same reason the reconcile fixture carries audit-evals.py.
    shutil.copy(os.path.join(ROOT, "rewrite-doc-links.py"), os.path.join(d, "rewrite-doc-links.py"))
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

    def _fixture(self, d, script):
        """A minimal repo both halves of the gate can run: a fake gate script plus the
        `check-data` target they now delegate to (#459)."""
        _write(d, "audit-evals.py", script)
        _write(d, "Makefile", "check-data:\n\tpython3 audit-evals.py --offline\n")

    def test_gate_blocks_commit_when_audit_fails(self):
        with tempfile.TemporaryDirectory() as d:
            self._fixture(d, self._FAILING_AUDIT)
            r = self._run_gate(d, '{"tool_input": {"command": "git commit -m x"}}')
            self.assertEqual(r.returncode, 2, msg=r.stdout + r.stderr)
            self.assertIn("BLOCKED", r.stderr)

    def test_gate_passes_non_commit_despite_failing_audit(self):
        with tempfile.TemporaryDirectory() as d:
            self._fixture(d, self._FAILING_AUDIT)
            r = self._run_gate(d, '{"tool_input": {"command": "git status"}}')
            self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)

    def test_gate_passes_commit_when_audit_clean(self):
        with tempfile.TemporaryDirectory() as d:
            self._fixture(d, "import sys; sys.exit(0)\n")
            r = self._run_gate(d, '{"tool_input": {"command": "git commit -m x"}}')
            self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)

    def test_gate_fails_open_on_garbage_payload(self):
        with tempfile.TemporaryDirectory() as d:
            self._fixture(d, self._FAILING_AUDIT)
            r = self._run_gate(d, "not json at all")
            self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)

    def test_gate_fails_open_when_the_target_is_absent(self):
        # "Could not run" is not "failed" (#319's rule, #459). A tree with no `check-data`
        # target — someone else's repo, an old checkout — must let the commit through.
        # Delegating to `make` makes this reachable in a way `python3 script.py` was not,
        # so it is pinned rather than assumed.
        with tempfile.TemporaryDirectory() as d:
            _write(d, "audit-evals.py", self._FAILING_AUDIT)  # no Makefile
            r = self._run_gate(d, '{"tool_input": {"command": "git commit -m x"}}')
            self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)

    @unittest.skipUnless(shutil.which("bun"), "bun not installed; opencode gate covered by the predicate pin only")
    def test_opencode_gate_blocks_commit_and_passes_noncommit(self):
        # Executes the REAL commit-gate plugin under bun against a fixture whose
        # audit always fails — the behavioral counterpart to the predicate pin.
        with tempfile.TemporaryDirectory() as d:
            self._fixture(d, self._FAILING_AUDIT)
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

    CATALOG = ("| Tool | Type | One-liner | Problem | Overlaps with | Ships inside |\n"
               "|---|---|---|---|---|---|\n"
               "| [foo](https://github.com/x/foo) | tool | l | p | | |\n"
               "| [bar](https://github.com/x/bar) | tool | l | p | | |\n")

    def _run(self, stack, ledger, comp, catalog=None):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "STACK.md", stack)
            _write(d, "STACK-LEDGER.md", ledger)
            _write(d, "COMPARISON.md", comp)
            _write(d, "CATALOG.md", self.CATALOG if catalog is None else catalog)
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
        catalog = ("| Tool | Type | One-liner | Problem | Overlaps with | Ships inside |\n"
                   "|---|---|---|---|---|---|\n"
                   "| [superpowers](https://github.com/obra/superpowers) | skill | l | p | | |\n")
        self.assertEqual(self._run(stack, ledger, comp, catalog), [])  # matched via repo basename

    # --- the reverse direction: a STACK member the catalog SKIPped (#416) ---

    def test_skipped_tool_in_stack_flagged(self):
        # Every other J check runs ledger->STACK or verdict->STACK. A SKIP verdict never
        # reaches the ledger (it holds ADOPT/KEEP only), so the install list could
        # recommend an eliminated tool forever — trailofbits/skills did, for ten months.
        comp = self.COMP.replace("| foo | tool | | ✓ | ADOPT | RUN |",
                                 "| foo | tool | | ✓ | SKIP | RUN |")
        ledger = "| bar | ADOPT | Plan | no | overlaps foo |\n"
        probs = self._run(self.STACK, ledger, comp)
        self.assertTrue(any("SKIPped in COMPARISON" in p and "x/foo" in p for p in probs), probs)

    def test_skip_check_resolves_by_slug_not_link_text(self):
        # The row reads "GSD" and the verdict is filed under "superpowers" — resolution goes
        # through the URL slug to the catalog row's name, detector P's rule. Keying on the
        # display text would silently pass every renamed pick.
        stack = "## Implement\n| [GSD](https://github.com/obra/superpowers) | desc | `cmd` | sig |\n"
        comp = ("## Implement\n| Tool | Type | Auto | Free | Evaluated |\n|---|---|---|---|---|\n"
                "| superpowers | skill | | ✓ | SKIP |\n")
        catalog = ("| Tool | Type | One-liner | Problem | Overlaps with | Ships inside |\n"
                   "|---|---|---|---|---|---|\n"
                   "| [superpowers](https://github.com/obra/superpowers) | skill | l | p | | |\n")
        probs = self._run(stack, "", comp, catalog)
        self.assertTrue(any("SKIPped in COMPARISON" in p for p in probs), probs)

    def test_uncatalogued_stack_pick_is_not_a_skip_finding(self):
        # A pick whose repo has no catalog row resolves to no verdict. That is a different
        # gap (and not one this check can name) — reporting it here would flag a healthy row.
        stack = "## Plan\n| [zzz](https://github.com/x/zzz) | desc | `cmd` | sig |\n"
        probs = self._run(stack, "", self.COMP)
        self.assertFalse(any("SKIPped in COMPARISON" in p for p in probs), probs)

    def test_non_skip_verdicts_never_flagged(self):
        for verdict in ("ADOPT", "KEEP", "CONDITIONAL", "DEFER", "discovery-log"):
            comp = self.COMP.replace("| foo | tool | | ✓ | ADOPT | RUN |",
                                     f"| foo | tool | | ✓ | {verdict} | RUN |")
            probs = self._run(self.STACK, self.LEDGER_OK, comp)
            self.assertFalse(any("SKIPped in COMPARISON" in p for p in probs), (verdict, probs))

    def test_live_stack_has_no_skipped_pick(self):
        # Pins the tree: the install list must never recommend an eliminated tool.
        probs = audit.audit_stack_drift(audit.DetectorContext(ROOT))
        self.assertEqual([p for p in probs if "SKIPped in COMPARISON" in p], [])

    # --- resolving a pick when one slug is claimed by several rows (#463) ---

    # A monorepo: three rows behind one `owner/repo`, each linking its own subpath, with
    # DIFFERENT verdicts — the live shape of anthropics/claude-plugins-official (9 rows,
    # all four verdict values) reduced to the three cases that matter.
    MONO = ("| Tool | Type | One-liner | Problem | Overlaps with | Ships inside |\n"
            "|---|---|---|---|---|---|\n"
            "| [alpha](https://github.com/x/pack/tree/main/plugins/alpha) | plugin | l | p | | x/pack |\n"
            "| [beta](https://github.com/x/pack/tree/main/plugins/beta) | plugin | l | p | | x/pack |\n"
            "| [pack](https://github.com/x/pack) | plugin | l | p | | |\n")
    MONO_COMP = ("## Plan\n| Tool | Type | Auto | Free | Evaluated | Evidence |\n"
                 "|---|---|---|---|---|---|\n"
                 "| alpha | plugin | | ✓ | SKIP | REVIEW |\n"
                 "| beta | plugin | | ✓ | KEEP | REVIEW |\n"
                 "| pack | plugin | | ✓ | KEEP | REVIEW |\n")

    def _resolve(self, text, url, catalog=None):
        row, cands = catalog_lib.resolve_link(
            catalog_lib.link_index(catalog or self.MONO), text, url)
        return (row.name if row else None,
                [c.name for c in cands] if cands else None)

    def test_unshared_slug_resolves_to_its_row(self):
        self.assertEqual(self._resolve("foo", "https://github.com/x/foo", self.CATALOG),
                         ("foo", None))

    def test_shared_slug_resolves_by_the_picks_own_name(self):
        # STACK links a component pick at the PACK ROOT, so the link identifies the
        # container while the text identifies the pick. The text wins: answering "is pack
        # SKIPped" is not the question that was asked.
        self.assertEqual(self._resolve("beta", "https://github.com/x/pack"), ("beta", None))

    def test_shared_slug_falls_back_to_an_exact_link(self):
        # No candidate is named "GSD", but one candidate's own URL is linked exactly.
        self.assertEqual(
            self._resolve("GSD", "https://github.com/x/pack/tree/main/plugins/beta"),
            ("beta", None))

    def test_shared_slug_matching_neither_resolves_to_nothing(self):
        # Not to whichever row the catalog lists first. The check cannot say which row it
        # would be checking, so it says so instead (#319's "silence is not success").
        row, candidates = self._resolve("gamma", "https://github.com/x/pack/tree/main/other")
        self.assertIsNone(row)
        self.assertEqual(candidates, ["alpha", "beta", "pack"])

    def test_container_row_is_the_one_linking_the_repo_root(self):
        # Deterministic where "the first row" was arbitrary: exactly one of the three
        # names the pack itself rather than an artifact inside it (#465).
        index = catalog_lib.link_index(self.MONO)
        self.assertEqual(catalog_lib.container_row(index, "x/pack").name, "pack")
        self.assertIsNone(catalog_lib.container_row(index, "x/nothing"))

    def test_ambiguous_pick_is_reported_not_skipped(self):
        stack = "## Plan\n| [gamma](https://github.com/x/pack/tree/main/other) | d | `c` | s |\n"
        probs = self._run(stack, "", self.MONO_COMP, self.MONO)
        self.assertTrue(any("3 catalog rows claim" in p and "gamma" in p for p in probs), probs)

    def test_the_skip_check_names_the_row_it_checked(self):
        stack = "## Plan\n| [alpha](https://github.com/x/pack) | d | `c` | s |\n"
        probs = self._run(stack, "", self.MONO_COMP, self.MONO)
        self.assertTrue(any("SKIPped in COMPARISON" in p and "'alpha'" in p for p in probs), probs)

    def test_a_sibling_of_the_skipped_row_is_not_flagged(self):
        # `beta` is KEEP and shares `alpha`'s slug. Resolving by slug alone reported this
        # as a SKIP whenever the catalog happened to list alpha first (#463).
        stack = "## Plan\n| [beta](https://github.com/x/pack) | d | `c` | s |\n"
        probs = self._run(stack, "", self.MONO_COMP, self.MONO)
        self.assertFalse(any("SKIPped in COMPARISON" in p for p in probs), probs)

    def test_findings_do_not_depend_on_catalog_row_order(self):
        # The property that was violated. Swapping two rows past each other is a pure
        # reorder, and on the live tree it turned a green `make check` into five gating
        # failures, each naming a KEEP tool for a SKIP belonging to neither.
        stack = ("## Plan\n| [alpha](https://github.com/x/pack) | d | `c` | s |\n"
                 "| [beta](https://github.com/x/pack) | d | `c` | s |\n")
        rows = self.MONO.splitlines(keepends=True)
        reordered = "".join([*rows[:2], rows[4], rows[3], rows[2]])
        self.assertEqual(self._run(stack, "", self.MONO_COMP, self.MONO),
                         self._run(stack, "", self.MONO_COMP, reordered))

    def test_live_stack_picks_all_resolve(self):
        # Nine of the tree's thirty picks link a slug several rows claim. Every one must
        # resolve to its OWN row — an unresolved pick is a check that silently did not run.
        ctx = audit.DetectorContext(ROOT)
        index = catalog_lib.link_index(ctx.catalog)
        for text, url, slug in audit._stack_picks_by_slug(ctx.stack):
            row, candidates = catalog_lib.resolve_link(index, text, url, slug)
            self.assertIsNone(candidates, msg=f"STACK pick '{text}' ({slug}) is ambiguous")
            if len(catalog_lib.rows_for_slug(index, slug)) > 1:
                self.assertEqual(row.name, text, msg=f"'{text}' resolved to a sibling: {row}")


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


# ----------------------------------------------------------------- gate coverage (#481)
class TestGateCoverage(unittest.TestCase):
    """#467's rule — a check reports the population it walked — reached all thirteen
    report-only detectors and none of the seven gates, where a bare `OK` is the
    strongest claim in the file and the line CI goes green on (#481)."""

    HEADER = "## Plan\n| Tool | Type | Auto | Free | Evaluated | Evidence |\n|---|---|---|---|---|---|\n"
    CAT = ("## Plan\n\n| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |\n"
           "|---|---|---|---|---|---|\n"
           "| [t](https://github.com/o/t) | tool | does a thing | a pain | x |  |\n")

    def _tree(self, d, comparison, evals, catalog=None):
        _write(d, "CATALOG.md", catalog if catalog is not None else self.CAT)
        _write(d, "COMPARISON.md", comparison)
        # Detector J reads both of these unconditionally, so a tree without them
        # cannot reach the gate at all — a fixture requirement, not a J finding.
        _write(d, "STACK.md", "# Stack\n")
        _write(d, "STACK-LEDGER.md", "# Ledger\n")
        for name, text in evals.items():
            _write(d, os.path.join("evaluations", name), text)
        return d

    def _cli(self, d, *flags):
        for fn in ("audit-evals.py", "catalog_lib.py"):
            shutil.copy(os.path.join(ROOT, fn), os.path.join(d, fn))
        return subprocess.run(["python3", "audit-evals.py", *flags],
                              cwd=d, capture_output=True, text=True, check=False)

    # --- the rule, applied to every gate ------------------------------------

    def test_every_offline_gate_headline_states_a_population(self):
        # Derived from OFFLINE_GATES, not hand-listed: an eighth gate added without a
        # population must fail here rather than inherit the silence this issue removed.
        with tempfile.TemporaryDirectory() as d:
            self._tree(d, self.HEADER + "| t | tool | | ✓ | SKIP | REVIEW |\n",
                       {"t.md": "**Evidence:** REVIEW\n\n## Verdict\n\n**SKIP**\n"})
            r = self._cli(d, "--offline")
            heads = [ln for ln in r.stdout.splitlines() if ln.startswith("== ")]
            self.assertEqual(len(heads), len(audit.OFFLINE_GATES), r.stdout)
            for h in heads:
                # `== <letter>. <title> — <...N...> ==` — a headline whose only digits
                # are the detector letter is the bare `OK` claim this issue is about.
                self.assertIn("—", h, msg=f"gate headline states no population: {h}")
                self.assertRegex(h.split("—", 1)[1], r"\d", msg=h)

    def test_coverage_never_reaches_the_exit_code(self):
        # THE invariant. A population is a report; only a finding may fail a build.
        # This tree is full of abstentions — an eval with a verdict and no COMPARISON
        # row, an eval with no `## How we tested` — and must still exit 0.
        with tempfile.TemporaryDirectory() as d:
            self._tree(d, self.HEADER + "| t | tool | | ✓ | SKIP | REVIEW |\n",
                       {"t.md": "**Evidence:** REVIEW\n\n## Verdict\n\n**SKIP**\n",
                        "rowless.md": "**Evidence:** REVIEW\n\n## Verdict\n\n**SKIP**\n",
                        "bare.md": "## Verdict\n\n**SKIP**\n"})
            r = self._cli(d, "--verdicts", "--fabrication")
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("no COMPARISON.md row at all", r.stdout)
            self.assertIn("rowless", r.stdout)

    def test_a_real_finding_still_fails_the_build(self):
        # The other direction: the refactor must not have turned a gate into a report.
        with tempfile.TemporaryDirectory() as d:
            self._tree(d, self.HEADER + "| t | tool | | ✓ | ADOPT | MEASURED |\n",
                       {"t.md": "**Evidence:** MEASURED\n\n## Verdict\n\n**SKIP**\n"})
            r = self._cli(d, "--verdicts")
            self.assertEqual(r.returncode, 1, r.stdout)
            self.assertIn("MISMATCH t", r.stdout)

    # --- D: the two abstentions, one of which was never stated --------------

    def _cov(self, comparison, evals):
        with tempfile.TemporaryDirectory() as d:
            self._tree(d, comparison, evals)
            return audit.verdict_coverage(audit.DetectorContext(d))

    def test_D_splits_leads_from_evals_with_no_row_at_all(self):
        # `discovery-log` was documented in code; "name didn't map" was an unchecked
        # assertion, and it is the one thing a verdict-sync gate cannot check about
        # itself — `design-extract` carried a real verdict with no row and D passed.
        cov = self._cov(self.HEADER + "| lead | tool | | ✓ | discovery-log | REVIEW |\n"
                        + "| real | tool | | ✓ | SKIP | REVIEW |\n",
                        {"lead.md": "## Verdict\n\n**discovery-log — tentative read**\n",
                         "real.md": "## Verdict\n\n**SKIP**\n",
                         "rowless.md": "## Verdict\n\n**ADOPT**\n",
                         "noverdict.md": "just prose.\n"})
        self.assertEqual(cov.declared, 3)          # evals carrying a `## Verdict`
        self.assertEqual(cov.compared, 1)          # only `real` reaches the comparison
        self.assertEqual(cov.leads, ["lead"])
        self.assertEqual(cov.unmapped, ["rowless"])

    def test_the_buckets_partition_the_declared_population(self):
        # compared + leads + unmapped == declared, so a reader can check the arithmetic
        # rather than trust the headline — the reason #435 gates a partition, not a total.
        cov = audit.verdict_coverage(audit.DetectorContext(ROOT))
        self.assertEqual(cov.compared + len(cov.leads) + len(cov.unmapped), cov.declared)
        self.assertGreater(cov.compared, 0)

    # --- the populations each gate walks ------------------------------------

    def test_fabrication_population_excludes_evals_asserting_nothing(self):
        with tempfile.TemporaryDirectory() as d:
            self._tree(d, self.HEADER, {"has.md": "## How we tested it\n\nsource review only.\n",
                                        "bare.md": "## Verdict\n\n**SKIP**\n"})
            ctx = audit.DetectorContext(d)
            self.assertEqual([e.name for e in audit.fabrication_population(ctx)], ["has"])
            self.assertEqual(len(ctx.evals), 2)   # the denominator the headline prints

    def test_verdict_evidence_population_is_adopt_keep_only(self):
        with tempfile.TemporaryDirectory() as d:
            self._tree(d, self.HEADER, {"a.md": "## Verdict\n\n**ADOPT**\n",
                                        "k.md": "## Verdict\n\n**KEEP**\n",
                                        "s.md": "## Verdict\n\n**SKIP**\n"})
            pop = audit.verdict_evidence_population(audit.DetectorContext(d))
            self.assertEqual(sorted(e.name for e in pop), ["a", "k"])

    def test_bulk_coverage_reports_the_human_exemption_apart(self):
        # An exemption folded into `OK` is indistinguishable from a check that ran.
        stamp = "**Last triaged:** 2026-01-01"
        with tempfile.TemporaryDirectory() as d:
            self._tree(d, self.HEADER, {
                "b.md": f"{stamp}  <!-- triaged: bulk -->\n\n## Verdict\n\n**SKIP**\n",
                "h.md": f"{stamp}  <!-- triaged: human -->\n\n## Verdict\n\n**ADOPT**\n",
                "none.md": "## Verdict\n\n**SKIP**\n"})
            cov = audit.bulk_triage_coverage(audit.DetectorContext(d))
            self.assertEqual((cov.bulk, cov.human, cov.stamped), (1, 1, 2))

    # --- O: the shared row-walk, and the direction that would overstate ------

    def test_comparison_body_rows_excludes_tables_the_gate_does_not_validate(self):
        # Counting every body row here would claim coverage O does not have — the
        # direction that makes a population worse than none. A foreign table (no
        # `Evaluated` column) and the `## Summary` block are scope, not findings.
        text = (self.HEADER + "| t | tool | | ✓ | SKIP | REVIEW |\n\n"
                "## Notes\n| a | b |\n|---|---|\n| one | two |\n\n"
                "## Summary\n| Stage | Tools | Validated |\n|---|---|---|\n| Plan | 1 | 1 |\n")
        self.assertEqual(len(list(catalog_lib.comparison_body_rows(text))), 1)
        self.assertEqual(catalog_lib.validate_comparison_rows(text), [])

    def test_catalog_body_rows_is_the_population_its_validator_walks(self):
        # One definition, two readers (#443): every row the validator can flag must be
        # a row the count includes, or the headline understates its own findings.
        bad = self.CAT + "| [u](https://github.com/o/u) | tool | short |\n"
        walked = [ln for ln, *_ in catalog_lib.catalog_body_rows(bad)]
        flagged = [ln for ln, _ in catalog_lib.validate_catalog_rows(bad)]
        self.assertEqual(len(walked), 2)
        self.assertTrue(set(flagged) <= set(walked), (flagged, walked))


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
            return audit.audit_overlaps(audit.DetectorContext(d), home or d)[:4]

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
            return audit.audit_clusters(audit.DetectorContext(d))[0]

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
            # catalog_lib comes along because the script reads the field from
            # comment-stripped text via the shared stripper (#451).
            for f in ("backfill-lastverified.py", "catalog_lib.py"):
                shutil.copy(os.path.join(ROOT, f), d)
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


class TestStackCount(unittest.TestCase):
    """#502 — STACK.md's own size is derived, from the same call the tiers block uses.

    `~25` was typed when the page held 22 picks and never moved while the list grew to
    30, twelve lines above a generated block printing the true total the whole time. It
    is the third number on that sentence; `reconcile-counts.py` already derived and gated
    the other two."""

    # Two rows for one tool (a pick listed under two stages), one repo shipping two
    # separately-installed picks. Three tools, four rows, two slugs — the three counts
    # that disagreed live.
    STACK = ("# Stack\n\nThe ~25 tools worth installing on every project.\n\n"
             "| [foo](https://github.com/x/foo) | d | `c` | s |\n"
             "| [bar](https://github.com/x/pack) | d | `c` | s |\n"
             "| [baz](https://github.com/x/pack) | d | `c` | s |\n"
             "| [foo](https://github.com/x/foo) | d | `c` | s |\n")

    def test_dedup_is_by_display_text_in_appearance_order(self):
        picks = catalog_lib.distinct_stack_picks(self.STACK)
        self.assertEqual([p.text for p in picks], ["foo", "bar", "baz"])

    def test_a_pack_shipping_several_picks_counts_once_per_pick(self):
        # The unit is what a reader installs, NOT the slug. Deduping by slug answers
        # detectors J/P's question and undercounts an install list — the miscount that
        # let a prior audit clear `~25` as "26 unique GitHub slugs".
        picks = catalog_lib.distinct_stack_picks(self.STACK)
        self.assertEqual(len({p.slug for p in picks}), 2)
        self.assertEqual(len(picks), 3)

    def test_prose_count_rewrites_and_consumes_the_tilde(self):
        out = reconcile.fix_stack_strings(self.STACK, 3)
        self.assertIn("The 3 tools worth installing", out)
        self.assertNotIn("~", out)

    def test_both_phrasings_are_reached(self):
        # STACK.md/README.md say "worth installing"; CLAUDE.md says "to actually install".
        src = "the ~25 tools worth installing, and ~25 tools to actually install"
        self.assertEqual(reconcile.fix_stack_strings(src, 30),
                         "the 30 tools worth installing, and 30 tools to actually install")

    def test_an_unrelated_number_is_never_touched(self):
        # Anchored on the trailing phrase, like every other pattern in the script.
        src = "679 catalog entries, 693 evaluations, 25 tools are cataloged, issue #25"
        self.assertEqual(reconcile.fix_stack_strings(src, 30), src)

    def test_stack_count_reads_the_repo_stack_file(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d, "STACK.md").write_text(self.STACK, encoding="utf-8")
            self.assertEqual(reconcile.stack_count(d), 3)

    def test_live_tree_prose_count_equals_the_generated_tiers_block(self):
        """The invariant the fix buys: the sentence and the block below it are one
        population. Both call `distinct_stack_picks`, so they cannot drift."""
        text = Path(ROOT, "STACK.md").read_text(encoding="utf-8")
        n = reconcile.stack_count(ROOT)
        tiers = [int(x) for x in re.findall(r"\*\*Tier \d — [a-z-]+ \((\d+)\)", text)]
        self.assertEqual(len(tiers), 2, "STACK.md should render exactly two tiers")
        self.assertEqual(sum(tiers), n)
        self.assertIn(f"The {n} tools worth installing", text)

    def test_the_two_consumers_render_the_same_population(self):
        """The "one definition" claim, pinned against the two implementations rather than
        against the committed text — a stale block in STACK.md would satisfy the test
        above while the two calls had silently diverged.

        `amap={}` sends every pick to Tier 2 (no eval -> SOURCE-ONLY); the tier *split* is
        not the subject here, the population is, and it skips building a DetectorContext."""
        text = Path(ROOT, "STACK.md").read_text(encoding="utf-8")
        t1, t2 = tier.stack_tiers(text, {})
        self.assertEqual(len(t1) + len(t2), reconcile.stack_count(ROOT))

    def test_live_tree_no_two_tools_share_a_display_name(self):
        """The one thing to watch about a text key: two distinct tools sharing a display
        name collapse into one and the count silently undercounts. None do today."""
        text = Path(ROOT, "STACK.md").read_text(encoding="utf-8")
        by_text = {}
        for p in catalog_lib.stack_picks(text):
            by_text.setdefault(p.text, set()).add(p.slug)
        collided = {t: s for t, s in by_text.items() if len(s) > 1}
        self.assertEqual(collided, {}, f"display name(s) covering two repos: {collided}")

    def test_live_tree_is_reconciled(self):
        text = Path(ROOT, "STACK.md").read_text(encoding="utf-8")
        self.assertEqual(reconcile.fix_stack_strings(text, reconcile.stack_count(ROOT)), text)


# ----------------------------------------------------------------- HTTP responses are closed (#455)
class TestHttpResponsesAreClosed(unittest.TestCase):
    """An `HTTPError` IS the response object, so the error path holds a socket exactly as
    the success path does. `http_status` uses `with urllib.request.urlopen(...)` and used
    to abandon the error, which is why it went unseen — on a healthy network almost every
    reply is a 200. `check_repo` moved off urllib entirely in #498 (authenticated `gh api`
    via subprocess, which has no such leak class); its own shape is pinned below instead."""

    def setUp(self):
        self._orig = audit.urllib.request.urlopen
        self.addCleanup(lambda: setattr(audit.urllib.request, "urlopen", self._orig))

    def _raise(self, code):
        def fake(req, timeout=None):
            raise urllib.error.HTTPError(req.full_url, code, "e", {}, None)
        audit.urllib.request.urlopen = fake

    def _warnings(self, fn, n=25):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            for i in range(n):
                fn(i)
            gc.collect()
            return [w for w in caught if issubclass(w.category, ResourceWarning)]

    def test_a_rate_limited_burst_leaks_nothing(self):
        # 50 calls used to produce 50 unclosed responses, 1:1 with no slack.
        self._raise(429)
        self.assertEqual(self._warnings(lambda i: audit.http_status(f"https://x/{i}")), [])

    def test_a_404_burst_leaks_nothing(self):
        # The one status that produces a verdict still has a response to close.
        self._raise(404)
        self.assertEqual(self._warnings(lambda i: audit.http_status(f"https://x/{i}")), [])

    def test_closing_did_not_change_a_single_verdict(self):
        for code, expected in ((404, audit.DEAD), (429, "unknown:HTTP 429"),
                               (503, "unknown:HTTP 503")):
            self._raise(code)
            self.assertEqual(audit.http_status("https://x/y"), expected)

    def test_the_two_checkers_share_one_vocabulary(self):
        # #447 gave detector A named constants; C built the same three strings by hand
        # forty lines away. One fact, one implementation (#443's rule).
        src = inspect.getsource(audit.check_repo)
        for copy in ('return "dead"', 'f"unknown:HTTP', 'f"unknown:{type(e)'):
            self.assertNotIn(copy, src, msg=f"check_repo re-builds the tri-state: {copy}")
        self.assertIn("DEAD", src)
        self.assertIn("_unknown(", src)

    def test_moved_stays_detector_Cs_own(self):
        # The one value A has no analogue for, so it is NOT hoisted into the shared set.
        self.assertFalse(hasattr(audit, "MOVED"))
        self.assertIn("moved:", inspect.getsource(audit.check_repo))


# ----------------------------------------------------------------- detector A: install resolver (#301)
class TestLinkRotUnknowns(unittest.TestCase):
    """Pins detector C's could-not-check state (#319), and its transport (#498): a
    live ★25.9K repo (ahujasid/blender-mcp) came back a false 404 under the old
    unauthenticated-HEAD burst, so C now makes the same authenticated `gh api` call
    detector H does. It used to fold every non-404 into 'ok', so GitHub's 429 on the
    burst turned the whole sweep into a silent no-op that still printed "OK — all
    612 links resolve". A clean bill of health and a total blackout must never
    render identically. Network-free: a fake `gh` script on PATH stands in for the
    real binary, so the real subprocess path — including marker parsing — is what
    runs, matching TestArchivedProbe's pattern for detector H's sibling call."""

    CATALOG = (
        "## Plan\n"
        "| Name | Type | One-liner | Problem | Overlaps with |\n"
        "|------|------|-----------|---------|---------------|\n"
        "| [a](https://github.com/x/a) | tool | one | two | none |\n"
        "| [b](https://github.com/x/b) | tool | one | two | none |\n"
    )

    def _fake_gh(self, d, body):
        bindir = os.path.join(d, "bin")
        os.makedirs(bindir, exist_ok=True)
        p = os.path.join(bindir, "gh")
        with open(p, "w", encoding="utf-8") as f:
            f.write("#!/bin/sh\n" + body + "\n")
        os.chmod(p, 0o755)
        return bindir

    def _run(self, gh_body):
        """(stdout+stderr) of a real `--links` run against a 2-row catalog."""
        with tempfile.TemporaryDirectory() as d:
            shutil.copy(os.path.join(ROOT, "audit-evals.py"), os.path.join(d, "audit-evals.py"))
            shutil.copy(os.path.join(ROOT, "catalog_lib.py"), os.path.join(d, "catalog_lib.py"))
            _write(d, "CATALOG.md", self.CATALOG)
            bindir = self._fake_gh(d, gh_body)
            r = subprocess.run([sys.executable, "audit-evals.py", "--links"], cwd=d,
                               capture_output=True, text=True, check=False,
                               env={**os.environ, "PATH": bindir})
            return r.stdout + r.stderr

    def test_rate_limit_is_unknown_not_ok(self):
        # The exact #319 failure, now via an authenticated rate limit on every call.
        out = self._run('echo "gh: API rate limit exceeded (HTTP 429)" >&2; exit 1')
        self.assertIn("0/2 checked", out)
        self.assertIn("INCONCLUSIVE", out)
        self.assertIn("gh exit 1", out)
        self.assertNotIn("OK — all", out, msg="a fully rate-limited sweep must never print an all-clear")

    def test_404_is_still_dead(self):
        # Only a 404 genuinely means "gone" — that verdict must survive the transport change.
        out = self._run('echo "gh: Not Found (HTTP 404)" >&2; exit 1')
        self.assertIn("2/2 checked", out)
        self.assertEqual(out.count("DEAD "), 2)
        self.assertNotIn("INCONCLUSIVE", out)

    def test_server_error_and_timeout_are_unknown(self):
        out = self._run('echo "gh: Internal Server Error (HTTP 500)" >&2; exit 1')
        self.assertNotIn("DEAD ", out)
        self.assertIn("INCONCLUSIVE", out)

    def test_moved_is_detected_from_the_canonical_full_name(self):
        # gh api follows GitHub's redirect for a renamed repo — the response names the
        # new slug directly, so C needs no separate rename probe. Only x/b is renamed;
        # x/a echoes its own slug back to prove the other row is unaffected.
        out = self._run('case "$2" in repos/x/a) echo "x/a" ;; repos/x/b) echo "y/b" ;; esac')
        self.assertIn("MOVED x/b -> y/b", out)
        self.assertNotIn("MOVED x/a", out)

    def test_reporting_says_inconclusive_not_ok(self):
        # End-to-end through main(): the output a maintainer actually reads must not
        # claim success when nothing could be checked.
        out = self._run('echo "gh: API rate limit exceeded (HTTP 429)" >&2; exit 1')
        self.assertIn("INCONCLUSIVE", out, msg=out)
        self.assertIn("0/2 checked", out)
        self.assertNotIn("OK — all", out,
                         msg="a fully rate-limited sweep must never print an all-clear")


class TestArchivedProbe(unittest.TestCase):
    """Pins detector H's could-not-check state (#504) — detector C's #319 defect, still
    live in C's sibling. `check_archived` returned `None` for a 404, a 451, a 429, a
    missing `gh` binary and a malformed payload alike, and `audit_archived` folded every
    one into *not archived*, so a total blackout printed
    `OK — none of 661 catalog repos are archived`."""

    CATALOG = (
        "## Plan\n"
        "| Name | Type | One-liner | Problem | Overlaps with |\n"
        "|------|------|-----------|---------|---------------|\n"
        "| [a](https://github.com/x/a) | tool | one | two | none |\n"
        "| [b](https://github.com/x/b) | tool | one | two | none |\n"
    )

    def _fake_gh(self, d, body):
        """Install a fake `gh` on PATH so the real subprocess path — including the
        marker parsing — is what runs, not a stubbed function."""
        bindir = os.path.join(d, "bin")
        os.makedirs(bindir, exist_ok=True)
        p = os.path.join(bindir, "gh")
        with open(p, "w", encoding="utf-8") as f:
            f.write("#!/bin/sh\n" + body + "\n")
        os.chmod(p, 0o755)
        return bindir

    def _run(self, gh_body=None):
        """(stdout) of a real `--archived` run against a 2-row catalog."""
        with tempfile.TemporaryDirectory() as d:
            shutil.copy(os.path.join(ROOT, "audit-evals.py"), os.path.join(d, "audit-evals.py"))
            shutil.copy(os.path.join(ROOT, "catalog_lib.py"), os.path.join(d, "catalog_lib.py"))
            _write(d, "CATALOG.md", self.CATALOG)
            # No `gh` in PATH at all when gh_body is None — the missing-binary case.
            bindir = self._fake_gh(d, gh_body) if gh_body else os.path.join(d, "emptybin")
            os.makedirs(bindir, exist_ok=True)
            # sys.executable, not "python3": PATH is stripped to the fake-gh dir so
            # the missing-binary case is real, and the interpreter must not need it.
            r = subprocess.run([sys.executable, "audit-evals.py", "--archived"], cwd=d,
                               capture_output=True, text=True, check=False,
                               env={**os.environ, "PATH": bindir})
            return r.stdout + r.stderr

    def test_a_missing_gh_binary_is_unchecked_not_a_clean_sweep(self):
        out = self._run(None)
        self.assertIn("0/2 checked", out)
        self.assertIn("INCONCLUSIVE", out)
        self.assertNotIn("OK — none of", out,
                         msg="a sweep that reached nothing must never print an all-clear")

    def test_a_rate_limit_is_unchecked(self):
        out = self._run('echo "gh: API rate limit exceeded (HTTP 429)" >&2; exit 1')
        self.assertIn("0/2 checked", out)
        self.assertIn("INCONCLUSIVE", out)
        self.assertNotIn("OK — none of", out)

    def test_a_malformed_payload_is_unchecked(self):
        out = self._run('echo "not json"; exit 0')
        self.assertIn("0/2 checked", out)
        self.assertIn("INCONCLUSIVE", out)

    def test_a_404_is_gone_and_counts_as_checked(self):
        # A definitive answer about the repo: not archived, and detector C reports DEAD.
        out = self._run('echo "gh: Not Found (HTTP 404)" >&2; exit 1')
        self.assertIn("2/2 checked", out)
        self.assertIn("GONE x/a — 404 not found", out)
        self.assertNotIn("INCONCLUSIVE", out)

    def test_a_451_block_is_gone_not_unchecked(self):
        # vkhanhqui/figma-mcp-go is permanently DMCA-blocked; treating it as unchecked
        # would park the detector at INCONCLUSIVE forever over one entry.
        out = self._run('echo "gh: Repository access blocked (HTTP 451)" >&2; exit 1')
        self.assertIn("2/2 checked", out)
        self.assertIn("451 access blocked", out)
        self.assertNotIn("INCONCLUSIVE", out)

    def test_a_live_repo_renders_the_all_clear_with_its_population(self):
        out = self._run('echo "[false, \\"2026-08\\"]"')
        self.assertIn("2/2 checked", out)
        self.assertIn("OK — none of 2 catalog repos are archived", out)

    def test_an_archived_repo_is_reported_with_the_population(self):
        out = self._run('echo "[true, \\"2025-01\\"]"')
        self.assertIn("2 archived (2 undisclosed), 2/2 checked", out)
        self.assertIn("ARCHIVED x/a", out)

    def test_the_headline_states_a_population(self):
        """#481/#494's rule, unmet in one of the three flags TestDetectorPopulations
        excludes by construction — so that sweep structurally could not see it."""
        out = self._run('echo "[false, \\"2026-08\\"]"')
        headline = next(ln for ln in out.splitlines() if ln.startswith("== H."))
        self.assertRegex(headline, r"\d+/\d+ checked")


class TestSweepWorkflow(unittest.TestCase):
    """The weekly sweep decides whether to open a tracking issue by grepping the
    detectors' prose. That is #443's two-extractors shape — a bash pattern coupled to
    Python output by nothing — and it had already rotted: C's INCONCLUSIVE line did not
    match, so a 160-link hole reported as a clean bill of health (#504).

    These pins read the workflow's real regex and test it against the detectors' real
    emitted lines, in both directions."""

    WF = os.path.join(ROOT, ".github", "workflows", "link-archive-sweep.yml")

    @classmethod
    def setUpClass(cls):
        cls.text = Path(cls.WF).read_text(encoding="utf-8")
        m = re.search(r"if grep -qE '([^']+)' sweep\.txt", cls.text)
        assert m, "the sweep's findings regex moved — update this test with it"
        # `grep -E` and Python's `re` agree on this subset; anchors are per-line.
        cls.pattern = re.compile(m.group(1), re.MULTILINE)

    def _matches(self, line):
        return bool(self.pattern.search(line))

    def test_actionable_detector_lines_match(self):
        for line in [
            "  DEAD 0xwilliamortiz/agents-council",
            "  MOVED old/name -> new/name",
            "  GONE x/a — 404 not found; not archived, and the entry still lists it",
            "  ARCHIVED foo/bar (last push 2025-01)  <- NOT disclosed in the entry; "
            "add a ⚠️ archived note or repoint",
            "  INCONCLUSIVE — 160 link(s) could not be verified (160x HTTP 429).",
            "  INCONCLUSIVE — 2 repo(s) could not be checked (2x gh not installed).",
        ]:
            self.assertTrue(self._matches(line), msg=f"must be actionable: {line!r}")

    def test_a_clean_run_is_not_actionable(self):
        for line in [
            "== C. link rot (CATALOG.md repo links) — 659/659 checked ==",
            "  OK — all 659 catalog repo links resolve to their canonical names",
            "== H. archived repos (report-only) — 5 archived (0 undisclosed), 661/661 checked ==",
            "  ARCHIVED AntonOsika/gpt-engineer (last push 2025-05)",
            "  (5 archived, all already disclosed with a ⚠️ note)",
            "  OK — none of 661 catalog repos are archived",
        ]:
            self.assertFalse(self._matches(line), msg=f"must not be actionable: {line!r}")

    def test_an_incomplete_sweep_is_not_read_as_clean(self):
        """`|| true` means a crash lands as a traceback that matches nothing, which used
        to render identically to a clean run."""
        self.assertIn("did not run to completion", self.text)
        self.assertRegex(self.text, r"grep -q '\^== C\\\.'")
        self.assertRegex(self.text, r"grep -q '\^== H\\\.'")

    def test_the_token_comment_reflects_C_now_authenticated(self):
        """#498 moved detector C onto authenticated `gh api` (the same call H already
        makes), after an unauthenticated HEAD burst returned a false DEAD for a live
        ★25.9K repo (ahujasid/blender-mcp). The workflow comment must track the
        transport it actually uses, not the stale claim #504 fixed in the other
        direction."""
        env_comment = self.text.split("GH_TOKEN:")[0].split("env:")[-1]
        self.assertNotIn("Detector C does NOT", env_comment)
        self.assertIn("#498", env_comment)

    def test_detector_c_now_uses_authenticated_gh_api(self):
        """The premise of the comment above (#498). If C ever moves off `gh api`, the
        comment and the INCONCLUSIVE handling both need revisiting again — fail here
        rather than let the workflow quietly describe a transport it no longer uses."""
        src = inspect.getsource(audit.check_repo)
        self.assertIn('"gh", "api"', src)
        self.assertIn("subprocess.run", src)
        self.assertNotIn("urllib.request.urlopen", src)


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

    def test_missing_binary_is_unchecked_not_broken_and_not_ok(self):
        # A checker that cannot run at all ("npm isn't installed") must resolve to
        # "cannot verify". Both wrong answers are live regressions: BROKEN fails the
        # build for a reason no commit caused, and OK — which is what this returned
        # until #447 — counted 57 of 85 targets as resolved without reaching any of
        # them. Before #301 it raised FileNotFoundError and took the run down.
        r = audit._run_status(["definitely-not-a-real-binary-ai-tooling"])
        self.assertTrue(r.startswith("unknown:"), msg=r)
        self.assertNotIn(r, (audit.OK, audit.DEAD))

    def test_a_cli_probe_separates_404_from_any_other_failure(self):
        # `npm view` and `gh api` exit non-zero for a missing package AND for a 5xx, a
        # rate limit or an auth wall, so the exit code alone cannot classify. The 404
        # marker in the output is what distinguishes gone from unreachable.
        self.assertEqual(audit._run_status(["bash", "-c", "exit 0"]), audit.OK)
        self.assertEqual(audit._run_status(["bash", "-c", "echo 'npm error code E404' >&2; exit 1"]),
                         audit.DEAD)
        self.assertEqual(audit._run_status(["bash", "-c", "echo 'gh: Not Found (HTTP 404)' >&2; exit 1"]),
                         audit.DEAD)
        rate = audit._run_status(["bash", "-c", "echo 'API rate limit exceeded' >&2; exit 1"])
        self.assertTrue(rate.startswith("unknown:"), msg=rate)

    def test_reports_every_occurrence(self):
        # Lookups dedupe; FINDINGS do not. One broken package cited in two files is two
        # findings, one per mention. The concurrent rewrite resolves unique targets, so
        # this is the property most at risk of silently collapsing to a single finding.
        audit.pypi_exists = lambda pkg: audit.DEAD
        with tempfile.TemporaryDirectory() as d:
            broken, unknown, targets = audit.audit_installs(self._ctx(d, "STACK.md", "CATALOG.md"))
        self.assertEqual(broken, [("STACK.md", "pypi", self.PKG),
                                  ("CATALOG.md", "pypi", self.PKG)])
        self.assertEqual((unknown, targets), ([], 1))

    def test_an_unreachable_registry_is_unknown_not_broken(self):
        # The #447 regression: a rate-limited crates.io failed the whole `make check`
        # on a PR that touched no eval, and re-running the identical tree passed.
        audit.pypi_exists = lambda pkg: "unknown:HTTP 429"
        with tempfile.TemporaryDirectory() as d:
            broken, unknown, targets = audit.audit_installs(self._ctx(d, "STACK.md"))
        self.assertEqual(broken, [])
        self.assertEqual(unknown, [("STACK.md", "pypi", self.PKG, "HTTP 429")])
        self.assertEqual(targets, 1)

    def test_resolves_each_unique_target_once(self):
        # The whole point of the `seen` dedupe: two mentions, one network round trip.
        calls = []
        audit.pypi_exists = lambda pkg: calls.append(pkg) or audit.DEAD
        with tempfile.TemporaryDirectory() as d:
            audit.audit_installs(self._ctx(d, "STACK.md", "CATALOG.md"))
        self.assertEqual(calls, [self.PKG])

    def test_ok_target_is_not_reported(self):
        audit.pypi_exists = lambda pkg: audit.OK
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(audit.audit_installs(self._ctx(d, "STACK.md", "CATALOG.md")),
                             ([], [], 1))

    def test_http_status_calls_only_a_404_dead(self):
        # Detector C's rule (#319), which this detector never learned: only a 404 means
        # gone. The old http_ok folded every one of these into False -> BROKEN.
        class _Resp:
            status = 200
            def __enter__(self): return self
            def __exit__(self, *a): return False
        with mock.patch("urllib.request.urlopen", return_value=_Resp()):
            self.assertEqual(audit.http_status("https://x/y"), audit.OK)
        for code, want in ((404, audit.DEAD), (429, "unknown:HTTP 429"), (503, "unknown:HTTP 503")):
            # HTTPError is file-like; closing it keeps this from adding to the
            # ResourceWarning noise ruff cleared out of every gate run (#388).
            with contextlib.closing(urllib.error.HTTPError("https://x/y", code, "e", {}, None)) as err, \
                 mock.patch("urllib.request.urlopen", side_effect=err):
                self.assertEqual(audit.http_status("https://x/y"), want)
        with mock.patch("urllib.request.urlopen", side_effect=TimeoutError()):
            self.assertEqual(audit.http_status("https://x/y"), "unknown:TimeoutError")

    def _cli(self, d, fake):
        """`audit-evals.py --installs` in a fixture tree, with pypi_exists replaced.

        A subprocess because the exit code IS the gate — asserting on the return value
        of audit_installs would not have caught #447, whose whole defect was in what the
        CLI did with it."""
        self._ctx(d, "STACK.md")
        return subprocess.run(
            [sys.executable, "-c",
             "import importlib.util,sys;"
             "spec=importlib.util.spec_from_file_location('ae',sys.argv[1]);"
             "ae=importlib.util.module_from_spec(spec);spec.loader.exec_module(ae);"
             # ae.ROOT is where main() builds its DetectorContext, so this is what
             # isolates the run from the real tree; every checker is faked so the
             # test never touches the network.
             f"ae.ROOT=sys.argv[2];ae.pypi_exists=ae.crates_exists=ae.npm_exists="
             f"ae.gh_repo_exists=lambda p:{fake};"
             "sys.argv=['audit-evals.py','--installs'];sys.exit(ae.main())",
             os.path.join(ROOT, "audit-evals.py"), d],
            cwd=d, capture_output=True, text=True, check=False,
            env=dict(os.environ, PYTHONPATH=ROOT))

    def test_an_unchecked_target_never_prints_ok_and_never_fails_the_build(self):
        # Both halves matter and they pull opposite ways. Not a build failure: nothing a
        # commit did caused it, and re-running gives a different answer. Not OK either:
        # "could not check" and "checked and fine" must not be the same value (#319).
        with tempfile.TemporaryDirectory() as d:
            r = self._cli(d, "'unknown:HTTP 429'")
        self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)
        self.assertIn("UNCHECKED", r.stdout)
        self.assertIn("INCONCLUSIVE", r.stdout)
        self.assertIn("0/1 target(s) checked", r.stdout)
        self.assertNotIn("OK —", r.stdout)

    def test_a_dead_target_still_fails_the_build(self):
        # The gate is not weakened: a 404 install command is a defect a commit caused,
        # and #416's reason stands — STACK.md is the page whose purpose is to be executed.
        with tempfile.TemporaryDirectory() as d:
            r = self._cli(d, "ae.DEAD")
        self.assertEqual(r.returncode, 1, msg=r.stdout + r.stderr)
        self.assertIn("BROKEN", r.stdout)


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
        # Offline and deterministic, so it gates from day one rather than after a
        # report-only tenure: a dead relative link is bookkeeping, not judgement (#437).
        "check-links.py --check",
        # The published package: the README's own install commands were both invented and
        # `claude plugin validate ./plugin` failed on a missing manifest (#439).
        "check-plugin.py --check",
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

    # `check-data` (#459) — the offline data gates alone: GATES minus the two linters
    # (they need the pinned dev venv, and a contributor without it must not be blocked
    # from committing), minus the unit suite (it tests the *scripts*, not the tree, and
    # costs 15.9s), minus the network resolver. It is what both commit hooks run, so
    # this tuple is the thing that keeps the hooks from drifting behind CI again.
    DATA_GATES = tuple(g for g in GATES if g not in (
        "$(RUFF) check",
        "$(MYPY)",
        "python3 -m unittest -q test_automation",
        "audit-evals.py --installs",
    ))

    # Both halves of the commit gate, held in lockstep (the same pair TestHookTriggerSeam
    # pins the commit predicate across).
    COMMIT_HOOKS = (".claude/hooks/audit-gate.sh", ".opencode/plugins/commit-gate.ts")

    # The gates whose `--check` has NO apply-mode counterpart, each with the reason it
    # cannot have one. DECLARED here, and deliberately never counted: the prose used to
    # state an *ordinal* for this set — "the only", "the second", "the second" — in three
    # places, three different answers, none of them right, with nothing that could check
    # any of them (#461). A set with reasons is checkable; an ordinal in prose is not.
    NO_APPLY_MODE = (
        ("audit-evals.py", "a detector reports; there is nothing to regenerate"),
        ("check-stars.py", "a missing **Stars:** value cannot be generated, only declared"),
        ("check-links.py", "a dead link can be repointed or its file restored — only an author knows which"),
        ("check-plugin.py", "the manifests and the plugin front door are hand-authored"),
        ("verify-installs.py", "the apply side (--record) reads ONE laptop's records (ADR-0006)"),
    )

    # The sentence both prose copies of the repair chain open with. Anchoring on it (not
    # on "the longest arrow-chain in the file") keeps the extractor from wandering onto
    # one of the four other `a → b` chains in CLAUDE.md.
    FIX_CHAIN_ANCHOR = "apply-mode fixers in dependency order"

    # Where the chain is restated outside the Makefile. Both are facts copied from the
    # recipe, so both get a test — `reconcile-counts.py` and TestPluginFrontDoorSignals
    # are the precedent for gating a restated fact rather than the file restating it.
    CHAIN_PROSE = ("CLAUDE.md", "opencode.json")

    def _raw_target_body(self, target):
        """The literal recipe lines of `target:`, delegation unexpanded. Prefix-safe —
        `check-offline:` does not start with `check:`, so the two targets never capture
        each other's bodies."""
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

    def _target_body(self, target="check", _seen=None):
        """The recipe lines of `target:`, with `$(MAKE) <other>` delegation expanded in
        place. `check` and `check-offline` both delegate their thirteen data gates to
        `check-data` (#459), so a gate-set assertion must follow the delegation or it
        would read a shared list as a dropped one. Cycle-guarded."""
        _seen = set() if _seen is None else _seen
        if target in _seen:
            return []
        _seen.add(target)
        out = []
        for line in self._raw_target_body(target):
            m = re.match(r"^[-@]*\$\(MAKE\)\s+(?:--\S+\s+)*(\S+)$", line)
            if m:
                out.extend(self._target_body(m.group(1), _seen))
            else:
                out.append(line)
        return out

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

    def test_check_data_is_the_offline_gates_minus_lint_and_the_unit_suite(self):
        # `check-data` is the ONE definition of the set both commit hooks run (#459).
        # Pinned in both directions: every offline gate must be in it, and the four
        # deliberate exclusions must stay out — each for a stated reason. Adding the unit
        # suite would put 15.9s on every commit; adding ruff/mypy would block a
        # contributor without the pinned dev venv; adding --installs would put the
        # network on the commit path.
        body = "\n".join(self._raw_target_body("check-data"))
        self.assertTrue(body, "Makefile has no `check-data:` target body")
        for gate in self.DATA_GATES:
            self.assertIn(gate, body, msg=f"`make check-data` is missing gate: {gate}")
        for excluded in ("$(RUFF)", "$(MYPY)", "unittest", "--installs"):
            self.assertNotIn(excluded, body,
                             msg=f"`make check-data` must not run {excluded}")

    def test_both_commit_hooks_run_the_shared_target(self):
        # The hooks ran `audit-evals.py --offline` alone — 1 of the 13 gates — while both
        # described themselves as running "the offline subset of `make check`" (#459).
        # Nothing coupled their list to the Makefile's, so every gate added since #153
        # widened the hole in silence. They delegate now, which is the rule CLAUDE.md
        # already states for every other hook here: one implementation.
        for rel in self.COMMIT_HOOKS:
            text = Path(ROOT, rel).read_text(encoding="utf-8")
            self.assertIn("check-data", text,
                          msg=f"{rel} must run the shared `make check-data` target")
            # Read the CODE, not the comments: both files narrate the gate they used to
            # run, and a header explaining the history is not a header re-running it —
            # detector AC's rule that a comment carries provenance, not the claim (#451).
            code = "\n".join(l for l in text.splitlines()
                             if not l.lstrip().startswith(("#", "//")))
            self.assertNotIn("audit-evals.py --offline", code,
                             msg=f"{rel} must not keep a private gate list — delegate")

    def test_both_commit_hooks_fail_open_when_the_gate_cannot_run(self):
        # "Could not run" is not "failed" (detector C's rule, #319, applied to the hooks).
        # A missing toolchain must let the commit through, and `make` cannot signal that
        # through its exit code — it exits non-zero for an absent target and for a real
        # finding alike — so both hooks decide it BEFORE the run, by probing the same
        # three preconditions. Without this the delegation would turn a machine without
        # `make` into one that can never commit.
        for rel in self.COMMIT_HOOKS:
            text = Path(ROOT, rel).read_text(encoding="utf-8")
            self.assertIn("command -v make", text,
                          msg=f"{rel} must probe for make before blocking on it")
            self.assertIn("command -v python3", text,
                          msg=f"{rel} must probe for python3 before blocking on it")
            self.assertIn("^check-data:", text,
                          msg=f"{rel} must probe that the target exists before running it")

    # ---- the repair chain (#461)
    @staticmethod
    def _gate_script(line):
        """The script a `check-data` recipe line invokes, or None."""
        m = re.match(r"^(?:python3\s+|\./)([\w.-]+\.(?:py|sh))\s+--", line)
        return m.group(1) if m else None

    def _fix_chain(self):
        """The fixers `make fix` runs, in order, named as the prose names them."""
        names = []
        for line in self._raw_target_body("fix"):
            if line.startswith("@$(MAKE)"):
                continue  # the trailing re-verify, not a fixer
            if line == "$(RUFF) check --fix":
                names.append("ruff --fix")
                continue
            m = re.match(r"^(?:python3\s+|\./)([\w.-]+)\.(?:py|sh)$", line)
            self.assertIsNotNone(m, msg=f"unrecognized `fix:` recipe line: {line}")
            names.append(m.group(1))
        return names

    def _prose_chain(self, rel):
        """The `a` → `b` → `c` chain a doc states for `make fix`, after the anchor."""
        text = Path(ROOT, rel).read_text(encoding="utf-8")
        at = text.find(self.FIX_CHAIN_ANCHOR)
        self.assertNotEqual(at, -1, msg=f"{rel} no longer states the repair chain")
        m = re.search(r"(?:`[^`]+`\s*(?:→|\\u2192)\s*)+`[^`]+`", text[at:])
        self.assertIsNotNone(m, msg=f"{rel} names no fixer chain after the anchor")
        return re.findall(r"`([^`]+)`", m.group(0))

    def test_every_gate_has_a_fixer_or_a_declared_reason(self):
        # `make check`'s gate set is pinned in both directions; the repair chain was
        # pinned in NO direction, and deleting backfill-evidence, triage and watchlist
        # from `fix:` left all 581 tests green (#461). Derived from the Makefile rather
        # than hand-listed, so adding a gate forces an explicit decision instead of
        # silently landing in neither the chain nor the declared exemptions.
        fix_lines = set(self._raw_target_body("fix"))
        exempt = dict(self.NO_APPLY_MODE)
        seen = set()
        for line in self._raw_target_body("check-data"):
            script = self._gate_script(line)
            self.assertIsNotNone(script, msg=f"unrecognized `check-data` line: {line}")
            seen.add(script)
            apply_form = ("python3 " if script.endswith(".py") else "./") + script
            if script in exempt:
                self.assertTrue(exempt[script].strip(),
                                msg=f"{script} is exempt with no reason given")
                self.assertNotIn(apply_form, fix_lines,
                                 msg=f"{script} runs in `fix` but is declared exempt — "
                                     f"drop it from NO_APPLY_MODE")
            else:
                self.assertIn(apply_form, fix_lines,
                              msg=f"`{apply_form}` gates in check-data but never runs in "
                                  f"`make fix` — wire it in, or declare why it cannot be")
        stale = set(exempt) - seen
        self.assertFalse(stale, msg=f"NO_APPLY_MODE names gates check-data no longer runs: {stale}")

    def test_every_fixer_answers_a_gate(self):
        # The reverse direction: a fixer whose gate was dropped regenerates a page nothing
        # verifies. `ruff --fix` is the one exception — the linter gates from `check`
        # directly, since it needs the dev venv `check-data` deliberately does not.
        gates = {self._gate_script(l) for l in self._raw_target_body("check-data")}
        for name in self._fix_chain():
            if name == "ruff --fix":
                continue
            self.assertTrue(any(g and g.startswith(name + ".") for g in gates),
                            msg=f"`make fix` runs {name} but nothing in check-data gates it")

    def test_the_prose_chains_match_the_recipe(self):
        # CLAUDE.md and the opencode `/fix` template each restate the chain, and both said
        # four of its eight steps (#461) — omitting `ruff --fix`, whose POSITION is a
        # documented invariant with its own test. The `/fix` one is prose fed to a model
        # and ends "Report which fixers applied", so a four-item chain meant `/fix` could
        # regenerate NEXT-EVALS.md and correctly report that it had not.
        recipe = self._fix_chain()
        for rel in self.CHAIN_PROSE:
            self.assertEqual(self._prose_chain(rel), recipe,
                             msg=f"{rel} states a repair chain that is not `make fix`'s")

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
            miss, picks = audit.audit_workflow_drift(self._ctx(d, stack, workflow))
            self.assertEqual(miss, [("own/b", 5)])  # slug + first STACK line
            self.assertEqual(picks, 2)              # the POPULATION, not the findings

    def test_all_picks_present_is_empty(self):
        stack = ("| Tool | What | Install | Signal |\n|---|---|---|---|\n"
                 "| [a](https://github.com/own/a) | x | `pip install a` | Correctness |\n")
        workflow = "the manual mentions [a](https://github.com/own/a) here\n"
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(audit.audit_workflow_drift(self._ctx(d, stack, workflow))[0], [])

    def test_excluded_prose_slug_is_not_a_pick(self):
        # A github slug named only in STACK prose (an *excluded* tool) is not a pick
        # and must not be flagged, even though it's absent from WORKFLOW.
        stack = ("| Tool | What | Install | Signal |\n|---|---|---|---|\n"
                 "| [a](https://github.com/own/a) | x | `pip install a` | Correctness |\n\n"
                 "- **excluded batch** — [b](https://github.com/own/b) didn't meet the bar.\n")
        workflow = "[a](https://github.com/own/a)\n"
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(audit.audit_workflow_drift(self._ctx(d, stack, workflow))[0], [])

    def test_slug_match_is_case_insensitive(self):
        # GitHub slugs are case-insensitive: STACK links Own/Repo, WORKFLOW own/repo.
        stack = ("| Tool | What | Install | Signal |\n|---|---|---|---|\n"
                 "| [a](https://github.com/Own/Repo) | x | `pip install a` | Correctness |\n")
        workflow = "[a](https://github.com/own/repo)\n"
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(audit.audit_workflow_drift(self._ctx(d, stack, workflow))[0], [])


    # --- one definition of a pick, shared with detector J and tier-stack (#469) ---

    def test_a_link_mid_cell_is_a_mention_not_a_pick(self):
        # STACK.md:117 reads `[GSD](…) planning + [graphify](…) views | … graphify is not
        # in STACK — evaluations/ only`. Reading any github link on any |-line counted it,
        # so P was one WORKFLOW.md edit away from demanding the manual document a tool
        # STACK disclaims — flagging a healthy row, the expensive direction (V's rule).
        stack = ("| Tool | What | Install | Signal |\n|---|---|---|---|\n"
                 "| [a](https://github.com/own/a) plus [b](https://github.com/own/b) "
                 "views | x | `pip install a` | b is not in STACK |\n")
        with tempfile.TemporaryDirectory() as d:
            miss, picks = audit.audit_workflow_drift(self._ctx(d, stack, "nothing here\n"))
            self.assertEqual(picks, 1)
            self.assertEqual(miss, [("own/a", 3)])

    def test_the_population_is_reported_even_when_nothing_is_missing(self):
        # CLAUDE.md describes P as "prints a count so it's a number to shrink"; the count
        # it printed was the FINDINGS. `0 of 0` and `0 of 24` are different reports and
        # only one of them is a pass — #467's rule, in the detector that stated it.
        stack = ("| Tool | What | Install | Signal |\n|---|---|---|---|\n"
                 "| [a](https://github.com/own/a) | x | `pip install a` | Correctness |\n")
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(
                audit.audit_workflow_drift(self._ctx(d, stack, "[a](https://github.com/own/a)"))[1], 1)
            self.assertEqual(
                audit.audit_workflow_drift(self._ctx(d, "no table here\n", ""))[1], 0)

    def test_every_consumer_reads_one_definition(self):
        # Five implementations, three of them the same regex written out again. A cell
        # rewritten `| Use [GSD](…)` used to drop obra/superpowers from J's gating SKIP
        # check and from triage.py's P2 band — 9 leads moved to P3, a band an unattended
        # pass may NOT SKIP from — while P still counted it.
        stack = ("| Tool | What | Install | Signal |\n|---|---|---|---|\n"
                 "| [a](https://github.com/own/a) | x | `pip install a` | Correctness |\n"
                 "| [b](https://github.com/own/b) | y | `pip install b` | Speed |\n")
        picks = catalog_lib.stack_picks(stack)
        self.assertEqual([p.slug for p in picks], ["own/a", "own/b"])
        # detector J's helper and tier-stack's renderer are the same list
        self.assertEqual(audit._stack_picks_by_slug(stack), picks)
        t1, t2 = tier.stack_tiers(stack, {})
        self.assertEqual([t for t, _e in [*t1, *t2]], ["a", "b"])
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(
                audit.audit_workflow_drift(self._ctx(d, stack, ""))[1], len(picks))

    def test_live_tree_pick_populations_agree_and_are_not_empty(self):
        # The property that, had it existed, would have caught the divergence: P counted
        # 25 slugs and J counted 24. A `for` loop over an empty pick list also passes
        # every existing assertion, so the floor is pinned here too.
        ctx = audit.DetectorContext(ROOT)
        picks = catalog_lib.stack_picks(ctx.stack)
        self.assertGreater(len(picks), 20, "STACK.md picks stopped parsing")
        self.assertEqual(audit.audit_workflow_drift(ctx)[1],
                         len({p.slug for p in picks}))

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

    def test_a_basename_collision_lends_no_pressure(self):
        # #413, the score half of #374. `vendor/widget` must NOT collect the citations
        # of the distinct row its basename spells — a basename is not a synonym between
        # two rows that each name a tool. Fanned out through alias_keys this scored +22
        # apiece and put two leads nothing points at into P0, the band reserved for
        # human attention.
        catalog = (
            "## Plan\n"
            "| Name | Type | One-liner | Problem | Overlaps with |\n"
            "|------|------|-----------|---------|---------------|\n"
            "| [widget](https://github.com/addy/widget) | tool | one | two | none |\n"
            "| [vendor/widget](https://github.com/vendor/widget) | tool | one | two | none |\n"
            "| [c1](https://github.com/x/c1) | tool | one | two | widget |\n"
            "| [c2](https://github.com/x/c2) | tool | one | two | widget |\n"
        )
        comparison = (
            "# Tool Comparison\n\n## Plan\n\n"
            "| Tool | Type | Auto | Free | Evaluated | Evidence |\n"
            "|------|------|------|------|-----------|----------|\n"
            "| widget | tool | | ✓ | ADOPT | MEASURED |\n"
            "| vendor/widget | tool | | ✓ | discovery-log | SOURCE-ONLY |\n"
            "| c1 | tool | | ✓ | discovery-log | SOURCE-ONLY |\n"
            "| c2 | tool | | ✓ | discovery-log | SOURCE-ONLY |\n"
        )
        with tempfile.TemporaryDirectory() as d:
            ranked = nexteval.rank(self._ctx(d, catalog, comparison))
            vendor = next(r for r in ranked if r[1] == "vendor/widget")
            self.assertEqual(vendor[3], 0,
                             "a slash-name must not collect its basename's citations")
            # and gains nothing over the uncited leads it sits beside
            self.assertEqual({r[0] for r in ranked}, {vendor[0]})

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
        ordered, ranked, _incumbents, _containers = triage.assign(ctx)
        return {b: [r[1] for r in rows] for b, rows in ordered.items()}, ranked

    # ---------------------------------------------------- P2 names its incumbent (#457)
    def test_the_incumbent_is_carried_forward_not_re_derived(self):
        # The band's disposition is `SKIP "redundant with <incumbent>"` and the page
        # never said who; the match was computed and thrown away (#457).
        skeys = triage.stack_keys(
            "| [GSD](https://github.com/obra/superpowers) | x | y | z |\n")
        self.assertEqual(triage.stack_incumbents("superpowers, ECC", skeys), ["GSD"])

    def test_the_token_is_not_the_pick_name(self):
        # `superpowers` is the REPO; the pick is named GSD — detector P's rule, and the
        # reason an agent copying the citation token writes the wrong name.
        skeys = triage.stack_keys(
            "| [GSD](https://github.com/obra/superpowers) | x | y | z |\n")
        self.assertNotIn("superpowers", triage.stack_incumbents("superpowers", skeys))

    def test_every_matched_pick_is_named_never_one_of_them(self):
        # One key can reach three picks that do three different jobs; choosing inside a
        # generator is the coin flip this exists to prevent.
        stack = ("| [code-review](https://github.com/anthropics/claude-plugins-official) | | | |\n"
                 "| [feature-dev](https://github.com/anthropics/claude-plugins-official) | | | |\n"
                 "| [stryker-js](https://github.com/stryker-mutator/stryker-js) | | | |\n")
        skeys = triage.stack_keys(stack)
        self.assertEqual(triage.stack_incumbents("claude-plugins-official, stryker-js", skeys),
                         ["code-review", "feature-dev", "stryker-js"])

    def test_no_lead_changes_band(self):
        # Membership is still "cites at least one pick"; only the answer is kept.
        skeys = triage.stack_keys(
            "| [GSD](https://github.com/obra/superpowers) | x | y | z |\n")
        self.assertEqual(triage.stack_incumbents("nothing, unrelated", skeys), [])
        self.assertTrue(triage.stack_incumbents("superpowers", skeys))

    def test_only_P2_rows_name_an_incumbent(self):
        # A band whose disposition holds no placeholder keeps the score terms in its Why
        # cell. P3 is such a band; P5 is NOT, which is what this test's own premise —
        # "the other bands' dispositions contain no placeholder" — got wrong (#477).
        ranked = [(2.0, "a", "Plan", 3, 1.0)]
        ordered = {name: [] for name, _, _ in triage.BANDS}
        ordered["P2 challenger"] = ranked
        out = triage.render(ordered, ranked, {"a": ["GSD"]})
        self.assertIn("challenges GSD · pressure 3, gap 1.0", out)
        ordered = {name: [] for name, _, _ in triage.BANDS}
        ordered["P3 backlog"] = ranked
        out = triage.render(ordered, ranked, {"a": ["GSD"]})
        self.assertNotIn("challenges", out)

    # ------------------------------------------------ P5 names its container (#477)
    def test_P5_rows_name_the_container_the_disposition_asks_for(self):
        # P5's disposition reads `SKIP "ships inside <container>"`; band_of read the cell
        # to assign the band and dropped it, so the row printed the score terms and an
        # agent went back to CATALOG.md for the one fact the verdict needs — #457's
        # defect in the band that landed after the fix.
        ranked = [(2.0, "a", "Plan", 3, 1.0)]
        ordered = {name: [] for name, _, _ in triage.BANDS}
        ordered["P5 ships-inside"] = ranked
        out = triage.render(ordered, ranked, {}, {"a": "mattpocock/skills"})
        self.assertIn("ships inside `mattpocock/skills` · pressure 3, gap 1.0", out)

    def test_the_container_is_not_offered_to_other_bands(self):
        # A P3 lead has no container to name; leaking one would assert containment the
        # row never declared. Asserted on the ROW, not the document — the band-summary
        # table quotes P5's disposition verbatim, so the phrase is always on the page.
        ranked = [(2.0, "a", "Plan", 3, 1.0)]
        ordered = {name: [] for name, _, _ in triage.BANDS}
        ordered["P3 backlog"] = ranked
        out = triage.render(ordered, ranked, {}, {"a": "mattpocock/skills"})
        row = next(ln for ln in out.splitlines() if ln.startswith("| a |"))
        self.assertEqual(row, "| a | Plan | 2.0 | pressure 3, gap 1.0 | `/triage-lead a` |")

    def test_the_container_comes_from_the_cell_that_banded_the_lead(self):
        # Backticks are stripped (the catalog writes the cell as code) and the value is
        # the declared slug — never the row's own name, which is the #343/#366 error.
        facts = {"a": triage.CatalogFacts("skill", "o/r", "", "`mattpocock/skills`")}
        self.assertEqual(triage.container_of("a", facts), "mattpocock/skills")
        self.assertEqual(triage.container_of("absent", facts), "")

    def test_assign_returns_the_container_for_every_P5_lead(self):
        with tempfile.TemporaryDirectory() as d:
            self._contained_tree(d)
            tr = _load("triage_fixture", os.path.join(d, "triage.py"))
            ordered, _ranked, _inc, containers = tr.assign(audit.DetectorContext(d))
            p5 = [r[1] for r in ordered["P5 ships-inside"]]
            self.assertEqual(p5, ["badskill"], msg="fixture no longer exercises P5")
            self.assertEqual(containers["badskill"], "x/pack")
            # The annotation is scoped to the band that asks for it.
            self.assertNotIn("plainlead", containers)

    def test_one_stack_parser_not_two(self):
        # The map and the key set must come from the same parse, or the queue and
        # detector J could disagree about what is "in STACK".
        stack = "| [GSD](https://github.com/obra/superpowers) | x | y | z |\n"
        self.assertEqual(set(audit._stack_member_key_map(stack)),
                         audit._stack_member_keys(stack))

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
        out = triage.render(ordered, ranked, {})
        self.assertIn("only 2 distinct values across these 3 leads", out)
        self.assertIn("2 have zero overlap pressure", out)
        self.assertIn("largest tie: 2", out)

    def test_render_survives_an_empty_queue(self):
        # max() over no scores would raise; an exhausted queue must still render.
        out = triage.render({name: [] for name, _, _ in triage.BANDS}, [], {})
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
            return audit.audit_lead_headlines(audit.DetectorContext(d))[0]

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
            by_tool = {tool: trig for tool, _stage, trig, _ev in rows}
            self.assertEqual(by_tool["blocked"], "the API stabilizes")
            self.assertEqual(by_tool["orphan"], watchlist._NO_TRIGGER)
            self.assertEqual(missing, 1)
            # stage travels with the row so section 1 can show it
            self.assertEqual({stage for _t, stage, _tr, _ev in rows}, {"Plan"})
            # a COMPARISON-sourced row carries no Evaluation — that marker is what
            # distinguishes it from an eval-only DEFER when rendering (#416)
            self.assertTrue(all(ev is None for *_x, ev in rows))

    # --- #416: the section is sourced from DEFER verdicts, not DEFER rows ---

    TRIGGER_PHRASINGS = (
        ("re-evaluate after the API stabilizes.", "the API stabilizes"),
        ("re-evaluate when the license clears.", "the license clears"),
        ("Revisit once a free tier exists.", "a free tier exists"),
        ("It becomes a clear ADOPT only if your goal shifts to app-building.",
         "your goal shifts to app-building"),
        ("Track it and adopt once a turnkey path exists.", "a turnkey path exists"),
    )

    def test_trigger_vocabulary_recovers_each_phrasing(self):
        # The single `re-evaluate (after|when)` pattern this replaces recovered 2 of the
        # tree's 4 triggers and printed "trigger not recorded — add one" beside two evals
        # that stated theirs plainly. Widening can only remove a false action item.
        for sentence, expected in self.TRIGGER_PHRASINGS:
            ev = audit.Evaluation("x", f"# x\n\n## Verdict\n\n**DEFER** — {sentence}\n")
            self.assertEqual(watchlist.eval_trigger(ev), expected, sentence)

    def test_trigger_takes_the_earliest_match_not_the_first_pattern(self):
        # Two phrasings in one Verdict: the eval's own sentence order decides, so the
        # list order of _TRIGGER_RES is never load-bearing.
        ev = audit.Evaluation("x", "# x\n\n## Verdict\n\n**DEFER** — adopt once A holds. "
                                   "Re-evaluate after B lands.\n")
        self.assertEqual(watchlist.eval_trigger(ev), "A holds")

    def test_trigger_stops_at_a_semicolon(self):
        # These verdicts join independent clauses with `;` and the trigger is the first —
        # without this, letta's cell trailed "; for the dev loop it documents, defer".
        ev = audit.Evaluation("x", "# x\n\n## Verdict\n\n**DEFER** — ADOPT only if "
                                   "the runtime is yours; for this loop, defer.\n")
        self.assertEqual(watchlist.eval_trigger(ev), "the runtime is yours")

    def test_trigger_escapes_a_pipe(self):
        # The cell is a prose sentence an eval author wrote; an unescaped `|` would
        # silently break the markdown table on a derived page nobody edits by hand.
        ev = audit.Evaluation("x", "# x\n\n## Verdict\n\n**DEFER** — re-evaluate after "
                                   "A | B ships.\n")
        self.assertEqual(watchlist.eval_trigger(ev), r"A \| B ships")

    def test_trigger_outside_the_verdict_section_is_not_read(self):
        ev = audit.Evaluation("x", "# x\n\n## Notes\n\nre-evaluate after the moon lands.\n"
                                   "\n## Verdict\n\n**DEFER** — no condition here\n")
        self.assertIsNone(watchlist.eval_trigger(ev))

    def test_eval_only_defer_is_listed_with_its_own_stage(self):
        # The tree's one row-less DEFER is a bake-off between two tools that each already
        # have a row — a comparison document, correctly rowless — and it was the most
        # actionable item on the page it was missing from.
        comparison = ("# Tool Comparison\n\n## Plan\n\n"
                      "| Tool | Type | Auto | Free | Evaluated | Evidence |\n"
                      "|------|------|------|------|-----------|----------|\n"
                      "| other | tool | | ✓ | ADOPT | RUN |\n")
        with tempfile.TemporaryDirectory() as d:
            _write(d, "COMPARISON.md", comparison)
            _write(d, "evaluations/a-vs-b-bakeoff.md",
                   "# Bake-off: a vs b\n\n**Dev loop stage:** Reflect\n\n## Verdict\n\n"
                   "**DEFER** — blocked; re-evaluate after the arms are run.\n")
            rows, missing = watchlist.deferred(audit.DetectorContext(d))
            self.assertEqual(len(rows), 1)
            tool, stage, trigger, ev = rows[0]
            self.assertEqual(tool, "a-vs-b-bakeoff")
            self.assertEqual(stage, "Reflect")          # from the eval's own header
            self.assertEqual(trigger, "the arms are run")
            self.assertIsNotNone(ev)                     # renders as an eval link
            self.assertEqual(missing, 0)

    def test_eval_with_a_row_is_not_listed_twice(self):
        comparison = ("# Tool Comparison\n\n## Plan\n\n"
                      "| Tool | Type | Auto | Free | Evaluated | Evidence |\n"
                      "|------|------|------|------|-----------|----------|\n"
                      "| blocked | tool | | ✓ | DEFER | REVIEW |\n")
        with tempfile.TemporaryDirectory() as d:
            _write(d, "COMPARISON.md", comparison)
            _write(d, "evaluations/blocked.md",
                   "# Evaluation: blocked\n\n**Dev loop stage:** Plan\n\n## Verdict\n\n"
                   "**DEFER** — re-evaluate after the API stabilizes.\n")
            rows, _missing = watchlist.deferred(audit.DetectorContext(d))
            self.assertEqual([r[0] for r in rows], ["blocked"])

    def test_non_defer_eval_is_never_promoted_into_the_section(self):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "COMPARISON.md", "# Tool Comparison\n")
            _write(d, "evaluations/skipped.md",
                   "# Evaluation: skipped\n\n## Verdict\n\n"
                   "**SKIP** — re-evaluate after nothing.\n")
            rows, _missing = watchlist.deferred(audit.DetectorContext(d))
            self.assertEqual(rows, [])

    def test_live_tree_records_every_defer_trigger(self):
        # Pins the repair: every DEFER in the tree states its trigger, so the section
        # can never regrow a manufactured "add one" action item unnoticed.
        rows, missing = watchlist.deferred(audit.DetectorContext(ROOT))
        self.assertEqual(missing, 0, [r[0] for r in rows if r[2] == watchlist._NO_TRIGGER])
        self.assertIn("agentmemory-vs-claude-mem-bakeoff", [r[0] for r in rows])

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


    def _find(self, ctx):
        """Just the findings. `audit_catalog_mirror` also returns coverage —
        how many evals it walked and why the rest were not (#467)."""
        return audit.audit_catalog_mirror(ctx)[0]

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
            self.assertEqual(self._find(ctx), [])

    def test_renamed_repo_is_a_LINK_finding(self):
        # The #336 failure: CATALOG gets repointed on a rename, the eval never does.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [self._row("t", "https://github.com/new/t")],
                            {"t": self._eval("t", "https://github.com/old/t",
                                             self._row("t", "https://github.com/old/t"))})
            kinds = [f.kind for f in self._find(ctx)]
            self.assertEqual(kinds, ["LINK", "LINK"])  # embedded row + **Repo:** header

    def test_case_only_link_diff_is_CASE_not_LINK(self):
        # GitHub slugs are case-insensitive and redirect: this cannot make an eval
        # assert the wrong repo's facts, so it must not dilute the LINK bucket.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [self._row("t", "https://github.com/Owner/T")],
                            {"t": self._eval("t", "https://github.com/owner/t",
                                             self._row("t", "https://github.com/owner/t"))})
            self.assertEqual({f.kind for f in self._find(ctx)}, {"CASE"})

    def test_one_liner_drift_is_a_TEXT_finding(self):
        url = "https://github.com/o/t"
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [self._row("t", url, one="catalog wording")],
                            {"t": self._eval("t", url, self._row("t", url, one="eval wording"))})
            f, = self._find(ctx)
            self.assertEqual(f.kind, "TEXT")
            self.assertTrue(f.detail.startswith("one_liner:"))

    def test_overlaps_drift_is_reported(self):
        # Not cosmetic: triage.py bands leads from the overlaps cell, so which copy
        # is authoritative decides which band a lead lands in (#344).
        url = "https://github.com/o/t"
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [self._row("t", url, ovl="incumbent")],
                            {"t": self._eval("t", url, self._row("t", url, ovl="something else"))})
            f, = self._find(ctx)
            self.assertEqual((f.kind, f.detail.split(":")[0]), ("TEXT", "overlaps"))

    def test_embedded_row_with_no_catalog_row_is_ORPHAN(self):
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [], {"t": self._eval("t", "https://github.com/o/t",
                                                    self._row("t", "https://github.com/o/t"))})
            self.assertEqual([f.kind for f in self._find(ctx)], ["ORPHAN"])

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
            self.assertEqual([f.kind for f in self._find(ctx)], [])

    def test_unlinked_catalog_row_is_never_a_link_finding(self):
        # There is no URL on the catalog side to compare against, so a mirror that
        # carries one is not a disagreement — reporting LINK here would demand the eval
        # drop a working link to match an absence.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, ["| t | tool | does a thing | a pain | x |\n"],
                            {"t": self._eval("t", "https://github.com/o/other",
                                             self._row("t", "https://github.com/o/other"))})
            self.assertEqual([f.kind for f in self._find(ctx)], [])

    def test_unlinked_catalog_row_still_reports_text_drift(self):
        # Indexing the row is not the same as excusing it. Once it resolves, its cells
        # are compared like any other row's — the finding becomes TRUE, not absent.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, ["| t | tool | catalog wording | a pain | x |\n"],
                            {"t": self._eval("t", "https://github.com/o/t",
                                             self._row("t", "https://github.com/o/t"))})
            finds = self._find(ctx)
            self.assertEqual([f.kind for f in finds], ["TEXT"])
            self.assertIn("one_liner", finds[0].detail)

    def test_a_genuinely_uncatalogued_tool_is_still_ORPHAN(self):
        # The fix must not swallow the real class: nothing named `t` exists here.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, ["| other | tool | does a thing | a pain | x |\n"],
                            {"t": self._eval("t", "https://github.com/o/t",
                                             self._row("t", "https://github.com/o/t"))})
            self.assertEqual([f.kind for f in self._find(ctx)], ["ORPHAN"])

    def test_live_tree_has_no_orphan_or_case_findings(self):
        # The #401 backlog, pinned at zero. TEXT is deliberately NOT pinned — #345's
        # sequencing note is that it stays a human's per-row call.
        finds = self._find(audit.DetectorContext(ROOT))
        self.assertEqual([f"{f.kind} {f.eval_name}" for f in finds
                          if f.kind in ("ORPHAN", "CASE", "LINK", "AMBIG")], [])

    # --- coverage: what U walked, and what it never reached (#467) -------------

    def _cover(self, ctx):
        return audit.audit_catalog_mirror(ctx)[1]

    def test_the_headline_denominator_is_the_population_not_the_finding_set(self):
        # It used to print `len({f.eval_name for f in drift})` — the evals it FOUND
        # something in — where every other detector here prints n/total. Two clean evals
        # and one drifted must report a population of 3, not 1.
        with tempfile.TemporaryDirectory() as d:
            rows = [self._row(n, f"https://github.com/o/{n}") for n in ("a", "b", "c")]
            evals = {n: (f"# Evaluation: {n}\n\n**Repo:** [s](https://github.com/o/{n})\n\n"
                         f"## Catalog entry\n\n{self.HDR}"
                         f"{self._row(n, f'https://github.com/o/{n}')}")
                     for n in ("a", "b")}
            evals["c"] = (f"# Evaluation: c\n\n**Repo:** [s](https://github.com/o/c)\n\n"
                          f"## Catalog entry\n\n{self.HDR}"
                          f"{self._row('c', 'https://github.com/o/c', one='drifted')}")
            ctx = self._ctx(d, rows, evals)
            finds, cover = audit.audit_catalog_mirror(ctx)
            self.assertEqual(len({f.eval_name for f in finds}), 1)
            self.assertEqual(cover.walked, 3)      # the number the headline must print
            self.assertEqual(sum(cover.skipped.values()), 0)

    def test_an_empty_walk_is_distinguishable_from_a_clean_one(self):
        # "0 disagreement(s) across 0 eval(s)" read identically to "0 evals were checked":
        # #319's silence-is-not-success, inside the report that exists to count drift.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [self._row("t", "https://github.com/o/t")],
                            {"t": "# Evaluation: t\n\nno mirror here.\n"})
            finds, cover = audit.audit_catalog_mirror(ctx)
            self.assertEqual((finds, cover.walked), ([], 0))
            self.assertEqual(sum(cover.skipped.values()), 1)

    def test_a_missing_mirror_is_split_by_whether_the_tool_is_catalogued(self):
        # 88 of the 99 name a tool CATALOG.md lists; the other 11 do not, and only the
        # first bucket is plausibly a defect. Printed, never counted either way — whether
        # a missing mirror is wrong is a human's call, and 88 findings would be a backlog
        # manufactured out of a question nobody asked.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [self._row("t", "https://github.com/o/t")],
                            {"t": "# Evaluation: t\n\nno mirror.\n",
                             "stranger": "# Evaluation: stranger\n\nno mirror.\n"})
            cover = self._cover(ctx)
            self.assertEqual(cover.skipped[audit.SKIP_NO_SECTION_CATALOGUED], 1)
            self.assertEqual(cover.skipped[audit.SKIP_NO_SECTION], 1)

    def test_a_declared_na_is_bucketed_apart_from_a_missing_section(self):
        # `cost-audit-compress-recipe` is a recipe that correctly has no row and says so.
        # Reporting it beside 88 genuine gaps would make the honest path look like one.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [self._row("t", "https://github.com/o/t")],
                            {"t": "# Evaluation: t\n\n## Catalog entry: n/a\n\nA recipe.\n"})
            self.assertEqual(self._cover(ctx).skipped[audit.SKIP_NA], 1)

    def test_a_section_with_no_parseable_row_is_its_own_bucket(self):
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [self._row("t", "https://github.com/o/t")],
                            {"t": "# Evaluation: t\n\n## Catalog entry\n\nprose, no table.\n"})
            self.assertEqual(self._cover(ctx).skipped[audit.SKIP_NO_ROW], 1)

    # --- an UNLINKED embedded row is indexed, not dropped (#401's rule, #467) ---

    def _unlinked(self, name, one="does a thing", ovl="x"):
        """An embedded row with no link — cells otherwise identical to `_row`'s."""
        return f"| {name} | tool | {one} | a pain | {ovl} |\n"

    def test_an_unlinked_embedded_row_is_compared_not_skipped(self):
        # The filter read `if r.url is not None`, the exact mirror of the one #401 removed
        # on the CATALOG side: a row with no repo to link still names a tool and its other
        # cells are still a mirror. Two live disagreements were invisible behind it.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [self._row("t", "https://github.com/o/t", ovl="a, b")],
                            {"t": f"# Evaluation: t\n\n## Catalog entry\n\n{self.HDR}"
                                  f"{self._unlinked('t', ovl='a, b, c')}"})
            finds, cover = audit.audit_catalog_mirror(ctx)
            self.assertEqual(cover.walked, 1)
            self.assertEqual([(f.kind, f.tool) for f in finds], [("TEXT", "t")])
            self.assertIn("overlaps", finds[0].detail)

    def test_an_unlinked_embedded_row_never_produces_a_link_finding(self):
        # Skipping the URL comparison is right; skipping the row is not. There is no URL
        # on the eval's side, so there is nothing to disagree about.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [self._row("t", "https://github.com/o/t")],
                            {"t": f"# Evaluation: t\n\n## Catalog entry\n\n{self.HDR}"
                                  f"{self._unlinked('t')}"})
            self.assertEqual(self._find(ctx), [])

    def test_eval_with_no_embedded_row_has_no_CELLS_to_compare(self):
        # 107 evals reach no embedded row, so no CELL can drift. The `**Repo:**` header
        # still can, and is still checked — see the #479 block below.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [self._row("t", "https://github.com/o/t")],
                            {"t": "# Evaluation: t\n\n**Repo:** [s](https://github.com/o/t)\n"})
            self.assertEqual(self._find(ctx), [])

    def test_site_headed_eval_reports_no_header_finding(self):
        # A commercial platform heads with **Site:**, not **Repo:** — absence is not drift.
        url = "https://github.com/o/t"
        with tempfile.TemporaryDirectory() as d:
            text = (f"# Evaluation: t\n\n**Site:** [x](https://example.com)\n\n"
                    f"## Catalog entry\n\n{self.HDR}{self._row('t', url)}")
            ctx = self._ctx(d, [self._row("t", url)], {"t": text})
            self.assertEqual(self._find(ctx), [])

    # --- the header check has its OWN precondition, and its own population (#479) ---
    #
    # U checks two facts. The CELLS need a mirror to compare against; the `**Repo:**`
    # header needs only a header. The header comparison used to sit inside the branch
    # that runs when a mirror parses, so it inherited the mirror's precondition and ran
    # on 580 of the 677 evals that declare a header. One live CASE sat in the other 90.

    def _headed(self, name, url):
        """An eval with a `**Repo:**` header and deliberately NO `## Catalog entry`."""
        return f"# Evaluation: {name}\n\n**Repo:** [s]({url})\n\nprose, no mirror.\n"

    def test_a_header_is_checked_even_with_no_mirror_to_hang_it_on(self):
        # The defect itself. Before #479 this eval was bucketed as skipped and its
        # header was never looked at, so a stale catalog link was invisible.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [self._row("t", "https://github.com/new/t")],
                            {"t": self._headed("t", "https://github.com/old/t")})
            self.assertEqual([(f.kind, f.tool) for f in self._find(ctx)], [("LINK", "t")])

    def test_the_live_agentgpt_shape_is_a_CASE_finding(self):
        # What the widening actually found: the eval header canonical, the CATALOG row
        # the stale side, differing only in case. Every metadata join lowercases, so no
        # band, score or record moves — which is exactly why nothing else could see it.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [self._row("t", "https://github.com/o/agentgpt")],
                            {"t": self._headed("t", "https://github.com/o/AgentGPT")})
            self.assertEqual([f.kind for f in self._find(ctx)], ["CASE"])

    def test_a_mirrorless_eval_is_still_bucketed_as_skipped(self):
        # Checking the header must not make the eval look mirrored: `walked` counts
        # mirrors, and the skip bucket is what tells a human the mirror is missing.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [self._row("t", "https://github.com/new/t")],
                            {"t": self._headed("t", "https://github.com/old/t")})
            cover = self._cover(ctx)
            self.assertEqual(cover.walked, 0)
            self.assertEqual(cover.skipped[audit.SKIP_NO_SECTION_CATALOGUED], 1)

    def test_the_header_population_is_the_headers_not_the_mirrors(self):
        # #467's rule, one clause over: two checks, two populations. One eval mirrors,
        # two only declare a header — a single number cannot honestly stand for both.
        urls = {n: f"https://github.com/o/{n}" for n in ("a", "b", "c")}
        with tempfile.TemporaryDirectory() as d:
            evals = {"a": self._eval("a", urls["a"], self._row("a", urls["a"])),
                     "b": self._headed("b", urls["b"]),
                     "c": self._headed("c", urls["c"])}
            ctx = self._ctx(d, [self._row(n, u) for n, u in urls.items()], evals)
            cover = self._cover(ctx)
            self.assertEqual(cover.walked, 1)          # mirrors
            self.assertEqual(cover.headers, 3)         # headers compared
            self.assertEqual(cover.header_total, 3)    # headers declared

    def test_an_eval_with_no_header_is_absent_from_the_header_population(self):
        # Not a 0-of-1 abstention — a **Site:**-headed eval asserts no repo at all, so
        # counting it as an unchecked header would manufacture a coverage gap.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [self._row("t", "https://github.com/o/t")],
                            {"t": "# Evaluation: t\n\n**Site:** [x](https://example.com)\n"})
            cover = self._cover(ctx)
            self.assertEqual((cover.headers, cover.header_total), (0, 0))

    def test_an_unlinked_catalog_row_is_a_declared_but_unchecked_header(self):
        # #401's rule on the OTHER side: `server-github` has no repo to link, so there
        # is no URL to compare. It declares a header (counted) and cannot be compared
        # (not checked) — the gap must be visible, not silently closed either way.
        with tempfile.TemporaryDirectory() as d:
            catalog = "| t | tool | does a thing | a pain | x |\n"
            ctx = self._ctx(d, [catalog],
                            {"t": self._headed("t", "https://github.com/o/t")})
            finds, cover = audit.audit_catalog_mirror(ctx)
            self.assertEqual(finds, [])
            self.assertEqual((cover.headers, cover.header_total), (0, 1))

    def test_a_header_naming_an_uncatalogued_tool_is_not_a_finding(self):
        # The six comparison and collection documents (`agent-harnesses`,
        # `recommended-tools`, …). No row resolves, so there is nothing to disagree
        # with — flagging one would flag a healthy file (detector V's rule).
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [self._row("t", "https://github.com/o/t")],
                            {"stranger": self._headed("stranger", "https://github.com/o/s")})
            finds, cover = audit.audit_catalog_mirror(ctx)
            self.assertEqual(finds, [])
            self.assertEqual((cover.headers, cover.header_total), (0, 1))

    def test_the_no_mirror_branch_resolves_by_the_same_name_as_its_skip_bucket(self):
        # The bucket and the comparison must not be able to disagree about which row an
        # eval is about — they are one `lookup(ev.name)` call apart. Asserted together:
        # resolving the header off a different name leaves the bucket saying the tool IS
        # catalogued while the header check silently abstains.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [self._row("t", "https://github.com/new/t")],
                            {"t": self._headed("t", "https://github.com/old/t")})
            finds, cover = audit.audit_catalog_mirror(ctx)
            self.assertEqual(cover.skipped[audit.SKIP_NO_SECTION_CATALOGUED], 1)
            self.assertEqual(cover.headers, 1)
            self.assertEqual([f.tool for f in finds], ["t"])

    def test_pack_eval_checks_every_embedded_row(self):
        # A pack eval embeds its siblings' rows too; each mirrors a catalog row.
        a, b = "https://github.com/o/a", "https://github.com/o/b"
        with tempfile.TemporaryDirectory() as d:
            text = (f"# Evaluation: pack\n\n**Repo:** [s]({a})\n\n## Catalog entry\n\n"
                    f"{self.HDR}{self._row('a', a)}{self._row('b', b, one='eval wording')}")
            ctx = self._ctx(d, [self._row("a", a), self._row("b", b, one="catalog wording")],
                            {"pack": text})
            f, = self._find(ctx)
            self.assertEqual((f.tool, f.kind), ("b", "TEXT"))

    def test_parenthetical_name_resolves_to_its_catalog_row(self):
        # 'GSD (gsd-core)' must find the catalog row via identity_keys, not report ORPHAN.
        url = "https://github.com/o/gsd"
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [self._row("GSD (gsd-core)", url)],
                            {"gsd": self._eval("GSD", url, self._row("GSD (gsd-core)", url))})
            self.assertEqual(self._find(ctx), [])

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

    def test_the_printed_headline_carries_BOTH_populations(self):
        # The headline is the surface a human reads, and #467 is about this exact line:
        # a coverage number that stands for the wrong population reads as a clean sweep.
        # Two checks, two denominators — one mirrored eval, three declaring a header.
        urls = {n: f"https://github.com/o/{n}" for n in ("a", "b", "c")}
        with tempfile.TemporaryDirectory() as d:
            for fn in ("audit-evals.py", "catalog_lib.py"):
                shutil.copy(os.path.join(ROOT, fn), os.path.join(d, fn))
            self._ctx(d, [self._row(n, u) for n, u in urls.items()],
                      {"a": self._eval("a", urls["a"], self._row("a", urls["a"])),
                       "b": self._headed("b", urls["b"]),
                       "c": self._headed("c", urls["c"])})
            r = subprocess.run(["python3", "audit-evals.py", "--catalog-mirror"],
                               cwd=d, capture_output=True, text=True, check=False)
            head = r.stdout.splitlines()[0]
            self.assertIn("of 1 mirrored eval(s)", head, msg=head)
            self.assertIn("header checked in 3 of 3 declaring one", head, msg=head)

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
            self.assertEqual(self._find(ctx), [])

    def test_collapsed_key_reaching_two_rows_is_AMBIG_not_a_guess(self):
        # No exact match, and the fallback key reaches two distinct tools: resolve to
        # nothing and say so, rather than to whichever row happened to come first.
        a = "https://github.com/one/agent-skills"
        b = "https://github.com/two/agent_skills"
        with tempfile.TemporaryDirectory() as d:
            ctx = self._ctx(d, [self._row("agent-skills", a), self._row("agent_skills", b)],
                            {"e": self._eval("e", a, self._row("agentskills", a))})
            f, = self._find(ctx)
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
            self.assertEqual(self._find(ctx), [])

    def test_header_naming_only_the_old_repo_is_still_drift(self):
        old, new = "https://github.com/o/old", "https://github.com/o/new"
        with tempfile.TemporaryDirectory() as d:
            text = (f"# Evaluation: t\n\n**Repo:** [old]({old})\n\n"
                    f"## Catalog entry\n\n{self.HDR}{self._row('t', new)}")
            ctx = self._ctx(d, [self._row("t", new)], {"t": text})
            # only the header is stale here — the embedded row already matches
            self.assertEqual([f.kind for f in self._find(ctx)], ["LINK"])


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

    # --- a record is a fact about a REPO, and a pack has several rows (#465) ---

    PACK = ("## Implement\n\n| Name | Type | One-liner | Problem it solves | Overlaps with |\n"
            "|---|---|---|---|---|\n"
            "| [alpha](https://github.com/x/pack/tree/main/plugins/alpha) | tool | live tool | y | z |\n"
            "| [pack](https://github.com/x/pack) | tool | the pack ⚠️ discontinued | y | z |\n")
    PACK_COMP = ("# T\n\n## Implement\n\n| Tool | Type | Auto | Free | Evaluated | Evidence |\n"
                 "|---|---|---|---|---|---|\n"
                 "| alpha | tool | y | y | ADOPT | REVIEW |\n"
                 "| pack | tool | y | y | SKIP | REVIEW |\n")

    def _pack_ctx(self, d, catalog):
        os.makedirs(os.path.join(d, "evaluations"), exist_ok=True)
        _write(d, "CATALOG.md", catalog)
        _write(d, "COMPARISON.md", self.PACK_COMP)
        _write(d, "repo-metadata.json", json.dumps(
            {"x/pack": {"archived": False, "license_spdx": "MIT",
                        "discontinued": "no longer maintained"}}))
        return audit.DetectorContext(d)

    def test_a_shared_slug_asks_every_row_about_disclosure(self):
        # `pack` discloses and `alpha` does not. Asking one row called this disclosed;
        # if the repo is dead, every row that advertises it needs the note (#465).
        with tempfile.TemporaryDirectory() as d:
            finds, _, _ = audit.audit_maintenance(self._pack_ctx(d, self.PACK))
            self.assertEqual(len(finds), 1)
            self.assertFalse(finds[0].disclosed)
            self.assertEqual(finds[0].silent, ("alpha",))
            self.assertEqual(finds[0].tool, "pack")          # the row that links the root
            self.assertEqual(finds[0].verdict, "ADOPT, SKIP")  # every verdict behind it

    def test_maintenance_findings_do_not_depend_on_row_order(self):
        rows = self.PACK.splitlines(keepends=True)
        flipped = "".join([*rows[:4], rows[5], rows[4]])
        with tempfile.TemporaryDirectory() as d1, tempfile.TemporaryDirectory() as d2:
            a, _, _ = audit.audit_maintenance(self._pack_ctx(d1, self.PACK))
            b, _, _ = audit.audit_maintenance(self._pack_ctx(d2, flipped))
            self.assertEqual(a, b)

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


class TestUnactionableContainment(unittest.TestCase):
    """Pins detector AA (#405). `Ships inside` is what triage.py bands P5 on, and P5's
    disposition — "settle the container" — has a precondition nobody checked: the
    container has to be findable. The cell is free text and its documented rules are
    enforced by nothing."""

    HDR = ("| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |\n"
           "|------|------|-----------|-------------------|---------------|--------------|\n")
    PACK = "https://github.com/o/pack"

    def _find(self, rows, verdicts=()):
        """rows is (name, url, ships_inside)."""
        with tempfile.TemporaryDirectory() as d:
            _write(d, "CATALOG.md", "## Implement\n\n" + self.HDR + "".join(
                f"| [{n}]({u}) | skill | x | y | z | {c} |\n" for n, u, c in rows))
            _write(d, "COMPARISON.md",
                   "# T\n\n## Implement\n\n"
                   "| Tool | Type | Auto | Free | Evaluated | Evidence |\n"
                   "|---|---|---|---|---|---|\n" + "".join(
                       f"| {n} | skill | y | y | {v} | REVIEW |\n" for n, v in verdicts))
            return audit.audit_containment(audit.DetectorContext(d))

    def test_a_container_with_no_catalog_row_is_unrowed(self):
        # `getsentry/skills` holds `presentation-creator` and is not itself catalogued,
        # so "settle the container" names something not in the inventory.
        finds, declared = self._find([("skill-a", self.PACK + "/tree/main/a", "o/pack")])
        self.assertEqual([(f.kind, f.tool, f.container) for f in finds],
                         [("UNROWED", "skill-a", "o/pack")])
        self.assertEqual(declared, 1)

    def test_a_catalogued_container_clears_the_row(self):
        finds, declared = self._find([("pack", self.PACK, ""),
                                      ("skill-a", self.PACK + "/tree/main/a", "o/pack")])
        self.assertEqual((finds, declared), ([], 1))

    def test_the_container_row_must_not_itself_be_contained(self):
        # A row that ships inside something is a member, never the pack — otherwise one
        # member would vouch for another and the group would clear itself.
        finds, _ = self._find([("member", self.PACK, "o/other"),
                               ("skill-a", self.PACK + "/tree/main/a", "o/pack")])
        self.assertEqual(sorted(f.tool for f in finds if f.kind == "UNROWED"),
                         ["member", "skill-a"])

    def test_self_linked_fires_only_on_a_root_link(self):
        # THE precision rule, and the bug this test was written against: both rows share
        # a repo root, and only the one linking the root is indistinguishable from the
        # pack. A subpath link names the artifact and is clean.
        finds, _ = self._find([("pack", self.PACK, ""),
                               ("root-linked", self.PACK, "o/pack"),
                               ("subpath", self.PACK + "/tree/main/a", "o/pack")])
        self.assertEqual([(f.kind, f.tool) for f in finds],
                         [("SELF-LINKED", "root-linked")])

    def test_both_kinds_can_fire_on_one_row(self):
        # `prisma` and `jira`: the container has no row AND the row links it. Two facts
        # are wrong, and they want different fixes, so they are two findings.
        finds, _ = self._find([("prisma", self.PACK, "o/pack")])
        self.assertEqual([f.kind for f in finds], ["UNROWED", "SELF-LINKED"])

    def test_an_undeclared_row_is_never_a_finding(self):
        # Empty is the column's default and means "independently installable" (#343).
        # A detector that read it as a hole would flag ~630 healthy rows.
        self.assertEqual(self._find([("a", self.PACK, ""), ("b", "https://github.com/o/b", "")]),
                         ([], 0))

    def test_leads_sort_ahead_of_disposed_rows_within_a_kind(self):
        # A stalled queue slot is the cost this detector is about, so a lead outranks a
        # row that already carries a verdict.
        finds, _ = self._find(
            [("done", self.PACK + "/tree/main/done", "o/pack"),
             ("lead", self.PACK + "/tree/main/lead", "o/pack")],
            [("done", "SKIP"), ("lead", "discovery-log")])
        self.assertEqual([f.tool for f in finds], ["lead", "done"])

    def test_live_run_produces_no_false_positives(self):
        # Guards the real tree STRUCTURALLY, not by count. A pinned backlog number would
        # fail the build the moment a human fixed one row or a discovery pass added a
        # declared one — U's rule: pin the buckets that must stay at zero, never the
        # bucket a human resolves. What must hold on any tree: only declaring rows are
        # ever findings, and SELF-LINKED never fires on a subpath link (the first draft
        # compared repo roots and flagged all 24 declarations, including the 8
        # claude-plugins-official plugins that link their own subpath).
        ctx = audit.DetectorContext(ROOT)
        finds, declared = audit.audit_containment(ctx)
        rows = {r.name: r for r in catalog_lib.parse_catalog_rows(ctx.catalog)}
        self.assertTrue(declared)
        for f in finds:
            self.assertIn(f.kind, ("UNROWED", "SELF-LINKED"))
            self.assertTrue(rows[f.tool].ships_inside, f"{f.tool} declares nothing")
            if f.kind == "SELF-LINKED":
                self.assertTrue(audit._links_repo_root(rows[f.tool].url),
                                f"{f.tool} links a subpath — not its container")

    def test_a_repointed_row_still_resolves_to_the_container_it_declares(self):
        # #405's SELF-LINKED remedy is a NARROWER link, and narrowing it wrongly is the
        # way to make things worse: a subpath under the wrong repo clears SELF-LINKED
        # (it is no longer a root link) while pointing every fact on the row — stars,
        # license, archival — at a stranger. AA cannot catch that; this can.
        for r in catalog_lib.parse_catalog_rows(audit.DetectorContext(ROOT).catalog):
            if not (r.ships_inside and r.url) or audit._links_repo_root(r.url):
                continue
            slugs = [s.lower() for s in catalog_lib.github_repos(r.url)]
            self.assertIn(r.ships_inside.strip().lower(), slugs,
                          f"{r.name} links a subpath of {slugs} but declares "
                          f"{r.ships_inside}")


class TestUnfalsifiedContainment(unittest.TestCase):
    """Pins detector AF (#431). AA checks that a `Ships inside` container is FINDABLE;
    this checks the rule the column is DEFINED by — "empty means independently
    installable" — which nothing could contradict. The cell buys a P5 band whose
    disposition is "never an independent lead", so a wrong one does not misrank a lead,
    it removes it from the queue."""

    HDR = ("| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |\n"
           "|------|------|-----------|-------------------|---------------|--------------|\n")
    PACK = "https://github.com/o/pack"

    @classmethod
    def setUpClass(cls):
        cls.refresh = _load("refresh_metadata", "refresh-metadata.py")

    def _run(self, rows, members=None, verdicts=()):
        """rows is (name, url, ships_inside); members is {subpath: package-or-None}."""
        with tempfile.TemporaryDirectory() as d:
            _write(d, "CATALOG.md", "## Implement\n\n" + self.HDR + "".join(
                f"| [{n}]({u}) | skill | x | y | z | {c} |\n" for n, u, c in rows))
            _write(d, "COMPARISON.md",
                   "# T\n\n## Implement\n\n"
                   "| Tool | Type | Auto | Free | Evaluated | Evidence |\n"
                   "|---|---|---|---|---|---|\n" + "".join(
                       f"| {n} | skill | y | y | {v} | REVIEW |\n" for n, v in verdicts))
            if members is not None:
                _write(d, "repo-metadata.json",
                       json.dumps({"o/pack": {"member_packages": members}}))
            return audit.audit_containment_evidence(audit.DetectorContext(d))

    def test_a_published_subpath_refutes_the_cell(self):
        # `src/memory` publishes @modelcontextprotocol/server-memory, which npx installs
        # and nothing else — so the artifact IS independently installable.
        ref, conf, unch, seen = self._run(
            [("member", self.PACK + "/tree/main/a", "o/pack")], {"a": "@scope/member"})
        self.assertEqual([(f.kind, f.tool, f.package) for f in ref],
                         [("REFUTED", "member", "@scope/member")])
        self.assertEqual((conf, unch, seen), ([], [], 1))

    def test_no_manifest_confirms_but_is_never_counted(self):
        # THE precision rule: absence is not proof of containment — a pack could publish
        # to npm without per-member manifests — so the test only ever REFUTES. That makes
        # detector V's rule (a false positive costs more than a miss) structural.
        ref, conf, _unch, seen = self._run(
            [("member", self.PACK + "/tree/main/a", "o/pack")], {"a": None})
        self.assertEqual(ref, [])
        self.assertEqual([(f.kind, f.tool) for f in conf], [("confirmed", "member")])
        self.assertEqual(seen, 1)

    def test_a_root_link_has_no_component_to_ask_about(self):
        # `prisma`, `jira`, `confluence` — already AA's SELF-LINKED, and reporting them
        # here as a second finding would put one defect on two scoreboards.
        ref, conf, unch, seen = self._run([("member", self.PACK, "o/pack")], {})
        self.assertEqual((ref, conf, seen), ([], [], 0))
        self.assertEqual([(f.kind, f.tool, f.path) for f in unch],
                         [("unchecked", "member", None)])

    def test_no_records_is_not_zero_findings(self):
        # Detector V's rule. An uncollected signal must never present as a clean sweep:
        # nothing was asked, so nothing can be concluded.
        ref, conf, unch, seen = self._run(
            [("member", self.PACK + "/tree/main/a", "o/pack")], None)
        self.assertEqual((ref, conf, seen), ([], [], 0))
        self.assertEqual(len(unch), 1)

    def test_an_undeclared_row_is_never_examined(self):
        # Empty is the column's default. A row that never claimed containment cannot
        # have its containment refuted.
        self.assertEqual(
            self._run([("a", self.PACK + "/tree/main/a", "")], {"a": "@scope/a"}),
            ([], [], [], 0))

    def test_leads_sort_ahead_of_disposed_rows(self):
        # A stalled queue slot is the cost; a wrong cell on a SKIPped row is a wrong fact
        # with no queue effect.
        ref, _, _, _ = self._run(
            [("done", self.PACK + "/tree/main/d", "o/pack"),
             ("lead", self.PACK + "/tree/main/l", "o/pack")],
            {"d": "@scope/d", "l": "@scope/l"},
            [("done", "SKIP"), ("lead", "discovery-log")])
        self.assertEqual([f.tool for f in ref], ["lead", "done"])

    def test_live_tree_has_no_refuted_declaration(self):
        # Pinned at zero, unlike AA's backlog: a REFUTED row is a mechanical fact npm
        # settles, not a human's judgement call, so it must never regrow. The three
        # `modelcontextprotocol/servers` cells were emptied in #431.
        ref, _conf, _unch, seen = audit.audit_containment_evidence(audit.DetectorContext(ROOT))
        self.assertEqual([f.tool for f in ref], [], f"refuted containment: {ref}")
        self.assertTrue(seen, "no member_packages records — run refresh-metadata "
                              "--containment (0 records is not 0 findings)")

    def test_a_private_container_manifest_is_not_a_member_package(self):
        # npm's own marker for "this is not published". @modelcontextprotocol/servers
        # carries it, which is why "settle the container" named an impossible operation.
        self.assertIsNone(self.refresh._manifest_package(
            'package.json', '{"name": "@scope/pack", "private": true}'))
        self.assertEqual(self.refresh._manifest_package(
            'package.json', '{"name": "@scope/member", "version": "1.0.0"}'), "@scope/member")
        self.assertEqual(self.refresh._manifest_package(
            'pyproject.toml', '[project]\nname = "member"\n'), "member")

    def test_only_subpath_links_are_collected(self):
        # The subpath IS the question. A row linking a repo root contributes nothing to
        # collect, so --containment never spends a call on one.
        got = self.refresh.declared_subpaths(
            self.HDR
            + f"| [root]({self.PACK}) | skill | x | y | z | o/pack |\n"
            + f"| [sub]({self.PACK}/tree/main/a) | skill | x | y | z | o/pack |\n"
            + f"| [free]({self.PACK}/tree/main/b) | skill | x | y | z |  |\n")
        self.assertEqual(got, {"o/pack": {"a": "sub"}})


class TestUnentitledConditional(unittest.TestCase):
    """Pins detector AB (#407). ADR-0005's rule is a disjunction — a real verdict needs
    the tool exercised OR a genuine `adopt-if:` condition — and #69 parked point 1 as an
    optional follow-up that was never done. Detector T guards the eval-headline direction
    of the same rule; nothing guarded the verdict data itself."""

    def _run(self, rows):
        """rows is (tool, evidence, verdict, eval_body_extra)."""
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "evaluations"), exist_ok=True)
            _write(d, "COMPARISON.md",
                   "# T\n\n## Implement\n\n"
                   "| Tool | Type | Auto | Free | Evaluated | Evidence |\n"
                   "|---|---|---|---|---|---|\n" + "".join(
                       f"| {t} | tool | y | y | {v} | {e} |\n" for t, e, v, _ in rows))
            for t, e, _, extra in rows:
                if e is None:
                    continue  # a CONDITIONAL row with no eval at all
                _write(d, f"evaluations/{t}.md",
                       f"# {t}\n\n**Repo:** [{t}](https://github.com/o/{t})\n\n"
                       f"## How we tested it\n\n**Evidence:** {e}\n\nRan it.\n\n"
                       f"## Verdict\n\n**CONDITIONAL**\n\n{extra}\n")
            return audit.audit_conditional_gate(audit.DetectorContext(d))

    def test_unexercised_and_ungated_is_the_finding(self):
        unent, ungated, total = self._run([("a", "REVIEW", "CONDITIONAL", "Use it when.")])
        self.assertEqual([(f.tool, f.evidence, f.gated) for f in unent],
                         [("a", "REVIEW", False)])
        self.assertEqual((ungated, total), ([], 1))

    def test_exercised_without_a_condition_is_context_not_a_finding(self):
        # Entitled under ADR-0005's second clause, so not a finding — but point 1 still
        # wants a condition string, and that number should be visible rather than implied.
        unent, ungated, _ = self._run([("a", "RUN", "CONDITIONAL", "Use it when.")])
        self.assertEqual(unent, [])
        self.assertEqual([f.tool for f in ungated], ["a"])

    def test_a_declared_condition_entitles_an_unexercised_row(self):
        # The whole point of point 1: a gate is the OTHER way to earn the word, so a
        # REVIEW row that declares one is in neither bucket.
        unent, ungated, total = self._run(
            [("a", "REVIEW", "CONDITIONAL", "adopt-if: linux-host — needs a Linux host.")])
        self.assertEqual((unent, ungated, total), ([], [], 1))

    def test_the_condition_match_tolerates_case_and_spacing(self):
        for form in ("Adopt-If: x", "adopt-if : x", "ADOPT-IF:x"):
            unent, _, _ = self._run([("a", "REVIEW", "CONDITIONAL", form)])
            self.assertEqual(unent, [], f"{form!r} should count as a declared condition")

    def test_only_conditional_rows_are_examined(self):
        # An unexercised ADOPT is detector K's business, not this one. Two detectors
        # reporting the same row under different rules is how a count stops meaning
        # anything.
        self.assertEqual(self._run([("a", "REVIEW", "ADOPT", ""),
                                    ("b", "REVIEW", "discovery-log", "")]), ([], [], 0))

    def test_a_conditional_row_with_no_eval_can_never_be_entitled(self):
        # No eval is the weakest possible ground: SOURCE-ONLY by backfill-evidence's own
        # rule, and there is no file in which to declare a gate.
        unent, _, total = self._run([("ghost", None, "CONDITIONAL", "")])
        self.assertEqual([(f.tool, f.evidence) for f in unent], [("ghost", "SOURCE-ONLY")])
        self.assertEqual(total, 1)

    def test_live_run_buckets_are_disjoint_and_cover_every_conditional(self):
        # Structural, not a pinned backlog count: humans will fix these one at a time,
        # and a count assertion would fail the build for the fix. What must hold on any
        # tree is that the two buckets partition the CONDITIONAL rows minus the gated
        # ones, and that no gated row is ever reported.
        unent, ungated, total = audit.audit_conditional_gate(audit.DetectorContext(ROOT))
        self.assertTrue(total)
        self.assertEqual({f.tool for f in unent} & {f.tool for f in ungated}, set())
        self.assertTrue(all(not f.gated for f in unent + ungated))
        self.assertTrue(all(f.evidence not in ("MEASURED", "RUN") for f in unent))
        self.assertTrue(all(f.evidence in ("MEASURED", "RUN") for f in ungated))


class TestWorkflowRecommendsSkip(unittest.TestCase):
    """Pins detector AE (#414). Detector P enforces that every STACK pick appears in
    WORKFLOW.md and explicitly exempts the reverse — right for CONDITIONAL, wrong for
    SKIP, which is the catalog concluding don't-use-this. `trailofbits/skills` is listed
    twice as a Review-stage option and SKIPped because vendoring it attaches CC-BY-SA
    ShareAlike to the consuming repo."""

    def _run(self, workflow, rows):
        """rows is (name, slug, verdict)."""
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "evaluations"), exist_ok=True)
            _write(d, "WORKFLOW.md", workflow)
            _write(d, "CATALOG.md", "## Plan\n"
                   "| Name | Type | One-liner | Problem | Overlaps with | Ships inside |\n"
                   "|---|---|---|---|---|---|\n" + "".join(
                       f"| [{n}](https://github.com/{s}) | tool | one | two | — | |\n"
                       for n, s, _ in rows))
            _write(d, "COMPARISON.md", "# T\n\n## Plan\n\n"
                   "| Tool | Type | Auto | Free | Evaluated | Evidence |\n"
                   "|---|---|---|---|---|---|\n" + "".join(
                       f"| {n} | tool | y | y | {v} | REVIEW |\n" for n, _, v in rows))
            return audit.audit_workflow_skips(audit.DetectorContext(d))

    def test_a_skipped_tool_recommended_without_disclosure_is_the_finding(self):
        finds, disclosed, linked = self._run(
            "## Review\n\n| [tob](https://github.com/trailofbits/skills) — audit methodology |\n",
            [("tob", "trailofbits/skills", "SKIP")])
        self.assertEqual([(f.tool, f.line) for f in finds], [("tob", 3)])
        self.assertEqual((disclosed, linked), ([], 1))

    # --- a WORKFLOW link into a pack is told apart by its text (#465) ---

    PACK_ROWS = ("## Plan\n"
                 "| Name | Type | One-liner | Problem | Overlaps with | Ships inside |\n"
                 "|---|---|---|---|---|---|\n"
                 "| [alpha](https://github.com/x/pack/tree/main/plugins/alpha) | tool | o | t | — | |\n"
                 "| [beta](https://github.com/x/pack/tree/main/plugins/beta) | tool | o | t | — | |\n")
    PACK_VERDICTS = ("# T\n\n## Plan\n\n| Tool | Type | Auto | Free | Evaluated | Evidence |\n"
                     "|---|---|---|---|---|---|\n"
                     "| alpha | tool | y | y | ADOPT | REVIEW |\n"
                     "| beta | tool | y | y | SKIP | REVIEW |\n")

    def _pack_run(self, workflow, catalog=None):
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "evaluations"), exist_ok=True)
            _write(d, "WORKFLOW.md", workflow)
            _write(d, "CATALOG.md", catalog or self.PACK_ROWS)
            _write(d, "COMPARISON.md", self.PACK_VERDICTS)
            return audit.audit_workflow_skips(audit.DetectorContext(d))

    def test_a_pack_root_link_is_resolved_by_its_text(self):
        # The manual links a component at the pack root — nine live WORKFLOW lines do.
        # Reading the slug alone asked whichever row came first, so the SKIPped `beta`
        # was reported or missed depending on CATALOG.md's row order (#465).
        finds, _, linked = self._pack_run(
            "## Review\n\n| [beta](https://github.com/x/pack) — a component |\n")
        self.assertEqual([(f.tool, f.line) for f in finds], [("beta", 3)])
        self.assertEqual(linked, 1)

    def test_a_healthy_sibling_of_a_skip_is_not_flagged(self):
        finds, _, linked = self._pack_run(
            "## Review\n\n| [alpha](https://github.com/x/pack) — a component |\n")
        self.assertEqual((finds, linked), ([], 1))

    def test_an_unidentifiable_pack_link_is_not_a_finding(self):
        # Neither the text nor the link names a candidate. Report-only, so silence beats
        # naming a stranger — flagging a healthy row costs more than missing a sick one.
        finds, _, linked = self._pack_run(
            "## Review\n\n| [the pack](https://github.com/x/pack) — everything |\n")
        self.assertEqual((finds, linked), ([], 0))

    def test_workflow_skip_findings_do_not_depend_on_row_order(self):
        rows = self.PACK_ROWS.splitlines(keepends=True)
        flipped = "".join([*rows[:3], rows[4], rows[3]])
        wf = "## Review\n\n| [beta](https://github.com/x/pack) — a component |\n"
        self.assertEqual(self._pack_run(wf), self._pack_run(wf, flipped))

    def test_only_skip_counts(self):
        # CONDITIONAL and discovery-log mentions are the exemption detector P grants;
        # DEFER means revisit, not don't-use. Reporting them would drown the ones that
        # matter, and two detectors scoring one row is how a count stops meaning anything.
        for verdict in ("CONDITIONAL", "discovery-log", "ADOPT", "KEEP", "DEFER"):
            finds, _, _ = self._run(
                "## Review\n\n| [t](https://github.com/o/t) — a tool |\n",
                [("t", "o/t", verdict)])
            self.assertEqual(finds, [], verdict)

    def test_a_line_that_discloses_is_printed_never_counted(self):
        for line in ("| [t](https://github.com/o/t) — SKIP, kept for reference |",
                     "| [t](https://github.com/o/t) — excluded, overlaps superpowers |",
                     "| [t](https://github.com/o/t) — ⚠️ superseded by u |"):
            finds, disclosed, _ = self._run(f"## Review\n\n{line}\n",
                                            [("t", "o/t", "SKIP")])
            self.assertEqual(finds, [], line)
            self.assertEqual(len(disclosed), 1, line)

    def test_the_manuals_own_excluded_section_is_a_disclosure(self):
        # WORKFLOW.md already carries the convention; a link inside that section is an
        # exclusion notice, not a recommendation.
        wf = ("## Review\n\n| [t](https://github.com/o/t) — SKIP noted |\n\n"
              "## Tools Deliberately Excluded\n\n"
              "| [u](https://github.com/o/u) | overlaps superpowers |\n")
        finds, disclosed, _ = self._run(wf, [("t", "o/t", "SKIP"), ("u", "o/u", "SKIP")])
        self.assertEqual(finds, [])
        self.assertEqual({f.tool for f in disclosed}, {"t", "u"})

    def test_the_excluded_section_ends_at_the_next_heading(self):
        wf = ("## Tools Deliberately Excluded\n\n| [u](https://github.com/o/u) | why |\n\n"
              "## Review\n\n| [t](https://github.com/o/t) — use this |\n")
        finds, disclosed, _ = self._run(wf, [("t", "o/t", "SKIP"), ("u", "o/u", "SKIP")])
        self.assertEqual([f.tool for f in finds], ["t"])
        self.assertEqual([f.tool for f in disclosed], ["u"])

    def test_matching_is_by_slug_not_display_name(self):
        # Detector P's rule: names vary, and "GSD" links to obra/superpowers. A link to a
        # DIFFERENT repo that happens to share a display name must not be attributed.
        finds, _, linked = self._run(
            "## Review\n\n| [skills](https://github.com/other/skills) — unrelated |\n",
            [("skills", "trailofbits/skills", "SKIP")])
        self.assertEqual((finds, linked), ([], 0))

    def test_a_missing_workflow_yields_zero_links_not_zero_findings(self):
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "evaluations"), exist_ok=True)
            _write(d, "CATALOG.md", "## Plan\n")
            _write(d, "COMPARISON.md", "# T\n")
            self.assertEqual(audit.audit_workflow_skips(audit.DetectorContext(d)),
                             ([], [], 0))

    def test_live_findings_all_name_a_skip_row(self):
        # Structural, not a pinned count: a human resolves these one at a time.
        finds, disclosed, linked = audit.audit_workflow_skips(audit.DetectorContext(ROOT))
        ctx = audit.DetectorContext(ROOT)
        self.assertTrue(linked)
        for f in finds + disclosed:
            v = next((ctx.comparison_verdict_map[k]
                      for k in audit.catalog_lib.identity_keys(f.tool)
                      if k in ctx.comparison_verdict_map), None)
            self.assertEqual(v, "SKIP", f.tool)


class TestLicenseHeaderVsRecord(unittest.TestCase):
    """Pins detector AC (#411). Every eval header restates an upstream fact by hand next
    to `repo-metadata.json`, which holds the same fact — and nothing compared them, so a
    SKIP reading "no declared license" stood against a record reading MIT. #372's shape
    in the file #372 did not look at: detector Z fires only on `license_spdx: NONE`, so
    an understatement on the EVAL's side is invisible to it."""

    def _run(self, evals, records, verdicts=None, verdict_prose=None):
        """evals is (name, slug, license_header); records is {slug: record}.
        verdicts/verdict_prose map an eval name to its COMPARISON verdict and its
        `## Verdict` text — the two inputs the UNGROUNDED-SKIP split reads (#417)."""
        verdicts, verdict_prose = verdicts or {}, verdict_prose or {}
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "evaluations"), exist_ok=True)
            rows = "".join(f"| {n} | tool | | ✓ | {v} | REVIEW |\n"
                           for n, v in verdicts.items())
            _write(d, "COMPARISON.md", "# T\n\n## Implement\n\n"
                   "| Tool | Type | Auto | Free | Evaluated | Evidence |\n|---|---|---|---|---|---|\n"
                   + rows)
            _write(d, "repo-metadata.json", json.dumps(records))
            for name, slug, lic in evals:
                head = "**Stars:** 1 | **Last updated:** 2026-01-01"
                if lic is not None:
                    head += f" | **License:** {lic}"
                body = ""
                if name in verdict_prose:
                    body = f"\n## Verdict\n\n{verdict_prose[name]}\n"
                _write(d, f"evaluations/{name}.md",
                       f"# Evaluation: {name}\n\n"
                       f"**Repo:** [{slug}](https://github.com/{slug})\n{head}\n\n"
                       "## How we tested it\n\n**Evidence:** REVIEW\n\nRead it.\n" + body)
            return audit.audit_license_header(audit.DetectorContext(d))

    @staticmethod
    def _rec(spdx, resolved=None):
        return {"license_spdx": spdx, "resolved_name": resolved, "archived": False}

    def test_an_asserted_absence_the_record_refutes_is_ungrounded(self):
        # The load-bearing kind: an absence is the one ground a P4 mechanical SKIP may
        # rest on, so contradicting it invalidates a disposition, not merely a fact.
        finds, redir, compared = self._run(
            [("pi", "o/pi", "none specified")], {"o/pi": self._rec("MIT")})
        self.assertEqual([(f.kind, f.name, f.header, f.spdx) for f in finds],
                         [("UNGROUNDED", "pi", "none specified", "MIT")])
        self.assertEqual((redir, compared), ([], 1))

    def test_two_named_licenses_that_differ_are_a_conflict(self):
        finds, _, _ = self._run([("a", "o/a", "MIT")], {"o/a": self._rec("Apache-2.0")})
        self.assertEqual([(f.kind, f.name) for f in finds], [("CONFLICT", "a")])

    # --- #417: an absence a live SKIP rests on is a void disposition, not a wrong fact ---

    SKIP_GROUND = "**SKIP** — no declared license; text carrying no license grant cannot be copied in."

    def test_absence_a_live_skip_rests_on_is_ungrounded_skip(self):
        finds, _, _ = self._run(
            [("pi", "o/pi", "none specified")], {"o/pi": self._rec("MIT")},
            verdicts={"pi": "SKIP"}, verdict_prose={"pi": self.SKIP_GROUND})
        self.assertEqual([(f.kind, f.name) for f in finds], [("UNGROUNDED-SKIP", "pi")])

    def test_absence_with_no_disposition_on_it_stays_plain_ungrounded(self):
        # kreuzberg/repowise shape: the header is wrong and the row is a discovery-log
        # lead, so an open item is answered — nothing is invalidated.
        finds, _, _ = self._run(
            [("k", "o/k", "none specified")], {"o/k": self._rec("MIT")},
            verdicts={"k": "discovery-log"},
            verdict_prose={"k": "**discovery-log** — pin the license terms first."})
        self.assertEqual([(f.kind, f.name) for f in finds], [("UNGROUNDED", "k")])

    def test_a_skip_not_grounded_on_the_license_is_not_ungrounded_skip(self):
        # Z's LICENSE_GROUND is deliberately narrow: a SKIP for another reason must not
        # be upgraded just because the header happens to be wrong.
        finds, _, _ = self._run(
            [("s", "o/s", "none specified")], {"o/s": self._rec("MIT")},
            verdicts={"s": "SKIP"},
            verdict_prose={"s": "**SKIP** — redundant with the incumbent."})
        self.assertEqual([(f.kind, f.name) for f in finds], [("UNGROUNDED", "s")])

    def test_a_withdrawn_ground_drops_back_to_plain_ungrounded(self):
        # Z's rule: quoting the claim you retract is the honest way to record a repair,
        # so a documented retraction must not read as a live invalid disposition.
        finds, _, _ = self._run(
            [("w", "o/w", "none specified")], {"o/w": self._rec("MIT")},
            verdicts={"w": "SKIP"},
            verdict_prose={"w": "**SKIP** — ~~no declared license~~. The license ground "
                                "is withdrawn; upstream added MIT."})
        self.assertEqual([(f.kind, f.name) for f in finds], [("UNGROUNDED", "w")])

    def test_ungrounded_skip_sorts_ahead_of_everything(self):
        finds, _, _ = self._run(
            [("c", "o/c", "MIT"), ("u", "o/u", "none specified"),
             ("z", "o/z", "none specified")],
            {"o/c": self._rec("Apache-2.0"), "o/u": self._rec("MIT"), "o/z": self._rec("MIT")},
            verdicts={"z": "SKIP"}, verdict_prose={"z": self.SKIP_GROUND})
        self.assertEqual([f.kind for f in finds],
                         ["UNGROUNDED-SKIP", "UNGROUNDED", "CONFLICT"])

    def test_an_html_comment_is_provenance_not_the_claim(self):
        # An honest correction quotes what it corrected, so a header can carry the word
        # NOASSERTION in a comment while asserting AGPL-3.0. Without stripping, the
        # accurate header reports as an asserted absence.
        header = ("AGPL-3.0  <!-- full license text added upstream 2026-07-12; the "
                  "header froze at the pre-detection NOASSERTION reading -->")
        finds, _, compared = self._run([("r", "o/r", header)],
                                       {"o/r": self._rec("AGPL-3.0")})
        self.assertEqual(finds, [])
        self.assertEqual(compared, 1)
        ev = audit.Evaluation("r", f"**License:** {header}\n")
        self.assertEqual(ev.license_header, "AGPL-3.0")

    def test_live_tree_has_no_ungrounded_skip(self):
        # Pins the repair: no live SKIP rests on an absence the record refutes.
        finds, _, _ = audit.audit_license_header(audit.DetectorContext(ROOT))
        self.assertEqual([f.name for f in finds if f.kind == "UNGROUNDED-SKIP"], [])

    def test_ungrounded_sorts_ahead_of_conflict(self):
        # Only the first can invalidate a disposition; a reader should meet it first.
        finds, _, _ = self._run(
            [("aaa", "o/aaa", "MIT"), ("zzz", "o/zzz", "no license")],
            {"o/aaa": self._rec("Apache-2.0"), "o/zzz": self._rec("MIT")})
        self.assertEqual([f.kind for f in finds], ["UNGROUNDED", "CONFLICT"])

    def test_a_header_naming_two_licenses_agrees_with_either(self):
        # `Apache-2.0 (docs CC-BY-4.0)` licenses code and prose differently and the
        # record can only hold one. Comparing a single "first family found" made this a
        # finding against a record naming one of the two it declares.
        finds, _, _ = self._run([("a", "o/a", "Apache-2.0 (docs CC-BY-4.0)")],
                                {"o/a": self._rec("Apache-2.0")})
        self.assertEqual(finds, [])

    def test_family_comparison_ignores_spelling_but_not_obligation(self):
        for header, spdx, conflict in (("MIT License", "MIT", False),
                                       ("mit", "MIT", False),
                                       ("Apache License 2.0", "Apache-2.0", False),
                                       ("AGPL-3.0", "GPL-3.0", True),
                                       ("CC-BY-4.0", "CC-BY-SA-4.0", True),
                                       ("LGPL-3.0", "GPL-3.0", True)):
            finds, _, _ = self._run([("a", "o/a", header)], {"o/a": self._rec(spdx)})
            self.assertEqual(bool(finds), conflict, f"{header!r} vs {spdx!r}")

    def test_an_unreadable_record_is_never_a_ground_to_contradict(self):
        # NONE means "no LICENSE *file*" (#372, detector Z's territory), 404 means
        # unreachable, NOASSERTION means unparsed. Re-reporting them here would put Z's
        # rows on a second scoreboard.
        for spdx in ("NONE", "NOASSERTION", "404"):
            finds, _, compared = self._run([("a", "o/a", "MIT")], {"o/a": self._rec(spdx)})
            self.assertEqual((finds, compared), ([], 0), spdx)

    def test_a_vague_header_is_an_honest_non_answer_not_a_conflict(self):
        # check-stars.py's rule: grading these would fail every legitimately-`n/a` field
        # and pressure authors into inventing a value. `NOASSERTION` is different — it is
        # a positive, checkable claim, which is why it lands in UNGROUNDED above.
        for header in ("n/a", "N/A", "unknown", "unspecified", "TBD", "—"):
            finds, _, compared = self._run([("a", "o/a", header)], {"o/a": self._rec("MIT")})
            self.assertEqual(finds, [], header)
            self.assertEqual(compared, 1, header)

    def test_a_redirected_record_is_printed_never_counted(self):
        # The record describes the DESTINATION. Counting it would pressure a human to
        # copy a known-false fact into a header — detector V's rule inverted.
        finds, redir, compared = self._run(
            [("a", "old/a", "n/a")], {"old/a": self._rec("MIT", "other/thing")})
        self.assertEqual(finds, [])
        self.assertEqual([(f.name, f.slug, f.spdx) for f in redir],
                         [("a", "other/thing", "MIT")])
        self.assertEqual(compared, 0)

    def test_a_rename_within_one_owner_is_not_a_redirect(self):
        # Same owner renaming their own repo still describes this row; only a change of
        # OWNER means the facts may belong to a different project.
        finds, redir, _ = self._run(
            [("a", "o/old", "no license")], {"o/old": self._rec("MIT", "o/new")})
        self.assertEqual(redir, [])
        self.assertEqual([f.kind for f in finds], ["UNGROUNDED"])

    def test_an_eval_with_no_license_header_is_skipped(self):
        finds, _, compared = self._run([("a", "o/a", None)], {"o/a": self._rec("MIT")})
        self.assertEqual((finds, compared), ([], 0))

    def test_a_missing_cache_yields_zero_compared_not_zero_findings(self):
        # V's rule: absence of the record file means "not collected", never "everything
        # agrees". The headline states the comparable count for exactly this reason.
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "evaluations"), exist_ok=True)
            _write(d, "COMPARISON.md", "# T\n")
            self.assertEqual(audit.audit_license_header(audit.DetectorContext(d)),
                             ([], [], 0))

    def test_the_header_field_is_read_mid_line(self):
        # `**License:**` shares a pipe-separated line with `**Stars:**` and
        # `**Last updated:**`, so a start-of-line anchor finds nothing at all — which is
        # what made a first pass report 630 evals as having no license header.
        ev = audit.Evaluation("x", "**Stars:** 12 | **Last updated:** 2026-01-01 | "
                                   "**License:** Apache-2.0\n")
        self.assertEqual(ev.license_header, "Apache-2.0")
        self.assertIsNone(audit.Evaluation("x", "no header here\n").license_header)

    def test_live_findings_are_well_formed_and_never_rest_on_an_unreadable_record(self):
        # Structural, not a pinned backlog count: a human fixes these one at a time and a
        # count assertion would fail the build for the fix (detector U's rule — pin the
        # buckets that must stay at zero, never the bucket a human resolves).
        finds, redir, compared = audit.audit_license_header(audit.DetectorContext(ROOT))
        self.assertTrue(compared)
        self.assertTrue(all(f.kind in ("UNGROUNDED", "CONFLICT") for f in finds))
        self.assertTrue(all(f.spdx not in audit.UNREADABLE_SPDX and f.spdx for f in finds))
        self.assertEqual({f.name for f in finds} & {f.name for f in redir}, set())


class TestDuplicateEvals(unittest.TestCase):
    """Pins detector AD (#412). Eight COMPARISON rows have two eval files, and three
    resolve to the weaker one — `prisma`'s row reads `discovery-log` / `SOURCE-ONLY`
    ("a name with no eval") while `prisma-mcp.md` holds a written CONDITIONAL, so the
    queue asks for an evaluation that exists and detector D cannot see the mismatch."""

    def _run(self, rows, evals):
        """rows is (tool, verdict); evals is (name, verdict, evidence, mirror_names)."""
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "evaluations"), exist_ok=True)
            _write(d, "COMPARISON.md", "# T\n\n## Implement\n\n"
                   "| Tool | Type | Auto | Free | Evaluated | Evidence |\n"
                   "|---|---|---|---|---|---|\n" + "".join(
                       f"| {t} | tool | y | y | {v} | REVIEW |\n" for t, v in rows))
            for name, verdict, evidence, mirrors in evals:
                mirror = ""
                if mirrors:
                    mirror = ("\n## Catalog entry\n\n"
                              "| Name | Type | One-liner | Problem it solves | Overlaps with |\n"
                              "|---|---|---|---|---|\n" + "".join(
                                  f"| {m} | tool | does things | a problem | — |\n"
                                  for m in mirrors))
                _write(d, f"evaluations/{name}.md",
                       f"# Evaluation: {name}\n\n"
                       f"**Repo:** [{name}](https://github.com/o/{name})\n\n"
                       f"## How we tested it\n\n**Evidence:** {evidence}\n\nRead it.\n"
                       + (f"\n## Verdict\n\n**{verdict}**\n\nBecause.\n" if verdict else "")
                       + mirror)
            return audit.audit_duplicate_evals(audit.DetectorContext(d))

    def test_an_unlinked_mirror_claims_its_row(self):
        # #401's ruling in the shared identity path, and the fix #433 applied: a mirror
        # names the row its eval CLAIMS, link or no link. Before it, `prisma-mcp`'s bare
        # mirror granted nothing, the row fell through to the stub, and this same fixture
        # reported SHADOWED — the arrangement that made a bulk lane write "no eval file
        # existed before this pass" beside a 6 KB eval of the same tool.
        finds, _ = self._run(
            [("prisma", "discovery-log")],
            [("prisma", None, "SOURCE-ONLY", ["prisma"]),
             ("prisma-mcp", "CONDITIONAL", "REVIEW", ["prisma"])])
        self.assertEqual([(f.kind, f.row, f.resolved[0]) for f in finds],
                         [("DUPLICATE", "prisma", "prisma-mcp")])
        self.assertEqual(finds[0].shadows, [("prisma", None, "SOURCE-ONLY")])

    def test_a_comparison_document_does_not_claim_its_referenced_rows(self):
        # AD's own precision rule: an eval embedding MORE than one mirror row is a
        # comparison document whose rows are references, not claims. Widening the
        # single-row case must not fan an eval out across every tool it mentions —
        # `cost-observability` embeds tokencost, Infracost and abtop.
        finds, _ = self._run(
            [("tokencost", "CONDITIONAL"), ("abtop", "CONDITIONAL")],
            [("cost-observability", None, "REVIEW", ["tokencost", "abtop"]),
             ("abtop", "CONDITIONAL", "MEASURED", ["[abtop](https://github.com/o/abtop)"])])
        self.assertEqual(finds, [])

    def test_the_row_resolving_to_the_stronger_file_is_only_a_duplicate(self):
        # Still a finding — two evals of one tool — but the record itself is right, so it
        # must not be reported as a row that misreports. The stronger file wins here
        # because its mirror carries a LINK, so today's `name_aliases` can already read
        # it; that link is the only difference between this row and `prisma` above.
        finds, _ = self._run(
            [("sentry", "discovery-log")],
            [("sentry", None, "SOURCE-ONLY", ["sentry"]),
             ("sentry-mcp", "CONDITIONAL", "REVIEW",
              ["[sentry](https://github.com/o/sentry-mcp)"])])
        self.assertEqual([f.kind for f in finds], ["DUPLICATE"])

    def test_shadowed_sorts_ahead_of_duplicate(self):
        # Resolution is first-wins over filename order, so the weaker file only wins when
        # it sorts first — `m-zzz` before `n-zzz`. That is the arrangement in which the
        # row reports less than the tree holds, and it outranks a merely redundant pair.
        finds, _ = self._run(
            [("zzz", "discovery-log"), ("aaa", "discovery-log")],
            [("aaa", "SKIP", "REVIEW", ["aaa"]), ("aaa-two", "SKIP", "REVIEW", ["aaa"]),
             ("m-zzz", None, "SOURCE-ONLY", ["zzz"]), ("n-zzz", "SKIP", "REVIEW", ["zzz"])])
        self.assertEqual([f.kind for f in finds], ["SHADOWED", "DUPLICATE"])

    def test_one_eval_per_row_is_never_a_finding(self):
        finds, claimed = self._run(
            [("a", "ADOPT"), ("b", "SKIP")],
            [("a", "ADOPT", "RUN", ["a"]), ("b", "SKIP", "REVIEW", ["b"])])
        self.assertEqual(finds, [])
        self.assertEqual(claimed, 2)

    def test_a_multi_row_eval_is_a_comparison_document_not_a_claimant(self):
        # cost-observability embeds tokencost, Infracost and abtop. Without this rule it
        # reads as a second eval of abtop, which it is not.
        finds, _ = self._run(
            [("abtop", "CONDITIONAL")],
            [("abtop", "CONDITIONAL", "MEASURED", ["abtop"]),
             ("cost-observability", "CONDITIONAL", "RUN", ["tokencost", "abtop"])])
        self.assertEqual(finds, [])

    def test_an_ambiguous_key_claims_nothing(self):
        # `agent-skills` and `agentskills` collapse to one name_key — detector U's AMBIG
        # example — but are two distinct rows with two distinct evals. A key-only match
        # would report a duplicate that isn't one, so an ambiguous key resolves to
        # nothing rather than to a coin flip.
        finds, _ = self._run(
            [("agent-skills", "ADOPT"), ("agentskills", "ADOPT")],
            [("agent-skills-addyosmani", "ADOPT", "REVIEW", ["agent-skills"]),
             ("agentskills", "ADOPT", "REVIEW", ["agentskills"])])
        self.assertEqual(finds, [])

    def test_strength_ranks_a_verdict_above_evidence(self):
        # A file that reaches a verdict says more than one that merely looked harder;
        # SOURCE-ONLY-with-no-verdict is the weakest thing a claimant can be.
        with_verdict = audit.Evaluation("a", "## How we tested it\n\n**Evidence:** REVIEW\n"
                                             "\n## Verdict\n\n**SKIP**\n")
        without = audit.Evaluation("b", "## How we tested it\n\n**Evidence:** MEASURED\n")
        self.assertGreater(audit._claim_strength(with_verdict),
                           audit._claim_strength(without))

    def test_every_single_mirror_eval_answers_to_the_row_it_names(self):
        # The #433 identity fix stated as a live-tree invariant. An eval's mirror names
        # the row it CLAIMS; if the eval does not answer to that name, some OTHER file
        # resolves the row — which is how eight stubs got written beside eight evals.
        # Pinned structurally rather than by count: AD's remaining backlog is a human's
        # merge call, but a mirror that does not grant its own name is a code defect.
        for e in audit.DetectorContext(ROOT).evals:
            rows = e.catalog_rows
            if len(rows) != 1:
                continue
            self.assertIn(catalog_lib.name_key(rows[0].name), e.name_aliases,
                          f"{e.name} embeds a mirror naming {rows[0].name!r} but does "
                          "not answer to it")

    def test_live_findings_name_real_rows_and_distinct_claimants(self):
        # Structural, not a pinned backlog count: a human merges these one at a time.
        finds, claimed = audit.audit_duplicate_evals(audit.DetectorContext(ROOT))
        ctx = audit.DetectorContext(ROOT)
        self.assertTrue(claimed)
        for f in finds:
            self.assertIn(f.row, ctx.comparison_verdict_map)
            self.assertTrue(f.shadows)
            names = [f.resolved[0]] if f.resolved else []
            names += [s[0] for s in f.shadows]
            self.assertEqual(len(names), len(set(names)), f.row)


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
        finds, cleared, examined = audit.audit_scope(audit.DetectorContext(ROOT))
        self.assertEqual({f.tool for f in finds} & {c.tool for c in cleared}, set())
        for f in finds + cleared:
            self.assertIn(f.typ, audit.SCOPE_TYPES)
            self.assertTrue(f.phrase.strip(), f.tool)
        # THIS assertion is the one that was missing, and its absence is why W's outage
        # ran from #478 to #494 unnoticed. Everything above iterates `finds + cleared`,
        # so a detector returning nothing satisfied all of it VACUOUSLY — a test that
        # passes more easily the more broken the detector is, which is exactly the test
        # direction #443 caught in the counts hook.
        self.assertGreater(examined, 0,
                           "W examined no framework/platform lead — a silent outage "
                           "reads identically to a clean sweep")

    def test_a_wider_assign_return_cannot_silence_the_detector(self):
        """`triage.assign` gained a fourth return value in #478 and W unpacked three, so
        the ValueError landed in W's own `except` and it reported OK while examining
        nothing. Indexing rather than unpacking is what makes that unrepeatable."""
        import types as _t
        mod = audit._load_sibling("triage_bands", "triage.py")
        real = mod.assign
        try:
            mod.assign = lambda ctx: (*real(ctx), "a fifth value")
            _, _, examined = audit.audit_scope(audit.DetectorContext(ROOT))
            self.assertGreater(examined, 0, "a wider return must not empty the detector")
        finally:
            mod.assign = real
        self.assertIsInstance(mod, _t.ModuleType)


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

    # --- the subject of a shared slug (#465) -----------------------------------
    # A `license_declared` record is a fact about the REPO, and six catalog rows can sit
    # behind one. Reading "the first row" made the finding's tool, verdict and — through
    # the verdict's prose — its whole GROUNDED/RECORDED classification a function of
    # CATALOG.md's row order.

    def _pack_ctx(self, d, catalog=None, evals=()):
        os.makedirs(os.path.join(d, "evaluations"), exist_ok=True)
        _write(d, "CATALOG.md", catalog or (
            "## Plan\n\n" + self.HDR +
            "| [pack](https://github.com/o/pack) | skill | one | two | none |\n"
            "| [alpha](https://github.com/o/pack/tree/main/skills/alpha) | skill | o | t | none |\n"
            "| [beta](https://github.com/o/pack/tree/main/skills/beta) | skill | o | t | none |\n"))
        _write(d, "COMPARISON.md",
               "# Tool Comparison\n\n## Plan\n\n"
               "| Tool | Type | Auto | Free | Evaluated | Evidence |\n"
               "|------|------|------|------|-----------|----------|\n"
               "| pack | skill | | \u2713 | discovery-log | SOURCE-ONLY |\n"
               "| alpha | skill | | \u2713 | discovery-log | SOURCE-ONLY |\n"
               "| beta | skill | | \u2713 | SKIP | REVIEW |\n")
        for name, text in evals:
            _write(d, f"evaluations/{name}.md",
                   f"# Evaluation: {name}\n\n## Verdict\n\n{text}\n")
        _write(d, "repo-metadata.json", json.dumps(
            {"o/pack": {"license_spdx": "NONE", "archived": False,
                        "license_declared": {"spdx": "MIT", "where": "readme",
                                             "phrase": "## License MIT"}}}))
        return audit.DetectorContext(d)

    GROUND: ClassVar[str] = ("**SKIP** — no declared license. A skill is *vendored* into "
                             "the consuming repo, and text carrying no license grant "
                             "cannot be copied in.")

    def test_the_subject_is_the_row_whose_verdict_rests_on_the_license(self):
        # `beta` is the row the declaration refutes; `pack` and `alpha` are leads it
        # merely corrects. Reporting the pack would file the strongest kind Z has under
        # a row that never claimed anything.
        with tempfile.TemporaryDirectory() as d:
            ctx = self._pack_ctx(d, evals=[("beta", self.GROUND)])
            finds, _, _ = audit.audit_license_declared(ctx)
            self.assertEqual([(f.kind, f.tool, f.verdict) for f in finds],
                             [("GROUNDED", "beta", "SKIP")])

    def test_with_no_grounded_row_the_subject_is_the_one_naming_the_repo(self):
        # Nothing to refute, so the record is about the artifact — and among rows sharing
        # a slug the one linking the repo ROOT is the row that names it (detector X's
        # container test), never whichever came first.
        with tempfile.TemporaryDirectory() as d:
            finds, _, _ = audit.audit_license_declared(self._pack_ctx(d))
            self.assertEqual([(f.kind, f.tool) for f in finds], [("RECORDED", "pack")])

    def test_license_findings_do_not_depend_on_row_order(self):
        base = ("## Plan\n\n" + self.HDR +
                "| [pack](https://github.com/o/pack) | skill | one | two | none |\n"
                "| [alpha](https://github.com/o/pack/tree/main/skills/alpha) | skill | o | t | none |\n"
                "| [beta](https://github.com/o/pack/tree/main/skills/beta) | skill | o | t | none |\n")
        lines = base.splitlines(keepends=True)
        head = len(lines) - 3          # "## Plan", blank, and the two header lines
        flipped = "".join([*lines[:head], lines[head + 2], lines[head + 1], lines[head]])
        # Both branches: with a grounded row to find, and with none (the container path).
        for evals in ([("beta", self.GROUND)], []):
            with (tempfile.TemporaryDirectory() as d1,
                  tempfile.TemporaryDirectory() as d2):
                a = audit.audit_license_declared(self._pack_ctx(d1, evals=evals))
                b = audit.audit_license_declared(self._pack_ctx(d2, flipped, evals=evals))
                self.assertEqual(a, b, evals)

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


# ----------------------------------------------------------------- check-links.py + rewrite-doc-links.py
class TestInternalLinks(unittest.TestCase):
    """Pins the offline link gate (#437). Detector C spends ~450 network requests on the
    links this repo does not control and disclaims its own result; these are free,
    deterministic, and were never checked — 26 were dead."""

    def _w(self, d, rel, text):
        p = os.path.join(d, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        Path(p).write_text(text, encoding="utf-8")

    def test_a_dead_relative_link_is_a_finding(self):
        with tempfile.TemporaryDirectory() as d:
            self._w(d, "a.md", "see [the eval](evaluations/gone.md) for why\n")
            f = checklinks.broken_links(d)
            self.assertEqual([(x.path, x.target) for x in f], [("a.md", "evaluations/gone.md")])

    def test_a_live_relative_link_is_not(self):
        with tempfile.TemporaryDirectory() as d:
            self._w(d, "evaluations/here.md", "# here\n")
            self._w(d, "a.md", "see [the eval](evaluations/here.md)\n")
            self.assertEqual(checklinks.broken_links(d), [])

    def test_a_link_inside_a_fence_is_sample_text(self):
        # evaluations/server-github.md shows illustrative shell output containing a
        # markdown link. Flagging a healthy row costs more than missing a sick one.
        with tempfile.TemporaryDirectory() as d:
            self._w(d, "a.md", "```bash\n# -> \"[GitHub](.../servers-archived/src/github)\"\n```\n")
            self.assertEqual(checklinks.broken_links(d), [])

    def test_a_link_inside_an_inline_span_is_sample_text(self):
        # evaluations/docmd.md quotes llms.txt's own `- [title](url)` format.
        with tempfile.TemporaryDirectory() as d:
            self._w(d, "a.md", "writes an index of every page as `- [title](url)` plus descriptions\n")
            self.assertEqual(checklinks.broken_links(d), [])

    def test_a_template_placeholder_is_exempt(self):
        with tempfile.TemporaryDirectory() as d:
            self._w(d, "TEMPLATE.md", "| [{name}]({url}) | tool |\n")
            self.assertEqual(checklinks.broken_links(d), [])

    def test_absolute_and_anchor_targets_are_out_of_scope(self):
        # Anchors are a fuzzier question (slugification varies by renderer); this gate
        # answers exactly one — does the file exist.
        with tempfile.TemporaryDirectory() as d:
            self._w(d, "a.md", "[x](https://example.com/y) [y](#some-heading) [z](mailto:a@b.c)\n")
            self.assertEqual(checklinks.broken_links(d), [])

    def test_a_fragment_on_a_real_file_resolves(self):
        with tempfile.TemporaryDirectory() as d:
            self._w(d, "b.md", "# b\n")
            self._w(d, "a.md", "[b](b.md#a-heading)\n")
            self.assertEqual(checklinks.broken_links(d), [])

    def test_the_reported_label_survives_code_stripping(self):
        # The label comes off the ORIGINAL line: `` [`gone.md`](gone.md) `` would
        # otherwise be reported with an empty label.
        with tempfile.TemporaryDirectory() as d:
            self._w(d, "a.md", "see [`gone.md`](gone.md)\n")
            self.assertEqual(checklinks.broken_links(d)[0].text, "`gone.md`")

    def test_line_numbers_survive_a_fence(self):
        with tempfile.TemporaryDirectory() as d:
            self._w(d, "a.md", "intro\n```\nx\n```\n[dead](nope.md)\n")
            self.assertEqual(checklinks.broken_links(d)[0].line, 5)

    def test_check_flag_gates_and_bare_run_reports(self):
        # check-stars.py's split: the gate-vs-report call is one word in the Makefile.
        r = subprocess.run(["python3", "check-links.py"], cwd=ROOT,
                           capture_output=True, text=True, check=False)
        self.assertEqual(r.returncode, 0)
        r = subprocess.run(["python3", "check-links.py", "--check"], cwd=ROOT,
                           capture_output=True, text=True, check=False)
        self.assertEqual(r.returncode, 0, msg=r.stdout)

    def test_live_tree_has_no_dead_links(self):
        self.assertEqual([f"{x.path}:{x.line} -> {x.target}" for x in checklinks.broken_links(ROOT)], [])


class TestDocLinkRewrite(unittest.TestCase):
    """Pins the sync's depth-only link rewrite (#437). The bundle is copied verbatim, so
    a link whose target is outside the watch set lands in a tree it is not in."""

    def _repo(self, d):
        Path(d, "docs").mkdir(parents=True, exist_ok=True)
        Path(d, "CLAUDE.md").write_text("root only\n", encoding="utf-8")
        Path(d, "docs", "adr.md").write_text("adr\n", encoding="utf-8")
        dest = os.path.join(d, "plugin", "docs")
        os.makedirs(os.path.join(dest, "methodologies"), exist_ok=True)
        return dest

    def test_an_outside_the_bundle_link_is_repointed_at_the_repo(self):
        with tempfile.TemporaryDirectory() as d:
            dest = self._repo(d)
            Path(dest, "PLAYBOOK.md").write_text("see [CLAUDE.md](CLAUDE.md)\n", encoding="utf-8")
            rewritelinks.rewrite_tree(dest, d)
            self.assertIn(rewritelinks.BLOB + "CLAUDE.md", Path(dest, "PLAYBOOK.md").read_text())

    def test_a_parent_relative_target_resolves_from_the_source_location(self):
        with tempfile.TemporaryDirectory() as d:
            dest = self._repo(d)
            Path(dest, "methodologies", "m.md").write_text("[ADR](../docs/adr.md)\n", encoding="utf-8")
            rewritelinks.rewrite_tree(dest, d)
            self.assertIn(rewritelinks.BLOB + "docs/adr.md", Path(dest, "methodologies", "m.md").read_text())

    def test_a_link_inside_the_bundle_is_left_relative(self):
        with tempfile.TemporaryDirectory() as d:
            dest = self._repo(d)
            Path(dest, "CATALOG.md").write_text("cat\n", encoding="utf-8")
            Path(dest, "PLAYBOOK.md").write_text("see [CATALOG.md](CATALOG.md)\n", encoding="utf-8")
            rewritelinks.rewrite_tree(dest, d)
            self.assertEqual(Path(dest, "PLAYBOOK.md").read_text(), "see [CATALOG.md](CATALOG.md)\n")

    def test_a_link_broken_at_root_is_left_alone(self):
        # The sync fixes depth, not rot. Minting a URL for a file nobody has would let
        # the sync launder a dead link into a plausible-looking one — the exact defect
        # this issue opened with.
        with tempfile.TemporaryDirectory() as d:
            dest = self._repo(d)
            Path(dest, "WORKFLOW.md").write_text("[eval](evaluations/gone.md)\n", encoding="utf-8")
            rewritelinks.rewrite_tree(dest, d)
            self.assertEqual(Path(dest, "WORKFLOW.md").read_text(), "[eval](evaluations/gone.md)\n")

    def test_a_fragment_is_carried_onto_the_rewritten_url(self):
        with tempfile.TemporaryDirectory() as d:
            dest = self._repo(d)
            Path(dest, "P.md").write_text("[c](CLAUDE.md#integrity-audit)\n", encoding="utf-8")
            rewritelinks.rewrite_tree(dest, d)
            self.assertIn(rewritelinks.BLOB + "CLAUDE.md#integrity-audit", Path(dest, "P.md").read_text())

    def test_rewriting_is_idempotent(self):
        with tempfile.TemporaryDirectory() as d:
            dest = self._repo(d)
            Path(dest, "P.md").write_text("see [CLAUDE.md](CLAUDE.md)\n", encoding="utf-8")
            rewritelinks.rewrite_tree(dest, d)
            once = Path(dest, "P.md").read_text()
            self.assertEqual(rewritelinks.rewrite_tree(dest, d), 0)
            self.assertEqual(Path(dest, "P.md").read_text(), once)

    def test_a_fenced_link_is_never_rewritten(self):
        with tempfile.TemporaryDirectory() as d:
            dest = self._repo(d)
            Path(dest, "P.md").write_text("```\n[c](CLAUDE.md)\n```\n", encoding="utf-8")
            rewritelinks.rewrite_tree(dest, d)
            self.assertEqual(Path(dest, "P.md").read_text(), "```\n[c](CLAUDE.md)\n```\n")

    def test_sync_runs_the_rewrite(self):
        # Lockstep: the rewrite must be part of the sync, not a step someone remembers.
        src = Path(ROOT, "sync-plugin-docs.sh").read_text(encoding="utf-8")
        self.assertIn("rewrite-doc-links.py", src)
        self.assertLess(src.index("rewrite-doc-links.py"), src.index("--- Skills:"),
                        "the rewrite must run after the docs copy loop")


# ----------------------------------------------------------------- check-plugin.py
class TestPluginPackage(unittest.TestCase):
    """Pins the offline structural check on the published plugin (#439). `claude plugin
    validate` is the upstream authority; this mirrors what is checkable from the tree,
    plus the cross-file agreements upstream cannot know about."""

    MARKET: ClassVar[dict] = {
        "name": "m", "owner": {"name": "N"}, "metadata": {"description": "d"},
        "plugins": [{"name": "ai-tooling", "version": "1.0.0", "source": "./plugin",
                     "description": "d"}]}
    MANIFEST: ClassVar[dict] = {"name": "ai-tooling", "description": "d", "version": "1.0.0"}

    def _tree(self, d, market=None, manifest=None, skills=("setup-workflow",),
              front="## Skills\n\n- `/setup-workflow` — bootstrap\n"):
        os.makedirs(os.path.join(d, ".claude-plugin"), exist_ok=True)
        os.makedirs(os.path.join(d, "plugin", ".claude-plugin"), exist_ok=True)
        Path(d, ".claude-plugin", "marketplace.json").write_text(
            json.dumps(self.MARKET if market is None else market), encoding="utf-8")
        if manifest is not None:
            Path(d, "plugin", ".claude-plugin", "plugin.json").write_text(
                json.dumps(manifest), encoding="utf-8")
        for s in skills:
            os.makedirs(os.path.join(d, "plugin", "skills", s), exist_ok=True)
            Path(d, "plugin", "skills", s, "SKILL.md").write_text(
                f"---\nname: {s}\ndescription: does a thing\n---\n\n# {s}\n", encoding="utf-8")
        if front is not None:
            Path(d, "plugin", "README.md").write_text(front, encoding="utf-8")

    def _kinds(self, d):
        return sorted(f.kind for f in checkplugin.audit_plugin(d))

    def test_a_well_formed_package_is_clean(self):
        with tempfile.TemporaryDirectory() as d:
            self._tree(d, manifest=self.MANIFEST)
            self.assertEqual(checkplugin.audit_plugin(d), [])

    def test_a_missing_plugin_manifest_is_a_finding(self):
        # The exact failure `claude plugin validate ./plugin` reported: the plugin dir
        # had skills, hooks and docs but no .claude-plugin/plugin.json.
        with tempfile.TemporaryDirectory() as d:
            self._tree(d, manifest=None)
            self.assertIn("MANIFEST", self._kinds(d))

    def test_unparseable_json_is_a_finding_not_a_traceback(self):
        with tempfile.TemporaryDirectory() as d:
            self._tree(d, manifest=self.MANIFEST)
            Path(d, "plugin", ".claude-plugin", "plugin.json").write_text("{oops", encoding="utf-8")
            self.assertIn("MANIFEST", self._kinds(d))

    def test_a_name_disagreement_is_a_finding(self):
        with tempfile.TemporaryDirectory() as d:
            self._tree(d, manifest={**self.MANIFEST, "name": "something-else"})
            self.assertIn("NAME", self._kinds(d))

    def test_versions_must_agree_across_every_declaration(self):
        with tempfile.TemporaryDirectory() as d:
            self._tree(d, manifest={**self.MANIFEST, "version": "2.0.0"})
            self.assertIn("VERSION", self._kinds(d))

    def test_a_reintroduced_package_json_is_a_third_place_to_drift(self):
        # #439 deleted plugin/package.json — an npm manifest for a registry this package
        # is not published to. If one comes back, its version is checked, not ignored.
        with tempfile.TemporaryDirectory() as d:
            self._tree(d, manifest=self.MANIFEST)
            Path(d, "plugin", "package.json").write_text('{"name":"x","version":"9.9.9"}', encoding="utf-8")
            self.assertIn("VERSION", self._kinds(d))

    def test_a_source_pointing_nowhere_is_a_finding(self):
        with tempfile.TemporaryDirectory() as d:
            market = json.loads(json.dumps(self.MARKET))
            market["plugins"][0]["source"] = "./nope"
            self._tree(d, market=market, manifest=self.MANIFEST)
            self.assertIn("SOURCE", self._kinds(d))

    def test_source_resolves_from_the_repo_root(self):
        # `./plugin` means <repo>/plugin, not <repo>/.claude-plugin/plugin — reading it
        # the other way reported a healthy package as broken.
        with tempfile.TemporaryDirectory() as d:
            self._tree(d, manifest=self.MANIFEST)
            self.assertNotIn("SOURCE", self._kinds(d))

    def test_a_skill_whose_frontmatter_name_differs_is_a_finding(self):
        # The registry keys skills by frontmatter `name:`, not by directory.
        with tempfile.TemporaryDirectory() as d:
            self._tree(d, manifest=self.MANIFEST)
            Path(d, "plugin", "skills", "setup-workflow", "SKILL.md").write_text(
                "---\nname: renamed\ndescription: d\n---\n", encoding="utf-8")
            self.assertIn("SKILL", self._kinds(d))

    def test_a_skill_missing_description_is_a_finding(self):
        with tempfile.TemporaryDirectory() as d:
            self._tree(d, manifest=self.MANIFEST)
            Path(d, "plugin", "skills", "setup-workflow", "SKILL.md").write_text(
                "---\nname: setup-workflow\n---\n", encoding="utf-8")
            self.assertIn("SKILL", self._kinds(d))

    def test_the_front_door_skills_list_must_match_the_tree(self):
        # plugin/README.md is hand-authored, so its skills list is a restated fact with no
        # generator — the shape that put its eval count 87 behind (#302).
        with tempfile.TemporaryDirectory() as d:
            self._tree(d, manifest=self.MANIFEST, skills=("setup-workflow", "audit-workflow"))
            self.assertEqual(self._kinds(d), ["FRONT-DOOR"])   # audit-workflow unlisted

    def test_a_listed_skill_that_does_not_exist_is_a_finding(self):
        with tempfile.TemporaryDirectory() as d:
            self._tree(d, manifest=self.MANIFEST,
                       front="- `/setup-workflow` — x\n- `/ghost` — never shipped\n")
            self.assertEqual(self._kinds(d), ["FRONT-DOOR"])

    def test_a_claude_md_back_at_the_plugin_root_is_the_mistake_returning(self):
        # `claude plugin validate` warns that Claude Code never loads it, which is why
        # the front door is README.md (#441). A reappearing CLAUDE.md is a finding, not
        # a second front door.
        with tempfile.TemporaryDirectory() as d:
            self._tree(d, manifest=self.MANIFEST)
            Path(d, "plugin", "CLAUDE.md").write_text("# ai-tooling Plugin\n", encoding="utf-8")
            self.assertIn("FRONT-DOOR", self._kinds(d))

    def test_the_plugin_ships_a_readme(self):
        # The plugin docs name README.md as the documented place for install and usage
        # instructions, and it is what GitHub renders when someone opens plugin/.
        readme = Path(ROOT, "plugin", "README.md").read_text(encoding="utf-8")
        self.assertIn("claude plugin marketplace add", readme)
        self.assertFalse(os.path.exists(os.path.join(ROOT, "plugin", "CLAUDE.md")))

    def test_check_flag_gates_and_bare_run_reports(self):
        r = subprocess.run(["python3", "check-plugin.py"], cwd=ROOT,
                           capture_output=True, text=True, check=False)
        self.assertEqual(r.returncode, 0)
        r = subprocess.run(["python3", "check-plugin.py", "--check"], cwd=ROOT,
                           capture_output=True, text=True, check=False)
        self.assertEqual(r.returncode, 0, msg=r.stdout)

    def test_live_package_is_clean(self):
        self.assertEqual([f"{f.kind} {f.detail}" for f in checkplugin.audit_plugin(ROOT)], [])

    def test_readme_install_commands_use_real_subcommands(self):
        # Both README commands were invented (`claude plugins:add-marketplace`), and
        # `claude` accepts an unrecognized first arg AS A PROMPT — so the broken command
        # launches a session instead of erroring, which is why it survived.
        readme = Path(ROOT, "README.md").read_text(encoding="utf-8")
        self.assertNotIn("plugins:", readme)
        self.assertIn("claude plugin marketplace add", readme)
        self.assertIn("claude plugin install", readme)
