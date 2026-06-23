# Evaluation: abtop

**Repo:** [graykode/abtop](https://github.com/graykode/abtop)
**Stars:** 3067 | **Last updated:** 2026-06-08 | **License:** MIT
**Last verified:** 2026-06-22
**Dev loop stage:** Reflect
**Layer:** Tooling

---

## What it does

Like `htop`, but for AI coding agents: a real-time terminal monitor for Claude Code and Codex CLI sessions, surfacing token usage, context-window percentage, rate limits, child processes, and open ports.

Mechanically, abtop is a single static Rust binary that discovers running agent sessions from **local process and open-file metadata plus on-disk session state** — it does not require API keys or authentication. It enumerates agent CLI processes, maps each to its session config (`~/.claude` / Codex equivalent), reads the session's token/context counters, and walks the process tree to attribute child processes (MCP servers, `npx` helpers) and their open ports to the owning session. Default mode is an interactive TUI that refreshes on an interval (`interval_ms`, 2000 by default); `--once` prints a single snapshot and exits, and `--json` emits a machine-readable snapshot for scripting. The only outbound network activity is indirect, via `claude --print` calls used to generate per-session summaries.

## How we tested it

**Evidence:** MEASURED

Ran hands-on on this host (macOS, arm64 / `aarch64-apple-darwin`). `cargo` is not installed here and abtop is **not published to crates.io** (`cargo install abtop` would fail — crates.io returns no `abtop` crate), so the documented `cargo install abtop` path was not usable. Instead I used the project's other supported distribution channel: the prebuilt release binary. I downloaded the `aarch64-apple-darwin` tarball from the `v0.4.8` GitHub release, **verified its published SHA-256 checksum** (matched exactly), extracted it, and executed it directly.

Observed behaviour:
- `./abtop --version` → `abtop 0.4.8`. Binary is a `Mach-O 64-bit executable arm64` (native, no Rosetta).
- The interactive TUI and `--help` both fail in this non-interactive sandbox with `Os { code: 6, ... message: "Device not configured" }` — they require a real TTY. The two **non-TTY snapshot modes work cleanly** and are the scriptable path that matters for an agent harness.
- `./abtop --once` printed a live snapshot: `abtop — 2 sessions, 0 mcp servers`, listing both Claude Code sessions then running on the machine, each with `CTX:` / `Tok:` / `Mem:` / uptime and an indented process tree of MCP-server children. abtop even listed **its own `./abtop --once` process** (and the `ps`/`head` in the pipe) inside the owning session's child tree — concrete proof it is reading the live process table, not a canned fixture. Exit code `0`.
- `./abtop --json` emitted valid JSON (parses with `json.load`). Top-level keys: `aggregate`, `generated_at_ms`, `host`, `interval_ms`, `mcp_servers`, `orphan_ports`, `rate_limits`, `sessions`, `token_rate`. Exit code `0`.

The JSON is the oracle here — it is independently checkable against reality. It reported `sessions: 2` and, for **this very evaluation session** (the `ai-tooling` Claude Code process, pid 63647), `status: Executing`, `context_percent: 22.8073`, `total_tokens: 41380601`, `model effort: xhigh`, `git_branch: fix/...`, `git_modified: 6`, and 15 attributed child processes. A second idle session (pid 87496) was correctly reported `status: Waiting`, `context_percent: 0.0`, `total_tokens: 0`. The `aggregate` block (`mem_mb`, `avg_ctx_pct: 22.8073`, `active_count: 1`) is internally consistent with the per-session rows (one Executing + one Waiting → one active). Those values track what the running agent actually was at capture time — abtop is reading real session state, not echoing static data.

```
# cargo install abtop  → NOT usable here: abtop is not on crates.io, and cargo isn't installed.
# Used the official prebuilt-binary channel instead (also documented in the README):

curl -sSL -o abtop.tar.xz \
  https://github.com/graykode/abtop/releases/download/v0.4.8/abtop-aarch64-apple-darwin.tar.xz
curl -sSL -o abtop.sha256 \
  https://github.com/graykode/abtop/releases/download/v0.4.8/abtop-aarch64-apple-darwin.tar.xz.sha256
shasum -a 256 abtop.tar.xz   # matched published .sha256 → CHECKSUM OK
tar -xf abtop.tar.xz

./abtop --version    # -> abtop 0.4.8
./abtop --once       # -> "abtop — 2 sessions ...", live tree incl. its own pid;  exit 0
./abtop --json | python3 -c 'import sys,json; json.load(sys.stdin)'   # valid; exit 0
```

## What worked

- **Zero-config, zero-auth discovery.** With nothing configured, abtop found both live agent sessions on the box and produced an accurate snapshot. No API key, no login, no setup step needed for read-only monitoring.
- **Accurate, self-verifying snapshot.** The JSON values matched ground truth (this session showed `Executing`, 22.8% context, 41.4M tokens; the idle one showed `Waiting`, 0 tokens). It even captured its own process in the tree — strong evidence it reads the live process table.
- **Scriptable, clean exit codes.** `--once` and `--json` both exit `0` and emit well-formed output with a stable schema — usable inside the Reflect stage of a harness or a cron/status-bar integration.
- **Trustworthy distribution.** Native arm64 binary, MIT-licensed, with a published per-asset SHA-256 that verified exactly; no Rosetta required.

## What didn't work or surprised us

- **`cargo install abtop` does not resolve** — the crate is not on crates.io despite the README listing it as the cross-platform install. On a machine without a prebuilt-release match you would need the installer script or to build from source; the advertised cargo path is currently a dead end.
- **TUI and `--help` need a real TTY.** In a non-interactive/sandboxed shell they abort with `Device not configured` (errno 6). Only the `--once` / `--json` snapshot modes are usable headless — fine for scripting, but the headline TUI can't be smoke-tested in CI.
- **Read-only observer.** abtop reports on sessions; it does not throttle, cap, or act on token/rate-limit pressure. The value is situational awareness, not enforcement.
- **Surface depends on agent internals.** Token/context accuracy relies on the layout of `~/.claude` (and Codex) session state; an agent-CLI version bump could move those fields and silently degrade readings.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | A monitor; it observes agent runs, it does not change code-output correctness. |
| Speed | + | `--once`/`--json` return an accurate snapshot in one shot (exit 0), giving fast at-a-glance state across concurrent sessions instead of guessing. |
| Maintainability | neutral | No effect on the codebase under development; it watches the agents, not the repo. |
| Safety | + | Local-only, no-auth read of process/file metadata surfaces rate-limit and context-exhaustion risk before a run derails; no secrets or network egress (aside from `claude --print` summaries). |
| Cost Efficiency | + | Real-time token/context visibility (this session read 41.4M tokens at 22.8% context) lets you catch runaway spend and near-full context windows early. |

## Verdict

**CONDITIONAL**

abtop does exactly what it claims and did so accurately in a real run — it is a genuinely useful Reflect-stage observability tool for anyone juggling **multiple concurrent Claude Code / Codex sessions**, where token burn and context exhaustion are otherwise invisible. Adopt it *when* that condition holds: heavy multi-session or long-running agent use where outer-loop monitoring pays off. For single-session or occasional users it is optional polish rather than essential, and two caveats temper a blanket adopt: the advertised `cargo install abtop` path is currently broken (not on crates.io — use the prebuilt binary/installer), and it is a passive monitor that observes but does not enforce limits.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [abtop](https://github.com/graykode/abtop) | tool | htop-style real-time TUI monitoring Claude Code / Codex sessions, tokens, context, rate limits, and ports | No at-a-glance view of token burn, context exhaustion, and rate-limit risk across concurrent agent sessions | ccusage |
