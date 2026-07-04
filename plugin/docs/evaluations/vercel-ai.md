# Evaluation: vercel-ai (AI SDK)

**Repo:** [vercel/ai](https://github.com/vercel/ai)
**Stars:** 24,995 | **Last updated:** 2026-06-19 (pushed; created 2023-05-23) | **License:** NOASSERTION (Apache-2.0 per package manifests; GitHub couldn't resolve a single SPDX for the monorepo)
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Mostly off-loop (an SDK for building LLM apps), with one genuine bridge into Implement: it ships an installable coding-agent skill and a `ToolLoopAgent` primitive people use to *build* coding harnesses.
**Layer:** Infrastructure — a provider-agnostic TypeScript toolkit (`ai`, `@ai-sdk/*`) imported into product code, plus UI hooks (`@ai-sdk/react`) and a Vercel AI Gateway path.

---

## What it does

The AI SDK is "a provider-agnostic TypeScript toolkit designed to help you build AI-powered applications and agents" across Next.js, React, Svelte, Vue, Angular, and Node. Its core is a **unified provider API**: `generateText({ model: 'anthropic/claude-opus-4.6', prompt })` routes through the Vercel AI Gateway by default, or you install `@ai-sdk/anthropic` / `@ai-sdk/openai` / `@ai-sdk/google` and call providers directly. On top of that sit structured-output helpers (`Output.object` with Zod schemas), an agent primitive (`ToolLoopAgent`), and **AI SDK UI** — framework-agnostic hooks (`useChat` via `@ai-sdk/react`) for streaming chatbots and generative UI.

Like LangChain, the primary purpose is building the LLM *application* you ship — a chatbot, a generative-UI feature, a tool-using product agent. The README's worked example builds an image-generation agent wired through a Next.js App Router route and a React tool-invocation view. That is app engineering, not dev-loop tooling.

**The dev-loop bridge — and it is real.** The README explicitly states: "If you use coding agents such as Claude Code or Cursor, we highly recommend adding the AI SDK skill to your repository: `npx skills add vercel/ai`." The repo ships a `.agents/skills` directory for exactly this. That makes the AI SDK *also* a SKILL.md publisher in the vercel-labs/skills ecosystem — it teaches your coding agent how to use the SDK correctly. Separately, `ToolLoopAgent` plus `openai.tools.localShell` wired to a Vercel Sandbox is a documented pattern for *building a coding/shell agent* — i.e., constructing a harness. Both put one foot inside the Implement stage in a way LangChain does not.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No `npm install ai`, no agent built, no `npx skills add vercel/ai` executed, no provider called. Claims come from GitHub metadata, the README, and the file tree — not observed behavior. License is flagged NOASSERTION because the GitHub API couldn't derive one SPDX for the changeset-managed monorepo; package manifests are Apache-2.0 (not independently re-verified here).

```bash
gh api repos/vercel/ai --jq '{desc,stars:.stargazers_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'  # license: NOASSERTION
gh api repos/vercel/ai --jq '{forks:.forks_count,open_issues:.open_issues_count,topics:.topics}'  # 4630 forks, 1790 open issues
gh api repos/vercel/ai/readme --jq '.content' | base64 -d | head -180
gh api "repos/vercel/ai/git/trees/HEAD?recursive=0" --jq '.tree[].path'   # .agents/skills, .changeset/* (changesets monorepo)
gh api repos/vercel/ai/releases --jq 'length'             # 30 (page-1 cap; per-package releases are very frequent)
gh api repos/vercel/ai/releases/latest --jq '{tag,date:.published_at[0:10]}'  # @ai-sdk/vue@3.0.208, 2026-06-18
```

## What worked

- **Clean provider interoperability.** A single model string (`'anthropic/claude-opus-4.6'`, `'openai/gpt-5.4'`, `'google/gemini-3-flash'`) through the AI Gateway, or direct `@ai-sdk/*` packages — minimal-ceremony, TypeScript-native, with Zod-typed structured output. The least-friction way to call multiple providers from TS.
- **A real dev-loop foothold.** Shipping `npx skills add vercel/ai` means the project authors a coding-agent skill that improves how an agent writes AI-SDK code in *your* repo — a legitimate Implement-stage artifact, and exactly the kind of build-backed skill the catalog values (cf. vercel-labs/agent-skills).
- **Harness-construction primitive.** `ToolLoopAgent` + `localShell` + Vercel Sandbox is a documented recipe for building a sandboxed shell/coding agent — the SDK can be the substrate under a custom coding harness, not just a chatbot.
- **Very actively maintained, framework-broad.** Changesets monorepo, near-daily per-package releases (`@ai-sdk/vue@3.0.208`), UI hooks across React/Svelte/Vue/Angular. The 1,790 open issues track surface area, not neglect.

## What didn't work or surprised us

- **Still primarily an app-building SDK.** The center of gravity — `generateText`, `useChat`, generative UI, route handlers — is for building the LLM product you ship, which is the class the catalog SKIPs (LangChain.js, LangGraph, Flowise, dify). The dev-loop bridges are real but peripheral to the SDK's stated purpose.
- **The skill, not the SDK, is the catalog-relevant artifact.** The genuinely dev-loop-useful piece is `npx skills add vercel/ai` — and that flows through vercel-labs/skills (already cataloged). Adopting the *SDK* for your workflow only makes sense if you are building a custom harness on `ToolLoopAgent`; otherwise you want the skill, not the framework.
- **Gateway-default coupling.** `generateText` routes through the Vercel AI Gateway unless you wire providers directly — convenient, but a vendor path worth noting for cost/lock-in if used as harness substrate.
- **License ambiguity at the repo root.** GitHub reports NOASSERTION; the effective license lives in per-package manifests (Apache-2.0). Fine in practice, but not a clean single-SPDX repo.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + (via the skill) | `npx skills add vercel/ai` teaches a coding agent the correct AI-SDK APIs, reducing hallucinated/outdated SDK usage in your code. The SDK itself affects the *app's* correctness (off-loop). |
| Speed | + (harness builders) | `ToolLoopAgent` + sandbox is a fast path to a custom coding/shell agent; for everyone else, off-loop (speeds app-building, not your dev cycle). |
| Maintainability | neutral / n/a | Skill keeps SDK usage current; the framework's abstraction is a property of product code, not your workflow. |
| Safety | neutral | Harness pattern runs shell in a Vercel Sandbox (isolation is opt-in and explicit). As app code, no workflow-safety role. |
| Cost Efficiency | − / neutral | Gateway-default routing is a cost/lock-in consideration if used as harness substrate; otherwise off-loop. |

## Verdict

**CONDITIONAL — catalog it for the coding-agent skill and the harness-building primitive, not as a workflow SDK.** vercel/ai is, like LangChain, primarily a framework for building LLM applications — the class this catalog SKIPs. But it crosses the bar two of its skipped siblings don't: it ships an installable coding-agent skill (`npx skills add vercel/ai`) that improves Implement-stage code generation, and `ToolLoopAgent` is a documented substrate for *building a coding harness*. Adopt it only in those two cases: (a) you write AI-SDK code and want the agent skill, or (b) you are building a custom TS coding harness. As a general workflow tool it offers nothing; default users want the skill via vercel-labs/skills, not the framework.

Compared to neighbors: against **LangChain (Python)** — which we SKIP for having no dev-loop bridge — vercel/ai earns CONDITIONAL precisely because it has one (the skill + harness primitive). It parallels **fast-agent**, cataloged despite being an agent framework because it doubles as a runnable coding agent; vercel/ai's bridge is thinner (a skill + a primitive, not a ready coding agent), hence CONDITIONAL not ADOPT. For pure provider interoperability, **aisuite** is the minimal alternative. The skill itself lives in the **vercel-labs/skills** / **vercel-labs/agent-skills** orbit already in the catalog.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [vercel-ai](https://github.com/vercel/ai) | framework | Provider-agnostic TS toolkit for building LLM apps/agents (unified `generateText`, Zod output, UI hooks) — ships an installable `npx skills add vercel/ai` coding-agent skill and a `ToolLoopAgent` harness primitive | Building LLM applications in TS with swappable providers; secondarily, teaching coding agents correct AI-SDK usage and building custom sandboxed coding harnesses | LangChain.js, LangGraph.js, aisuite, fast-agent; vercel-labs/skills & vercel-labs/agent-skills (the skill path) |
