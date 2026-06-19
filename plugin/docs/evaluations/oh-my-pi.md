# Evaluation: oh-my-pi (omp)

**Repo:** [can1357/oh-my-pi](https://github.com/can1357/oh-my-pi)
**Stars:** 13,501 (1,187 forks) | **Last updated:** 2026-06-19 | **License:** MIT
**Dev loop stage:** Plan + Implement + Verify + Review (a full inner-loop terminal agent — a *replacement* front-end, not a Claude Code add-on)
**Layer:** Tooling (an alternative agent harness / standalone CLI), with substantial Infrastructure (its own LSP/DAP/runtime/browser plumbing)

---

## What it does

Catalog one-liner: "Full coding agent with 32 tools, LSP/DAP integration, hash-anchored edits, 40+ providers." That is accurate and grounded — the README headline reads "**40+** providers · **32** built-in tools · **14** lsp ops · **28** dap ops · **~55k** lines of Rust core." Ground truth: **omp is a standalone, multi-provider terminal coding agent (the `omp` binary), a hard fork of [Mario Zechner's Pi](https://github.com/badlogic/pi-mono) by the author of the "[The Harness Problem](https://blog.can.ac/2026/02/12/the-harness-problem/)" post — not a Claude Code plugin, skill, or MCP.** You install it and run it *instead of* `claude`, not bolt it onto an existing Claude Code session. Anthropic is one of its 40+ supported model providers (with `oauth`), not the harness it extends.

The whole project is organized around one thesis from the author's blog post: the *harness* (the tool definitions and edit format the model is forced to use), not the model, is often what caps coding-agent performance. So omp re-engineers the agent's tool surface from the ground up. The README's own benchmark table claims large per-model lifts purely from changing the edit tool (Grok Code Fast 1 6.7% → 68.3% edit success; Grok 4 Fast −61% output tokens; MiniMax 2.1× pass rate) — these are the project's self-reported numbers, not independently reproduced here.

Mechanically, what you get is a Bun-runtime CLI with a ~55k-line Rust core and a deep, IDE-grade tool surface, all living in one flat namespace alongside `read`/`bash`:

- **Hashline edits** — the `edit` tool patches by content-hash anchors instead of retyping lines; stale anchors are detected and the patch is rejected before it can corrupt a file (the same idea oh-my-openagent credits *back* to oh-my-pi). Plus `ast_edit`/`ast_grep` over 50+ tree-sitter grammars for structural rewrites with a preview/accept step.
- **LSP wired into every write** (14 ops) — renames route through `workspace/willRenameFiles` so re-exports/barrels/aliases update; diagnostics, references, code actions, symbols.
- **A real debugger** (DAP, 28 ops) — attaches lldb/dlv/debugpy, sets breakpoints, steps, reads frames/variables.
- **In-process native tooling** — ripgrep, glob, find linked into the process (no fork-exec, runs on Windows without WSL); `brush` as an in-process bash with persistent sessions.
- **Code execution with tool re-entry** — persistent Python + Bun kernels that can call back into the agent's own tools over a loopback bridge.
- **Subagents** (`task`) in isolated git worktrees returning schema-validated objects; an **advisor** second model watching every turn; **time-traveling stream rules** that abort mid-token on a regex match, inject a rule, and retry from the same point (survives compaction).
- **FS-as-everything URI schemes** — `pr://`, `issue://`, `agent://`, `skill://`, `conflict://`, etc. resolve inside every FS-shaped tool, so `read pr://1428` returns the same shape as `read src/foo.ts`, and merge conflicts resolve by writing `@theirs`/`@ours` to `conflict://N`.
- **Memory** ("Hindsight" — `retain`/`recall`/`reflect`, project-scoped), **collab** relay sharing with QR links, **browser/Electron** automation (drives Slack), `web_search` across 14 providers feeding `read`, **ACP** so it runs inside Zed.
- **Config interop** — reads eight existing rule formats in their native shape (Cursor MDC, Cline `.clinerules`, Codex `AGENTS.md`, Copilot `applyTo`, etc.) without a migration step.

Note the same naming/relationship trap as the rest of the harness cluster: omp *consumes* other agents' config formats (including `AGENTS.md` and `.claude-plugin` examples in its skills docs) — but that means it behaves like / ingests-the-config-of those tools, not that it plugs *into* Claude Code.

## How we tested it

**Method: inspected the repo, README, full recursive file tree, license, and maturity signals via the GitHub API and the npm registry API. Did NOT install or run it.** This is a deliberate non-install evaluation. omp is an *alternative harness* — installing it (`curl -fsSL https://omp.sh/install | sh`, Homebrew, or `bun install -g @oh-my-pi/pi-coding-agent`) gives you a separate coding agent that *replaces* the front-end of this catalog's standardized Claude Code dev loop rather than extending it. Running it would not exercise the harness (Claude Code) this catalog standardizes on, and it wants its own provider/API-key config across 40+ providers. So the verdict rests on the repo, the documented mechanics, the license, and the maturity signals below. No metrics are invented; star/fork/release/contributor/commit counts are from live API calls, the npm download number is from the npm registry API, and every benchmark figure (Grok edit-success, token deltas, MiniMax pass rate) is quoted explicitly as the *project's own self-reported* claim.

```bash
gh api repos/can1357/oh-my-pi --jq '{stars:.stargazers_count,forks:.forks_count,license:.license.spdx_id,description,created_at,pushed_at,language}'
# 13,501 stars; 1,187 forks; MIT; TypeScript (+~55k-line Rust core); created 2025-12-31; pushed 2026-06-19
gh api repos/can1357/oh-my-pi/readme --jq '.content' | base64 -d            # full README
gh api "repos/can1357/oh-my-pi/git/trees/HEAD?recursive=1" --jq '.tree[].path'   # packages/{ai,coding-agent,...}, AGENTS.md, docs/
gh api repos/can1357/oh-my-pi/releases/latest --jq '{tag,published_at}'      # v16.1.3, 2026-06-19
gh api repos/can1357/oh-my-pi/releases --paginate --jq '.[].tag_name' | wc -l   # 466
gh api repos/can1357/oh-my-pi/contributors --paginate --jq '.[].login' | wc -l  # 240
gh api repos/can1357/oh-my-pi/commits --paginate --jq '.[].sha' | wc -l         # 9,920
curl -s https://api.npmjs.org/downloads/point/last-month/@oh-my-pi/pi-coding-agent  # 134,282/mo
# Confirmed Anthropic appears only under packages/ai/src/providers/ (one of 40+ providers), not as a host harness.
```

Reviewed: README (English, very detailed — 20 numbered feature sections + a full 32-tool reference + the provider matrix), the recursive file tree (`packages/ai/src/providers/*` showing Anthropic as one provider among many, `AGENTS.md`, `docs/`, `docs/skills/`), the benchmark table, and the maturity signals above.

## What worked

- **Genuinely best-in-class harness engineering — the technical differentiators are real and specific.** Hashline content-hash edits (reject stale patches before corruption), LSP-aware renames through `workspace/willRenameFiles`, a real DAP debugger driving lldb/dlv/debugpy, in-process ripgrep/glob/find (no fork-exec, native Windows), code-execution kernels that re-enter the agent's tools, FS-as-everything URI schemes (`pr://`, `conflict://`, `agent://`), and time-traveling stream rules are each a concrete, well-motivated attack on a real coding-agent failure mode. This is the project that *originated* the Hashline idea that oh-my-openagent later borrowed. The "harness, not model" thesis is coherent and the tool surface is the most complete in the catalog's standalone-agent cluster.
- **High and fast-rising maturity for an alternative agent.** 13.5k stars, 466 tagged releases, ~9,900 commits, 240 contributors, and **~134k npm downloads/month** in under six months (created 2025-12-31). That puts adoption in the same order of magnitude as oh-my-claudecode and well above claurst (~626/mo) — real production usage, active CI, daily releases (v16.1.3 shipped the same day as this eval).
- **MIT license** — the permissive norm for this catalog, and notably more permissive than oh-my-openagent (SUL-1.0, non-commercial) or claurst (GPL-3.0). No commercial-redistribution friction.
- **Provider-agnostic and anti-lock-in.** 40+ providers, hundreds of models, role-based routing (`default`/`smol`/`slow`/`plan`/`commit`) so cheap models do cheap fan-out — directly aligned with Cost Efficiency for users not on a single Claude subscription. Anthropic is a first-class `oauth` provider but just one of many.
- **Honest provenance and config interop.** Clearly credits the upstream Pi fork and the author's own blog thesis; ingests eight existing rule formats natively instead of forcing a migration.

## What didn't work or surprised us

- **It is NOT a Claude Code tool — this is the central caveat and the basis for the verdict.** omp is a standalone agent you run *instead of* Claude Code. There is no plugin, skill, or MCP to adopt into an existing Claude Code session. For a catalog standardized on the Claude Code dev loop, adopting omp means *switching harnesses* (and switching the agent's runtime, config, provider setup, and tool surface), which is a large commitment, not an enhancement. This is the same disqualifier that placed oh-my-openagent and claurst at SKIP. "Reads Codex `AGENTS.md` / has `.claude-plugin` examples" means it *consumes* those formats, not that you install omp into Claude Code.
- **Self-reported benchmarks, marketing-forward framing.** The headline lifts (Grok 6.7%→68.3%, −61% tokens, MiniMax 2.1×) are the project's own numbers from its own harness post — plausible and well-argued, but not independently reproduced here. The README is heavy on "benchmaxxed / the most capable agent surface that ships" superlatives.
- **Enormous surface area + heavy install.** 32 tools, 14 LSP ops, 28 DAP ops, browser/Electron automation, collab relay, Hindsight memory, code-execution kernels, ACP, ~55k-line Rust core. Powerful, but a large attack/maintenance surface and a steep learning curve relative to an in-loop skill or plugin. Several tools are setting-gated off by default (`github`, `tts`, `retain`/`recall`/`reflect`, etc.) precisely because the surface is so wide.
- **Very fast churn.** 466 releases and ~9,900 commits in ~6 months (already at v16.x), with same-day releases — expect a high breaking-change cadence and single-creator-vision concentration risk if you build on it.
- **Footgun-adjacent capabilities.** Default-on browser stealth, Electron in-place automation that "reads your Slack DMs," `ssh`, and a collab relay are genuinely useful but raise the safety review bar well above a read/edit/bash agent.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + (potential) | Hashline rejects stale edits before corruption; LSP-aware renames; AST edits with preview; advisor second-model review; `/review` P0–P3 verdicts — but the headline edit-success lifts are self-reported, not reproduced here |
| Speed | + (potential) | In-process ripgrep/glob/find/bash (no fork-exec), instant search, parallel worktree subagents — but unverified here, and small tasks gain nothing from switching harness |
| Maintainability | - (for *this* loop) | Adopting it replaces the Claude Code front-end rather than integrating into the loop; you maintain a separate agent runtime, config, and 40-provider setup; very fast release churn |
| Safety | +/- | MIT, setting-gated tools off by default, ACP per-tool permission prompts, client-sealed collab frames are positives; offset by `curl \| bash` install, default-on browser stealth, Electron/Slack automation, `ssh`, and a large tool surface |
| Cost Efficiency | + | Role-based model routing (`smol`/`slow`), 40+ providers including cheap open models, Hashline token savings (claimed −61% on Grok 4 Fast), summarized reads — squarely aimed at token spend for users off a single premium provider |

## Verdict

**SKIP** (for *this* catalog's Claude Code dev loop) — the most technically impressive standalone agent in the catalog, wrong category; steal the ideas, and re-evaluate only if the user's stack moves off Claude Code.

omp is a legitimately excellent piece of harness engineering — Hashline content-hash edits, LSP/DAP integration, in-process native tooling, FS-as-everything URI schemes, code-execution kernels, and time-traveling stream rules are each a real, well-motivated contribution, and it is the project that *originated* the Hashline idea others have since borrowed. It is also mature (13.5k stars, ~134k npm downloads/month, 240 contributors, MIT-licensed). But for a catalog standardized on the Claude Code harness, it is a SKIP as an *installable artifact*: it is an **alternative agent you run instead of Claude Code** (a hard fork of Pi, with Anthropic as just one of 40+ providers), not a plugin/skill/MCP that extends the existing dev loop. Adopting it means switching front-ends — the same disqualifier that placed oh-my-openagent and claurst at SKIP. The SKIP is on category fit, not quality: on engineering and adoption it is the *strongest* member of the standalone-agent cluster, and its MIT license is friendlier than either SKIP precedent.

**Differentiation from the harness cluster:**
- vs. **oh-my-openagent** (SKIP): the relationship is direct — OmO credits *oh-my-pi* for the Hashline edit idea, and oh-my-openagent's ROADMAP even lists "Pi" as a target harness. Both are front-ends you switch *to*. OmO runs on OpenCode/Codex and its transferable value is harness ideas; omp *is* the source of several of those ideas and ships them in one MIT binary. Where they overlap, omp has the more complete native tool surface (real DAP debugger, in-process ripgrep) and the more permissive license.
- vs. **claurst** (SKIP): same category (standalone Claude Code alternative), but omp is far more mature (~134k vs ~626 npm downloads/mo) and out of beta (v16.x vs v0.1.5). claurst's angle is Rust clean-room provenance; omp's is the deepest re-engineered tool surface.
- vs. **opencode / qwen-code / goose** (the standalone-alternative-agent cluster): omp is the same *kind* of thing, distinguished by its IDE-grade plumbing (LSP+DAP+in-process native tools) and the explicit "harness is the bottleneck" design thesis.
- vs. **oh-my-claudecode** (CONDITIONAL): sharp contrast — oh-my-claudecode is a *real Claude Code plugin* you install via the marketplace and that lives inside the loop; omp replaces the loop. If you must pick one for a Claude Code stack, oh-my-claudecode is the integrated choice; omp is not in that comparison.

Re-evaluate to CONDITIONAL/ADOPT if the user's stack moves off Claude Code (omp would then compete strongly on its own terms against opencode/qwen-code/claurst — its LSP/DAP/Hashline/native-tooling surface and MIT license are genuine pluses, and Anthropic models run natively via `oauth`).

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [oh-my-pi](https://github.com/can1357/oh-my-pi) | platform | Standalone multi-provider terminal coding agent (Pi fork) — 32 tools, LSP/DAP, hash-anchored edits, 40+ providers; not a Claude Code plugin | Want the deepest re-engineered agent tool surface (IDE-grade LSP/DAP, Hashline edits, native in-process tooling) as a provider-agnostic alternative to Claude Code | oh-my-openagent, claurst, opencode, qwen-code, goose |
