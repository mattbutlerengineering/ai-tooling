# Evaluation: Google Antigravity SDK (Python)

**Repo:** [google-antigravity/antigravity-sdk-python](https://github.com/google-antigravity/antigravity-sdk-python)
**Stars:** 1,885 | **Last updated:** 2026-06-18 (pushed; created 2026-04-29) | **License:** Apache-2.0 | **Package:** PyPI `google-antigravity`
**Dev loop stage:** Implement (agent-building SDK / framework)
**Layer:** Infrastructure (SDK + compiled runtime binary)

---

## What it does

The Google Antigravity SDK is a **Python library for building AI agents powered by Google Antigravity and Gemini.** It provides a "secure, scalable, and stateful infrastructure layer that abstracts the agentic loop," so you write what your agent *does* rather than how it runs. Install is `pip install google-antigravity`; notably, the SDK **relies on a compiled runtime binary** shipped inside the platform-specific wheels — i.e. the agentic-loop runtime itself is closed, with the Python SDK as the open (Apache-2.0) surface.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No agent built, no runtime exercised. Behavior comes from the README and packaging notes, not observed usage. The dependence on a compiled runtime binary is taken from the README's own note.

```bash
gh api repos/google-antigravity/antigravity-sdk-python --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 1.9K, Apache-2.0
gh api repos/google-antigravity/antigravity-sdk-python/readme --jq '.content' | base64 -d | head -20   # Gemini/Antigravity agent SDK, abstracts agentic loop, compiled runtime
```

## What worked

- **First-party Google agent SDK.** For teams building on Gemini/Antigravity, an official, supported SDK with a stateful, managed agentic loop is the credible foundation versus rolling your own.
- **"Focus on what the agent does" abstraction.** Hiding the loop/state/scaling infrastructure behind an SDK is the right ergonomic for application agents.
- **Apache-2.0 SDK surface, actively maintained,** with quick traction (~1.9K stars).

## What didn't work or surprised us

- **Closed compiled runtime.** The Apache-2.0 license covers the SDK, but the actual agentic-loop runtime is a precompiled binary in the wheels — so it's not fully open/self-hostable, and you're coupled to Google's runtime and (implicitly) Gemini/Antigravity.
- **Ecosystem lock-in.** It's the Google-Antigravity-and-Gemini path; portability to other models/runtimes isn't the pitch (contrast model-agnostic harnesses in this catalog).
- **Tangential to the Claude-Code coding loop.** It's for *building* application agents on Google's stack, not improving an AI-assisted coding workflow — same class as the catalog's other agent frameworks (vercel-ai, LangGraph, fast-agent).
- **Young; opaque internals.** A compiled runtime is harder to audit/debug than source.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Agent-building SDK; correctness depends on your agent, not the catalog's coding loop. |
| Speed | + / neutral | Managed agentic loop removes boilerplate for Gemini/Antigravity agents. |
| Maintainability | neutral / − | First-party SDK is well-supported, but a closed compiled runtime is hard to audit and ties you to Google. |
| Safety | neutral / − | "Secure infrastructure" is claimed; the closed runtime + cloud coupling is a trust surface. |
| Cost Efficiency | neutral | Depends on Gemini/Antigravity usage. |

## Verdict

**CONDITIONAL** — the Google Antigravity SDK is the **official Python way to build stateful AI agents on Google Antigravity + Gemini**, Apache-2.0 on the SDK surface with a managed agentic-loop abstraction. Adopt it if you're committed to the Google/Gemini agent stack and want first-party, supported infrastructure. Weigh two caveats: the agentic-loop **runtime is a closed compiled binary** (not fully open/auditable/self-hostable), and it's **tangential to the AI-assisted coding loop** this catalog centers on — it's for building application agents, like vercel-ai or LangGraph, not improving how you code. Avoid if you need model-agnostic portability.

Compared to neighbors: **vercel-ai**, **LangGraph**, and **fast-agent** are agent-building frameworks (model/provider-flexible to varying degrees). The Antigravity SDK's distinguishing pitch is **first-party Google Antigravity/Gemini integration with a managed (closed-runtime) agentic loop**.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [antigravity-sdk-python](https://github.com/google-antigravity/antigravity-sdk-python) | framework | Official Google Python SDK (Apache-2.0) for building stateful AI agents on Antigravity + Gemini — abstracts the agentic loop; relies on a closed compiled runtime binary | Building application agents on Google's Antigravity/Gemini stack without rolling your own agentic-loop infrastructure | vercel-ai, LangGraph, fast-agent |
