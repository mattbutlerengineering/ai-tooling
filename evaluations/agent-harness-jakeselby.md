# Evaluation: agent-harness (JakeSelby)

**Repo:** [JakeSelby/agent-harness](https://github.com/JakeSelby/agent-harness)
**Stars:** 15 | **Last updated:** 2026-09-23 (pushed) | **License:** MIT
**Last verified:** 2026-09-23
**Last triaged:** 2026-09-23  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

An editor-agnostic rule/skill checkout (Python, MIT) for Claude Code and Codex — one checkout of
rules, skills, subagents, slash commands, hooks, and output styles, projected into `AGENTS.md` and
`~/.claude`, with switchable stances for autonomy, testing, delegation, and cost, and rule-fire
detectors that report which configured rules actually influenced a session.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata and
the README's description of the checkout/projection model and rule-fire detectors. That is sufficient
to catalog it and place it relative to existing peers, not to support an ADOPT.

## Verdict

**discovery-log — tentative read**

## Triage note

P3 backlog. Overlaps `superpowers`/`gstack`/`aster` on "curated agent configuration", but its
distinguishing claim — detecting which configured rules actually fire in a session, not just shipping
more of them — isn't covered by any catalogued incumbent. 137 open issues on a 15-star, one-week-old
repo is a lot of self-filed scope/roadmap noise to read through before a hands-on eval; noting it
rather than acting on it. Left at `discovery-log`.

_Triaged 2026-09-23 by the P3 backlog band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [agent-harness](https://github.com/JakeSelby/agent-harness) | harness | Editor-agnostic rule/skill checkout (MIT) for Claude Code and Codex — projects rules, skills, subagents, hooks, and output styles into AGENTS.md/~/.claude with switchable autonomy/testing/delegation/cost stances, and detects which rules actually fire | Agent rule files accumulate with no way to tell which ones influence behavior, and no portable way to switch autonomy/cost posture | superpowers, gstack, aster |  |
