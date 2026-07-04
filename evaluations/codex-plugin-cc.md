# Evaluation: codex-plugin-cc

**Repo:** [openai/codex-plugin-cc](https://github.com/openai/codex-plugin-cc)
**Stars:** 21,295 | **Last updated:** 2026-06-14 | **License:** Apache-2.0
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Review (primary) — also Implement via `/codex:rescue` delegation
**Layer:** Tooling

---

## What it does

Catalog one-liner: "Use OpenAI Codex from Claude Code to review code or get a cross-model second opinion." This is the **official OpenAI** plugin (author field literally `"name": "OpenAI"`, Apache-2.0, NOTICE file) that lets Claude Code invoke Codex as a reviewer or task delegate without leaving the Claude Code session.

Mechanically it is a native Claude Code plugin installed from OpenAI's own marketplace (`/plugin marketplace add openai/codex-plugin-cc` → `/plugin install codex@openai-codex` → `/reload-plugins` → `/codex:setup`). It ships 7 slash commands, 1 subagent (`codex:codex-rescue`), 3 skills (`codex-cli-runtime`, `codex-result-handling`, `gpt-5-4-prompting`), and lifecycle hooks. The differentiated surface is small and focused:

- **`/codex:review`** — a normal read-only Codex review of uncommitted changes or a branch diff (`--base <ref>`), with `--wait`/`--background` execution modes. "Same quality of code review as running `/review` inside Codex directly." Returns Codex output verbatim; the command is hard-constrained to review-only ("Do not fix issues, apply patches").
- **`/codex:adversarial-review`** — a *steerable* challenge review that pressure-tests design decisions, tradeoffs, hidden assumptions, and risk areas (auth, data loss, rollback, race conditions). Takes free-text focus after the flags. Also read-only.
- **`/codex:rescue`** — delegates an actual task (investigate/fix/continue) to Codex through the `codex-rescue` subagent, with `--model`, `--effort`, `--resume`, `--fresh`, `--background`. This is the only write-capable path.
- **`/codex:status` / `/codex:result` / `/codex:cancel`** — manage background Codex jobs; `/codex:result` surfaces the Codex session ID so you can `codex resume <id>` and continue the work inside Codex natively.
- **`/codex:setup`** — checks Codex install/auth, can install Codex via npm, and toggles an optional **review gate** (`--enable-review-gate`).

The integration is genuinely thin, which is the key architectural fact: the plugin **wraps the local Codex CLI / Codex app server** on the same machine (`scripts/app-server-broker.mjs`, `scripts/lib/app-server.mjs`). It uses the same `codex` binary, the same local auth state, the same repo checkout, and the same `~/.codex/config.toml` / `.codex/config.toml` config the user already has. It does not bundle its own model runtime or keys — it brokers to Codex. The optional review gate is a `Stop` hook (`stop-review-gate-hook.mjs`, 900s timeout) that runs a targeted Codex review on Claude's response and *blocks the stop* if Codex finds issues, forcing Claude to address them before finishing — with an explicit WARNING that it can create a long-running Claude/Codex loop and "drain usage limits quickly."

## How we tested it

**Evidence:** REVIEW

Inspected the repo, README, plugin manifest, hooks, and the `/codex:review` command file via the GitHub API — **did not install or run it**. No Codex jobs were dispatched and no review output was produced; exercising the differentiated path requires a logged-in local Codex CLI (ChatGPT subscription or OpenAI API key) and would consume Codex usage limits. The verdict rests on the manifest, the command/hook contracts, the wrapper architecture, the maintenance signals, and OpenAI-official authorship — none of the findings below are invented metrics.

```bash
gh api repos/openai/codex-plugin-cc --jq '{stars:.stargazers_count,license:.license.spdx_id,description:.description,pushed_at,created_at}'
gh api repos/openai/codex-plugin-cc/readme --jq '.content' | base64 -d
gh api "repos/openai/codex-plugin-cc/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api repos/openai/codex-plugin-cc/contents/plugins/codex/.claude-plugin/plugin.json --jq '.content' | base64 -d
gh api repos/openai/codex-plugin-cc/contents/plugins/codex/hooks/hooks.json --jq '.content' | base64 -d
gh api repos/openai/codex-plugin-cc/contents/plugins/codex/commands/review.md --jq '.content' | base64 -d
gh api repos/openai/codex-plugin-cc/releases --paginate --jq '.[].tag_name'   # v1.0.0 .. v1.0.4
gh api repos/openai/codex-plugin-cc/contributors --paginate --jq '.[].login' | wc -l   # 11
```

## What worked

- **Official OpenAI authorship is the headline differentiator.** Among catalog tools that wire Codex into Claude Code, this is the first-party one — author `OpenAI`, Apache-2.0, NOTICE file, OpenAI's own marketplace namespace (`openai-codex`). That means it tracks the Codex CLI / app-server contract directly and is far less exposed to the CLI-version-churn risk that single-author cross-vendor tools (e.g. architect-loop) explicitly warn about.
- **Thin wrapper over the local Codex install — no second runtime, no separate account.** It reuses the user's existing `codex` binary, local auth, repo checkout, and `config.toml`. If you already use Codex, it works immediately; there is no new credential surface and config behavior is predictable. This is a much smaller blast radius than heavy multi-model orchestration plugins.
- **Tight, legible scope.** 7 commands, 1 subagent, 3 skills. Compared with claude-octopus (49 commands / 32 personas / 54 skills) or architect-loop's full build loop, this does one thing — Codex as reviewer/delegate from inside Claude Code — and the command files enforce it (review commands are hard-constrained read-only, return Codex output verbatim, forbidden from applying fixes).
- **Two genuinely distinct review modes.** `/codex:review` mirrors Codex's native `/review`; `/codex:adversarial-review` is steerable and explicitly targets design assumptions, tradeoffs, and named risk areas. That adversarial mode is the real cross-model value: a second vendor's model challenging Claude's own direction, not just lint-level nits.
- **Background job machinery is first-class.** `--background`/`--wait`, `/codex:status`, `/codex:result`, `/codex:cancel`, plus session-resume via the surfaced Codex session ID. The `review.md` command even estimates diff size and recommends background for anything non-trivial. Mature ergonomics for long-running reviews.
- **Real test suite and CI.** `tests/` covers broker endpoint, commands, git, process, render, runtime, and state; there is a `pull-request-ci.yml` workflow. The wrapper code (`scripts/lib/*.mjs`) is modular and tested — engineering quality is high.
- **The risky feature is opt-in and honestly labeled.** The Stop-hook review gate is off by default, toggled explicitly, and carries a clear WARNING about looping and usage drain. Good restraint for a foot-gun feature.

## What didn't work or surprised us

- **The value still requires a second vendor's usage budget.** Reviews and rescue tasks consume Codex usage limits (ChatGPT subscription incl. Free tier, or OpenAI API key). The Free tier lowers the barrier versus architect-loop's hard ChatGPT-plan dependency, but meaningful multi-file reviews and `/codex:rescue` runs will eat into Codex limits — this is still a cross-vendor cost, not free.
- **No published evidence that a Codex second opinion catches what Claude's own review misses.** The cross-model premise is plausible and the adversarial mode is well-designed, but there is no benchmark in-repo showing Codex review beats Claude-native `/review` or `/security-review`. The payoff is asserted by construction (different vendor, different blindspots), not measured.
- **Very young.** Created 2026-03-30, releases only v1.0.0 → v1.0.4, 26 commits, 11 contributors. The 21K stars reflect the OpenAI brand and the Claude-Code-plus-Codex zeitgeist more than a long track record. It is first-party and tested, but it has not weathered much version churn yet.
- **The review gate is a real loop hazard.** A Stop hook that re-runs Codex on every Claude response and blocks completion on findings can burn both Claude and Codex budgets fast and stall sessions. The docs are honest about it, but it is the kind of feature that bites unattended/CI usage. Leave it off unless actively monitoring.
- **Requires Codex already set up on the machine.** Node 18.18+, `npm install -g @openai/codex`, `codex login`. `/codex:setup` smooths this, but a Claude-Code-only user with no Codex footprint has real first-run setup before any value appears.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + (potential) | Independent second-vendor review (`/codex:review`) plus a steerable adversarial mode that challenges design, tradeoffs, and named risk areas (auth, data loss, race conditions) targets blindspots a single model's self-review can miss; unproven by benchmark but mechanically sound and read-only |
| Speed | +/- | Background jobs + status/result/cancel let reviews run async without blocking the session; large multi-file reviews are slow and the README itself steers you to `--background` |
| Maintainability | + | Verbatim, non-fixing review output keeps the human in the loop; first-party wrapper tracks the Codex contract directly; modular tested scripts and CI |
| Safety | +/- | Review commands are hard-constrained read-only; no new credential surface (reuses local Codex auth); offset by routing code/diffs to a second external vendor (data egress) and the opt-in Stop-gate loop hazard |
| Cost Efficiency | - | Consumes Codex usage limits on top of Claude usage; mitigated by the ChatGPT Free tier and by being a single second model (not a 5–9-model fan-out), but the review gate can drain limits quickly if enabled |

## Verdict

**CONDITIONAL**

Adopt when you (1) already have Codex set up on the machine (ChatGPT subscription, incl. Free tier, or an OpenAI API key) and (2) want a genuine cross-model second opinion — especially the adversarial design review — before shipping high-stakes changes, all without leaving Claude Code. For that profile this is the cleanest option in its niche: it is **OpenAI-official**, a thin well-tested wrapper over your existing local Codex install (no second runtime, no extra account, predictable config), and narrowly scoped to review/delegation with read-only review commands and good background-job ergonomics. The first-party authorship materially de-risks the CLI-churn problem that plagues third-party cross-vendor tools.

It is not an unconditional ADOPT because the cross-model payoff is asserted rather than benchmarked, it still spends a second vendor's usage budget, it is young (v1.0.x, ~3 months old), and the opt-in Stop-gate review loop is a real cost/latency foot-gun. Claude-Code-only users with no Codex footprint, or anyone doing small inline changes, get little marginal value over Claude-native `/review`.

Differentiation from overlaps: **claude-octopus** is a heavy multi-vendor *consensus* engine (up to 9 models, 75% gate, 49 commands) — maximal blindspot coverage at maximal cost and footprint; codex-plugin-cc is the focused, first-party *one second opinion* (Codex only) with a tiny surface. **architect-loop** is a cross-vendor *build loop* (Claude Fable architect / GPT-5.5 Codex builder) for PR-sized parallel construction; codex-plugin-cc is not a build loop — it is review-first with optional single-task delegation (`/codex:rescue`). A focused Codex-from-CC reviewer is additive precisely because it is the low-ceremony, official, single-second-opinion point on a spectrum whose other end (octopus) is heavyweight consensus and whose adjacent neighbor (architect-loop) is a full build loop.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [codex-plugin-cc](https://github.com/openai/codex-plugin-cc) | plugin | Official OpenAI plugin to run Codex code review and task delegation from inside Claude Code (21K stars) | Single-model self-review misses blindspots; want a first-party cross-model second opinion without leaving Claude Code | claude-octopus, architect-loop |
