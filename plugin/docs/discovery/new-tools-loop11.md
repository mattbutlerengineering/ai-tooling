# New Tools Evaluation (Loop 11-12)

Tools discovered via skills.sh leaderboard, web research on DORA metrics, and GitHub search. Evaluated against dev loop stages and quality signals.

## Apache DevLake

**Repo:** [apache/incubator-devlake](https://github.com/apache/incubator-devlake)
**Stars:** 3,038 | **Last updated:** 2026-06-16 | **License:** Apache-2.0
**Stage:** Ship (inner loop), Retrospect (outer loop)
**Layer:** Infrastructure
**Signals:** Speed, Correctness, Safety

**What it does:** Open-source dev data platform that ingests data from GitHub, GitLab, Jira, Jenkins, and more, then visualizes it through pre-built Grafana dashboards. Tracks DORA metrics out of the box: deployment frequency, lead time, change failure rate, MTTR. Also tracks engineering throughput and community growth.

**Why it matters for our workflow:** We identified a gap — the infrastructure layer for Ship and Retrospect has no drop-in tool. PR acceptance rates, delivery stability, and MTTR all need tracking, and our workflow currently says "build this yourself." DevLake is the closest thing to a turnkey solution.

**Overlaps with:** langfuse (both are observability, but langfuse tracks LLM behavior while DevLake tracks delivery metrics — complementary, not competing)

**Risks:**
- 3K stars — modest community for an Apache project
- Requires Docker + Grafana — nontrivial setup overhead for solo developers
- Designed for teams — may be over-engineered for a solo dev workflow
- For solo devs, a simple `gh` script that queries PR merge rates might suffice

**Verdict:** CONDITIONAL — add to Infrastructure layer for teams. For solo developers, the setup overhead may exceed the value. Recommend at the Autonomy adoption tier where delivery volume justifies the infrastructure investment.

## AI Code Churn Rate (metric concept)

**Source:** [DX research](https://getdx.com/blog/dora-metrics-tools/), [Oobeya analysis](https://oobeya.io/blog/dora-metrics-not-enough-2026)
**Stage:** Ship, Retrospect
**Layer:** Infrastructure (measurement)
**Signals:** Correctness, Speed

**What it is:** The rate at which recently written AI-assisted code gets deleted or substantially rewritten. Research shows AI-generated code has pushed throughput up 30-40% but doubled code churn and dropped delivery stability by 7.2%. Standard DORA metrics don't capture this.

**Why it matters for our workflow:** High speed + high churn = generating throwaway code. This is a failure mode our five quality signals should catch but currently don't explicitly name. A team could show improving Speed (faster time-to-merge) while Correctness is actually declining (the merged code gets reverted or rewritten within days).

**How to measure:** `git log --diff-filter=M --since="30 days ago" -- <files touched by AI>` compared to overall change volume. Track the ratio of "code written in the last 7 days that was modified again within 7 days."

**Verdict:** ADD as a metric to track under the Speed signal's feedback arc. Not a tool — a measurement practice. High churn is the canary that Speed is masking quality problems.

## DX Core 4 Framework (reference)

**Source:** [DX (getdx.com)](https://getdx.com/blog/dora-metrics/)
**Stage:** Cross-cutting
**Layer:** Reference

**What it is:** A balancing model organized around Speed, Effectiveness, Quality, and Business Impact. Prevents metric gaming by requiring simultaneous optimization across all dimensions. Used by elite engineering teams alongside DORA.

**How it maps to our signals:**
| DX Core 4 | Our Signal |
|-----------|-----------|
| Speed | Speed |
| Effectiveness | Speed + Cost Efficiency |
| Quality | Correctness + Maintainability + Safety |
| Business Impact | (not covered — out of scope for code quality workflow) |

**Verdict:** REFERENCE — our five signals already cover three of four DX dimensions. Business Impact is intentionally out of scope (we measure code quality, not business outcomes). Worth noting in WORKFLOW.md as prior art.

## Skills.sh Leaderboard (audit)

Checked top 20 most-installed skills (2.1M to 252K installs). All relevant skills already in our workflow:
- find-skills (2.1M) — installed
- frontend-design (553K) — Anthropic, installed
- agent-browser (455K) — Vercel Labs, installed
- grill-me (327K) — mattpocock/skills, recommended
- improve-codebase-architecture (267K) — mattpocock/skills, recommended
- grill-with-docs (262K) — mattpocock/skills, recommended
- caveman (254K) — recommended
- tdd (252K) — mattpocock/skills, recommended

No leaderboard gaps found.
