// opencode commit-gate plugin (#153, parent #144).
//
// Re-implements the Claude Code `.claude/hooks/audit-gate.sh` PreToolUse(Bash) hook
// in opencode-native form. Before the `bash` tool runs, if the command is a
// `git commit`, run the repo's offline data gates (`make check-data`). On non-zero
// exit, BLOCK the commit by rewriting the command to a diagnostic echo so the agent
// reads the failure and fixes the tree instead of retrying. Fail-open and no-op for
// any command that is not a commit, and fail-open if the gate itself can't run —
// exactly mirroring audit-gate.sh's contract.
//
// Same target, no gate drift: this calls the identical `make check-data` that Claude
// Code's hook and CI (`make check`) call, so local opencode / local Claude Code / CI
// all reference one implementation. It used to run `python3 audit-evals.py --offline`
// alone — 1 of the 13 gates in that set — while this comment called it "the offline
// subset of `make check`" (#459); every gate added since then widened the hole
// silently, because nothing coupled the hook's list to the Makefile's.
//
// **"Could not run" is not "failed."** The preconditions are probed explicitly — make,
// python3, the target — and any one of them missing returns without blocking. Exit
// codes cannot carry that distinction (make exits non-zero for a missing target and
// for a real finding alike), so it is decided BEFORE the run, never inferred from it.

import type { Plugin } from "@opencode-ai/plugin"

// The one commit predicate — pinned in lockstep with .claude/hooks/audit-gate.sh's
// `case *"git commit"*` by TestHookTriggerSeam in test_automation.py (#202). Keep it
// metacharacter-free so the regex test stays a plain substring match, same as bash's.
const COMMIT_RE = /git commit/
const DIAG_TRUNC = 4000

export default (async ({ worktree, $ }) => {
  return {
    "tool.execute.before": async (input, output) => {
      // Only the bash tool carries a `command` string arg. Identifying by the arg
      // shape (not just the tool name) keeps this robust to tool-id casing.
      const toolIsBash = /bash/i.test(input.tool ?? "")
      const command: string = output.args?.command
      if (!toolIsBash || typeof command !== "string") return

      // Fail-open: only gate commit invocations; everything else passes through.
      if (!COMMIT_RE.test(command)) return

      try {
        // The same three preconditions audit-gate.sh checks, in the same order.
        const probe = await $.nothrow().cwd(worktree)`sh -c 'command -v make >/dev/null 2>&1 && command -v python3 >/dev/null 2>&1 && grep -q "^check-data:" Makefile'`
        if (probe.exitCode !== 0) return // cannot run → never block

        const result = await $.nothrow().cwd(worktree)`make --no-print-directory check-data`
        if (result.exitCode === 0) return // gates clean → allow the commit unchanged

        const diag =
          (result.stderr?.toString("utf8") || "") ||
          (result.stdout?.toString("utf8") || "")
        const trimmed = diag.slice(0, DIAG_TRUNC)
        // base64-encode so the gate output (multi-line, quotes) survives the shell
        // round-trip intact. Decode with python3 (already a dependency of the gates).
        const b64 = Buffer.from(trimmed, "utf8").toString("base64")
        output.args.command =
          "echo \"BLOCKED by opencode commit-gate: 'make check-data' failed before 'git commit' — fix the tree, then re-run the commit.\" ; " +
          "python3 -c \"import base64,sys;sys.stdout.write(base64.b64decode('" +
          b64 +
          "').decode(errors='replace'))\""
      } catch {
        // Fail-open: if the gate itself can't run, never block. Mirror audit-gate.sh.
      }
    },
  }
}) satisfies Plugin
