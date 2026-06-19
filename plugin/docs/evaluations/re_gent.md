# Evaluation: re_gent

**Repo:** [regent-vcs/re_gent](https://github.com/regent-vcs/re_gent)
**Stars:** 744 | **Last updated:** 2026-06-13 | **License:** Apache-2.0
**Dev loop stage:** Implement (audit trail of agent edits) — also Reflect (after-the-fact provenance/debugging)
**Layer:** Tooling

---

## What it does

Version control *for AI coding agents* — a separate audit-trail layer that records what an agent did, which prompt produced each line, and the conversation context behind any change. It is not a replacement for git; it sits alongside it.

The mechanism: `rgt init` creates a `.regent/` directory (deliberately modeled on `.git/`) and auto-configures hooks for Claude Code, Codex, and OpenCode. From then on, every tool-using agent turn fires a hook that captures a **Step** — a content-addressed (BLAKE3) snapshot of the workspace tree plus the *cause* of the change (`tool_name`, args, result), the `session_id`, timestamp, and the surrounding conversation. Steps chain into a per-session DAG (each agent session is its own ref/branch; common ancestors dedupe), stored as content-addressed blobs in `.regent/objects/` with a SQLite index (`.regent/index.db`) for sub-10ms queries. You then inspect it with git-flavored commands: `rgt log` (history, filterable by session), `rgt blame src/file.go:42` (per-line provenance back to the prompt that wrote it), `rgt show <step>` (full tool call + conversation for one step), `rgt sessions`, `rgt status`, `rgt cat <hash>`. A key feature is that the captured conversation **survives `/compact` and `/clear`**, so the provenance outlives the agent's own context window. There is also a companion VSCode extension for inline blame annotations and a session timeline.

## How we tested it

Inspected the GitHub repo metadata, full README, file tree, release history, and contributor count. Did not install or run `rgt` in this environment. This is a repo/README/source-structure review, not hands-on usage — no timing, dedup ratio, or correctness numbers are claimed (the "sub-10ms" figure is the project's own).

```bash
gh api repos/regent-vcs/re_gent --jq '{stars,license,description,pushed_at,created_at,language,forks,open_issues}'
gh api repos/regent-vcs/re_gent/readme --jq '.content' | base64 -d
gh api "repos/regent-vcs/re_gent/git/trees/main?recursive=0" --jq '.tree[].path'
gh api repos/regent-vcs/re_gent/contributors --jq 'length'
gh api repos/regent-vcs/re_gent/releases --jq '.[0:5] | .[] | {tag: .tag_name, date: .published_at}'
# Catalog overlap check (worktrunk, dmux, version-control terms):
grep -inE "worktrunk|regent|checkpoint|rewind|provenance|blame|version control" /Users/mbutler/github/ai-tooling/CATALOG.md
```

What the source tree confirms beyond the README: a real Go codebase under `internal/` with separated concerns (`store/` content-addressed objects + refs + blame + transcript, `snapshot/`, `treediff/`, `diff/` Myers diff, `index/` SQLite, `hook/` + `jsonl/` for capturing agent transcripts, `conversation/` converter). Test files accompany nearly every package, plus a `test/` dir with `integration_test.go`, `phase1_acceptance_test.go`, and `session_branching_test.go`. Hook adapters exist for Codex, OpenCode, and `pi` (`cmd/rgt/*_hook.go`), and Claude Code skills (`blame`, `log`, `show`, `rewind`) ship under `.claude/skills/`. A worked example (`examples/bad-refactor/`) demonstrates tracing a billing regression.

## What worked

- **The problem is real and under-served.** Agents have write access to the codebase but no native, queryable record of *which prompt caused which line*. Git tracks code; it does not track agent intent, the conversation, or concurrent agent sessions. "It was working five minutes ago / why did you change that file / go back to before the refactor" is a genuine recurring pain, and `blame → prompt` provenance is a clean answer to it.
- **Sound, git-literate design.** Content-addressed BLAKE3 objects, refs, a DAG, ACID/CAS concurrency safety, and a SQLite query index is the right architecture — it mirrors git's proven model rather than inventing magic. The `.regent/` ↔ `.git/` mental model lowers the learning curve.
- **Genuinely engineered, not a prototype.** Go, Apache-2.0, v1.1.0 (five tagged releases since early May 2026), 6 contributors, per-package unit tests plus integration/acceptance/branching tests, GoReleaser + CI, Homebrew tap, a worked example, and a companion VSCode extension. This is well past the thin-README stage that warrants a reflexive SKIP.
- **Transparent, multi-agent capture.** Hook-driven and zero-config after `rgt init`; supports Claude Code, Codex, and OpenCode, with concurrent sessions tracked as separate refs. Conversation capture survives `/compact` and `/clear` — addressing the exact moment provenance is normally lost.
- **Complements rather than competes with git and worktrunk.** It explicitly positions as additive ("use both"), and occupies a different niche from worktree tools (isolation/parallelism) — re_gent is about *provenance and audit*, not branch management.

## What didn't work or surprised us

- **Not validated hands-on here.** Everything above is from the README and source tree. The sub-10ms query claim, dedup behavior, and hook reliability under real concurrent sessions were not observed in this environment.
- **A second metadata store to maintain.** `.regent/` is a parallel object database alongside `.git/`. GC and integrity verification are still on the roadmap, so on a busy repo the object store can grow unbounded today — a real operational cost for a benefit (deep per-line agent provenance) that not every team will exercise.
- **Rewind is not shipped where it matters most.** A `rewind` skill exists under `.claude/skills/`, but the README lists "non-destructive rewind and fork" as *roadmap*, and the documented CLI commands are read-only (log/blame/show/cat/sessions/status). So the catalog one-liner's "manage agent-generated changes" overstates today's capability — it currently *tracks and inspects*, it does not yet *manage* (revert/fork) them via stable CLI.
- **Value scales with team/audit needs, not solo speed.** For a solo dev who already reads diffs and trusts their agent, the marginal benefit over `git diff` + the agent transcript is modest. The payoff concentrates where multiple agents/sessions touch a codebase, or where you must later answer "why did this line change."
- **Young project risk.** 744 stars, 6 contributors, ~6 weeks old at evaluation. Healthy trajectory, but the format and hooks could still churn; betting a team audit workflow on it carries early-adopter risk.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Doesn't change what the agent writes; aids *diagnosing* bad changes after the fact (the bad-refactor example) but adds no verification gate |
| Speed | neutral/+ | Hook capture adds small per-turn overhead; speeds up *debugging* "what changed and why" via blame/show vs. reconstructing from memory |
| Maintainability | + | Per-line prompt provenance and durable conversation history make agent-authored code auditable and explainable long after the session ends |
| Safety | + | Tamper-evident, content-addressed audit trail of every agent tool call — answers "what did the agent touch?"; offsets some risk of giving agents write access |
| Cost Efficiency | neutral | Free/Apache-2.0, no token cost; storage cost of a second object DB grows until GC ships |

## Verdict

**CONDITIONAL**

Adopt re_gent when you need an **audit trail and per-line provenance for agent-authored code** — specifically: teams running one or more coding agents where "which prompt wrote this, and why" must be answerable later, or where you want a tamper-evident record of what agents touched (compliance, post-incident review, debugging bad refactors). It is a well-engineered, git-literate, hook-driven tool that fills a real gap git does not cover, and it is mature enough (v1.1.0, real tests, multi-agent hooks, VSCode extension) to take seriously. It is not a default for everyone: a solo dev who reads diffs and trusts their agent gets modest marginal value, the destructive "manage/rewind" half of the pitch is still roadmap, and a second growing object store without GC is a real operational caveat. Re-evaluate toward ADOPT-for-teams once rewind/fork and garbage collection ship and the format stabilizes. **KEEP** in the catalog — the existing entry is accurate; consider softening the one-liner from "manage" to "track and inspect" to match shipped capability.

**vs. worktrunk / dmux** (also in catalog): these are not competitors. worktrunk and dmux solve *isolation and parallelism* (git worktrees, a branch + working dir per agent so concurrent agents don't collide). re_gent solves *provenance and audit* (what each agent did, which prompt caused each line, the conversation behind it). You could run re_gent inside a worktrunk/dmux setup to get both isolation and an audit trail. The catalog's "complementary" framing is correct; the distinction is isolation-of-work (worktrunk/dmux) vs. record-of-work (re_gent).

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [re_gent](https://github.com/regent-vcs/re_gent) | tool | Version control for AI coding agents — track agent edits, per-line prompt provenance, and conversation history | Agent-generated code changes lack specialized version control, audit trail, and per-line prompt provenance | worktrunk, dmux (complementary: worktrunk/dmux = work isolation, re_gent = work provenance/audit) |
