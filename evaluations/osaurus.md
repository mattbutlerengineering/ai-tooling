# Evaluation: osaurus

**Repo:** [osaurus-ai/osaurus](https://github.com/osaurus-ai/osaurus)
**Stars:** ~5,970 | **Last updated:** 2026-06-20 | **License:** MIT
**Dev loop stage:** Implement (local agent harness)
**Layer:** Tooling

---

## What it does

A native macOS harness for AI agents — "own your AI." Osaurus runs agents, persistent memory, tools, and **cryptographic identity** entirely locally on your Mac, with any model, fully offline, and autonomous execution. It's built purely in Swift.

The emphasis is ownership and privacy: rather than a cloud-hosted agent platform, everything (the agent loop, its memory, its tools, and a cryptographic identity for the agent) lives on your machine and runs offline. It's a Mac-native (Swift) application, so it integrates with the OS rather than being a cross-platform CLI.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README (Mac-native Swift harness; local agents + persistent memory + tools + cryptographic identity; offline; autonomous execution). Confirmed the own-your-AI, fully-local/offline positioning and the Swift/macOS-native implementation. Not run live on a Mac, so condition-gated.

```bash
gh api repos/osaurus-ai/osaurus --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/osaurus-ai/osaurus/readme --jq '.content' | base64 -d
```

## What worked

- **Fully local + offline.** Running agents, memory, and tools on-device with no cloud dependency is a strong privacy/ownership story — distinctive among agent harnesses.
- **Mac-native (Swift).** Native integration and performance on macOS, rather than a generic cross-platform wrapper.
- **Cryptographic identity.** Giving agents a cryptographic identity is an unusual, forward-looking feature for provenance/trust.

## What didn't work or surprised us

- **macOS-only.** Swift/Mac-native means no Linux/Windows; narrows the audience.
- **Local-model ceiling.** Fully-offline operation leans on local models, which trade capability for privacy versus frontier cloud models.
- **Overlaps gptme/HolyClaude/letta-code.** Local/own-your-agent harnesses exist; osaurus's edge is the Mac-native, offline, cryptographic-identity combination.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Depends on the (often local) model used |
| Speed | + | Native Swift, on-device — no cloud round-trip |
| Maintainability | neutral | A harness/app; doesn't change your codebase |
| Safety | + | Fully local/offline; cryptographic agent identity |
| Cost Efficiency | + | Offline/local models — no API or platform fees |

## Verdict

**CONDITIONAL**

Adopt if you want a private, offline, Mac-native agent runtime where agents, memory, identity, and tools live on your machine — its ownership/offline story and cryptographic identity are the differentiators. Accept the macOS-only constraint and the local-model capability ceiling. For cross-platform or maximal capability, a CLI harness (gptme/opencode) or cloud-capable agent fits better; osaurus is for the privacy-first, own-your-AI use case.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [osaurus](https://github.com/osaurus-ai/osaurus) | harness | Native macOS harness for AI agents (MIT, ★6K) — "own your AI": agents, persistent memory, tools, and cryptographic identity running locally on your Mac, any model, fully offline, autonomous execution; built purely in Swift | Want a private, offline, Mac-native agent runtime with persistent memory and identity you own — not a cloud-hosted harness | gptme, HolyClaude, letta-code, eigent |
