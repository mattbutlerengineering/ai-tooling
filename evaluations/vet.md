# Evaluation: Vet (Verify Everything)

**Repo:** [imbue-ai/vet](https://github.com/imbue-ai/vet)
**Stars:** 476 | **Last updated:** 2026-06-10 (pushed) | **License:** AGPL-3.0 | **Language:** Python (PyPI: `verify-everything`)
**Last verified:** 2026-10-16
**Last triaged:** 2026-10-16  <!-- triaged: bulk -->
**Dev loop stage:** Code Review & Quality / Verify
**Layer:** Tooling (CLI + agent skill + CI)

---

## What it does

Vet (by [Imbue](https://imbue.com)) is **a standalone verification tool for code changes and coding-agent behavior** — "find issues worth your attention." It **reviews intent and code**: it checks agent *conversations* for goal adherence and code *changes* for correctness. It **runs anywhere** — from the terminal, as an agent skill (auto-runs after code changes to flag issues and request/action mismatches), or in CI. It's **bring-your-own-model** (any provider via your keys), works with existing **Anthropic/OpenAI subscriptions** (`--agentic`), and is **free/open source** (AGPL-3.0) with no account, fees, or data collection — requests go directly to your inference provider. The skill installs across `.agents/`, `.opencode/`, `.claude/`, and `.codex/` skill directories (project or user level), so multiple agents discover it.

## How we tested it

**Evidence:** RUN

**Hands-on** — installed it via `pip install verify-everything` (PyPI, v0.2.16) into a clean venv and ran the CLI against a two-commit fixture repo under `/tmp/eval-vet/fx`: `calc.py` committed with a correct `average()`, then an uncommitted edit introducing a planted off-by-one (`/ (len(xs) + 1)`) plus an unclosed file handle in a new `load()`. The model-backed review is the tool's core job and needs an Anthropic/OpenAI key or a logged-in agent CLI; neither exists in this sandbox, so what was exercised is everything that works before the model call.

```
$ vet --version                    -> vet 0.2.16
$ vet --list-issue-codes           -> 28 codes (logic_error, incorrect_algorithm, fails_silently, hardcoded_secret, insecure_code, ...)
$ vet --list-models                -> anthropic: claude-fable-5, claude-haiku-4-5, claude-opus-4-x ... (plus other providers)
$ vet --list-configs               -> "No configurations found." (reads ~/.config/vet/configs.toml and <repo>/.vet/configs.toml)
$ vet "fix average" --repo .       (no key, 3.9s wall)
analyzing . (relative to HEAD)
vet: Neither ANTHROPIC_API_KEY nor ANTHROPIC_AUTH_TOKEN environment variable is set
hint: If you have a Claude, Codex, or OpenCode subscription, try --agentic to use your
      locally installed coding agent CLI instead.
$ env -i ... vet --repo .          (no goal, no key)  -> same message, exit code 2
$ ANTHROPIC_API_KEY=invalid vet "fix average" --repo .   -> prints "analyzing . (relative to HEAD)", then no output until a 60s timeout killed it (exit 124)
```

## Test design

- **Task/corpus:** fixture repo `/tmp/eval-vet/fx` — `calc.py` with a planted off-by-one in `average()` and an unclosed file handle in `load()`, as an uncommitted diff against HEAD.
- **Baseline:** none for the detection question — no model was reachable, so there is no with/without detection delta. The baseline arm (no tool) is trivially "defects unflagged".
- **Metric:** install success, CLI surface, startup-to-failure wall-clock (3.9s), exit code and message clarity when the credential is missing.
- **Reproduce:** `python3 -m venv v && v/bin/pip install verify-everything && cd <git repo with a diff> && v/bin/vet "goal"`; add `--agentic` with a logged-in `claude`/`codex`/`opencode` CLI to use a subscription.

## What worked

- **Clean install.** One `pip install` from PyPI, a `vet` entry point, no extra setup; the package name (`verify-everything`) differs from the repo name but resolves and matches the catalog's note.
- **Honest failure on a missing credential.** Fails fast (3.9s) with a named missing variable and a pointer to `--agentic`, and a non-zero exit (2) that CI can gate on.
- **Documented, enumerable surface.** `--list-issue-codes` shows 28 concrete issue classes (logic errors, incorrect algorithms, silent failures, hardcoded secrets, insecure code, instruction-file disobedience, commit-message mismatch) that line up with the README's "intent + code" pitch; `--history-loader` accepts a conversation-history command to derive the goal, `--staged` and `--base-commit` scope the diff, and `--max-spend` caps cost.
- **Subscription path exists.** `--agentic` with `--agent-harness {claude,codex,opencode}` delegates to a local agent CLI instead of an API key.

## What didn't work or surprised us

- **The core job went unexercised.** No key and no logged-in agent CLI were available, so whether vet flags the planted off-by-one or the unclosed handle is unknown; false-positive and false-negative rates remain unmeasured, and all claims about review quality stay vendor claims.
- **A bad key hangs silently.** With an invalid key and a walled network the run printed one line and then produced nothing for 60s; whether that is the sandbox proxy or missing client-side timeout handling is unresolved.
- **AGPL-3.0.** Strong copyleft — fine for a dev-time tool you run, a consideration if embedded in a product or service.
- **Verification costs inference.** Every review is model calls; `--max-spend` mitigates but the cost is real.
- **Overlaps the review field.** Conceptually near code-review/pr-review-toolkit/brooks-lint; the wedge is intent-adherence and agent-behavior verification.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Detection quality unmeasured here; the 28 issue codes and intent-vs-diff design target correctness, but no model run backs it. |
| Speed | neutral | Startup-to-failure was 3.9s; per-review latency with a model is unmeasured. |
| Maintainability | neutral | Not measured; the issue-code list includes refactoring/duplication classes. |
| Safety | + | Fails closed with exit 2 and a clear message when no credential is present; `hardcoded_secret` and `insecure_code` are among its codes (detection unmeasured). |
| Cost Efficiency | neutral | Free, AGPL-3.0, BYO-model with `--max-spend`; model spend per review unmeasured. |
| Verifiability | + | Output is machine-formattable (`--output-format`, `--output-fields`) and issues carry a code and confidence threshold, so a human can check each finding; accuracy of findings is unverified. |

## Verdict

**discovery-log — tentative read** — Installs and runs cleanly and fails fast with a clear message when no model credential exists, but its actual job (flagging the planted off-by-one and unclosed handle, and checking goal adherence) was never exercised for lack of a key or logged-in agent CLI, so there is no detection evidence either way. A human with an API key or an agent subscription should rerun the fixture above (`vet "fix average" --repo /tmp/eval-vet/fx`, or with `--agentic`) and score findings against the two planted defects before any promotion; AGPL-3.0 and the near-peers code-review/pr-review-toolkit are the other open points.

Compared to neighbors: **code-review**/**pr-review-toolkit** review the diff across dimensions; **brooks-lint** reviews for design decay. Vet's distinguishing pitch is **verifying coding-agent behavior (goal adherence) alongside code correctness, runnable as a terminal/CI/skill, BYO-model.**

## Triage note

Re-examined 2026-10-16 by the P0 measure lane (`eval-runner` routine): upgraded from a README review to a RUN of the install and credential-free CLI surface. Left at `discovery-log`; no verdict authority was exercised.

_Triaged 2026-10-16 by the P0 measure band (unattended eval-runner pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [vet](https://github.com/imbue-ai/vet) | tool | Standalone verification for code changes AND coding-agent behavior (Imbue, AGPL-3.0) — checks agent conversations for goal adherence and diffs for correctness; runs from the terminal, as an agent skill (auto-runs after changes), or in CI; BYO-model | Agents drift from the user's request and ship subtly wrong code; want an independent verifier of both intent-adherence and correctness | code-review, pr-review-toolkit, brooks-lint |
