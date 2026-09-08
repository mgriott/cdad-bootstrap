#!/usr/bin/env python3
"""
CDAD drift detector - control plane, advisory.

PostToolUse on write-class tools. Compares the written path against the
cdad-drift-signals block declared in cdad/context/stack.md.

Governed regime only: pre-freeze there is nothing ratified to contradict.
Never blocks - L3 is free by design. Warns once per category per session.
"""
import fnmatch
import json
import os
import re
import sys
import tempfile
from pathlib import Path

REPO = Path.cwd()
FROZEN = REPO / "cdad" / ".frozen"
STACK = REPO / "cdad" / "context" / "stack.md"
BLOCK = re.compile(r"```cdad-drift-signals\s*\n(.*?)```", re.S)
GOVERNED_PREFIXES = ("cdad/context/", "cdad/adr/")


def ok():
    sys.exit(0)


def seen_file(session_id):
    """Session-scoped, in the OS temp dir. Dies with the session, by design.

    Keying this on the session is the whole point: a repo-lifetime file would
    go silent after the first hit per category and never speak again.
    """
    safe = re.sub(r"[^A-Za-z0-9_.-]", "_", session_id or "nosession")
    return Path(tempfile.gettempdir()) / f"cdad-drift-{safe}"


def load_signals():
    if not STACK.exists():
        return {}
    match = BLOCK.search(STACK.read_text(encoding="utf-8"))
    if not match:
        return {}
    signals = {}
    for line in match.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, raw = line.split(":", 1)
        globs = [g.strip() for g in raw.split(",") if g.strip()]
        if globs:
            signals[key.strip()] = globs
    return signals


def matches(rel, globs):
    for pattern in globs:
        if fnmatch.fnmatch(rel, pattern):
            return True
        # ** should span directories; fnmatch does not do that natively
        if pattern.startswith("**/") and fnmatch.fnmatch(rel, pattern[3:]):
            return True
        if pattern.endswith("/**") and rel.startswith(pattern[:-3] + "/"):
            return True
        if "/" not in pattern and fnmatch.fnmatch(Path(rel).name, pattern):
            return True
    return False


def main():
    if not FROZEN.exists():
        ok()

    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        ok()

    ti = event.get("tool_input") or {}
    raw = ti.get("file_path") or ti.get("path") or ti.get("notebook_path")
    if not raw:
        ok()

    try:
        rel = str(Path(raw).resolve().relative_to(REPO.resolve())).replace("\\", "/")
    except (ValueError, OSError):
        ok()

    # Governed paths are protect-l0.py's job; it already denied them.
    if rel.startswith(GOVERNED_PREFIXES):
        ok()

    signals = load_signals()
    hits = [k for k, globs in signals.items() if matches(rel, globs)]
    if not hits:
        ok()

    seen = seen_file(event.get("session_id", ""))
    already = set()
    if seen.exists():
        try:
            already = {ln.strip() for ln in seen.read_text(encoding="utf-8").splitlines()}
        except OSError:
            pass
    fresh = [h for h in hits if h not in already]
    if not fresh:
        ok()

    try:
        with seen.open("a", encoding="utf-8") as fh:
            for h in fresh:
                fh.write(h + "\n")
    except OSError:
        pass

    sys.stderr.write(
        "CDAD DRIFT SIGNAL\n"
        f"  file:     {rel}\n"
        f"  category: {', '.join(fresh)}\n"
        "\n"
        "This path is declared in cdad/context/stack.md as architecture-bearing.\n"
        "The write succeeded. What may now be stale is the ratified context.\n"
        "\n"
        "Before continuing, invoke the cdad-drift-response skill: check whether\n"
        "this change contradicts L0, and if it does, draft a proposal under\n"
        "cdad/proposals/ and emit the ratification commands. Do not run them.\n"
        "Do not edit cdad/context/ or cdad/adr/.\n"
    )
    sys.exit(2)


if __name__ == "__main__":
    main()
