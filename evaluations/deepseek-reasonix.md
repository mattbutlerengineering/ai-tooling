# Evaluation: DeepSeek-Reasonix

**Repo:** [esengine/DeepSeek-Reasonix](https://github.com/esengine/DeepSeek-Reasonix)
**Stars:** 23,214 | **Last updated:** 2026-06-19 (pushed; created 2026-04-21) | **License:** MIT
**Dev loop stage:** Implement (inner loop) — a terminal coding agent you point at a repo (`reasonix run "implement the TODOs in main.go"`), with the same agentic surface as Claude Code / opencode: tools, plugins (MCP), slash commands, `@` references, permissions/sandbox, checkpoints. Touches Plan and Verify only insofar as the agent plans-then-edits-then-tests inside one session.
**Layer:** Infrastructure (a single static Go binary harness that drives an LLM over your codebase) + Tooling (config-driven provider/tool/plugin registry)

---

## What it does

The catalog one-liner: "DeepSeek-native terminal coding agent optimized for prefix-cache stability." Reasonix is a **CLI coding agent** in the opencode / qwen-code / goose family — distinct from the visual no-code platforms elsewhere in this category. As of the inspected `main-v2` branch it is a **ground-up Go rewrite (1.0)**; the earlier `0.x` TypeScript releases are legacy on the `v1` branch. Install is `npm i -g reasonix` (pulls a prebuilt native binary) or `brew install esengine/reasonix/reasonix`; there is also a desktop app and IM-bot bridges (Feishu / Lark / WeChat).

The pitch is narrow and concrete: a harness **tuned around DeepSeek's prefix cache** so token cost stays low across long sessions. Everything is config-driven via `reasonix.toml` — providers, the active agent, enabled tools, and plugins are declarations, not code. DeepSeek (flash/pro) and MiMo ship as presets; any OpenAI-compatible endpoint is a config entry. It supports a **two-model setup** (separate executor + planner sessions, each kept cache-stable), MCP-compatible plugins over stdio JSON-RPC, `/init` to generate an `AGENTS.md` project-memory file, and snapshot-based **checkpoints / rewind** (Esc-Esc) as an edit safety net. The repo tree shows a serious Go codebase (`cmd/reasonix`, `desktop/` with extensive `_test.go` coverage, `cmd/e2ebench` mutation/diff benchmarks, `benchmarks/context-maintenance-e2e`), GoReleaser cross-compile to six targets, SignPath-signed Windows builds, and a `.reasonix/commands/review.md` slash command.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No binary was installed, no `reasonix.toml` was written, no `reasonix run` was executed against a repo, and no DeepSeek API key was used. Every claim below comes from the repository (GitHub metadata, README, recursive file tree, CHANGELOG, commit/release/contributor counts) — not from observed agent behavior. The "low token cost / cache-stable" framing is the authors' design claim; we did not measure tokens, latency, or edit quality. The oosmetrics "Top 2 in Agents by velocity" badges in the README are third-party velocity rankings, not correctness benchmarks.

```bash
gh api repos/esengine/DeepSeek-Reasonix --jq '{desc,stars:.stargazers_count,forks:.forks_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id,lang:.language}'  # Go, MIT, 23.2K stars, created 2026-04-21
gh api repos/esengine/DeepSeek-Reasonix/readme --jq '.content' | base64 -d | head -230
gh api "repos/esengine/DeepSeek-Reasonix/git/trees/HEAD?recursive=1" --jq '.tree[].path'  # cmd/, desktop/ (+ _test.go), cmd/e2ebench, benchmarks/
gh api repos/esengine/DeepSeek-Reasonix/commits   --jq 'length'   # 30 (page-1 cap)
gh api repos/esengine/DeepSeek-Reasonix/releases  --jq 'length'   # 30 (page-1 cap; active release cadence to v1.8.1+)
gh api repos/esengine/DeepSeek-Reasonix/contributors --jq 'length'  # 30 (page-1 cap)
```

## What worked

- **Sharp, defensible thesis.** Rather than "another coding agent," it picks one provider and engineers around its economics — DeepSeek's prefix cache — keeping the executor/planner sessions cache-stable. For DeepSeek-on-budget users this is a real, specific reason to choose it over a generic harness.
- **Clean distribution and operational hygiene.** `CGO_ENABLED=0` static Go binary with one TOML-parser dependency, GoReleaser cross-compile to six targets, prebuilt archives + `SHA256SUMS` on every release, and SignPath-signed Windows builds. This is more supply-chain discipline than most coding-agent repos.
- **Config-driven, not code-driven.** Providers, agent, tools, and plugins all live in `reasonix.toml` with a clear resolution order (flag > project > user > defaults); secrets come from env/OS credential store and are never written to config. Easy to reason about and to swap models without forking.
- **MCP-compatible and feature-complete for the inner loop.** Plugins run as stdio JSON-RPC subprocesses; it has permissions/sandbox, slash commands, `@` references, `AGENTS.md` memory, and checkpoint/rewind — the table stakes a serious coding agent needs.
- **Real test and benchmark code.** The tree includes substantial `desktop/*_test.go` coverage and a `cmd/e2ebench` harness with diff/mutation logic plus a context-maintenance e2e benchmark — the maintainers measure their own agent, not just ship it.

## What didn't work or surprised us

- **DeepSeek-native is the whole bet — and the whole risk.** The optimization that differentiates it (prefix-cache stability) only pays off on DeepSeek/MiMo. Point it at Claude or GPT via the OpenAI-compatible path and you get a generic agent with none of the cache advantage — at which point opencode/goose are more mature.
- **Very young, fast-moving.** Created 2026-04-21; the current default is a `main-v2` Go rewrite that obsoletes the `0.x` TS line. Config paths already moved (`~/.reasonix/config.toml` as of v1.8.1, with a migration doc). High churn means breaking changes are likely.
- **Unverified efficiency claims.** "token costs stay low across long sessions" is the headline selling point and we measured none of it. The e2ebench harness exists in-repo but we did not run it; the oosmetrics badges rank velocity, not output quality.
- **Single-maintainer center of gravity.** Despite a contributor graph and bilingual Discord, the donation links (PayPal / WeChat) and acknowledgments point to one primary author. Bus-factor and longevity are open questions for a 2-month-old project.
- **Mostly relevant only if you're already a DeepSeek shop.** For a Claude Code user, this is a sidegrade at best; its reason to exist is cost on a specific provider, not a capability the incumbent lacks.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Standard plan-edit-test agent loop with checkpoints/rewind as a safety net; no benchmark we ran substantiates better-than-peers edit quality. Correctness ultimately rides on the chosen DeepSeek model. |
| Speed | + | Static Go binary (fast startup, no Node runtime); prefix-cache-stable sessions and two-model executor/planner split are designed to keep long sessions responsive — claimed, not measured. |
| Maintainability | neutral | Affects how you *drive* the codebase, not the codebase itself. `AGENTS.md` memory and config-as-declaration help reproducibility; project's own churn is a maintenance caveat for adopters. |
| Safety | + / neutral | Permissions + sandbox, secrets kept out of config files (env / OS credential store), signed Windows builds, SHA256SUMS. Plugins run as subprocesses (MCP) — standard agent attack surface applies. |
| Cost Efficiency | + | The entire design goal: exploit DeepSeek's prefix cache to cut token spend over long sessions, plus DeepSeek's already-low per-token price. Strongest signal — but unverified by us and DeepSeek-specific. |

## Verdict

**CONDITIONAL — adopt only if DeepSeek (or MiMo) is your primary coding model; otherwise DEFER.** Reasonix is a genuinely well-engineered terminal coding agent: static Go binary, signed releases, MCP plugins, checkpoints, two-model setup, and a clear, honest thesis (cost-optimize around one provider's prefix cache). That thesis is also its boundary — the differentiating optimization only pays off on DeepSeek/MiMo, the project is 2 months old with a just-completed Go rewrite and active config-path migrations, and the headline cost claims are unmeasured. For a DeepSeek-on-a-budget shop running long sessions it is a strong, specific pick worth piloting; for a Claude Code / GPT user it's a generic agent without its raison d'être.

Compared to neighbors: **opencode** and **goose** are more mature, model-agnostic platforms — better defaults if you're not married to DeepSeek. **qwen-code** is the closest analog (a vendor-native CLI agent built around one model family); Reasonix differs by optimizing for *cache economics* rather than model capability. Against all three, Reasonix wins only on the narrow axis of DeepSeek token efficiency and Go-binary distribution; it does not yet have the track record or breadth to displace them as a default.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [DeepSeek-Reasonix](https://github.com/esengine/DeepSeek-Reasonix) | platform | DeepSeek-native terminal coding agent (Go binary, MCP plugins, checkpoints) tuned around DeepSeek's prefix cache to keep long-session token cost low | Want a long-running, cost-optimized coding agent for DeepSeek/MiMo without paying Claude/GPT token prices | opencode, qwen-code, goose |
