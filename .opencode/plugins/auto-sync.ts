// opencode auto-sync plugin (#154, parent #144).
//
// Re-implements the Claude Code `.claude/hooks/auto-sync.sh` PostToolUse(Edit|Write)
// hook in opencode-native form. After the `edit` or `write` tool runs, if the edited
// file path is a root doc that sync-plugin-docs.sh mirrors and is NOT already inside
// plugin/docs/, re-run ./sync-plugin-docs.sh so plugin/docs/ never drifts during a
// session. Fail-open and silent — mirror auto-sync.sh's contract.
//
// Same script, no gate drift: calls the identical sync-plugin-docs.sh that Claude
// Code's hook and CI (make check) call. The trigger set is DERIVED from
// `sync-plugin-docs.sh --list-watched` — the one definition of the syncable set —
// never restated here (#194, pinned by TestWatchListSeam in test_automation.py).

import type { Plugin } from "@opencode-ai/plugin"

// The watch set as emitted by --list-watched: root-file basenames plus
// directories whose contents are mirrored (trailing "/" in the emitted form).
interface WatchList {
  files: Set<string>
  dirs: string[]
}

function parseWatchList(text: string): WatchList {
  const files = new Set<string>()
  const dirs: string[] = []
  for (const raw of text.split("\n")) {
    const line = raw.trim()
    if (!line) continue
    if (line.endsWith("/")) dirs.push(line.slice(0, -1))
    else files.add(line)
  }
  return { files, dirs }
}

function pathFromArgs(args: any, watched: WatchList): string {
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
    for (const b of watched.files) {
      const i = s.indexOf(b)
      if (i >= 0) return s.slice(Math.max(0, s.lastIndexOf('"', i) + 1), i + b.length)
    }
    for (const d of watched.dirs) {
      const m = s.match(new RegExp(`${d}[\\/\\\\][^"'\\s\\\\]+\\.md`))
      if (m) return m[0]
    }
  } catch {
    /* fall through */
  }
  return ""
}

// True if the path is a watched root doc that should trigger a re-sync.
function isSyncableRootDoc(fp: string, watched: WatchList): boolean {
  if (!fp) return false
  const norm = fp.replace(/\\/g, "/")
  // Edits already inside the derived plugin/docs/ copy would loop / double-sync — skip.
  if (norm.includes("/plugin/docs/")) return false
  const base = norm.slice(norm.lastIndexOf("/") + 1)
  if (watched.files.has(base)) return true
  // any file under a watched directory (not under plugin/docs/, checked above)
  return watched.dirs.some((d) => norm.includes(`/${d}/`) || norm.startsWith(`${d}/`))
}

export default (async ({ worktree, $ }) => {
  // Derived once per session, on first edit; cached only on success so a
  // transient failure doesn't disable auto-sync for the whole session.
  let watched: WatchList | null = null
  const loadWatchList = async (): Promise<WatchList> => {
    if (watched) return watched
    try {
      const r = await $.nothrow().cwd(worktree)`./sync-plugin-docs.sh --list-watched`.quiet()
      if (r.exitCode === 0) {
        watched = parseWatchList(r.stdout.toString())
        return watched
      }
    } catch {
      /* fall through */
    }
    // Fail-open: an empty watch set means "never trigger", never break the session.
    return { files: new Set(), dirs: [] }
  }

  return {
    "tool.execute.after": async (input, output) => {
      const tool = (input.tool ?? "").toLowerCase()
      if (tool !== "edit" && tool !== "write") return

      const w = await loadWatchList()
      const fp = pathFromArgs(input.args, w)
      if (!isSyncableRootDoc(fp, w)) return

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
