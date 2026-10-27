# Evaluation: BeautifulRust

**Repo:** [morganlinton/BeautifulRust](https://github.com/morganlinton/BeautifulRust)
**Stars:** ~1,300 (approx., GitHub page display — gh API access to this repo was not available this session) | **Last updated:** 2026-10-27 (pushed) | **License:** MIT
**Last verified:** 2026-10-27
**Last triaged:** 2026-10-27  <!-- triaged: bulk -->
**Dev loop stage:** Implement / Review (Rust-specific)
**Layer:** Tooling (agent skill)

---

## What it does

Three Agent Skills (standard Agent Skills format — also works with Codex, Copilot,
Cursor, Gemini CLI, not just Claude Code) for writing, reviewing, and porting Rust:
`rust-best-practices` (applies while writing/changing Rust), `rust-review` (reviews a
file/crate/diff and produces a prioritized, rule-citing report), and `rust-port`
(ports C/C++/Python/Go/JS to idiomatic Rust, checking behavior against the original
tests). Ships alongside a separate clippy lint configuration enforced in CI.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata (via the public GitHub web page and a shallow git clone — this
session's GitHub API access does not cover unattached repositories) plus the README.
That is sufficient to place the lead, not to support an ADOPT, and none is offered
here.

## Triage note

Left at `discovery-log`. Cites `terraform-skill`, `azure-skills`, `guard-skills` in
"Overlaps with" — none a STACK pick, so this doesn't band P2 challenger. It's the
catalog's first Rust-specific review/port skill pack (no existing row targets Rust
the way `terraform-skill` targets Terraform), MIT-licensed, and includes a testable
claim (`rust-port`'s behavior-checked-against-original-tests porting flow) worth a
real hands-on look rather than a mechanical SKIP.

_Triaged 2026-10-27 by the P3 backlog band (newly catalogued same day)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [BeautifulRust](https://github.com/morganlinton/BeautifulRust) | skill | Rust-specific agent skills (MIT, ★1.3K) — write/review/port idiomatic Rust, plus a clippy lint config enforced in CI | Agents write non-idiomatic or subtly-wrong Rust with no authoritative, language-specific review discipline | terraform-skill, azure-skills, guard-skills |
