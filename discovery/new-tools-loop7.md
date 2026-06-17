# New Tools Evaluation (Loop 7)

User-requested tools and remaining catalog gaps, assessed for WORKFLOW.md inclusion.

## docmd
**Repo:** [docmd-io/docmd](https://github.com/docmd-io/docmd)
**Stars:** 2,038 | **Last updated:** 2026-06-15 | **Forks:** 117
**What it does:** Converts a `docs/` folder of Markdown files into a production-ready static documentation site via a single CLI command. No React or heavy build tooling — outputs plain HTML with built-in search, PWA support, and ~18 KB of JS. Includes an MCP server for agent integration, auto-generates `llms.txt` context files, and exposes browser widgets for copying Markdown into AI chat interfaces.
**Current workflow alternative:** Nothing in the catalog covers Markdown-to-docs-site generation. The closest tangent is plain Markdown files in `evaluations/` and `skills/`.
**Key difference:** The MCP server and `llms.txt` generation make it AI-native beyond typical static site generators. Agents can query and validate documentation programmatically.

**Verdict:** CONDITIONAL at L3+ for teams with public docs
**Justification:** Actively maintained with solid traction (2K stars). AI-native features (MCP server, `llms.txt`, agent skills) are genuinely relevant. However, earns a slot only for teams that publish documentation externally — for purely internal or code-only repos it adds no value over raw Markdown.

---

## agent-rules-books
**Repo:** [ciembor/agent-rules-books](https://github.com/ciembor/agent-rules-books)
**Stars:** 1,869 | **Last updated:** 2026-05-22 | **Forks:** 300
**What it does:** Distills 13 classic software engineering books (Clean Code, DDD, Refactoring, DDIA, Clean Architecture, Release It!, The Pragmatic Programmer, etc.) into actionable AGENTS.md/CLAUDE.md rule sets, each available in full/mini/nano token-budget tiers.
**Current workflow alternative:** mattpocock/skills (L2) encodes engineering philosophy. User's global rules already capture Clean Code and simplicity principles.
**Key difference:** Encodes established canonical principles from 13 foundational texts with tiered token budgets (full/mini/nano). The DDD, DDIA, Clean Architecture, and Release It! rule sets cover production reliability, data systems, and strategic architecture — territory no existing catalog entry addresses.

**Verdict:** CONDITIONAL at L3-L4
**Justification:** For teams that don't already have production-hardened principles in their CLAUDE.md, the DDD, Clean Architecture, DDIA, and Release It! rule sets fill genuine gaps. The tiered sizing is a practical differentiator — the only catalog entry that explicitly manages context budget for rule sets. For users who already have global rules encoded, the Clean Code and Refactoring sets are redundant; value arrives at L3+ when teams need shared canonical references.

---

## ralph-claude-code
**Repo:** [frankbria/ralph-claude-code](https://github.com/frankbria/ralph-claude-code)
**Stars:** 9,339 | **Last updated:** 2026-06-15 | **Forks:** 714
**What it does:** Wraps Claude Code in a persistent autonomous loop that reads project tasks from `.ralph/PROMPT.md`, executes Claude Code iteratively, and exits only when a dual-condition gate (completion indicators + explicit EXIT_SIGNAL) is satisfied. Includes rate limiting (100 calls/hour), circuit breaker, tmux dashboard, Docker sandboxing, GitHub Issues import/sync, and batch processing with dependency tracking.
**Current workflow alternative:** superpowers (L3) provides orchestration patterns but assumes human-in-the-loop. No existing entry covers a fully unattended loop-until-done harness with cost-safe exit detection.
**Key difference:** Purpose-built for unattended long-running autonomous development. The dual-condition exit gate prevents premature or infinite runs. Superpowers teaches orchestration patterns; Ralph is an execution harness for lights-out execution.

**Verdict:** ADD to L4
**Justification:** At L4 teams begin delegating multi-step work without babysitting — Ralph's intelligent exit detection and rate-limit safeguards are exactly the infrastructure needed. Its 9K+ stars and 714 forks signal strong adoption, and GitHub Issues integration slots into existing issue-driven workflows. Complementary to superpowers (patterns) rather than redundant.

---

## ghostsecurity/skills
**Repo:** [ghostsecurity/skills](https://github.com/ghostsecurity/skills)
**Stars:** 389 | **Last updated:** 2026-03-11 | **Forks:** 26
**What it does:** AI-native AppSec plugin providing a full SAST/SCA/DAST pipeline within Claude Code: dependency vulnerability analysis, secrets scanning, AI-driven static code analysis, dynamic validation against a running app via HTTP proxy, and unified security reporting.
**Current workflow alternative:** trailofbits/skills (L3) covers professional security auditing. Built-in `/security-review` handles pre-commit checks.
**Key difference:** The only entry completing the full AppSec loop end-to-end — SCA (deps), SAST (code), secrets detection, and live DAST validation against a running application. The `ghost-validate` + `ghost-proxy` pair is uniquely runtime-aware.

**Verdict:** CONDITIONAL at L4 (concept sound but project health concerns)
**Justification:** The full AppSec loop concept fills a real gap between the built-in security-review spot-check and a full external SAST tool. However, at 389 stars and last updated March 2026 (3+ months stale), the project health doesn't warrant a firm recommendation. Watch for resumed activity before adopting. trailofbits/skills remains the primary security recommendation at L3.
