# Evaluation: tabby

**Repo:** [TabbyML/tabby](https://github.com/TabbyML/tabby)
**Stars:** ~33,600 | **Last updated:** 2026-03-02 | **License:** open-source / on-prem (repo SPDX returns NOASSERTION)
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A self-hosted AI coding assistant — an open-source, on-premises alternative to GitHub Copilot. Tabby runs your own completion and chat models on your own hardware so your code never leaves your infrastructure.

Key properties per the README: **self-contained** (no external DBMS or cloud service required), an **OpenAPI interface** for easy integration with existing infrastructure (e.g. Cloud IDEs), and support for **consumer-grade GPUs**. Beyond inline code completion it has an "answer engine" (chat side panel) and a context/retrieval layer that can index your repositories, your own documentation (via REST APIs), and even GitLab Merge Requests as context. Recent releases connect to the team's agent project (Pochi) for issue→PR workflows, but the core Tabby server is the self-hosted completion + answer engine.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README and release notes. Confirmed the self-hosted/on-prem Copilot-alternative positioning, the self-contained (no-DBMS/cloud) deployment, the OpenAPI integration surface, consumer-GPU support, and the repo/doc/GitLab-MR context indexing. Last push ~2026-03 (steadier cadence than some peers). License resolves to NOASSERTION via the API — it is open-source/self-hostable, but pin the exact license terms before commercial redistribution. Not deployed against a live model/IDE, so condition-gated.

```bash
gh api repos/TabbyML/tabby --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/TabbyML/tabby/readme --jq '.content' | base64 -d
```

## What worked

- **Code never leaves your infra.** Fully self-hosted completion + chat is the decisive feature for privacy/compliance-bound teams that can't use cloud Copilot.
- **Low-barrier self-hosting.** Self-contained (no DBMS/cloud) and consumer-GPU-capable makes on-prem realistic without a big infra investment.
- **Context-aware.** Indexing repos, internal docs (via REST), and GitLab MRs grounds completions/answers in your actual codebase, not just the open model's priors.

## What didn't work or surprised us

- **License ambiguity.** API returns NOASSERTION; confirm the exact terms for commercial/redistribution use.
- **Model quality ceiling.** Self-hosted open models on consumer GPUs won't match frontier cloud models — a quality/privacy tradeoff.
- **Different tool class than agentic CLIs.** Tabby is a completion/answer server (Copilot-style), not an autonomous coding agent like Claude Code/OpenHands; the agent story (Pochi) is adjacent.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Repo/doc-grounded completions reduce off-base suggestions |
| Speed | + | Local inline completion with no cloud round-trip |
| Maintainability | neutral | A dev aid; doesn't change codebase structure |
| Safety | + | On-prem: source code never sent to a third-party service |
| Cost Efficiency | + | No per-seat Copilot fees; runs on your own (consumer) GPUs |

## Verdict

**discovery-log — tentative read**

Adopt when privacy/compliance rules out cloud Copilot and you want self-hosted completion + chat grounded in your code, on hardware you control. Accept the model-quality tradeoff versus frontier cloud assistants, and pin the license terms for commercial use. It complements — rather than replaces — agentic coding CLIs.

## Triage note

Left at `discovery-log`. ★33.8K, pushed 2026-06-30.

Checked its category placement, and it is not actually in the cluster: Tabby is **self-hosted
completion + chat**, not an agentic coding CLI. Its own eval says it "complements — rather than
replaces — agentic coding CLIs", so no member of this slice can subsume it and it cannot subsume them.

The open item is the license. GitHub records `NOASSERTION` — its parser could not read the LICENSE
file — and the eval already flags "pin the license terms for commercial use". Following the rule this
repo applies elsewhere, `NOASSERTION` disposes nothing on its own: in this same triage lane it has now
concealed a permissive Apache-2.0 (`terraform-skill`) and a blocking CC BY-NC (`academic-research-skills`).
Reading the actual LICENSE text is the resolution, and it is a task rather than a verdict.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [tabby](https://github.com/TabbyML/tabby) | platform | Self-hosted AI coding assistant (open-source, on-prem; ★34K) — OpenAI-compatible Copilot alternative with code completion + answer engine, self-contained (no DBMS/cloud), consumer-GPU-capable, indexes repos/docs/GitLab MRs as context | Want completion + chat grounded in your own code without a cloud Copilot; need on-prem, GPU-friendly self-hosting | forgecode, opencode, oh-my-openagent |
