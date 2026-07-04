# Evaluation: architect-loop

**Repo:** [DanMcInerney/architect-loop](https://github.com/DanMcInerney/architect-loop)
**Stars:** 518 | **Last updated:** 2026-06-13 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Plan + Implement (also Review/Verify within the loop)
**Layer:** Process

---

## What it does

Claude Fable as architect, GPT-5.5 Codex as builder — a cross-vendor agent loop where the repo is the only memory. It ships as **two Claude Code skills** (`/architect` for the build loop, `/architect-research` for the research loop) that wire a strict separation of roles: Claude Fable (high effort) does planning, slice decomposition, gate-writing, and judgment — and never writes implementation code. The actual building is delegated to parallel `codex exec` runs (GPT-5.5, xhigh reasoning), each in its own git worktree.

The mechanism is concrete and enforced. Per work block, Fable: (1) specs a one-PR slice and splits it into 1–4 lanes whose file-touch sets are checked for overlap; (2) commits acceptance gates to `docs/gates/<slice>.md` *before* any builder starts — gates are frozen, and a builder edit to a gate file (caught by `git diff`) is an automatic slice FAIL; (3) dispatches one fresh `codex exec --sandbox workspace-write -m gpt-5.5` per lane in an isolated worktree, with builders required to argue with the spec (silent compliance = defect) and forbidden commit access; (4) in a *fresh* session, runs the gate commands itself (builder claims are treated as hearsay), reads the diff against the spec's intent, then merges passing lanes. State lives entirely in the repo: `docs/HANDOFF.md` (a pruned ~150-line table of contents), `docs/gates/`, `docs/lanes/`, and git history. The research skill follows a scout → design-lanes → parallel-fan-out → adversarial-verify → single-author-write pattern modeled on production deep-research systems.

No API keys required by default: Claude Code runs on the Claude plan, Codex CLI on a ChatGPT plan.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README, `DESIGN.md`, the two `SKILL.md` files, `dispatch.md`, `install.sh`, and `tests/validate_skills.py`, plus repo metadata. Not hands-on installed/run — executing a full loop requires an active ChatGPT/Codex CLI subscription (≥ 0.133) alongside Claude Code, and would consume a meaningful fraction of a weekly Codex quota per run. Verdict is based on inspecting the actual skill mechanics, the verified-live dispatch commands, and the cited design rationale.

```bash
gh api repos/DanMcInerney/architect-loop --jq '{stars,license,description,created,updated}'
gh api repos/DanMcInerney/architect-loop/readme --jq '.content' | base64 -d
gh api "repos/DanMcInerney/architect-loop/git/trees/main?recursive=1" --jq '.tree[].path'
gh api repos/DanMcInerney/architect-loop/contents/skills/architect/SKILL.md --jq '.content' | base64 -d
gh api repos/DanMcInerney/architect-loop/contents/skills/architect/dispatch.md --jq '.content' | base64 -d
gh api repos/DanMcInerney/architect-loop/contents/install.sh --jq '.content' | base64 -d
```

## What worked

- **The reasoning/execution split is real and enforced, not aspirational.** The architect skill's hard rules forbid it from writing implementation code, freeze gates before results exist, treat builder claims as hearsay, and forbid judging a run in the same session that dispatched it. These are concrete, checkable invariants, not vibes.
- **Cross-vendor by design with a defensible rationale.** Cited research ("weak planners hurt more than weak executors") motivates putting the stronger-reasoning model on design and the strong-coding model on execution. `DESIGN.md` documents 12 enforced rules, a failure-mode table, and full source citations — unusually rigorous for a single-author skill.
- **Worktree isolation + frozen external gates is a sound topology.** Manager + worktree-isolated parallel workers avoids the shared-file coordination collapse that naive multi-agent setups hit. Gates committed before dispatch, plus the architect re-running gates and reading the diff, directly counter the well-known "agents game visible tests and ship unmergeable green PRs" failure.
- **Repo-as-memory avoids memory-file rot.** HANDOFF.md is deliberately kept a short pruned map with detail pushed to linked gate/lane files — a thoughtful answer to the context-rot problem other memory tools wrestle with.
- **Operationally careful.** `dispatch.md` is "verified live against Codex CLI 0.139," corrects real CLI misinformation (model slug `gpt-5.5`, `--search`/`-a` rejected by `codex exec`), mandates a canary first dispatch, stdin-not-argument prompt passing, liveness checks, stall triage, and explicit timeouts. `tests/validate_skills.py` enforces frontmatter limits, links, and fences.
- **Trivial install.** `./install.sh` copies the two skills to `~/.claude/skills/`; `--project` scopes to one repo. No build step.

## What didn't work or surprised us

- **Hard dependency on a second paid subscription.** The builder is Codex CLI signed into a ChatGPT plan. Without it, only the architect half functions — and the architect deliberately never writes code, so the loop is inert. This is a two-vendor commitment, not a Claude-Code-only tool.
- **Cost asymmetry is significant.** The FAQ states a multi-hour builder run is "a meaningful fraction of a weekly window" of the ChatGPT plan's quota, and research-grade fan-out is "~15× chat-level tokens." You are burning two metered budgets, and the heavy one (Codex execution) is the one with the harder weekly cap.
- **Very young and single-author.** Created 2026-06-12, ~518 stars in days, one maintainer, derived from an X-post idea. No release history, no external contributors yet, no track record across CLI version churn — and it explicitly depends on Codex CLI flags that "churn between versions" (its own warning).
- **Heavy process overhead for the payoff.** Gates, lanes, worktrees, freeze commits, fresh-session judging, handoff pruning — the loop is slice-sized ceremony. The skill itself says trivial fixes should skip it. The value only materializes on genuinely PR-sized, parallelizable work.
- **Not hands-on validated here.** Claims about merge quality and throughput rest on the design's cited research and the skill's enforced rules, not on an observed run in this environment.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Frozen pre-committed gates, architect re-runs gates itself (builder claims = hearsay), reads diff against intent before merge, mandatory builder disagreement |
| Speed | + (large slices) / - (small) | Parallel worktree-isolated builders speed PR-sized work; per-slice ceremony makes it slower than a normal session for trivial fixes |
| Maintainability | + | Repo-as-memory with pruned HANDOFF.md, gates/lanes as durable artifacts, diff-against-intent review keeps merges principled |
| Safety | + | Builders run `--sandbox workspace-write` with no commit access; nothing reaches a branch until tamper/boundary/gate checks pass; broken worktrees discarded and re-dispatched from freeze commit |
| Cost Efficiency | - | Requires two paid subscriptions; Codex builder runs consume a meaningful fraction of a weekly ChatGPT quota; research fan-out ~15× chat tokens |

## Verdict

**CONDITIONAL**

Adopt when you (1) hold both a Claude paid plan and a ChatGPT/Codex CLI subscription, and (2) regularly do PR-sized, parallelizable work where the planning-vs-execution split and frozen-gate review pay for the ceremony. The cross-model separation is genuinely well-reasoned and rigorously enforced — this is one of the more disciplined multi-agent skills in the catalog, and its DESIGN.md is a model of source-backed justification. But the second paid subscription, the heavy Codex-side weekly-quota cost, the single-author/days-old maturity, and the per-slice overhead make it a deliberate choice for a specific workflow, not a default. Single-vendor Claude-Code users, or anyone doing small/inline changes, get little from it. Re-evaluate maturity (releases, contributors, resilience to Codex CLI version churn) after it has run for a few months.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [architect-loop](https://github.com/DanMcInerney/architect-loop) | skill | Claude Fable 5 as architect, GPT-5.5 Codex as builder — cross-vendor agent loop | Single-vendor agent loops miss cross-model strengths; separates reasoning from execution | compound-engineering, claude-code-staff-engineer |
