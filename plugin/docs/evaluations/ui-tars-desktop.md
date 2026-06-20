# Evaluation: UI-TARS-desktop

**Repo:** [bytedance/UI-TARS-desktop](https://github.com/bytedance/UI-TARS-desktop)
**Stars:** ~37,000 | **Last updated:** 2026-06-18 | **License:** Apache-2.0
**Dev loop stage:** Implement (GUI agent stack)
**Layer:** Tooling

---

## What it does

A multimodal AI agent stack from ByteDance, shipping two projects under the "TARS" umbrella:

- **Agent TARS** — a general multimodal agent that brings GUI-agent and vision capabilities into your terminal, computer, browser, and product. It ships a CLI and Web UI and integrates with real-world MCP tools, aiming for human-like task completion via multimodal LLMs.
- **UI-TARS Desktop** — a desktop application providing a native **GUI agent** based on the UI-TARS vision model, with local and remote **computer** operators as well as **browser** operators (i.e., it sees the screen and drives the mouse/keyboard/browser).

The defining capability is vision-driven control: the agent perceives a real GUI (screenshots) and operates it like a human, rather than being limited to text/API tool calls.

## How we tested it

Architecture review against the README and the two-project structure (Agent TARS CLI/Web UI + MCP integration; UI-TARS Desktop native GUI agent with computer/browser operators powered by the UI-TARS model). Confirmed the multimodal/vision-driven control model and the local+remote operator support. Did not run the desktop app or drive a live GUI, so condition-gated.

```bash
gh api repos/bytedance/UI-TARS-desktop --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/bytedance/UI-TARS-desktop/readme --jq '.content' | base64 -d
```

## What worked

- **Vision-driven GUI control.** Operating real interfaces via a vision model unlocks tasks that text/API-only agents can't do — legacy apps, arbitrary websites, desktop software with no API.
- **Two on-ramps.** Agent TARS (CLI/Web UI, MCP-integrated) for general multimodal tasks, plus UI-TARS Desktop for native computer/browser operation — covers both developer and end-user use.
- **Backed and active.** ByteDance-maintained, Apache-2.0, ~37K stars — a serious entry in the computer-use/GUI-agent space.

## What didn't work or surprised us

- **High-risk action surface.** A vision agent driving your real mouse/keyboard/browser is powerful and dangerous; needs sandboxing/supervision (pairs conceptually with isolation infra like daytona/agent-sandbox).
- **Model + compute dependency.** Best results rely on the UI-TARS vision model and meaningful compute; GUI agents are still error-prone vs. API tool calls.
- **Adjacent to the coding dev loop.** It's a computer/browser-use agent stack, not a code-writing harness; relevant for automation/QA and as agent infrastructure more than day-to-day coding.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | GUI agents are capable but still error-prone vs. API calls |
| Speed | + | Automates manual GUI/browser workflows end-to-end |
| Maintainability | neutral | An agent stack; not part of your codebase |
| Safety | - | Vision-driven control of real computer/browser is high-risk without sandboxing |
| Cost Efficiency | neutral | OSS, but vision-model inference and compute add cost |

## Verdict

**CONDITIONAL**

Adopt when you need an agent to operate real GUIs/browsers — desktop automation, computer-use, or web tasks without APIs — and can run it under supervision/sandboxing given the action risk. As a coding-dev-loop tool it's adjacent (automation/QA infra rather than code authoring). Strong, well-backed option in the GUI-agent space; weigh the safety surface and compute needs.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [UI-TARS-desktop](https://github.com/bytedance/UI-TARS-desktop) | harness | Multimodal GUI-agent stack (Apache-2.0, ★37K, by ByteDance) — Agent TARS (general multimodal agent, CLI/Web UI, MCP) + UI-TARS Desktop (native GUI agent driving local/remote computer and browser operators via the UI-TARS vision model) | Text-only agents can't operate real GUIs; want a vision-driven agent that sees and controls computer/browser like a human | nanobrowser, agent-browser, chrome-devtools-mcp, eigent |
