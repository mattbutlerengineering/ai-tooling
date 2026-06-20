#!/usr/bin/env python3
"""
find-gaps.py — surface tools that probably belong in CATALOG.md but aren't there.

Two signals, both read-only (never edits the catalog):

  1. Detector F (audit-evals.py --overlaps): "Overlaps with" tokens naming a tool
     that has no entry of its own — referenced-but-not-catalogued.
  2. Foundational checklist: a curated list of heavyweight, in-scope tools whose
     peers are already catalogued. Their absence is the systemic blind spot that
     hid codex (92K), cline (63K), MetaGPT (69K) until this checklist was run.

A "present" check is `[name](` appearing in CATALOG.md (case-insensitive). Output is
a candidate list for human review — vet scope before adding (skip proprietary-only,
model-serving infra, chat UIs, general business automation).

  python3 .claude/skills/find-catalog-gaps/find-gaps.py
"""
import os, re, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

# Curated heavyweight, in-scope tools, grouped by where their peers live. Extend
# this as the ecosystem moves — it is a checklist, not an exhaustive index. Each
# value is the name(s) as they'd appear in a `[name](` link; first match = present.
CHECKLIST = {
    "coding agents":   ["aider", "cline", "continue", "codex", "Roo-Code", "void",
                        "opencode", "goose", "gpt-engineer", "SWE-agent", "kilocode",
                        "OpenHands", "gemini-cli", "qwen-code", "tabby"],
    "frameworks":      ["langchain", "llama_index", "autogen", "crewAI", "LangGraph",
                        "semantic-kernel", "dspy", "smolagents", "MetaGPT", "haystack",
                        "pydantic-ai"],
    "eval/observ":     ["promptfoo", "deepeval", "ragas", "langfuse", "phoenix",
                        "Helicone", "openinference", "logfire", "opik", "weave"],
    "memory/context":  ["mem0", "letta", "claude-mem", "cognee", "repomix", "gitingest",
                        "context7", "serena", "markitdown"],
}

def catalog_text():
    return open(os.path.join(ROOT, "CATALOG.md"), encoding="utf-8").read().lower()

def present(name, cat):
    return f"[{name.lower()}](" in cat

def run_detector_f():
    try:
        out = subprocess.run([sys.executable, "audit-evals.py", "--overlaps"],
                             cwd=ROOT, capture_output=True, text=True, timeout=60).stdout
    except Exception as e:
        return f"  (could not run detector F: {e})"
    return "\n".join(l for l in out.splitlines() if l.strip().startswith(("GAP?", "maybe")))

def main():
    cat = catalog_text()
    print("== F. referenced-but-not-catalogued (detector F) ==")
    print(run_detector_f() or "  (none)")
    print("\n== foundational checklist — missing heavyweight tools ==")
    any_missing = False
    for group, names in CHECKLIST.items():
        missing = [n for n in names if not present(n, cat)]
        if missing:
            any_missing = True
            print(f"  {group}:")
            for n in missing:
                print(f"    MISSING  {n}  (peers are catalogued — vet scope, then add)")
    if not any_missing:
        print("  OK — every checklist tool has a catalog entry")
    print("\nVet each candidate's scope before adding; use /add-catalog-entry to add.")

if __name__ == "__main__":
    main()
