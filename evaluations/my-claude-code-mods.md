# Evaluation: my-claude-code-mods

**Repo:** [YeonwooSung/my-claude-code-mods](https://github.com/YeonwooSung/my-claude-code-mods)
**Stars:** 815 | **Last updated:** 2026-10-14 (pushed) | **License:** NONE
**Last verified:** 2026-10-15
**Last triaged:** 2026-10-15  <!-- triaged: bulk -->
**Dev loop stage:** Skills & Plugins (Claude Code mods)
**Layer:** Tooling (hook-based Claude Code customizations, installed as plugins)

---

## What it does

A personal collection of six Claude Code "mods" — hook-based customizations installed
individually as `plugin@marketplace`: an agent profiler, a context-window-waste
inspector, branching file-snapshot "time machine," a repeated-failure detector, pinned
memos/todos, a model/effort-band display, and a local runner for request failures.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG.md one-liner. That is sufficient for the verdict
below, because the verdict turns on *license*, not on the mods' behavior — a question
the repo's own LICENSE page (none present) answers directly. It would not be
sufficient to support an ADOPT, and this eval does not offer one.

## Verdict

**SKIP** — no declared license. Each mod here is a plugin installed as
`plugin@marketplace`, which copies its hook/skill text into the consuming repo; a
vendored artifact with no license grants nothing to copy in. `CLAUDE.md`'s license
bar requires permissive, MIT-like OSS for anything vendored, and GitHub's repo page
shows no LICENSE file. Two existing catalog rows (`claude-code-mods (karanb192)`,
`claude-code-mods (hamzafer)`) already cover the same "Claude Mods" niche under MIT,
so there is no gap here worth re-checking for a license fix.

_Triaged 2026-10-15 by the P4 mechanical-skip band. Zero judgement: the license and
the vendored Type are the reason._
