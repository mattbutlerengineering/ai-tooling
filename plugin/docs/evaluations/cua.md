# Evaluation: cua

**Repo:** [trycua/cua](https://github.com/trycua/cua)
**Stars:** ~18,600 | **Last updated:** 2026-06-20 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Implement (computer-use agent infrastructure)
**Layer:** Infrastructure

---

## What it does

Open-source infrastructure for **Computer-Use Agents** — sandboxes, SDKs, and benchmarks to build, train, and evaluate agents that control full desktops (macOS, Linux, Windows). It's a stack of pieces rather than a single app.

Per the README the components are: **Cua** (build your own computer-use agent), **Cua Drivers** (background computer-use on macOS/Windows, Linux pre-release — agents click, type, and verify **without stealing the cursor or focus**, exposed via the same CLI and MCP server usable from Claude Code/Cursor/Codex/OpenClaw/custom clients), **Cua Bench** (evaluate/train models on computer-use tasks), and **Lume** (macOS VMs). The standout is background drivers: an agent can operate native desktop apps while you keep using your machine.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README and the component breakdown (Cua / Drivers / Bench / Lume). Confirmed the background, focus-preserving driver model, the CLI + MCP server interface across multiple coding agents, the cross-OS support (with Linux as pre-release), and the benchmarking/VM pieces. Did not run a live driver session, so condition-gated.

```bash
gh api repos/trycua/cua --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/trycua/cua/readme --jq '.content' | base64 -d
```

## What worked

- **Background drivers are the killer feature.** Operating native apps without stealing cursor/focus makes computer-use practical alongside human work — a real differentiator over screen-takeover agents.
- **Full stack, not a demo.** Sandboxes + SDKs + benchmarks (Cua Bench) + VMs (Lume) cover building, evaluating, *and* training computer-use agents.
- **MCP + multi-agent.** The same CLI/MCP server works from Claude Code, Cursor, Codex, and custom clients — drop-in computer-use for existing harnesses.

## What didn't work or surprised us

- **High-risk surface.** An agent driving real desktop apps needs sandboxing/supervision; pair with isolation (Lume VMs / daytona / agent-sandbox) for untrusted tasks.
- **Cross-OS maturity varies.** Linux drivers are pre-release; capabilities differ by platform.
- **Overlaps UI-TARS-desktop.** Both target computer-use; cua is the infrastructure/SDK/bench layer (give an existing coding agent a computer), UI-TARS bundles a vision model + desktop app.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Computer-use is capable but still error-prone vs. APIs |
| Speed | + | Background drivers automate desktop tasks without takeover |
| Maintainability | + | Standard CLI/MCP interface and benchmarks for repeatable eval |
| Safety | - | Driving real desktops is high-risk without VM/sandbox isolation |
| Cost Efficiency | ✓/$ | OSS; VMs/compute and model inference add cost |

## Verdict

**CONDITIONAL**

Adopt when you need to give a coding agent (Claude Code/Cursor/Codex) real, benchmarkable computer-use across desktops — the background, focus-preserving drivers and the Bench/Lume stack are its standout. Run untrusted tasks inside Lume VMs or other isolation given the action risk. Versus UI-TARS-desktop, choose cua for the infra/SDK/eval layer; mind that Linux support is still pre-release.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [cua](https://github.com/trycua/cua) | harness | Infrastructure for computer-use agents (MIT, ★19K) — sandboxes, SDKs, and benchmarks to build/train/evaluate desktop-controlling agents; background "Cua Drivers" operate native apps without stealing focus via CLI + MCP from Claude Code/Cursor/Codex; Lume VMs + Cua Bench | Computer-use agents need isolated, benchmarkable desktop environments; want background-capable drivers + sandboxes + evals, not a fragile screen-scraper | UI-TARS-desktop, daytona, agent-sandbox, nanobrowser |
