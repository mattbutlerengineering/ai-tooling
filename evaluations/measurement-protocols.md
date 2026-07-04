# Evaluation: Per-signal measurement protocols

**Repo:** _(methodology — not a third-party tool; the protocols live in this repo)_
**Last verified:** 2026-07-03
**Evidence:** MEASURED
**Dev loop stage:** Reflect
**Layer:** Process

---

## What this is

The generalization of [`token-savings-protocol.md`](token-savings-protocol.md) — which
measures exactly one quality signal (Cost Efficiency) — to the rest of the five signals.
Before this doc, only Cost had a defined measurement; Correctness, Speed, Maintainability,
and Safety were recorded as `{+/-/neutral}` + one sentence (`TEMPLATE.md`) even in evals
stamped MEASURED, so the badge spanned everything from a rigorous multi-variant A/B to an
n=1 smoke run. This file defines the missing protocols so "MEASURED" means the same thing
across evals, comparative bake-offs have a metric to rank on, and REVIEW → MEASURED
graduation has a bar for more than token savings.

The method is always the same **four moves** (lifted verbatim from the token-savings method):

1. **Fix the task.** A small, real, *disclosed* task set or corpus — the exact input,
   named in the eval so the run is reproducible. No hand-picked best case.
2. **Fix the measure.** A deterministic, mechanical oracle or counter (a test that passes,
   a `tiktoken` count, a wall-clock timer) — not a human "feels better."
3. **Run with/without.** Measure the metric with the tool on (treatment) and with the tool
   off (baseline). The delta *is* the evidence; a number with no baseline measures nothing.
4. **Record honestly.** Claimed vs measured, on the named task. A tool that underdelivers is
   recorded as such — the catalog stays trustworthy even when a tool disappoints.

## Correctness protocol

Fix a **task set of 3–5 tasks, each with a binary pass/fail oracle** — this is the
skill-creator eval's pattern (N broken-skill variants, each with a known-correct fix, scored
6/6). Requirements:

- **Task set disclosed in the eval** — the prompts/inputs, verbatim or as a runnable file.
- **Mechanical oracle** — the test suite passes, the output matches an expected string, the
  linter/typechecker accepts it. No "the answer looked right."
- **Report `k/N with vs k/N without`** — pass-rate with the tool vs the same task set run
  with/without it, same harness/model. The with/without delta is the correctness signal;
  a single with-tool pass-rate and no baseline is RUN, not MEASURED.

## Speed protocol

Fix the **same task set**, then measure a wall-clock and/or agent-turn cost with/without the
tool, holding harness and model constant. Requirements:

- **Metric:** wall-clock seconds and/or agent turns per task; tokens-in/out per task where
  the harness reports them.
- **N ≥ 3 runs** per condition (agent latency is noisy) — **report median + range**, never a
  lone number. A single timed run is RUN, not MEASURED.
- **Same everything but the tool** — model, harness, prompt, machine — so the with/without
  delta is attributable to the tool and not to a warm cache or a faster model.

## Maintainability & Safety — honest rubrics, not fake numbers

These two signals stay **qualitative by policy**. There is no honest mechanical oracle for
"maintainability" or "safety" of a tool, and inventing a 0–10 score would be exactly the
fake precision this repo exists to fight. The protocol is a **named-criteria rubric** —
specific observed criteria, each cited to evidence, not a manufactured number:

- **Maintainability:** does the change the tool produces reduce file size, coupling, or
  duplication? Cite the diff (lines added/removed, files touched, a function extracted).
  Judge the artifact, not the vibe.
- **Safety:** what permissions did it request, what network calls did it make, did it run
  under the sandbox? Cite the observed behavior (the permission prompt, the outbound host,
  the sandbox exit code).

State it plainly in the eval: **a rubric judgment is not a measurement.** A well-argued
rubric can support a `+`/`-` in the signals table, but it never *alone* justifies the
MEASURED badge — MEASURED requires a measured signal under one of the protocols above.

## What qualifies as MEASURED

At least one signal measured under its protocol — **a with/without delta on a disclosed
task set**, with a mechanical metric. Concretely:

- **MEASURED** — Correctness (`k/N with vs k/N without`), Speed (median of N≥3 with/without),
  or Cost (`tiktoken` with/without) measured against a named task set. The Test-design block
  in the eval records the task, baseline, metric, and reproduce command.
- **RUN, not MEASURED** — an n=1 smoke run with **no baseline** ("I ran it once and it
  worked"), a with-tool number with nothing to compare it against, or a Maintainability/Safety
  rubric with no measured signal alongside it. Honest and useful, but it is `RUN`.
- **REVIEW / SOURCE-ONLY** — read the source or the metadata, did not run it. Unchanged.

The distinction is the baseline. A measurement is a *comparison*; without the "without" arm
there is no delta, and without a delta there is no measurement — only an anecdote.

## Worked pointers

- **Cost** → [`token-savings-protocol.md`](token-savings-protocol.md) — fixed corpus + fixed
  `tiktoken cl100k_base` + tokens-in with/without; the parent method this doc generalizes.
- **Correctness** → [`skill-creator.md`](skill-creator.md) — the 6/6 broken-skill oracle:
  N variants, each with a mechanical known-correct check, scored with vs without the skill.
- **Cost (deterministic A/B on a skill)** → [`caveman.md`](caveman.md) — apply the skill's
  rules by hand, count tokens with `tiktoken` with/without; a measured 49–59% against a
  looser vendor headline.

## How we tested it

**Evidence:** MEASURED

This is a methodology doc, not a run of a third-party tool — it is distilled from the
**hands-on**, measured evals already in this repo, and every move it prescribes is one that
has already been executed here. The Correctness protocol is the measured A/B behind
`skill-creator.md` (6/6 broken-skill oracle, pass-rate with vs without the skill); the Cost
protocol is the `tiktoken` baseline vs treatment run in `token-savings-protocol.md` (0–2% on
real corpora) and `caveman.md` (49–59%). No metric here is asserted that isn't backed by one
of those disclosed runs; nothing is invented. The doc's job is to name the bar those evals
already cleared so future evals clear the same one.

> This protocol is itself a methodology eval, **intentionally not added to
> `CATALOG.md`/`COMPARISON.md`** — it is a measuring instrument, not a tool in the inventory.
> No catalog count changes.

## Verdict

**ADOPT** (as the standard measurement method for the four measurable signals)

Use these protocols to graduate any eval from REVIEW to MEASURED, and to design the
head-to-head bake-offs. The Test-design block in `TEMPLATE.md` is the per-eval record that a
measurement followed one of them; an ADOPT/KEEP verdict resting on an n=1 smoke run should be
re-run under the relevant protocol before it claims MEASURED.

## Catalog entry

_Intentionally none._ This is a methodology eval (a measuring instrument), not a third-party
tool, so it has no `CATALOG.md`/`COMPARISON.md` row and does not change the catalog count.
