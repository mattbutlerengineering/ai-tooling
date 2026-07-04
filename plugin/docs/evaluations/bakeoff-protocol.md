# Evaluation: Overlap-cluster bake-off protocol

**Repo:** _(methodology — not a third-party tool; the method lives in this repo)_
**Last verified:** 2026-07-03
**Evidence:** REVIEW
**Dev loop stage:** Reflect
**Layer:** Process

---

## What this is

The head-to-head generalization of [`measurement-protocols.md`](measurement-protocols.md).
Those protocols measure one tool with-vs-without itself; a **bake-off** measures **tool A
vs tool B** for the *same job*, under one disclosed task set, so the catalog can answer the
question users actually ask — "A or B?" — with a run, not prose judgment.

Every `CATALOG.md` row names its "Overlaps with" peers and `WORKFLOW.md` lists overlap
groups where "we compared competitors, picked a winner", but those winners were picked by
reading, not by a shared-task run. The two comparative evals that exist
(`mem0-vs-claude-mem.md`, `mattpocock-vs-agent-skills.md`) are both `SOURCE-ONLY`, resting on
unreproduced vendor benchmarks — exactly the failure `token-savings-protocol.md` was written
to stop. This protocol is the method for producing run-backed head-to-heads instead.

It reuses the four moves of the measurement protocols verbatim (fix the task, fix the
measure, run with/without, record honestly) and adds the structure a two-tool comparison
needs: a shared task set, a third "neither" arm, and an explicit resolution rule.

## The six parts

1. **Same job.** Name the overlap cluster and the single job both tools claim — quote it
   from their `CATALOG.md` "Problem it solves" cells so the comparison is same-job, not
   same-category. If the two rows describe different jobs, there is no bake-off to run.

2. **Same task set.** One fixed, *disclosed* task set of **3–5 tasks, each with a mechanical
   oracle** (a test that passes, an expected string, a `tiktoken` count) — the Correctness
   task-set requirement from [`measurement-protocols.md`](measurement-protocols.md). No
   hand-picked best case; the prompts/inputs are named verbatim so the run is reproducible.

3. **Same harness — three arms.** Same model, same session shape, same machine. Run the task
   set three times: **tool A**, **tool B**, and **neither** (baseline, no tool). The neither
   arm is the teeth of the design — it catches "both tools are worse than nothing", which a
   two-way comparison structurally cannot see. A bake-off that drops the neither arm must say
   why, or it is rejected.

4. **Record per signal.** Report each signal under its protocol from
   [`measurement-protocols.md`](measurement-protocols.md): **Correctness** as pass-rate
   (`k/N` per arm), **Speed** as the median of N≥3 runs per arm (with range), **Cost** as
   tokens per arm (`tiktoken cl100k_base`). **Maintainability** and **Safety** stay
   named-criteria rubric notes — observed criteria cited to evidence, never a manufactured
   number.

5. **Resolve.** State the outcome explicitly, one of: **winner** (A or B beats the other and
   the neither arm on the measured signals), **split-decision** ("A for X, B for Y" — a
   legitimate result; record the condition that selects each), or **neither** (the baseline
   arm matched or beat both). The result updates *both* tools' "Versus alternatives" sections
   and the `WORKFLOW.md` overlap-groups list, with a link to the bake-off eval.

6. **Honesty.** A bake-off you could not complete is recorded as such — the code-on-incus
   precedent, where a blocked attempt is committed honestly rather than dressed up as a run.
   Evidence is `MEASURED` **only** if all three arms actually ran on the disclosed task set;
   a designed-but-not-executed bake-off is `REVIEW` with a not-run disclaimer, never a
   fabricated result. Detector B (fabrication) enforces this.

## How we tested it

**Evidence:** REVIEW

**Source-grounded — the three-arm head-to-head has not been run hands-on yet.** This protocol
is composed from methods each *already measured* in this repo — the Correctness pass-rate
oracle behind `skill-creator.md` (6/6), and the token-count cost baseline in
`token-savings-protocol.md` (0–2%) and `caveman.md` (49–59%) — but the combined three-arm,
two-tool structure it prescribes has **not been reproduced end-to-end**. Its first validation
is the Memory & Context pilot (`agentmemory-vs-claude-mem-bakeoff.md`), which is **BLOCKED
pending an attended run** (plan 011). No head-to-head number is asserted here; nothing is
invented. The doc's job is to name the bar that first bake-off must clear, and to do so
before the run exists — so this is a source-grounded method spec, not a report of a run.

> This protocol is itself a methodology eval, **intentionally not added to
> `CATALOG.md`/`COMPARISON.md`** — it is a measuring instrument, not a tool in the inventory.
> No catalog count changes.

## Verdict

**ADOPT** (as the standard method for overlap-cluster head-to-heads)

Use this for any "A vs B for the same job" question the catalog's overlap markers raise. It
inherits the honesty machinery of the measurement protocols it composes, so a thin or
un-run bake-off is caught rather than trusted. Its own first end-to-end validation is the
blocked pilot above; adopt it as the required shape for every future bake-off regardless.

## Catalog entry

_Intentionally none._ This is a methodology eval (the measuring instrument), not a
third-party tool, so it has no `CATALOG.md`/`COMPARISON.md` row and does not change the
catalog count.
