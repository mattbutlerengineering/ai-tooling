# Evaluation: claude-red

**Repo:** [0xwilliamortiz/claude-red](https://github.com/0xwilliamortiz/claude-red)
**Stars:** 352 | **Last updated:** 2026-08-05 (pushed) | **License:** MIT
**Last verified:** 2026-08-06
**Last triaged:** 2026-08-06  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

Curated library of offensive-security skills for **authorized** engagements — structured SKILL.md files priming Claude with expert methodology per attack surface (SQLi, shellcode, EDR evasion, exploit development).

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata (README, topics, license) via the GitHub API, plus the CATALOG "Overlaps with" cell.

## Verdict

**SKIP** — the repo and its author account (`0xwilliamortiz`) are both gone (404 via the GitHub
API) as of 2026-08-15, caught by the link-rot sweep after detector C moved onto authenticated
`gh api` (#498). Nothing left to install or evaluate, and no successor is evident.

_Triaged 2026-08-15 after the account/repo was found gone during a repo audit._

## Triage note (superseded)

Previously left at `discovery-log` (triaged 2026-08-06): overlapped `pentest-ai-agents` (already
SKIPped — not a settled incumbent to be redundant with) and `Claude-BugHunter`/`ctf-skills`, both
themselves unevaluated leads. Moot now that the repo is gone.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-red](https://github.com/0xwilliamortiz/claude-red) | skill | Curated library of offensive-security skills for **authorized** engagements (MIT) — structured SKILL.md files priming Claude with expert methodology per attack surface, from SQLi to EDR evasion to exploit development | Offensive-security testing needs per-attack-surface expertise; want it as installable Claude skills instead of ad-hoc prompting | pentest-ai-agents, Claude-BugHunter, ctf-skills |
