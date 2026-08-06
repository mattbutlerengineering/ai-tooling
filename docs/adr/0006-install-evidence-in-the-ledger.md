# ADR-0006: Split the install fact out of the verdict

- **Status:** Accepted
- **Date:** 2026-08-05
- **Issue:** #382 (escalated from #366; the class was found by #332)
- **Amends:** [ADR-0005 (verdict vocabulary)](0005-verdict-vocabulary.md)

## Context

ADR-0005 defines the also-ran resolution as:

> designate **exactly one** best-in-class `ADOPT` — the pick — and resolve the also-rans
> to `SKIP` (**or `KEEP` if already installed**)

That parenthesis makes `KEEP` do two jobs at once. It is a **recommendation** ("we still
want this available") and simultaneously an **assertion of fact about one laptop** ("it is
here"). Nothing checked the second half, and a verdict is not a place where an unchecked
fact can live quietly — because a verdict is exactly what other machinery reads as though
it were checked. `STACK.md` is the install list; detector J gates STACK derivation against
the verdict data; `STACK-LEDGER.md` records why each ADOPT/KEEP tool is or is not in STACK.
Every one of those rests on an install fact that nothing looked at.

Detector Y (#366) was the first thing to look, and it found the drift immediately. Of the
catalog's 9 `KEEP` rows, four are `plugin` Type — the only Type the machine's records can
speak to — and **all four were unbacked**:

| Row | Detector Y | What is on disk |
|---|---|---|
| `code-review` | COLLISION | the name resolves to `mattpocock/skills`' own `code-review`, a different tool |
| `feature-dev` | NO-RECORD | nothing answers to it |
| `pr-review-toolkit` | NO-RECORD | nothing answers to it |
| `claude-reflect` | CACHE-ONLY | v3.1.0 was **fetched**; whether it was activated is unrecorded |

The other five `KEEP`s are `MCP server` / `framework` / `tool` / `reference`. They leave no
mark in these records at all, so their absence from the findings is **not checked** — never
*verified installed*. That distinction is the whole problem in miniature: the verdict said
"installed" for all nine and the evidence covered none.

#382 framed three readings, and two of them answer the question rather than dissolving it:

1. *STACK is a recommendation list* — then `KEEP`'s installed-half is vestigial and the four
   rows should be re-verdicted on merit. But the ambiguity survives: the next reader still
   has to know that half of `KEEP`'s definition is dead letter.
2. *STACK describes this machine* — then the four rows are wrong until something is
   reinstalled. This makes the docs a mirror of one laptop, and #366 was explicit that
   install status "can never be a CI gate", so a description CI cannot check is a
   description that will drift again.
3. **Split the fact out.** Verdicts answer *do we recommend it*; a ledger column answers
   *is it here, how was that checked, and when*. Neither silently asserts the other.

## Decision

**Adopt (3).**

**`KEEP` no longer asserts installation.** It means: *an also-ran in an overlap cluster that
we still recommend keeping available, rather than eliminating.* `SKIP` remains the also-ran
we do not. The distinction is now about recommendation only, which is a property of the tool
and not of a laptop, so it is stable across machines and checkable by reading the eval.

ADR-0005's cluster rule reads, as amended: *designate exactly one best-in-class `ADOPT` — the
pick — and resolve the also-rans to `SKIP`, or `KEEP` if the tool is still worth having
available.* Everything else in ADR-0005 stands.

**The install fact moves to `STACK-LEDGER.md`, as a column.** Every ADOPT/KEEP row carries an
`Install evidence` value recording **how** and **when**:

| Value | Means |
|---|---|
| `lockfile <date>` | the row's own slug is in `~/.agents/.skill-lock.json` — installed, settled |
| `plugins-json <date>` | recorded in `~/.claude/plugins/installed_plugins.json` |
| `skills-dir <date>` | a directory answering to it exists under `~/.claude/skills/` |
| `cache <version> <date>` | the plugin cache holds a **fetched** version; activation is unrecorded |
| `collision <date>` | this row's slug is absent **and** its name here resolves to a different repo |
| `none <date>` | checked on that date, nothing on the machine answered to it |
| `n/a` | this Type leaves no install record — the question is unanswerable, not answered |

`n/a` is the load-bearing value and the reason a bare "installed: yes/no" column would have
been worse than nothing. An `MCP server` row is not *not installed*; it is **unobservable by
these records**, and the ledger now says so instead of implying a clean check.

**Slug, never name.** The evidence is joined on the row's `owner/repo`, exactly as detector Y
does, because name-matching *is* the bug this came from (#332, #343, #366): `code-review` is
`anthropics/claude-plugins-official` in the catalog while the `code-review` on this machine
is `mattpocock/skills`' own, a different tool with a different design.

`collision` exists so that case cannot quietly flatten into `skills-dir`. The row's own slug
is asked first; only when it is absent does the name get consulted, and then only to say
*something else owns this name*. Writing the first draft without it recorded `code-review`
and `skill-creator` as installed on the strength of a directory belonging to another tool —
the very error the column was built to end, reproduced inside the fix.

**One more identity trap, on the catalog side.** `name_key` is not an identity here:
`agent-skills` (addyosmani, a skill) and `agentskills` (the `SKILL.md` spec, a reference)
collapse to the same key, and the first draft handed the reference row the skill's
`lockfile`. Resolution is therefore **exact catalog name first**, with the key fallback used
only for keys no other row claims — detector U's rule, that an ambiguous fallback resolves to
nothing rather than to a coin flip.

## Consequences

**Nothing is re-verdicted.** The four rows keep `KEEP` and are now *consistent* with it,
because `KEEP` no longer claims what the machine cannot back. `code-review` records
`collision`, `feature-dev` and `pr-review-toolkit` record `none`, `claude-reflect` records
`cache 3.1.0`. Each is a fact with a date and a method beside it. This is the property
that made (3) worth the extra work: the repair is a recording, not a restructuring —
option (1) would have moved three tools out of STACK's stage tables and out of the ledger
entirely, and option (2) would have demanded reinstalls to satisfy a document.

**`verify-installs.py` writes the column and checks it.** The split it enforces is the same
one the offline-gate invariant already demands elsewhere:

- `--record` reads this machine's install records and rewrites the column. **Local only**,
  because that is what the records are.
- `--check` validates **shape** — every ADOPT/KEEP row has a well-formed value from the
  vocabulary above. Offline, no machine access, safe in CI, and part of `make check`.

CI therefore gates that the fact is *declared and well-formed*, never that it is *true*.
A build must not fail because a laptop changed, and #366 said so before any of this existed.

**A stale value is visible rather than silent.** `none 2026-08-05` is a dated claim someone
can disagree with. The old `KEEP` was an undated claim nobody could even locate.

**The first recording, 2026-08-05, over 33 rows:** `n/a` 16 · `lockfile` 8 · `cache` 4 ·
`none` 3 · `collision` 2. Read that top line first. **Sixteen of thirty-three ADOPT/KEEP
rows — half the list — are simply not observable by any record this machine keeps**, and
under the old scheme every one of them was carrying, or sitting beside, a verdict that
implied they had been checked. The eight settled by `lockfile` are the only rows where
"installed" is a fact rather than an inference; the other nine are a fetch, an absence, or
another tool wearing the name.

**What this does not do.** It does not decide whether these four tools *should* be on this
machine — that is a separate call, and #382 put it out of scope. It also does not give
`watchlist.py` section 2 its machine-readable flagged-for-hands-on field; that is a second
column, a separate change, and this ADR is the precedent for it rather than the delivery.
