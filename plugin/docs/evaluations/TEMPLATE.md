# Evaluation: {Tool Name}

**Repo:** [{owner}/{repo}](https://github.com/{owner}/{repo})
**Stars:** {count} | **Last updated:** {date} | **License:** {license}
**Last verified:** {YYYY-MM-DD}  <!-- the date you last checked this eval against reality; staleness sweep (audit-evals.py --staleness) flags evals older than their category threshold -->
<!-- OPTIONAL next line: **Last triaged:** {YYYY-MM-DD} — add it only for a lead the triage
     lane actually looked at. Its ABSENCE is meaningful: this lead has never been examined.
     Never backfill it; a date here asserts someone looked, which is the claim detector B
     exists to catch. triage.py sinks stamped leads within their band so each pass surfaces
     fresh ones. An unattended bulk pass also appends an HTML-comment marker reading
     "triaged: bulk" to that line, after which detector Q forbids the eval any verdict
     stronger than SKIP (eliminate-only). A human who exercises the tool removes the marker,
     and says so under "How we tested it", before writing a stronger verdict. -->
**Dev loop stage:** {Plan | Implement | Verify | Review | Ship | Reflect}
**Layer:** {Process | Tooling | Infrastructure}

---

## What it does

{One-liner from the catalog, then a paragraph explaining the mechanism — what actually happens when you invoke it, not marketing copy.}

## How we tested it

**Evidence:** {MEASURED | RUN | REVIEW | SOURCE-ONLY}

> **Choosing a value** — the `Evidence` field records *how hard we looked*, separate from the verdict (*what we concluded*). Pick the strongest one that is honestly true:
> - `MEASURED` — ran it hands-on **and** captured metrics (token deltas, latency, A/B accuracy, counts) under a protocol from [`measurement-protocols.md`](measurement-protocols.md) — a with/without delta on a disclosed task, not an n=1 smoke run.
> - `RUN` — executed it hands-on, but no formal metrics (smoke test, exercised the CLI/flow).
> - `REVIEW` — read the docs/source carefully, did **not** run it (needs an API key, heavy infra, untrusted install).
> - `SOURCE-ONLY` — catalog-inferred from repo metadata (stars/README/license); not opened in depth.
>
> This must agree with the honesty disclosure below: a `REVIEW` or `SOURCE-ONLY` value requires the "not run hands-on" disclaimer. `audit-evals.py --evidence` reports the distribution (report-only for now).

{Describe the actual hands-on usage. What project did you run it on? What commands did you execute? What was the input and what came back? This section must contain evidence of real usage, not README paraphrasing.}

> **Honesty rule (checked by `audit-evals.py`):** if you did NOT actually run the tool, say so plainly — open this section with a disclaimer like "**Source-grounded review — not run hands-on**" and explain why (needs an API key, heavy infra, untrusted install, etc.). Never invent a run, specific metrics, or example outputs; a fabricated run is worse than an honest review. Quote any vendor benchmark as the vendor's, not as measured. Verify every install command resolves (npm/PyPI/crates/GitHub) before publishing — a wrong install command is a dead giveaway the tool was never run.

## Test design

> Required for MEASURED evals; recommended for RUN. See [`measurement-protocols.md`](measurement-protocols.md) for the per-signal method (Correctness/Speed measured with-vs-without; Maintainability/Safety as named-criteria rubrics).

- **Task/corpus:** {the fixed, disclosed input — the task set / corpus, named so the run is reproducible}
- **Baseline:** {what "without the tool" means here — the arm you compare against}
- **Metric:** {pass-rate (k/N) / wall-clock / tokens / counts — per the protocol}
- **Reproduce:** {the command(s) to re-run this measurement}

### Test design — skills (required when Type is skill or plugin)

A skill's value is a *change in agent behaviour*, not a CLI you can run — so measure both dimensions the way Anthropic's `skill-creator` does (see [issue #38](https://github.com/mattbutlerengineering/ai-tooling/issues/38)):

- **Triggering:** {should-fire prompts k/N; shouldn't-fire prompts k/N — does the skill's `description` fire on the right prompts and *not* the wrong ones? Skills tend to *under*-trigger. Measure via `skill-creator/scripts/run_eval.py` (`claude -p`) or a balanced hand-judged should/shouldn't-trigger prompt set.}
- **Output A/B:** {a **with-skill vs baseline A/B** — same prompt, skill on vs off; report token/latency deltas and an explicit accuracy check. For a deterministic skill with a quantitative claim, apply its `SKILL.md` rules by hand and count tokens with `tiktoken` (cheap, reproducible — see `caveman.md`); for non-deterministic skills, compare outputs qualitatively.}
- **Not run?** say so plainly — the honesty rule above applies unchanged; a not-run skill review must still disclose it.

```
{Paste the actual command(s) you ran — or, for a not-run review, the documented install/usage clearly labeled as such}
```

## What worked

- {Concrete positive finding from hands-on testing}
- {Another}

## What didn't work or surprised us

- {Concrete negative finding or unexpected behavior}
- {Another}

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | {+/-/neutral} | {one sentence} |
| Speed | {+/-/neutral} | {one sentence} |
| Maintainability | {+/-/neutral} | {one sentence} |
| Safety | {+/-/neutral} | {one sentence} |
| Cost Efficiency | {+/-/neutral} | {one sentence} |

## Verdict

**{ADOPT | CONDITIONAL | SKIP | DEFER}**

{2-3 sentences explaining the verdict. ADOPT = use in all projects. CONDITIONAL = use when {specific condition}. SKIP = evaluated and rejected. DEFER = promising but blocked by {reason}, re-evaluate after {trigger}.}

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [{name}]({url}) | {type} | {description} | {problem} | {overlaps} |
