# Evaluation: 8090 Software Factory

**Site:** [8090.ai](https://www.8090.ai/) · [docs](https://www.8090.ai/docs/general/introduction) · [EY.ai PDLC](https://www.ey.com/en_us/services/consulting/ai-native-pdlc-reinventing-software-delivery)
**Stars:** n/a (commercial product, no public repo) | **Last updated:** n/a | **License:** Proprietary / commercial (enterprise SaaS)
**Last verified:** 2026-06-29
**Dev loop stage:** Plan (requirements → specs → work orders is the differentiator; the platform then spans Implement → Ship → Reflect)
**Layer:** Infrastructure (AI-native SDLC control plane / platform)

---

## What it does

8090's **Software Factory** is a commercial **"AI-native SDLC control plane"** — a platform that drives software from *business intent* to *production code* through a mesh of specialized AI agents under continuous human oversight, with a full audit trail. It is co-launched with EY as the **EY.ai PDLC** (Product Development Lifecycle) and aimed at regulated enterprises (healthcare, financial services, manufacturing, government) where compliance visibility and traceability matter.

Its thesis is that "single-player" AI coding tools are fast but sloppy because they skip the front of the lifecycle (requirements refinement, architecture capture, work planning) and leave no auditable trail. Software Factory orchestrates the *whole* loop instead, feeding agents structured context rather than vague prompts. The documented pipeline is a chain of modules, each producing a durable artifact:

- **Requirements** → a Product Requirements Document (PRD) — "Define your product."
- **Blueprints** (powered by a *Feature Extraction Agent*) → structured **Feature Nodes** that expand the PRD into implementation specs — "Translate vision into specs."
- **Work Orders** / **Planner** → actionable, codebase-tied development tasks that name files to create/update — "Turn specs into tasks."
- **Development** → code, tests, documentation, and infrastructure.
- **Validator** → converts user feedback into new development tasks — "Close the loop."

Two cross-cutting elements bind these together: a **Knowledge Graph** that links requirements, architecture, and implementation as a single source of truth and automatically propagates changes across artifacts; and a **control plane** that keeps "full control, visibility, and auditability over every decision from start to finish," with human oversight focused on intent, scope, and governance. Collaboration is "multiplayer" — PM, design, engineering, and business stakeholders co-create against shared context.

## How we tested it

**Evidence:** REVIEW

**Source-grounded review — not run hands-on.** Software Factory is a closed commercial platform with no public repo, free tier, or self-serve trial available to us; we did not install, log into, or run it. Findings come from 8090's own product site and documentation (the Introduction and module pages) and EY's PDLC materials — the vendor's framing, not observed behavior. Any quantitative results below are quoted as the **vendor's** claims, not measured by us.

```
# Sources reviewed (vendor/partner documentation, read not run):
https://www.8090.ai/                                  # product positioning, three-phase model
https://www.8090.ai/docs/general/introduction         # modules + artifacts pipeline
https://www.8090.ai/docs/modules/planner              # Planner / Work Orders
https://www.ey.com/.../ai-native-pdlc-...             # EY.ai PDLC lifecycle framing
# PR (EY + 8090 launch) cites a vendor case study: ~70% productivity gain,
# "80x" faster delivery, 95%+ automated test coverage — 8090/EY figures, unverified by us.
```

## What worked

- **Front-loaded lifecycle is the right critique.** The core insight — that prompt-only coding tools fail because they skip requirements/architecture/planning and leave no trail — matches what this repo's WORKFLOW.md argues about the Plan stage. The artifact chain (PRD → Feature Nodes → Work Orders) is a coherent intent→code path.
- **Knowledge Graph as single source of truth.** Linking requirements↔architecture↔implementation with automatic change propagation is the strongest idea here: it attacks specification drift directly, which most agent tools ignore.
- **Auditability as a first-class concern.** A control plane that records "every decision start to finish" is genuinely differentiated and is the feature that makes it credible for regulated delivery — most agent orchestration tools have no audit story.
- **Human oversight by design.** Keeping humans on intent/scope/governance while agents execute is a defensible division of labor rather than full autonomy.

## What didn't work or surprised us

- **Proprietary, closed, enterprise-only.** No public repo, no free tier, no self-serve access — it is unevaluable hands-on and unadoptable in an open-tool stack. This is the disqualifying caveat for this catalog.
- **Vendor metrics are unverified.** The headline "80x faster / 70% productivity / 95%+ test coverage" figures come from an 8090/EY case study, not independent measurement; treat as marketing until reproduced.
- **Methodology > product, for our purposes.** The valuable, transferable part is the *pipeline shape* (intent → PRD → specs → work orders → dev → validator, over a knowledge graph), not the SaaS itself. That shape can be reconstructed from open skills we already have (see #173/#174).
- **Enterprise framing.** Positioned for regulated orgs with EY as integration partner — heavy for an individual or small team, and pricing/access are gated behind sales.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Structured context (PRDs, Feature Nodes, work orders) and a propagating knowledge graph reduce specification drift vs. vague prompting — per vendor design, not measured by us. |
| Speed | + (claimed) | Vendor cites large delivery speedups ("80x"); unverified by us. |
| Maintainability | + | Durable, linked artifacts and audit trail favor long-term maintainability over one-shot generation. |
| Safety | + | Full auditability, human oversight on intent, and governance guardrails are built for regulated/compliance settings. |
| Cost Efficiency | − / unknown | Commercial enterprise SaaS gated behind sales; no public pricing — not cost-efficient for an open-tool stack. |

## Verdict

**SKIP** (commercial / no access) — Disqualified by this catalog's permissive-OSS adoption bar: Software Factory is a closed, proprietary enterprise platform with no public repo or free tier, so it cannot be installed, evaluated hands-on, or adopted in our open-tool workflow. _The methodology is the takeaway, not the product:_ its AI-native SDLC — intent → PRD → Feature Nodes → Work Orders → Development → Validator, bound by a knowledge graph and an auditable control plane — is exactly the shape worth studying, and it can be reconstructed from open skills we already have. Catalogued as a reference example of an AI-native SDLC; the stage-by-stage mapping and a self-hosted pipeline recipe are tracked in [#173](https://github.com/mattbutlerengineering/ai-tooling/issues/173) and [#174](https://github.com/mattbutlerengineering/ai-tooling/issues/174).

Compared to neighbors: **AgentsMesh** is a self-hosted control plane for running *many agents in parallel* (execution scale), and **dify** is a visual agentic-workflow platform — both are about orchestrating execution. 8090 Software Factory is the distinct **full-SDLC / intent-to-production** end of the spectrum: its differentiator is the front of the loop (requirements/specs/planning) and an end-to-end audit trail, not parallel-agent throughput.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [8090 Software Factory](https://www.8090.ai/) | platform | AI-native SDLC control plane (commercial; EY.ai PDLC) — drives business intent → production code via an agent mesh over a knowledge graph, with full audit trail | Single-player AI coding tools skip requirements/specs/planning and leave no auditable trail for regulated delivery | AgentsMesh, dify, vibe-kanban, EY.ai PDLC (ext.) |
