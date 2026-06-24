# Generative-UI frameworks: a landscape evaluation

**Evidence:** REVIEW
**Last verified:** 2026-06-24
**Dev loop stage:** Implement (building agent-facing UIs)
**Layer:** Tooling / Reference

A comparative survey of the **generative-UI** framework landscape, in response to issue #127.
"Generative UI" means AI/LLM systems that *produce or drive user-interface output dynamically*
— rendering real components from model output, streaming agent state into a UI, or emitting a
structured renderable UI spec — as opposed to plain chat text.

## How we evaluated

**Source-grounded — not run hands-on.** Each framework was assessed from its GitHub repo,
README, and docs; repo metadata (stars, license, last activity, archived status) was verified
live via the GitHub API on 2026-06-24. No framework was installed or built against here — a
hands-on MEASURED eval would mean building a React/Angular app per framework, which is out of
scope for this landscape pass (and several would hit an external-code-execution gate). Verdicts
here are therefore REVIEW-strength: a map of the space and how the pieces differ, not a
benchmarked head-to-head. License classifications were read from the actual `LICENSE` file where
GitHub's SPDX field said `NOASSERTION` (it mislabels some permissive licenses).

## The four approaches

Generative UI is not one technique. The frameworks cluster into four distinct approaches, and
the right pick depends on which one you need — they compose more than they compete.

### A. Server-driven / prop-streaming (model output → typed components)

The model's tool call decides *which* pre-built component renders; props stream in as it runs.
The LLM never emits markup — it selects from components you registered. The dominant approach.

- [vercel-ai](https://github.com/vercel/ai) (framework, Apache-2.0, ★25K) — `streamUI()` streams React Server Components from tool calls. The default for Next.js apps.
- [tambo](https://github.com/tambo-ai/tambo) (framework, MIT, ★11K) — register components with Zod schemas; the agent picks one and streams its props. Fullstack React SDK + backend.
- [assistant-ui](https://github.com/assistant-ui/assistant-ui) (framework, MIT, ★11K) — React chat primitives that render tool calls/JSON as live components, with inline human-in-the-loop approvals and frontend tools.
- [hashbrown](https://github.com/liveloveapp/hashbrown) (framework, MIT, ★0.7K) — the LLM picks and streams your exposed components; **the only option that natively covers Angular** as well as React.
- [CopilotKit](https://github.com/CopilotKit/CopilotKit) (framework, MIT, ★35K) — components bound to shared agent↔app state; renders generative UI over its AG-UI protocol.

### B. Interaction protocol (the wire format the others ride on)

A transport-agnostic event format the agent emits (state/text/tool deltas) and any frontend
consumes. Not a renderer itself — the substrate the component frameworks build on.

- [ag-ui](https://github.com/ag-ui-protocol/ag-ui) (reference/protocol, MIT, ★14K, by CopilotKit) — the Agent-User Interaction Protocol; `npx create-ag-ui-app`, framework integrations, a "Dojo".

### C. Declarative UI-spec emitter (model returns a serialized UI document)

The model produces a structured, framework-agnostic UI description (JSON/JSONL/tag-based) that
an SDK renders into native components — portable across frontends, at the cost of a fixed
component vocabulary.

- [a2ui](https://github.com/a2ui-project/a2ui) (reference/spec, Apache-2.0, ★15K) — from the **Gemini / Flutter-GenUI** ecosystem; agents emit streaming JSONL UI documents rendered platform-agnostically.
- [openui](https://github.com/thesysdev/openui) (reference, MIT, ★7K) — the Crayon SDK; the LLM streams a UI representation the React SDK converts to components ("open standard for generative UI").
- [MCP Apps (ext-apps)](https://github.com/modelcontextprotocol/ext-apps) (reference/spec, ★2K) — MCP servers serve interactive UI embedded inside AI chat hosts (ChatGPT/Claude).
- [OpenGenerativeUI](https://github.com/CopilotKit/OpenGenerativeUI) (framework, MIT, ★1K, by CopilotKit) — renders model-produced UI as interactive components in **sandboxed iframes**, with theming and progressive reveal; the isolation answer for untrusted model output.

### D. Streaming output renderers (presentation, not generation)

These smooth LLM token streams and render custom block types, but the model does *not* choose
components — closer to rich chat formatting than true generative UI. Real and useful, but a tier
below the above for this purpose, so they are noted here rather than catalogued:
[llm-ui](https://github.com/richardgill/llm-ui) (MIT, ★2K) and
[run-llama/chat-ui](https://github.com/run-llama/chat-ui) (MIT, ★0.6K).

## Choosing one

- **Next.js / React app, want the path of least resistance** → vercel-ai (`streamUI`).
- **Register your own design-system components for the agent to drive** → tambo or assistant-ui (assistant-ui if chat + HITL approvals are central; tambo for schema-first component selection).
- **Angular** → hashbrown (effectively the only native option).
- **Cross-framework / vendor-neutral standard, not tied to React** → a2ui (Gemini-ecosystem) or openui/Crayon; MCP Apps if your UI ships *from* an MCP server into a host.
- **Rendering untrusted model-generated UI safely** → OpenGenerativeUI (iframe sandboxing).
- **Building the transport layer / integrating multiple frontends** → ag-ui as the protocol underneath.

These layer: ag-ui (B) can carry a2ui/openui specs (C) into a component framework (A). Stacking
two *component* frameworks (A) in one app is the redundant case to avoid.

## Caveats and exclusions

- **OpenUI name collision.** Our catalog's [openui](https://github.com/thesysdev/openui) (thesysdev, ★7K, the Crayon SDK) is a *different project* from [wandb/openui](https://github.com/wandb/openui) (★22K), a describe-UI-in-natural-language **component generator** (a v0-style design tool, not a runtime gen-UI framework). They share a name only.
- **Proprietary, excluded as catalog candidates:** Vercel **v0** (v0.dev, no source) and Thesys **C1** (hosted API; the open piece is `thesysdev/openui`). Mentioned for context only.
- **License-disqualified:** `nlkitai/nlux` ships a modified MPL-2.0 with AI-training/translation restrictions — fails the permissive bar; excluded.
- **Stale / too thin to catalog:** `zerodays/react-native-gen-ui` (last push 2024) and `eylonmiz/react-agent` (code-gen, not runtime gen-UI; stale); `mdocui/mdocui` is on-thesis but ~36 stars — watch, not catalogued.
- **Evidence:** this is a REVIEW-strength survey. Graduating any single framework to a MEASURED eval (build a small app, stream a component) is a sensible follow-up if one becomes a stack candidate.
