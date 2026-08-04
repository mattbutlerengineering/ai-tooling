# Evaluation: waza (Microsoft)

**Repo:** [microsoft/waza](https://github.com/microsoft/waza)
**Stars:** ~1,000 | **Last updated:** 2026-06-19 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Reflect (skill quality evaluation)
**Layer:** Tooling

> ⚠️ **Name collision:** This is Microsoft's skill-evaluation CLI, a different project from [tw93/Waza](https://github.com/tw93/Waza) (a curated engineering-habits skill suite) which is catalogued separately as `Waza`.

---

## What it does

A Go CLI/framework from Microsoft for **evaluating AI agent skills**. Where most skill collections are written by intuition with no quality signal, Waza lets you scaffold eval suites, run benchmarks, and compare results across models — so you can create, test, **measure, and improve** skill quality systematically.

Mechanically it installs as a standalone Go binary (curl|bash, checksum-verified, cross-platform). You scaffold an eval suite for a skill, define benchmark cases, run them against one or more models, and compare results — treating skill effectiveness as something measurable rather than asserted. It's the skills analogue of an eval harness: instead of shipping a skill and hoping it triggers/performs, you benchmark it.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README and the documented workflow (scaffold eval suites → run benchmarks → compare across models). Confirmed the standalone Go-binary install, the cross-model comparison model, and the "measure/improve skill quality" positioning. Verified the name collision with tw93/Waza (different project, same name). Not run against a live skill suite, so condition-gated.

```bash
gh api repos/microsoft/waza --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/microsoft/waza/readme --jq '.content' | base64 -d
```

## What worked

- **Brings measurement to skills.** Skills have proliferated with no objective quality bar; a benchmark/eval harness for them is exactly the missing discipline — conceptually like promptfoo/deepeval but for skills.
- **Cross-model comparison.** Comparing a skill's effectiveness across models tells you where it works and helps tune triggering/content — actionable, not just a score.
- **Microsoft + single binary.** Credible maintainer and a zero-dependency Go binary make adoption low-friction.

## What didn't work or surprised us

- **Name collision.** Shares the name "Waza" with tw93/Waza (a popular skill suite) — easy to confuse when searching/installing.
- **Young and thin docs.** ~1K stars and early; the eval methodology depth isn't fully proven yet.
- **You must author benchmarks.** Like any eval harness, value depends on writing representative cases — effort that pays off only for skills you maintain seriously.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Benchmarks catch skills that misfire or underperform before reliance |
| Speed | neutral | Adds an eval step to skill development |
| Maintainability | + | Regression-tests skills across model changes |
| Safety | neutral | Quality tooling; no direct safety effect |
| Cost Efficiency | + | Free/OSS; avoids shipping low-value skills |

## Verdict

**discovery-log — tentative read**

Adopt if you author or maintain agent skills seriously and want to benchmark their effectiveness across models rather than trusting vibes — the skills equivalent of an eval harness. For one-off personal skills it's overkill; the value is in regression-testing a skill library. Overlaps skill-creator's eval features — pick by whether you want a standalone cross-model benchmarker (this) or integrated authoring+eval (skill-creator).

## Triage note

Left at `discovery-log`, not SKIPped. The eval frames it as a genuine pick-one against
[`skill-creator`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator)
(STACK) — "a standalone cross-model benchmarker (this) or integrated authoring+eval
(skill-creator)" — and on this repo's own terms the standalone side is not obviously the loser.

The differentiator is *cross-model*: skill-creator's harness measures a skill against Claude, while
this benchmarks the same skill across models and compares. That is precisely the instrument the
[#38](https://github.com/mattbutlerengineering/ai-tooling/issues/38) skill-measurement backlog and
`evaluations/measurement-protocols.md` are asking for, in a repo that gates on
`--skills`/`--skill-design` counts and authors its own skills.

"Overkill for one-off personal skills" is the eval's own caveat and it is fair; this repo maintains
a skill library, which is the case the eval says the value is in. Worth exercising, which is P0
work — not a bulk SKIP.

Not to be confused with `Waza` (tw93), the engineering-habits skill suite, which this pass SKIPped
as redundant with superpowers.

_Triaged 2026-08-04 by the P2 challenger band ([#263](https://github.com/mattbutlerengineering/ai-tooling/issues/263))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [waza (Microsoft)](https://github.com/microsoft/waza) | tool | CLI/framework for evaluating agent skills (MIT, by Microsoft; not to be confused with tw93/Waza) — scaffold eval suites, run benchmarks, and compare results across models to measure and improve skill quality | Skills are written by vibes with no quality signal; want to benchmark and compare skill effectiveness like code under test | skill-creator, evaluate-tool, tdd-guard, promptfoo |
