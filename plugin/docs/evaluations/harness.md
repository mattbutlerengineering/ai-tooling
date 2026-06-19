# Evaluation: harness

**Repo:** [revfactory/harness](https://github.com/revfactory/harness)
**Stars:** 7,095 | **Last updated:** 2026-06-10 (pushed; created 2026-03-26) | **License:** Apache-2.0
**Dev loop stage:** Outer-loop **Architect / Decompose** — it is a *setup-time* generator, not a per-task tool. You run it once to manufacture a domain-tailored `.claude/agents/` + `.claude/skills/` team, which then operates across the inner loop (Plan → Implement → Verify) on subsequent sessions. It builds the harness; the harness does the work.
**Layer:** Process generator that emits Process artifacts (markdown agent/skill definitions). No runtime of its own — it leans on Claude Code's Agent Teams API (`TeamCreate`/`SendMessage`/`TaskCreate`) at generation and execution time.

---

## What it does

The catalog one-liner: "Meta-skill that designs domain-specific agent teams and generates specialized skills." Harness brands itself an **"L3 Meta-Factory / Team-Architecture Factory"** — say "build a harness for this project" (or the Korean/Japanese equivalents) and a single skill (`skills/harness/SKILL.md`) walks a **6-phase workflow**: Phase 0 audit of any existing harness → Phase 1 domain analysis → Phase 2 team-architecture design → Phase 3 agent-definition generation → Phase 4 skill generation → Phase 5 integration/orchestration → Phase 6 validation/testing. The output is files written into *your* `.claude/agents/` and `.claude/skills/`, plus a pointer registered in `CLAUDE.md` so the orchestrator re-triggers in future sessions.

The design substance lives in `references/agent-design-patterns.md`: it picks among **6 named team-architecture patterns** — Pipeline, Fan-out/Fan-in, Expert Pool, Producer-Reviewer, Supervisor, Hierarchical Delegation — and chooses an execution mode (Agent Teams as default, sub-agents as the lower-overhead alternative, or a per-phase hybrid). It is, in effect, a guided prompt-program: the skill body is the algorithm, the reference files are the design library, and Claude is the interpreter. The repo is unusually well-documented for a single-skill project — tri-lingual READMEs (EN/KO/JA), a strict 5-minute `quickstart.md`, a CHANGELOG, ISSUE_TEMPLATEs, a `_workspace/` of release-audit artifacts, and an honest `docs/experimental-dependency.md` that owns its hard dependency on an experimental flag.

## How we tested it

**Source-grounded inspection — not installed, not run.** No marketplace was added, no plugin installed, no "build a harness" prompt issued, and no generated team was executed. Every claim comes from the repository (GitHub metadata, the three READMEs, the recursive file tree, `SKILL.md`, `references/agent-design-patterns.md`, `docs/quickstart.md`, `docs/experimental-dependency.md`, commit/contributor counts) — not from observed generation or agent behavior. The 6-pattern / 6-phase framing and the "factory" language are the author's, not measurements I made.

```bash
gh api repos/revfactory/harness --jq '{desc,stars:.stargazers_count,forks:.forks_count,pushed:.pushed_at,created:.created_at,license:.license.spdx_id}'
gh api repos/revfactory/harness/readme --jq '.content' | base64 -d            # tri-lingual, L3 framing
gh api "repos/revfactory/harness/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api repos/revfactory/harness/contents/skills/harness/SKILL.md --jq '.content' | base64 -d   # 6-phase workflow (Korean)
gh api repos/revfactory/harness/contents/skills/harness/references/agent-design-patterns.md --jq '.content' | base64 -d  # 6 patterns
gh api repos/revfactory/harness/contents/docs/experimental-dependency.md --jq '.content' | base64 -d  # flag dependency
gh api repos/revfactory/harness/commits --jq 'length'        # 30 (page-1 cap)
gh api repos/revfactory/harness/releases --jq 'length'       # 0 tagged releases (README badge says v1.2.0)
gh api repos/revfactory/harness/contributors --jq '[.[].login]'  # 6 contributors
```

## What worked

- **Real design content, not persona theater.** The 6 team patterns plus a sub-agent-vs-team decision tree and 4-axis agent-separation criteria (specialization, parallelism, context, reusability) are a legitimate, reusable framework for *how to shape a team* — the genuine gap that a 271-file roster like agency-agents leaves open.
- **Generates the skills, not just the agents.** It writes both "who" (agent definitions) and "how" (skills with progressive disclosure), and forbids inline-prompt agents — every agent must be a reusable `.claude/agents/{name}.md` file. That separation is the right instinct for cross-session durability.
- **Evolution is a first-class principle.** SKILL.md treats the harness as a living system: Phase 0 audits existing agents/skills, detects drift against `CLAUDE.md`, and re-runs only the phases a change requires (a documented Phase-selection matrix). This matches this catalog's outer-loop "Reflect" emphasis better than most generators.
- **Notably honest, disciplined docs.** `experimental-dependency.md` openly states the hard dependency on `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, names the three flag-gated primitives, and commits to monitoring it — a level of operational candor rare in this catalog. Tri-lingual READMEs and a strict quickstart lower adoption friction.

## What didn't work or surprised us

- **Hard dependency on an experimental flag.** Without `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, generated teams "silently fall back to single-agent execution, which silently breaks the Pipeline / Fan-out-in / Supervisor / Hierarchical Delegation patterns" (the repo's own words). Four of six headline patterns degrade silently — a fragile foundation for the marquee feature.
- **The skill body is Korean.** `SKILL.md` and `references/` are written primarily in Korean (the README is tri-lingual; the skill is not). The model can follow it, but for an English-speaking team it hurts auditability — you cannot easily review what the generator is instructed to do.
- **Generation cost and unverifiable output quality.** Running the full 6-phase team-generation flow is itself a multi-agent, multi-call operation, and nothing in the repo benchmarks the *quality* of the teams it produces. The 6-pattern menu is sound in theory; whether the generator picks the right one for a given domain is unmeasured.
- **Versioning theater.** The README badge advertises **v1.2.0**, but there are **0 tagged GitHub releases** — you install whatever `main` is, with no pinned bundle. CHANGELOG exists but isn't backed by tags.
- **Small bus factor for big ambition.** 6 contributors and 30 commits behind a self-described "meta-factory." The framing ("L3 Meta-Factory," coexistence tables with Archon/meta-harness/ECC) is more grandiose than a single-skill plugin warrants.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + / neutral | A well-chosen team pattern (producer-reviewer, supervisor) can sharpen task decomposition, but no benchmark substantiates that generated teams produce more-correct code than a hand-written setup. |
| Speed | + / − | Saves the hours of hand-authoring an agent/skill set; offset by a non-trivial generation run and by the risk of silent single-agent fallback when the flag is unset. |
| Maintainability | + | Phase-0 drift detection, the Phase-selection matrix, and file-based agent definitions are explicitly built to keep a harness coherent and re-runnable as the project evolves — its strongest signal. |
| Safety | neutral | Generates only markdown definitions; no code executes during generation. Residual risk is silent degradation under a missing experimental flag, and an unauditable (Korean) skill body. |
| Cost Efficiency | − / neutral | Multi-agent generation plus Agent Teams execution spends tokens up front; justified only if you reuse the generated harness across many sessions. |

## Verdict

**CONDITIONAL — adopt as a one-time scaffolder if you already run Agent Teams; skip if you don't.** Harness is the most *substantive* team-generator among its neighbors: it ships a real design framework (6 patterns + execution-mode decision tree + drift-aware evolution) rather than a roster, and its docs are unusually honest about their own fragility. But the marquee multi-agent patterns are gated behind an experimental flag that fails silently, the skill body is Korean (hard to audit), there are no tagged releases despite a "v1.2.0" badge, and the generated output quality is unbenchmarked. The right move: use it once to bootstrap a tailored agent/skill set, then read, prune, and own the generated files yourself.

Compared to neighbors: **agency-agents** hands you 271 uncoordinated personas to activate by hand; harness instead *designs and wires* a small team — strictly more useful if the design step works. **gstack** is a curated, opinionated *fixed* setup (~53 chosen skills); harness generates a *bespoke* one per domain — better fit, less battle-testing. **superpowers** ships a complete methodology you adopt as-is; harness produces a methodology *for your domain*. **ruflo** is a heavyweight all-in-one swarm harness with its own runtime; harness is a lean generator that defers execution to Claude Code's native Agent Teams. Pick harness when you want a tailored team scaffolded fast and are comfortable curating the output; pick superpowers/gstack when you want something proven off the shelf.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [harness](https://github.com/revfactory/harness) | skill | Meta-skill that generates a domain-tailored agent team + skills via 6 team-architecture patterns; depends on Claude Code's experimental Agent Teams flag | Need agents and skills tailored to a specific domain without hand-authoring each one — and a framework for *how* to shape the team | ruflo, superpowers, gstack; agency-agents (roster vs. designed team) |
