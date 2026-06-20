# Evaluation: Portkey-gateway

**Repo:** [Portkey-AI/gateway](https://github.com/Portkey-AI/gateway)
**Stars:** ~12,100 | **Last updated:** 2026-05-25 | **License:** MIT
**Dev loop stage:** Implement (AI gateway)
**Layer:** Infrastructure

---

## What it does

An open-source AI gateway that routes to 1,600+ LLMs (language, vision, audio, image) through one fast, OpenAI-compatible API — with **integrated guardrails**. The differentiator versus a plain gateway is the bundled 50+ AI guardrails alongside routing.

Per the README, it's lightweight and fast: <1ms latency overhead and a ~122kb footprint, battle-tested at 10B+ tokens/day. Core capabilities include unified routing across providers, automatic retries and fallbacks, load balancing, caching, and the guardrails layer (input/output checks). It's enterprise-ready with security/scale/custom deployment options, self-hostable or hosted, and integrates in "under 2 minutes." (Gateway 2.0 is merging the enterprise core into open source.)

## How we tested it

Architecture review against the README and the feature set (1,600+ model routing, retries/fallbacks, load balancing, caching, 50+ guardrails). Confirmed the OpenAI-compatible single-API model, the lightweight/fast positioning, and the guardrails integration that sets it apart from pure gateways. The latency/footprint/throughput numbers are vendor-published. Not load-tested live, so condition-gated.

```bash
gh api repos/Portkey-AI/gateway --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/Portkey-AI/gateway/readme --jq '.content' | base64 -d
```

## What worked

- **Gateway + guardrails together.** Bundling 50+ guardrails into the routing layer means safety checks happen at the same chokepoint as provider routing — less glue than gateway + separate guardrail SDK.
- **Lightweight and proven.** <1ms overhead, tiny footprint, and 10B+ tokens/day battle-testing make it credible for production routing.
- **MIT + broad model support.** Permissive license and 1,600+ models via one OpenAI-compatible API ease adoption and avoid lock-in.

## What didn't work or surprised us

- **Vendor-published perf numbers.** Verify <1ms/122kb/10B-tokens claims on your traffic.
- **Overlaps bifrost/litellm/Helicone.** The gateway space is crowded; Portkey's edge is the integrated guardrails (vs. bifrost's raw speed, litellm's ecosystem, Helicone's observability).
- **Enterprise gating in flux.** Gateway 2.0 is merging enterprise features into OSS — confirm what's open in the version you deploy.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Guardrails catch unsafe/malformed I/O at the gateway |
| Speed | + | <1ms claimed overhead; caching and load balancing |
| Maintainability | + | One OpenAI-compatible API replaces per-provider SDKs |
| Safety | + | 50+ integrated guardrails at the routing chokepoint |
| Cost Efficiency | + | Caching + load balancing cut spend; pay providers directly |

## Verdict

**CONDITIONAL**

Adopt when you want one fast, self-hostable gateway that unifies many providers **and** enforces guardrails at the same layer, rather than bolting a separate safety SDK onto a plain proxy. If you only need raw routing speed, bifrost competes; if you want deep observability, Helicone. Verify the performance claims and the OSS/enterprise boundary for your deployment.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Portkey-gateway](https://github.com/Portkey-AI/gateway) | tool | Open-source AI gateway with integrated guardrails (MIT, ★12K) — route to 1,600+ LLMs through one fast (<1ms, 122kb) OpenAI-compatible API with 50+ guardrails, retries/fallbacks, load balancing, and caching; self-host or hosted | Want one fast, lightweight gateway that unifies providers AND enforces guardrails/observability, not just routing | bifrost, litellm, Helicone, NeMo-Guardrails |
