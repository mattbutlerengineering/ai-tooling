# AWS AI-DLC — an AI-native SDLC, mapped to our dev loop

**What this is:** a stage-by-stage reading of AWS's **AI-Driven Development Lifecycle (AI-DLC)** —
an openly-published methodology (announced on the [AWS DevOps & Developer Productivity
blog](https://aws.amazon.com/blogs/devops/ai-driven-development-life-cycle/), expanded in
[building with AI-DLC using Amazon Q Developer](https://aws.amazon.com/blogs/devops/building-with-ai-dlc-using-amazon-q-developer/)
and an [AWS for Industries deep dive for financial services](https://aws.amazon.com/blogs/industries/ai-driven-development-lifecycle-for-financial-services/))
— translated into this repo's [inner/outer dev loop](../WORKFLOW.md) and the catalogued
tools/skills that fill each role.

**Update (2026-08-10):** AWS [announced](https://aws.amazon.com/blogs/devops/amazon-q-developer-end-of-support-announcement/)
on 2026-04-30 that Amazon Q Developer — the product the "expanded" post linked above
demonstrates AI-DLC against — is being sunset in favor of **Kiro**, AWS's newer agentic IDE:
new Q Developer signups blocked from 2026-05-15, the latest coding models Kiro-exclusive from
2026-05-29, full end of support 2027-04-30. AI-DLC the *methodology* is vehicle-agnostic —
Bolts, Units of Work, and Mob Elaboration/Construction are process concepts, not features of
any one product — so the mapping below is unaffected. But the worked example the methodology
was originally demonstrated against is now a product AWS itself is retiring, which is worth
knowing before pointing anyone at that specific post. Kiro has no `CATALOG.md` row of its own
yet (only mentioned in passing, as one of several config formats `agnix` lints) — worth a
discovery-lane look given it is now AWS's flagship agentic IDE.

**Update (2026-08-24):** `awslabs/aidlc-workflows`'s `main` branch now announces general
availability of **"AI-DLC Workflows 2.0"** (confirmed by fetching `main`'s `README.md` directly,
not from search summaries; the git tag is still `v1.0.1` — that is two independent version
numbers, package tag vs. methodology name, not a stale-release bug). The shipped GA version adds
internal structure this doc's pipeline diagram below doesn't yet reflect, but the **Operations gap
this doc already calls out is unchanged in what's actually shipped**: `main`'s own README still
reads, verbatim, *"🟡 OPERATIONS PHASE — Deployment and monitoring (future)"*. What's new is
upstream and not yet released: a `v2` branch (self-versioned `2.6.70`, not merged to `main` or
tagged) restructures the pipeline into 5 phases / 33 stages / a 14-agent roster, and — the material
part — its Operation phase is no longer a placeholder. It has 7 concrete stages, each with an
assigned lead agent: CD pipeline config and rollback runbooks, environment provisioning,
deployment plus smoke tests, observability dashboards/alarms/SLOs, incident runbooks, load testing
against NFRs, and a closing SLO report/cost analysis/feedback-loop doc — all 7 conditional and
skippable for `mvp`/`poc` scope. That would be the first concrete Operations answer from **AWS's
own** reference implementation; until now only the third-party
[`bushido-ai-dlc-2026.md`](bushido-ai-dlc-2026.md) fork filled this gap. It just hasn't shipped:
worth re-checking (and re-mapping the table below) once `v2` merges to `main` and gets a tag.
Sources: [`main` README](https://github.com/awslabs/aidlc-workflows/blob/main/README.md),
[`v2` branch](https://github.com/awslabs/aidlc-workflows/tree/v2),
[`v2`'s phases-and-stages doc](https://github.com/awslabs/aidlc-workflows/blob/v2/docs/guide/04-phases-and-stages.md).

**Update (2026-09-02):** the "worth re-checking once `v2` merges to `main` and gets a tag" note above
is now resolved — confirmed by cloning `main` read-only (`github.com` and `raw.githubusercontent.com`
reachable this pass) rather than from search summaries. `main`'s HEAD (`a277af2`, 2026-09-02) now
reads *"AI-DLC Workflows 2.0 is GA on `main`"*; the newest git tag is `v2.7.0` (2026-09-01, one day
before this pass), with a full `v2.1.0`–`v2.7.0` tag history behind it, so this is a completed merge
and release train, not a preview flag. Three things changed from the 3-phase pipeline this doc maps
below. **The phase count went 3 → 5**: Initialization (0.1–0.3, workspace scaffold) and Ideation
(1.1–1.7, intent capture through team formation and approval) now precede Inception, for 33 stages
total run by a 14-agent roster (11 domain experts, 2 quality-gate reviewers, 1 adaptive-workflows
composer) — Inception, Construction, and Operation keep their names and roughly their old scope.
**The Operations gap this doc has called a placeholder since it was first written is closed in the
reference implementation**: Operation (4.1–4.7) now ships seven named, agent-owned conditional
stages — Deployment Pipeline, Environment Provisioning, Deployment Execution, Observability Setup,
Incident Response, Performance Validation, and a terminal Feedback & Optimization stage that either
closes the workflow or loops back to Ideation 1.1 — matching almost exactly what the 2026-08-24
update above described as still unmerged upstream work. All seven stay skippable for `mvp`/`poc`
scope, so "Operations is optional" survives; "Operations is unspecified" does not. **"Mob
Elaboration"/"Mob Construction" as a synchronous, whole-team ceremony no longer appears in the
shipped docs at all** — the closest surviving concept, `mode: mob` ("mob execution"), is now an
asynchronous AI-agent mesh: a lead agent drafts, mutually-blind AI collaborators (design/developer/
quality) each write a contribution file in parallel, the lead integrates, and only unresolved
judgment calls surface to a human mid-stage. User Stories (2.4) is the one shipped example. That is
a materially different mechanism than *"product, engineering, and QA reacting live to AI-generated
questions in the same session"* — the "Single-player, not Mob" divergence bullet below was written
against the original AWS blog posts' description and is now stale as a description of *this*
reference implementation specifically; whether AWS's own methodology definition changed the same way
is unconfirmed — the linked blog posts were not re-fetched this pass, only the OSS implementation's
own docs, which now cite an "AI-DLC Workflows 2.0 Specification" whitepaper as their source rather
than the original blog posts. Re-mapping the full stage table below to the 5-phase/33-stage shape is
a larger job than this pass's conservative-diff mandate covers — flagged here rather than attempted
piecemeal. Sources: [`main` README](https://github.com/awslabs/aidlc-workflows/blob/main/README.md),
[`main`'s phases-and-stages guide](https://github.com/awslabs/aidlc-workflows/blob/main/docs/guide/04-phases-and-stages.md),
[`main`'s glossary](https://github.com/awslabs/aidlc-workflows/blob/main/docs/guide/glossary.md).

Unlike 8090's Software Factory, AI-DLC is not a paid product:
AWS ships it as methodology plus an open rule-file reference implementation,
[`awslabs/aidlc-workflows`](https://github.com/awslabs/aidlc-workflows) (catalogued, evaluated —
see the [evaluation](../evaluations/aidlc-workflows.md), verdict **SKIP**, redundant with
`superpowers`/GSD at the task level). This doc maps the *methodology*; the linked evaluation
covers the *reference implementation* as an installable tool — same split as 8090's product
eval vs. this doc.

## The AI-DLC pipeline

AI-DLC's thesis: put AI at the center of the whole lifecycle, not just code generation, while
keeping humans as the approval gate at every phase transition — *"AI systematically creates
detailed work plans, actively seeks clarification and guidance, and defers critical decisions to
humans."* Work runs in **Bolts** (AI-DLC's replacement for the sprint — a cycle measured in hours
or days, not weeks) across three phases:

```
Business intent
   → Inception   (Mob Elaboration: requirements, personas, user stories,
                   acceptance criteria, Units of Work, first app design)
   → Construction (Mob Construction: architecture, domain models, code, tests
                    — validated against Inception's acceptance criteria)
   → Operations  (deploy, monitor, infra config — placeholder in the OSS
                   reference implementation as of this writing)
```

**Units of Work** are AI-DLC's decomposition granule — the AI proposes a breakdown (e.g.
*customer identity*, *claim submission*, *notification service*), each carrying dependencies,
acceptance criteria, and parallelization boundaries, for the team to validate.

**Mob Elaboration** and **Mob Construction** are AI-DLC's signature ritual: a *synchronous*,
whole-team session (product, engineering, QA together) where the AI drafts — questions, proposed
requirements, proposed architecture — and the team validates live, rather than the AI's output
going through async review later. AWS positions this as the difference between an individual
"vibe coding" against an agent and a team-scale, auditable process.

## Mapping: AI-DLC phase → our dev loop → our stack

| AI-DLC phase | Artifact | Our loop stage | Catalogued tool / skill |
|---|---|---|---|
| Inception (Mob Elaboration) | Requirements, personas, user stories, acceptance criteria, Units of Work, first app design | Outer **Discover/Architect** → inner **Plan** | `to-prd` ([eval](../evaluations/skills-collections.md)); `brainstorming` + `writing-plans` ([superpowers eval](../evaluations/agent-harnesses.md)); `to-issues` + `beads` for Units-of-Work decomposition ([eval](../evaluations/beads.md)) |
| Construction (Mob Construction) | Architecture, domain models, code, tests validated against Inception's acceptance criteria | inner **Implement → Verify** | `implement-issue` (TDD, quality gates); `feature-dev` code-architect ([eval](../evaluations/feature-dev.md)); `tdd` + `code-review`'s Spec axis |
| Operations | Deploy, monitor, infra config | inner **Ship**; outer nothing formalized | CI pipeline / `make check`-style gates (this repo's own integrity suite is the closest analog, not AI-DLC-specific) |
| *(cross-cutting)* Bolt cadence | short, hours-to-days work cycles | spans the whole inner loop | no direct tool — a process cadence, not a stage |
| *(cross-cutting)* Mob Elaboration / Mob Construction | synchronous, whole-team live validation | none — see "Where we diverge" | none; our stack has no synchronous multiplayer session equivalent |

## Stage notes

- **Inception → to-prd + brainstorming/writing-plans + to-issues/beads.** AI-DLC folds
  requirements gathering *and* work decomposition into one phase (Units of Work emerge alongside
  requirements, not as a separate downstream planning stage the way 8090 splits Requirements from
  Work Orders). Our stack still does this as two skill calls — `to-prd` for the PRD,
  `brainstorming`/`writing-plans` for the spec, `to-issues`/`beads` for the task graph — so the
  mapping is many-to-one on our side.
- **Construction → implement-issue + feature-dev + tdd/code-review.** AI-DLC's requirement that
  Construction validate against Inception's acceptance criteria is exactly what `code-review`'s
  **Spec** axis checks (the change against the originating issue, not just code conventions) —
  the same alignment the 8090 mapping draws for its Tests module.
- **Operations → mostly unfilled on both sides.** AI-DLC's own reference implementation
  (`aidlc-workflows`) leaves Operations a placeholder — "just a directory structure and a TODO
  note" per our evaluation. We don't have a stronger answer either: CI and this repo's own
  `make check` gates are the nearest infra-layer analog, but neither AI-DLC nor our stack has a
  filled-in AI-authored-deploy-and-monitor story yet. Worth revisiting when AWS ships it.
- **Distinctive ideas with no stack slot yet.** Two things `aidlc-workflows` implements that
  our skills don't formalize as explicit gates: **overconfidence prevention** (default to asking
  more questions rather than silently skipping a category when unsure — a documented fix for a
  real LLM failure mode) and **depth-level adaptation** (the agent scales artifact detail to
  problem complexity: a one-line bug fix gets concise requirements, a system migration gets
  multi-round questioning). Both are process ideas worth stealing into `brainstorming`/`to-prd`
  even though we didn't adopt the framework that ships them.

## Where our open-tool stack diverges from AI-DLC

- **Single-player, not Mob.** AI-DLC's core mechanism is synchronous multi-role validation —
  product, engineering, and QA reacting live to AI-generated questions in the same session. Our
  pipeline is one operator driving skills in sequence, coordinated through the issue tracker —
  the same gap the 8090 mapping calls out as 8090's "multiplayer" claim. Two independently
  designed AI-native methodologies converging on live multi-role validation as differentiator is
  a signal worth taking seriously, even though neither maps onto a single-operator stack.
- **No formalized Operations phase — on our side only, as of 2026-09-02.** This bullet stood on the
  claim that *neither* AI-DLC's reference implementation *nor* our stack has a real answer for
  AI-authored deploy/monitor/remediate; that first half is no longer true. **Update (2026-08-07):**
  a third-party fork of this same methodology,
  [TheBushidoCollective/ai-dlc](https://github.com/TheBushidoCollective/ai-dlc) (community-authored,
  not AWS's), filled the gap with declarative Scheduled/Reactive/Process operation specs — see
  [`bushido-ai-dlc-2026.md`](bushido-ai-dlc-2026.md). **Update (2026-09-02):** AWS's own reference
  implementation now ships a concrete answer too — see the dated update note earlier in this file:
  `awslabs/aidlc-workflows` `main` (GA, v2.7.0) runs a seven-stage Operation phase with a named owning
  agent per stage (deploy, provision, execute, observe, respond to incidents, validate performance,
  close the loop with a feedback/cost report). Our own stack still has no equivalent — the gap named
  in this bullet is now specifically ours, not a shared one.
- **The task-level half is already what we do, per our own evaluation.** Our
  [evaluation](../evaluations/aidlc-workflows.md) of the reference implementation found
  Construction-phase behavior "redundant at the task level" with `superpowers`'s inner loop —
  TDD, debugging, and review workflows AI-DLC's OSS rules don't provide. The part of AI-DLC that
  isn't redundant with what we already run is the enterprise-governance half: an auditable,
  cross-editor (Kiro/Amazon Q/Cursor/Cline/Copilot/Claude Code) requirements ceremony for mixed
  teams — a want this single-tool-stack repo doesn't have a customer for today.
- **No vendor throughput claims taken at face value.** AWS cites a 40-person-year rebuild done by
  six engineers in 76 days (Amazon Bedrock inference engine, via Kiro) as a headline result. That
  is a vendor-reported outcome for one project, not a controlled measurement — treated the same
  way this repo treats 8090's "80x faster" claim: informative, not adopted as our own number.
