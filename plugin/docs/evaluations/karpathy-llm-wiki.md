# Evaluation: karpathy-llm-wiki

**Repo:** [Astro-Han/karpathy-llm-wiki](https://github.com/Astro-Han/karpathy-llm-wiki)
**Stars:** 1,164 | **Last updated:** 2026-04-13 (pushed; created 2026-04-05; updated 2026-06-19) | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Plan (knowledge layer — feeds research/design with a durable, citable knowledge base); touches Reflect (compounding knowledge over time)
**Layer:** Process / Tooling (a portable Agent Skill that drives an agent-maintained markdown knowledge base; no server, no infrastructure)

---

## What it does

The catalog one-liner: "Agent Skills-compatible LLM wiki — build knowledge bases from raw sources with citations." It packages [Karpathy's LLM Wiki idea](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) as a single installable [Agent Skills](https://agentskills.io) skill (one `SKILL.md` plus four markdown templates under `references/`).

The mechanism is a prompt-defined workflow over plain markdown — there is no code, no MCP server, no embeddings. The skill instructs the agent to maintain two directories: `raw/` (immutable ingested source material, dated) and `wiki/` (durable, LLM-compiled knowledge pages, plus a global `index.md` table of contents and an append-only `log.md`). It exposes three operations the agent runs in natural language:

- **Ingest** — collect a URL/file/pasted text into `raw/`, then compile or update the relevant `wiki/` pages, strengthening cross-references and recording contradictions.
- **Query** — search the wiki and answer with citations linking back to the markdown pages (not to raw chunks).
- **Lint** — check index integrity, broken links, missing index entries, and stale cross-references; auto-fix where possible.

The explicit contrast it draws is "LLM Wiki vs RAG": RAG retrieves raw chunks at query time; this approach front-loads synthesis at ingest time into curated, human-readable pages that compound over time. So it is a *general* knowledge-base-builder mechanism, not a fixed corpus — you point it at whatever sources you choose. Installs cross-tool via `npx add-skill Astro-Han/karpathy-llm-wiki` (Claude Code, Cursor, OpenCode) or by copying `SKILL.md` (Codex).

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** The skill was not installed via `add-skill`, no wiki was ingested, no query or lint was executed, so every claim below is from the repository (GitHub metadata, README, full file tree, templates, maturity counts), not from observed tool output. No metrics below are invented; the "94 articles / 99 sources" figures are the author's self-reported numbers from the README, not anything I measured.

```bash
gh api repos/Astro-Han/karpathy-llm-wiki
gh api repos/Astro-Han/karpathy-llm-wiki/readme --jq '.content' | base64 -d
gh api "repos/Astro-Han/karpathy-llm-wiki/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api repos/Astro-Han/karpathy-llm-wiki/commits --jq 'length'        # 14
gh api repos/Astro-Han/karpathy-llm-wiki/contributors --jq '[.[].login]'  # single author
gh api repos/Astro-Han/karpathy-llm-wiki/releases --jq 'length'       # 0
```

## What worked

- **General mechanism, not a fixed book.** Unlike single-source knowledge tools (gentleman-book-mcp serves one author's book), this builds a wiki from *whatever sources you choose* — papers, blog posts, PDFs, pasted text. The marginal value scales with the knowledge you actually lack, which is exactly where a knowledge layer earns its keep.
- **Zero-infrastructure, fully portable.** No server, no embeddings, no API keys, no build step. The entire skill is one `SKILL.md` plus four markdown templates; the output is plain markdown you own in your own repo. Cross-tool by design (Agent Skills standard: Claude Code, Cursor, Codex, OpenCode).
- **Citations and lint address real failure modes.** Query answers cite back to wiki pages, and the lint operation targets index integrity and broken/stale cross-references — directly relevant to Correctness (grounded answers) and Maintainability (the knowledge base doesn't rot silently).
- **Compounding-knowledge model fits Reflect.** Synthesis at ingest time into durable pages, with an append-only `log.md` and recorded contradictions, is a sound design for knowledge that improves across sessions rather than being re-derived each query.
- **Clear, honest README.** Includes a design spec (`SKILL.md`), templates, worked examples (`examples/`), and an explicit RAG comparison. Notably credits prior community implementations rather than claiming originality.
- **Reasonable traction:** 1,164 stars / 151 forks, MIT-licensed, with open issues/discussions enabled.

## What didn't work or surprised us

- **It is a workflow, not a tool — outcomes depend on the driving model.** There is no code enforcing the rules; the skill is a set of prompts. Quality of compilation, citation discipline, and lint fidelity all rest on the agent following `SKILL.md` faithfully. There is nothing deterministic to verify it does so.
- **Self-reported production claims are unverifiable.** "94 articles / 99 sources maintained daily since April 2026" is the author's own knowledge base, not shipped in the repo and not independently checkable. Treat as anecdote, not benchmark.
- **Low maturity by code-project standards.** Single author, 14 commits, 0 releases/tags, last pushed 2026-04-13 (a ~1-week burst in early April), no tests (there is no code to test). High star count relative to a very thin, young artifact — popularity is driven by the Karpathy association more than by demonstrated longevity.
- **Crowded space, explicitly acknowledged.** The README itself links two sibling implementations (`lucasastorian/llmwiki`, `atomicmemory/llm-wiki-compiler`). This is one of several near-identical takes on the same gist; no clear moat beyond packaging it as a clean Agent Skill.
- **Content licensing shifts to the user.** The skill is MIT, but *you* ingest the sources, so redistribution/IP responsibility for ingested material is yours. Less of a flag than tools that ship someone else's content, but worth noting for teams with IP discipline.
- **Overlaps with existing memory/context tooling.** For many teams an agent-maintained markdown knowledge base competes with already-installed memory systems (e.g. OMEGA-style persistent memory) or simple `docs/`-in-repo conventions.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Answers cite curated wiki pages rather than re-derived chunks; contradictions are explicitly recorded at ingest — grounding reduces hallucination on domain knowledge you've ingested. |
| Speed | + / neutral | Front-loads synthesis at ingest so repeated questions are answered from durable pages instead of re-researching; offsetting cost is the upfront ingest/maintenance effort. |
| Maintainability | + | Plain markdown you own, with a lint operation for index/link integrity and an append-only log — the knowledge base is human-readable and degrades visibly, not silently. |
| Safety | neutral | No server, no network access, no system/DB reach — pure file authoring. IP responsibility for ingested sources moves to the user. |
| Cost Efficiency | neutral / + | No infra or API cost beyond the agent's own tokens; ingest spends tokens once, then cheap cited lookups. Token spend grows with wiki size at query time. |

## Verdict

**CONDITIONAL** — adopt when you have a *recurring, evolving* knowledge domain the base model doesn't already know well (a specific codebase's history, a fast-moving library, an internal research corpus) and you want durable, citable, version-controlled knowledge in your own repo. Skip it for one-off questions or for knowledge frontier models already hold.

karpathy-llm-wiki is the strongest of this catalog's single-purpose knowledge-layer cluster precisely because it is *general*: it is a zero-infrastructure, portable Agent Skill that turns any sources you choose into a compounding, cited markdown wiki, rather than a server bolted to one fixed book. That generality, plus citations and a lint operation, is what lets it move Correctness and Maintainability on knowledge you actually lack. The caveats are that it is a *workflow, not a tool* — there is no code, so results depend entirely on the driving model following the spec — and that maturity is thin (single author, 14 commits, 0 releases, a ~1-week build) with self-reported production stats that can't be verified.

Compared to neighbors: **gentleman-book-mcp (SKIP)** serves one author's book and earns SKIP because that content is mainstream and already in training data; **book-to-skill** and **andrej-karpathy-skills** are likewise narrower (turn a specific book into a skill / a fixed set of Karpathy-derived skills). karpathy-llm-wiki sits above them because the corpus is *yours*. But it is not an ADOPT-everywhere: it competes with existing memory systems and plain `docs/` conventions, and for many projects the base model plus a couple of pinned reference docs is enough. Adopt deliberately for the evolving-corpus case; otherwise the lighter-weight option wins.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [karpathy-llm-wiki](https://github.com/Astro-Han/karpathy-llm-wiki) | skill | Agent Skill that has the agent compile raw sources into a durable, cited markdown wiki (ingest/query/lint); zero infra, cross-tool | Want a compounding, citable, version-controlled knowledge base over your own evolving sources instead of re-researching or RAG-chunking each query | andrej-karpathy-skills, gentleman-book-mcp, book-to-skill (all narrower / single-source) |
