# Evaluation: HERO-Anti-OverDefense

**Repo:** [wanshuiyin/HERO-Anti-OverDefense](https://github.com/wanshuiyin/HERO-Anti-OverDefense)
**Stars:** 76 | **Last updated:** 2026-08-11 (pushed) | **License:** MIT
**Last verified:** 2026-08-11
**Last triaged:** 2026-08-11  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Process

---

## What it does

A paste-in contract (MIT, Markdown-only) naming the four shapes coding agents over-defend in — Hashing, Edge cases, Rubrics, Overbuild (HERO) — and instructing the agent to stop doing them. Works with Claude Code, Codex, Antigravity, Cursor, Copilot, Windsurf, Gemini CLI.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata and README/topic description. Whether the contract actually curbs over-engineering in practice, versus just adding more instructions an agent may or may not follow, is untested here.

## Verdict

**discovery-log — tentative read**

## Triage note

Newly discovered and catalogued today. Left at `discovery-log` — the same behavior-shaping niche as `pristine-skill` (First-Time Principle) and `ratchet` (mid-session drift grading), but targeting a distinct failure mode (defensive over-engineering rather than incompleteness/drift), so not a clean redundancy SKIP against either.

_Triaged 2026-08-11 by the daily discovery-and-triage pass._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [HERO-Anti-OverDefense](https://github.com/wanshuiyin/HERO-Anti-OverDefense) | skill | Paste-in contract (MIT) stopping the four shapes coding agents over-defend in — hashing, edge cases, rubrics, overbuild | Agents over-engineer defenses nobody asked for, bloating diffs and hiding the real change | pristine-skill, ratchet, tdd-guard |
