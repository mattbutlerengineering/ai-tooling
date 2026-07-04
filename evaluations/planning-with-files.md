# Evaluation: planning-with-files

**Repo:** [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files)
**Stars:** 23,613 | **Last updated:** 2026-06-16 (created 2026-01-03) | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Plan (with carry-through to Implement/Verify via durable progress + completion gate)
**Layer:** Process (a planning discipline) with a Tooling spine (lifecycle hooks + shell/PowerShell scripts)

---

## What it does

Catalog one-liner (as filed): "Persistent file-based planning that survives context loss, /clear, and crashes." planning-with-files is a single Claude Code / Agent-Skills skill that codifies the "Manus" context-engineering pattern: treat the context window as volatile RAM and the filesystem as durable disk, so anything important is written to markdown on disk. It standardizes a **3-file pattern** the agent maintains for any multi-step task:

- `task_plan.md` — phases, status checkboxes, decisions, an errors table
- `findings.md` — research/discoveries (and the designated sink for untrusted external content)
- `progress.md` — session log and test results

The mechanism is not just a prompt. The SKILL.md frontmatter registers **lifecycle hooks** that do the enforcement: `UserPromptSubmit` re-injects the active plan at the start of each turn (so goals stay in the attention window as the conversation grows), `PreToolUse` re-injects before tool calls (legacy mode), `PostToolUse` (on Write/Edit) nudges the agent to update `progress.md`, `PreCompact` reminds the agent to flush progress before `/compact`/autoCompact and prints the attested `Plan-SHA256`, and `Stop` runs a completion check. Bundled scripts add real machinery: `init-session.sh` (with a slug mode for parallel isolated plans under `.planning/YYYY-MM-DD-<slug>/`), `set-active-plan.sh`/`resolve-plan-dir.sh` (multi-plan switching), `check-complete.sh` (deterministic completion gate), `session-catchup.py` (recovers context after `/clear` by diffing planning-file mtimes against the IDE session store), and `attest-plan.sh` (SHA-256 locks the plan; hooks refuse to inject a tampered plan). v3 adds opt-in `--autonomous` (drops per-tool-call recitation for strong models, keeps turn-start injection) and `--gated` modes (a host-aware Stop gate that blocks termination until the plan reports complete, with a block-count cap and stall detector so it can't trap a session). It installs across 60+ agents via the SKILL.md open standard.

## How we tested it

**Evidence:** REVIEW

**Inspected the repo, README, the canonical English `skills/planning-with-files/SKILL.md`, the file tree, and release history via the GitHub API. I did not install it, did not run the hooks, and did not execute a planning loop. No metrics in this document are mine — the 96.7% pass-rate figure below is the author's self-reported benchmark, quoted as such.** The decisive question for the catalog is not "does file-based planning work" (it plainly does — it is the same principle the user's incumbent GSD is built on) but "is a *standalone* planning-files skill additive for a user who already runs GSD and superpowers?" That is a redundancy comparison, answerable from the skill's mechanism plus the user's installed footprint.

```bash
gh api repos/OthmanAdi/planning-with-files --jq '{stars,license,description,pushed_at,created_at,forks,open_issues}'
# 23,613 stars, MIT, created 2026-01-03, pushed 2026-06-16, 2066 forks, 6 open issues
gh api "repos/OthmanAdi/planning-with-files/git/trees/master?recursive=1" --jq '.tree[].path'   # default branch is master, not main
gh api repos/OthmanAdi/planning-with-files/readme --jq '.content' | base64 -d                    # full README
gh api repos/OthmanAdi/planning-with-files/contents/skills/planning-with-files/SKILL.md -q .content | base64 -d  # canonical SKILL.md + hooks
# Local footprint check (redundancy question):
ls -d ~/.claude/skills/planning-with-files            # not installed
ls ~/.claude/plugins/marketplaces/ | grep planning    # not installed
grep -rl "STATE.md\|CONTEXT.md" ~/.claude/get-shit-done/   # GSD already manages durable planning state on disk
```

## What worked

- **The hooks are the real differentiator, and they are well-engineered.** This is not "tell the model to write a plan." The `UserPromptSubmit`/`PreCompact` re-injection is a concrete implementation of Anthropic's "structured note-taking": durable state outside the window, read back in each turn. The hook commands are defensively written (auto-resolve skill dir, fall back to known install paths, `exit 0` so they never break the session).
- **Genuine maturity for a five-month-old project.** 23.6K stars, MIT, 2K forks, only 6 open issues, pushed within days of this eval, a 180+-test suite, version 3.1.3, and an unusually disciplined CHANGELOG (security hardening, YAML-frontmatter validation, cross-platform shebang/exec-bit fixes, KV-cache hygiene). This is not a thin skeleton — it is over-built relative to most single skills.
- **Security awareness above the norm for a planning skill.** It explicitly treats `findings.md` as the untrusted-content sink, wraps injected plan content in BEGIN/END data delimiters, and ships opt-in (legacy) / default-on (v3) SHA-256 attestation so a silently-rewritten `task_plan.md` is refused at injection. It is honest about the limits (nonce can't defend against an attacker with plan-write access; attestation is the real control).
- **The completion gate is a real idea GSD-style frameworks also chase.** The v3 gated mode judges the plan artifact on disk (a termination oracle) rather than the transcript, with a block cap and stall detector to avoid trapping the user — directly informed by a real "accidental blocking infuriates users" issue (#178).
- **Portability the user's incumbent does not match.** One `npx skills add` installs it across Claude Code, Codex, Cursor, Gemini CLI, Copilot, Kiro, and 60+ runtimes via the SKILL.md standard.

## What didn't work or surprised us

- **Heavy conceptual overlap with the user's incumbent GSD.** GSD already implements durable file-based planning that survives session boundaries (`STATE.md`, `CONTEXT.md`, `PROJECT.md`, roadmap/phase files under `.planning/`) plus a deterministic CLI for state transitions and a verify gate — confirmed in the user's installed `~/.claude/get-shit-done/`. planning-with-files' core thesis (filesystem as memory, re-read the plan, completion check) is the *same* thesis GSD is built on. For this user the 3-file pattern is a lighter re-statement of something they already run more comprehensively.
- **Two skills, one trigger, competing artifacts.** planning-with-files fires on "plan/break down a multi-step task"; GSD owns the same Plan stage and writes its *own* planning tree. Running both means two planning vocabularies (`task_plan.md`/`findings.md`/`progress.md` vs GSD's `STATE.md`/`CONTEXT.md`/phase files) and two sets of hooks competing to inject "the plan" — exactly the dueling-phase-gate problem flagged in the diagnosing-bugs eval, but at the Plan stage.
- **It is not currently installed.** Nothing to retarget or de-dup in `~/.claude` — this is a genuine adopt/skip decision, not catalog hygiene like GSD was.
- **The headline benchmark is narrow and self-reported.** The README is candid that 96.7% measures *file-pattern fidelity* (did the agent create/maintain the 3 files) on `claude-sonnet-4-6` at v2.21.0 — not goal-drift reduction over long autonomous runs, and not on current models. It is evidence the pattern is followed, not that outcomes improve.
- **Marketing-forward framing.** "Work like Manus — the company Meta bought for $2 billion" leads the README. The engineering underneath is solid, but the pitch oversells; the actual value is the disciplined hook plumbing, not the Manus association.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Turn-start plan re-injection + completion gate + 3-strike error protocol keep goals in attention and force a done-check; but GSD already supplies this for the user |
| Speed | + (long/multi-session) / - (small) | Session-catchup after `/clear` and durable progress make long runs resumable; the 3-file ceremony + per-tool injection is overhead for small tasks (v3 autonomous mode drops the per-call tax) |
| Maintainability | + | `task_plan.md`/`findings.md`/`progress.md` persist intent, decisions, and errors in the repo rather than in throwaway context |
| Safety | + | findings.md untrusted-content sink, BEGIN/END data delimiters, and SHA-256 plan attestation are above-average prompt-injection rails for a planning skill; runs in-session with no new API key |
| Cost Efficiency | neutral | Context-rot mitigation cuts re-planning waste; offset by per-tool-call plan injection in legacy mode (author measured a +68% token tax, addressed by v3 autonomous mode) |

## Verdict

**SKIP** (for this user — redundant with the incumbent GSD; would be CONDITIONAL/ADOPT for a user without a planning framework)

planning-with-files is a high-quality, unusually mature, security-aware skill that does exactly what it claims: durable file-based planning that survives `/clear`, compaction, and crashes, enforced by real lifecycle hooks rather than prose. The reason to skip is not quality — it is **redundancy with the user's incumbent GSD**, which already implements the same filesystem-as-memory thesis with durable `STATE.md`/`CONTEXT.md`/phase artifacts, a deterministic state CLI, and a verify gate (verified installed at `~/.claude/get-shit-done/`). Adopting planning-with-files alongside GSD would put two planning skills on the same "plan this" trigger, writing two competing artifact sets with two hook stacks injecting "the plan" — net friction, not net capability. This mirrors why spec-kit and claude-task-master were judged redundant for this user: GSD already owns the Plan→Implement→Verify loop in-session.

For a user *without* a planning framework, this would be a strong **CONDITIONAL/ADOPT** — it is arguably the best standalone Manus-style planning skill available, and its multi-runtime portability (Codex, Cursor, Gemini, 60+ agents via SKILL.md) exceeds GSD's. Re-evaluate if the user ever drops GSD, or for cross-runtime work where GSD's Claude-centric install doesn't reach. The catalog "Overlaps with" should keep **GSD** as the primary overlap (the redundancy that drives this verdict) alongside feature-dev and plannotator (complementary visual review).

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [planning-with-files](https://github.com/OthmanAdi/planning-with-files) | skill | Manus-style persistent 3-file planning (task_plan/findings/progress) with lifecycle hooks that survive context loss, /clear, and crashes; 60+ agents via SKILL.md (23.6K stars) | Agents lose track of multi-step plans when context resets, compacts, or crashes; keep durable plan state on disk and re-inject it each turn | GSD (durable STATE.md/CONTEXT.md planning — primary redundancy), feature-dev, plannotator (complementary: visual plan review) |
