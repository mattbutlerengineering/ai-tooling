# Plan 015: Stop hand-written numbers from going stale inside derived surfaces

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md`.
>
> **Drift check (run first)**:
> `git diff --stat a388dd2..HEAD -- reconcile-counts.py triage.py plugin/CLAUDE.md plugin/hooks/validate-counts.sh CLAUDE.md NEXT-EVALS.md test_automation.py`
> If any of those changed since this plan was written, compare the
> "Current state" excerpts against the live code before proceeding; on a
> mismatch, treat it as a STOP condition.

## Status

- **Priority**: P2
- **Effort**: M
- **Risk**: LOW
- **Depends on**: none
- **Category**: bug
- **Planned at**: commit `a388dd2`, 2026-08-03

## Why this matters

This repo's stated rule is "**Never hand-edit counts**" (`CLAUDE.md`), enforced by
`reconcile-counts.py` and detector G. Three places quietly violate it, and one of them is
crying wolf on every edit right now:

1. **`plugin/CLAUDE.md:18` says `469` evaluation files; the real number is `556`.** That file
   *is* already in `reconcile-counts.py`'s `FILES_TOTAL`, so the count looks maintained — but
   neither `EVAL_PATTERNS` regex matches its phrasing ("evaluation and comparison files"
   rather than "evaluations"), so it has been silently skipped and has drifted by 87.

   The two daily-discovery commits between `1b46c82` and `a388dd2` demonstrate the bug in
   miniature: `reconcile-counts.py` updated the **catalog** count on line 17 from `620` to
   `634`, while the **eval** count on line 18 stayed frozen at `469`. One maintained number
   and one abandoned number, in adjacent lines, updated by the same script in the same run.
   That adjacency is exactly what makes the stale one deceptive to a reader.

2. **`plugin/hooks/validate-counts.sh` reports a false failure today.** Running it right now
   prints `README.md says 556 eval files but evaluations/ has 557`. README is correct; the
   hook is wrong. It counts `evaluations/*.md` including `TEMPLATE.md`, while
   `reconcile-counts.py`'s `eval_count()` deliberately excludes the template. A hook that
   reports drift when there is none trains the maintainer to ignore it — the worst possible
   state for a hook whose entire job is to be believed.

3. **`triage.py` prints stale hand-typed statistics into a generated page.** `NEXT-EVALS.md`
   is a derived file nobody may edit by hand, yet line 5 of it reads "that score only has ~83
   distinct values" — a number typed into `triage.py:233` months ago. The real values today
   are **104** distinct scores, largest tie **36**, **187** zero-pressure leads, **476** total
   leads; the docstring and `CLAUDE.md` repeat the same four stale numbers. A derived page
   asserting a hand-typed stale statistic undermines the credibility of every other number on
   it.

   These four figures moved *while this plan was being written* — 105/37/180/465 at
   `1b46c82` became 104/36/187/476 two commits later. That is the argument for the fix in one
   observation: any figure typed into a generator's output is wrong within days.

None of these is dangerous on its own. Together they are the specific failure mode this
repo's entire automation layer exists to prevent, occurring inside that automation layer.

## Current state

### Finding 1 — the eval-count pattern that does not match

`plugin/CLAUDE.md:16-18`:

```markdown
- `CATALOG.md` — flat inventory of 634 tools across 13 categories with overlap markers
- `WORKFLOW.md` — inner/outer dev loop stages, tools per stage, quality signals, adoption guide
- `evaluations/` — 469 evidence-based evaluation and comparison files
```

(The `634` on the first line was rewritten by `reconcile-counts.py` two commits ago. The `469`
on the third was not. Same file, same script, same run.)

`reconcile-counts.py:33-38` — the derived count, which excludes the template:

```python
def eval_count(root=None):
    # Derived eval-file count: every evaluations/*.md except the TEMPLATE.
    # `root` is injectable for tests, mirroring catalog_count().
    files = glob.glob(os.path.join(root or ROOT, "evaluations", "*.md"))
    return sum(1 for f in files if os.path.basename(f) != "TEMPLATE.md")
```

`reconcile-counts.py:54-59` — the patterns that miss it:

```python
EVAL_PATTERNS = [
    (r"\b\d+( evidence-based evaluations)", r"{E}\g<1>"),
    (r"\b\d+( evaluations)", r"{E}\g<1>"),
]
```

`reconcile-counts.py:135` — `plugin/CLAUDE.md` is already in the file list:

```python
FILES_TOTAL = ["README.md", "CLAUDE.md", "STACK.md", "plugin/CLAUDE.md"]
```

Verified: `re.search(r"\b\d+( evidence-based evaluations)", "- `evaluations/` — 469 evidence-based evaluation and comparison files")`
is `False`, and so is the second pattern. The comment above `EVAL_PATTERNS` says the patterns
are "Anchored on the word 'evaluations' so unrelated numbers (issue refs, dates) are never
touched" — that intent is right and must be preserved by any new pattern.

### Finding 2 — the hook's off-by-one

`plugin/hooks/validate-counts.sh:43-50`:

```bash
# Count actual evaluation files
actual_evals=$(ls "$REPO_ROOT/evaluations/"*.md 2>/dev/null | wc -l | tr -d ' ')

# Check README.md eval count
readme_evals=$(num_before "evidence" "$README")
if [ -n "$readme_evals" ] && [ "$readme_evals" != "$actual_evals" ]; then
  issues="${issues}README.md says $readme_evals eval files but evaluations/ has $actual_evals\n"
fi
```

Running `bash plugin/hooks/validate-counts.sh` at `a388dd2` prints:

```
⚠️  ai-tooling: count drift detected
README.md says 556 eval files but evaluations/ has 557
Actual: 634 catalog entries, 557 evaluation files
```

`README.md:32` reads `- [evaluations/](evaluations/) — 556 evidence-based evaluations with verdicts (ADOPT/CONDITIONAL/SKIP)`
and is correct. `ls evaluations/*.md | wc -l` is 557; excluding `TEMPLATE.md` it is 556. The
gap is always exactly 1 — the template — so the hook has been wrong every single run.

The script's own header comment records that a previous portability bug made these checks
"a dead no-op" on macOS — so this check has likely been correct-and-loud only since that fix.

### Finding 3 — hand-typed statistics in a generated page

`triage.py:1-9` (module docstring):

```python
"""
triage.py — band the 461 `discovery-log` leads and regenerate NEXT-EVALS.md.

`next-evals.py` scores leads; this decides what may be *done* with each one. The
score alone cannot order the queue: 176 leads have zero overlap pressure and the
whole set collapses into ~83 distinct scores (largest tie: 45 tools), so below
roughly rank 100 a ranked table is alphabetical order wearing a costume. Bands are
honest about the resolution the signal actually has.
```

`triage.py:219-235` — `render()`, where the stale number is *emitted into the page*:

```python
def render(ordered, ranked):
    """NEXT-EVALS.md in full. Bands replace the old flat top-25 table; every band
    prints its true size, and any band listing only a sample says so — the repo's
    no-silent-caps rule."""
    total = len(ranked)
    lines = [
        "# Next evals — a banded promotion queue",
        "",
        f"The {total} `discovery-log` leads, **derived** (not hand-maintained) from data "
        "already in the repo plus `repo-metadata.json`. Regenerate with `python3 triage.py`; "
        "do not edit between the markers.",
        "",
        "Leads are grouped into **bands**, not a single ranked list. Within a band the order "
        "is `2*overlap_pressure + stage_gap_weight + evidence_bonus` (see `next-evals.py`), "
        "but that score only has ~83 distinct values across these leads — enough to pick a "
        "head, not to rank a tail. Leads already stamped `**Last triaged:**` sink within "
        "their band so each pass surfaces un-examined ones.",
```

Note `total` on the line above is computed correctly — only the "~83" is hardcoded, three
lines later, in the same string list.

`CLAUDE.md:107` repeats the same four numbers in prose: "176 leads have zero overlap pressure
and the set collapses into ~83 distinct values (largest tie: 45 tools)".

### The measured truth at `a388dd2`

Computed via `next-evals.py`'s `rank(ctx)` (each row is
`(score, name, stage, overlap_pressure, stage_gap_weight)`):

| Statistic | Written | Actual |
|---|---|---|
| total `discovery-log` leads | 461 (docstring) | **476** |
| leads with zero overlap pressure | 176 | **187** |
| distinct score values | ~83 | **104** |
| largest tie | 45 tools | **36** |

The `total` printed in `NEXT-EVALS.md`'s first paragraph is already correct (476) because it
is computed — which is precisely the fix pattern to extend.

### Repo conventions that apply

- Python 3, **stdlib only**; no type annotations; comments explain *why*.
- `CLAUDE.md`: "**Never hand-edit counts.** Run `python3 reconcile-counts.py`."
- Generated pages carry `START`/`END` markers and a "do not edit between the markers" line.
  Anything inside them must be computed, not typed.
- Tests live in `test_automation.py`, against fixtures in a temp dir. `TestReconcileMain` and
  the surrounding reconcile tests are the exemplars for finding 1's test.

## Commands you will need

| Purpose | Command | Expected on success |
|---------|---------|---------------------|
| Reconcile counts (apply) | `python3 reconcile-counts.py` | exit 0 |
| Reconcile counts (gate) | `python3 reconcile-counts.py --check` | exit 0, `reconcile: OK — …` |
| Regenerate the queue | `python3 triage.py` | exit 0 |
| Gate the queue | `python3 triage.py --check` | exit 0 |
| Run the counts hook | `bash plugin/hooks/validate-counts.sh` | exit 0, **no output** |
| Sync the plugin mirror | `./sync-plugin-docs.sh` | exit 0 |
| Unit suite | `python3 -m unittest -q test_automation` | exit 0 |
| Full gate | `make check` | exit 0 (detector A needs network + `gh` auth) |
| Full repair | `make fix` | exit 0 |

## Scope

**In scope** (the only files you should modify):

- `reconcile-counts.py` — `EVAL_PATTERNS` only
- `plugin/CLAUDE.md` — the eval count (via `reconcile-counts.py`, not by hand)
- `plugin/hooks/validate-counts.sh` — the `actual_evals` line
- `triage.py` — module docstring and `render()`
- `NEXT-EVALS.md` — regenerated, never hand-edited
- `CLAUDE.md` — the one prose sentence at line 107
- `test_automation.py` — new tests

**Out of scope** (do NOT touch, even though they look related):

- **`STACK.md`'s "The ~25 tools worth installing"** — this was checked and is **accurate**:
  26 unique GitHub slugs appear in STACK's install tables, and `STACK-LEDGER.md` records 22
  `yes` + 4 `conditional`. Do not "fix" it. The same phrase in `README.md:30` is likewise fine.
- `next-evals.py`'s scoring weights (`2*overlap_pressure + …`). This plan reports the score
  distribution accurately; it does not change it. Changing weights changes the queue order,
  which is a judgment call for a human.
- `catalog_count()` / `catalog_lib.catalog_count()` and the catalog total (634). Correct and
  maintained.
- `TOTAL_PATTERNS` in `reconcile-counts.py`. Only `EVAL_PATTERNS` is broken.
- Deleting `plugin/hooks/validate-counts.sh` because `make check` supersedes it. It runs at a
  different moment (post-edit, pre-commit) and that overlap is a design question, not a bug.

## Git workflow

- Branch: `advisor/015-derived-surface-numbers`
- Conventional commits — consider one commit per finding, e.g.
  `fix(reconcile): match plugin/CLAUDE.md's eval-count phrasing`,
  `fix(hooks): exclude TEMPLATE.md from the hook's eval count`,
  `fix(triage): compute the score-distribution stats instead of hardcoding them`
- Do NOT push or open a PR unless the operator instructed it.

## Steps

### Step 1: Reproduce all three findings

```sh
echo "--- finding 1: plugin/CLAUDE.md eval count"
grep -n "evidence-based evaluation" plugin/CLAUDE.md
ls evaluations/*.md | grep -v TEMPLATE | wc -l

echo "--- finding 2: the hook cries wolf"
bash plugin/hooks/validate-counts.sh

echo "--- finding 3: stale stats"
grep -n "~83 distinct" triage.py NEXT-EVALS.md CLAUDE.md
```

**Verify**: finding 1 shows `469` against an actual of `556`; finding 2 prints a
`count drift detected` block naming README; finding 3 shows three hits. If any does not
reproduce, STOP — that finding has already been fixed and its steps must be skipped, not
guessed at.

### Step 2 (finding 1): Teach `reconcile-counts.py` the plugin phrasing

Add a third pattern to `EVAL_PATTERNS`, **before** the two existing ones so the more specific
phrase wins (same ordering rationale the existing comment already states):

```python
EVAL_PATTERNS = [
    # plugin/CLAUDE.md phrases the same count as "N evidence-based evaluation and
    # comparison files". It has always been in FILES_TOTAL, but neither pattern below
    # matched that wording, so the number drifted 63 behind while the catalog count on
    # the line above it stayed correct — the most misleading kind of stale number.
    (r"\b\d+( evidence-based evaluation and comparison files)", r"{E}\g<1>"),
    (r"\b\d+( evidence-based evaluations)", r"{E}\g<1>"),
    (r"\b\d+( evaluations)", r"{E}\g<1>"),
]
```

Then apply it:

```sh
python3 reconcile-counts.py
```

**Verify**: `grep -n "evidence-based evaluation and comparison" plugin/CLAUDE.md` shows the
current eval count (556 at the time of writing, whatever `ls evaluations/*.md | grep -v TEMPLATE | wc -l`
prints now). `python3 reconcile-counts.py --check` → exit 0.

### Step 3 (finding 2): Align the hook's count with `eval_count()`

In `plugin/hooks/validate-counts.sh`, replace line 44:

```bash
# Count actual evaluation files. TEMPLATE.md is the eval *template*, not an eval —
# reconcile-counts.py's eval_count() excludes it, so this must too, or the hook reports
# a false off-by-one on a tree that is actually correct.
actual_evals=$(ls "$REPO_ROOT/evaluations/"*.md 2>/dev/null | grep -v '/TEMPLATE\.md$' | wc -l | tr -d ' ')
```

**Verify**: `bash plugin/hooks/validate-counts.sh; echo "rc=$?"` → **no output** and `rc=0`.

### Step 4 (finding 3): Compute the score-distribution stats in `render()`

`render(ordered, ranked)` already receives `ranked`, and each row's score is `row[0]` and its
overlap pressure is `row[3]` — everything needed is already in hand.

Compute the three statistics at the top of `render()`, next to the existing
`total = len(ranked)`:

```python
    total = len(ranked)
    # These three were hardcoded ("~83 distinct values", "largest tie: 45") and drifted
    # to 104/36 while NEXT-EVALS.md kept printing the old numbers — a hand-typed stat
    # inside a page whose header says "derived (not hand-maintained)". Compute them.
    scores = collections.Counter(r[0] for r in ranked)
    distinct = len(scores)
    largest_tie = max(scores.values()) if scores else 0
    zero_pressure = sum(1 for r in ranked if r[3] == 0)
```

Add `collections` to `triage.py`'s import line (check the existing line first; if it already
imports `collections`, do not duplicate it).

Then replace the hardcoded sentence in the same string list:

```python
        "Leads are grouped into **bands**, not a single ranked list. Within a band the order "
        "is `2*overlap_pressure + stage_gap_weight + evidence_bonus` (see `next-evals.py`), "
        f"but that score has only {distinct} distinct values across these {total} leads "
        f"({zero_pressure} have zero overlap pressure; largest tie: {largest_tie}) — enough "
        "to pick a head, not to rank a tail. Leads already stamped `**Last triaged:**` sink "
        "within their band so each pass surfaces un-examined ones.",
```

Note this is an f-string where the original was a plain string — make sure every literal
brace, if any, is handled. (There are none in this sentence.)

**Verify**: `python3 triage.py && grep -n "distinct values" NEXT-EVALS.md` → shows the
computed numbers (104 / 36 / 187 / 476 at the time of writing). `python3 triage.py --check`
→ exit 0.

### Step 5 (finding 3): Fix the two prose copies

`triage.py`'s module docstring (lines 3-7) hardcodes the same four numbers and cannot be
computed — it is a docstring. Rewrite it so it does not assert stale specifics; describe the
shape rather than the values, e.g. "a large minority of leads have zero overlap pressure and
the scores collapse into far fewer distinct values than there are leads, so below roughly the
head a ranked table is alphabetical order wearing a costume. The exact figures are computed
and printed in `NEXT-EVALS.md`." Do the same for the `461` in line 3 — say "the
`discovery-log` leads", with no number.

`CLAUDE.md:107` — apply the same treatment to the sentence ending "…so it ranks *within* a
band, never the whole queue." Remove the four stale numbers, keep the point, and point at
`NEXT-EVALS.md` for the current figures.

**Verify**: `grep -rn "~83\|largest tie: 45\|176 leads\|461 " triage.py CLAUDE.md NEXT-EVALS.md`
→ no matches.

### Step 6: Sync and gate

```sh
./sync-plugin-docs.sh
make fix
```

**Verify**: `make fix` exits 0 (it re-runs `make check` at the end, so a clean exit means the
tree is green). If detector A fails on network/auth, run `make check-offline` if it exists, or
`python3 audit-evals.py --offline` plus each `--check` gate individually.

## Test plan

Add to `test_automation.py`:

1. **In the reconcile test area** (near `TestReconcileMain`), add
   **`test_fixes_plugin_claudemd_eval_phrasing`** — build a fixture tree with an
   `evaluations/` directory containing N real eval files plus a `TEMPLATE.md`, and a
   `plugin/CLAUDE.md` whose line reads `- \`evaluations/\` — 1 evidence-based evaluation and comparison files`.
   Assert `fix_eval_strings(text, E)` rewrites `1` to `E`. Follow the existing fixture helpers
   (`_write`) rather than touching real files.

2. **`test_eval_count_excludes_template`** — assert `reconcile.eval_count(root=fixture_dir)`
   equals the number of non-template files. (If an equivalent test already exists, do not
   duplicate it — check first with `grep -n "eval_count" test_automation.py`.)

3. **A new `TestValidateCountsHook`** — run `bash plugin/hooks/validate-counts.sh` via
   `subprocess.run` against the **real repo** (the hook resolves its root with
   `git rev-parse --show-toplevel`, so it cannot easily be pointed at a fixture) and assert
   stdout is empty. This is the regression test for the false alarm. Mark it clearly in a
   comment as the one test that reads the real tree, and note it is read-only.
   If the hook cannot be made to run in the test environment (no git, no bash), skip this test
   with `unittest.skipUnless` rather than asserting something weaker.

4. **`test_render_computes_score_stats`** — call `triage.render(ordered, ranked)` with a small
   hand-built `ranked` list of known scores (e.g. three rows with scores `1.0, 1.0, 2.0` and
   overlap pressures `0, 0, 3`) and assert the output text contains `2 distinct values`,
   `largest tie: 2`, and `2 have zero overlap pressure`. This pins that the numbers are
   derived, not typed. You will need a matching `ordered` dict — inspect `render`'s use of it
   (`ordered[name]` per band in `BANDS`) and pass empty lists for every band.

**Verify**: `python3 -m unittest -q test_automation` → exit 0, with 4 more tests than before
(3 if `test_eval_count_excludes_template` already existed).

## Done criteria

Machine-checkable. ALL must hold:

- [ ] `python3 reconcile-counts.py --check` exits 0
- [ ] `grep -oE "[0-9]+ evidence-based evaluation and comparison" plugin/CLAUDE.md` prints the
      same number as `ls evaluations/*.md | grep -v TEMPLATE | wc -l`
- [ ] `bash plugin/hooks/validate-counts.sh` produces **no output** and exits 0
- [ ] `python3 triage.py --check` exits 0
- [ ] `grep -rn "~83\|largest tie: 45\|176 leads" triage.py CLAUDE.md NEXT-EVALS.md` → no matches
- [ ] `grep -c "distinct values" NEXT-EVALS.md` prints `1`, and the number in that sentence
      equals the output of the distinct-score computation (re-run the snippet from
      "The measured truth" to confirm)
- [ ] `python3 -m unittest -q test_automation` exits 0 with the new tests
- [ ] `./sync-plugin-docs.sh --check` exits 0
- [ ] `make check` exits 0 (detector A network failure excepted)
- [ ] `git status` shows only the in-scope files modified
- [ ] `plans/README.md` status row for 015 updated

## STOP conditions

Stop and report back (do not improvise) if:

- Step 1 does not reproduce a finding — skip that finding's steps and say so; do not invent a
  replacement fix.
- Adding the new `EVAL_PATTERNS` entry causes `reconcile-counts.py` to rewrite a number
  anywhere unexpected. Check with `git diff` after Step 2: the **only** changed line should be
  `plugin/CLAUDE.md:18`. If `README.md`, `CLAUDE.md`, `STACK.md` or `COMPARISON.md` also
  change, the pattern is too greedy — STOP.
- Fixing the hook's count surfaces a *different*, real mismatch (e.g. `plugin/CLAUDE.md`'s
  entry count vs `CATALOG.md`). That is a genuine finding: report it, and fix it via
  `reconcile-counts.py` / `sync-plugin-docs.sh` rather than by hand-editing the number.
- The computed distinct-score count in Step 4 comes out near 83 rather than near 104. That
  would mean the score function changed since this plan was written and the audit numbers are
  stale — report the real value; the fix (compute, don't hardcode) is still correct, but say
  so explicitly.
- `python3 triage.py` produces a `NEXT-EVALS.md` diff touching band membership or lead rows.
  This plan should change exactly one sentence of that page. Band churn means something else
  changed — STOP.
- You conclude `STACK.md`'s "~25 tools" should be updated. It should not; see "Out of scope".

## Maintenance notes

For whoever owns this next:

- **The general rule this plan is enforcing**: a number inside a generated page must be
  computed in the generator. If you find yourself typing a figure into a `render()` string
  list, that is the bug.
- **What a reviewer should scrutinize**: that the new `EVAL_PATTERNS` entry is anchored on a
  distinctive phrase (so it cannot match an issue number or a date), and that the `triage.py`
  docstring no longer asserts *any* specific figure — a docstring cannot self-update, so the
  only safe content there is shape, not values.
- **The remaining structural gap**: `plugin/CLAUDE.md` is a *hand-maintained* file that
  duplicates root `CLAUDE.md` content, unlike `plugin/docs/` which `sync-plugin-docs.sh`
  mirrors and gates. That is why its numbers can drift at all. Bringing it under the sync
  script (or generating it) is the durable fix and is deliberately **out of scope** here —
  it changes the plugin's packaging story and deserves its own decision.
- **Watch for**: any future prose that quotes a queue statistic. `CLAUDE.md`, `PLAYBOOK.md`
  and `discovery/README.md` all describe the triage system; each is a place a figure could be
  typed again. A cheap follow-up would be a report-only detector that flags a numeric literal
  inside any file the generators own.
