# Watchlist — what to revisit, and when

Everything worth re-evaluating or watching, **derived** (not hand-maintained) from data already in the repo: DEFER verdicts and their triggers, the STACK prose flags, the staleness sweep, and the unverified-claim / skill-measurement backlogs. Regenerate with `python3 watchlist.py`; do not edit between the markers. For *first-time* evaluation priorities see [NEXT-EVALS.md](NEXT-EVALS.md); this page is for *revisiting* work already started.

<!-- WATCHLIST:START -->

## 1. Deferred — re-evaluate when trigger fires (3)

`DEFER` rows from [COMPARISON.md](COMPARISON.md): promising but blocked, each with the re-evaluate trigger from its eval's `## Verdict` (per TEMPLATE.md's DEFER definition). A missing trigger is itself an action item.

| Tool | Stage | Re-evaluate when |
|------|-------|------------------|
| Apache DevLake | Outer Loop | working in a team context or when managing multiple repos with CI/CD pipelines |
| letta | Memory & Context | trigger not recorded — add one |
| SkillOpt | Skills & Plugins | trigger not recorded — add one |

## 2. Flagged for hands-on before promotion (3)

Candidates the [STACK.md](STACK.md) prose flags for a hands-on eval before any promotion — surfaced by scanning STACK for its flag phrases (fragile by design; the durable fix is a machine-readable column in STACK-LEDGER.md).

| Tool | Flagged as |
|------|------------|
| worktrunk | pending a hands-on eval |
| [code-on-incus](https://github.com/mensfeld/code-on-incus) | flagged for a hands-on eval |
| [brooks-lint](https://github.com/hyhmrright/brooks-lint) | flagged for a hands-on eval |

## 3. Stale / undated evals (0 stale)

A point-in-time eval rots. The staleness sweep flags evals whose `**Last verified:**` date is older than its category threshold; ages are not printed so the page stays deterministic (`make fix` regenerates when a date crosses a threshold).

| Eval | Type | Last verified | Threshold (days) |
|------|------|---------------|------------------|
| _none stale_ | | | |

_0 eval(s) carry no `**Last verified:**` date (field presence is gated separately by `backfill-lastverified.py`)._

## 4. Unverified claims & measurement backlog (18)

**Unverified token-savings claims (15).** CATALOG rows with a numeric token-savings headline whose eval is not run-backed (`MEASURED`/`RUN`). Run the token-savings protocol to verify, or add an in-row disclaimer.

| Tool | Evidence | Disclaimer in row? |
|------|----------|--------------------|
| ACE (agentic-context-engine) | REVIEW | no |
| claude-code-memory-setup | REVIEW | yes |
| claw-compactor | REVIEW | no |
| cocoindex-code | REVIEW | no |
| code-context-engine | REVIEW | no |
| context-mode | REVIEW | no |
| GenericAgent | REVIEW | no |
| gortex | REVIEW | no |
| h5i | (no eval) | no |
| MemOS | REVIEW | no |
| OmniRoute | (no eval) | yes |
| rtk | REVIEW | no |
| semble | REVIEW | no |
| SocratiCode | REVIEW | no |
| token-optimizer-mcp | REVIEW | no |

**ADOPT skills lacking measured backing (3).** ADOPT-verdict skill evals not yet graduated to a measured run (#38): agent-skills-addyosmani, cc-skills-golang, vercel-labs-agent-skills.

<!-- WATCHLIST:END -->
