# Evaluation: freestyle

**Repo:** [freestyle-voice/freestyle](https://github.com/freestyle-voice/freestyle)
**Stars:** ~390 | **Last updated:** 2026-06-20 | **License:** MIT
**Dev loop stage:** Implement (voice input)
**Layer:** Tooling

---

## What it does

A local-first **voice dictation** app: hold a hotkey, talk, release, and clean text appears wherever your cursor is — including into a coding agent's prompt box. The pitch is "speak 4× faster than you type."

Per the README: it's free, open-source, and local-first — run a local model so dictations never leave your device, or bring your own API key for a cloud provider (OpenAI, Groq, Anthropic, Google, Deepgram, ElevenLabs). Features include **transcription cleaning** (grammar/punctuation, removing "um/uh"), a **custom dictionary** for phrase replacement (e.g. `"type script"` → `TypeScript`), and **contextual correction** (reformat text based on where you're typing — e.g. into email format). It's a general-purpose dictation tool; its dev-loop relevance is faster, hands-free prompt entry to coding agents.

## How we tested it

Architecture review against the README (hotkey dictation, local-first/BYO-key, multi-provider STT, transcription cleanup, custom dictionary, contextual correction). Confirmed it's a general system-wide dictation app (pastes at cursor) rather than a Claude-Code-specific integration, despite the "voice for coding agents" positioning. Catalogued for the prompt-entry use case — it fills a modality gap (no voice/dictation tooling otherwise in the catalog). Not run live, so condition-gated.

```bash
gh api repos/freestyle-voice/freestyle --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/freestyle-voice/freestyle/readme --jq '.content' | base64 -d
```

## What worked

- **Fills a modality gap.** Nothing else in the catalog covers voice/dictation; for devs who dictate prompts, speaking is genuinely faster than typing long instructions to an agent.
- **Local-first + BYO-key.** Run a local STT model for fully-private dictation, or bring your own cloud key — good privacy story and no per-use platform fee.
- **Dev-aware niceties.** A custom dictionary (`"type script"`→`TypeScript`) and transcription cleaning address the exact failure modes of dictating technical text.

## What didn't work or surprised us

- **General-purpose, not dev-specific.** It's a system-wide dictation app that happens to be useful for coding agents — not a Claude Code integration. Scope here is borderline; it's catalogued for the prompt-entry use, not as a dev tool per se.
- **Young/small.** ~390 stars and newly created — maturity and longevity unproven.
- **Accuracy depends on STT model.** Local models trade accuracy for privacy; technical jargon and code symbols are hard for dictation even with a dictionary.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Input modality; cleanup/dictionary help, but STT can misrecognize |
| Speed | + | "4× faster than typing" for prompt entry to coding agents |
| Maintainability | neutral | An input tool; doesn't touch your codebase |
| Safety | + | Local-first option keeps dictation on-device (BYO-key optional) |
| Cost Efficiency | + | Free/OSS; local model means no API cost |

## Verdict

**CONDITIONAL**

A niche but genuinely novel addition: voice dictation for faster, hands-free prompt entry to coding agents, local-first with BYO-key and dev-aware cleanup/dictionary. It's a general-purpose dictation app (not a Claude Code integration), so its catalog relevance is specifically the prompt-entry modality — which nothing else here covers. Worth trying if you'd rather speak prompts than type them; manage expectations on STT accuracy for code-heavy dictation.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [freestyle](https://github.com/freestyle-voice/freestyle) | tool | Local-first voice dictation (MIT) — hold a hotkey, speak, and clean text pastes at your cursor (incl. into Claude Code / any coding agent); BYO-key across OpenAI/Groq/Anthropic/Google/Deepgram/ElevenLabs or local model; transcription cleanup, custom dictionary, contextual reformatting | Typing long prompts to a coding agent is slow; want fast, local, private voice input for prompts — a modality the catalog otherwise lacks | caveman, agent-browser, ccs |
