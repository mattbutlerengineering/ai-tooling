# Evaluation: rogue

**Repo:** [qualifire-dev/rogue](https://github.com/qualifire-dev/rogue)
**Stars:** ~1,040 | **Last updated:** 2026-05-04 | **License:** source-available (repo SPDX returns NOASSERTION)
**Dev loop stage:** Reflect (agent evaluation + red-teaming / Outer Loop)
**Layer:** Tooling

---

## What it does

An AI-agent **evaluator and red-team platform** — "stress-test your AI agents before attackers do." Rogue offers two complementary modes of hardening.

Per the README: **Automatic Evaluation** tests your agent against **business policies** and expected behaviors — you define scenarios and expected outcomes, and it verifies the agent complies with your business rules. The **red-team** side runs adversarial scenarios against the agent to probe for unsafe, non-compliant, or exploitable behavior. Together they cover "does the agent do what it should" (compliance) and "can the agent be made to misbehave" (adversarial), in one platform.

## How we tested it

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

**CONDITIONAL**

Adopt to harden an agent before deployment when you need both business-policy compliance evaluation and adversarial red-teaming in one scenario-driven platform. Pin the license terms. Overlaps garak (LLM red-team), promptfoo (eval+red-team), and superagent (runtime guard) — choose Rogue for the agent-level compliance-plus-adversarial bundle, or compose best-of-breed.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [rogue](https://github.com/qualifire-dev/rogue) | tool | AI-agent evaluator + red-team platform (★1K; SPDX unverified) — automatic evaluation against business policies/expected behaviors plus adversarial red-team scenarios that probe for unsafe or non-compliant agent behavior | Agents may violate business rules or break under adversarial input; want compliance evaluation and red-teaming in one platform | garak, superagent, promptfoo, NeMo-Guardrails |
