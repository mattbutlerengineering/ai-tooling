# Evaluation: happy

**Repo:** [slopus/happy](https://github.com/slopus/happy)
**Stars:** 22,068 | **Last updated:** 2026-06-10 | **License:** MIT
**Dev loop stage:** Implement + Verify (remote access/monitoring across the inner loop)
**Layer:** Infrastructure (access/transport layer around the agent, not the agent itself)

---

## What it does

Catalog one-liner: "Mobile and web client for Codex and Claude Code with realtime voice and encryption." Happy (npm package `happy`, formerly `happy-coder`) is a remote-control layer that lets you drive an *existing* Claude Code or Codex session from a phone, browser, or another terminal. It does not replace Claude Code or change how the agent reasons — it adds a transport and presentation surface around it.

The mechanism is a thin CLI wrapper plus a sync relay. On your machine you run `happy` instead of `claude` (or `happy codex`, `happy gemini`, `happy openclaw`, or `happy acp -- <any ACP agent>`). The wrapper starts the real agent locally and prints a QR code; scanning it pairs a mobile/web client. From then on you can watch the session, approve permission prompts, and send new prompts from your phone. A background **daemon** (`happy daemon start/stop/status`) can stay resident so you can spawn and manage sessions remotely without an open terminal. Pressing any key on the desktop reclaims local control. Four packages make up the system: `happy-cli` (the wrapper/daemon), `happy-app` (Expo web + native client), `happy-agent` (remote session control CLI), and `happy-server` (the encrypted sync backend).

The security model is the standout. The server is **zero-knowledge**: clients generate keys locally, encrypt every message before it leaves the device, and the relay only stores/forwards opaque encrypted blobs. Per `docs/encryption.md`, two variants are implemented — legacy NaCl `secretbox` (XSalsa20-Poly1305, 24-byte nonce) and a newer AES-256-GCM "dataKey" variant with per-session/per-machine keys wrapped via `tweetnacl.box`. Auth is by public-key signature (no passwords stored). Push notifications are content-blind. The hosted relay (`happy-api.slopus.com`) is free, and the whole server is self-hostable as a single Docker container (PGlite + local FS + in-memory bus, no Postgres/Redis/S3 required). Realtime voice is a separate feature built on **ElevenLabs** (`docs/voice-architecture.md`, `docs/paid-voice.md`) — a paid third-party API, not part of the E2E-encrypted core.

## How we tested it

**Evidence:** REVIEW

Inspected the repository, root README, the `happy-cli`, `happy-server`, and `happy-agent` package READMEs, `docs/encryption.md`, and `docs/voice-architecture.md`; reviewed the monorepo file tree and pulled maturity metrics via the GitHub and npm APIs. **Did not install the CLI, pair a device, or run a remote session** — doing so requires installing a global npm package that wraps the agent, registering a device against the relay (or self-hosting the server), and an iOS/Android/web client outside this environment; and the differentiated voice path requires a paid ElevenLabs account. Verdict rests on source/doc inspection and maturity signals, not a hands-on run.

```bash
gh api repos/slopus/happy --jq '{stars,license,description,created,pushed,forks,open_issues}'
gh api repos/slopus/happy/readme --jq '.content' | base64 -d
gh api "repos/slopus/happy/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api repos/slopus/happy/contents/packages/happy-server/README.md --jq '.content' | base64 -d
gh api repos/slopus/happy/contents/packages/happy-cli/README.md --jq '.content' | base64 -d
gh api repos/slopus/happy/contents/docs/encryption.md --jq '.content' | base64 -d
gh api repos/slopus/happy/contents/docs/voice-architecture.md --jq '.content' | base64 -d
gh api repos/slopus/happy/releases --paginate --jq '.[].tag_name' | wc -l    # 4 GitHub releases
gh api repos/slopus/happy/contributors --paginate --jq '.[].login' | wc -l   # 64 contributors
curl -s https://api.npmjs.org/downloads/point/last-month/happy                # ~14,620/mo
```

## What worked

- **Genuine end-to-end encryption with a zero-knowledge, self-hostable relay.** Established primitives (NaCl secretbox / AES-256-GCM, public-key auth), a documented binary layout, an `encryption.test.ts`, and a single-container self-host option. The server "stores encrypted blobs it cannot read" claim is consistent with the design docs — this is the most credible security posture among remote-agent clients.
- **Non-invasive integration.** It wraps the agent CLI rather than mutating `~/.claude` (no skills/agents/hooks installed). You opt in per session by typing `happy` instead of `claude`, and reclaim local control with one keypress. Low lock-in: stop using it and your normal `claude` workflow is untouched.
- **Broad agent support and an escape hatch.** Works with Claude Code, Codex, Gemini, OpenClaw, and any ACP-compatible agent (`happy acp -- <agent>`), so it is not a single-vendor bet.
- **Strong maturity for the catalog.** 22k stars, MIT, 64 contributors, ~14.6k npm downloads/month, shipping iOS/Android/web apps, active push-notification + daemon features, and detailed protocol/encryption/voice docs. Far past the single-author/days-old profile.
- **Real workflow value for one specific pain.** Async approval of permission prompts and monitoring long autonomous runs from a phone removes the "tethered to the terminal while the agent waits on me" friction — push notifications when the agent needs permission or errors out.

## What didn't work or surprised us

- **It is a convenience/access layer, not a dev-loop quality tool.** It changes *where* and *when* you can interact with the agent, not *how well* the agent plans, implements, verifies, reviews, or ships. The code that gets written is identical to running `claude` directly.
- **Adds a network surface and a default dependency on a third-party relay.** The convenient path routes your (encrypted) session through `happy-api.slopus.com`. E2E encryption mitigates content exposure, but it still introduces an external service and traffic metadata into the loop unless you self-host. That is a new trust/availability dependency the bare CLI does not have.
- **The headline "realtime voice" feature is paid and external.** Voice rides on ElevenLabs (`paid-voice.md`), so the most-marketed differentiator is gated behind a separate paid API and is outside the encrypted core — easy to over-weight from the catalog one-liner.
- **Only 4 GitHub releases despite high activity.** Most distribution is via app stores and npm, so GitHub release count understates maturity, but it also means versioning/changelog discipline on GitHub is thin compared to its star count.
- **Mobile is a poor surface for deep code work.** Reviewing diffs, steering architecture, or debugging on a phone is constrained; the realistic use is monitoring and lightweight approvals, not primary development.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Does not alter agent reasoning, prompts, or verification — same output as `claude` |
| Speed | + (situational) | Async remote approval lets long autonomous runs proceed without waiting for you at the desk; reduces wall-clock stalls on permission gates |
| Maintainability | neutral | No effect on code structure, tests, or review; it is a transport/UI layer |
| Safety | +/- | Strong E2E encryption + self-hostable zero-knowledge relay are real positives; offset by adding a network surface and (by default) a third-party relay vs. a purely local CLI |
| Cost Efficiency | neutral / - | Core sync is free/self-hostable (neutral); the voice feature adds paid ElevenLabs cost if used |

## Verdict

**CONDITIONAL**

Adopt happy when remote or asynchronous access to your coding agent is a real need — you run long autonomous sessions and want to monitor them or approve permission prompts from a phone, or you want to kick off/check work away from your desk. The encryption model is genuine and the self-host option means you can keep the security posture of a local-only setup while gaining remote control. It is non-invasive and low lock-in, which makes it a safe trial.

It is not an unconditional ADOPT because it sits *beside* the dev loop rather than inside it: it improves access and convenience but does not move Correctness, Maintainability, or (for the core feature) Cost. For developers who always work at their keyboard, it adds a network surface and an external relay dependency in exchange for benefits they won't use. The catalog already marks it "unique: mobile client," and that uniqueness is exactly its scope — a remote-access convenience layer, valuable for the specific async/mobile workflow and skippable otherwise.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [happy](https://github.com/slopus/happy) | platform | Mobile and web client for Codex and Claude Code with realtime voice and encryption | Want to use Claude Code from mobile/web with voice support | — (unique: mobile client) |
