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

    def test_fix_eval_strings_both_variants(self):
        self.assertEqual(reconcile.fix_eval_strings("distilled from 471 evaluations.", 487),
                         "distilled from 487 evaluations.")
        self.assertEqual(reconcile.fix_eval_strings("471 evidence-based evaluations here", 487),
                         "487 evidence-based evaluations here")

    def test_fix_eval_strings_ignores_unrelated_numbers(self):
        # The regex is anchored on "evaluations"; issue refs / bare counts are left alone.
        s = "see issue 471 and 12 tools cataloged"
        self.assertEqual(reconcile.fix_eval_strings(s, 487), s)


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


# ----------------------------------------------------------------- detector G (audit_comparison)
class TestDetectorG(unittest.TestCase):
    def _run_audit(self, catalog, comparison):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "CATALOG.md", catalog)
            _write(d, "COMPARISON.md", comparison)
            return audit.audit_comparison(audit.DetectorContext(d))

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
    shutil.copy(os.path.join(ROOT, "catalog_lib.py"), os.path.join(d, "catalog_lib.py"))  # verify block imports it
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
        self.assertIn("| Stage | Tools | Evaluated | Adoption rate |", cmp6)
        # body counts unchanged -> detector G / reconcile see the same rows
        self.assertEqual(reconcile.comparison_body_counts(cmp6), {"Plan": 2, "Ship": 1})
        self.assertEqual(backfill.rebuild_comparison(cmp6, {}), cmp6)  # idempotent
        with tempfile.TemporaryDirectory() as d:
            _write(d, "CATALOG.md", CATALOG_OK)
            _write(d, "COMPARISON.md", cmp6)
            # G still clean with the new column
            self.assertEqual(audit.audit_comparison(audit.DetectorContext(d)), [])


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
