# Evaluation: plannotator

**Repo:** [backnotprop/plannotator](https://github.com/backnotprop/plannotator)
**Stars:** 6,338 | **Last updated:** 2026-06-19 | **License:** Apache-2.0 (dual-licensed Apache-2.0 / MIT)
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Review (plan review at the Plan→Implement gate; diff/PR review at the Implement→Ship gate)
**Layer:** Tooling

---

## What it does

Annotate and review coding agent plans and code diffs visually, share with your team, send feedback to agents with one click. Plannotator is a local, browser-based review surface that plugs into a coding agent through its hooks and slash commands. Three review modes: (1) **plan review** — no command needed; it is wired into the harness's hooks so any time the agent proposes a plan, a markdown review UI opens in the browser; (2) **code review** — `/plannotator-review` captures `git diff` (or fetches a GitHub PR / GitLab MR by URL) and opens a side-by-side diff viewer; (3) **artifact annotation** — `/plannotator-annotate <file | folder | URL>` and `/plannotator-last` annotate any markdown, HTML, or the agent's last message.

The mechanism for plan review (the load-bearing path) on Claude Code is precise: the agent calls `ExitPlanMode` → a `PermissionRequest` hook with matcher `ExitPlanMode` fires the `plannotator` binary (with a 345,600s / 4-day timeout, i.e. it blocks until the human responds) → a local server reads the plan from the hook's stdin payload → it opens a browser on a random local port with the review UI → the human marks up the plan inline → **Approve** lets the agent proceed; **Request changes** returns the annotations as structured feedback (a hook deny with a reason), so the agent revises and a "plan diff" shows what changed on resubmission. A second `PreToolUse`/`EnterPlanMode` hook (`plannotator improve-context`, 5s) runs as the agent *enters* plan mode. Code review works the same loop in reverse: comments and suggested code on the diff are sent back into the agent session; Approve sends "LGTM."

Distribution: a single `curl | bash` installer drops a compiled `plannotator` binary, auto-detects installed agents, and configures hooks/skills/slash-commands for each of nine agents (Claude Code, Codex, Copilot CLI, Gemini CLI, OpenCode, Kiro, Droid, Amp, Pi). On Claude Code the recommended path is the plugin marketplace (`/plugin marketplace add backnotprop/plannotator` → `/plugin install plannotator@plannotator`, then restart), with a documented manual-hook fallback. Sharing is client-side encrypted: small plans encode entirely in the URL hash (no server); large plans go through a short-link service, AES-256-GCM encrypted in-browser with the key living only in the URL fragment (PrivateBin model), auto-deleting after 7 days, self-hostable, and disableable with `PLANNOTATOR_SHARE=disabled`. Integrations include VS Code, Obsidian, and Bear for saving approved plans.

## How we tested it

**Evidence:** REVIEW

Repo + README + plugin-config inspection. **Did not install or run the binary.** Method: pulled repo metadata via the GitHub API; read the full root `README.md`, the Claude Code plugin README (`apps/hook/README.md`), and the actual Claude Code hook configuration (`apps/hook/hooks/hooks.json`); enumerated the repo tree to confirm the plugin manifest, the compiled-binary server (`apps/hook/server/`), and the presence of tests; and checked release cadence/tags for maturity. I read the exact `ExitPlanMode` → `PermissionRequest` hook wiring rather than paraphrasing the marketing claim, which is what lets me describe the blocking-review mechanism with confidence. I did not exercise a live plan-review round-trip in a throwaway repo, so claims about UI ergonomics and round-trip latency are from documentation, not observation.

```bash
gh api repos/backnotprop/plannotator --jq '{stars:.stargazers_count,license:.license.spdx_id,description,pushed_at,created_at,language,open_issues:.open_issues_count,homepage}'
gh api repos/backnotprop/plannotator/readme --jq '.content' | base64 -d            # full README
gh api "repos/backnotprop/plannotator/git/trees/HEAD?recursive=1" --jq '.tree[].path' | grep -iE 'claude|mcp|cli|package.json|hook|README|bin'
gh api repos/backnotprop/plannotator/contents/apps/hook/README.md --jq '.content' | base64 -d
gh api repos/backnotprop/plannotator/contents/apps/hook/hooks/hooks.json --jq '.content' | base64 -d   # the actual hook wiring
gh api repos/backnotprop/plannotator/tags --jq '.[].name'                          # release cadence
# Catalog overlap scan:
grep -inE "plannotator|planning-with-files|plan review|ExitPlanMode" /Users/mbutler/github/ai-tooling/CATALOG.md
```

## What worked

- **It intercepts at exactly the right place in the dev loop.** The `PermissionRequest`/`ExitPlanMode` hook fires at the Plan→Implement boundary — the single highest-leverage gate, because every wasted implementation turn downstream traces back to a plan the human waved through. The 4-day hook timeout means the agent genuinely *blocks* on human review rather than racing ahead, which is the correct semantics for a gate (contrast with after-the-fact review, where the bad work is already done).
- **The deny path is structured feedback, not a binary reject.** "Request changes" returns the inline annotations to the agent as the hook's denial reason, and resubmission shows a plan diff. This closes the loop in a way a plain approve/deny prompt cannot — the agent gets *what to fix and where*, which is the difference between a review tool and a gate that just says "no."
- **Strong maturity and provenance signals.** 6.3K stars, created Dec 2025, pushed today, latest release v0.20.3 (2026-06-16) atop a dense tag history (multiple v0.19.x and v0.20.x), dual Apache-2.0/MIT license, tests in the repo (`cli.test.ts`, `codex-session.test.ts`, `session-log.test.ts`), and an official docs site. This is an actively maintained, fast-shipping project, not a weekend prototype.
- **Security posture is unusually serious for a dev tool.** Released binaries ship SHA256 sidecars and SLSA build-provenance attestations (from v0.17.2), with an opt-in `--verify-attestation` install path. Team sharing is client-side AES-256-GCM encrypted with the key never leaving the URL fragment, server stores only ciphertext, 7-day auto-delete, self-hostable, and fully disableable. For a tool that pipes your plans/diffs through a browser and optional share service, this directly answers the obvious "where does my code go" objection.
- **One installer, nine agents, low lock-in.** The single `curl | bash` installer auto-detects agents and wires each one's native hook/skill/command surface; on Claude Code it ships as a proper plugin via the marketplace. The manual-hook fallback is a four-line `settings.json` snippet, so adoption and removal are both cheap and transparent.
- **Plan review needs zero workflow change.** Because it rides the existing plan-mode hook, the human does nothing differently until a plan appears — it opens automatically. That is the right ergonomics for a quality gate: it can't be forgotten, and it adds no command to remember.

## What didn't work or surprised us

- **It is a human-in-the-loop tool, which caps its fit for autonomous/AFK workflows.** The whole value proposition is *blocking the agent until a human reviews*. In fully autonomous or fleet/AFK setups (the kind this catalog also tracks), a 4-day blocking hook on every plan is the opposite of what you want. Its sweet spot is interactive, single-developer-with-agent sessions and team plan review — not unattended pipelines.
- **Reviewing in a browser is a context switch.** The benefit (rich visual annotation, diff viewer, side-by-side) comes at the cost of leaving the terminal/editor for the browser on every plan and every review. For developers who live in the TUI, this friction is real; the VS Code extension mitigates it but adds another moving part.
- **Heavier and more opinionated than the plan-mode default.** Claude Code already has a built-in plan-mode approve/deny prompt. Plannotator replaces a zero-install built-in with a compiled binary, a plugin, multiple hooks (including a `PreToolUse` `improve-context` hook on every plan-mode entry), and a browser surface. The added capability (inline annotation + structured feedback + sharing) is real, but it is not free — it's more surface area to install, trust, and keep updated against a fast release cadence.
- **110 open issues** for a six-month-old project signals both heavy usage and a still-stabilizing surface across nine agent integrations; the per-agent install steps vary (some "nothing," some manual plugin copies, some `npm:` extensions), so the experience is uneven across harnesses. Claude Code's path is among the better-supported ones.
- **Could not verify UI/round-trip ergonomics first-hand.** Claims about annotation feel, how cleanly the plan diff renders, and review latency are documentation-derived. The mechanism is sound on paper; the lived experience is unverified here.
- **Overlap is genuinely complementary, as the catalog states.** `planning-with-files` persists plans to disk for durability and re-grounding; plannotator gates and annotates the plan at the moment of proposal. They address different halves of "the plan matters" — durability vs. human review — and compose well rather than competing.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Catching a flawed plan at the `ExitPlanMode` gate, with structured annotations the agent acts on, prevents whole chains of misdirected implementation before any code is written |
| Speed | neutral | Saves the large cost of re-doing work built on a bad plan, but adds a synchronous human-review pause and a browser context switch on every plan/review — net depends on how often plans would otherwise go wrong |
| Maintainability | + | Forcing a readable, annotated, human-approved plan (optionally archived to Obsidian/Bear with metadata) leaves a clearer decision trail than an agent silently proceeding from an un-reviewed plan |
| Safety | + | A blocking human gate before implementation is itself a safety control; reinforced by SLSA provenance + SHA256 on binaries and client-side AES-256-GCM, server-ciphertext-only, disableable sharing |
| Cost Efficiency | + | Rejecting a bad plan for the price of one human review avoids many wasted agent turns of implementing the wrong thing — the cheapest place in the loop to spend a correction |

## Verdict

**CONDITIONAL**

Plannotator is a well-built, actively maintained, security-conscious tool that intervenes at the highest-leverage point in the dev loop: the Plan→Implement gate. Visual plan review is a genuine lever, not a nice-to-have — its blocking `ExitPlanMode` hook plus *structured* deny-feedback (annotations routed back to the agent, with a plan diff on resubmission) turns plan approval from a rubber-stamp into a real quality gate, and catching a bad plan there is the cheapest correction available anywhere in the loop. Maturity is strong (v0.20.3, dual-licensed, SLSA provenance, client-side-encrypted sharing, tests, nine agent integrations with a first-class Claude Code plugin).

It is CONDITIONAL rather than ADOPT because its value is structurally tied to a human being in the loop. Adopt it for interactive, human-supervised agent sessions — especially where plans are non-trivial, where a teammate should weigh in on a plan or diff before execution, or where an annotated decision trail has value. Skip it for autonomous/AFK or fleet workflows, where a multi-day blocking review hook on every plan is an anti-pattern, and weigh the browser context switch for terminal-native developers against Claude Code's lighter built-in plan-mode prompt. It complements `planning-with-files` (plan durability) rather than overlapping it: one persists the plan, the other gates and annotates it.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [plannotator](https://github.com/backnotprop/plannotator) | tool | Annotate and review coding agent plans and code diffs visually, share with team | Agent plans are hard to review and discuss with teammates | planning-with-files (complementary) |
