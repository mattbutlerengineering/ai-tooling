# Evaluation: Pare

**Repo:** [Dave-London/Pare](https://github.com/Dave-London/Pare)
**Stars:** 129 | **Last updated:** 2026-06-16 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Implement / Verify (intervenes on every git/test/build/package tool call across the inner loop)
**Layer:** Tooling

---

## What it does

Pare is a suite of **28 MCP servers** (240 tools) that wrap common developer CLIs — git, gh, npm, pip, cargo, go, docker, kubectl, terraform, the major test runners and linters, ripgrep/fd, and more — and return **schema-validated JSON instead of raw terminal text**. Each tool emits two outputs: a human-readable `content` string and a typed `structuredContent` object backed by MCP's `outputSchema`. So instead of an agent shelling out to `git status` and regex-parsing prose that varies by OS, locale, and tool version, it calls a `status` MCP tool and gets back `{branch, upstream, ahead, staged[], modified[], untracked[], conflicts[], clean}`.

The framing matters for placing this in the catalog cluster: Pare's **primary** claim is correctness/reliability — eliminating the entire class of brittle-string-parsing errors — and token reduction is explicitly positioned as a "bonus." It is not a compression layer interposed on existing output (the rtk/headroom model); it is a *replacement* for the CLI-shell path with a structured MCP interface. The token savings come from the structured representation being smaller than verbose CLI text (published table: docker build 95%, git log --stat 92%, npm install 83%, vitest 80%, down to npm audit 36% — savings scale with how verbose the raw output is). For terse tools (eslint, tsc) the savings are modest and the stated value is the typed data, not the token count.

Servers are independent npm packages (`@paretools/git`, `@paretools/docker`, etc.) installed à la carte — "most projects need just 2-4." Setup is `npx @paretools/init --client claude-code --preset <web|python|rust|...>` plus appending a rules file to `CLAUDE.md` so the agent prefers Pare tools over raw Bash. Tool surface is filterable via `PARE_TOOLS` / `PARE_{SERVER}_TOOLS` env vars (e.g. read-only git: `PARE_GIT_TOOLS=status,log,diff,branch,show`).

## How we tested it

**Evidence:** REVIEW

Architecture-review evaluation. Method: inspected the GitHub repo metadata (`gh api`), the full README (problem statement, the 8-row token-savings table, the `git status` worked example, the 28-server/240-tool catalog, Quick Setup, the tool-selection env vars, troubleshooting), `SECURITY_MODEL.md`, the reproducible benchmark methodology (`benchmarks/v2/methodology-reproducible.md`), the repo tree, contributor list, and release/tag history. Calibrated against the existing token-efficiency peer evals `evaluations/rtk.md` (CONDITIONAL) and `evaluations/headroom.md` (CONDITIONAL), and the overlapping catalog rows (git-mcp, token-optimizer-mcp, headroom, context-mode). **Not installed and not exercised in a live Claude Code session** — no MCP servers were configured and no tools were called, so every token figure below is the project's own published estimate (cl100k_base `length/4` heuristic, median of N runs over 117 read-only scenarios), not measured here.

```bash
gh api repos/Dave-London/Pare --jq '{stars,license,description,pushed_at,created_at,language,open_issues}'
gh api repos/Dave-London/Pare/readme --jq '.content' | base64 -d
gh api "repos/Dave-London/Pare/git/trees/main?recursive=1" --jq '.tree[].path'
gh api repos/Dave-London/Pare/contributors --jq '.[].login'
gh api repos/Dave-London/Pare/releases --jq '.[].tag_name'
gh api repos/Dave-London/Pare/contents/SECURITY_MODEL.md --jq '.content' | base64 -d
gh api repos/Dave-London/Pare/contents/benchmarks/v2/methodology-reproducible.md --jq '.content' | base64 -d
# Catalog overlap scan + peer calibration:
grep -niE 'git-mcp|token-optimizer|headroom|pare|paretools' /Users/mbutler/github/ai-tooling/CATALOG.md
#   evaluations/rtk.md (CONDITIONAL), evaluations/headroom.md (CONDITIONAL)
```

## What worked

- **Correctness-first design is genuinely differentiated in this cluster.** Every other token tool in the catalog (rtk, headroom, context-mode, token-optimizer-mcp, caveman) *compresses existing output* — they take fragile CLI text and make it smaller, but the agent still consumes a lossy derivative of platform/locale/version-specific prose. Pare attacks the root cause: it returns typed JSON with stable field names so the agent never parses strings at all. The token win is a side effect of using a smaller, structured representation. That makes Pare additive to, not redundant with, the compression cluster.
- **Honest, reproducible, self-bounded benchmarks.** The savings table spans 95% down to 36% and the README explicitly says terse tools (eslint, tsc) get little token benefit and should be valued for the typed data instead. The methodology doc documents 117 read-only scenarios across 76 tools, a deterministic `length/4` token heuristic, median-of-N runs, and auto-skip when a CLI isn't installed. This is more transparent than a single cherry-picked headline number.
- **Strong security posture for a tool that executes real CLIs.** A dedicated `SECURITY_MODEL.md` lays out the trust boundary (MCP client owns consent/sandboxing), an explicit, reasoned decision to leave `path`/`cwd` unrestricted, and `assertNoFlagInjection()` validation rejecting `-`-prefixed positional args plus format-regex validation for `ports[]`/`volumes[]`/`env[]`. Plus OpenSSF Scorecard + Best Practices badges, CodeQL, SBOM workflow, security audit docs, and a SECURITY.md. Unusually mature security hygiene for a 129-star project.
- **À la carte, filterable surface keeps MCP-tool sprawl in check.** Servers install independently (just the 2-4 you need), presets map to ecosystems, and `PARE_TOOLS`/`PARE_{SERVER}_TOOLS` let you whitelist a minimal tool set (e.g. read-only git). This directly mitigates the standard MCP failure mode where 240 tool definitions bloat the system prompt — the README calls this out in troubleshooting.
- **Real engineering maturity for the size.** TypeScript-strict monorepo, changesets-driven releases at v0.20.0 with per-package versioning, CI + codecov + canary + nightly + release workflows, multiple human contributors (not a single-author script), MIT license, published to npm with download badges, per-tool schema docs. Pushed three days before evaluation.

## What didn't work or surprised us

- **Adoption depends on the agent actually choosing Pare tools over Bash.** The value only materializes if the agent calls the `status` MCP tool instead of running `git status` in a Bash shell. The setup leans on appending a rules file to `CLAUDE.md` to steer tool selection — but Claude Code's default reflex is the Bash tool, and there is no enforcement layer (unlike rtk's PreToolUse hook, which transparently rewrites Bash calls whether the agent cooperates or not). In practice an agent may keep shelling out and bypass Pare entirely.
- **Coverage gap vs. the raw CLI surface.** 240 wrapped tools is broad but git/gh/docker/etc. each have hundreds of flags and subcommands. Any operation outside the wrapped set forces a fall-back to raw Bash, so a session is a mix of structured-and-typed Pare calls plus unstructured shell output — the agent doesn't get a uniformly clean context. This is inherent to the wrap-the-CLI approach.
- **Pre-1.0, fast-moving, small audience.** Created 2026-02, at v0.20.0 with frequent per-package releases — schemas and tool names may still churn, and a `CLAUDE.md` rules file pinned to one version can drift. 129 stars means limited real-world battle-testing compared with the 37K-63K-star compression peers.
- **Structured-only is one-way for fields the schema omits.** If a tool's output schema doesn't model a detail the raw CLI would have shown (an obscure warning, a non-modeled status), the agent simply never sees it — there is no retrieve-the-raw-output fallback the way rtk tees full output on failure or headroom caches originals for `retrieve`. The mitigation is that Pare also returns a human-readable `content` string, but that is the same prose the structured path is meant to replace.
- **Different problem from git-mcp despite the catalog overlap.** git-mcp serves *remote GitHub repo source/docs* as MCP resources to stop API hallucination; Pare wraps the *local* git CLI for structured status/log/diff/commit. They share the word "git" and the MCP transport but solve unrelated problems — not real overlap. The genuine neighbors are the compression tools, and against those Pare is complementary, not competing.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | The core value: schema-validated JSON with stable field names eliminates fragile CLI-text parsing across OS/locale/tool-version differences — a class of silent agent bugs the compression tools don't address |
| Speed | + | Fewer input tokens per tool call (published 36-95%, scaling with verbosity) means faster turns and more headroom before compaction |
| Maintainability | neutral | Strong CI/test/release discipline and multi-contributor, but pre-1.0 with churning schemas and a `CLAUDE.md` rules file that must stay in sync |
| Safety | + | `assertNoFlagInjection` on positional args, explicit documented trust model, OpenSSF Scorecard/Best-Practices, CodeQL, SBOM — but servers execute real CLIs and `path`/`cwd` is intentionally unrestricted, so client-side workspace sandboxing is required |
| Cost Efficiency | + | Project-claimed 36-95% token reduction on wrapped commands, with a reproducible benchmark suite; gains are largest on verbose build/install/test output and minimal on terse linters |

## Verdict

**CONDITIONAL**

Adopt Pare when you run AI coding agents that lean heavily on git, test runners, builds, installs, and container/infra tooling, and you want **reliable typed tool output** rather than agents regex-parsing fragile terminal text — that reliability angle, not the token savings, is the real reason to choose it. It is the only tool in its catalog cluster that attacks the *source* of verbose/fragile CLI output (a structured MCP replacement) instead of compressing the output after the fact, which makes it complementary to rtk/headroom rather than redundant: Pare cleans up the git/test/build path, a compression layer can still mop up the remaining raw Bash and file-read context. Install only the 2-4 servers your stack needs and use `PARE_TOOLS` to keep the tool surface small. Security hygiene is unusually strong for the size (documented trust model, flag-injection guards, OpenSSF badges).

It stops short of ADOPT for three reasons. First, **enforcement**: the benefit only lands if the agent actually calls Pare tools over its default Bash reflex, and the only lever is a `CLAUDE.md` rules file — there is no transparent hook like rtk's that guarantees interception. Second, **coverage**: 240 wrapped tools still leaves most CLI flags unwrapped, so sessions remain a mix of clean structured calls and raw shell output. Third, **maturity**: at 129 stars and v0.20.0 (created four months before evaluation) the schemas may still churn and real-world battle-testing is thin versus the 37K-63K-star compression peers. Skip it if your agent's context is dominated by file reads rather than dev-tool output (the compression tools reach those; Pare does not), or if you can't reliably steer tool selection. Note the catalog "overlaps with git-mcp" is misleading — git-mcp is remote-repo-source-as-resource and solves an unrelated problem; Pare's true neighbors are the token-compression tools, which it complements.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Pare](https://github.com/Dave-London/Pare) | MCP server | Suite of MCP servers that wrap git/test/npm/Docker CLIs and return schema-validated JSON instead of fragile terminal text (bonus: 36-95% fewer tokens) | Generic dev-tool output is fragile to parse and wastes tokens; agents need structured, compact, typed tool interfaces | headroom, rtk, token-optimizer-mcp (complementary — Pare replaces the CLI path with structured output, the others compress existing output) |
