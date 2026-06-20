# Evaluation: MiMo Code

**Repo:** [XiaomiMiMo/MiMo-Code](https://github.com/XiaomiMiMo/MiMo-Code)
**Stars:** 9,944 | **Last updated:** 2026-06-19 (pushed; created 2026-06-10) | **License:** MIT | **Releases:** 2
**Dev loop stage:** Implement (a terminal coding agent CLI; touches all inner-loop stages)
**Layer:** Tooling (TypeScript, `npm i -g @mimo-ai/cli` or one-line installer)

---

## What it does

MiMo Code is **Xiaomi's terminal-native AI coding agent** — a Claude Code-style CLI that reads and writes code, runs commands, manages Git, and keeps a **persistent memory system** for a deep, cross-session understanding of your project while "continuously improving itself." It's the MiMo team's entry in the vendor-coding-CLI category (peer to gemini-cli, qwen-code, grok-cli, kimi-code, DeepSeek-Reasonix).

The notable on-ramp is **MiMo Auto** — a free-for-a-limited-time anonymous channel that lets you start with **zero configuration**, no API key. First launch walks you through options: MiMo Auto, Xiaomi MiMo Platform (OAuth), **import existing Claude Code authentication in one step**, or any custom OpenAI-compatible provider added in the TUI. It advertises **multiple agents** and a persistent project memory as core features.

## How we tested it

**Source-grounded inspection — not installed, not run.** No CLI installed, no session. Claims come from the repository (GitHub metadata, README, install/config section) — the project's own documentation, not observed coding quality.

```bash
gh api repos/XiaomiMiMo/MiMo-Code --jq '{stars,created_at,pushed_at,license:.license.spdx_id,lang:.language}'
gh api repos/XiaomiMiMo/MiMo-Code/readme --jq '.content' | base64 -d   # features, install, providers
gh api repos/XiaomiMiMo/MiMo-Code/releases --jq 'length'              # 2
```

## What worked

- **Zero-config + Claude Code import lowers the trial barrier.** A free anonymous channel and one-step migration of existing Claude Code auth make it unusually easy to try without committing keys or config — good for evaluation.
- **Persistent project memory is first-class**, not bolted on — the right instinct for cross-session continuity, and a differentiator vs. simpler vendor CLIs.
- **Provider-agnostic.** Any OpenAI-compatible API works, so it isn't locked to Xiaomi's models — you can run it as a harness over whatever you already pay for.
- **Strong early traction + backing.** ~10K stars in ~9 days and a major vendor behind it suggest resources and momentum.

## What didn't work or surprised us

- **Brand new and thin on release history.** Created 2026-06-10 with only 2 releases at evaluation — stability, longevity, and the durability of the "free for a limited time" channel are all unproven.
- **Free channel is explicitly temporary.** "MiMo Auto" will presumably gate or monetize later; don't build a workflow around the zero-cost path.
- **Crowded category with no clear inner-loop edge yet.** It does what gemini-cli/qwen-code/Claude Code already do; the differentiators (persistent memory, multi-agent) are claims that aren't independently verified here, and the strongest models in the space remain the frontier ones.
- **Privacy posture of an "anonymous channel" deserves scrutiny** before sending proprietary code through it — terms unverified.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Output quality tracks the chosen model; no distinctive verification layer described. |
| Speed | + / neutral | Persistent memory can reduce re-explaining context across sessions; otherwise a standard agent loop. |
| Maintainability | neutral | A coding tool, not a codebase-structure influence. |
| Safety | neutral / − | Runs shell + edits files like any terminal agent; the free anonymous channel's data handling is unverified — vet before proprietary use. |
| Cost Efficiency | + / neutral | Free MiMo Auto channel (time-limited) + BYO-provider give cost flexibility; long-term pricing unknown. |

## Verdict

**CONDITIONAL** — a credible, easy-to-try vendor coding CLI with a genuinely low on-ramp (free channel + one-step Claude Code import) and first-class persistent memory. Worth a look if you want to sample another terminal agent or run a provider-agnostic harness with built-in memory. But it's days old with minimal release history, the free channel is temporary, and it doesn't yet show a clear advantage over the established CLIs or change the fact that model quality dominates outcomes. Try it; don't make it load-bearing until it matures, and check the anonymous channel's data terms before sending proprietary code.

Compared to neighbors: it sits squarely with **gemini-cli** / **qwen-code** / **grok-cli** / **kimi-code** / **DeepSeek-Reasonix** as a vendor-native terminal agent. Its pitch is the **zero-config free channel + Claude Code auth import + persistent memory**; gemini-cli leads on context size/free tier and grok-cli on autonomy features. Pick by which model/ecosystem you want and how much the easy migration matters.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [MiMo-Code](https://github.com/XiaomiMiMo/MiMo-Code) | platform | Xiaomi's terminal AI coding agent — zero-config free channel, one-step Claude Code auth import, persistent project memory, any OpenAI-compatible provider | Want to try another terminal coding agent (or a provider-agnostic harness with built-in memory) with minimal setup | gemini-cli, qwen-code, grok-cli, kimi-code, DeepSeek-Reasonix |
