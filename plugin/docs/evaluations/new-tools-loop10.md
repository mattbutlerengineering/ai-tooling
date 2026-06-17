# New Tools Evaluation (Loop 10)

Tools discovered during workflow reframe research. Evaluated against dev loop stages and quality signals.

## code-review-graph

**Repo:** [tirth8205/code-review-graph](https://github.com/tirth8205/code-review-graph)
**Stars:** 18,578 | **Last updated:** 2026-06-14 | **License:** MIT
**Stage:** Plan (orientation), Review (inner loop)
**Layer:** Tooling
**Signals:** Cost Efficiency, Speed, Correctness

**What it does:** Local-first code intelligence graph for MCP and CLI. Builds a persistent map of your codebase so AI tools read only what matters. Key feature: blast-radius analysis identifies exactly which files are affected by a change. Incremental updates in <2s. Benchmarked 38x-528x token reduction on reviews and large-repo workflows.

**Overlaps with:** codegraph (both build persistent code graphs with MCP), graphify (structural analysis)

**Key difference:** code-review-graph adds review-aware blast-radius analysis that neither codegraph nor graphify provides. The benchmarked token reductions are dramatically stronger than codegraph's claimed 58% fewer tool calls. Review-focused intelligence means it directly serves the Review stage, not just orientation.

**Verdict:** CONDITIONAL — evaluate as a codegraph replacement
**Justification:** The blast-radius feature is unique and directly moves Correctness (know what your change affects before you ship). The benchmarked token reductions are best-in-class for code understanding tools. 18K stars and MIT license are strong. However, codegraph is already in the workflow — this would be a swap, not an addition. Worth a hands-on comparison before switching.

## deer-flow

**Repo:** [bytedance/deer-flow](https://github.com/bytedance/deer-flow)
**Stars:** 71,320 | **Last updated:** 2026-06-16 | **License:** Apache-2.0
**Stage:** Outer loop (all stages), Autonomy
**Layer:** Tooling
**Signals:** Speed, Correctness

**What it does:** ByteDance's open-source long-horizon agent harness. Handles tasks ranging from minutes to hours with sandboxes, memories, tools, skills, subagents, and a message gateway. Designed for multi-step autonomous work that exceeds single-session scope.

**Overlaps with:** ralph-claude-code (autonomous dev loop), GSD (multi-phase orchestration), claude-squad (multi-agent management)

**Key difference:** deer-flow is a standalone platform rather than a Claude Code plugin. It operates outside the Claude Code ecosystem with its own sandbox, memory, and orchestration layer. The 71K stars reflect broad adoption but for a different use case than augmenting Claude Code.

**Verdict:** SKIP — catalog only
**Justification:** Like OpenHands and nanobot, deer-flow is an alternative agent platform, not a tool that improves the Claude Code dev loop. It doesn't integrate into the inner/outer loop stages — it replaces them. The 71K stars are impressive but represent a different audience. Keep in catalog under Agent Harnesses for users exploring alternatives.

## stryker-js (mutation testing)

**Repo:** [stryker-mutator/stryker-js](https://github.com/stryker-mutator/stryker-js)
**Stars:** 2,916 | **Last updated:** 2026-06-16 | **License:** Apache-2.0
**Stage:** Verify (inner loop)
**Layer:** Infrastructure
**Signals:** Correctness

**What it does:** Mutation testing framework for JavaScript/TypeScript. Introduces small changes (mutations) into your source code, then runs your tests. If tests still pass after a mutation, they're not catching that case — revealing gaps in test quality. Supports Jest, Vitest, Mocha, Karma, and more.

**Key insight for our workflow:** Our Verify stage currently checks "do tests pass?" but not "are the tests actually good?" Mutation testing answers the second question. A test suite with 90% coverage but low mutation score is giving false confidence.

**Overlaps with:** Nothing in the current workflow. This is a gap — no tool currently evaluates test quality.

**Verdict:** ADD to Verify stage (infrastructure layer, JavaScript/TypeScript projects)
**Justification:** Fills a genuine gap in the Verify stage. Coverage gating tells you "did you write tests?" Mutation testing tells you "are your tests worth anything?" This directly moves Correctness by catching test suites that pass but don't actually verify behavior. 2.9K stars is modest but mutation testing is a niche — Stryker is the established leader for JS/TS. Apache-2.0 license. Language-specific (JS/TS only), so it's infrastructure you build per-project, not a universal tool.

## nanobot

**Repo:** [HKUDS/nanobot](https://github.com/HKUDS/nanobot)
**Stars:** 44,292 | **Last updated:** 2026-06-16
**Stage:** N/A
**Signals:** N/A

**Verdict:** SKIP — alternative AI agent platform (chat, Telegram, Discord), not a Claude Code workflow tool. Same exclusion logic as OpenHands and Flowise.

## ai-devkit

**Repo:** [codeaholicguy/ai-devkit](https://github.com/codeaholicguy/ai-devkit)
**Stars:** 1,364 | **Last updated:** 2026-06-16
**Stage:** All (kitchen-sink workflow tool)
**Signals:** Correctness, Speed

**Verdict:** SKIP — duplicates superpowers + agent-skills + claude-mem individually. Cross-agent compatibility is its differentiator, but we're focused on Claude Code. No license listed.

## zcf (Zero-Config Code Flow)

**Repo:** [UfoMiao/zcf](https://github.com/UfoMiao/zcf)
**Stars:** 6,041 | **Last updated:** 2026-06-16
**Stage:** N/A (API relay setup)
**Signals:** Cost Efficiency (API routing)

**Verdict:** SKIP — API relay/router setup wizard, not a dev loop tool. README dominated by relay provider ads. Useful for cost optimization but doesn't move quality signals in the dev loop itself.

## agent-skill-creator

**Repo:** [FrancyJGLisboa/agent-skill-creator](https://github.com/FrancyJGLisboa/agent-skill-creator)
**Stars:** 1,513 | **Last updated:** 2026-06-16 | **License:** MIT
**Stage:** Outer loop (Decompose — meta-tooling)
**Signals:** Speed

**Verdict:** CONDITIONAL — useful if you create skills frequently, but doesn't improve code quality directly. Meta-tool that improves the tools, not the code. Keep in catalog.
