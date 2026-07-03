// opencode commit-gate plugin (#153, parent #144).
//
// Re-implements the Claude Code `.claude/hooks/audit-gate.sh` PreToolUse(Bash) hook
// in opencode-native form. Before the `bash` tool runs, if the command is a
// `git commit`, run the offline integrity audit (`audit-evals.py --offline` — the
// offline subset of `make check`, no network). On non-zero exit, BLOCK the commit
// by rewriting the command to a diagnostic echo so the agent reads the failure and
// fixes the tree instead of retrying. Fail-open and no-op for any command that is
// not a commit, and fail-open if the audit itself can't run — exactly mirroring
// audit-gate.sh's contract.
//
// Same script, no gate drift: this calls the identical `audit-evals.py` that
// Claude Code's hook and CI (`make check`) call, so local opencode / local Claude
// Code / CI all reference one implementation.

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
        const result = await $.nothrow().cwd(worktree)`python3 audit-evals.py --offline`
        if (result.exitCode === 0) return // audit clean → allow the commit unchanged

        const diag =
          (result.stderr?.toString("utf8") || "") ||
          (result.stdout?.toString("utf8") || "")
        const trimmed = diag.slice(0, DIAG_TRUNC)
        // base64-encode so the audit output (multi-line, quotes) survives the shell
        // round-trip intact. Decode with python3 (already a dependency of the audit).
        const b64 = Buffer.from(trimmed, "utf8").toString("base64")
        output.args.command =
          "echo \"BLOCKED by opencode commit-gate: 'audit-evals.py --offline' failed before 'git commit' — fix the tree, then re-run the commit.\" ; " +
          "python3 -c \"import base64,sys;sys.stdout.write(base64.b64decode('" +
          b64 +
          "').decode(errors='replace'))\""
      } catch {
        // Fail-open: if the audit itself can't run, never block. Mirror audit-gate.sh.
      }
    },
  }
}) satisfies Plugin