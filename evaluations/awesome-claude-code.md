# Evaluation: awesome-claude-code

**Repo:** [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)
**Stars:** 52,881 | **Last updated:** 2026-08-24 (last push) | **License:** CC-BY-NC-ND-4.0 <!-- declared in LICENSE as plain prose; GitHub's licensee records NOASSERTION -->
**Last verified:** 2026-08-23
**Dev loop stage:** Discover (outer loop)
**Layer:** Infrastructure

---

## What it does

A curated catalog of Claude Code resources — skills, hooks, slash-commands, agent orchestrators, developer tooling, observability stacks, status lines, and alternative clients. The data lives in a structured CSV (`THE_RESOURCES_TABLE_NEW.csv`) with 12 columns per entry: display name, category, sub-category, link, author, `Active`/`Stale` flags, `Date Added`, `Last Checked`, and a hand-written description. Pre-rendered README variants in `README_ALTERNATIVES/` provide category- and sort-specific views, and `generate_readme.py` builds the front page from the CSV.

The editorial voice is the distinguishing feature — each entry gets a hand-written review rather than the repo's own tagline, often explaining *why* a tool is good or what makes it unusual. That is rare for an awesome list, and it is also what the licence protects (below).

## How we tested it

**Evidence:** RUN

Fetched the live data and **measured the one number the previous review claimed but never reported** — it said it "compared entry overlap with our catalog" and gave no figure. This run computes it, by GitHub slug rather than by display name (the identity discipline `CLAUDE.md` applies everywhere else), and re-checks the two freshness claims the old verdict rested on.

```bash
gh api repos/hesreallyhim/awesome-claude-code --jq '.stargazers_count, .pushed_at, .license.spdx_id'
gh api repos/hesreallyhim/awesome-claude-code/git/trees/main --jq '.tree[].path'
gh api repos/hesreallyhim/awesome-claude-code/contents/THE_RESOURCES_TABLE_NEW.csv --jq '.content' | base64 -d > table.csv
# then: csv.DictReader -> category/Active/Date Added tallies; slug-join against CATALOG.md
```

**1. The previous eval's own re-evaluation trigger has fired.** Its verdict read: *"the 2-month content freeze and gutted README drop it from ADOPT… Re-evaluate if the reorganization completes and regular updates resume."* Both conditions are met. The README is no longer *"just TODO"* — it is a full, banner-headed page explaining that the current iteration was relaunched deliberately to feature resources **not** on the previous one, with legacy entries preserved under `README_ALTERNATIVES/`. And `Date Added` shows **20 entries in 2026-08**, 30 in 2026-07, 66 in 2026-06 — the freeze is over.

**2. The reproduction command in the old eval is dead.** `THE_RESOURCES_TABLE.csv` **404s**; the file is now `THE_RESOURCES_TABLE_NEW.csv`, and the shape changed with the rename: **226 entries / 20 columns → 157 entries / 12 columns**. The activity columns survived (`Active`, `Stale`); the licence-detection and release-tracking columns did not.

**3. Overlap with this catalog: 30 of 142 — 21%.** Of 157 entries, 142 resolve to a distinct GitHub `owner/repo` (15 link elsewhere). Thirty are already linked somewhere in `CATALOG.md`; **112 are not.**

| | count |
|---|---|
| entries | 157 |
| distinct GitHub slugs | 142 |
| already in `CATALOG.md` | **30 (21%)** |
| **not catalogued here** | **112** |
| `Active: TRUE` | 148 of 157 |

The 21% is low *because* of finding 1 — the list was rebuilt to surface work its earlier iteration did not carry, which is exactly the property that makes it a high-yield gap source rather than a redundant one. Spot-checks confirm the join is honest rather than an extraction artifact: `anthropics/claude-code-security-review` (Anthropic's own), `colemurray/claude-code-otel` and `ctxlint/ctxlint` are genuinely absent from both `CATALOG.md` and `evaluations/`.

**4. The licence is CC BY-NC-ND 4.0, and the record understates it.** `repo-metadata.json` and GitHub both read `NOASSERTION` because the `LICENSE` file states the grant in prose rather than in a form licensee parses — **detector Z's exact case**, an absence that is not an absence. It matters here in a specific way, because the way this repo would *use* the list is to mine it: **NoDerivatives** covers the curated selection and the hand-written descriptions, and the maintainer says so directly in the file — *"if you are interested in making a project that utilizes this list in a modified form, you are welcome to contact the maintainer."*

**Not exercised:** `generate_readme.py`, the `ticker/` pipeline, the `tests/` suite, and the accuracy of the `Active`/`Last Checked` flags against the linked repos (46 entries carry no `Last Checked` date at all). Nothing here claims the 148 `Active: TRUE` entries were independently verified as live.

## Test design

- **Task/corpus:** the live `THE_RESOURCES_TABLE_NEW.csv` (157 rows) joined against every `github.com/owner/repo` link in `CATALOG.md` (742 distinct slugs).
- **Baseline:** the previous `REVIEW` eval's written claims — 226 entries / 20 columns, "README is gutted… just says TODO", "no new entries in ~2 months", and an unquantified overlap comparison.
- **Metric:** entry count, column count, category and `Date Added` tallies, and the slug-join overlap as `n/total`.
- **Reproduce:** the command block above, plus a `csv.DictReader` join. Deterministic, no API key beyond `gh` auth.
- **Identity rule:** joined on lowercased `owner/repo` extracted from the link, **never** on display name — a name-keyed join is the error this repo has fixed four times (#343 / #366 / #374 / #413), and the catalog side is deliberately generous (any link anywhere in the file counts, per `freshness.py`'s rule) so an already-examined repo is not re-offered as a gap.

## What worked

- **It is a high-yield lead source, measured: 112 uncatalogued repos**, including one published by Anthropic. That is a concrete number this catalog can act on, and it is the value the previous review asserted without quantifying.
- **It is actively maintained again** — 20 additions this month, the README rebuilt, `Active`/`Stale` flags carried forward.
- **Editorial quality remains the distinguishing feature.** Hand-written evaluative descriptions, not repo taglines.
- **Structured CSV makes it programmatically queryable**, which is what made this whole measurement a fifteen-minute job rather than a reading exercise.
- **Category coverage is complementary rather than overlapping** — 23 Observability & Monitoring, 16 Security, 8 Remote Control / Notifications / Voice I/O, 3 Status Lines. These are Claude-Code-specific slices a general AI-tooling catalog covers thinly.

## What didn't work or surprised us

- **The licence is the real adoption constraint, and nothing in this repo had noticed it.** CC BY-NC-ND 4.0 recorded as `NOASSERTION`. Reading the list imposes nothing; **reproducing its curated text does.** Facts (a tool exists, at this URL) are not copyrightable and can be mined freely; the selection and the descriptions are the author's work.
- **The rename silently broke the old eval's reproduction command**, and shrank the dataset by 69 entries and 8 columns. An eval that quotes a raw file path is one rename from being unreproducible — this one was.
- **The list got smaller, not bigger.** 226 → 157. Legacy entries are preserved but frozen in `README_ALTERNATIVES/`, so "the list" now means two datasets with different freshness guarantees.
- **`Last Checked` is incomplete** — 46 of 157 entries carry no date, so the `Active: TRUE` flag on those rests on the entry never having been re-checked.
- **Nine entries are already `Active: FALSE`** and still listed, which is honest bookkeeping rather than a defect, but means the list is not pre-filtered for you.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Reference list — no effect on code quality |
| Speed | + | Hand-written evaluative descriptions save repo-by-repo triage; the CSV made a 142-slug overlap join a single script |
| Maintainability | neutral | No impact on code |
| Safety | + / - | `Active`/`Stale` flags surface dead repos — but 46 entries have never been re-checked, and 9 known-inactive entries remain listed |
| Cost Efficiency | + | Structured CSV enables programmatic querying instead of manual reading |
| Verifiability | + | Every claim here is a count over a file anyone can re-fetch; the previous review's overlap claim was unverifiable precisely because it carried no number |

## Verdict

**CONDITIONAL** — adopt-if: you use it as a **pointer list** — mining the links and writing your own descriptions — rather than reproducing its curated text.

That gate is the licence, not a quality reservation. CC BY-NC-ND 4.0 (recorded upstream as `NOASSERTION`, so nothing in this repo was tracking it) covers the selection and the hand-written reviews; the bare facts it points at do not belong to anyone. For this catalog that is a workable arrangement and worth stating explicitly, because the natural way to use a list like this — copy the row, adjust the wording — is the one use the licence singles out.

On the merits it now clears the bar the previous verdict set for itself. That verdict withheld ADOPT over a content freeze and a gutted README and said to *"re-evaluate if the reorganization completes and regular updates resume"*; both have. **112 of its 142 GitHub-linked entries are absent from this catalog** — the highest-yield discovery source measured here — and its strongest categories (Observability, Security, Remote Control, Status Lines) are the ones this catalog covers most thinly.

Two caveats for whoever mines it: the dataset was renamed and cut from 226 entries to 157, with the remainder frozen under `README_ALTERNATIVES/`; and `Active: TRUE` is not a liveness guarantee, since 46 entries have no `Last Checked` date.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | reference | Curated, editorially-reviewed Claude Code resources in a queryable CSV (53K stars; CC-BY-NC-ND) | Hard to discover what's available in the Claude Code ecosystem | awesome-claude-skills (travisvn), awesome-claude-skills (Composio) |
