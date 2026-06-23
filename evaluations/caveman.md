# Evaluation: caveman

**Repo:** [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman)
**Stars:** 74,045 | **Last updated:** 2026-06-17 | **License:** MIT
**Dev loop stage:** All stages (output compression)
**Layer:** Tooling

---

## What it does

Claude Code skill that cuts output tokens (measured ~49–59% on prose; see below) by instructing the model to drop articles, filler words, and pleasantries while keeping full technical accuracy. Activated via `/caveman` as a mode toggle — not a background process or proxy. The model continues to produce code, commands, and paths at full fidelity; only the surrounding prose is compressed.

## How we tested it

**Evidence:** MEASURED

**Hands-on, measured A/B** (the repo's first measured *skill* eval — pilots the methodology in issue #38). Skills can't be run like a CLI, so we measured the skill's core quantitative claim directly: read caveman's actual compression rules from its `SKILL.md` (drop articles/filler/pleasantries/hedging, fragments, short synonyms, abbreviate common terms, arrows for causality; *code/paths/errors unchanged*), then ran a with-skill-vs-baseline comparison on **4 representative technical explanations** in natural assistant register (React re-render, an auth bug, a status+next-steps update, a DB-pool ops issue). Baseline = normal prose; with-skill = the same content compressed per the documented rules. Token counts via `tiktoken` (gpt-4o), measured at two compression intensities to bracket the real range:

```
                      base -> caveman   reduction
conservative pass:    269  -> 138       48.7%   (43–51% per case)
aggressive pass:      269  -> 110       59.1%   (53–63% per case)
```

The **triggering** dimension is trivial here — caveman is explicitly user-invoked (`/caveman`), not auto-triggered — so this eval measures the **output-quality** dimension: token reduction and accuracy preservation.

**Accuracy assertion (passed):** every technical identifier survived compression in all 4 cases — `useMemo`, the `<` vs `<=` operator fix, "API gateway", "integration tests", "pool max size". No code, path, or operator was altered. The claim of "full technical accuracy" holds.

## What worked

- **Measured ~49–59% output-token reduction on explanatory prose** (48.7% conservative, 59.1% aggressive across 4 cases) — a real, repeatable saving.
- **Accuracy preserved** — code, commands, paths, operators, and named components were untouched in every case; the rules explicitly leave code blocks and quoted errors exact.
- Immediate activation, zero config — just `/caveman`.
- Particularly suited to agent-to-agent / background work where human readability isn't the priority.

## What didn't work or surprised us

- **The headline "~60–75%" is optimistic for natural register.** On already-polite-but-normal assistant prose we measured ~49% (conservative) and reached ~59% only with maximally aggressive abbreviation. Hitting 70%+ requires *very* verbose/corporate baselines (lots of pleasantries and hedging to strip) — i.e. the reduction scales with how bloated the baseline was, not a fixed rate.
- **Savings are output-only and prose-only.** Code-heavy or already-terse responses compress little (caveman leaves code unchanged), so the per-session saving depends heavily on the prose-to-code ratio.
- Transcript readability drops for humans skimming session history.
- Sticky per-session but doesn't persist across sessions; can "drift" verbose on long sessions and need a reminder.
- Not for polished prose (docs, PR descriptions, commit messages).

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | All technical identifiers/operators/code preserved across the 4-case A/B. |
| Speed | + | Fewer output tokens → faster completion (proportional to the ~49–59% prose reduction). |
| Maintainability | neutral | Output content identical; only prose style differs. |
| Safety | neutral | Rules carve out an exception that drops caveman for security warnings & destructive-op confirmations. |
| Cost Efficiency | + | Measured ~49–59% fewer output tokens on prose responses (0% on code). |

## Verdict

**ADOPT**

Zero-friction mode toggle with **measured** token savings — ~49% (conservative) to ~59% (aggressive) on explanatory prose in a 4-case with-skill-vs-baseline A/B, with no accuracy loss on technical content (all identifiers/operators/code preserved). Note the magnitude: the repo's earlier "~60–75%" was optimistic; real-world savings depend on baseline verbosity and prose-to-code ratio, so budget ~50% on prose, near-0% on code-heavy turns. Ideal for autonomous agent workflows, background tasks, and cost-sensitive sessions; skip when polished human-readable output is the goal.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [caveman](https://github.com/JuliusBrussee/caveman) | skill | Cuts output tokens (~49–59% measured on prose) by dropping filler while keeping technical accuracy | Verbose agent output wastes tokens and slows responses | context-mode (input side), headroom |
