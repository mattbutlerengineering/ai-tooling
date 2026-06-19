# Evaluation: agnix

**Repo:** [agent-sh/agnix](https://github.com/agent-sh/agnix)
**Stars:** 293 | **Last updated:** 2026-06-19 (release v0.33.2, 2026-06-18) | **License:** MIT OR Apache-2.0
**Dev loop stage:** Verify (lints config artifacts) — also Ship (CI gate) and Implement (in-editor LSP)
**Layer:** Tooling

---

## What it does

A linter and language server for AI coding-assistant configuration files. The catalog one-liner ("validates CLAUDE.md, AGENTS.md, SKILL.md, hooks, MCP") undersells the current scope: as of v0.33.2 it ships **425 rules across 9+ tool families** — Claude Code (CC-*, 53), Agent Skills (AS-*/CC-SK-*, 31), Kiro (52), Cursor (16), AGENTS.md (13), MCP (12), Gemini CLI (9), GitHub Copilot (6), and Cline (4). It validates SKILL.md frontmatter, CLAUDE.md/AGENTS.md instruction files, hooks JSON, MCP server configs, agent definitions, and editor-specific rule formats.

The mechanism: a Rust workspace compiled into multiple delivery surfaces from one shared engine (`agnix-core`). The rule set lives as structured data in `knowledge-base/rules.json` (each rule has an id, name, severity HIGH/MEDIUM/LOW, category, and fixability), and `agnix-rules` is generated from it. That single engine is exposed as:

- `agnix-cli` — `npx agnix .` walks a directory and prints diagnostics in the Rust-compiler style (`file:line:col severity: message [fixable]` + a `help:` line).
- `agnix-lsp` — a real Language Server, so VS Code / JetBrains / Neovim / Zed extensions show diagnostics inline as you type.
- `agnix-mcp` — an MCP server so an agent can lint configs itself.
- `agnix-wasm` — powers a browser playground (paste a config, get diagnostics, no install).
- A GitHub Action (`agent-sh/agnix@v0`) for CI gating, with SARIF output for code scanning.

Auto-fix is tiered by confidence: `--fix-safe` (HIGH only), `--fix` (HIGH+MEDIUM), `--fix-unsafe` (all incl. LOW), plus `--dry-run --show-fixes` to preview diffs and `--strict` to treat warnings as errors. The framing motivation is that misconfigured agent files fail *silently* — e.g. a SKILL.md with the wrong `name` casing never triggers (the README cites Vercel's finding that skills invoke at ~0% without correct syntax).

## How we tested it

Source-grounded inspection — **not installed or run.** Examined the GitHub repo metadata, the full README, the recursive file tree, the release/tag history, the contributor graph, and parsed `knowledge-base/rules.json` directly to confirm the rule count (425), schema, and severity model. Verdict and signal claims below are grounded in the actual artifact (rule data, crate layout, CI workflows), not paraphrased marketing. Diagnostic output samples shown are the README's own examples, labeled as such — no lint results were fabricated.

```bash
gh api repos/agent-sh/agnix --jq '{stars,license,description,pushed_at,created_at,language}'
gh api repos/agent-sh/agnix/readme --jq '.content' | base64 -d
gh api "repos/agent-sh/agnix/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api repos/agent-sh/agnix/releases/latest --jq '{tag,published,name}'
gh api "repos/agent-sh/agnix/contributors?per_page=10" --jq '.[] | {login,contributions}'
# Parsed knowledge-base/rules.json -> 425 rules, schema {id,name,severity,category,fixable}
gh api "repos/agent-sh/agnix/contents/knowledge-base/rules.json" --jq '.content' | base64 -d
```

Example diagnostic output (from the project README, not run locally):

```
.claude/skills/review/SKILL.md:3:1 error: Invalid name 'Review-Code' [fixable]
  help: Use lowercase letters and hyphens only (e.g., 'code-review')
```

## What worked

- **Broad, structured rule coverage that maps to the real failure mode.** 425 rules in machine-readable form, severity-tagged and source-attributed (official specs, academic research, real breakage). The SKILL.md `name`-casing rule is exactly the silent failure the catalog entry names — a skill that never triggers because of a frontmatter typo, with no runtime error to surface it.
- **One engine, every surface.** CLI + LSP + MCP + GitHub Action + WASM playground all compile from `agnix-core`, so the same rule fires in-editor, in CI, and inside an agent. This is the right architecture for a linter and is unusually complete for a 293-star project.
- **Confidence-tiered auto-fix.** The HIGH / MEDIUM / LOW split (`--fix-safe` vs `--fix-unsafe`) with `--dry-run --show-fixes` is a mature design — it lets you trust safe fixes in CI while keeping risky rewrites opt-in. Most config linters offer no fixes at all.
- **Strong engineering hygiene for its age.** Rust workspace with fuzz targets, proptest regressions, criterion/iai benches, SARIF output, i18n locales (en/es/zh-CN), spec-drift and tool-release-watch CI workflows that detect when upstream tools change their config formats. Created 2026-01-30, already at v0.33.2 with frequent releases (v0.31/v0.32/v0.33 in sequence).
- **Genuinely complementary to its catalog overlaps.** It validates *correctness/syntax* of configs; the Security & Safety neighbors (SkillSpector, hol-guard, agentlint) scan for *malice/danger*. Different question entirely.

## What didn't work or surprised us

- **Single-author bus factor.** One maintainer (avifenesh) has 817 of the commits; the rest are Dependabot, Copilot, GitHub Actions, and a handful of one-commit external contributors. The dual MIT/Apache license and tidy contribution funnel mitigate lock-in risk, but continuity depends almost entirely on one person.
- **Catalog one-liner is stale.** The entry frames it as Claude/AGENTS/SKILL/hooks/MCP only. It now spans Cursor, Copilot, Kiro, Gemini, and Cline — the "multi-tool stack" pitch is the actual differentiator and isn't reflected.
- **Real overlap with two non-security catalog entries.** `reporails/cli` (AI-instructions diagnostics across Claude/Codex/Copilot/Cursor/Gemini) is the same job; agnix is the broader/more-mature take (more rules, real LSP, auto-fix, MCP, CI). `agentlint` (77 runtime guardrail rules) overlaps on the "rules engine" framing but acts at agent *runtime*, not on static config. The catalog currently lists agnix's overlap only as SkillSpector, which is the *least* overlapping of these.
- **Telemetry exists.** There's a `telemetry/` module in the CLI (with a `telemetry_stub.rs` opt-out path). Worth knowing for privacy-sensitive environments; not a blocker but should be verified/disabled in CI.
- **Value is bounded by how often you author configs.** For a stable single-tool repo, you write a SKILL.md once and rarely touch it — the recurring pain is real but modest. The payoff scales with multi-tool stacks and teams authoring many skills/agents.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Catches malformed configs (wrong SKILL.md name casing, invalid hooks/MCP JSON) that otherwise fail silently and make skills/agents never trigger |
| Speed | + | LSP surfaces config errors at author-time instead of after a failed agent run; auto-fix removes manual correction |
| Maintainability | + | Keeps agent configs spec-conformant across CLAUDE.md/SKILL.md/hooks/MCP and 9+ tools; spec-drift CI flags when upstream formats change |
| Safety | + (modest) | Catches misconfiguration, not malice — prevents broken/ignored configs; does not detect prompt injection or exfiltration (that's SkillSpector/hol-guard's job) |
| Cost Efficiency | + | A broken config that makes an agent silently ignore instructions wastes a whole run; cheap static validation avoids those wasted token loops |

## Verdict

**CONDITIONAL**

agnix is the most complete config linter in this catalog's space — 425 severity-tagged rules, a single Rust engine exposed as CLI + LSP + MCP + GitHub Action + browser playground, and confidence-tiered auto-fix, all actively maintained. Config-linting is a real recurring pain (silent skill/agent misfires), and agnix moves Maintainability and Correctness clearly, with a modest Safety lift. **Adopt it when you author agent configs regularly or run a multi-tool stack** (Claude Code + Cursor + Copilot + others) and want CI/editor enforcement; the `agnix-mcp` server lets an agent self-check its own configs. Hold off if you're a single-tool repo that touches its configs rarely — the payoff is thin and the single-author bus factor argues against a hard dependency. Not ADOPT-everywhere because the value is conditional on authoring volume and the one-maintainer risk; not SKIP because it cleanly fills a real gap. The catalog one-liner and overlap column should be refreshed to reflect multi-tool scope and the closer `reporails/cli` / `agentlint` overlaps.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agnix](https://github.com/agent-sh/agnix) | tool | Linter + LSP + MCP for AI coding configs — 425 rules across Claude Code, Cursor, Copilot, Kiro, Gemini, MCP, SKILL.md, hooks | Misconfigured agent files fail silently (skills don't trigger, hooks/MCP ignored) with no runtime error | reporails/cli (same job, agnix broader: LSP + auto-fix + CI); agentlint (rules engine but at runtime); SkillSpector (complementary: agnix = syntax validity, SkillSpector = malice) |
