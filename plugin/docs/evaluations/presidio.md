# Evaluation: presidio

**Repo:** [microsoft/presidio](https://github.com/microsoft/presidio)
**Stars:** ~9,250 | **Last updated:** 2026-06-18 | **License:** MIT
**Dev loop stage:** Reflect (data protection / Outer Loop)
**Layer:** Infrastructure

---

## What it does

A data-protection and de-identification SDK from Microsoft. Presidio provides context-aware **identification** and **anonymization** of private entities (PII) — names, credit card numbers, SSNs, locations, phone numbers, bitcoin wallets, financial data, and more — across text, images, and structured data.

Mechanically it's a pluggable pipeline: **analyzers** detect PII using a mix of NLP (NER models), regex/pattern matching, context words, and checksums; **anonymizers** then redact, mask, replace, hash, or encrypt the detected entities. Everything is customizable — you can add recognizers for domain-specific identifiers, swap NLP engines, and tune the pipeline. For an LLM workflow, Presidio sits at the boundary: scrub PII out of prompts/logs/training data before they reach a model or a store, and optionally re-identify on the way back.

## How we tested it

Architecture review against the README and the analyzer/anonymizer pipeline model. Confirmed the multi-modal coverage (text/image/structured), the pluggable recognizer architecture (NLP + pattern + context), and the customization story. Presidio is a mature, widely-used Microsoft OSS project. Not wired into a live pipeline, so condition-gated.

```bash
gh api repos/microsoft/presidio --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/microsoft/presidio/readme --jq '.content' | base64 -d
```

## What worked

- **Purpose-built PII boundary.** A dedicated, mature SDK for detecting and anonymizing PII is the right primitive for keeping sensitive data out of prompts, logs, and training sets.
- **Pluggable and customizable.** Add domain-specific recognizers, swap NLP engines, choose redact/mask/hash/encrypt — adapts to real compliance requirements rather than a fixed ruleset.
- **Multi-modal.** Covers text, images, and structured data — broader than regex-only secret scanners.

## What didn't work or surprised us

- **Not LLM-specific.** It's a general PII SDK; you must integrate it into your agent/prompt pipeline (it's not a drop-in guardrail like NeMo-Guardrails/superagent).
- **Detection isn't perfect.** NER + patterns miss novel/contextual PII and can over-redact; tuning recognizers is real work for high-stakes use.
- **Operational integration.** Value requires wiring it at the right boundaries (ingress/egress) — a design task, not a config flag.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Protects data; doesn't affect code correctness directly |
| Speed | neutral | Adds a scan step at boundaries |
| Maintainability | + | Centralizes PII handling in a pluggable, testable pipeline |
| Safety | + | Detects/redacts/anonymizes PII before it reaches models or stores |
| Cost Efficiency | + | Free/OSS; avoids costly data-leak incidents |

## Verdict

**CONDITIONAL**

Adopt when your AI workflow handles PII and you need to detect/redact/anonymize it before prompts, logs, or training data leave a trusted boundary — the mature, customizable choice for the PII problem specifically. Pair it with runtime guardrails (NeMo-Guardrails/superagent) which handle prompt-injection/unsafe-output rather than PII. Budget for recognizer tuning in high-stakes contexts.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [presidio](https://github.com/microsoft/presidio) | tool | PII de-identification SDK (MIT, ★9.2K, by Microsoft) — context-aware identification + anonymization of private entities across text, images, and structured data via NLP + pattern matching + customizable pipelines | LLM prompts/logs/training data leak PII; want to detect, redact, mask, or anonymize sensitive data before it reaches a model or store | superagent, NeMo-Guardrails, ghostsecurity/skills |
