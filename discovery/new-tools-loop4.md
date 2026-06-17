# New Tools Evaluation (Loop 4)

High-star catalog tools without dedicated evaluations, assessed for WORKFLOW.md inclusion.

## Fabric
**Repo:** [danielmiessler/Fabric](https://github.com/danielmiessler/Fabric)
**Stars:** 42,393 | **Last updated:** 2026-06-09 | **Forks:** 4,173
**What it does:** CLI framework that organizes crowdsourced AI prompts ("Patterns") into reusable, pipeable modules. Ships with ~200 built-in patterns for summarizing, extracting wisdom, analyzing claims, writing documentation. Patterns are composable and can be served via REST API. LLM-agnostic (Claude, OpenAI, Ollama, etc.).
**Current workflow alternative:** Claude Code's native slash commands and skills cover coding-specific use cases (code review, TDD, security review).
**Key difference:** Fabric is LLM-agnostic, CLI-native, and pattern-library-first. It operates outside Claude Code on arbitrary content (clipboard, files, URLs), whereas the current workflow's skills operate inside Claude Code on codebases.

**Verdict:** SKIP
**Justification:** The workflow is coding-focused, and Fabric's coding-specific patterns are thin compared to what Claude Code skills already provide with full codebase context. Fabric's real strength is general content augmentation (summarizing podcasts, extracting wisdom from articles) which is outside the scope of this dev workflow guide. Teams already using Claude Code have little marginal gain from adding Fabric for coding tasks.

---

## claude-task-master
**Repo:** [eyaltoledano/claude-task-master](https://github.com/eyaltoledano/claude-task-master)
**Stars:** 27,549 | **Last updated:** 2026-04-28 | **Forks:** 2,583
**What it does:** MCP server + CLI that converts PRDs into structured, dependency-aware task hierarchies. Parses requirements documents, breaks them into tasks with complexity scores and subtasks, tracks status across sessions, and exposes tasks to AI editors (Cursor, Windsurf, Claude Code, VS Code) so agents always know what to work on next.
**Current workflow alternative:** GSD (L4) provides project orchestration with milestones, phases, planning, execution, and verification.
**Key difference:** Taskmaster is an editor-agnostic, PRD-first task store; GSD is a Claude Code-native workflow harness with goal-backward verification and deviation handling.

**Verdict:** SKIP
**Justification:** GSD already covers project decomposition, phase planning, milestone tracking, and verification at L4 — with goal-backward analysis that Taskmaster lacks. Adding both introduces redundant task state with no clear ownership (the "multiple overlapping orchestration systems" anti-pattern the workflow guards against). With 27K stars it's legitimate for teams not using GSD, but the overlap is direct enough to require choosing one.

---

## scorecard
**Repo:** [ossf/scorecard](https://github.com/ossf/scorecard)
**Stars:** 5,528 | **Last updated:** 2026-06-08 | **Forks:** 664
**What it does:** Automated security health assessment for open source repositories. Runs ~20 checks across supply chain hygiene: branch protection, code review enforcement, signed releases, dependency update tooling, SAST presence, CI/CD pinning, vulnerability status. Produces a 0-10 weighted score per check. Used by 1M+ critical OSS projects via weekly OpenSSF scans.
**Current workflow alternative:** trailofbits/skills (L3) audits code for security vulnerabilities. SkillSpector (L5) scans proposed skills for malicious content.
**Key difference:** Assesses whether a repository's practices and configurations meet supply chain security standards — "is this dependency safe to adopt?" rather than "does this function have an injection flaw?" Orthogonal to both trailofbits/skills (code correctness) and SkillSpector (skill malware scanning).

**Verdict:** CONDITIONAL at L3 as CI gate for dependency vetting
**Justification:** Scorecard occupies a distinct, unfilled niche: supply chain hygiene vs. code vulnerability analysis. The L3 workflow enforces quality gates (coverage, PR review) but has no signal about dependency or repo practice security — a real blind spot when agents start autonomously adding dependencies. Most valuable as a GitHub Action in CI rather than ad-hoc; teams without CI discipline (pre-L3) won't use it consistently enough.

---

## SimpleMem
**Repo:** [aiming-lab/SimpleMem](https://github.com/aiming-lab/SimpleMem)
**Stars:** 3,512 | **Last updated:** 2026-05-21 | **Forks:** 362
**What it does:** Three-stage memory compression system for LLM agents — semantic structured compression, online semantic synthesis (deduplication at write time), and intent-aware retrieval. Ships an Omni-SimpleMem extension covering text, image, audio, and video. Available as local Python library, Docker self-hosted, or cloud MCP endpoint. Claims 26.4% F1 gain on LoCoMo benchmarks and ~30x token reduction vs. raw-history accumulation.
**Current workflow alternative:** claude-mem (recommended at L4) handles persistent cross-session memory with MCP integration.
**Key difference:** The only evaluated option with academic benchmark backing (LoCoMo, published results), native multimodal memory (images, audio, video), and explicit semantic compression designed to cut token costs — concerns neither claude-mem nor OMEGA addresses.

**Verdict:** CONDITIONAL at L4 alongside claude-mem
**Justification:** SimpleMem fills a gap the current stack doesn't cover: multimodal memory and token-cost-aware compression, backed by reproducible benchmarks. For teams at L4 hitting context-window costs or needing to persist non-text artifacts, SimpleMem is a credible complement or replacement for claude-mem. Recommend the self-hosted Docker path for production use over the cloud endpoint.
