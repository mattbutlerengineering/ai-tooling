# Bake-off: agentmemory vs claude-mem — Memory & Context pilot

**Evidence:** REVIEW
**Last verified:** 2026-07-03
**Dev loop stage:** Reflect
**Layer:** Tooling
**Status:** BLOCKED (pilot needs attended run) — the three-arm head-to-head below is
**designed but NOT run**. This file records the design honestly; it contains no measured
result. See [`bakeoff-protocol.md`](bakeoff-protocol.md).

---

## What it does

The first pilot for [`bakeoff-protocol.md`](bakeoff-protocol.md), in the weakest validated
category (Memory & Context: 2 validated of 47 catalogued, verified 2026-07-03).

**The pair:**

- **Incumbent (A):** [claude-mem](https://github.com/thedotmack/claude-mem) — the ADOPT/KEEP
  Memory & Context tool, already installed (it powers this repo's own session memory), so the
  A/B has a live baseline. Native Claude Code plugin, observation-based auto-capture, SQLite +
  Chroma, 18+ bundled skills.
- **Challenger (B):** [agentmemory](https://github.com/rohitg00/agentmemory) — MCP-based
  persistent memory, Apache-2.0, self-contained (zero external databases), claims 95.2% R@5
  and 92% token reduction; works across Claude Code / Codex / Cursor / Gemini.

**Selection rationale (per the plan's bounded procedure):**

- **Default satisfied:** claude-mem (incumbent) vs the strongest *free/local* Memory & Context
  challenger. agentmemory is `Free ✓` (no paid tier) and runs locally with no external
  database and no mandatory cloud LLM — it clears the plan's "free/local, no paid API" bar.
- **Already the ranked runner-up:** the existing prose comparison `memory-systems.md` ranks
  "claude-mem > agentmemory > OMEGA" and calls agentmemory the explicit **runner-up**;
  claude-mem's own `CATALOG.md` "Overlaps with" cell names agentmemory directly. The
  head-to-head that prose gestures at has never been *run* — this pilot is that run.
- **Highest overlap pressure among valid contestants:** 8 `CATALOG.md` rows cite agentmemory
  in "Overlaps with". Higher-cited peers were excluded for cause: **OMEGA** (22 cites) is
  itself the other validated KEEP incumbent, not a challenger; **cognee** (15), **supermemory**
  (13), **MemOS** (10) are heavy platforms whose memory extraction defaults to a paid LLM API,
  tripping the free/local constraint; **mem0** (9) already has a head-to-head record
  (`mem0-vs-claude-mem.md`) this protocol supersedes by method. agentmemory is therefore the
  strongest challenger that is both a genuine peer and honestly runnable free/local.

## How we tested it

**Evidence:** REVIEW

**Source-grounded — not run hands-on. This bake-off was NOT executed.** As an unattended
executor I did not install or run either tool and did not measure any arm; running the pilot
(Step 3 of plan 011) requires an attended session and is the hard STOP point for this task.
Nothing below is a measured result — the numbers agentmemory and claude-mem *claim* are the
vendors', not reproduced here, and no pass-rate, latency, or token count in this file was
observed. The design in "Test design" is what **would** be run; Evidence stays `REVIEW` and
the verdict stays `DEFER` until the three arms are actually run and recorded. Fabricating a
run here would be caught by detector B, and would be worse than this honest blocked record.

## Test design

> The design an attended run WOULD execute — recorded now, measured later. Follows
> [`measurement-protocols.md`](measurement-protocols.md) and the six parts of
> [`bakeoff-protocol.md`](bakeoff-protocol.md). None of this has been run.

- **Same job:** "persistent memory across sessions for a coding agent" — the job both
  `CATALOG.md` rows claim (claude-mem: "searchable, structured memory with temporal
  awareness"; agentmemory: "memory validated against actual dev workflows").
- **Task/corpus:** a fixed set of **4 planted-fact recall tasks**, each with a **binary
  mechanical oracle** — in session 1 plant a specific fact (e.g. "the deploy token env var is
  `FOO_DEPLOY_KEY`"; "the staging DB port is 5544"; "the release owner is Priya"; "the flaky
  test is `test_retry_backoff`"); in a *fresh* session ask for it and score exact-string recall
  pass/fail. No human quality judgment — the fact is either returned verbatim or it is not.
- **Baseline / arms (three):** **A** = claude-mem on; **B** = agentmemory on; **neither** =
  fresh session, no memory tool (expected to fail recall — the arm that catches "both worse
  than nothing"). Same model, same session shape, same machine across all three.
- **Metric:** Correctness = recall pass-rate `k/4` per arm; Speed = median wall-clock over
  N≥3 recall runs per arm; Cost = `tiktoken cl100k_base` tokens injected into the fresh
  session's context per arm. Maintainability/Safety = rubric notes (install footprint,
  external DBs, permissions/network calls observed).
- **Reproduce (install commands — both resolve; verified via detector A):**

```
claude install-plugin thedotmack/claude-mem
npm install -g @agentmemory/agentmemory
```

Then, per arm, plant the 4 facts in session 1, start a fresh session, ask for each fact,
and score exact-string recall `k/4`; repeat N≥3 for the Speed median.

## What worked

- _Not run — nothing to report. To be filled by the attended run._

## What didn't work or surprised us

- _Not run — nothing to report. To be filled by the attended run._

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Not measured — recall pass-rate is the designed metric but no arm was run |
| Speed | neutral | Not measured — no timed runs |
| Maintainability | neutral | Not measured — install-footprint rubric deferred to the attended run |
| Safety | neutral | Not measured — permission/network observation deferred to the attended run |
| Cost Efficiency | neutral | Not measured — per-arm token injection is the designed metric, unrun |

## Verdict

**DEFER** — the pilot is designed but blocked by needing an attended run. Re-evaluate after
the three arms are actually run and the per-signal results recorded; only then can a winner /
split-decision / neither be declared, and only then can Evidence graduate to MEASURED. No
verdict on either tool changes on the basis of this file — it is a blocked-attempt record,
not a result. The honest SOURCE-ONLY `mem0-vs-claude-mem.md` and the prose
`memory-systems.md` ranking remain the current comparative surface until this bake-off runs.
