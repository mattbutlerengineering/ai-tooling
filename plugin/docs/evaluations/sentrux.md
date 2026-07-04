# Evaluation: sentrux

**Repo:** [sentrux/sentrux](https://github.com/sentrux/sentrux)
**Stars:** 2,480 | **Last updated:** 2026-03-19 (release v0.5.7, 2026-03-18) | **License:** MIT (free core); Pro tier is BSL/commercial
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Verify (structural quality gate) — also Review (architecture inspection) and Reflect (cross-session degradation tracking)
**Layer:** Tooling

---

## What it does

The catalog one-liner — "Real-time architectural sensor enabling recursive self-improvement of code quality" — is marketing-flavored but maps onto a real mechanism. sentrux is a single Rust binary that statically analyzes a codebase's dependency/call graph and emits **one continuous quality score (0–10000)** plus a live interactive treemap. It is built to sit in an AI-agent feedback loop: scan before a session, let the agent write code, rescan after, and detect architectural degradation the agent (and the human) would otherwise never see from the terminal stream of `Modified src/foo.rs` lines.

The score is computed from **5 "root cause" structural metrics**, each grounded in a real algorithm (verified in `sentrux-core/src/metrics/` and `docs/quality-signal-design.md`):

1. **Modularity** — Newman's Q (community detection) on the import+call graph. Adding fake edges moves the graph toward random and *lowers* Q, so it resists the obvious gaming.
2. **Acyclicity** — Tarjan's SCC count of circular dependencies, sigmoid-normalized.
3. **Depth** — longest dependency chain (Lakos levelization), sigmoid-normalized.
4. **Equality** — Gini coefficient of per-function cyclomatic complexity (detects god functions/files).
5. **Redundancy** — `(dead + duplicate functions) / total` (Kolmogorov-complexity framing).

The design doc explicitly argues *against* letter grades (gameable boundaries) and *against* 20 proxy metrics (measure symptoms, gameable individually) in favor of these 5 "ungameable" root-cause properties — a more thoughtful rationale than most quality tools ship with. Language parsing is delegated to **tree-sitter plugins (52 languages)** declared as `plugin.toml` + `tags.scm`; the binary carries zero per-language Rust code.

Surfaces:
- **GUI** (`sentrux`) — live wgpu treemap with dependency edges; files glow as the agent edits them.
- **CLI** — `sentrux check .` (rules pass/fail, CI exit code), `sentrux gate --save .` / `sentrux gate .` (baseline-vs-after degradation gate).
- **MCP server** (`sentrux --mcp`) — exposes ~9–15 tools (`scan`, `health`, `session_start`, `session_end`, `rescan`, `check_rules`, `evolution`, `dsm`, `test_gaps`, `blast_radius`, `level`, …) so the agent itself can read its structural impact mid-session.
- **Claude Code plugin** — `/plugin marketplace add sentrux/sentrux` ships a `scan` skill wired to the MCP tools.
- **Rules engine** — `.sentrux/rules.toml` declares layers, allowed boundaries, `max_cycles`, `max_cc`, `no_god_files`, coupling grade caps; enforced in CI.

**On "recursive self-improvement":** verified against the actual code, this is *not* the tool autonomously improving itself. It is the cybernetic loop the design doc names directly (Wiener 1948): sensor (sentrux) → signal → controller (the AI agent/human) → actuator (code edits) → system (codebase) → sensor. The "recursion" is the agent iterating against the score across sessions. The `evolution` MCP tool is git-history analysis (churn, bus factor, coupling history) — a Reflect-stage diagnostic, not self-modification. The substance is real; the phrase oversells it.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed or run.** sentrux is a GUI-first desktop binary (wgpu/eframe) distributed via Homebrew/curl/release artifacts; this evaluation did not install it or execute a scan, so no scores, treemaps, or gate results are reported as observed. Claims below are grounded in the actual repository artifacts, not paraphrased marketing. I examined repo metadata, the full English README, the recursive file tree (121 `.rs` files, 24 test files), the release history (29 releases v0.3.0→v0.5.7 over ~7 days in March 2026), the contributor list, the quality-signal design doc, the MCP handler source, the license/tier source, and the Pro-architecture doc.

```bash
gh api repos/sentrux/sentrux --jq '{stars,license,description,pushed_at,created_at,forks,open_issues}'
gh api repos/sentrux/sentrux/readme --jq '.content' | base64 -d
gh api "repos/sentrux/sentrux/git/trees/HEAD?recursive=1" --jq '.tree[].path'   # 121 .rs, 24 test files
gh api repos/sentrux/sentrux/contents/docs/quality-signal-design.md --jq '.content' | base64 -d   # 5 metrics + formulas
gh api repos/sentrux/sentrux/contents/sentrux-core/src/app/mcp_server/handlers_evo.rs --jq '.content' | base64 -d
gh api repos/sentrux/sentrux/contents/sentrux-core/src/license.rs --jq '.content' | base64 -d   # Free/Pro/Team tiers
gh api repos/sentrux/sentrux/contents/docs/pro-architecture.md --jq '.content' | base64 -d   # $15/mo Pro dylib
gh api repos/sentrux/sentrux/releases --jq '.[].tag_name'
gh api "repos/sentrux/sentrux/contributors?per_page=15" --jq '.[] | {login,contributions}'
```

Example agent workflow (from the project README, **not** run locally — labeled as illustrative):

```
Agent: session_start()  → { quality_signal: 7342 }
  ... agent writes 500 lines ...
Agent: session_end()    → { pass: false, signal_before: 7342, signal_after: 6891,
                            summary: "Quality degraded during this session" }
```

## What worked

- **The metric design is genuinely substantive, not vaporware.** Each of the 5 metrics maps to a named algorithm with a stated formula, range, and normalization (Newman's Q, Tarjan SCC, Gini, Lakos depth, dead/duplicate ratio). The accompanying anti-gaming argument (continuous score over letter grades; root causes over proxies) is the strongest part of the project and is exactly the right framing for an *AI-agent* quality sensor, where the controller will reliably game any boundary you give it.
- **Real Claude Code / MCP integration.** Unlike many catalog candidates, sentrux ships an actual MCP server with `session_start`/`session_end` (baseline-vs-after gate) and a Claude Code plugin marketplace entry. The `session_end → pass:false` degradation signal is precisely the inner-loop Verify-stage feedback the catalog cares about, and it is agent-readable, not just human-readable.
- **Right architecture for the job.** Pure Rust single binary, no runtime deps, 52 languages via tree-sitter plugins with zero per-language Rust code (generic platform + `tags.scm` query files). Cross-platform (macOS/Linux/Windows) with GPU-backend fallback. 121 `.rs` files with 24 test files including dedicated metric/graph/DSM/evo tests.
- **Layered rules engine for CI governance.** `.sentrux/rules.toml` encodes layer order, boundary constraints, and cycle/complexity/god-file caps — turning architectural intent into a machine-enforced gate (`sentrux check .` with exit code). This is real outer-loop Ship-stage value.
- **Self-aware positioning.** The README's critique of Spec Kit ("reinvented waterfall, no feedback loop, no structural analysis") is accurate and the philosophy doc ("verification is more valuable than generation") is coherent. The tool knows what gap it fills.

## What didn't work or surprised us

- **Severe maturity / bus-factor risk.** Despite 2,480 stars, the contributor graph is essentially **one person** (3 contributors total: `v1b3coder` 5 commits, `sentrux` 4, `trevorsilence` 1). The project is ~5 weeks old (created 2026-03-11), at **v0.5.x** (pre-1.0), with 29 releases compressed into a single week of March and **no commits since 2026-03-19** at the time of evaluation. Stars are running far ahead of code maturity and continuity is unproven.
- **"Recursive self-improvement" is marketing.** The mechanism is a human/agent-in-the-loop cybernetic feedback cycle, not autonomous self-improvement. Useful, but the phrase should be read with skepticism — the tool does not improve itself, it gives the agent a score to optimize against.
- **Commercial open-core model with a paid tier.** The free binary is MIT and genuinely functional (5 metrics, treemap, MCP, rules, session gate), but there is a **Pro tier ($15/mo, Stripe/LemonSqueezy)** delivering features via an Ed25519-licensed, per-user *watermarked* dylib under BSL (source-available, no redistribution). Detail limits are tier-gated in `license.rs` (`Tier::Free` `detail_limit() = 0`). Not disqualifying — the core is real — but it's a vendor-driven product, not a community project, and feature depth is partly paywalled.
- **GUI-first, desktop-bound.** The headline experience is a wgpu treemap desktop app, which is awkward for headless CI/agent boxes; the CLI/MCP paths are the relevant ones for an automated dev loop and the GUI value is hard to realize in agent contexts.
- **Metrics are structural-only and unvalidated against outcomes.** The score measures graph structure; there is no evidence (benchmarks, studies) that a higher sentrux score correlates with fewer agent errors or better maintainability beyond the theoretical argument. The README's "6772" demo number is illustrative, not a validated baseline.
- **Score thresholds are opaque.** A single 0–10000 number is easy to track but hard to interpret in absolute terms ("is 7342 good?"); its value is mostly *relative* (before vs after), which is how the gate is designed to use it.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + (modest) | Catches architectural drift (new cycles, god files, dead/duplicate code) an agent introduces silently; structural, not behavioral — does not catch logic bugs |
| Speed | neutral / + | Static analysis is "milliseconds" per the docs; surfaces degradation in-session rather than weeks later, but adds a scan step to the loop |
| Maintainability | + | Core value: 5 root-cause metrics (modularity, acyclicity, depth, complexity equality, redundancy) plus a layered rules engine directly target long-term architectural health |
| Safety | neutral | Not a security/malice tool; the only "safety" is the human-in-the-loop governance framing, not threat detection |
| Cost Efficiency | + (modest) | A degrading codebase makes each subsequent agent session more expensive (more failed searches/edits); catching drift early avoids compounding waste — though the claim is unmeasured |

## Verdict

**CONDITIONAL**

sentrux is a real, thoughtfully-designed architectural quality sensor, not vaporware — the 5 root-cause metrics rest on named algorithms (Newman's Q, Tarjan, Gini, Lakos), the anti-gaming rationale is the best-articulated in this catalog's quality space, and it ships genuine Claude Code/MCP integration with a `session_start`/`session_end` degradation gate that fits the inner-loop Verify stage exactly. The "recursive self-improvement" framing oversells a standard human/agent-in-the-loop feedback cycle, and the `evolution` tool is git-history analysis, not self-modification — but the underlying substance holds up.

What keeps it from ADOPT is **maturity, not concept**: a ~5-week-old, pre-1.0, effectively single-author project whose stars vastly outrun its commit base, with a commercial open-core paid tier and no commits in the months since its March burst. **Adopt it conditionally when** (a) you run multi-session agent work on a codebase whose architecture you care about, (b) you can use the CLI/MCP paths headlessly (the GUI is secondary for agent loops), and (c) you treat the score as a *relative* before/after gate rather than an absolute target. Pin a known release, keep the free MIT core, and re-evaluate continuity (commits resuming, 1.0, broader contributor base) before depending on it in CI. Not SKIP — it fills a real and under-served niche (architecture-level feedback for agent-written code) with credible engineering.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [sentrux](https://github.com/sentrux/sentrux) | tool | Rust structural quality sensor: 5 root-cause metrics (modularity/acyclicity/depth/Gini/redundancy) into one score, with live treemap, rules engine, and MCP session-degradation gate for agent-written code | AI agents silently degrade codebase architecture session-over-session (new cycles, god files, tangled deps) with no terminal-visible feedback loop | agnix (config linting — different target: configs vs. architecture); code-review tools (behavioral/style, not graph structure); Spec Kit (plan-first, explicitly critiqued by sentrux as having no implementation feedback loop) |
