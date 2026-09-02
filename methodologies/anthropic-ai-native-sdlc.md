# Anthropic's AI-Native SDLC playbook — mapped to our dev loop

**What this is:** a stage-by-stage reading of
[The AI-Native SDLC playbook](https://claude.com/blog/the-ai-native-sdlc-playbook), published
2026-08-21 by Anthropic's own Applied AI team — translated into this repo's
[inner/outer dev loop](../WORKFLOW.md) and the catalogued tools/skills that fill each role. Unlike
8090's Software Factory (a paid product) or a third-party fork of AWS's AI-DLC, this is a first-party
methodology from the lab whose model this repo's own stack is built around, published as a doc rather
than sold as a platform — the closest thing to "how Anthropic itself says to restructure the SDLC."

**A disclosure this entry needs up front.** `claude.com` was `EGRESS_BLOCKED` in this pass's
sandbox, the same wall every prior Anthropic-hosted or first-party source on
[`LEARNING.md`](../LEARNING.md) has hit — so the playbook itself was never directly read. Everything
below is cross-checked across multiple independent third-party write-ups that converge on the same
stage names, the same six artifact filenames, and the same defining quotes (port.io, Waydev, an
X/Twitter thread paraphrasing the post, agenticaiarch.com, getaibook.com, menuagentic.com, and a
third-party GitHub implementation naming the same six stages) — not read from the source, the same
standard `LEARNING.md` applies throughout. One exact stage→artifact pairing is uncertain (see the
Build stage note below) precisely because it could not be checked against the primary text; it is
flagged rather than guessed past.

## The pipeline

Anthropic's stated thesis, paraphrased consistently across every summary found: coding agents now
finish code in hours, but planning, review, and deployment still run at human speed — the bottleneck
moved from generation to everything around it. The playbook's fix is a **closed loop of git-committed
artifacts**, not a linear stage-gate chain: each of six stages ends by committing one version-controlled
Markdown or diff artifact, and the next stage begins by reading it, so the artifact chain **is** the
audit trail rather than a separate log describing it.

```
   Plan    → intent.md            (the ask, the reason, the constraints — committed before design or build)
      ↓
   Design  → spec.md              (Claude reads intent.md; Skills encode brand/security/UX as hard constraints)
      ↓
   Build   → plan.md, then a diff + its tests
      ↓
   Test    → a PR carrying its own review findings
      ↓
   Deploy  → production
      ↓
   Maintain → an incident record                                       ─┐
      ↑                                                                  │  the artifact chain = the audit trail
      └──────────────────── feeds back into the next Plan ──────────────┘
```

Governance is built in as code — hooks, skills, and evals enforce constraints automatically — with
human judgment reserved for what code can't decide: a low-blast-radius change with passing tests can
move toward automatic acceptance, while regulated, high-risk, and core-architectural changes keep a
human's approval. That is a materially different claim from "a human reviews every PR" — it is a
policy for *deciding which changes still need one*, the same shape as this repo's own eliminate-only
rule deciding which verdicts an unattended pass may write.

## Mapping: Anthropic stage → our dev loop → our stack

| Playbook stage | Artifact | Our loop stage | Catalogued tool / skill |
|---|---|---|---|
| Plan | `intent.md` (ask, reason, constraints) | Outer **Discover/Architect** → inner **Plan** | `brainstorming` ([superpowers eval](../evaluations/agent-harnesses.md)); a GitHub issue plays the same role today |
| Design | `spec.md` (Skills encode brand/security/UX as constraints) | inner **Plan** (outer **Architect**) | `writing-plans`; `feature-dev` code-architect ([eval](../evaluations/feature-dev.md)) — our skills already play the "hard constraint" role the playbook assigns to Skills |
| Build | `plan.md`, then a diff + tests | inner **Implement** | `implement-issue`; `tdd` |
| Test | a PR carrying its own review findings | inner **Verify → Review** | `code-review` (dual-axis: standards + spec) |
| Deploy | production | inner **Ship** | CI pipeline / `make check`-style gates |
| Maintain | an incident record | inner **Reflect** / outer **Retrospect** | `triage` (feedback/incidents → agent-ready issues) — the closest thing we have; see "Where we diverge" |
| *(cross-cutting)* governance-as-code + risk-tiered approval | the artifact chain itself | spans **Verify/Ship** | this repo's `make check` / `audit-evals.py` gates — deterministic, CI-enforced, no risk tiering |

## Stage notes

- **Plan → `intent.md`.** Described consistently as a short, version-controlled file recording the
  ask, its reason, and its constraints, committed *before* anyone designs or builds — the same
  discipline `brainstorming` already asks for (surface intent and assumptions first), just without a
  standardized filename. One write-up (agenticaiarch.com) frames `intent.md` as a "regulated record"
  from day one, i.e. a compliance artifact as much as a planning one — a framing this repo's own
  GitHub-issue-as-intent-record habit doesn't currently carry.
- **Design → `spec.md`.** The distinctive claim here is mechanical, not procedural: "Claude reads
  `intent.md` and generates `spec.md`, while reusable Claude Skills encode brand, security, and UX
  constraints as hard generation requirements" (paraphrased consistently across sources). That is our
  own skills model applied to spec generation itself, not just to code — worth noting since it is the
  playbook's most concrete point of overlap with what this repo already does.
- **Build → `plan.md`, then a diff.** This is the one pairing this entry can't fully verify: multiple
  summaries state "Build produces a `plan.md` before any code is edited," which reads oddly next to a
  stage named *Build* producing a *plan* — plausibly a technical/implementation plan distinct from
  Design's product spec, but the primary post was not read directly, so the exact boundary between
  Design's and Build's planning artifacts is stated here as reported, not as confirmed.
- **Test → a PR with its own review findings.** The PR carries the review, not a separate document —
  consistent with this repo's own `code-review` skill attaching findings to the diff under review
  rather than a standalone report.
- **Maintain → an incident record.** The playbook's own answer for this stage is reported as thin by
  at least one independent write-up (Draftt.io, proposing how to make Maintain "autonomous"), which
  reads as the same shape as this repo's own AI-DLC reading: Operations/Maintain is the stage every
  AI-native SDLC currently under-specifies relative to Plan/Build/Test.

## Practitioner critique found alongside the playbook

Unusual for how fast it arrived — multiple independent critical engagements inside two weeks of
publication, which is itself a signal the playbook is being taken seriously enough to argue with
rather than just summarized:

- **A measurement gap.** Waydev's response argues the playbook names no metrics for whether the loop
  is actually working, and proposes concrete ones in the same spirit as this repo's own Verifiability
  signal — time to first review (which should fall to minutes if the loop works), the share of review
  comments resolved without a human touching the branch, and defects/vulnerabilities caught before
  merge versus escaping to production. Worth reading against our own [Verifiability
  rationale](../WORKFLOW.md#why-verifiability-is-its-own-signal): a governance-as-code claim with no
  stated way to check it is exactly the gap that signal exists to name.
- **Stops at the database.** Atlas's response (a schema-migration tool vendor, so read the specificity
  as informed rather than neutral) argues the artifact chain has no answer for schema/data-layer
  changes — a gap this repo's own stack doesn't obviously fill either.
- **Three links have no check.** menuagentic.com's response argues specific handoffs in the artifact
  chain (which links, unconfirmed without the primary source) move review upstream without adding a
  verification step to match — the same failure shape this repo's own detector suite exists to catch
  in its own domain (a check stated but not gated is a check that can silently rot).

None of this is confirmed against Anthropic's own text, and is presented here as **what practitioners
said about the playbook**, not as this repo's own independent finding.

## Where our open-tool stack diverges

- **No standardized artifact filenames.** The playbook's contribution is arguably the naming
  convention itself — `intent.md`/`spec.md`/`plan.md` as a fixed chain every stage reads and writes —
  more than any single stage's content, most of which already has a skill-shaped analog here. Our
  equivalent artifacts (issues, plans, PRs) exist but aren't named or chained this uniformly.
- **No risk-tiered automatic acceptance.** Our gates (`make check`) are binary — pass or fail, human
  or bulk-lane eliminate-only — not a blast-radius policy that lets some changes skip human approval
  entirely. Adopting that distinction deliberately is a bigger governance decision than this doc
  should make on its own.
- **No incident-record artifact for Maintain.** `triage` converts feedback into issues; it does not
  produce anything shaped like the playbook's structured incident record feeding back into the next
  Plan. This is the same Operations/Maintain gap [`aws-ai-dlc.md`](aws-ai-dlc.md) and
  [`bushido-ai-dlc-2026.md`](bushido-ai-dlc-2026.md) already document from AI-DLC's side — a third
  independent AI-native methodology landing on the same thin stage is worth taking as a signal, not a
  coincidence.
- **No vendor throughput numbers to weigh.** Unlike 8090's "80x" or AI-DLC's cited case studies, the
  summaries found here cite no headline performance multiple — the playbook is presented as a
  structural recommendation, not a benchmarked product, which is also why there is nothing here to
  file next to this repo's usual skepticism of vendor claims.

A third-party open-source implementation of this playbook exists
([`bashebr/ai-native-sdlc`](https://github.com/bashebr/ai-native-sdlc), a Codex + Claude Code skill/
plugin scaffolding the same six stages with approval gates at every handoff) — named here for the
discovery lane; this research lane does not add catalog rows.
