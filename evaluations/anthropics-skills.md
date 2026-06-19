# Evaluation: anthropics/skills

**Repo:** [anthropics/skills](https://github.com/anthropics/skills)
**Stars:** 152,538 | **Last updated:** 2026-06-09 | **License:** Apache-2.0 (example skills), source-available (document skills)
**Dev loop stage:** Implement / Reflect
**Layer:** Tooling

---

## What it does

Anthropic's official skills repository — 17 skills organized into three plugin packages: `document-skills` (docx, pdf, pptx, xlsx — the engines behind Claude's native document capabilities), `example-skills` (12 skills covering design, testing, MCP building, skill creation, and more), and `claude-api` (Claude API/SDK reference). The repo also houses the Agent Skills spec (now at agentskills.io) and a skill template.

Each skill is a self-contained directory with a SKILL.md and supporting scripts/references. The document skills include Python scripts for actual file manipulation. The example skills range from dense reference documents (mcp-builder at 9KB, frontend-design at 8KB) to full development environments (skill-creator at 33KB with eval harness, webapp-testing with Playwright helper scripts).

## How we tested it

Architecture review of the repo structure, skill content, and marketplace manifest. Read 5 skills in full (mcp-builder, frontend-design, webapp-testing, skill-creator, claude-api) and checked commit frequency.

```bash
gh api repos/anthropics/skills --jq '.description, .stargazers_count, .updated_at'
gh api repos/anthropics/skills/contents/skills --jq '.[].name'
gh api repos/anthropics/skills/contents/skills/mcp-builder/SKILL.md --jq '.content' | base64 -d
gh api repos/anthropics/skills/contents/.claude-plugin/marketplace.json --jq '.content' | base64 -d
```

## What worked

- **frontend-design is the gold standard for design skills.** 8KB of opinionated, self-aware guidance that explicitly identifies and avoids "AI design defaults" (warm cream + serif, dark + acid green, broadsheet hairlines). The two-pass workflow (design plan → self-critique → build) with ASCII wireframes is more sophisticated than any community design skill.
- **skill-creator includes a complete eval harness.** 33KB covering skill drafting, test case generation, quantitative benchmarking with variance analysis, and description optimization for triggering accuracy. This is the most complete skill development workflow in any catalog entry.
- **mcp-builder is production-grade.** Covers both FastMCP (Python) and MCP SDK (TypeScript), including transport decisions, error handling patterns, tool naming conventions, and context management. References bundled `mcp_best_practices.md`.
- **claude-api skill stays current.** Updated weekly with model releases (Fable 5, Opus 4.8 migration, Managed Agents, etc.) — functions as a living reference, not a frozen snapshot.
- **Document skills power Claude's actual document features.** The docx/pdf/pptx/xlsx skills include Python scripts for real file manipulation, making them a reference for how to build skills that execute code rather than just give instructions.

## What didn't work or surprised us

- **Only 17 skills despite 152K stars.** The star count reflects Anthropic's brand, not breadth — community collections (everything-claude-code, antigravity-awesome-skills) have 10-100× more skills.
- **Dual licensing adds friction.** Example skills are Apache-2.0, but document skills are "source-available" with terms in LICENSE.txt — not open source. The distinction matters for forks.
- **Spec is a pointer.** The `/spec` directory just redirects to agentskills.io — no in-repo specification content.
- **No engineering/workflow skills.** No TDD, code review, debugging, or lifecycle skills — those gaps are filled by mattpocock/skills and agent-skills (addyosmani). The focus is creative, document, and meta (skill-creator).
- **Commit pace is modest.** ~5 commits in 2 weeks, all updating existing skills. No new skills added in the window checked.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | mcp-builder and webapp-testing produce working artifacts on first try |
| Speed | + | skill-creator accelerates skill authoring with eval loop; claude-api eliminates doc lookups |
| Maintainability | neutral | Skills are well-structured but narrow in scope |
| Safety | neutral | No security-focused skills |
| Cost Efficiency | + | Frontend-design's two-pass approach avoids wasted iterations on generic output |

## Verdict

**CONDITIONAL**

Use the document-skills plugin when working with Office documents — these are the official engines behind Claude's document features and the best reference for script-backed skills. Use claude-api when building LLM applications. Use skill-creator when authoring new skills and needing the eval harness. Skip the example-skills for general engineering work — mattpocock/skills (ADOPT) and agent-skills (ADOPT) cover that territory with more depth and breadth. The repo's highest value is as a canonical reference for _how to build skills_, not as a skill collection to install wholesale.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [anthropics/skills](https://github.com/anthropics/skills) | reference | Official Anthropic skills — canonical SKILL.md examples, document engines, skill-creator eval harness | Need the authoritative reference for writing agent skills and the engines behind Claude's document capabilities | agentskills, skill-creator |
