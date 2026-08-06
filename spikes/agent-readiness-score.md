# Spike: score this repo on agent readiness

**Issue:** [#385](https://github.com/mattbutlerengineering/ai-tooling/issues/385) · **Date:** 2026-08-05 · **Outcome:** measured score + one correction to [`methodologies/software-factories.md`](../methodologies/software-factories.md). The spike itself made no behavior changes; the Level 1 failure it found was then fixed by [#388](https://github.com/mattbutlerengineering/ai-tooling/issues/388), and both the before and after figures are kept below.

[`software-factories.md`](../methodologies/software-factories.md#agent-readiness-is-the-prerequisite-nobody-sells-you)
asserted a readiness grade for this repo and said outright that the grade was
asserted, not measured. This spike measures it.

**Why it matters:** the only *measured* claim in all the vendor material is
Factory's — level 4–5 codebases show "massive acceleration" of end-to-end product
life cycles; **level 1–2 codebases show "very active deceleration."** If that is
true, readiness is not a nice-to-have that follows adoption, it is the gate in
front of it.

## What is being scored against

Factory's [Agent Readiness Model](https://docs.factory.ai/web/agent-readiness/overview):
nine pillars, five levels, and a gate — **you must pass 80% of a level's criteria to
unlock the next.**

**This is a faithful reconstruction, not Factory's scorer.** The published overview
gives level names, definitions, the nine pillars and *representative* criteria; the
full criteria list, weights, and per-pillar breakdown are not public. So the level
numbers below are what the published rules produce on the evidence gathered here.
Every row cites what was checked, so a wrong criterion set changes the score
transparently rather than invisibly.

## Evidence gathered (2026-08-05)

| Fact | Value | How checked |
|---|---|---|
| CI wall-clock | **median 34s**, min 26s, max 46s | `gh run list --workflow=integrity.yml --limit 20`, computed from `createdAt`/`updatedAt` |
| CI reliability | **20 / 20 success** over the last 20 runs | same |
| Unit tests | **324** | `grep -c "def test_" test_automation.py` |
| Python surface | **8,223 lines across 11 files** (`test_automation.py` 3,852; `audit-evals.py` 2,411) | `wc -l *.py` |
| Linter | **none** | no `ruff`/`flake8`/`pylint` config anywhere in the tree |
| Type checker | **none** | no `mypy.ini`, no `pyproject.toml`, no annotations gate |
| Coverage measurement | **none** | no coverage tool in `Makefile` or CI |
| Branch protection | `audit` required on `main`; `strict: false`, `enforce_admins: false`, no required reviews | `gh api …/branches/main/protection` |
| Secret scanning | **enabled**, with push protection **enabled** | `gh api repos/…` `security_and_analysis` |
| Dependabot security updates | **enabled** (server-side; no `.github/dependabot.yml`) | same |
| Git pre-commit hooks | **none** (`.git/hooks/` holds only samples) | `ls .git/hooks/` |
| Harness hooks | `PreToolUse` → `.claude/hooks/audit-gate.sh`; `PostToolUse` → `auto-sync.sh`; opencode equivalents in `.opencode/plugins/` | `.claude/settings.json` |
| `AGENTS.md` | **absent by design** ([ADR-0002](../docs/adr/0002-catalog-source-of-truth.md)) — opencode reads `CLAUDE.md` as its rules fallback | tree + ADR |
| Devcontainer | **none** | no `.devcontainer/` |
| `CODEOWNERS` | **none** | `ls .github/CODEOWNERS` |
| Flaky-test detection | **none** | no retry/quarantine machinery |
| Task discovery | `NEXT-EVALS.md` + `WATCHLIST.md` (both generated), triage bands, label vocabulary, `scan` issues | `triage.py`, `watchlist.py`, `docs/agents/` |

## The score

### Level 1 — Functional · **4 / 4 = 100% · gate cleared** *(was 2/4 — see below)*

> *"Code runs, but requires manual setup and lacks automated validation."*

| Criterion | Verdict | Evidence |
|---|---|---|
| README | ✅ | `README.md`, plus `PLAYBOOK.md` as the routed front door and `CLAUDE.md` as the agent entrypoint |
| Unit tests | ✅ | 333 tests, CI-gated via `make check` |
| Linter | ✅ | `ruff==0.16.1`, first line of `make check` and of CI ([#388](https://github.com/mattbutlerengineering/ai-tooling/issues/388)) |
| Type checker | ✅ | `mypy==2.3.0`, same gate |

> **Scored 2/4 when this spike was written on 2026-08-05, and that is the number the
> spike existed to produce.** The measurement is what got the linter added: it named a
> failed criterion nobody had noticed, #388 measured what fixing it would actually cost
> (149 ruff findings, **zero live bugs** — every bug-shaped rule hand-checked and cleared),
> and the fix landed the same day. Both figures are kept here rather than overwritten,
> because a readiness score that only ever shows its current value cannot show that it
> moved anything.

**The finding is still worth sitting with, even though it is now fixed.** This repo ran
fifteen detectors, regenerated six pages from data, gated every push in CI, and refused
to let a count be hand-edited — and it scored Level 1 because **the code that enforced
all of that was itself ungated.** The rigor was aimed entirely at the *data*
(`CATALOG.md`, `COMPARISON.md`, the evals) and not at all at the *program*.
`audit-evals.py` is 2,411 lines, and before #388 a rename inside it was caught only if a
test happened to cover that path.

`software-factories.md` called guardrails "strong." That was true of the data plane and
false of the code plane, and the distinction was invisible until the score forced it.

**What the linter did not find is as much the point as what it did.** Of 149 findings,
none was a live bug. The value was the 22 unclosed-file sites — which had been printing a
wall of `ResourceWarning` on every `make check` run, in plain sight, for months — and
drift prevention from here on. A gate that starts green is not a gate that was
unnecessary.

### Levels 2–5, scored anyway

The gate no longer stops at Level 1, but the *shape* of the result below is the real
diagnostic and it has not changed: the levels above are passed on substance and failed
on literal criteria.

**Level 2 — Documented** · 1 hard pass, 3 substance-passes that fail literally

| Criterion | Verdict | Note |
|---|---|---|
| Branch protection | ✅ | `audit` required on `main` — the routine lane depends on it |
| `AGENTS.md` | ⚠️ | Deliberately absent (ADR-0002): both supported harnesses read `CLAUDE.md`, and a second file would be a duplicate that drifts. The criterion is really *"is there a machine-discoverable agent entrypoint"* — there is. A literal scorer marks this failed. |
| Pre-commit hooks | ⚠️ | No git hook. There are **harness** hooks: a `PreToolUse` Bash gate and a `PostToolUse` auto-sync, mirrored as opencode plugins. Stronger than a git hook in one direction (it gates the *agent*, which is what does the work here) and weaker in the other (a human's `git commit` at the CLI is ungated). |
| Devcontainer | ⚠️ | None, but there is no build: `python3` + `gh` + `node` and `make check` runs. Trivially satisfiable, currently undeclared. |

**Level 3 — Standardized** · effectively passed

| Criterion | Verdict | Note |
|---|---|---|
| Integration tests | ✅ | `make check` runs the full pipeline against the real tree; `test_automation.py` characterizes the generators against temp fixtures |
| Secret scanning | ✅ | enabled, with **push protection** |
| Distributed tracing | n/a | no runtime service to trace |

**Level 4 — Optimized** · half passed, and the half that passes was the one assumed missing

| Criterion | Verdict | Note |
|---|---|---|
| Rapid CI feedback | ✅ | **median 34s**, max 46s across 20 runs. Fast enough that an agent can treat CI as part of the inner loop rather than as a wait. |
| Flaky-test detection | ❌ | none — though 20/20 green is evidence there is nothing to detect yet |

**Level 5 — Autonomous** · genuinely present, and no longer sitting on an ungated L1

> *"Systems are self-improving with sophisticated orchestration."*

- Six pages regenerate from data (`triage.py`, `watchlist.py`, `tier-stack.py`,
  `reconcile-counts.py`, `backfill-evidence.py`, `backfill-lastverified.py`); nobody
  edits them by hand.
- The routine lane lands its own PRs on green CI.
- Triage bands **declare what an unattended pass may conclude** about each lead, and
  detector Q enforces it mechanically — eliminate-only, with attribution markers
  separating a bulk lane from a human one.
- Weekly report-only sweeps open a tracking issue instead of failing a build.

## The shape of the result

```
   L5  ████████░░  orchestration — present, and unusual
   L4  █████░░░░░  fast CI ✓ · flaky detection ✗
   L3  █████████░  integration ✓ · secret scanning ✓ · tracing n/a
   L2  ███░░░░░░░  branch protection ✓ · three substance-passes that fail literally
   L1  ██████████  README ✓ · tests ✓ · linter ✓ · type checker ✓   ← the gate, cleared

   as measured 2026-08-05, before #388:
   L1  █████░░░░░  README ✓ · tests ✓ · linter ✗ · type checker ✗   ← the gate
```

**Level-5 orchestration on a Level-1 foundation.** That inversion was the whole finding,
and it is exactly what the gated model is designed to catch: sophisticated process built
on top of a program nobody validates. The gate exists to stop a repo buying its way past
a missing fundamental with one impressive capability, and here it did its job — the
foundation row is filled in now *because* the gate flagged it.

It also validates the model's own premise from the other direction. The reason the
orchestration works at all is that this repo's *data* has the deterministic signals
Factory's model is asking for — `make check` exits non-zero with a file and a line.
Extending that same discipline to the code was a small, obvious piece of work that was
invisible until something scored it — and once scored, it took one issue and one
afternoon.

## What this corrects in `software-factories.md`

| Claim there | Status after measuring |
|---|---|
| "Guardrails are strong — `make check`…" | **Was true of the data plane, false of the code plane** — 8,223 lines of Python with no linter, no type checker, no coverage number. Fixed by #388 for the first two; coverage is still unmeasured. |
| "What is missing is feedback speed instrumentation" | **Wrong.** It was un-instrumented, not slow: median 34s, 20/20 green. Measuring it took one command. |
| "the grade above is asserted, not measured" | Resolved — this spike is the measurement. |

The doc is updated to point here.

## Follow-ups (not done here)

Ranked by what the gate actually blocks on:

1. ~~**Add a linter and a type checker for the repo's own Python**, wired into `make check`
   so they gate in CI like everything else.~~ **Done** — `ruff` and `mypy`, pinned, first
   line of `make check` and of CI ([#388](https://github.com/mattbutlerengineering/ai-tooling/issues/388)).
   The prediction that it would take an afternoon held; the prediction of "real findings"
   did not — 149 findings, **zero live bugs**. The payoff was 22 unclosed-file handles
   that had been printing `ResourceWarning` on every gate run in plain sight, and drift
   prevention from here on.
2. **Declare the environment** — a one-command bootstrap or a devcontainer. Nothing is
   broken; it is undeclared, which is a different failure for an agent that has to
   guess.
3. **Instrument CI duration as a tracked number**, not a number this spike happened to
   compute once. It is the closest thing to the cycle-time metric rule 7 asks for.
4. **Leave `AGENTS.md` alone.** The literal criterion fails and ADR-0002 is right;
   a duplicate that drifts is worse than a missing file. Worth recording as a
   *deliberate* miss rather than an unnoticed one — which is the whole reason to score
   against someone else's model instead of your own.

Flaky-test detection is deliberately **not** on this list: with 20/20 green there is
nothing to detect, and building the machinery before the problem is the kind of
scaffolding-before-shipping this repo's own evaluations are skeptical of.
