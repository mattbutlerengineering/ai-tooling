# Evaluation: Flowise

**Repo:** [FlowiseAI/Flowise](https://github.com/FlowiseAI/Flowise)
**Stars:** 53,727 | **Last updated:** 2026-06-16 (pushed; created 2023-03-31) | **License:** Apache-2.0 with Commons Clause (reported as NOASSERTION / "Other" by the GitHub license API)
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** *Builds the product, not the loop.* Maps loosely to Implement — but the artifact you implement is an end-user LLM *application* (chatbot, RAG pipeline, agent workflow), not your own codebase. It does not write, review, test, or ship the code in your repo; it is a destination you build apps in, adjacent to the dev loop this catalog optimizes.
**Layer:** Infrastructure (a self-hostable Node/React monorepo app + visual builder) with a managed cloud option

---

## What it does

The catalog one-liner: "Build AI agents visually with drag-and-drop." Flowise is a mature **low-code / no-code visual agent builder** — you wire LLM nodes, retrievers, tools, and an "agentflow" canvas together in a browser UI to produce deployable chat assistants, RAG pipelines, and multi-step agent workflows, then expose them via API/embed. Install is `npm install -g flowise && npx flowise start` (then `localhost:3000`) or Docker Compose; there is also a hosted **Flowise Cloud**. The repo is a pnpm/turbo monorepo with `packages/` for `server` (Express API), `ui` (React frontend), `components` (third-party node integrations), `agentflow`, `observe`, and auto-generated swagger `api-documentation`.

This is a heavyweight, widely adopted end-user platform: 53.7K stars, ~24.5K forks, an i18n'd README (EN/TW/ZH/JA/KR), `SECURITY.md`, `CODE_OF_CONDUCT.md`, changesets, artillery load-test config, and a metrics directory. It is a direct peer of **dify** (production agentic-workflow platform) and **LangGraph** (the code-first graph framework Flowise is the visual analog of). The value proposition is *democratization*: build and ship LLM apps without writing orchestration code.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** Flowise was not installed, no `flowise start` was executed, no Docker stack was brought up, and no flow was built on the canvas or in Flowise Cloud. Every claim comes from the repository (GitHub metadata, README, top-level tree, `packages/` listing, release/contributor counts, license API) — not from hands-on use of the builder. We did not evaluate the UX of the canvas, runtime performance, or generated-app quality; the "build visually" experience is the project's framing.

```bash
gh api repos/FlowiseAI/Flowise --jq '{desc,stars:.stargazers_count,forks:.forks_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id,lang:.language}'  # TypeScript, NOASSERTION, 53.7K stars, created 2023-03-31
gh api repos/FlowiseAI/Flowise/license --jq '.license.name, .license.spdx_id'   # "Other" / NOASSERTION (Apache-2.0 + Commons Clause)
gh api repos/FlowiseAI/Flowise/readme --jq '.content' | base64 -d | head -120
gh api "repos/FlowiseAI/Flowise/git/trees/HEAD" --jq '.tree[].path'   # monorepo: packages/, docker/, turbo.json, pnpm-workspace.yaml
gh api repos/FlowiseAI/Flowise/contents/packages --jq '.[].name'      # agentflow, api-documentation, components, observe, server, ui
gh api repos/FlowiseAI/Flowise/releases  --jq 'length'   # 30 (page-1 cap; long, active release history)
gh api repos/FlowiseAI/Flowise/contributors --jq 'length'  # 30 (page-1 cap; large contributor base)
```

## What worked

- **Genuine maturity and adoption.** 53.7K stars, ~24.5K forks, three years of active development (created 2023-03-31), a long release history, SECURITY policy, load-test config, and a clean pnpm/turbo monorepo with separated server/ui/components packages. This is a battle-tested platform, not a weekend project.
- **Real democratization value.** For non-engineers (or engineers prototyping fast), the drag-and-drop canvas genuinely lets you assemble a RAG pipeline or agent workflow and expose it as an API in minutes — no orchestration code to write or maintain.
- **Broad integration surface and deployment options.** The `components` package carries many third-party node integrations; you can self-host (npm or Docker Compose) or use Flowise Cloud, and ship flows via API/embed. Flexible for both POCs and production hosting.
- **Healthy operational signals.** Auto-generated swagger API docs, observability package (`observe`), changesets-based releases, and i18n suggest a team that runs this as a product, not a demo.

## What didn't work or surprised us

- **It builds the app, not the dev loop.** This catalog optimizes the *software-development* loop — writing, reviewing, testing, shipping code in a repo. Flowise produces a different artifact: an end-user LLM application. It does not improve how you write your own code; it is where you'd build a chatbot. The relevance to "AI-assisted development that produces high-quality code" is indirect.
- **Visual flows resist the engineering practices this catalog values.** Drag-and-drop canvases are hard to diff, code-review, unit-test, and version meaningfully. For anything beyond a prototype, a code-first framework (LangGraph) gives you the Git/test/review discipline that visual flows obscure — the opposite of where this catalog's quality signals point.
- **License is not plain OSS.** GitHub reports the license as "Other"/NOASSERTION — Flowise uses Apache-2.0 **with a Commons Clause** restricting commercial resale of the software as a hosted service. Fine for internal/self-host use, but it is not unencumbered Apache-2.0; teams must read the terms before building a commercial product on it.
- **Heavyweight to self-host.** A full Node monorepo (server + React UI + components) plus a datastore is real infrastructure to run and maintain — a large footprint relative to the inner-loop CLI tools that dominate this catalog.
- **Overlaps heavily with dify and LangGraph already in the catalog.** It adds breadth to the "visual agent platform" cluster but little that dify (production-scale visual workflows) and LangGraph (code-first graphs) don't already cover.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Correctness of a *built app* depends on the flow you design and the models you wire in; the platform neither improves nor measures the correctness of code in your own repo. |
| Speed | + | Fast time-to-prototype for an LLM app — assemble RAG/agent flows on a canvas in minutes vs. writing orchestration code. This is speed-of-product-build, not speed of your dev loop. |
| Maintainability | − | Visual flows are hard to diff, code-review, and unit-test; beyond prototypes the canvas becomes a maintenance liability compared to versioned, testable code (LangGraph). |
| Safety | neutral / − | Self-hostable with a SECURITY policy and credential handling, but standard LLM-app risks (prompt injection, tool/data exposure) apply, and the Commons-Clause license adds a legal constraint, not a safety one. |
| Cost Efficiency | neutral | No bearing on the token/effort cost of *your* development; running the platform adds infra cost, while it can lower the build cost of a one-off LLM app. |

## Verdict

**SKIP for this catalog's purpose (keep as a reference entry) — it is an excellent product in the wrong loop.** Flowise is a mature, widely adopted, well-engineered visual agent-building platform, and for shipping an LLM *application* without writing orchestration code it is a legitimate choice alongside dify. But this catalog is an operating manual for AI-assisted *software development* — improving how high-quality code gets written, reviewed, tested, and shipped. Flowise builds a different artifact (the end-user app) and, with its hard-to-diff visual flows, actively cuts against the engineering discipline (versioning, review, testing) the catalog's quality signals reward. It earns a catalog entry as a known platform, but it is not a tool to adopt into the dev loop.

Compared to neighbors: **dify** is the closer and arguably more production-hardened peer in the same visual-workflow lane — if you want this kind of platform, evaluate them head-to-head. **LangGraph** is the code-first inverse: less accessible but Git/test/review-friendly, which makes it the better fit when the workflow must live inside a real engineering process. Flowise wins on accessibility and prototyping speed; it loses on everything that makes a workflow a maintainable software asset.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Flowise](https://github.com/FlowiseAI/Flowise) | platform | Build LLM apps and agent workflows visually with drag-and-drop; self-host (Node monorepo) or Flowise Cloud | Want to compose RAG/agent workflows and ship them as APIs without writing orchestration code | LangGraph (code-first inverse), dify (production-scale visual peer) |
