# AWS AI-DLC — an AI-native SDLC, mapped to our dev loop

**What this is:** a stage-by-stage reading of AWS's **AI-Driven Development Lifecycle (AI-DLC)** —
an openly-published methodology (announced on the [AWS DevOps & Developer Productivity
blog](https://aws.amazon.com/blogs/devops/ai-driven-development-life-cycle/), expanded in
[building with AI-DLC using Amazon Q Developer](https://aws.amazon.com/blogs/devops/building-with-ai-dlc-using-amazon-q-developer/)
and an [AWS for Industries deep dive for financial services](https://aws.amazon.com/blogs/industries/ai-driven-development-lifecycle-for-financial-services/))
— translated into this repo's [inner/outer dev loop](../WORKFLOW.md) and the catalogued
tools/skills that fill each role. Unlike 8090's Software Factory, AI-DLC is not a paid product:
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
- **No formalized Operations phase.** Neither AI-DLC's public reference implementation nor our
  stack has a real answer for AI-authored deploy/monitor/remediate yet — see the stage note
  above. **Update (2026-08-07):** a third-party fork of this same methodology,
  [TheBushidoCollective/ai-dlc](https://github.com/TheBushidoCollective/ai-dlc) (community-authored,
  not AWS's), fills this gap concretely — declarative Scheduled/Reactive/Process operation specs with
  explicit `agent`/`human` ownership. See [`bushido-ai-dlc-2026.md`](bushido-ai-dlc-2026.md) for the
  full reading; our own stack still has no equivalent, but the shape of a filled-in Operations phase is
  no longer purely hypothetical.
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
