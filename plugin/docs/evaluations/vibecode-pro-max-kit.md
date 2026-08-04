# Evaluation: vibecode-pro-max-kit

**Repo:** [withkynam/vibecode-pro-max-kit](https://github.com/withkynam/vibecode-pro-max-kit)
**Stars:** 948 | **Last updated:** 2026-06-17 (pushed; created 2026-05-27) | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Inner loop, full sweep — Plan (Research/Spec/Innovate/Plan), Implement (Execute), Verify (Validate, test-check-fix loops), plus Reflect (self-improving project memory / Update-Process). A spec-driven autopilot harness.
**Layer:** Process + Tooling (a RIPER-5 workflow expressed as Claude Code agents/skills, plus real Node.js hooks — installed per project, no server)

---

## What it does

The catalog one-liner: "Spec-driven coding harness with self-improving context memory and 15-agent autopilot." It drops a RIPER-5-style plan-first process into any project via one `curl | bash` installer (Node ≥ 22). The advertised shape: **15 agents · 33 skills · 10 hooks · 36 validators**, version 3.0.0.

The mechanism is a 7-gated-phase workflow (Research → Spec → Innovate → Plan → Validate → Execute → Update-Process) implemented as Claude Code subagents (`.claude/agents/vc-*.md` — plan, spec, research, execute, validate, tester, code-reviewer, code-simplifier, debugger, git-manager, ui-ux-designer, etc.) backed by real Node.js hooks under `.claude/hooks/` (with `__tests__/` — actual unit tests). The selling points: a `/goal` "run-until-done" token that keeps the agent looping phase-to-phase and resumes in a fresh session; **PVL + EVL self-healing loops** (plan-check-fix and test-check-fix, up to 10 cycles); three autopilot lanes (quick/fast/full) matching ceremony to risk; a "smart strategy picker" that weighs one-agent vs. many vs. team with cost estimates; "smart model use" (expensive model writes code, cheaper model does the rest); progress notes written to disk every phase to survive context resets; and a `vc-setup` step that scans the codebase to build project-specific knowledge groups. Notably, the hooks include real safety/quality machinery: a `privacy-block.cjs`, a `scout-block` broad-pattern detector (with its own test suite), `post-edit-simplify-reminder`, `post-write-plan-check`, and `post-commit-lint`.

So: a spec-driven, autopilot, self-healing Claude Code/Codex harness aimed explicitly at "vibecoders, product owners, CEOs" — non-engineers who want hands-free shipping.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No `install.sh` was piped to a shell, no `vc-setup` scan ran, no `/goal` autopilot loop executed, and no PVL/EVL self-healing cycle was observed. Every claim below comes from the repository (GitHub metadata, README, full recursive file tree showing the agents/hooks/tests, release tags, single-contributor history), not from observed behavior. The "36 validators," "10 cycles," "kills context rot," and "ships features not spaghetti" figures are the author's README marketing, not anything I measured.

```bash
gh api repos/withkynam/vibecode-pro-max-kit --jq '{desc,stars:.stargazers_count,forks:.forks_count,pushed:.pushed_at,created:.created_at,license:.license.spdx_id,lang:.language}'
gh api repos/withkynam/vibecode-pro-max-kit/readme --jq '.content' | base64 -d
gh api "repos/withkynam/vibecode-pro-max-kit/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api repos/withkynam/vibecode-pro-max-kit/commits --jq 'length'        # 30 (page-1 cap)
gh api repos/withkynam/vibecode-pro-max-kit/releases --jq '.[].tag_name'  # v3.0.0 … v2.3.0 (5 releases)
gh api repos/withkynam/vibecode-pro-max-kit/contributors --jq '[.[].login]'  # ["withkynam"] — single author
```

## What worked

- **There is real engineering under the hype.** Unlike pure prompt packs, the hooks are tested Node.js: `.claude/hooks/__tests__/` and `scout-block/tests/` contain genuine unit tests for the statusline, session-state, context-builder, project-detector, and pattern-matcher. Someone is testing their own tooling — rare in this space.
- **Coherent, opinionated workflow.** RIPER-5 (Research→Spec→…→Execute) with gates is a sound plan-first discipline, and the spec sign-off step ("state what to build in plain user stories before any design") puts intent-capture at the cheapest point to catch mistakes.
- **Concrete safety hooks.** `privacy-block` and a `scout-block` broad-pattern detector (blocking overbroad reads/edits) are real PreToolUse-style guardrails, not just instructions — and they ship with tests.
- **Cost-awareness is built in.** The "expensive model codes, cheap model does the rest" routing and a strategy picker with cost estimates target Cost Efficiency directly — a signal most harnesses ignore.
- **Resumability by design.** Per-phase progress notes to disk plus a resumable `/goal` token addresses context rot concretely (state survives a session reset), which is the central failure mode it names.
- **Actively versioned.** 5 tagged releases (through v3.0.0) in under a month, cross-tool install (Claude Code, Codex, Cursor, Windsurf, Copilot, OpenCode), 10-language README.

## What didn't work or surprised us

- **Hype-name and hype-copy demand heavy discounting.** "pro-max-kit," anime GIFs, "Total Concentration — Spec Breathing," "Built by world-class engineers," "ships features, not spaghetti," "0 need for human gate" — the marketing is loud and the claims (36 validators, 10-cycle self-healing, "kills context rot") are entirely self-asserted with no benchmark. Treat every superlative as unverified.
- **Single author, ~3 weeks old.** Created 2026-05-27, one contributor (`withkynam`), tied to a commercial product (flowser.ai). Bus factor of one on a harness that runs *autopilot with no human gate* is a real risk.
- **"0 need for human gate" is a feature and a hazard.** A hands-free loop running up to 10 self-healing cycles, marketed to non-engineers ("CEOs, vibecoders"), is exactly the population least equipped to catch when the autopilot confidently ships the wrong thing. The self-healing loops verify against the *spec and tests it wrote itself* — closed-loop validation, not external truth.
- **curl | bash install from a single-author repo.** The one-line installer pipes a remote script to a shell; combined with a young, single-maintainer, commercially-affiliated project, that is a supply-chain surface to weigh.
- **Heavy overlap with more mature options.** GSD already does context-engineering Discuss→Plan→Execute→Verify→Ship with durable STATE.md and restricted-tool subagents; superpowers does TDD/review/verification skills; ralph-claude-code does autonomous loops with exit detection. vibecode-pro-max-kit recombines these ideas with more marketing and less track record.
- **Complexity for the stated audience.** 15 agents + 33 skills + 10 hooks + 36 validators + 7 phases + 3 lanes is a lot of machinery to drop on "vibecoders"; the simplicity it promises is buried under its own surface area.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + / − | Plan-first gates, spec sign-off, and test-check-fix loops push toward correctness; but self-healing validates against self-written specs/tests (closed loop), and "no human gate" removes the external check. |
| Speed | + | `/goal` autopilot, resumable disk state, and quick/fast lanes get from intent to shipped change with minimal hand-holding — when it stays on track. |
| Maintainability | + / neutral | Spec-first + simplify hooks + self-improving project memory aim at maintainable output; unproven, and the kit's own 15/33/10/36 surface area is itself a lot to maintain. |
| Safety | − | curl\|bash install, single-author/commercial-affiliated, ~3 weeks old, autopilot with "0 human gate"; partially offset by real `privacy-block`/`scout-block` guardrail hooks (with tests). |
| Cost Efficiency | + | Explicit cheap-model-for-everything-but-code routing and a cost-estimating strategy picker target token spend directly — a differentiator vs. most harnesses. |

## Verdict

**SKIP** — redundant with [`superpowers`/GSD](https://github.com/obra/superpowers) (STACK, `MEASURED`) on the spec-driven-workflow job, and the delta it sells is one its
own evaluation says never to enable: *"try it in a sandbox, with a human gate, never as unattended
autopilot on real work."*

The RIPER-5 plan-first workflow, resumable state and cost routing are the discipline layer the
incumbent occupies, and methodology packs do not stack. What is left as differentiation is the
15-agent hands-free autopilot, marketed as *"0 need for human gate"* — a claim aimed at
non-engineers that the evaluation identifies as the riskiest possible combination with everything
else about the project.

Everything else about the project is the reason the redundancy is not even the strongest argument:
single-author, roughly three weeks old, commercially affiliated, ★1K, installed via `curl | bash`.
The evaluation's honest finding is that there is real substance underneath (tested Node hooks,
genuine PreToolUse guardrails) — substance is not the issue; trust surface is.

Re-open if it matures, drops the unattended-autopilot pitch, and ships a reviewable install path.

_Triaged 2026-08-04 by the P2 challenger band ([#262](https://github.com/mattbutlerengineering/ai-tooling/issues/262))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [vibecode-pro-max-kit](https://github.com/withkynam/vibecode-pro-max-kit) | harness | Spec-driven RIPER-5 autopilot harness (15 agents/33 skills/10 tested hooks) with self-healing plan/test loops, resumable disk state, and cheap-model cost routing; single-author, ~3 weeks old | AI loses context and ships spaghetti; want spec-first gated phases with hands-free loops — but it markets "0 human gate" to non-engineers | GSD, superpowers, ralph-claude-code (more mature takes on plan-first / autonomous-loop harnesses) |
