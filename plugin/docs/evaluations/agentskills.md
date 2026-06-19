# Evaluation: agentskills

**Repo:** [agentskills/agentskills](https://github.com/agentskills/agentskills)
**Stars:** 20,770 | **Last updated:** 2026-05-20 | **License:** Apache-2.0 (docs CC-BY-4.0)
**Dev loop stage:** Discover
**Layer:** Infrastructure

---

## What it does

The canonical open specification and documentation home for the Agent Skills format — the `SKILL.md` standard originally developed by Anthropic and released as an open standard now adopted across a growing set of agent products. A skill is a folder with a required `SKILL.md` (metadata: `name` + `description`, plus instructions) and optional `scripts/`, `references/`, and `assets/`. Agents load skills through three-stage progressive disclosure: discovery (name + description only, at startup), activation (full `SKILL.md` read when a task matches), and execution (follow instructions, optionally running bundled code or loading referenced files). This keeps many skills on hand at a small context cost.

The repo backs **agentskills.io**: the spec lives in `docs/specification.mdx`, with guides, a skill-creation walkthrough, client-implementation docs, and a Client Showcase listing skills-compatible tools. A `skills-ref/` directory holds a reference Python implementation (`pyproject.toml`, `src`, `tests`) of the loader/validator. It is the standard-and-docs reference that many ecosystem tools (e.g. karpathy-llm-wiki, the broader skills ecosystem) point at as the authority for the format — not a registry of installable skills itself and not an in-loop tool.

## How we tested it

Method: inspected the GitHub repo metadata, README, and file tree only via `gh api`. Did NOT clone the repo, run the `skills-ref` implementation, or browse agentskills.io. No hands-on usage is reported — observations are repo/README-sourced and noted as such.

```bash
gh api repos/agentskills/agentskills \
  --jq '{desc,stars:.stargazers_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'
gh api repos/agentskills/agentskills/git/trees/main --jq '.tree[].path'
gh api repos/agentskills/agentskills/contents/docs --jq '.[].name'
gh api repos/agentskills/agentskills/contents/skills-ref --jq '.[].name'
gh api repos/agentskills/agentskills/commits --jq '.[0].commit.committer.date'
```

Reviewed: repo description, license (Apache-2.0 code, CC-BY-4.0 docs), activity dates, the README (format definition, progressive-disclosure model, client showcase, contribution model), the `docs/` tree (`specification.mdx`, `skill-creation`, `client-implementation`, `clients.mdx`), and the `skills-ref/` reference-implementation layout.

## What worked

- **It is the spec, not a clone** — this is the authoritative, vendor-originated (Anthropic) open standard for `SKILL.md`, with a published specification and a reference implementation. For "what is the canonical skill format," this is the source of truth.
- **Clear, well-documented model** — the three-stage progressive-disclosure mechanism and the required/optional folder layout are documented precisely, which is exactly what you need when authoring portable skills.
- **Cross-tool portability is the whole point** — write a skill once, run it across any skills-compatible client (Client Showcase). That is real Discover-stage value: it tells you the format your skills must follow to be reusable.
- **Healthy governance signals** — Apache-2.0 / CC-BY-4.0, `CONTRIBUTING.md`, open-to-ecosystem development, 20K+ stars in ~6 months, and a reference implementation with tests.

## What didn't work or surprised us

- **Not exercised** — only metadata, README, and tree were inspected; the spec text and `skills-ref` validator were not run or read in full.
- **It is a spec/registry-of-clients, not a registry of skills** — unlike [skills.sh](https://skills.sh) or [buildwithclaude](https://github.com/davepoon/buildwithclaude), it does not let you browse or install community skills. To find actual skills you still go elsewhere (the README points to [anthropics/skills](https://github.com/anthropics/skills) for examples).
- **Slightly less fresh than the discovery hubs** — last commit 2026-05-20 (vs. daily activity on the directories); expected for a spec repo, but worth noting it is documentation cadence, not active tooling cadence.
- **Discovery value is indirect** — it answers "what format" and "which clients support it," not "which skill solves my task." Pair it with a discovery hub for the latter.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | A spec; correctness depends on the skills you write to it, not the standard |
| Speed | neutral | Reference/standard; no direct dev-loop speed effect |
| Maintainability | + | A stable, portable, version-controlled skill format improves long-term reuse across agents |
| Safety | neutral | Spec only; safety depends on the skills authored and the code they bundle |
| Cost Efficiency | + | Progressive disclosure keeps many skills loadable at small context cost — a real token efficiency for the format |

## Verdict

**ADOPT** (as the reference standard)

This is the authoritative open specification for `SKILL.md` — the format every skill in this catalog's ecosystem ultimately conforms to. Adopt it as the canonical reference for authoring portable skills: read `specification.mdx` and the skill-creation guide before writing or reviewing any skill. It is not a discovery registry, so it does not replace the hubs — it is upstream of them. Compared to [skills.sh](https://skills.sh) and [buildwithclaude](https://github.com/davepoon/buildwithclaude) (which help you *find and install* skills), agentskills tells you *what a skill is*; compared to [anthropics/skills](https://github.com/anthropics/skills) (canonical *examples*), this is the canonical *spec*. Keep all three: spec here, examples at anthropics/skills, discovery at the hubs.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agentskills](https://github.com/agentskills/agentskills) | reference | Canonical open specification for portable AI agent skills (SKILL.md format), with reference implementation and client showcase | No standard format for writing skills that work across agents and editors | anthropics/skills (examples), skills.sh, buildwithclaude (discovery) |
