# Evaluation: kodus-ai

**Repo:** [kodustech/kodus-ai](https://github.com/kodustech/kodus-ai)
**Stars:** ~1,200 | **Last updated:** 2026-06-19 | **License:** open-core (repo LICENSE returns NOASSERTION; Open Source / Teams / Enterprise tiers)
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A self-hostable AI code-review platform ("Kody"). It reviews pull requests with an LLM and posts feedback directly in the PR across GitHub, GitLab, Bitbucket, and Azure Repos, and also runs from a CLI in CI/CD.

The distinguishing design choices, per the README:
- **Model-agnostic with zero LLM-cost markup** — use Claude, GPT-5, Gemini, Llama, GLM, Kimi, or any OpenAI-compatible endpoint, and pay the model provider directly (no hidden multipliers).
- **Custom rules in plain language** — you define review rules in natural language, and Kody adapts to your architecture/standards over time (context-learning).
- **Privacy/self-host** — source code isn't used to train models; data encrypted in transit/at rest; self-hosted runners supported; self-hosted instances send one anonymous daily heartbeat (aggregated counters, opt-out via `KODUS_TELEMETRY_DISABLED=true`).
- **Operational metrics** — tracks technical debt and delivery metrics alongside review quality.

It's a monorepo (NestJS-style `apps/api`, `apps/webhooks`, `apps/worker`, Next.js `apps/web`) with Cloud and self-hosted (Docker/Railway) editions.

## How we tested it

Architecture review against the README, the monorepo structure, the deployment options (Cloud, Docker, Railway), and the open-core tier split. Confirmed the model-agnostic/no-markup billing model, plain-language custom rules, the multi-platform PR integration, CLI/CI support, and the telemetry/privacy posture. License is unresolved at the API level (NOASSERTION) — it's open-core with paid Teams/Enterprise tiers; treat the OSS scope as "self-hostable core, gated advanced features." Not run on a live PR, so condition-gated.

```bash
gh api repos/kodustech/kodus-ai --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/kodustech/kodus-ai/readme --jq '.content' | base64 -d
```

## What worked

- **You own the model and the bill.** Bring any provider/endpoint and pay them directly — no per-review markup. For teams already on a Claude/GPT contract, that's a real cost-control lever versus closed SaaS reviewers.
- **Plain-language org rules + context-learning.** Encoding your standards in natural language and having the reviewer adapt addresses the "generic reviewer misses our conventions" problem.
- **Self-host + clear privacy stance.** Self-hosted runners, encryption, no-training guarantee, and opt-out telemetry suit privacy-sensitive orgs.

## What didn't work or surprised us

- **Open-core, license unclear.** The API reports NOASSERTION and the README routes to a paid pricing page; the boundary between OSS and Teams/Enterprise needs checking before you rely on a feature.
- **Operational weight.** It's a multi-service monorepo (api/webhooks/worker/web) — self-hosting is a real deployment, not a CLI drop-in like skylos.
- **Crowded review space.** Overlaps claude-octopus, vet, brooks-lint, and the built-in /code-review; the edge is self-host + model control + org rules.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | LLM PR review against org-specific, plain-language rules |
| Speed | + | Automated PR feedback + CI gate shortens review latency |
| Maintainability | + | Tracks tech debt and delivery metrics over time |
| Safety | + | Self-host, encryption, no-training, opt-out telemetry |
| Cost Efficiency | ✓/$ | No LLM markup (pay providers); advanced tiers are paid |

## Verdict

**CONDITIONAL**

Adopt when a team wants a self-hosted PR reviewer with full model choice, direct provider billing, and org-specific rules — and can run a multi-service deployment. For a solo dev or quick local checks, the built-in /code-review or a single-binary tool (skylos) is lighter. Confirm the OSS/paid feature boundary before standardizing.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [kodus-ai](https://github.com/kodustech/kodus-ai) | platform | Self-hostable AI code review (open-core) — model-agnostic PR reviews with zero LLM-cost markup, plain-language custom rules, context-learning, native GitHub/GitLab/Bitbucket/Azure + CLI/CI | Want a self-hosted PR reviewer where you control the model, pay providers directly, and enforce org rules | claude-octopus, vet, brooks-lint, code-review |
