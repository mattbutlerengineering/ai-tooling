# New Tools Evaluation (Loop 2)

Tools from the catalog that lacked dedicated evaluations. Each assessed for whether it earns a slot in the recommended WORKFLOW.md stack.

## claude-code-action
**Repo:** [anthropics/claude-code-action](https://github.com/anthropics/claude-code-action)
**Stars:** 8,023 | **Last updated:** 2026-06-15 | **Forks:** 1,905
**What it does:** GitHub Actions integration that deploys Claude directly into PR and issue workflows. Responds to `@claude` mentions in PRs/issues, implements fixes, reviews code, answers architecture questions, and can run on automated triggers (e.g., every PR open). Supports Anthropic API, AWS Bedrock, Google Vertex AI, and Microsoft Foundry as providers. Runs on your own GitHub Actions runners with file system and GitHub API access. Also supports structured JSON output for complex automation pipelines.
**Current workflow alternative:** Nothing in the catalog covers this exact niche. The `pr-review-toolkit` plugin handles local pre-commit review. KARIMO mentions "CI-friendly agent teams" but operates at the harness level, not as a GitHub-native action.
**Key difference:** The only Anthropic-official tool that moves Claude out of the local terminal and into the asynchronous GitHub collaboration layer — teammates can invoke it without installing anything, and it responds to events rather than commands.

**Verdict:** ADD to L3
**Justification:** At 8K stars with daily maintenance and first-party Anthropic support, this fills a genuine gap: async, teammate-accessible AI assistance triggered by GitHub events rather than local CLI invocations. It earns its slot at L3 where teams start operating and PRs become the primary coordination mechanism. No existing catalog entry covers GitHub-native, event-driven AI integration.

---

## shadcn/improve
**Repo:** [shadcn/improve](https://github.com/shadcn/improve)
**Stars:** 4,890 | **Last updated:** 2026-06-15 | **Forks:** 168
**What it does:** Orchestrates a two-model audit pipeline — a capable model audits the codebase across nine categories (correctness, security, performance, tech debt, test coverage, etc.) and writes self-contained markdown execution plans into a `plans/` directory; cheaper models or humans then execute those plans in isolation. Never modifies source code directly; optionally publishes plans as GitHub issues.
**Current workflow alternative:** The `code-review` plugin and `pr-review-toolkit` cover per-PR review. The `improve-codebase-architecture` skill covers broad refactoring audits.
**Key difference:** The explicit separation of auditor model and executor model is the novel mechanism — the expensive model is used only for analysis and plan-writing, while a cheap model (Haiku) does the execution. This maps directly to the ACMM performance guidance (Haiku for workers, Sonnet/Opus for orchestration) and produces durable, human-readable plan artifacts that survive context resets and can be assigned as GitHub issues.

**Verdict:** ADD to L4
**Justification:** At 4.9K stars and updated same-day, this fills a distinct gap: existing review tools are PR-scoped and reactive, while `improve` is codebase-scoped and proactive, producing persistent plan artifacts rather than inline comments. The two-model cost optimization pattern aligns with the workflow's existing performance guidelines. Best introduced at L4 where multi-agent orchestration and model-routing become practical.

---

## design-council
**Repo:** [sjsyrek/design-council](https://github.com/sjsyrek/design-council)
**Stars:** 164 | **Last updated:** 2026-05-28 | **Forks:** 16
**What it does:** Convenes 11 role-specialized peer agents (principal-engineer, security-engineer, PM, UX, accessibility, etc.) to debate a technical decision in real time, with the invoking Claude acting as CEO. Runs in 6 phases: plan card, shared brief, parallel spawn, cross-talk (up to 3 debate rounds via SendMessage), CEO arbitration, and decision log. Prompt caching across the shared brief recovers 7-12K tokens per council. Results saved to `~/.claude/councils/`.
**Current workflow alternative:** The L3 stack includes `code-review plugin` (multi-agent confidence-scored review) and `pr-review-toolkit` (structured dimensions: type analysis, silent failures, test coverage). Both review code artifacts after implementation.
**Key difference:** Operates upstream of code: debates *decisions* before anything is implemented. The adversarial multi-role structure (11 independent contexts, no priming between agents) surfaces cross-cutting concerns that single-agent review systematically misses. Explicitly high-cost by design (10-20x token multiplier) and self-limits to decisions crossing 2+ specialist domains.

**Verdict:** CONDITIONAL at L4
**Justification:** At 164 stars, this is early-stage but architecturally novel. It fills a gap no other recommended tool covers (pre-implementation adversarial design debate). The 10-20x token cost makes it wasteful as a default step, but valuable for non-trivial architecture decisions crossing multiple specialist domains. Best at L4+ where context compression (headroom) and memory infrastructure make the cost manageable. Invoke selectively, not routinely.
