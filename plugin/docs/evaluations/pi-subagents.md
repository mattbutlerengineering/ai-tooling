# Evaluation: pi-subagents

**Repo:** [nicobailon/pi-subagents](https://github.com/nicobailon/pi-subagents)
**Stars:** ~2,260 | **Last updated:** 2026-06-20 | **License:** none specified
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-07-09  <!-- triaged: bulk -->
**Dev loop stage:** Implement (subagent orchestration for Pi)
**Layer:** Tooling

---

## What it does

An extension for the **Pi** coding agent that lets Pi delegate work to focused child agents. It adds async subagent delegation — useful for code review, scouting, implementation, parallel audits, saved workflows, background jobs, and anything that benefits from a second or third set of model eyes.

Per the README, install is one step (`pi install npm:pi-subagents`), with optional pieces added later. Beyond basic delegation it provides **output truncation** (keep subagent results from blowing up the parent context), **artifacts** (structured outputs from child agents), and **session sharing** (children operate with shared session context). It's the parallel/delegated-subagent capability for Pi specifically.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README and the documented features (async delegation, truncation, artifacts, session sharing; one-command install). Confirmed it's a Pi-specific extension for fanning out focused child agents. Note: **no license is specified** on the repo — a real adoption caveat. Not run live, so condition-gated.

```bash
gh api repos/nicobailon/pi-subagents --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/nicobailon/pi-subagents/readme --jq '.content' | base64 -d
```

## What worked

- **Brings parallel subagents to Pi.** Async delegation for review/scouting/parallel audits is the same productivity pattern as Claude Code subagents — valuable for Pi users who lack it natively.
- **Context-hygiene built in.** Truncation + artifacts keep subagent output from flooding the parent context — a thoughtful detail that many delegation tools miss.
- **One-command install.** Low friction (`pi install npm:pi-subagents`), with optional pieces layered later.

## What didn't work or surprised us

- **No license specified.** Absence of a license is a genuine blocker for many users/orgs — clarify before relying on it.
- **Pi-only.** Useful only if you use the Pi coding agent; not portable to other harnesses.
- **Overlaps general subagent patterns.** Claude Code/others already have subagents; this is the Pi-specific implementation, valuable within that ecosystem.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Parallel audits/reviews add independent checks |
| Speed | + | Async delegation fans out work concurrently |
| Maintainability | neutral | An extension; doesn't change your codebase |
| Safety | + | Truncation/artifacts keep parent context clean and bounded |
| Cost Efficiency | - | Multiple child agents multiply token usage |

## Verdict

**SKIP** — no declared license. A skill/plugin is *vendored* — its text is copied into the consuming repo — and text carrying no license grant cannot be copied in.

_Superseded the review-based read below on 2026-07-09 (bulk license triage, P4 mechanical-skip). The read was never wrong about the tool's quality — the licence, not the craft, is disqualifying._

**CONDITIONAL**

Adopt if you use the Pi coding agent and want async, parallel subagent delegation (review, scouting, parallel audits, background jobs) with sensible context hygiene (truncation/artifacts/session sharing). The missing license is a real caveat — clarify it before depending on the tool. Not relevant outside Pi; for other harnesses, use their native subagent mechanisms.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [pi-subagents](https://github.com/nicobailon/pi-subagents) | plugin | Async subagent delegation for the Pi coding agent (no explicit license) — delegate to focused child agents for review, scouting, implementation, parallel audits, saved workflows, and background jobs, with output truncation, artifacts, and session sharing | Pi lacks built-in parallel subagent delegation; want to fan out focused child-agent work with managed artifacts and shared sessions | claude-octopus, agency-agents, phantom, orca |
