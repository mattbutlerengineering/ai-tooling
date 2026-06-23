# Evaluation: Lifecycle frameworks cluster — agent-skills vs superpowers vs GSD vs feature-dev

**Cluster:** Dev Workflow / lifecycle frameworks (the default Plan→Implement→Verify→Ship loop)
**Contenders:** [agent-skills](https://github.com/addyosmani/agent-skills) (ADOPT, recommended primary) · [superpowers](https://github.com/obra/superpowers) (ADOPT) · [GSD](https://github.com/open-gsd/gsd-core) (KEEP, incumbent) · [feature-dev](https://github.com/anthropics/claude-plugins-official) (KEEP)
**Last verified:** 2026-06-22
**Dev loop stage:** Plan + Implement + Verify + Ship (these frameworks drive the whole loop)
**Layer:** Process (a phase-loop methodology) with a Tooling spine (slash commands / skills / installer)

---

## What it does

Every tool in this cluster imposes a disciplined development lifecycle on an AI coding agent — replacing "prompt and pray" with explicit, gated phases — but they differ in *scope* and *ceremony*:

- **agent-skills** (addyosmani) — 24 production-grade engineering skills behind a 7-command lifecycle (`/spec → /plan → /build → /test → /review → /code-simplify → /ship`), with skills that auto-activate by context, a `/build auto` autonomous mode, 4 specialist agents, and cross-editor support. Broad lifecycle coverage with deep skill content.
- **superpowers** (obra) — an agentic-skills framework and software-development methodology that gives raw Claude Code structured workflows for brainstorming, TDD, debugging, code review, and verification-before-completion. STACK installs it under the GSD row (`obra/superpowers`) for milestone/phase planning.
- **GSD** (Git. Ship. Done.) — a context-engineering Discuss→Plan→Execute→Verify→Ship phase loop with restricted-tool subagents and durable `STATE.md`/`CONTEXT.md` artifacts; the operator's *installed incumbent* (verified at v1.22.4 in `~/.claude/`). Heaviest ceremony, best for multi-session/greenfield work.
- **feature-dev** (Anthropic, official) — a 7-phase guided workflow scoped to a *single feature*: planning, implementation, verification. The lightest, most focused option, shipped first-party in the official marketplace.

Choosing within this cluster decides the STACK's **default loop**. STACK is explicit: "**pick one as primary** … run one as your default loop and pull the others in only when their scale fits, rather than layering all three."

## How we tested it

**Source-grounded comparison — not a fresh hands-on A/B.** We did not run all four frameworks through the same feature on the same repo, did not measure executor green-rates, token cost, or time-to-ship, and did not benchmark generated-code quality. This entry synthesizes the existing individual evaluations and catalog verdicts along a shared dimension (lifecycle breadth vs. ceremony vs. scope), then names the recommended primary.

**Evidence:** REVIEW

Sources read and cross-referenced:

```
evaluations/agent-skills-addyosmani.md      # ADOPT — "highest-quality full-lifecycle skill collection"
evaluations/mattpocock-vs-agent-skills.md   # "Use both" — lifecycle coverage vs. philosophy/vocabulary
evaluations/gsd.md                          # KEEP — "the user's own GSD, not a new tool to add"
evaluations/claude-plugins-official.md      # feature-dev's first-party source (KEEP/ADOPT-as-channel)
CATALOG.md (Dev Workflow / Skills rows)     # agent-skills, superpowers, GSD, feature-dev overlap markers
STACK.md (lifecycle "pick one as primary" note + rows)
```

No standalone `evaluations/superpowers.md` or `evaluations/feature-dev.md` exists; superpowers' grounding comes from the CATALOG overlap rows and the STACK GSD-row install, and feature-dev's from `claude-plugins-official.md` (its first-party marketplace source) and `gsd.md`.

## What worked

- **agent-skills has the deepest, broadest lifecycle.** `agent-skills-addyosmani.md` rates it **ADOPT** — "the highest-quality full-lifecycle skill collection in the catalog. 24 skills with genuinely deep content (not checklists), 7 intuitive slash commands, `/build auto` for autonomous implementation." Its `doubt-driven-development` (mid-flight adversarial review) and `source-driven-development` skills are "unique innovations not found in competing collections."
- **GSD's context-rot mitigation is a real differentiator.** `gsd.md`: running "heavy work in fresh-context subagents while keeping the main session lean, plus durable `STATE.md`/`CONTEXT.md` artifacts across sessions, is a concrete, well-motivated design — not persona theater." It is the operator's verified incumbent (v1.22.4), so for this user "there is nothing to install."
- **feature-dev is first-party and tightly scoped.** From `claude-plugins-official.md`, feature-dev ships in Anthropic's official marketplace (lowest supply-chain risk) and is purpose-built for single-feature work — exactly the scale where GSD's 40+ `/gsd:*` commands are overkill.
- **The frameworks are complementary, not strictly redundant.** `mattpocock-vs-agent-skills.md` concludes "use both" for the skills layer — agent-skills gives *lifecycle coverage* (incremental implementation, CI/CD, shipping, security hardening) while mattpocock gives *philosophy and vocabulary*. The same logic scales the cluster: each tool's sweet spot is a different project size.

## What didn't work or surprised us

- **Layering all four is the failure mode STACK warns against.** Running GSD's phase loop *and* agent-skills' `/spec→/ship` *and* feature-dev's 7 phases simultaneously means three competing orchestration disciplines fighting for the same loop. STACK's "pick one as primary" exists precisely to prevent this.
- **agent-skills is more prescriptive than it first appears.** `agent-skills-addyosmani.md`: "The 7-command lifecycle is opinionated — using just 2-3 commands feels incomplete, and the auto-activation can surprise users." It also lacks domain-modeling vocabulary and systematic grilling skills (mattpocock covers those).
- **GSD's ceremony is overkill for small changes.** `gsd.md`: "40+ `/gsd:*` commands and a multi-agent fleet are a lot of process for small changes — the same 'great for greenfield/large features, overkill for a one-line fix' tradeoff." It also drifts (the installed copy is materially behind upstream).
- **feature-dev is the narrowest.** It does single-feature flow well but doesn't carry milestone/roadmap state across sessions the way GSD does; it is a scope choice, not a full project methodology.

## Quality signals affected

| Signal | agent-skills | superpowers | GSD | feature-dev |
|--------|--------------|-------------|-----|-------------|
| Correctness | + (gated /spec→/ship, doubt-driven mid-flight review) | + (TDD + verification-before-completion discipline) | + (Discuss→Verify gates, goal-backward verification) | + (per-feature plan→verify) |
| Speed | + (`/build auto` autonomous multi-task) | + (structured workflows cut decision overhead) | + large / − small (fresh-context subagents vs. phase ceremony) | + (focused single-feature flow) |
| Maintainability | + (ADR + code-simplify skills) | + (methodology survives in skills) | + (durable PROJECT.md/roadmap/CONTEXT.md artifacts) | neutral (no cross-session state) |
| Safety | + (security-auditor agent + checklist) | + (verification gates) | neutral/+ (restricted-tool subagents, verify step) | + (first-party, lowest supply-chain risk) |
| Cost Efficiency | neutral (no token optimization) | neutral | neutral/+ (context-rot mitigation, offset by subagent passes) | + (light footprint) |

## Verdict

**Winner: agent-skills (ADOPT) as the recommended primary.** STACK frames this cluster as "pick one as primary," and agent-skills is the broadest, deepest default: `agent-skills-addyosmani.md` rates it the **highest-quality full-lifecycle skill collection in the catalog**, its 7-command `/spec→/ship` pipeline covers the whole loop with genuinely deep skills (not checklists), `/build auto` gives autonomous multi-task implementation, and it is cross-editor. For a general-purpose default loop, it is the recommended primary.

**When a runner-up wins instead:**
- **superpowers (ADOPT)** for heavier *planning* discipline — milestone/phase structure, brainstorming-first, and verification-before-completion rigor; pull it in when planning ceremony pays off.
- **GSD (KEEP)** when the work is multi-session or greenfield and context rot is the real enemy — its fresh-context subagents + durable `STATE.md`/`CONTEXT.md` make long projects resumable. It is also the operator's installed incumbent, so for this user it's already the in-session default.
- **feature-dev (KEEP)** for a *single feature* — its tight, first-party 7-phase flow is the right scale where GSD's 40+ commands are overkill.

Run exactly one as the default and reach for the others only when their scale fits; layering all four is the anti-pattern this cluster exists to prevent.

## Catalog entry

n/a — this compares existing catalog entries (agent-skills, superpowers, GSD, feature-dev) rather than introducing a new row.
