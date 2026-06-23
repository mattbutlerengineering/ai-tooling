# Evaluation: awesome-claude-skills (Composio)

**Repo:** [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)
**Stars:** 65,223 | **Last updated:** 2026-05-22 | **License:** none declared (README badge claims Apache-2.0)
**Dev loop stage:** Discover (outer loop)
**Layer:** Infrastructure

---

## What it does

A vendor-backed (Composio) curated list of Claude Skills, organized into ten task-domain sections — Document Processing, Development & Code Tools, Data & Analysis, Business & Marketing, Communication & Writing, Creative & Media, Productivity & Organization, Collaboration & Project Management, Security & Systems, Assistive Technology — plus an "App Automation via Composio" section. The README lists roughly 195 hand-annotated entries (each with a one-line description and an author credit), and the repo itself bundles ~30 first-party skill directories (mcp-builder, skill-creator, changelog-generator, file-organizer, etc.).

The list is unusually well-written at the top: the "What Are Claude Skills?" section is one of the clearest plain-English explanations of the Skills format anywhere — covering progressive disclosure, the ~100-token-per-skill cost, and the precise distinction between Skills, MCP, and tools. Beyond the list it carries real how-to content (using Skills in Claude.ai / Claude Code / via API, a skill template, best practices).

## How we tested it

**Evidence:** REVIEW

Source-grounded inspection only — no install or execution. We pulled metadata, recent commit dates, the full README, and the repo's top-level directory listing via the GitHub API, then counted entries and read the explanatory sections.

```
gh api repos/ComposioHQ/awesome-claude-skills --jq '{desc,stars:.stargazers_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'
gh api repos/ComposioHQ/awesome-claude-skills/commits --jq '.[0].commit.committer.date'
gh api repos/ComposioHQ/awesome-claude-skills/readme --jq '.content' | base64 -d | grep -cE '^\s*-\s+\['
gh api repos/ComposioHQ/awesome-claude-skills/contents --jq '.[].name'
```

## What worked

- **Best explanatory prose of any list in this space.** The Skills-vs-MCP-vs-tools section and the progressive-disclosure walkthrough are genuinely educational, not boilerplate. A newcomer learns the model here.
- **Clean task-domain taxonomy.** Ten use-case sections (legal, marketing, security, assistive tech, etc.) make it browsable by *what you want to do* rather than by tool type — complementary to our catalog's tool/skill/plugin axis.
- **Hand-written, attributed annotations.** Each entry has a one-line description and an author credit, giving more signal than a bare tagline.
- **Reach beyond Claude.** Explicitly positions skills as portable across Codex, Cursor, Gemini CLI, Antigravity, Windsurf — useful framing for a multi-agent shop.
- **Recently maintained.** Last commit 2026-05-22 with a steady commit cadence through April–May; the freshest of the awesome-lists currently in the catalog.

## What didn't work or surprised us

- **"1000+" is marketing, not the README count.** The description claims "1000+ production ready" skills; the README actually lists ~195 curated entries and the repo bundles ~30 skills. The big number presumably counts Composio's 500+ connected apps, which is a different thing.
- **Heavy vendor self-promotion.** The README opens with a Composio banner, a "Connect Claude to 500+ Apps" quickstart pushing the `connect-apps` plugin (requires a Composio API key), and repeated affiliate CTAs. The list is good, but it exists partly to funnel users to Composio's product.
- **No license file.** Apache-2.0 badge in the README but `license: null` from the API — no `LICENSE` in the repo. Technically unlicensed.
- **Heavy overlap with siblings.** Many top entries (anthropics docx/pdf/pptx/xlsx, superpowers, artifacts-builder) are the same ones VoltAgent, travisvn, and buildwithclaude already list. Its distinguishing value is the prose and the domain taxonomy, not unique entries.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Reference list — no direct effect on code quality |
| Speed | + | Domain-organized list + clear explainer speeds both learning and tool-finding |
| Maintainability | neutral | No impact on code |
| Safety | neutral | No activity/dead-link tracking; vendor CTAs require handing an API key to a third party |
| Cost Efficiency | + | Browse-by-use-case taxonomy and annotations cut scanning time |

## Verdict

**CONDITIONAL**

The clearest explainer and the cleanest use-case taxonomy in the awesome-Skills space, and the most recently maintained — worth pointing newcomers at to *understand* Skills and to browse by task domain. But the inflated "1000+" claim, pervasive Composio self-promotion, missing license, and heavy entry overlap with VoltAgent/travisvn/buildwithclaude keep it from ADOPT. Use it for its prose and taxonomy; rely on the editorial-quality lists (awesome-claude-code) and the existing siblings for breadth. Pick one general Skills list to track — this one earns its place mainly on freshness and explanation quality.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [awesome-claude-skills (Composio)](https://github.com/ComposioHQ/awesome-claude-skills) | reference | Vendor-curated, use-case-organized Claude Skills list with a strong Skills explainer (65K stars) | Hard to learn the Skills model and find skills by task domain | awesome-claude-skills (travisvn), awesome-agent-skills (VoltAgent), awesome-agent-skills (libukai), awesome-claude-code, buildwithclaude |
