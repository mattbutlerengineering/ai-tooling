// opencode auto-sync plugin (#154, parent #144).
//
// Re-implements the Claude Code `.claude/hooks/auto-sync.sh` PostToolUse(Edit|Write)
// hook in opencode-native form. After the `edit` or `write` tool runs, if the edited
// file path is a root doc that sync-plugin-docs.sh mirrors (CATALOG.md /
// WORKFLOW.md / STACK.md / evaluations/*.md) and is NOT already inside
// plugin/docs/, re-run ./sync-plugin-docs.sh so plugin/docs/ never drifts during a
// session. Fail-open and silent — mirror auto-sync.sh's contract.
//
// Same script, no gate drift: calls the identical sync-plugin-docs.sh that Claude
// Code's hook and CI (make check) call.

import type { Plugin } from "@opencode-ai/plugin"

// Root docs that sync-plugin-docs.sh mirrors from the repo root into plugin/docs/.
const ROOT_DOC_BASENAMES = new Set(["CATALOG.md", "WORKFLOW.md", "STACK.md"])

function pathFromArgs(args: any): string {
  if (!args) return ""
  if (typeof args === "string") return args
  // opencode edit/write arg shapes aren't in the plugin SDK types, so read the
  // path defensively from any common key, then fall back to scanning the JSON.
  for (const k of ["file_path", "filePath", "path", "file"]) {
    const v = args[k]
    if (typeof v === "string") return v
  }
  try {
    const s = JSON.stringify(args)
    for (const b of ROOT_DOC_BASENAMES) {
      const i = s.indexOf(b)
      if (i >= 0) return s.slice(Math.max(0, s.lastIndexOf('"', i) + 1), i + b.length)
    }
    const m = s.match(/evaluations[\/\\][^"'\s\\]+\.md/)
    if (m) return m[0]
  } catch {
    /* fall through */
  }
  return ""
}

// True if the path is a root doc that should trigger a re-sync.
function isSyncableRootDoc(fp: string): boolean {
  if (!fp) return false
  const norm = fp.replace(/\\/g, "/")
  // Edits already inside the derived plugin/docs/ copy would loop / double-sync — skip.
  if (norm.includes("/plugin/docs/")) return false
  const base = norm.slice(norm.lastIndexOf("/") + 1)
  if (ROOT_DOC_BASENAMES.has(base)) return true
  // evaluations/<name>.md under the repo root (not under plugin/docs/, checked above)
  if (/\/evaluations\/[^/]+\.md$/.test(norm)) return true
  return false
}

export default (async ({ worktree, $ }) => {
  return {
    "tool.execute.after": async (input, output) => {
      const tool = (input.tool ?? "").toLowerCase()
      if (tool !== "edit" && tool !== "write") return

      const fp = pathFromArgs(input.args)
      if (!isSyncableRootDoc(fp)) return

      try {
        // Re-sync the derived plugin/docs/ copy. Fail-open and silent: any error is
        // swallowed so the session never breaks. Closes the drift loop in-session.
        await $.nothrow().cwd(worktree)`./sync-plugin-docs.sh`
        // Leave a benign trace for observability without surfacing to the agent.
        output.metadata = { ...(output.metadata ?? {}), opencodeAutoSynced: fp }
      } catch {
        // Fail-open: never break the session if the sync script can't run.
      }
    },
  }
}) satisfies Plugin