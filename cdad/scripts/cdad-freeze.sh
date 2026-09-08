#!/usr/bin/env bash
# CDAD - freeze. The act of ratification.
#
# Run by the Solution Designer, never by an agent. Validates that L0 holds
# real content, then writes the marker that switches the project from the
# pre-freeze regime to the governed regime.
#
# Exit 0 = frozen, 1 = validation failed, 2 = already frozen.

set -euo pipefail

MARKER="cdad/.frozen"
CTX="cdad/context"
REQUIRED=(stack.md architecture.md solution-vision.md principles.md constraints.md glossary.md)

if [ -f "$MARKER" ]; then
  echo "cdad-freeze: already frozen ($MARKER exists, written $(cat "$MARKER" | head -1))." >&2
  echo "             Freeze is not idempotent by accident. Nothing to do." >&2
  exit 2
fi

fail=0
for f in "${REQUIRED[@]}"; do
  path="$CTX/$f"
  if [ ! -f "$path" ]; then
    echo "cdad-freeze: missing $path" >&2
    fail=1
    continue
  fi
  lines="$(grep -cve '^\s*$' "$path" || true)"
  if [ "$lines" -le 5 ]; then
    echo "cdad-freeze: $path has $lines non-empty lines - still effectively empty" >&2
    fail=1
  fi
  if grep -qE 'TODO|PLACEHOLDER|REPLACE ME|<[a-z][^>]*>' "$path"; then
    echo "cdad-freeze: $path still contains template placeholders" >&2
    fail=1
  fi
done

if ! ls cdad/adr/ADR-001*.md >/dev/null 2>&1; then
  echo "cdad-freeze: ADR-001 not found under cdad/adr/" >&2
  fail=1
fi

if [ "$fail" -ne 0 ]; then
  cat >&2 <<'MSG'

cdad-freeze: FAILED

Freezing is a ratification, not a file move. Context that is still template
text would be ratified as if it were a decision. Fill in the files above, or
run the cdad-bootstrap skill, then try again.
MSG
  exit 1
fi

{
  date -u +"%Y-%m-%dT%H:%M:%SZ"
  echo "Frozen by: ${USER:-unknown}"
} > "$MARKER"

if [ -d "cdad/proposals/bootstrap" ]; then
  rm -rf cdad/proposals/bootstrap
  echo "cdad-freeze: removed cdad/proposals/bootstrap (superseded by ratified context)."
fi

cat <<'MSG'
cdad-freeze: DONE

cdad/context/ and cdad/adr/ are now read-only for agents. From here, changes
go through CHANGE-REQUEST.md -> cdad/proposals/ -> you apply.

Commit cdad/.frozen. It is versioned on purpose: a clone of a frozen project
stays frozen.
MSG
