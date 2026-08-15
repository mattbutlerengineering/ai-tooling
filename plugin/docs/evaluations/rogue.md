# Evaluation: rogue

**Repo:** [rogue-security/rogue](https://github.com/rogue-security/rogue) (transferred from `qualifire-dev/rogue`)
**Stars:** ~1,040 | **Last updated:** 2026-05-04 | **License:** source-available (repo SPDX returns NOASSERTION)
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Reflect (agent evaluation + red-teaming / Outer Loop)
**Layer:** Tooling

---

## What it does

An AI-agent **evaluator and red-team platform** — "stress-test your AI agents before attackers do." Rogue offers two complementary modes of hardening.

Per the README: **Automatic Evaluation** tests your agent against **business policies** and expected behaviors — you define scenarios and expected outcomes, and it verifies the agent complies with your business rules. The **red-team** side runs adversarial scenarios against the agent to probe for unsafe, non-compliant, or exploitable behavior. Together they cover "does the agent do what it should" (compliance) and "can the agent be made to misbehave" (adversarial), in one platform.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README and the two-mode model (policy/expected-behavior evaluation + adversarial red-team). Confirmed the scenario-definition + compliance-verification flow and the red-team positioning. License resolves to NOASSERTION via the API — confirm exact terms before commercial reliance. Last push ~2026-05. Not run against a live agent, so condition-gated.

```bash
gh api repos/qualifire-dev/rogue --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/qualifire-dev/rogue/readme --jq '.content' | base64 -d
```

## What worked

- **Compliance + adversarial in one.** Pairing business-policy evaluation with red-team scenarios covers both "is it correct/compliant" and "is it attackable" — most tools do only one.
- **Scenario-driven.** Defining scenarios and expected outcomes makes evaluation explicit and repeatable, suitable for CI gating before deploy.
- **Targets the agent, pre-deploy.** Hardening an agent before shipping is the right place to catch policy/safety failures.

## What didn't work or surprised us

- **License unresolved.** NOASSERTION — pin terms before relying on it.
- **Overlaps garak/superagent/promptfoo.** garak red-teams LLMs, promptfoo evals+red-teams, superagent guards at runtime; Rogue's niche is agent-level compliance + red-team evaluation. Evaluate whether you want this bundle or composed pieces.
- **You author the scenarios.** Coverage depends on the business rules and adversarial cases you define.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Policy/expected-behavior checks catch compliance regressions |
| Speed | neutral | Adds an evaluation stage pre-deploy |
| Maintainability | + | Scenario suites regression-test agent behavior over changes |
| Safety | + | Adversarial red-team probes uncover unsafe/exploitable behavior |
| Cost Efficiency | ✓/$ | OSS core; red-team/eval runs consume model calls |

## Verdict

**discovery-log — tentative read**

Adopt to harden an agent before deployment when you need both business-policy compliance evaluation and adversarial red-teaming in one scenario-driven platform. Pin the license terms. Overlaps garak (LLM red-team), promptfoo (eval+red-team), and superagent (runtime guard) — choose Rogue for the agent-level compliance-plus-adversarial bundle, or compose best-of-breed.

## Triage note

Left at `discovery-log`. Scenario-driven agent hardening that bundles two things usually bought
separately: business-policy compliance evaluation and adversarial red-teaming.

The licence is the reason to look and not the reason to dispose. `repo-metadata.json` records
**`NOASSERTION`** and the eval's own advice is *"pin the license terms"* — an instruction that was never
carried out, and which per CLAUDE.md means GitHub could not parse the file rather than that no grant
exists. Two rows in the previous slice showed both outcomes (`Memori` was Apache-2.0 all along; `sentry`
appears to be a source-available FSL), so guessing is not available to this lane.

Not disposed as redundant either. It overlaps `garak` (LLM red-teaming), `promptfoo` (eval plus red-team)
and `superagent` (runtime guarding), and the compliance-plus-adversarial bundle is a distinct offer —
the same bundle-versus-compose choice that runs through this whole cluster.

★1.1K and pushed 2026-05-04, so it is the smallest and quietest of the group. Licence first, then a
measured comparison against garak.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [rogue](https://github.com/rogue-security/rogue) | tool | AI-agent evaluator + red-team platform (★1K; SPDX unverified) — automatic evaluation against business policies/expected behaviors plus adversarial red-team scenarios that probe for unsafe or non-compliant agent behavior | Agents may violate business rules or break under adversarial input; want compliance evaluation and red-teaming in one platform | garak, superagent, promptfoo, NeMo-Guardrails |
