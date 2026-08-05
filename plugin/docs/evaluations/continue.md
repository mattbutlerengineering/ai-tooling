# Evaluation: continue

**Repo:** [continuedev/continue](https://github.com/continuedev/continue)
**Stars:** 34,771 | **Last updated:** 2026-07-10 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-08-03
**Last triaged:** 2026-08-05  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Open-source coding agent for IDEs + CLI — autocomplete, chat, inline edit, and agentic workflows in
VS Code/JetBrains plus a `cn` CLI, with custom models, rules, and a hub of shareable
assistants/MCP blocks.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (eca, aider, opencode, cline). That is sufficient to place
the lead, not to support an ADOPT — this eval offers none.

## Verdict

**SKIP — the project shipped a deliberate final release and closed the repository to writes.**

Read live on 2026-08-05, the README says so directly, under a **"Final 2.0.0 Release"** heading:

> _Note: The `continuedev/continue` repository is no longer actively maintained and is read-only for
> all users._
>
> We polished Continue and did a final 2.0.0 release of the VS Code extension, CLI, and JetBrains
> plugin. This included removing anonymous telemetry, pulling out authentication, squashing bugs,
> and more.

`archived` is `false` and `pushed_at` is the day of the scan, so neither the P1 archive check nor any
dormancy threshold would have found this. It took reading the banner (detector V, #351).

**This reverses the previous triage note on this file, which held Continue back for the P0/eval-runner
lane, and the reversal is deliberate.** That note was right that ★35K and a distinct IDE-plus-hub
story deserve more than a mechanical SKIP; it was written on 2026-08-03 with no signal that the
project had ended. The `plandex` precedent governs the disposition: a *coding agent* rots when model
APIs turn over, and plandex was SKIPped at 13 months of dormancy on exactly that reasoning. Continue
is further along than dormant — it is closed, with the maintainers stating there will be no further
releases. Sending it to the P0 lane now would spend a measured evaluation on a project that cannot
receive a fix.

A SKIP keeps the row (the `Flowise` precedent), so a reader looking for Continue still finds it, and
the final 2.0.0 artifacts remain installable. What changes is that the catalog stops implying it is a
maintained choice alongside `aider` / `opencode` / `cline` / `eca`, none of which carry that caveat.

★34.8K and Apache-2.0 at the end — a lifecycle call, not a quality judgement.

_Triaged 2026-08-05 by the detector-V maintenance sweep ([#360](https://github.com/mattbutlerengineering/ai-tooling/issues/360))._
