# Evaluation: arrow-js

**Repo:** [standardagents/arrow-js](https://github.com/standardagents/arrow-js)
**Stars:** 3,666 | **Last updated:** 2026-04-01 (pushed; created 2022-11-08) | **License:** MIT
**Dev loop stage:** Implement — it is a UI runtime/library you build *with*, not a workflow that drives the loop. Its agent-relevant hooks (the `@arrow-js/skill` installer, the QuickJS sandbox) touch Plan/Implement and Safety, but the artifact is application code.
**Layer:** Infrastructure (a published npm runtime — `@arrow-js/core` and a monorepo of framework/SSR/hydrate/sandbox/compiler packages — that ships inside the product, not into the agent's config).

---

## What it does

ArrowJS bills itself as "the UI framework for coding agents": a tiny, type-safe reactive UI runtime built on platform primitives that LLMs already know cold — JavaScript modules, tagged template literals, and the DOM. The core (`@arrow-js/core`, v1.0.6, "Reactivity without the framework") gives you `reactive()` state, `html` tagged-template rendering, `component()`, and `nextTick()` with no build step (it imports directly from `esm.sh`). The monorepo layers optional packages on the same component model: `@arrow-js/framework` (async components, boundaries), `@arrow-js/ssr` (`renderToString`, payload serialization), `@arrow-js/hydrate` (adopt SSR HTML on the client), `@arrow-js/vite-plugin-arrow`, a `compiler`, a `highlight`/VSCode syntax package, and `create-arrow-js` for scaffolding a Vite 8 app.

Two pieces make the "for coding agents" claim more than a tagline. **`@arrow-js/sandbox`** runs user- or agent-authored Arrow code inside an async **QuickJS/WASM VM**, rendering through trusted host DOM code — so untrusted/generated code never executes in the page's `window` realm (it ships AST preprocessing for implicit imports, a sandbox-specific core shim, and a delegated event bridge). **`@arrow-js/skill`** (`npx @arrow-js/skill@latest`) installs an Arrow coding-agent skill for Claude Code or Codex, wiring local references, examples, and project guidance so an agent follows Arrow conventions. The repo is agent-friendly throughout: top-level `AGENTS.md` and `docs/AGENTS.md`, non-interactive release automation, `.dmux-hooks/` worktree hooks, and a `js-framework-benchmark` harness backing the "blazing-fast" claim.

## How we tested it

**Source-grounded inspection — not installed, not run.** Nothing was `npm install`-ed, no app was scaffolded, no sandbox executed, and the `@arrow-js/skill` installer was not invoked. Claims come from the README, the recursive file tree, the per-package `README.md`/`package.json` (e.g. `@arrow-js/sandbox`, `@arrow-js/skill`, `@arrow-js/core`), and `AGENTS.md` — not from observed runtime, bundle-size, or benchmark numbers. The "tiny / blazing-fast / type-safe" language is the authors' framing and the `bench/` harness their own; no independent measurement was taken here.

```bash
gh api repos/standardagents/arrow-js --jq '{desc:.description,stars:.stargazers_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'
gh api repos/standardagents/arrow-js/readme --jq '.content' | base64 -d
gh api "repos/standardagents/arrow-js/git/trees/HEAD?recursive=1" --jq '.tree[].path'   # packages/{core,sandbox,skill,framework,ssr,hydrate,compiler,...}
gh api repos/standardagents/arrow-js/contents/packages/sandbox/README.md --jq '.content' | base64 -d  # QuickJS/WASM realm isolation
gh api repos/standardagents/arrow-js/contents/AGENTS.md --jq '.content' | base64 -d     # agent automation guide
```

## What worked

- **The thesis is genuinely sharp for agent-written code.** Template literals + plain modules + direct DOM is exactly the surface LLMs generate most reliably — no JSX transform, no opaque compiler step, no large framework API to hallucinate. "Platform primitives the model already understands" is a real ergonomic advantage, not just marketing.
- **The sandbox is the standout, and it's the right primitive.** A QuickJS/WASM VM that runs untrusted/agent-generated UI code off the host `window` realm while still rendering real DOM is a concrete safety mechanism — directly relevant to the "agent writes code, then we run it" risk that most UI frameworks ignore entirely.
- **Clean layering.** Core stays DOM-first and framework-agnostic; async/SSR/hydrate are opt-in on the same `component()` model. You can adopt just the runtime or the full stack without rewriting components.
- **Agent integration is first-class, not bolted on.** `@arrow-js/skill` installs conventions/examples into Claude Code or Codex, `AGENTS.md` documents non-interactive release flows, and `.dmux-hooks/` supports worktree-based parallel agent work.
- **Real package, real CI.** npm-published with version/size/test badges, Vitest + Playwright e2e, trusted-publishing workflow, 7 releases. A maintained 2022-era project repositioned for the agent era, not a weekend demo.

## What didn't work or surprised us

- **It is a UI framework, not an agent tool — odd fit for this catalog.** Most catalog entries move dev-loop quality signals across *any* project; ArrowJS only matters if you are building a web UI *in ArrowJS*. Its catalog value is narrow and conditional on tech-stack choice.
- **Adoption bet against incumbents.** "Coding agents understand it better" is plausible but unproven; React/Svelte/Solid have vastly more training data and ecosystem. Choosing Arrow for agent-friendliness trades a massive corpus advantage for a cleaner primitive — a real risk for agent-generated code, the opposite of the pitch.
- **3.6K stars over a 2022→2026 span** signals a niche, slow-burn project recently re-pitched for agents (last push 2026-04-01), not a movement. Small ecosystem, few third-party components.
- **Sandbox ≠ host safety.** QuickJS/WASM isolates the *rendering realm*, not your machine; it doesn't sandbox an agent's filesystem/network tool calls. It mitigates "run this generated UI snippet safely," not "let an agent run arbitrary commands."
- **"For coding agents" is partly aspirational.** The strongest agent-specific assets (skill installer, sandbox) are thin relative to the framework itself; strip them and it reads as a lean reactive UI library with good agent ergonomics.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + / neutral | Template-literal + DOM primitives reduce the surface an agent can get wrong (no JSX/compiler quirks); offset by far less training data than React/Svelte. |
| Speed | + | No build step for core, direct ESM import, and a self-reported `js-framework-benchmark` harness backing "blazing-fast" rendering (unverified here). |
| Maintainability | + / neutral | Small API and clean core/framework/SSR layering keep app code legible; niche ecosystem means fewer off-the-shelf parts. |
| Safety | + | `@arrow-js/sandbox` runs untrusted/agent-generated UI in a QuickJS/WASM VM off the host `window` realm — concrete realm isolation for generated code. |
| Cost Efficiency | + / neutral | Tiny runtime + primitives the model already knows means fewer tokens spent explaining framework idioms; marginal at the catalog level. |

## Verdict

**CONDITIONAL — adopt only if you are building a web UI and want agent-generated frontend code to run in a sandbox.** ArrowJS is a well-engineered, genuinely thoughtful reactive UI runtime whose "primitives the model understands" thesis and QuickJS/WASM sandbox are real, differentiated ideas for the agent era. But it is application *infrastructure*, not a dev-loop tool: it only earns its place when your stack is (or could be) ArrowJS, and the bet that agents code it better than React is unproven against the incumbents' training-data advantage. Worth a catalog entry as a reference example of agent-first UI design and for its sandbox primitive — not a default recommendation.

Compared to neighbors: it sits oddly among Agent Orchestration entries. **LangGraph** and **sandcastle** orchestrate *agents*; ArrowJS orchestrates *DOM updates* — the only true overlap is the sandbox concept, where ArrowJS isolates a *rendering realm* while sandcastle/forkd isolate whole *agent processes* (microVMs/containers). They solve different layers of the same "run generated code safely" problem. The existing catalog row already (correctly) flags no real peer ("Overlaps with: —"); the closest conceptual cousin is **sandcastle** on the sandbox axis only.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [arrow-js](https://github.com/standardagents/arrow-js) | framework | Tiny reactive UI runtime pitched "for coding agents" (template literals + DOM + modules), with a QuickJS/WASM sandbox to run agent-generated UI off the host realm | Need a UI framework whose primitives an LLM gets right, plus realm-isolated execution of agent-written frontend code | sandcastle (sandbox/realm isolation only); otherwise no direct peer (it is a UI runtime, not an agent tool) |
