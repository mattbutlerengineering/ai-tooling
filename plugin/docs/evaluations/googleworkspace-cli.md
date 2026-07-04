# Evaluation: googleworkspace-cli

**Repo:** [googleworkspace/cli](https://github.com/googleworkspace/cli)
**Stars:** 27,161 | **Last updated:** 2026-06-10 (pushed; created 2026-03-02) | **License:** Apache-2.0
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Outer-loop *side channel*, not a code stage. `gws` is a tool an agent **calls** to read/write Google Workspace (Drive, Gmail, Calendar, Sheets, Docs, Chat) — useful for Ship/Reflect-adjacent ops (post a release note to Chat, file a status in Sheets, pull a spec from a Doc) but it touches no source code and intervenes in no inner-loop quality signal directly.
**Layer:** Tooling — a Rust CLI binary (`gws`) plus a shipped bundle of 100+ Agent Skills that teach an LLM how to invoke it.

---

## What it does

`gws` is "one CLI for all of Google Workspace — built for humans and AI agents" (README). Rather than shipping a static command list, it reads Google's own [Discovery Service](https://developers.google.com/discovery) JSON at runtime and builds its entire `clap` command surface dynamically (confirmed in `AGENTS.md`: the project deliberately avoids generated Rust crates like `google-drive3` and instead parses Discovery docs live). So when Google adds an endpoint, `gws` picks it up without a release. Every response is structured JSON, with `--dry-run`, `--page-all` (NDJSON streaming), `gws schema <method>` introspection, and auto-pagination.

The AI-agent angle is the reason it is in scope for this catalog: the repo ships **100+ `SKILL.md` files** (one per supported API, plus higher-level helpers and 50 curated Gmail/Drive/Docs/Calendar/Sheets recipes), installable via `npx skills add`. There is also a Gemini CLI extension and an OpenClaw install path (the `gws-shared` skill auto-installs the binary via npm if it is not on PATH). The header line — "Zero boilerplate. Structured JSON output. 40+ agent skills included" — is the explicit pitch: pair the CLI with the skills and an LLM manages Workspace with no custom tooling. Note the disclaimer: it is **not** an officially supported Google product despite the org name, and it is pre-v1.0 with expected breaking changes.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No binary was downloaded, no `gws auth setup` was performed, no OAuth flow exercised, no skill installed, and no Workspace API called. Every claim comes from the GitHub repo (metadata, README, `AGENTS.md`, file tree), not from observed behavior. The "40+/100+ skills" and "structured JSON" claims are the authors' README framing plus the visible repo layout, not anything I measured at runtime.

```bash
gh api repos/googleworkspace/cli --jq '{desc,stars:.stargazers_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'
gh api repos/googleworkspace/cli/readme --jq '.content' | base64 -d        # README (humans + AI agents pitch)
gh api repos/googleworkspace/cli/contents/AGENTS.md --jq '.content' | base64 -d  # dynamic-discovery architecture
gh api "repos/googleworkspace/cli/git/trees/HEAD?recursive=1" --jq '.tree[].path'  # .agent/, .claude/, .gemini/, skills/, crates/
gh api repos/googleworkspace/cli/commits  --jq 'length'   # 30 (page-1 cap; active)
gh api repos/googleworkspace/cli/releases --jq 'length'   # 30 (changesets-driven, frequent releases)
```

## What worked

- **Dynamic Discovery is the right architecture.** Building the command surface from Google's live Discovery JSON means new Workspace endpoints work without a `gws` release — far more durable than hand-maintained wrappers, and a real maintainability win for any agent depending on it.
- **Agent-first design is genuine, not bolted on.** Structured JSON on every response, `--dry-run` to preview mutations, `gws schema <method>` for request/response introspection, NDJSON streaming, and 100+ shipped `SKILL.md` files. This is a tool deliberately shaped to be driven by an LLM, which is exactly the catalog's interest.
- **Multi-harness reach.** Native skills install via `npx skills add`, plus a first-class Gemini CLI extension and OpenClaw path. Not locked to one agent runtime.
- **Strong repo hygiene for its age.** 30 releases via changesets in ~3 months, CI with coverage gates, an `AGENTS.md` that documents the dynamic-discovery invariant for contributors, and policy/audit workflows. Apache-2.0, multiple install channels (npm, cargo, Homebrew, Nix, prebuilt binaries).

## What didn't work or surprised us

- **It is a Workspace CLI, not an AI/dev tool — scope is the central question.** Its core job is "stop writing curl against Google REST docs." The AI-agent framing is real and well-executed, but the *value* is Workspace access, not code quality. It belongs in this catalog only as a *capability an agent can call*, the way a Slack or GitHub MCP would — not as a dev-loop intervention. Flagged as adjacent/out-of-core-scope.
- **No inner-loop relevance.** Nothing here plans, implements, verifies, reviews, or ships *code*. Its dev-loop touch points are incidental (drop a release note in Chat, log status to a Sheet, read a spec from a Doc) and equally served by other integrations.
- **"googleworkspace/" org name oversells provenance.** It is explicitly *not* an officially supported Google product. The org placement implies more than the disclaimer delivers.
- **Pre-v1.0, breaking changes expected.** The README warns of churn toward v1.0 — fine for experiments, a stability risk for anything an agent depends on unattended.
- **OAuth + Google Cloud project setup is non-trivial.** Requires a GCP project and OAuth credential flow before first use; meaningfully heavier onboarding than a stateless dev CLI.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Operates on Workspace data, not your codebase; cannot make code more correct. Structured JSON + `--dry-run` make agent calls *to it* more reliable, but that is tool-call hygiene, not code correctness. |
| Speed | + | For workflows that genuinely need Workspace (pull a spec Doc, post a status), one JSON-native CLI beats hand-rolled API calls or curl. Irrelevant if your loop never touches Workspace. |
| Maintainability | + / neutral | Dynamic Discovery means the *tool* self-maintains against API drift — a real plus for anyone integrating it. No effect on your project's maintainability. |
| Safety | − / neutral | Holds OAuth credentials with broad Workspace scopes (Gmail/Drive read-write); an agent driving it can read or mutate real user data. `--dry-run` mitigates but the blast radius is your actual inbox/drive. Pre-v1.0 adds churn risk. |
| Cost Efficiency | neutral | Free, open-source binary; cost is API quota + onboarding time, not tokens. |

## Verdict

**SKIP (for the dev loop) — adjacent capability tool, out of core scope.** `gws` is a well-built, genuinely agent-first Workspace CLI: dynamic Discovery, JSON-native output, 100+ shipped skills, multi-harness install. But this catalog is an operating manual for AI-assisted *development* organized around dev-loop stages and code-quality signals, and `gws` moves none of them — it is a side-channel for reading/writing Google Workspace, in the same family as a Slack or Gmail integration. Worth knowing about if your agent workflow legitimately needs Workspace (status reporting, spec retrieval from Docs, calendar ops), but it is not a tool to install *for building software*.

It has no real neighbor among the slide/dev tools — the closest catalog analogues are MCP-style capability connectors (the Gmail/Drive/Calendar MCP servers an agent calls), not any inner-loop tool. If admitted at all, it belongs in **MCP Servers / capability integrations** with an explicit "Workspace access, not code" caveat, not in any Plan/Implement/Verify/Review/Ship category. I would leave it out of the curated dev catalog and note it only as a reference connector.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [googleworkspace-cli](https://github.com/googleworkspace/cli) | tool | JSON-native Rust CLI (`gws`) for all of Google Workspace built from Google's live Discovery API, with 100+ agent skills — a Workspace capability agents call, not a dev-loop tool | Want an agent to read/write Drive, Gmail, Calendar, Docs, Sheets without custom API wrappers (scope-adjacent: Workspace access, not code quality) | Workspace/Gmail/Drive MCP connectors; capability integrations rather than any inner-loop tool |
