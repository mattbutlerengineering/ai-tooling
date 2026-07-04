# Evaluation: plumb-mcp (Plumb)

**Repo:** [tathagat22/plumb-mcp](https://github.com/tathagat22/plumb-mcp)
**Stars:** 57 | **Last updated:** 2026-06-18 (last push; latest tag v0.12.0) | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Implement (Figma design→code grounding) + Verify (`plumb_verify` / `plumb_fit` diff rendered code against the design)
**Layer:** Tooling (agent-facing MCP bridge + verification CLI — not hosted infrastructure)

---

## What it does

Catalog one-liner: *"Local Figma MCP server with no REST rate limits, no metered tool-call quotas, and a verification loop — drop-in alternative to Figma's Dev Mode MCP and Framelink, works on every plan including Free."*

Plumb is a TypeScript MCP server that reads Figma through a **desktop-app plugin** (the same plugin-bridge architecture as figma-mcp-go) so it never touches Figma's metered REST API — no per-call quota, no rate limit, and Variables are readable even on Free plans (the REST Variables API is Enterprise-only). The plugin pairs over a localhost WebSocket control channel (`ws://127.0.0.1:31337`) plus a loopback HTTP path for binary blobs (screenshots/assets POSTed straight to disk, no base64). A secondary headless **REST path** exists (needs `FIGMA_TOKEN`) for CI use where Figma desktop isn't open; tools auto-pick the path.

Its distinguishing mechanism is two-fold. First, it normalizes Figma into a compact **Plumb Design Spec (PDS)**: auto-layout resolved to flexbox, design tokens deduped into short handles (`$c1`, `$t1`), depth-stable `el` node handles — collapsing the multi-hundred-thousand-token JSON the Figma API emits down to a fraction (the README claims a 178-node dialog comes back at ~2.6k tokens vs. Dev Mode MCP's 25k token cap / 351K observed). Second, and uniquely among its peers, it **closes the loop on the generated code**: `plumb_verify` drives headless Chrome to diff the rendered DOM against the design — structured deltas with ΔE2000 perceptual colour distance, shadow/rotation/flex-child/fill-stack checks, no pixel diff — and `plumb_fit` turns that into a self-healing loop, scoring the build 0–100 and handing back prioritised deltas so the agent iterates to pixel-perfect. The loop runs in-editor (MCP, free, agent is the generator), from the terminal (`plumb-mcp fit <url>`, needs `ANTHROPIC_API_KEY`), or in a hosted browser Playground.

It exposes **15 MCP tools**: `plumb_status`, `plumb_outline`, `plumb_node`, `plumb_query` (slices to stay under token budget), `plumb_describe` (text-only narrative for image-blind harnesses), `plumb_tokens`, `plumb_selection`, `plumb_assets` (SVG/PNG export to disk), `plumb_screenshot`, `plumb_search`, `plumb_components`, `plumb_verify`, `plumb_fit`, and two headless `.fig`-file readers (`plumb_fig_outline`, `plumb_fig_node`) that work with no Figma desktop and no token. Install is `npm install -g plumb-mcp` → `plumb-mcp init` (auto-wires Claude Code / Cursor / VS Code / Windsurf) plus one-time plugin sideload; also `npx`, Docker (`ghcr.io/tathagat22/plumb-mcp`), and Cursor/VS Code deeplinks.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed or run.** I confirmed the repo via `gh search repos plumb-mcp` (the catalog entry was unlinked) and examined the GitHub repo metadata, the full README, the tag history, and the recursive file tree. I did **not** install the npm package, sideload the Figma plugin, pair a session, run the verify/fit CLIs, or invoke any of the 15 MCP tools. No designs were read, no code was generated or diffed — so there are no measured token-reduction figures, verify accuracy, fit-convergence rates, or output-fidelity numbers below. The 15-tool surface, the PDS/token-dedup claims, the ΔE2000 verification mechanism, the plugin-bridge architecture, the `ws://127.0.0.1:31337` bind, and the dual plugin/REST data paths are taken from the README and the `docs/tools/*.md` tree, not from execution.

```bash
gh search repos plumb-mcp --json fullName,description,stargazersCount,url,updatedAt
gh api repos/tathagat22/plumb-mcp --jq '{stars,license,pushed_at,topics,open_issues_count}'
gh api repos/tathagat22/plumb-mcp/readme --jq '.content' | base64 -d
gh api repos/tathagat22/plumb-mcp/tags --jq '.[0:5][].name'
gh api "repos/tathagat22/plumb-mcp/git/trees/HEAD?recursive=1" --jq '.tree[].path'
# Calibration against catalog peers:
#   evaluations/figma-mcp-go.md (CONDITIONAL), evaluations/design-extract.md (CONDITIONAL)
```

## What worked

- **The verification loop is the genuine differentiator.** Figma-Context-MCP, design-extract, and figma-mcp-go all *feed* the agent a design; none *check* whether the shipped code matches it. `plumb_verify` (ΔE2000 colour deltas, flex/shadow/rotation checks, headless-Chrome DOM diff) and `plumb_fit` (0–100 score + prioritised deltas → self-healing iteration) close the design→code→verify loop. That is a real Verify-stage capability its catalog peers lack.
- **Token economy is the right problem to attack.** The Figma REST/Dev Mode JSON is notoriously huge; the PDS normalization (auto-layout→flexbox, token dedup to `$c1`/`$t1`, depth-stable handles, fit-to-budget auto-depth) directly targets the "exceeded the 25k token cap / 351K tokens observed" failure mode that makes naive Figma MCPs unusable in an agent loop.
- **Plugin-bridge architecture removes the plan/quota wall** — same structural premise as figma-mcp-go: no REST, no per-call quota, works on Free, and reads Variables (otherwise Enterprise-only). Plus a secondary REST/headless path and offline `.fig`-file readers for CI, which figma-mcp-go does not advertise.
- **Strong agent ergonomics and client breadth.** `plumb-mcp init` auto-detects and wires Claude Code / Cursor / VS Code / Windsurf; npx, Docker, and editor deeplinks; an in-browser Playground for zero-install trials; documented per-tool docs (`docs/tools/*.md`) and a stated agent flow.
- **Engineering hygiene present.** CI workflows (`release.yml`, `docker.yml`, `docs.yml`), a VitePress docs site, Docker image, four localized READMEs, and a thoughtful transport design (per-item upload acks to avoid Figma IPC buffering/redelivery) suggest more than a thin wrapper.

## What didn't work or surprised us

- **Early-stage, low-adoption project.** 57 stars, latest tag **v0.12.0**, created 2026-05-23 — under a month old at this evaluation. Single maintainer. API stability and longevity are unproven; the broad 15-tool + verify/fit surface reached this fast almost certainly varies in per-tool quality.
- **Requires Figma desktop with the plugin sideloaded and paired** for the primary (rate-limit-free) path — not headless/CI-friendly. The REST and `.fig`-file paths exist for headless use but inherit REST rate limits / lack Variables, so the headline benefits and the headless benefits are mutually exclusive.
- **The terminal `fit` loop costs Anthropic API tokens.** `plumb-mcp fit <url>` needs `ANTHROPIC_API_KEY` and runs an iterative generate→render→diff→correct loop — real model spend per convergence run. The in-editor `plumb_fit` is free only because your existing agent is the generator.
- **Local write-capable-ish surface and verification fidelity unverified.** A localhost WS control channel plus a loopback HTTP upload endpoint POSTing binaries to disk is a local attack surface (mitigated by 127.0.0.1 bind + Origin-aware pairing). Whether `plumb_verify`'s ΔE2000/flex deltas actually catch real layout regressions, and whether PDS reconstructs designs faithfully, is unverified here.
- **Read-focused on Figma (no design *generation/editing*).** Unlike figma-mcp-go (full read/write, 73 tools, text-to-design), Plumb reads Figma and verifies code — it does not create or edit designs inside Figma.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + (strong, if verify works) | PDS grounds generated UI in the actual Figma spec, and `plumb_verify`/`plumb_fit` close the loop by diffing rendered DOM against the design (ΔE2000, flex/shadow checks) — the only catalog peer that verifies output. Verify fidelity unverified here. |
| Speed | + / mixed | PDS token dedup avoids blowing the agent's context (claimed ~2.6k vs 25k+ for a dialog), speeding iteration; but the rate-limit-free path needs Figma desktop + plugin paired (manual, not headless). |
| Maintainability | + | Design-token table + structured PDS + CI-runnable `plumb-mcp verify` (headless) can guard against design drift in CI, not just one-shot generation. |
| Safety | - (caution) | Localhost WS + loopback HTTP upload-to-disk is a local surface (mitigated by 127.0.0.1 + Origin-aware pairing); very young v0.x single-maintainer project raises reliability risk; REST path needs a `FIGMA_TOKEN`. |
| Cost Efficiency | + (with one caveat) | Free, MIT, self-hosted; plugin path eliminates Figma's metered tool-call cost and works on Free plans. Caveat: terminal `plumb-mcp fit` consumes Anthropic API tokens per run. |

## Verdict

**CONDITIONAL**

Plumb is the only Figma-MCP in the catalog cluster that **closes the loop on the generated code** — `plumb_verify` diffs your rendered DOM against the design (ΔE2000 colour + flex/shadow/rotation deltas via headless Chrome) and `plumb_fit` turns that into a self-healing 0–100 convergence loop. Combined with a plugin-bridge that removes Figma's REST quota/plan wall (works on Free, reads Variables) and a PDS normalizer that collapses Figma's giant JSON into a token-budget-friendly spec, it targets the two things that make naive Figma MCPs fail in an agent loop: context blowup and unverified output. **Adopt it when your project does meaningful Figma→code work, you want the agent to verify (not just guess) that the build matches the design, and you can run Figma desktop with the plugin paired** — confirming verify fidelity on a sample run first.

It is not ADOPT-everywhere: it's niche to Figma-using teams; the rate-limit-free path demands a manual desktop + plugin pairing that rules out pure headless/CI (the REST/`.fig` fallbacks lose Variables and inherit rate limits); the terminal `fit` loop spends Anthropic tokens; and it's a very young (v0.12.0, ~1 month old, 57 stars, single maintainer) project whose verify/PDS fidelity is unverified here. Not SKIP because the verification loop is a real, differentiated Verify-stage capability none of its peers offer, the token-economy and plan-bypass premises are structurally sound, and the engineering (CI, Docker, docs, transport design) looks legitimate. Among the cluster: choose **Figma-Context-MCP** for plain read-only design→code; **figma-mcp-go** when the agent must *write/generate* inside Figma; **design-extract** when the source of truth is a live website rather than a Figma file; and **plumb-mcp** when you want compact Figma reads plus a closed design→code→verify loop.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [plumb-mcp](https://github.com/tathagat22/plumb-mcp) | MCP server | Local Figma→code MCP (15 tools) with no REST rate limits and a closed verify/fit loop that diffs rendered code against the design — works on every plan incl. Free (57 stars) | Figma's Dev Mode MCP blows the token budget and meters tool calls, and no Figma MCP checks whether shipped code actually matches the design | Figma-Context-MCP and figma-mcp-go also read Figma via a plugin bridge, but plumb-mcp adds compact PDS specs + a headless-Chrome verification loop (plumb_verify/plumb_fit) they lack |
