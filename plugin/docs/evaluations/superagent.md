# Evaluation: superagent

**Repo:** [superagent-ai/superagent](https://github.com/superagent-ai/superagent)
**Stars:** ~6,600 | **Last updated:** 2026-04-11 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Reflect (agent safety / Outer Loop)
**Layer:** Tooling

---

## What it does

An open-source SDK for AI **agent safety** — "make your AI apps safe." Superagent embeds protection directly into your app and produces compliance evidence for customers.

Per the README, the core component is **Guard**: at runtime it detects and blocks prompt injections, malicious instructions, and unsafe tool calls. Beyond that it redacts PII and secrets, scans repositories for threats, and runs red-team scenarios against your agent. It ships TypeScript (and Python) SDKs so you wrap your agent's inputs/outputs/tool calls with the guard layer. The positioning combines runtime defense (block bad inputs/actions) with proactive assurance (repo scanning + red-teaming) and compliance reporting.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README and the feature set (Guard runtime blocking, PII/secret redaction, repo threat scanning, red-team scenarios). Confirmed the SDK integration model (TypeScript/Python wrapping agent I/O and tool calls) and the dual runtime-defense + red-teaming positioning. Last push ~2026-04. Not integrated into a live agent, so condition-gated.

```bash
gh api repos/superagent-ai/superagent --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/superagent-ai/superagent/readme --jq '.content' | base64 -d
```

## What worked

- **Agent-specific threat model.** Blocking prompt injection and **unsafe tool calls** at runtime targets exactly the attack surface that generic content filters miss.
- **Defense + red-teaming in one.** Pairing runtime Guard with red-team scenarios and repo scanning covers both "stop attacks now" and "find weaknesses proactively."
- **Embeddable SDK.** TS/Python wrapping makes it practical to add to an existing agent without a separate gateway.

## What didn't work or surprised us

- **Overlaps NeMo-Guardrails/presidio/garak.** Runtime guard ≈ NeMo; PII redaction ≈ presidio; red-teaming ≈ garak/promptfoo. Superagent's pitch is bundling these for agents — evaluate whether you want one bundle or best-of-breed pieces.
- **Detection limits.** Prompt-injection detection is an arms race; expect false positives/negatives and tune accordingly.
- **Compliance framing.** "Prove compliance" is a product angle; verify what evidence it actually produces for your requirements.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Safety layer; doesn't change task correctness |
| Speed | - | Runtime guard adds an interception step per call |
| Maintainability | + | One SDK centralizes agent safety vs. scattered checks |
| Safety | + | Blocks injection/unsafe tool calls, redacts PII/secrets, red-teams |
| Cost Efficiency | neutral | OSS; detection may add model calls |

## Verdict

**discovery-log — tentative read**

Adopt when you ship an agent with tool access and want bundled runtime protection (prompt-injection + unsafe-tool-call blocking + PII/secret redaction) plus red-teaming in one SDK. If you prefer best-of-breed, compose NeMo-Guardrails (dialog rails) + presidio (PII) + garak (red-team) instead. Tune detection thresholds and verify the compliance evidence fits your needs.

## Triage note

Left at `discovery-log`. The bundle is the pitch: prompt-injection blocking, unsafe-tool-call
interception, and PII/secret redaction in one SDK, with red-teaming alongside. MIT, ★6.7K.

Its own eval names the alternative honestly — compose `NeMo-Guardrails` for dialog rails, `presidio` for
PII, `garak` for red-teaming — which is the bundle-versus-best-of-breed choice, and neither answer is
this lane's to write. All four rows were left standing in this pass for that reason.

The one thing that would settle it is a measurement rather than an argument: detection thresholds are
tunable, and a guardrail is only worth its latency if the false-positive rate is low enough that people
leave it on. That is a with/without run on a disclosed set of injection attempts and benign prompts,
which `evaluations/measurement-protocols.md` already describes how to do.

Pushed 2026-04-11 — nearly four months, worth a freshness check but not yet a concern for a security SDK.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [superagent](https://github.com/superagent-ai/superagent) | tool | AI-agent safety SDK (MIT, ★6.6K) — runtime Guard blocks prompt injections, malicious instructions, and unsafe tool calls, redacts PII/secrets, scans repos for threats, and runs red-team scenarios; TypeScript/Python | Agents are exposed to prompt injection, data leaks, and unsafe tool use; want embedded runtime protection plus red-teaming | NeMo-Guardrails, presidio, garak, vet |
