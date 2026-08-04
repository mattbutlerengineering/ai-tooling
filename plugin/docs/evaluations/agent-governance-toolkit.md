# Evaluation: agent-governance-toolkit

**Repo:** [microsoft/agent-governance-toolkit](https://github.com/microsoft/agent-governance-toolkit)
**Stars:** ~4,430 | **Last updated:** 2026-06-19 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Reflect (agent governance / Outer Loop)
**Layer:** Infrastructure

---

## What it does

An AI Agent Governance Toolkit from Microsoft for shipping autonomous agents to production safely. It covers four pillars: **policy enforcement**, **zero-trust identity**, **execution sandboxing**, and **reliability engineering** — and explicitly maps to all of the **OWASP Agentic Top 10** risks ("ship agents to production without losing sleep").

Mechanically it provides specifications and components (PyPI package) to put governance around an autonomous agent: enforce policies on what an agent may do, give agents zero-trust identities, sandbox their execution, and apply reliability-engineering practices — i.e., the operational controls an agent needs in production that a bare agent loop doesn't provide. The OWASP Agentic Top 10 coverage gives it a concrete, externally-defined checklist rather than ad-hoc safety.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README and the four governance pillars (policy enforcement, zero-trust identity, execution sandboxing, reliability engineering) plus the OWASP Agentic Top 10 mapping. Confirmed the production-governance framing and the PyPI delivery. Not integrated into a live agent, so condition-gated.

```bash
gh api repos/microsoft/agent-governance-toolkit --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/microsoft/agent-governance-toolkit/readme --jq '.content' | base64 -d
```

## What worked

- **Governance as a structured discipline.** Policy + identity + sandboxing + reliability, mapped to the OWASP Agentic Top 10, turns "agent safety" from vibes into a checklist you can verify against.
- **Production-focused + credible.** Microsoft-maintained, MIT, aimed squarely at the gap between a working agent and a *deployable* one (identity, policy, reliability).
- **Complements runtime guards.** Where NeMo-Guardrails/superagent guard model I/O, this covers identity, sandboxing, and reliability — the operational governance layer.

## What didn't work or surprised us

- **Adoption is real work.** Zero-trust identity, policy enforcement, and sandboxing are infrastructure commitments, not a library you drop in for free.
- **For teams shipping agents to prod.** Most relevant when you actually deploy autonomous agents at scale; overkill for personal/local agent use.
- **Overlaps guardrail tools partially.** Sandboxing overlaps daytona/agent-sandbox; runtime policy overlaps NeMo-Guardrails/superagent — this is the governance umbrella over those.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Reliability engineering reduces flaky/unreliable agent behavior |
| Speed | neutral | Governance layer; not a runtime speed change |
| Maintainability | + | Structured, OWASP-mapped governance vs. ad-hoc controls |
| Safety | + | Policy, zero-trust identity, sandboxing — covers OWASP Agentic Top 10 |
| Cost Efficiency | neutral | OSS; governance infra has setup/operational cost |

## Verdict

**discovery-log — tentative read**

Adopt when you're deploying autonomous agents to production and need real governance — policy enforcement, zero-trust identity, execution sandboxing, and reliability — mapped to the OWASP Agentic Top 10 rather than assembled ad hoc. It's an infrastructure commitment, best for teams shipping agents at scale. Complements runtime guardrails (NeMo-Guardrails/superagent) and sandboxes (daytona/agent-sandbox) as the governance umbrella over them.

## Triage note

Left at `discovery-log`. Microsoft, MIT, ★4.7K, pushed this week — policy enforcement, zero-trust identity,
execution sandboxing and reliability, mapped to the **OWASP Agentic Top 10** rather than assembled ad hoc.

The mapping is the part that makes it more than another safety row. A named external threat model turns a
governance story into something a reviewer can check off, which is a Verifiability property — the sixth
quality signal this catalog added — and it is rare in this category.

Not disposed, because it sits *above* the tools it overlaps rather than beside them: `NeMo-Guardrails` and
`superagent` are runtime rails, `daytona` and `agent-sandbox` are isolation, and this is the governance
umbrella over both. Umbrella-versus-component is not a redundancy relation.

The honest scope note is that it is an infrastructure commitment aimed at teams shipping autonomous agents
to production. For a developer running a coding agent locally it is heavy machinery for a threat model they
do not have — which is a condition on the reader, not a defect in the tool, and exactly why it is neither
ADOPT-everywhere nor SKIP.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agent-governance-toolkit](https://github.com/microsoft/agent-governance-toolkit) | framework | AI-agent governance toolkit (MIT, by Microsoft) — policy enforcement, zero-trust identity, execution sandboxing, and reliability engineering for autonomous agents, covering the OWASP Agentic Top 10 | Production agents need governance — identity, policy, sandboxing, reliability — not ad-hoc safety; want a structured toolkit mapped to OWASP Agentic risks | NeMo-Guardrails, superagent, rogue, daytona |
