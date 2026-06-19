# Evaluation: diagnosing-bugs

**Repo:** [mattpocock/skills](https://github.com/mattpocock/skills)
**Stars:** 136,415 | **Last updated:** 2026-06-19 | **License:** MIT
**Dev loop stage:** Verify (debug)
**Layer:** Process

---

## What it does

A structured diagnosis loop for hard bugs and performance regressions, packaged as a Claude Code skill (`skills/engineering/diagnosing-bugs/SKILL.md`). It triggers on "diagnose"/"debug this" or when the user reports something broken/throwing/failing/slow.

The mechanism is a six-phase discipline, but the entire skill is organized around a single thesis stated in Phase 1: **build a tight, red-capable feedback loop before you do anything else.** Phase 1 is explicitly called "the skill"; the other five phases are described as "mechanical" consumers of that loop. The phases:

1. **Build a feedback loop** — a ranked menu of 10 ways to construct a pass/fail signal that goes red on *this* bug (failing test → curl script → CLI snapshot diff → headless browser → trace replay → throwaway harness → property/fuzz loop → bisection harness → differential loop → HITL bash script as last resort). Includes a "tighten the loop" sub-discipline (faster, sharper, more deterministic) and explicit handling for non-deterministic bugs (raise the reproduction rate, don't chase a clean repro). Completion criterion: you must name **one command you have already run at least once**, paste its invocation and output, and it must be red-capable, deterministic, fast, and agent-runnable. Hard gate: "No red-capable command, no Phase 2."
2. **Reproduce + minimise** — run the loop, confirm it produces the *user's exact* symptom (not a nearby one), then shrink to the smallest scenario that still goes red, cutting one element at a time.
3. **Hypothesise** — generate **3–5 ranked falsifiable hypotheses** before testing any, each stating a prediction; show the ranked list to the user as a cheap checkpoint.
4. **Instrument** — one variable at a time, debugger/REPL preferred over logs, tag every debug log with a unique prefix (`[DEBUG-a4f2]`) so cleanup is one grep; a dedicated perf branch (measure-first, bisect, don't log).
5. **Fix + regression test** — write the test before the fix, *but only if a correct seam exists*; if no correct seam exists, that absence is itself a finding to flag.
6. **Cleanup + post-mortem** — checklist (repro gone, test passes, all tagged logs removed, prototypes deleted, correct hypothesis recorded in the commit message), then "what would have prevented this?" with a handoff to `/improve-codebase-architecture`.

It also reads `CONTEXT.md` and ADRs if present, and ships one bundled resource: `scripts/hitl-loop.template.sh`, a human-in-the-loop bash harness with `step`/`capture` helpers that structures the loop even when a human must click, feeding captured output back to the agent.

Authored by Matt Pocock (well-known TypeScript educator, Total TypeScript). The repo — "Skills for Real Engineers. Straight from my .claude directory." — is at 136K stars, MIT-licensed, and was pushed within the last day, so maintenance and credibility are both strong.

## How we tested it

Skill-mechanism review: read the full `SKILL.md` and the bundled `hitl-loop.template.sh`, then did a side-by-side comparison against the user's already-installed competitor, superpowers' `systematic-debugging` (read from `~/.claude/plugins/cache/claude-plugins-official/superpowers/6.0.3/skills/systematic-debugging/SKILL.md`, including its supporting `root-cause-tracing.md`/`defense-in-depth.md`/`condition-based-waiting.md` references). Not run end-to-end on a live bug — this is a process skill whose value is in its method, and the decisive question for the catalog is redundancy versus systematic-debugging, which is a documentary comparison.

Notably, this exact skill is already present in the running session's skill list **twice** — as `diagnosing-bugs` and as a near-identical local `diagnose` ("Reproduce → minimise → hypothesise → instrument → fix → regression-test") — because the user has `mattpocock/skills` cloned at `~/github/skills`. So the practical question is not "install this?" but "does it earn shelf space alongside systematic-debugging, which the user already runs as a plugin?"

```bash
gh api repos/mattpocock/skills --jq '{stars, license:.license.spdx_id, description, pushed}'
gh api "repos/mattpocock/skills/git/trees/main?recursive=1" --jq '.tree[] | select(.path | test("diagnos";"i")) | .path'
gh api repos/mattpocock/skills/contents/skills/engineering/diagnosing-bugs/SKILL.md --jq '.content' | base64 -d
gh api repos/mattpocock/skills/contents/skills/engineering/diagnosing-bugs/scripts/hitl-loop.template.sh --jq '.content' | base64 -d
# Comparison target (installed):
#   ~/.claude/plugins/cache/claude-plugins-official/superpowers/6.0.3/skills/systematic-debugging/SKILL.md
```

## What worked

- **Feedback-loop-first framing is a genuinely different center of gravity.** systematic-debugging's Iron Law is "NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST" — it gates on *understanding*. diagnosing-bugs gates on *an artifact*: a named command you have already run that goes red. "No red-capable command, no Phase 2" is a harder, more verifiable gate than "investigate first," and it's exactly the discipline LLM agents most often skip (they jump to a hypothesis from reading code).
- **The 10-option feedback-loop menu is concrete and ordered.** systematic-debugging tells you to "reproduce consistently" but doesn't enumerate *how*. diagnosing-bugs gives an actionable, ranked toolkit (trace replay, differential loop, property/fuzz, `git bisect run` harness) that turns "reproduce it" from an instruction into a checklist.
- **Better non-determinism handling.** Explicitly reframes flaky bugs as "raise the reproduction rate until debuggable" (loop 100×, parallelise, inject sleeps) rather than demanding a clean repro. systematic-debugging mostly says "if not reproducible → gather more data."
- **Cleanup hygiene built for agents.** The `[DEBUG-xxxx]` tagging convention so removal is one grep, plus a mandatory cleanup checklist, addresses the real failure mode of agent-driven debugging (leftover instrumentation). systematic-debugging has no cleanup phase at all.
- **Seam-honesty in Phase 5.** "If no correct seam exists, that itself is the finding" — it refuses to write a false-confidence regression test, and routes the gap to architecture work. A sharper, more intellectually honest stance than systematic-debugging's flat "MUST have a test before fixing."
- **Strong provenance and maintenance.** 136K stars, MIT, Matt Pocock, pushed today. Bundled HITL harness is a thoughtful touch for human-gated repros.

## What didn't work or surprised us

- **Heavy overlap with already-installed systematic-debugging.** Both are multi-phase "no fix before X" debugging disciplines covering reproduce → hypothesise → instrument → minimal-fix → verify. A user running superpowers already has the spine of this method. The two are 70% the same skill.
- **It is *weaker* than systematic-debugging on the parts systematic-debugging emphasizes.** systematic-debugging has explicit root-cause *tracing* (backward through the call stack via `root-cause-tracing.md`), a Phase-2 pattern-analysis step (find working examples, diff against references), an escalation rule (3+ failed fixes = question the architecture), and a Red Flags / Common Rationalizations table tuned to catch the agent mid-mistake. diagnosing-bugs has none of these — its Phase 4 is thinner on "where does the bad value originate."
- **Single-hypothesis vs multi-hypothesis is the one clean methodological win, and it cuts against systematic-debugging.** diagnosing-bugs requires 3–5 ranked falsifiable hypotheses (anti-anchoring); systematic-debugging explicitly says "Form Single Hypothesis." This is a real disagreement, and diagnosing-bugs is right — but it's one delta, not a new skill's worth of value.
- **No hands-on differentiator surfaced.** On any given bug, an agent running either skill would do substantially the same thing. The choice is stylistic, not capability-expanding.
- **Running both risks dueling phase-gates.** With both skills triggering on "debug this," you get two competing playbooks (systematic-debugging's "investigate first" vs diagnosing-bugs' "build a loop first") and no rule for which wins. Pick one as the canonical debug skill.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Red-capable-loop gate + 3–5 falsifiable hypotheses + minimisation reduce wrong-fix risk; but systematic-debugging already delivers most of this |
| Speed | + | "Build the loop, bug is 90% fixed" + tighten-the-loop discipline cut thrashing time on hard bugs |
| Maintainability | + | `[DEBUG-xxxx]` tagging, mandatory cleanup, regression-test-or-flag-the-seam, and post-mortem-to-architecture handoff keep the codebase clean after a fix |
| Safety | neutral | Process skill; no new permissions or attack surface (HITL script is local, agent-run) |
| Cost Efficiency | + | Faster convergence on hard bugs means fewer agent turns; loop-first avoids expensive "stare at code" token spend |

## Verdict

**CONDITIONAL**

diagnosing-bugs is a high-quality, well-maintained debug-stage process skill with one genuinely better idea than the catalog's incumbent (a *red-capable artifact* gate and a concrete 10-option feedback-loop menu, plus multi-hypothesis anti-anchoring and agent-grade cleanup hygiene). But it overlaps ~70% with superpowers' `systematic-debugging`, which the user already runs as a plugin, and it is actually *thinner* on root-cause tracing, pattern analysis, and the failed-fix-count escalation that systematic-debugging does well. Running both invites two competing phase-gates on the same "debug this" trigger.

Adopt it **as a replacement for, not an addition to, systematic-debugging** if you value the loop-first / artifact-gated framing (strongest fit for agent-driven debugging, where the failure mode is hypothesising before reproducing) — or stay on systematic-debugging if you value root-cause tracing and the rationalization-catching guardrails. Do not run both. It does not earn a second seat in the stack; it earns the right to compete for the one debug-skill seat.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [diagnosing-bugs](https://github.com/mattpocock/skills) | skill | Structured diagnosis loop: build feedback loop first, then bisect/hypothesize/instrument | Jumping straight to "staring at code" wastes hours on hard bugs | systematic-debugging (superpowers) |
