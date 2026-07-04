# Evaluation: microsoft/skills

**Repo:** [microsoft/skills](https://github.com/microsoft/skills)
**Stars:** 2,592 | **Last updated:** 2026-06-18 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

175 skills across 7 language tracks (Core, Foundry, Python, .NET, TypeScript, Java, Rust) for Azure SDK and Microsoft AI Foundry development. Ships as a Claude Code marketplace plugin with 7 sub-plugins (deep-wiki, azure-skills, azure-sdk-python/dotnet/typescript/java/rust), plus custom agents, hooks, and MCP configurations.

Each skill is a SKILL.md with practitioner-level SDK patterns — authentication (DefaultAzureCredential preferred over connection strings), service class architecture, error handling, and test patterns. The repo also includes 3 role-specific agents (wiki-architect, wiki-researcher, wiki-writer) and a continual-learning hook system.

## How we tested it

**Evidence:** REVIEW

Architecture review: examined repo structure, marketplace.json plugin configuration, 3 representative SKILL.md files (cloud-solution-architect, azure-cosmos-db-py, mcp-builder), the test harness, and CI workflows.

```
gh api repos/microsoft/skills --jq '.description, .stargazers_count'
gh api repos/microsoft/skills/contents/.github/skills/cloud-solution-architect/SKILL.md
gh api repos/microsoft/skills/contents/.github/plugins/azure-sdk-python/skills/azure-cosmos-db-py/SKILL.md
gh api repos/microsoft/skills/contents/.github/skills/mcp-builder/SKILL.md
gh api repos/microsoft/skills/contents/tests/README.md
```

Not hands-on tested (no Azure project available). Evaluation based on SKILL.md quality, repo engineering, and test infrastructure.

## What worked

- **Cloud Solution Architect skill is exceptional** — 10 design principles, 6 architecture styles with selection criteria, 44 cloud design patterns mapped to Well-Architected Framework pillars. This is a full architecture reference, not a prompt.
- **SDK skills encode real production patterns** — Cosmos DB skill covers dual auth (DefaultAzureCredential + emulator), partition key strategies, parameterized queries, and TDD patterns. Includes security rules ("avoid connection strings, they bypass Entra audit and rotation").
- **Test harness with 141 scenarios** — TypeScript-based eval framework with acceptance criteria, correct/incorrect pattern matching, and iterative improvement loop (`ralph-loop.ts`). CI runs evals on every PR.
- **mcp-builder skill** is a strong meta-skill for building MCP servers across Python (FastMCP), TypeScript, and C#/.NET — includes the full Microsoft MCP ecosystem map.
- **deep-wiki plugin** generates structured wiki documentation with Mermaid diagrams using 3 specialized agents.
- **Daily commits** from multiple contributors including automated syncs from GitHub-Copilot-for-Azure upstream.

## What didn't work or surprised us

- **Azure-locked** — 155 of 175 skills are Azure-specific. The 20 non-Azure skills (core + deep-wiki) are useful anywhere, but the collection's value drops sharply outside Microsoft ecosystems.
- **Skill Explorer website** (microsoft.github.io/skills) only links to Copilot SDK installation — no `npx skills add` or Claude Code-specific install path documented on the site.
- **"Work in Progress" banner** in README despite 175 skills and a test harness suggests the team considers this pre-v1.
- **Plugin structure is complex** — 7 sub-plugins mean installing the full collection pulls a lot. No guidance on which sub-plugin to install for a given project type.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | SDK skills encode security best practices (DefaultAzureCredential, managed identity) that prevent real production bugs |
| Speed | + | Eliminates Azure SDK research time — patterns are ready to copy |
| Maintainability | + | Architecture skills (cloud-solution-architect) guide long-term design decisions |
| Safety | + | Authentication patterns default to credential rotation and Entra audit compliance |
| Cost Efficiency | neutral | Standard context cost; skills load on-demand via progressive disclosure |

## Verdict

**CONDITIONAL**

Use when building on Azure or Microsoft AI Foundry — the SDK skills encode genuine production patterns that prevent real security and architecture mistakes. The cloud-solution-architect and mcp-builder skills have standalone value outside Azure projects. Skip if your stack doesn't touch Microsoft services — the 155 Azure-specific skills provide no value and the 20 general skills are covered better by mattpocock/skills (ADOPT) and agent-skills (ADOPT).

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [microsoft/skills](https://github.com/microsoft/skills) | skill | Skills, MCP servers, and Agents.md for Microsoft SDKs to ground coding agents | Need AI assistance with Microsoft/Azure/dotnet workflows | google/skills |
