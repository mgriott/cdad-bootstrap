#!/usr/bin/env python3
"""
CDAD L0 protection hook - control plane, PreToolUse.

Two regimes, discriminated by the cdad/.frozen marker:

  pre-freeze (marker absent) : cdad/context/, cdad/adr/ and SOURCE-BRIEF.*
                               are writable. Nothing is ratified yet.
  governed   (marker present): those paths are denied.

Machinery paths are denied in BOTH regimes, without exception: the agent may
never rewrite its own directives, its own enforcement, or the freeze marker.

Blocks direct write tools and shell mutations alike. Emits the
hookSpecificOutput JSON contract on stdout before exiting 2.
"""
import json
import re
import sys
from pathlib import Path

REPO = Path.cwd()
FROZEN = REPO / "cdad" / ".frozen"

# Denied in every regime. No exceptions, ever.
ALWAYS_PROTECTED = re.compile(
    r"(?:^|[/\\\s>;&|])("
    r"AGENTS\.md"
    r"|CHANGE-REQUEST\.md"
    r"|\.claude/settings\.json"
    r"|\.claude/settings\.local\.json"
    r"|\.claude/rules/"
    r"|\.claude/hooks/"
    r"|\.kiro/settings/"
    r"|\.kiro/steering/"
    r"|\.kiro/hooks/"
    r"|\.kiro/permissions\.yaml"
    r"|cdad/\.frozen"
    r")"
)

# Denied only under the governed regime.
GOVERNED = re.compile(
    r"(?:^|[/\\\s>;&|])("
    r"cdad/context/"
    r"|cdad/adr/"
    r"|SOURCE-BRIEF\."
    r")"
)

# Heuristic for "this file has real content", mirrored in cdad-freeze.sh.
PLACEHOLDER = re.compile(r"TODO|PLACEHOLDER|REPLACE ME|<rellenar>|<[a-z][^>]*>")

WRITE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}


def respond(decision, reason):
    """Emit the hookSpecificOutput contract Claude Code surfaces to the agent."""
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision,
            "permissionDecisionReason": reason,
        }
    }))
    sys.stderr.write(reason + "\n")
    sys.exit(2 if decision == "deny" else 0)


def ok():
    sys.exit(0)


def frozen():
    return FROZEN.exists()


def candidate_paths(event):
    """Every repo-relative path this tool call might mutate."""
    tool = event.get("tool_name", "")
    ti = event.get("tool_input") or {}
    found = []

    if tool in WRITE_TOOLS:
        for key in ("file_path", "path", "notebook_path"):
            if ti.get(key):
                found.append(str(ti[key]))
        for edit in ti.get("edits") or []:
            if isinstance(edit, dict) and edit.get("file_path"):
                found.append(str(edit["file_path"]))

    if tool == "Bash":
        # Coarse but sufficient: any protected path named anywhere in the
        # command line is treated as a mutation target. False positives are
        # acceptable here; a missed shell workaround is not.
        found.append(str(ti.get("command", "")))

    return found


def normalise(raw):
    try:
        return str(Path(raw).resolve().relative_to(REPO.resolve())).replace("\\", "/")
    except (ValueError, OSError):
        return raw.replace("\\", "/")


def looks_populated():
    ctx = REPO / "cdad" / "context"
    if not ctx.is_dir():
        return False
    for md in ctx.glob("*.md"):
        try:
            text = md.read_text(encoding="utf-8")
        except OSError:
            continue
        body = [ln for ln in text.splitlines() if ln.strip()]
        if len(body) > 5 and not PLACEHOLDER.search(text):
            return True
    return False


def main():
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        ok()

    targets = [normalise(t) for t in candidate_paths(event)]
    if not targets:
        ok()

    for target in targets:
        if ALWAYS_PROTECTED.search(target):
            respond("deny", (
                "CDAD: this path is governance machinery and is protected in "
                "every regime, including pre-freeze. An agent may not rewrite "
                "its own directives, its own enforcement, or the freeze marker. "
                "If it genuinely needs to change, write a proposal under "
                "cdad/proposals/ and stop."
            ))

    if frozen():
        for target in targets:
            if GOVERNED.search(target):
                respond("deny", (
                    "CDAD: this project is frozen (cdad/.frozen present). "
                    "cdad/context/, cdad/adr/ and SOURCE-BRIEF.* are ratified "
                    "context and are read-only for you. This block is the "
                    "system working - do not look for another way in. Write a "
                    "proposal to cdad/proposals/ and hand the Solution Designer "
                    "the commands to apply it."
                ))
        ok()

    # Pre-freeze. Writes are allowed, but warn if the context already looks
    # ratified - most likely a project bootstrapped before ADR-008 existed.
    for target in targets:
        if GOVERNED.search(target) and looks_populated():
            respond("allow", (
                "CDAD WARNING: cdad/context/ already looks populated, but "
                "cdad/.frozen is absent. If this project was governed before "
                "this version of CDAD, run cdad/scripts/cdad-freeze.sh now "
                "rather than treating it as a fresh bootstrap. The write is "
                "allowed; this is a warning, not a block."
            ))

    ok()


if __name__ == "__main__":
    main()
